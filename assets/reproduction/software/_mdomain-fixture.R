# Two domains; complete crossed finite law from the theory pilot.
md_fixture <- function() {
  units <- c("Alder", "Birch"); domains <- c("Domain1", "Domain2")
  x <- array(0, c(2L, 2L, 2L), dimnames = list(c("state1", "state2"), units, domains))
  x[1, , ] <- rbind(c(1, -1), c(0, 0)); x[2, , ] <- rbind(c(-1, 1), c(0, 0))
  targets <- setNames(lapply(domains, function(d) list(definition = paste("Fictional priority in", d),
    units = "arbitrary", orientation = "larger_is_higher", equality_classes = setNames(units, units),
    equality_provenance = "No structural identity is imposed between the two units.")), domains)
  provenance <- list(input_id = "phase7-crossed", law_id = "phase7-crossed-law", proper_law = TRUE,
    joint_generation = "Each listed state jointly specifies both units in both domains.",
    sampling_assumptions = list(finite_support_origin = "These two states and rational masses define the complete fictional law."))
  input <- postrank_mdomain_input(x, targets = targets, provenance = provenance,
    representation = "exact_finite_law", masses = c("4/5", "1/5"))
  decision <- postrank_mdomain_decision(weights = c("1/2", "1/2"), tau = "1/3",
    q = NULL, t = "0", alpha = "1/4")
  bank <- list(W = setNames(c(1L, 1L), units), AB = setNames(c(1L, 2L), units),
    BA = setNames(c(2L, 1L), units))
  grades <- cbind(Domain1 = bank$AB, Domain2 = bank$BA)
  list(input = input, decision = decision, bank = bank, grades = grades, x = x,
    targets = targets, provenance = provenance, units = units, domains = domains)
}
