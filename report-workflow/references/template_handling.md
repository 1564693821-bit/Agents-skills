# Template Handling

## Identify Template Format

Inspect `task_config.yaml`, `input/template/`, `input/problems/`, and `input/references/` to identify the template format: Markdown, DOCX, PDF, LaTeX, spreadsheet, presentation, plain text, or another format. If `template_filename` is set, prioritize that file.

A template may live outside `input/template/`. Treat a problem or reference file as a template-like source when it is an answer sheet, lab handout with answer spaces, rubric document to be filled, partially completed report, or required document shell.

## Create a Working Template Copy

Before editing any template or template-like source, copy it out of `input/` and into a writable working area:

```text
work/assets/template_working/
```

Preferred helper: run `scripts/prepare_working_template.py <project-root>` from this skill when the template can be found from `task_config.yaml`. If the helper cannot identify the file, choose the source manually and still place the copy under `work/assets/template_working/`.

Rules:

- Preserve the original filename when practical, or use a clearly related name such as `<stem>.working.<ext>`.
- Record the original input path and working-copy path in `work/notes.md`.
- Perform all in-place template edits on the working copy only.
- Keep temporary conversion products beside the working copy or in `work/assets/`, not in `output/`.
- Export or copy only the finished deliverable into `output/`.
- If the working copy already exists from a previous run, reuse it only when it matches the current source and intended edits; otherwise create a fresh working copy and record the choice.

## Separate Template Shell From Existing Content

If the template already contains a completed report, sample answers, old lab content, comments, or filled-in placeholders, do not treat that content as part of the new answer.

Before generating the final report:

- Identify reusable structure: title page fields, section order, headings, table layout, styles, numbering, figure/table caption style, headers/footers, and required boilerplate.
- Identify old content: previous answers, previous code, previous figures, previous conclusions, old dates, old experiment names, and sample filler text.
- Identify fidelity-critical content: section depth, long explanations, formulas, figures, tables, appendices, logs, data listings, captions, and repeated answer patterns that must be preserved or replaced at a comparable level of detail.
- Record the separation in `work/notes.md`, including which template fields should be retained and which old content must be replaced.
- Use old content only when it is generic boilerplate or still correct for the new report. Record the reason when old content is intentionally retained.
- If the distinction between reusable structure and old content is ambiguous and materially affects the final report, ask the user.

## Preserve the Original

Never edit the original template in `input/` directly. Copy the template to `work/assets/template_working/` and edit that working copy. The final file in `output/` should normally be produced from the edited working copy.

Do not rebuild a document from scratch merely because `input/` is read-only. Read-only input is solved by copying the file into `work/`, not by discarding the template structure.

## Preserve Structure

Preserve section order, headings, styles, numbering, captions, tables, required fields, and placeholders where appropriate. Replace placeholders with final content only after drafting answers in `work/draft.md`.

This rule is strict: a template is not a style mood board. A template is the document shell to fill. The correct mental model is a human opening the copied template in Word, selecting old or placeholder content, and replacing it with the new report while leaving the template's visible structure intact.

Mandatory template-filling behavior:

- Fill the copied template in place whenever possible.
- Replace old report text, metadata, answer paragraphs, code listings, figures, captions, tables, and appendices at their corresponding locations.
- Preserve the original page setup, margins, section order, heading hierarchy, indentation, fonts, spacing, headers/footers, numbering, caption conventions, and repeated answer patterns.
- When the template has a repeated block, duplicate that block's style for additional required answers instead of inventing a different layout.
- Use tools that let you fill or verify the template faithfully. If a normal text/DOCX library is not enough, use stronger document tools such as LibreOffice/soffice rendering, DOCX XML/package edits, PDF/PNG page renders, screenshots, or visual inspection.

Prohibited template behavior:

- Do not make a new polished document that merely resembles the template.
- Do not replace the template with a custom design because it is easier to generate.
- Do not treat "cleaner", "prettier", or "more organized" as better when it moves away from the supplied template.
- Do not call the task complete while the output has major visual differences from the template that a human grader would notice.

Do not use template placement as the first writing pass. First draft and review the content in `work/draft.md`; then place the checked content into the copied template and adjust layout.

Do not substantially redesign the template. Keep the template's layout and visual conventions unless:

- The user explicitly asks for a redesign.
- The template format cannot be edited with available tools.
- The template structure prevents the required answers from fitting correctly.

When exact in-place editing is possible, replace old content within the working template shell rather than creating a new document from scratch. When exact in-place editing is not possible, recreate the closest possible structure and record the limitation in `work/checks.md`.

The "exact in-place editing is not possible" exception must be earned, not assumed. Try reasonable template-filling tools first. If the exception is used, `work/checks.md` must say what failed, why filling the copied template was impossible, and how the fallback preserves the original template as closely as possible.

## Preserve Information Density

For template-backed paraphrase, rewrite, or "use this report as the base" tasks, the template is both a style source and a coverage source. Do not summarize away detail.

Required actions:

- Create a template fidelity map in `work/task_inventory.md` or `work/notes.md` before final generation.
- Map each source section, subsection, figure, table, appendix, formula block, code/log/data listing, and repeated answer pattern to a final report location.
- Match the template's level of detail unless the user explicitly requests a shorter report. A detailed procedure should remain a detailed procedure; a full appendix/log should remain a full appendix/log; a multi-row table should remain a multi-row table.
- If a source appendix/table/log is too wide for the final format, adjust layout using landscape pages, smaller readable font, split tables, or repeated headers. Do not drop columns or rows simply to make formatting easier.
- If exact preservation is impossible because of tool limits or unreadable source content, record the limitation in `work/checks.md` and preserve the closest readable equivalent.

Blocking issues:

- A final report that has the right section names but much less content than the template is incomplete.
- A final appendix that replaces a detailed reference/log/table with selected rows or a narrative summary is incomplete unless the user requested an abridgement.
- Missing captions, missing figure/table numbers, missing appendix columns, or missing log rows are formatting or coverage errors depending on severity.

## Keep Process Metadata Out of the Final Report

Task instructions guide the work but are not report content. Do not put prompt wording, transformation instructions, data-adjustment rules, "paraphrase" requests, local file paths, "source report", "baseline source", "processed", "offset", "as requested", tool limitations, or internal assumptions into the final deliverable unless the assignment explicitly asks for a methods note about them.

Allowed locations for process metadata:

- `work/notes.md`
- `work/checks.md`
- comments inside scripts under `work/code/`
- final assistant response when summarizing limitations

Final-report language should read like a natural report in the requested discipline. If values are adjusted, anonymized, normalized, or transformed per configuration, present the final values as ordinary report results and keep the transformation rule internal.

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

- Prefer editing the copied DOCX package in `work/assets/template_working/` or using a DOCX library against that working copy.
- Treat the copied DOCX as the primary artifact. The goal is to fill that file, not to generate a separate Word document with similar headings.
- Reuse the template's defined styles for title, headings, body text, captions, tables, headers, and footers whenever possible.
- If the template lacks usable styles, create a restrained academic/report layout rather than inventing a decorative design.
- Apply layout after the content review passes. The DOCX pass should organize checked content; it should not be the moment where missing answers or weak derivations are first discovered.
- Keep margins, page size, header/footer placement, and section breaks stable unless they make the report unreadable.
- Use consistent heading levels that mirror the problem hierarchy and preserve sub-question labels.
- Keep body text readable, normally 10.5-12 pt, with consistent paragraph spacing and line spacing.
- Use paragraphs for explanations, methods, and analysis; use lists only for parallel steps, conditions, observations, or deliverables; use tables for repeated structured values or comparisons.
- Remove excessive fragmented bullets, one-item lists, and non-parallel lists introduced during drafting.
- Avoid random text boxes, floating shapes, excessive colors, inconsistent fonts, oversized headings, and manual blank-line spacing.
- Use readable tables with header rows, sensible column widths, consistent borders, and no clipped text.
- Use numbered captions for figures and tables when present.

DOCX template-fidelity verification is mandatory before completion:

- Render or open the original template and final DOCX when feasible.
- Compare the first page, metadata block, main section pages, representative code/table/figure pages, and final page.
- Check that the final DOCX looks like the template with new content inserted.
- Iterate on mismatches in spacing, widths, indentation, line breaks, code block shading, caption style, figure sizing, and page flow.
- Record the render/open tool, pages inspected, mismatches found, and fixes made in `work/checks.md`.

If LibreOffice/soffice, Word, or another renderer is missing and visual fidelity matters, obtain or request the needed tool rather than accepting an unverified template-backed DOCX. If a renderer truly cannot be used, record the limitation clearly and perform the strongest structural inspection available.

## Formula Rules

Use LaTeX as the formula source of truth during drafting and checking.

- In Markdown and LaTeX final outputs, keep formulas in LaTeX with consistent inline and display delimiters.
- In DOCX final outputs, prefer native Word-compatible equation objects or a reliable conversion from LaTeX to Word equations.
- Do not assume Word will automatically transform raw LaTeX delimiters into equations. The agent must explicitly convert, render, or choose a documented fallback.
- Display important equations on their own line with consistent alignment.
- Keep inline formulas short and readable.
- Do not leave raw `$...$`, `$$...$$`, `\(...\)`, `\[...\]`, or LaTeX commands in the final DOCX unless the user explicitly requested raw LaTeX text, but keep the LaTeX source in `work/draft.md` or `work/notes.md` for traceability.
- Use plain-text math only when native equations are not feasible, and record the limitation in `work/checks.md`.
- Use equation images only as a last resort. If used, they must be high-resolution, readable, and aligned with the surrounding text.
- Keep notation, units, subscripts, superscripts, fractions, matrices, vectors, and significant figures consistent.
- Check that no formula block from the template or draft was omitted, mistranscribed, or replaced by a vague prose summary.

## Required Sections Without Matching Answers

If the template has required sections but no matching answer, record the issue in both `work/notes.md` and `work/checks.md`. Ask the user if the missing content materially affects correctness.

## Figures and Tables

Place generated figures, tables, processed images, and reusable assets in `work/assets/`. Insert or reference them properly in the final report. Captions and numbering must match the text.

For template-backed reports, compare figure/table coverage against the template:

- Same conceptual figure/table should appear unless replaced by a better equivalent.
- Tables should preserve required columns and row coverage.
- Raw logs, Fourier tables, appendices, code listings, and data sheets should remain detailed when the template/reference is detailed.
- Wide technical tables may use landscape layout or smaller readable text; layout pressure is not a reason to omit data.

## Tooling Limitations

If exact manipulation is not possible because of file format or tooling limits, produce the closest possible final report and record the limitation in `work/checks.md`.

## Final Output

Save only final deliverables in `output/`. Do not place temporary conversion files or scratch files there. The working template copy and all intermediate edited versions belong in `work/assets/template_working/`.
