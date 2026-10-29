# Third-party notices

These notices identify components distributed with the book's public source. They do not grant a license to the monograph itself; see [RIGHTS.md](RIGHTS.md).

## MathJax

`assets/mathjax/` supplies the local JavaScript mathematics renderer and its associated font assets, from the [MathJax project](https://www.mathjax.org/). The included [Apache License, Version 2.0](assets/mathjax/LICENSE) is retained. The release package preserves these local component files without changes. The post-render helper removes an external ES6 polyfill script tag from generated HTML; it does not modify the MathJax distribution files.

## APA citation style

`assets/apa.csl` identifies itself as **APA Style 7th edition** (embedded update date: 7 February 2026), with the upstream style identifier [http://www.zotero.org/styles/apa](http://www.zotero.org/styles/apa). Its embedded authors are **Brenton M. Wiernik** and **Andrew Dunning**, and its contributor is **Jay Pfaffman**. The embedded rights element specifies [Creative Commons Attribution-ShareAlike 3.0](http://creativecommons.org/licenses/by-sa/3.0/). The style’s author, contributor, and rights metadata are intact. A header comment identifying the upstream style-building tool was omitted during packaging; the citation-style rules are unchanged. The style's license is not asserted as the license of the surrounding book.

## Files supplied by the rendering toolchain

Quarto generates HTML support files under `_book/site_libs/` when the book is rendered. Those toolchain assets are distinct from the book's original prose and figures. Their embedded notices and applicable upstream licenses should be retained with the rendered output. This notice does not claim a separate full dependency-license audit or replace the licenses supplied by Quarto and its components.
