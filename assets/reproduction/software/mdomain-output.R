source("scripts/examples/_setup.R")
fit <- readRDS("evidence/software/mdomain-fit.rds")
finite <- readRDS("evidence/software/mdomain-finite.rds")
iid <- readRDS("evidence/software/mdomain-iid.rds")
mcmc <- readRDS("evidence/software/mdomain-mcmc.rds")
g <- postrank_mdomain_grades(fit)
stopifnot(identical(g, fit$grades), identical(postrank_mdomain_grades(finite$card), g),
  all(postrank_mdomain_grades(finite$held) == 1L),
  identical(postrank_mdomain_grades(iid$evaluation), iid$grades),
  identical(postrank_mdomain_grades(mcmc$evaluation), mcmc$grades))
dir.create("evidence/software/plots", showWarnings = FALSE)
plots <- list(grades = postrank_plot_mdomain(fit, "grades", base_size = 14),
  cells = postrank_plot_mdomain(fit, "cells", base_size = 14),
  pair = postrank_plot_mdomain(fit, "pair", units = rownames(g), base_size = 14),
  held = postrank_plot_mdomain(finite$held, "pair", units = rownames(g), base_size = 14))
for (name in names(plots)) {
  ggplot2::ggsave(paste0("evidence/software/plots/", name, ".png"), plots[[name]], width = 8, height = 5.5, dpi = 160)
  ggplot2::ggsave(paste0("evidence/software/plots/", name, ".pdf"), plots[[name]], width = 8, height = 5.5)
}
saveRDS(lapply(plots, function(p) list(data = p$data, metadata = attr(p, "postrank_mdomain"))),
  "evidence/software/plot-data.rds")
write_result(list(step = "7.22", status = "PASS", grades = g,
  held_domain_table = finite$held$domain_table,
  plots = lapply(plots, function(p) list(data = p$data, metadata = attr(p, "postrank_mdomain"))),
  extraction_checked_for = c("finite fit", "finite card", "all-withheld", "iid assessment evaluation", "MCMC assessment evaluation"),
  scope = "Stored-result extraction and plot-data execution; actual browser layout is not checked."),
  "results/software/mdomain-output.json")
