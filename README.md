# Decisions from Noisy Multidimensional Indicators

## Theory, Evidence, and Posterior Grading

**JoonHo Lee ([jlee296@ua.edu](mailto:jlee296@ua.edu))** · [ORCID 0009-0006-4019-8703](https://orcid.org/0009-0006-4019-8703)

A Quarto book on decisions from noisy multidimensional indicators: theory, evidence, and posterior grading

This book studies how uncertain, multidimensional indicators can support common ordered grades for public decisions. It develops the institutional context, related literature, mathematical definitions, decision losses, computation, numerical uncertainty and interpretation of posterior grading. The book contains 22 chapters, five appendices, a preface and 58 referenced works. It provides the theory and literature foundation for P1 in the postrank research program.

The manuscript version is **v3**. The source is prepared here for publication review; no public release tag or DOI is assigned by this copy.

## Build and preview

Use [Quarto 1.9.37](https://quarto.org/docs/get-started/) and Python 3. From the repository root:

```sh
quarto render
quarto preview
```

The HTML book is written to `_book/index.html`. Rendering uses the supplied text, figures, bibliography, local MathJax and fonts. Scientific code execution is disabled. Rendering does not require R, the postrank package, an optimizer or historical empirical data.

## Contents

The six parts cover public decisions and measurement; Bayesian ranking, uncertainty and multicriteria methods; mathematical foundations; computation and numerical uncertainty; evaluation and comparison; and interpretation and research use. Appendices provide the proof guide, notation, source provenance, software correspondence and reproduction materials.

## Reproduction

`assets/reproduction/p1-small-examples.zip` contains four finite Python calculations and two R plotting scripts. Extract it, enter `p1-small-examples/`, and run:

```sh
python3 verify.py
python3 examples/fixed-order-dp.py --check
python3 examples/exact-common-grade.py --check
python3 examples/objective-contrast.py --check
python3 examples/matched-disclosure.py --check
```

The finite Python checks use the standard library. The R scripts list their plotting dependencies in the archive's environment record. Figure source code, small plotting inputs and a command guide are supplied separately in `assets/reproduction/figures/` and `assets/reproduction/figure-sources-2026-10-27.zip`. Appendix E explains the scope of each calculation. None of these materials runs the proposed main empirical study.

## Citation and rights

[CITATION.cff](CITATION.cff) provides the book's author, title and manuscript version. Cite the version actually consulted. Original text, figures and accompanying code are attributed to JoonHo Lee; see [RIGHTS.md](RIGHTS.md) for rights status. Third-party components retain the notices identified in [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md).

## GitHub Pages

The repository is [joonho112/postrank-theory-book](https://github.com/joonho112/postrank-theory-book). The included workflow is started manually and defaults to building without deployment. After GitHub Pages is configured to use Actions, a manually selected publish run can deploy the rendered book. The configured destination is `https://joonho112.github.io/postrank-theory-book/`.
