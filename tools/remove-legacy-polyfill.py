#!/usr/bin/env python3
"""Normalize local render resources for this modern-browser book.

MathJax and its fonts are served locally. MathJax documentation no longer
recommends a polyfill for modern browsers: https://docs.mathjax.org/en/stable/web/start.html
Only the exact known external script is removed; mathematical content is untouched.
"""
from pathlib import Path
import re

# Author: JoonHo Lee (jlee296@ua.edu)

root = Path(__file__).resolve().parent.parent
output = root / '_book'
script = '<script src="https://cdnjs.cloudflare.com/polyfill/v3/polyfill.min.js?features=es6"></script>'
changed = 0
for page in sorted(output.rglob('*.html')):
    original = page.read_text(encoding='utf-8')
    count = original.count(script)
    if count:
        if count != 1:
            raise RuntimeError(f'Unexpected duplicate legacy polyfill in {page.relative_to(root)}')
        page.write_text(original.replace(script, ''), encoding='utf-8')
        changed += 1
print(f'Removed the legacy external polyfill from {changed} HTML pages.')

# Retain icon definitions referenced by the book or its local runtime resources.
# Font declarations and the common icon rendering rules are preserved.
icons = output / 'site_libs/bootstrap/bootstrap-icons.css'
if icons.is_file():
    referenced = set()
    for resource in output.rglob('*'):
        if resource.is_file() and resource != icons and resource.suffix in {'.html', '.js', '.css'}:
            referenced.update(re.findall(r'\bbi-[a-z0-9-]+', resource.read_text(encoding='utf-8')))
    original = icons.read_text(encoding='utf-8')
    removed = []
    def retain_used(match):
        name = match.group(1)
        if name in referenced:
            return match.group(0)
        removed.append(name)
        return ''
    cleaned = re.sub(r'^\.(bi-[a-z0-9-]+)::before\s*\{[^{}]*\}\s*', retain_used, original, flags=re.MULTILINE)
    icons.write_text(cleaned, encoding='utf-8')
    print(f'Removed {len(removed)} unused icon rules; retained {len(referenced)} referenced icon names.')
