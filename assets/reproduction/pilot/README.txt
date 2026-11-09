Exact finite-law example for domain profiles

Author: JoonHo Lee (jlee296@ua.edu)

Extract this archive and open a terminal in the extracted directory. Use an
existing R library containing postrank 1.2.0 and the R packages gmp, jsonlite
and digest. The Python calculation uses only the standard library.

  POSTRANK_LIB=/path/to/library Rscript scripts/examples/pilot.R
  python3 scripts/examples/pilot-oracle.py
  python3 scripts/examples/compare-pilot.py

The fixture in evidence/pilot/fixture-spec.json specifies complete synthetic
finite laws. The checks compare the exact risk, joint error probability,
feasibility, minimizing sets and common-card membership for 63 cards across
seven examples. The common family is the diagonal subset of the same
nine-card profile family. Reference CSVs are provided. The commands write
new results and computational receipts in results/pilot/.

The R and Python implementations evaluate the same mathematical definitions.
The separate crossed-example.R script reproduces the two-unit example in
Chapter 14. Run it in a fresh R process with POSTRANK_LIB set as above.

The desktop and stacked figures show the same scientific values. To regenerate
them, run scripts/examples/pilot-figure.py and pilot-figure-stacked.py from the
extracted directory with ReportLab and Poppler available. These dependencies
are only needed for figure regeneration.
