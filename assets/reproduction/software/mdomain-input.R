source("scripts/examples/_setup.R")
source("scripts/examples/_mdomain-fixture.R")
f <- md_fixture()
stopifnot(inherits(f$input, "postrank_mdomain_input"), inherits(f$decision, "postrank_mdomain_decision"),
  identical(dim(f$x), c(2L, 2L, 2L)))
saveRDS(f, "evidence/software/mdomain-fixture.rds")
write_result(list(step = "7.17", status = "PASS", dimensions = dim(f$x),
  state_ids = dimnames(f$x)[[1]], unit_ids = f$units, domain_ids = f$domains,
  masses = c("4/5", "1/5"), weights = c("1/2", "1/2"), tau = "1/3", t = "0", alpha = "1/4",
  input_summary = capture.output(summary(f$input)), decision_summary = capture.output(summary(f$decision)),
  scope = "Complete fictional joint law; producer declarations are not empirical validation."),
  "results/software/mdomain-input.json")
