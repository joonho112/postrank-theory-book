# Author: JoonHo Lee (jlee296@ua.edu)
# Exact crossed-law example retained from the reviewed pilot.
# Run in a fresh R session with POSTRANK_LIB set to a postrank 1.2.0 library.
library(postrank, lib.loc = Sys.getenv("POSTRANK_LIB"))
stopifnot(as.character(packageVersion("postrank")) == "1.2.0")
units <- c("Alder", "Birch")
domains <- c("Domain1", "Domain2")
x <- array(0, c(2, 2, 2),
  dimnames = list(c("state1", "state2"), units, domains))
x[1, , ] <- rbind(c(1, -1), c(0, 0))
x[2, , ] <- rbind(c(-1, 1), c(0, 0))
targets <- setNames(lapply(domains, function(d) list(
  definition = paste("Synthetic priority in", d), units = "arbitrary units",
  orientation = "larger_is_higher", equality_classes = units,
  equality_provenance = "The two targets have no structural identity.")), domains)
input <- postrank_mdomain_input(x, targets = targets,
  provenance = list(input_id = "crossed", law_id = "crossed", proper_law = TRUE,
    joint_generation = "Each listed state jointly specifies both domains.",
    sampling_assumptions = list(
      finite_support_origin = "The two states and masses define the complete law.")),
  representation = "exact_finite_law", masses = c("4/5", "1/5"))
decision <- postrank_mdomain_decision(weights = c("1/2", "1/2"),
  tau = "1/3", q = NULL, t = "0", alpha = "1/4")
bank <- list(W = setNames(c(1L, 1L), units),
  AB = setNames(c(1L, 2L), units), BA = setNames(c(2L, 1L), units))
family <- postrank_mdomain_family(input,
  columns = setNames(list(bank, bank), domains), max_actions = 9L)
fit <- postrank_mdomain_solve(input, family, decision, max_actions = 9L)
card <- postrank_mdomain_evaluate(input, fit$grades, decision)
assessment <- postrank_mdomain_assess(input, card, method = "exact")
stopifnot(nrow(fit$candidate_table) == 9L, fit$optimizer_count == 1L,
  card$risk_exact == "1/5", card$J_exact == "1/5",
  assessment$status == "evaluated_declared_finite_law")
fit$grades
fit$candidate_table[, c("action_id", "risk_exact", "J_exact",
  "feasible_for_represented_measure", "optimal")]
