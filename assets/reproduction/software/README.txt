postrank 1.2.0: small monograph examples

Unzip software-examples.zip and work from its root directory. Install postrank 1.2.0 and its dependencies in a library of your choice; set POSTRANK_LIB to that library before starting a fresh R process. The scripts assert the version and loaded path. HiGHS is explicitly selected for the common and equality-neutral examples. No empirical model is fitted.

Run these scripts in order with Rscript --vanilla:
  scripts/examples/common.R
  scripts/examples/equality-neutral.R
  scripts/examples/mdomain-input.R
  scripts/examples/mdomain-finite.R
  scripts/examples/mdomain-iid.R
  scripts/examples/mdomain-mcmc.R
  scripts/examples/mdomain-solve.R
  scripts/examples/mdomain-output.R

The helper files provide the full input declarations. Individual linked scripts need these helpers and are best used from the complete bundle. Generated results go to results/software; input and assessment records go to evidence/software. JSON null preserves unavailable ratios. Exact rational quantities are strings.

The iid example freezes its report and validation design before generating a prespecified batch of 59 whole states. Its conditional guarantee concerns only that joint event. The Markov example generates fictional dependent chains and reports diagnostics only. Replaying this demonstration is not independent scientific validation of any empirical posterior.

The larger synthetic40 replay uses separately archived source inputs and is documented in the local execution log; those histories are not included in this small bundle.
