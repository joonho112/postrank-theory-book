# Bounded independent scenario-constraint replay; no mathematical-programming solver.
args <- commandArgs(trailingOnly=TRUE)
root <- if(length(args)) normalizePath(args[1L],mustWork=TRUE) else normalizePath(getwd(),mustWork=TRUE)
for(f in c("input.R","input-summary.R","action.R","decision.R","evaluate-expected.R",
           "evaluate-joint.R","oracle.R","candidates.R","solve-candidates.R"))
  source(file.path(root,"R/profile",f))
source(file.path(root,"tests/profile/helper-input-fixtures.R"))
source(file.path(root,"tests/profile/helper-evaluator-fixtures.R"))
path <- file.path(root,"fixtures/p2-v1/saa-oracle-check.json")
fixture <- jsonlite::fromJSON(path,simplifyVector=FALSE)
checks <- 0L
check <- function(ok,label) { checks <<- checks+1L; if(!isTRUE(ok)) stop(label,call.=FALSE) }
grade_key <- function(g) paste(as.vector(g),collapse=",")
provenance <- function(x) list(construction_method="Full n<=3 ordered-column enumeration for bounded formulation check",
  source_input_hash=p2_hash(x$original_spec),source_ids="saa-oracle-check.json",construction_draw_ids=character(),
  source_artifact_hashes=character(),sample_adaptive=c(order=FALSE,seeds=FALSE,cut_positions=FALSE,configuration=FALSE),
  depends_on_y=FALSE,fixed_universe_claim=TRUE,fixed_universe_justification="All ordered columns enumerated before scenario evaluation",
  selection_validation_relationship="Exact check of supplied measure; no independent validation claim")
rows_table <- function(rows) if(!length(rows)) data.frame() else do.call(rbind,lapply(rows,as.data.frame,stringsAsFactors=FALSE))
case_results <- list(); action_total <- z_total <- 0L
for(case in fixture$cases) {
  n <- as.integer(case$n); D <- as.integer(case$D); S <- length(case$states)
  if(!n %in% 2:3 || !D %in% 1:2 || S<1L || S>3L) stop("Replay bounds: n=2..3, D=1..2, S=1..3",call.=FALSE)
  theta <- array(0,c(S,n,D))
  for(s in seq_len(S)) theta[s,,] <- matrix(unlist(case$states[[s]]),n,D,byrow=TRUE)
  spec <- p2_test_expected_spec(theta,if(is.null(case$masses)) NULL else unlist(case$masses),case$representation)
  spec$input_id <- case$id; input <- p2_validate_input(spec)
  masses <- if(case$representation=="exact_finite_law") p2_parse_rational(unlist(case$masses)) else gmp::as.bigq(rep(1L,S),S)
  scopes <- lapply(case$scopes,function(kind) {
    m <- matrix(1L,n,n); diag(m) <- 0L
    if(kind=="site1") { m[,] <- 0L; m[1,-1] <- 1L; m[-1,1] <- 1L }
    m
  })
  decision <- p2_validate_decision(input,weights=unlist(case$weights),tau=unlist(case$tau),scopes=scopes,
    joint=rows_table(case$joint),expected=rows_table(case$expected),alpha=case$alpha)
  banks <- setNames(lapply(seq_len(D),function(d) {
    columns <- p2_enumerate_columns(n,input$equality_classes[[d]])
    p2_build_domain_bank(input,input$domain_ids[d],seeds=lapply(seq_len(nrow(columns)),function(b) unname(columns[b,])),provenance=provenance(input))
  }),input$domain_ids)
  family <- p2_build_candidate_family(input,banks)
  H <- nrow(decision$joint); scope_ids <- names(scopes); M <- n*(n-1L)/2L
  # Independent counts: loop issued ordered directions and literal target values.
  pre <- lapply(seq_len(D),function(d) lapply(seq_len(banks[[d]]$column_count),function(b) {
    g <- banks[[d]]$columns[b,]; F <- matrix(0L,S,length(scopes),dimnames=list(NULL,scope_ids)); N <- setNames(integer(length(scopes)),scope_ids)
    Ffull <- integer(S); Nfull <- 0L
    for(i in seq_len(n-1L)) for(j in seq.int(i+1L,n)) if(g[i]!=g[j]) {
      err <- if(g[i]<g[j]) theta[,i,d]<=theta[,j,d] else theta[,j,d]<=theta[,i,d]
      Ffull <- Ffull+as.integer(err); Nfull <- Nfull+1L
      for(h in seq_along(scopes)) if(scopes[[h]][i,j]==1L) { F[,h] <- F[,h]+as.integer(err); N[h] <- N[h]+1L }
    }
    cost <- decision$weights_exact[d]*(sum(masses*Ffull)+decision$tau_exact[d]*(M-Nfull))/M
    list(F=F,N=N,Ffull=Ffull,Nfull=Nfull,cost=cost)
  }))
  # Exact, uniform-over-bank safe constants. Optional tighter state ranges are unnecessary.
  big_m <- big_floor <- vector("list",H)
  for(h in seq_len(H)) {
    d <- match(decision$joint$domain_id[h],input$domain_ids); scope <- decision$joint$scope_id[h]; t <- decision$joint_t_exact[h]
    Ns <- vapply(pre[[d]],function(p) unname(p$N[scope]),integer(1))
    big_m[[h]] <- (1-t)*max(Ns)
    big_floor[[h]] <- max(gmp::as.bigq(Ns)-gmp::as.bigq(as.character(floor(t*Ns))))
  }
  products <- as.matrix(expand.grid(lapply(family$column_counts,seq_len),KEEP.OUT.ATTRS=FALSE))
  zpatterns <- as.matrix(expand.grid(rep(list(0:1),S),KEEP.OUT.ATTRS=FALSE))
  records <- vector("list",nrow(products))
  for(aidx in seq_len(nrow(products))) {
    pick <- products[aidx,]; chosen <- lapply(seq_len(D),function(d) pre[[d]][[pick[d]]])
    G <- do.call(cbind,lapply(seq_len(D),function(d) banks[[d]]$columns[pick[d],]))
    F <- matrix(0L,S,H); N <- integer(H); e <- matrix(FALSE,S,H); floors <- vector("list",H)
    for(h in seq_len(H)) {
      d <- match(decision$joint$domain_id[h],input$domain_ids); scope <- decision$joint$scope_id[h]
      F[,h] <- chosen[[d]]$F[,scope]; N[h] <- chosen[[d]]$N[scope]
      floors[[h]] <- floor(decision$joint_t_exact[h]*N[h])
      e[,h] <- as.logical(gmp::as.bigq(F[,h])>decision$joint_t_exact[h]*N[h])
      check(identical(e[,h],as.logical(gmp::as.bigz(F[,h])>=gmp::as.bigz(as.character(floors[[h]]))+1L)),paste(case$id,"integer cutoff"))
    }
    union <- if(H) rowSums(e)>0L else rep(FALSE,S)
    J <- sum(masses*as.integer(union))
    constraints_feasible <- bigm_feasible <- floor_feasible <- logical(nrow(zpatterns))
    for(zidx in seq_len(nrow(zpatterns))) {
      z <- zpatterns[zidx,]; budget <- sum(masses*z)<=decision$alpha_exact
      pass <- bm <- fl <- TRUE
      for(h in seq_len(H)) {
        pass <- pass && all(z>=as.integer(e[,h]))
        bm <- bm && all(gmp::as.bigq(F[,h])-decision$joint_t_exact[h]*N[h]<=big_m[[h]]*z)
        fl <- fl && all(gmp::as.bigq(F[,h])-gmp::as.bigq(as.character(floors[[h]]))<=big_floor[[h]]*z)
      }
      constraints_feasible[zidx] <- budget && pass
      bigm_feasible[zidx] <- budget && bm
      floor_feasible[zidx] <- budget && fl
      check(identical(pass,bm) && identical(pass,fl),paste(case$id,"same selected-column constraints for each z"))
    }
    tail_ok <- as.logical(J<=decision$alpha_exact)
    check(identical(any(constraints_feasible),tail_ok),paste(case$id,"existential common-z equivalence"))
    check(identical(constraints_feasible,bigm_feasible) && identical(constraints_feasible,floor_feasible),paste(case$id,"safe big-M encodings"))
    mean_ok <- TRUE
    for(h in seq_len(nrow(decision$expected))) {
      d <- match(decision$expected$domain_id[h],input$domain_ids); scope <- decision$expected$scope_id[h]
      mean_ok <- mean_ok && (sum(masses*chosen[[d]]$F[,scope])<=decision$expected_q_exact[h]*chosen[[d]]$N[scope])
    }
    risk <- sum(do.call(c,lapply(chosen,function(p) p$cost)))
    utility <- sum(vapply(chosen,function(p) p$Nfull,integer(1)))
    records[[aidx]] <- list(key=grade_key(G),risk=as.character(risk),J=as.character(J),utility=utility,
      mean_feasible=mean_ok,tail_feasible=tail_ok,feasible=mean_ok && tail_ok,
      feasible_z_count=sum(constraints_feasible),minimal_z=as.integer(union),N=N)
  }
  keys <- vapply(records,`[[`,character(1),"key")
  feasible <- vapply(records,`[[`,logical(1),"feasible")
  optimizer_checks <- list()
  for(objective in c("A","B")) {
    solver <- p2_solve_candidates(input,family,decision,objective=objective)
    oracle <- p2_oracle(input,decision,objective=objective)
    for(ref in list(solver,oracle)) {
      table <- ref$candidate_table
      reference_keys <- vapply(ref$actions,grade_key,character(1)); at <- match(reference_keys,keys)
      check(!anyNA(at) && length(at)==length(keys),paste(case$id,"every product present"))
      check(identical(unname(table$risk_exact),vapply(records[at],`[[`,character(1),"risk")),paste(case$id,"risk agreement"))
      check(identical(unname(table$J_exact),vapply(records[at],`[[`,character(1),"J")),paste(case$id,"joint probability agreement"))
      check(identical(table$feasible_for_represented_measure,feasible[at]),paste(case$id,"complete feasibility set agreement"))
      scores <- if(objective=="A") p2_parse_rational(vapply(records,`[[`,character(1),"risk")) else gmp::as.bigq(vapply(records,`[[`,integer(1),"utility"))
      best <- if(objective=="A") min(scores[feasible]) else max(scores[feasible])
      opt <- keys[feasible & as.logical(scores==best)]
      reference_opt <- unname(vapply(ref$actions[ref$optimizer_ids],grade_key,character(1)))
      check(setequal(opt,reference_opt),paste(case$id,"complete optimizer set agreement",objective))
      check(!ref$receipts$numerical_guarantee,paste(case$id,"no numerical certificate"))
    }
    optimizer_checks[[objective]] <- list(independent=sort(opt),
      candidate_solver=sort(unname(vapply(solver$actions[solver$optimizer_ids],grade_key,character(1)))),
      full_small_oracle=sort(unname(vapply(oracle$actions[oracle$optimizer_ids],grade_key,character(1)))))
  }
  action_total <- action_total+nrow(products); z_total <- z_total+nrow(products)*nrow(zpatterns)
  case_results[[case$id]] <- list(status="PASS",representation=case$representation,scenario_count=S,
    bank_counts=unname(family$column_counts),product_count=nrow(products),z_patterns_per_product=nrow(zpatterns),
    protected_event_count=H,big_m=as.character(do.call(c,big_m)),integer_big_m=as.character(do.call(c,big_floor)),
    optimizer_sets=optimizer_checks,all_product_records=records)
}
files <- c("scripts/p2_check_saa.R",paste0("R/profile/",c("input.R","input-summary.R","action.R","decision.R","evaluate-expected.R","evaluate-joint.R","oracle.R","candidates.R","solve-candidates.R")),"tests/profile/helper-input-fixtures.R","tests/profile/helper-evaluator-fixtures.R")
fixture$replay <- list(status="PASS",checked_at_utc=format(Sys.time(),tz="UTC",usetz=TRUE),
  assertions=checks,case_count=length(case_results),product_count=action_total,selected_action_z_assignments=z_total,
  mip_solver_invoked=FALSE,empirical_posterior_certificate=FALSE,R=R.version.string,
  command="Rscript scripts/p2_check_saa.R",source_sha256=setNames(lapply(file.path(root,files),digest::digest,file=TRUE,algo="sha256"),files),
  cases=case_results)
jsonlite::write_json(fixture,path,pretty=TRUE,auto_unbox=TRUE,null="null",digits=NA)
cat(jsonlite::toJSON(fixture$replay[c("status","assertions","case_count","product_count","selected_action_z_assignments","mip_solver_invoked")],auto_unbox=TRUE,pretty=TRUE),"\n")
