source("scripts/examples/_setup.R")
units <- c("Alder", "Birch")
targets <- list(priority = list(definition = "Fictional priority coordinate", units = "arbitrary",
  orientation = "larger_is_higher", equality_classes = setNames(units, units),
  equality_provenance = "Distinct targets have no structural identity."))
make_states <- function(ids, reversed) {
  x <- array(0, c(length(ids), 2L, 1L), dimnames = list(ids, units, "priority"))
  x[, 1L, 1L] <- ifelse(reversed, -1, 1); x
}
provenance <- list(input_id = "phase7-exploration", law_id = "phase7-iid-law", proper_law = TRUE,
  producer = "Literal independent Bernoulli generator with event probability .01",
  joint_generation = "Each Bernoulli outcome defines the whole two-unit state.",
  sampling_assumptions = list(iid_whole_states = TRUE))
explore_ids <- paste0("explore-", 1:2)
set.seed(119)
explore <- postrank_mdomain_input(make_states(explore_ids, runif(2) < .01),
  targets = targets, provenance = provenance, representation = "iid_equal_weight_draws")
g <- matrix(1:2, 2, 1, dimnames = list(units, "priority"))
d <- postrank_mdomain_decision(weights = "1", tau = "1/4", t = "0", alpha = "1/10")
card <- postrank_mdomain_evaluate(explore, g, d)
S <- 59L; ids <- paste0("validation-", seq_len(S))
design <- list(spec_hashes = card$receipts$validation_spec_hashes, beta_exact = "1/20",
  fixed_S = S, iid_whole_states = TRUE, independent_of_exploration = TRUE,
  frozen_before_validation = TRUE, fixed_sample_size = TRUE, no_validation_reuse = TRUE,
  no_optional_stopping = TRUE, iid_mechanism = "Independent runif Bernoulli(.01) whole states with prespecified seed120.",
  independence_justification = "Fresh independent-generator calls after the frozen record; fictional law only.",
  exploration_history_id = "phase7-exploration", frozen_record_id = "phase7-frozen59",
  validation_batch_id = "phase7-validation59", exploration_state_ids = explore_ids,
  validation_state_ids = ids)
# Persist the design BEFORE generating/inspecting the validation batch.
saveRDS(list(card = card, design = design, validation_seed = 120L), "evidence/software/iid-frozen.rds")
jsonlite::write_json(design, "evidence/software/iid-frozen-design.json", auto_unbox = TRUE, pretty = TRUE)
set.seed(120)
reverse <- runif(S) < .01
provenance$input_id <- "phase7-validation"
input <- postrank_mdomain_input(make_states(ids, reverse), targets = targets,
  provenance = provenance, representation = "iid_equal_weight_draws")
a <- postrank_mdomain_assess(input, card, method = "iid", design = design, beta = "1/20")
stopifnot(a$method == "iid", abs(a$J - mean(reverse)) < 1e-12)
saveRDS(a, "evidence/software/mdomain-iid.rds")
write_result(list(step = "7.19", status = "PASS", fixed_S = S, seed = 120L, hits = sum(reverse),
  true_fictional_J = .01, assessment_status = a$status, empirical_J = a$J,
  joint_certificate = a$joint_certificate, certificate_scope = a$certificate_scope,
  assurance = a$assurance, count_bound = json_safe(a$native$count_bound),
  scope = "Actual fixed-design simulated iid execution; accepted count bound, if any, is conditional and concerns only the frozen joint event."),
  "results/software/mdomain-iid.json")
