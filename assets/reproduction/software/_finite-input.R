# Literal two-unit complete laws; metadata describes these fictional coordinates only.
finite_payload <- function(equal_mass = FALSE) {
  units <- c("Alder", "Birch")
  theta <- if (equal_mass) list(c(1, 0), c(0, 0)) else list(c(1, 0), c(-1, 0))
  masses <- if (equal_mass) c(1L, 1L) else c(4L, 1L)
  den <- sum(masses)
  x <- list(schema_version = "applied-0.1", input_kind = "exact_finite_posterior",
    dependence_mode = "joint_model", requested_functional = "expected_rank_loss",
    entity_ids = units, criterion_ids = "priority",
    targets = list(list(criterion_id = "priority", estimand = "Fictional priority coordinate",
      entity_population = "Two fictional units", time_reference = "Constructed law",
      units = "arbitrary", source_transform = "identity",
      identification_basis = "Explicit labeled coordinates", orientation = "higher_priority")),
    context = list(cohort_id = "book-two-unit", data_version = "1",
      data_conditioning = "Complete fictional law",
      model_summary = "Two support states; no fitted model or sampling"),
    identification = list(status = "identified_declared", note = "Defined coordinates"),
    tie_policy = list(rule = "pairwise_tie_free", declared = TRUE,
      justification = "Every positive-mass state has distinct coordinates",
      observed_tie_action = "reject_and_review"),
    provenance = list(producer = "v4 monograph example", artifact_id = "two-unit-law",
      artifact_hash = digest::digest(list(theta, masses), algo = "sha256"),
      construction_note = "Literal complete fictional law", created_at = "2026-11-09T00:00:00Z"),
    finite_law = list(denominator = den, value_representation = "safe_integer",
      states = lapply(1:2, function(s) list(state_id = paste0("state-", s),
        mass_numerator = masses[s], theta = matrix(theta[[s]], 2, 1,
          dimnames = list(entity = units, criterion = "priority")))),
      law_definition = "The two listed states and masses are the complete law",
      not_empirical_posterior_relabeling = TRUE))
  x
}
neutral_payload <- function(equal_mass = TRUE) {
  x <- finite_payload(equal_mass)
  x$schema_version <- "tie-aware-input-0.1"
  x$tie_policy <- list(rule = "equality_neutral", declared = TRUE,
    justification = "Exact equal values, when present, are genuine finite-law equality",
    observed_tie_action = "accept_declared_exact_equality")
  x$equality <- list(basis = "exact_finite_law",
    justification = "Derived from every positive-mass support state",
    criterion_classes = list(priority = c(Alder = "Alder", Birch = "Birch")))
  x
}
