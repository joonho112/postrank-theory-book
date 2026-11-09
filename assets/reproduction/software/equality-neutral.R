source("scripts/examples/_setup.R")
source("scripts/examples/_finite-input.R")
payload <- neutral_payload(TRUE)
jsonlite::write_json(payload, "evidence/software/neutral-fixture.json", auto_unbox = TRUE, pretty = TRUE)
pw <- postrank_tie_pairwise(as_postrank_tie_draws(payload))
bank <- list(W = c(Alder = 1L, Birch = 1L), AB = c(Alder = 1L, Birch = 2L), BA = c(Alder = 2L, Birch = 1L))
ev <- lapply(bank, function(g) postrank_tie_evaluate(g, pw, c(priority = 1), .25))
risks <- vapply(ev, function(e) e$primary_risk, 0)
stopifnot(max(abs(risks - c(.125, 0, .5))) < 1e-12, ev$W$R0 == .125,
  is.na(ev$W$E_over_N), is.na(ev$W$E_over_D))
p <- postrank_tie_problem(pw, c(priority = 1), .25, G_max = 2L)
fit <- postrank_tie_solve(p, backend = "highs", control = postrank_control(
  strategy = "label_mip", time_limit = 10, threads = 1L, seed = 701L, absolute_risk_gap = 1e-10))
stopifnot(fit$incumbent_validated, identical(fit$grade, bank$AB), abs(fit$evaluation$primary_risk) < 1e-12)
# The ordinary input route excludes positive latent ties. Score the SAME law
# with the weak-error multidomain evaluator, using one domain and no joint guard.
x <- array(c(1, 0, 0, 0), c(2L, 2L, 1L), dimnames = list(c("state1", "state2"), names(bank$AB), "priority"))
i <- postrank_mdomain_input(x, targets = list(priority = list(definition = "Fictional priority coordinate", units = "arbitrary",
  orientation = "larger_is_higher", equality_classes = names(bank$AB),
  equality_provenance = "The two coordinates are not structurally identical.")),
  provenance = list(input_id = "positive-equality", law_id = "positive-equality", proper_law = TRUE,
    joint_generation = "Each whole state jointly defines both units.",
    sampling_assumptions = list(finite_support_origin = "Two listed states have equal mass and define the entire law.")),
  representation = "exact_finite_law", masses = c("1/2", "1/2"))
d <- postrank_mdomain_decision(weights = "1", tau = "1/4", t = NULL)
weak <- vapply(bank, function(g) postrank_mdomain_evaluate(i,
  matrix(g, 2, 1, dimnames = list(names(g), "priority")), d)$risk, 0)
stopifnot(max(abs(weak - c(.25, .5, 1))) < 1e-12)
# The losses agree when the same finite law has no equality mass.
no_tie <- postrank_tie_pairwise(as_postrank_tie_draws(neutral_payload(FALSE)))
legacy <- postrank_pairwise(as_postrank_draws(finite_payload(FALSE)))
reduction <- vapply(bank, function(g) postrank_tie_evaluate(g, no_tie, c(priority = 1), .25)$primary_risk -
  postrank_evaluate(g, legacy, c(priority = 1), .25)$primary_risk, 0)
stopifnot(max(abs(reduction)) < 1e-12)
write_result(list(step = "7.16", status = "PASS", neutral_risks = risks, weak_risks = weak,
  expected_neutral = c("1/8", "0", "1/2"), expected_weak = c("1/4", "1/2", "1"),
  no_equality_reduction_errors = reduction, tolerance = 1e-12, grade = as.list(fit$grade),
  solver_status = fit$status, objective = fit$objective,
  scope = "Positive equality changes the loss; same-law tie-free reduction checked separately. HiGHS arithmetic remains floating."),
  "results/software/equality-neutral.json")
