source("scripts/examples/_setup.R")
units <- c("Alder", "Birch"); S <- 400L
ids <- paste0("markov-", seq_len(S))
# Two explicitly simulated stationary two-state chains. Transition probabilities
# P(0->1)=.02 and P(1->0)=.18 give stationary event probability .1.
# This is a fictional Markov history, not a new empirical posterior fit.
set.seed(721)
chain <- function(n) {
  z <- logical(n); z[1] <- runif(1) < .1
  for (s in 2:n) z[s] <- if (z[s-1]) runif(1) >= .18 else runif(1) < .02
  z
}
reversed <- c(chain(200L), chain(200L))
x <- array(0, c(S, 2L, 1L), dimnames = list(ids, units, "priority"))
x[, 1L, 1L] <- ifelse(reversed, -1, 1)
origin <- data.frame(source_index = seq_len(S), chain_id = rep(c("chain1", "chain2"), each = 200L),
  iteration_id = rep(seq_len(200L), 2), state_id = ids)
i <- postrank_mdomain_input(x, targets = list(priority = list(definition = "Fictional priority coordinate",
  units = "arbitrary", orientation = "larger_is_higher", equality_classes = setNames(units, units),
  equality_provenance = "No model identity between units.")),
  provenance = list(input_id = "phase7-markov", law_id = "phase7-markov-law", proper_law = TRUE,
    producer = "Explicit stationary two-state Markov generator",
    joint_generation = "Every Markov state determines both unit coordinates.",
    sampling_assumptions = list(stationary_initialization = "Bernoulli(.1)",
      transition_01 = .02, transition_10 = .18, seed = 721L)),
  representation = "mcmc_equal_weight_draws", state_origin = origin)
g <- matrix(1:2, 2, 1, dimnames = list(units, "priority"))
d <- postrank_mdomain_decision(weights = "1", tau = "1/4", t = "0", alpha = "1/4")
a <- postrank_mdomain_assess(i, g, d, method = "mcmc", batch_size = 50L,
  design = list(role = "fictional_fixed_report_diagnostic", report_prespecified = TRUE))
stopifnot(a$method == "mcmc", !isTRUE(a$joint_certificate), !a$assurance$numerical_guarantee,
  abs(a$J - mean(reversed)) < 1e-12)
saveRDS(a, "evidence/software/mdomain-mcmc.rds")
write_result(list(step = "7.20", status = "PASS", seed = 721L, states = S, chains = 2L,
  hits = sum(reversed), empirical_J = a$J, stationary_fictional_J = .1,
  assessment_status = a$status, joint_certificate = a$joint_certificate,
  assurance = a$assurance, diagnostic_summary = capture.output(summary(a)),
  native = json_safe(a$native),
  scope = "Actual simulated dependent histories; empirical fixed-report diagnostics only. No iid or convergence certificate, empirical refit or held-out claim."),
  "results/software/mdomain-mcmc.json")
