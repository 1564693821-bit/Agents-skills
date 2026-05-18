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

## Correctness Check

- Answers directly address the prompt.
- Reasoning steps are sufficient.
- Assumptions are stated.
- Units are consistent.
- Notation is consistent.
- Computations are reproducible.
- Tables and figures match text.
- Claims are supported by references where required.

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
- Body font is readable and consistent, typically 10.5-12 pt.
- Heading styles are applied consistently and reflect the original problem hierarchy.
- Paragraph spacing and line spacing are consistent, without repeated blank paragraphs used for layout.
- Page numbers are present when the document is longer than one page.
- Tables have readable column widths, header rows where appropriate, consistent borders, and no clipped text.
- Figures and tables have numbered captions when present.
- The document avoids excessive colors, decorative shapes, random text boxes, oversized headings, inconsistent indentation, and mixed font families.
- Every sub-question label is visually findable in the DOCX.

## DOCX Formula Check

Use this section when the final deliverable contains formulas or equations.

- Important equations are displayed on their own line and aligned consistently.
- Inline formulas are short and readable.
- Word-compatible equation objects are used where feasible.
- Raw LaTeX is not left in the final DOCX unless the user explicitly requested raw LaTeX text.
- Plain-text math or image equations are used only when native equations are not feasible, and the limitation is recorded.
- Equation images, if unavoidable, are high-resolution, aligned with surrounding text, and not blurry.
- Notation, units, subscripts, superscripts, fractions, vectors, matrices, and significant figures are consistent.
