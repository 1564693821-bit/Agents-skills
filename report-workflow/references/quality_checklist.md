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
- Required code listings, commands, formulas, derivations, figures, tables, computations, verification, citations, and requested discussion points are present when the prompt asks for them.
- Concise/simple style requirements did not remove required content.
- Every required artifact listed in `work/task_inventory.md` appears in the final report or has a recorded limitation.
- Every required code block, command, formula, derivation, numerical result, figure/table, verification, and discussion appears under the correct sub-question.
- Every planned figure/table is mapped to the sub-question it supports.
- No unrelated content added.

## Correctness Check

- Answers directly address the prompt.
- Reasoning steps are sufficient.
- Assumptions are stated.
- Units are consistent.
- Notation is consistent.
- Computations are reproducible.
- Tables and figures match text.
- Figures match their captions, axes/units, legends, source data, and assigned sub-question.
- Repeated figures are intentional and documented.
- Included code matches the computation or figure it supports, or any intentional difference is recorded.
- Claims are supported by references where required.

## Reference Comparison Check

Use this section when a peer/example report, old submission, solution sample, or worked reference is supplied.

- Primary problem files and explicit user instructions were treated as the authoritative source for required questions.
- Peer/example reports were treated as comparison material unless the user explicitly said otherwise.
- Coverage differences between the current report and peer/example report are recorded.
- Code and figure differences are recorded when they affect correctness or completeness.
- Extra peer/example sub-questions not present in the primary problem file were not added without approval.
- Disagreements were resolved by the primary problem statement, theory, or reproducible computation.
- Numerical or theoretical validation was run for important code/plot disagreements when feasible.

## Pitfall Check

- All pitfalls in `notes.md` reviewed.
- Ambiguities handled.
- Edge cases considered.
- Common mistakes avoided.

## Formatting Check

- Final file exists.
- Template preserved.
- If a populated template was used, old report content was separated from the reusable template shell.
- Old template content was replaced or intentionally retained with a recorded reason.
- The template's main layout, section order, styles, numbering, and caption conventions were not substantially redesigned unless necessary or requested.
- Template font sizes, font families, paragraph spacing, line spacing, alignment, margins, page size, headers/footers, heading style definitions, numbering, captions, and table styles were preserved unless a specific exception is recorded.
- Content was inserted into existing placeholders or matching styled blocks where feasible, instead of rebuilding the document with new default formatting.
- Every template formatting deviation is recorded in `work/checks.md` with a reason.
- Required artifacts are placed under the correct sub-question, not only in appendices or broad exercise sections.
- Headings consistent.
- Sub-question headings or labels remain visible and separate.
- Equations readable.
- Captions present.
- Citations consistent.
- No TODO/FIXME/placeholders.
- `output/` contains only final files.

## DOCX Layout Check

Use this section when the final deliverable is DOCX or a Word-compatible document.

- Page size and margins are clean and professional, preferably A4 with approximately 2.54 cm margins unless a template requires otherwise.
- If a DOCX template is used, its original page size, margins, fonts, font sizes, styles, spacing, headers/footers, section breaks, numbering, captions, and table styles are preserved unless a documented exception applies.
- Body font is readable and consistent, typically 10.5-12 pt.
- Heading styles are applied consistently and reflect the original problem hierarchy.
- Paragraph spacing and line spacing are consistent, without repeated blank paragraphs used for layout.
- Page numbers are present when the document is longer than one page.
- Tables have readable column widths, header rows where appropriate, consistent borders, and no clipped text.
- Figures and tables have numbered captions when present.
- The document avoids excessive colors, decorative shapes, random text boxes, oversized headings, inconsistent indentation, and mixed font families.
- Every sub-question label is visually findable in the DOCX.
- For image-heavy DOCX files, visible figure captions, embedded image references, image relationships, and media files were counted and reconciled.
- Unused template images or stale media were removed when feasible, or their presence was recorded.

## DOCX Formula Check

Use this section when the final deliverable contains formulas or equations.

- Important equations are displayed on their own line and aligned consistently.
- Inline formulas are short and readable.
- Word-compatible equation objects are used where feasible.
- Raw LaTeX is not left in the final DOCX unless the user explicitly requested raw LaTeX text.
- Plain-text math or image equations are used only when native equations are not feasible, and the limitation is recorded.
- Equation images, if unavoidable, are high-resolution, aligned with surrounding text, and not blurry.
- Notation, units, subscripts, superscripts, fractions, vectors, matrices, and significant figures are consistent.
