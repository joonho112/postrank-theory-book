source("scripts/examples/_setup.R")
source("scripts/examples/_mdomain-fixture.R")
f <- md_fixture()
family <- postrank_mdomain_family(f$input, columns = setNames(list(f$bank, f$bank), f$domains), max_actions = 9L)
fit <- postrank_mdomain_solve(f$input, family, f$decision, max_actions = 9L)
stopifnot(nrow(fit$candidate_table) == 9L, fit$optimizer_count == 1L,
  fit$evaluation$risk_exact == "1/5", fit$evaluation$J_exact == "1/5",
  identical(fit$grades, f$grades))
error <- tryCatch(postrank_mdomain_solve(f$input, family, f$decision, max_actions = 8L),
  error = function(e) e)
stopifnot(inherits(error, "error"))
# A separate symmetric law has nine exact risk ties when every card is feasible.
p <- f$provenance; p$input_id <- "symmetric"; p$law_id <- "symmetric"
i <- postrank_mdomain_input(f$x, targets = f$targets, provenance = p,
  representation = "exact_finite_law", masses = c("1/2", "1/2"))
d <- postrank_mdomain_decision(weights = c("1/2", "1/2"), tau = "1/2", t = "0", alpha = "1")
b <- postrank_mdomain_family(i, columns = setNames(list(f$bank, f$bank), f$domains), max_actions = 9L)
tied <- postrank_mdomain_solve(i, b, d, max_actions = 9L)
stopifnot(tied$optimizer_count == 9L, all(tied$candidate_table$optimal), all(tied$grades == 1L))
saveRDS(fit, "evidence/software/mdomain-fit.rds")
write_result(list(step = "7.21", status = "PASS", candidates = fit$candidate_table,
  optimizer_ids = fit$optimizer_ids, grades = fit$grades, search_scope = fit$search_scope,
  solve_status = fit$status, max_actions_error = conditionMessage(error),
  max_actions_error_class = class(error), symmetric_ties = tied$optimizer_count,
  symmetric_selected = tied$grades, symmetric_candidate_table = tied$candidate_table,
  scope = "Complete nine-card banks only; all exact ties and canonical representative retained. Oversized bank refused without incumbent or truncation."),
  "results/software/mdomain-solve.json")
