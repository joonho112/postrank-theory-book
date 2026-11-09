source("scripts/examples/_setup.R")
source("scripts/examples/_mdomain-fixture.R")
f <- md_fixture()
card <- postrank_mdomain_evaluate(f$input, f$grades, f$decision)
a <- postrank_mdomain_assess(f$input, card, method = "exact")
held <- postrank_mdomain_evaluate(f$input, cbind(Domain1 = f$bank$W, Domain2 = f$bank$W), f$decision)
expected <- postrank_mdomain_evaluate(f$input, f$grades, f$decision, mode = "expected")
stopifnot(card$risk_exact == "1/5", card$J_exact == "1/5", card$feasible_for_represented_measure,
  a$status == "evaluated_declared_finite_law", held$risk_exact == "1/3", held$J_exact == "0",
  is.na(expected$J), is.na(expected$feasible_for_represented_measure))
saveRDS(list(card = card, assessment = a, held = held), "evidence/software/mdomain-finite.rds")
write_result(list(step = "7.18", status = "PASS", risk_exact = card$risk_exact, J_exact = card$J_exact,
  assessment_status = a$status, arithmetic = card$status, held_risk_exact = held$risk_exact,
  held_J_exact = held$J_exact, expected_mode_joint_unknown = is.na(expected$J),
  assurance = a$assurance, scope = "Exact arithmetic for the declared complete finite law, not a fitted-posterior certificate."),
  "results/software/mdomain-finite.json")
