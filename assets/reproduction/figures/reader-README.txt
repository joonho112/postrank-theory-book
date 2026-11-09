Compact reader-size figure sources

Extract into a NEW directory and run there. These plotting commands write their
outputs and generated receipts, so do not run them in the canonical book tree.
Preserve the archived directory structure. The included previous outputs permit
identity comparisons; original scientific input files remain unchanged.

Requirements: Python with matplotlib, Pillow and CairoSVG; native Cairo for
CairoSVG; Poppler pdftoppm on PATH. The recorded host used CPython 3.13.2.
The exact versions and font information for the original plotting sources are
recorded separately in the monograph graphics environment. Other hosts/fonts
may produce different graphical bytes. No R package, fitted model, optimizer,
posterior histories or network source is required by these commands.

From the extracted root:
  mkdir -p evidence/editorial/figure-sizing/rasters evidence/figures/rasters
  python3 scripts/figures/reader-compact.py
  python3 scripts/figures/reader-matrices.py
  python3 scripts/figures/reader-f19a.py
  python3 scripts/figures/reader-governance.py
  python3 scripts/figures/reader-proof-guide.py
  python3 scripts/figures/reader-compact-appendices.py
  python3 scripts/figures/reader-exact-grids.py
  python3 scripts/figures/reader-exact-comparisons.py

The commands redraw retained coordinates, exact saved CSV values or symbolic
conditions. They do not refit empirical models or repeat upstream optimization.
Their generated receipts initially state that new visual review is pending.
The source-context file preserves the two Chapter 25 paragraphs used in the
figure receipt. The plotting values come from the supplied data files.

FB's full zero-denominator and varying-report qualifications remain adjacent
to its figure in Appendix B. FA has two panels; both retain their hypotheses.
The book's per-figure placement is separate from plot generation. Its selected
widths and source hashes are included in reader-sizes.json. Actual browser and
whole-book print checks remain outside the static plotting observations.

The producer inputs and outputs were checked during authoring.
The archive supplies the sources and retained exports for those comparisons.
