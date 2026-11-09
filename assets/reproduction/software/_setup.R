# Run from the monograph root with POSTRANK_LIB set to the verified 1.2.0 library.
lib <- Sys.getenv("POSTRANK_LIB")
stopifnot(nzchar(lib), dir.exists(lib))
library(postrank, lib.loc = lib)
stopifnot(as.character(packageVersion("postrank")) == "1.2.0",
  normalizePath(find.package("postrank")) == normalizePath(file.path(lib, "postrank")))
options(width = 110)
dir.create("evidence/software", recursive = TRUE, showWarnings = FALSE)
dir.create("results/software", recursive = TRUE, showWarnings = FALSE)
write_result <- function(x, file) {
  x$package_version <- as.character(packageVersion("postrank"))
  x$execution <- "current Phase7 run"
  jsonlite::write_json(x, file, auto_unbox = TRUE, pretty = TRUE, digits = 16,
    null = "null", na = "null")
}

# Preserve exact integers/rationals as strings in inspectable JSON outputs.
json_safe <- function(x) {
  if (inherits(x, "bigq") || inherits(x, "bigz")) return(as.character(x))
  if (is.list(x)) return(lapply(x, json_safe))
  x
}
