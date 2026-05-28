# Checks

## Coverage Check

- [ ] Every question in `work/task_inventory.md` is answered.
- [ ] Every sub-question is answered.
- [ ] Every sub-question is a separate inventory item.
- [ ] Every sub-question has a separate draft subsection.
- [ ] Every sub-question has a separately visible final answer.
- [ ] Question numbering matches the source.
- [ ] Grouped ranges such as `(a)-(f)` were expanded instead of merged.
- [ ] No unrelated content is added.
- [ ] For template-backed reports, sections, figures, tables, appendices, formulas, logs/data listings, and captions from the template are preserved or explicitly accounted for.
- [ ] Detailed appendices/logs/tables/procedures were not replaced by summaries unless requested.

## Correctness Check

- [ ] Each answer directly addresses the prompt.
- [ ] Assumptions are stated.
- [ ] Reasoning is complete.
- [ ] Computations are reproducible.
- [ ] Units and notation are consistent.
- [ ] Formulas have LaTeX source in `work/draft.md` or `work/notes.md`.
- [ ] Important equations and derivations were checked against the LaTeX source.
- [ ] Figures and tables match the report.
- [ ] Pitfalls in `work/notes.md` were reviewed.
- [ ] Template-backed rewrites preserve the expected detail level, not just the headings.
- [ ] Appendix/log/table row counts, columns, and coverage are comparable to the source template or reference.

## Content-First Review

- [ ] Content coverage and correctness were reviewed before layout/template polishing.
- [ ] Content defects found during review were fixed in `work/draft.md`.
- [ ] Layout changes did not alter results, remove assumptions, weaken derivations, or hide sub-question answers.
- [ ] Unavoidable content limitations are recorded here before completion.

## Formatting Check

- [ ] Final report is saved in `output/`.
- [ ] Template formatting is preserved if a template exists.
- [ ] If a populated template exists, reusable structure was separated from old/sample content.
- [ ] Old/sample template content was replaced or intentionally retained with a recorded reason.
- [ ] The template was not substantially redesigned unless necessary or requested.
- [ ] Headings and numbering are consistent.
- [ ] Sub-question headings or labels remain visible and separate.
- [ ] Figures and tables have captions if needed.
- [ ] Equations are readable.
- [ ] Markdown/LaTeX outputs use consistent LaTeX delimiters for formulas.
- [ ] DOCX outputs do not show raw LaTeX delimiters or commands as ordinary text unless explicitly requested.
- [ ] DOCX equations were converted/rendered from LaTeX source where feasible, or the fallback is recorded in Known limitations.
- [ ] Lists are purposeful, parallel, and not overused.
- [ ] Explanations and analysis are coherent paragraphs rather than fragmented bullets where prose is clearer.
- [ ] Tables are used for structured values/comparisons, not to hide long reasoning in cramped cells.
- [ ] Citations/references are consistent if used.
- [ ] No TODO, FIXME, placeholder, or internal note remains.
- [ ] No prompt/meta leakage remains in the final report, including prompt wording, transformation rules, data-adjustment rules, local paths, tool notes, or phrases such as "source report", "processed", "offset", "baseline", or "as requested".
- [ ] Wide appendix/log/data tables are formatted readably instead of being shortened to fit.
- [ ] No temporary files are in `output/`.

## Final Summary

- Final output:
- Intermediate files:
- Code/assets:
- Checks performed:
- Known limitations:
- Assumptions made:
