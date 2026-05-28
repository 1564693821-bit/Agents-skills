# Template Handling

## Identify Template Format

Inspect `task_config.yaml` and `input/template/` to identify the template format: Markdown, DOCX, PDF, LaTeX, spreadsheet, presentation, plain text, or another format. If `template_filename` is set, prioritize that file.

## Separate Template Shell From Existing Content

If the template already contains a completed report, sample answers, old lab content, comments, or filled-in placeholders, do not treat that content as part of the new answer.

Before generating the final report:

- Identify reusable structure: title page fields, section order, headings, table layout, styles, numbering, figure/table caption style, headers/footers, and required boilerplate.
- Identify old content: previous answers, previous code, previous figures, previous conclusions, old dates, old experiment names, and sample filler text.
- Record the separation in `work/notes.md`, including which template fields should be retained and which old content must be replaced.
- Use old content only when it is generic boilerplate or still correct for the new report. Record the reason when old content is intentionally retained.
- If the distinction between reusable structure and old content is ambiguous and materially affects the final report, ask the user.

## Preserve the Original

Never edit the original template in `input/template/` directly. Copy the template to `output/` or generate a new final file based on it.

## Preserve Structure

Preserve section order, headings, styles, numbering, captions, tables, required fields, and placeholders. Replace placeholders with final content only after drafting answers in `work/draft.md`.

The default behavior is template filling, not redesign. Replace only the content that must change: placeholder text, old/sample answers, metadata values, figure/table slots, and required answer blocks. Keep the surrounding template shell unchanged.

Do not change the template's font sizes, font families, run styles, paragraph styles, line spacing, paragraph spacing, alignment, margins, page size, section breaks, headers/footers, heading style definitions, numbering style, caption style, or table style unless:

- The user explicitly requests that formatting change.
- The template cannot fit or display required content without a minimal local adjustment.
- The available tooling cannot preserve that formatting.

Any exception must be recorded in `work/checks.md` with the affected element and reason.

Do not substantially redesign the template. Keep the template's layout and visual conventions unless:

- The user explicitly asks for a redesign.
- The template format cannot be edited with available tools.
- The template structure prevents the required answers from fitting correctly.

When exact in-place editing is possible, replace old content within the existing styled template shell rather than creating a new document from scratch. When exact in-place editing is not possible, recreate the closest possible structure and record the limitation in `work/checks.md`.

For DOCX templates, preserve the style of the paragraph, run, table cell, heading, or caption that receives replacement content. If replacing text through a library, avoid operations that rebuild the whole document with default styles. If a placeholder spans multiple runs, replace the minimum necessary runs and keep the original formatting of the placeholder container.

## Preserve Sub-Question Granularity

Templates often have broad sections such as "Procedures" or "Analysis." Even inside these broad sections, each required sub-question must remain visible as its own heading, label, table row, or clearly separated paragraph.

Rules:

- Do not merge multiple sub-questions into one combined answer section.
- Do not use headings like `Exercise 3.4(a-c)` when the source separately asks for `(a)`, `(b)`, and `(c)`.
- Use shared setup text only before the separated answers.
- Keep numbering consistent across `work/task_inventory.md`, `work/draft.md`, and the final report.
- If the template has too few answer slots, duplicate the nearest matching styled block or add new same-style labeled blocks so each sub-question remains separate.
- If a table is used for compactness, place each sub-question in its own row or clearly separated block. Do not combine multiple labels in one row merely to save space.

## DOCX Template and Layout Rules

When the template is DOCX or the final output is DOCX:

- Reuse the template's defined styles for title, headings, body text, captions, tables, headers, and footers whenever possible.
- For a DOCX template, reuse means preserving the actual existing styles and formatting, not approximating them with a new default Word document.
- Do not globally redefine styles, normalize fonts, resize headings, change margins, alter line spacing, or rebuild section layout unless the user requested redesign or a technical limitation is recorded.
- If the template lacks usable styles, create a restrained academic/report layout rather than inventing a decorative design.
- Keep margins, page size, header/footer placement, and section breaks stable unless they make the report unreadable.
- Use consistent heading levels that mirror the problem hierarchy and preserve sub-question labels.
- Keep body text readable, normally 10.5-12 pt, with consistent paragraph spacing and line spacing.
- Avoid random text boxes, floating shapes, excessive colors, inconsistent fonts, oversized headings, and manual blank-line spacing.
- Use readable tables with header rows, sensible column widths, consistent borders, and no clipped text.
- Use numbered captions for figures and tables when present.

## DOCX Formula Rules

When formulas are present in DOCX output:

- Prefer native Word-compatible equation objects or a reliable conversion from LaTeX to Word equations.
- Display important equations on their own line with consistent alignment.
- Keep inline formulas short and readable.
- Do not leave raw LaTeX commands in the final DOCX unless the user explicitly requested raw LaTeX text.
- Use plain-text math only when native equations are not feasible, and record the limitation in `work/checks.md`.
- Use equation images only as a last resort. If used, they must be high-resolution, readable, and aligned with the surrounding text.
- Keep notation, units, subscripts, superscripts, fractions, matrices, vectors, and significant figures consistent.

## Required Sections Without Matching Answers

If the template has required sections but no matching answer, record the issue in both `work/notes.md` and `work/checks.md`. Ask the user if the missing content materially affects correctness.

## Figures and Tables

Place generated figures, tables, processed images, and reusable assets in `work/assets/`. Insert or reference them properly in the final report. Captions and numbering must match the text.

## Tooling Limitations

If exact manipulation is not possible because of file format or tooling limits, produce the closest possible final report and record the limitation in `work/checks.md`.

Tooling limitations do not permit silent redesign. If the tool cannot preserve a template's formatting, state what changed and why in `work/checks.md`.

## Final Output

Save only final deliverables in `output/`. Do not place temporary conversion files or scratch files there.
