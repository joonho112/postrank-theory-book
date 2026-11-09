source("scripts/examples/_setup.R")
source("scripts/examples/_finite-input.R")
payload <- finite_payload()
jsonlite::write_json(payload, "evidence/software/common-fixture.json", auto_unbox = TRUE, pretty = TRUE)
pw <- postrank_pairwise(as_postrank_draws(payload))
bank <- list(W = c(Alder = 1L, Birch = 1L), AB = c(Alder = 1L, Birch = 2L),
  BA = c(Alder = 2L, Birch = 1L))
ev <- lapply(bank, function(g) postrank_evaluate(g, pw, c(priority = 1), .25))
risks <- vapply(ev, function(e) e$primary_risk, 0)
stopifnot(max(abs(risks - c(.25, .2, .8))) < 1e-12,
  ev$W$N == 0, is.na(ev$W$E_over_N))
problem <- postrank_problem(pw, c(priority = 1), .25, G_max = 2L)
fit <- postrank_solve(problem, backend = "highs", strategy = "label_mip",
  control = postrank_control(strategy = "label_mip", time_limit = 10,
    threads = 1L, seed = 701L, absolute_risk_gap = 1e-10))
stopifnot(fit$incumbent_validated, identical(get_grades(fit), bank$AB),
  abs(fit$evaluation$primary_risk - min(risks)) < 1e-12)
write_result(list(step = "7.15", status = "PASS", expected_risks = c(W = "1/4", AB = "1/5", BA = "4/5"),
  evaluated_risks = risks, tolerance = 1e-12, grades = as.list(get_grades(fit)),
  criterion_profile = get_profile(fit), solver_status = fit$status,
  objective = fit$objective, backend = fit$backend,
  scope = "All three coherent two-unit actions independently enumerated; floating HiGHS solution compared with literal expected values. No posterior calibration claim."),
  "results/software/common.json")
