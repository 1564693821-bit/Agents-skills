# Quality Checklist

## Coverage Check

- Every problem was found.
- Every sub-question was found.
- Every sub-question is represented as its own inventory item.
- Every sub-question has its own draft subsection.
- Every sub-question has a separately visible final answer.
- Every required output is represented.
- Numbering is preserved.
- Grouped ranges such as `(a)-(f)` were expanded and not answered as one combined item.
- No sub-question is hidden inside another answer, a broad exercise summary, or a combined table cell.
- Each final answer label maps back to exactly one inventory item, except report-level sections.
- No unrelated content added.
- For template-backed reports, every template fidelity item is represented: sections, figures, tables, appendices, formulas, logs/data listings, captions, and repeated answer patterns.
- Detailed template/reference appendices, logs, tables, or procedures were not replaced by summaries unless the user requested abridgement.

## Correctness Check

- Answers directly address the prompt.
- Reasoning steps are sufficient.
- Assumptions are stated.
- Units are consistent.
- Notation is consistent.
- Formulas have a LaTeX source form in the draft or notes.
- Important equations, derivations, and formula references were checked against that LaTeX source.
- Computations are reproducible.
- Tables and figures match text.
- Claims are supported by references where required.
- Template-backed rewrites preserve the source template's expected detail level, not just its headings.
- Appendix/log/table row counts, column meanings, and coverage are comparable to the source template or reference material.

## Content-First Review

- Content coverage and correctness were reviewed before final layout or template placement.
- Content defects found during review were fixed in `work/draft.md` before polishing layout.
- Final layout changes did not alter results, remove assumptions, weaken derivations, or hide sub-question answers.
- Any unavoidable content limitation was recorded in `work/checks.md` before completion.

## Pitfall Check

- All pitfalls in `notes.md` reviewed.
- Ambiguities handled.
- Edge cases considered.
- Common mistakes avoided.
- Internal process instructions were kept out of final prose.
- Data-adjustment, anonymization, paraphrase, style-transfer, or tool-choice rules are recorded only in work notes/checks unless explicitly required in the report.

## Formatting Check

- Final file exists.
- Template preserved.
- If a populated template was used, old report content was separated from the reusable template shell.
- Old template content was replaced or intentionally retained with a recorded reason.
- The template's main layout, section order, styles, numbering, and caption conventions were not substantially redesigned unless necessary or requested.
- Headings consistent.
- Sub-question headings or labels remain visible and separate.
- Equations readable.
- Markdown/LaTeX final outputs use LaTeX delimiters consistently for formulas.
- Lists are purposeful, parallel, and not overused.
- Explanatory content is written as coherent paragraphs rather than fragmented bullets where prose is clearer.
- Tables are used for structured comparison or repeated values, not to hide long reasoning in cramped cells.
- Captions present.
- Citations consistent.
- No TODO/FIXME/placeholders.
- No prompt/meta leakage: prompt wording, transformation instructions, local paths, tool notes, "paraphrase", "source report", "baseline source", "processed", "offset", "as requested", or data-adjustment rules.
- `output/` contains only final files.

## DOCX Layout Check

Use this section when the final deliverable is DOCX or a Word-compatible document.

- Page size and margins are clean and professional, preferably A4 with approximately 2.54 cm margins unless a template requires otherwise.
- Body font is readable and consistent, typically 10.5-12 pt.
- Heading styles are applied consistently and reflect the original problem hierarchy.
- Paragraph spacing and line spacing are consistent, without repeated blank paragraphs used for layout.
- Page numbers are present when the document is longer than one page.
- Tables have readable column widths, header rows where appropriate, consistent borders, and no clipped text.
- Wide appendix/log/data tables use readable layout strategies such as landscape pages, repeated headers, split tables, or smaller readable font instead of dropping content.
- Figures and tables have numbered captions when present.
- The document avoids excessive colors, decorative shapes, random text boxes, oversized headings, inconsistent indentation, and mixed font families.
- Every sub-question label is visually findable in the DOCX.

## DOCX Formula Check

Use this section when the final deliverable contains formulas or equations.

- Important equations are displayed on their own line and aligned consistently.
- Inline formulas are short and readable.
- Equations were generated or checked from LaTeX source in the draft/notes.
- Word-compatible equation objects are used where feasible.
- Raw LaTeX delimiters or commands are not left as ordinary text in the final DOCX unless the user explicitly requested raw LaTeX text.
- The DOCX was inspected for pasted LaTeX source such as `$...$`, `$$...$$`, `\(...\)`, or `\[...\]`.
- Plain-text math or image equations are used only when native equations are not feasible, and the limitation is recorded.
- Equation images, if unavoidable, are high-resolution, aligned with surrounding text, and not blurry.
- Notation, units, subscripts, superscripts, fractions, vectors, matrices, and significant figures are consistent.
