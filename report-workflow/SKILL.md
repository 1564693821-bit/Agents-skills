---
name: report-workflow
description: A self-initializing report-writing workflow. Use this skill when the user wants Codex to create or use a standardized report project for homework reports, experiment reports, course reports, technical reports, or template-based answer files. On first use, the skill detects whether the current directory is initialized; if not, it creates input/, work/, output/, task_config.yaml, and starter files, then stops. On later use, it reads problems, references, templates, drafts answers, generates the final report, and performs correctness and formatting checks. Also use this skill when the user says a report task is finished or "任务结束" and wants problems from the task summarized, presented, and folded back into this report-workflow skill.
---

# Purpose

Use this skill to manage a standardized report-writing project from initialization through final checked deliverable. The skill has two modes:

- First-run initialization mode: create the project structure and starter files, then stop.
- Report-writing mode: read configuration, problems, references, and templates; inventory tasks; draft answers; generate the final report; and check correctness and formatting.
- Task-end retrospective mode: when the user says `任务结束` or asks to reflect on the completed report task, summarize task problems first, present them to the user, then integrate approved lessons into this skill's existing logic.

Load detailed runbooks from `references/` only as needed:

- `references/workflow.md` for the full phase-by-phase runbook.
- `references/initialization.md` for first-run behavior.
- `references/project_structure.md` for directory roles.
- `references/template_handling.md` for template-based reports.
- `references/quality_checklist.md` for final checking.

# Project State Detection

Every invocation must begin with project state detection.

Inspect the current working directory. If it contains all of the following, treat it as an initialized report project and enter Report-Writing Mode:

- `task_config.yaml`
- `input/`
- `work/`
- `output/`

If any required item is missing, enter First-Run Initialization Mode.

If some files exist but the structure is incomplete, do not delete user files. Create only the missing directories and starter files. If a starter file already exists, do not overwrite it unless it is empty or the user explicitly asks. If the current directory contains unrelated files, do not move, rename, or delete them.

# First-Run Initialization Mode

Run `scripts/init_report_project.py` from this skill against the current working directory. The script must create missing directories and starter files from `assets/`.

Required structure after initialization:

```text
./
+-- README.md
+-- task_config.yaml
+-- input/
|   +-- problems/
|   +-- references/
|   +-- template/
+-- work/
|   +-- task_inventory.md
|   +-- notes.md
|   +-- draft.md
|   +-- checks.md
|   +-- code/
|   +-- assets/
+-- output/
```

Initialization rules:

- Create missing directories.
- Create missing starter files from `assets/`.
- Do not overwrite non-empty existing files.
- Do not solve the task.
- Do not scan for answers.
- Do not generate a final report.
- Stop after initialization.
- Tell the user exactly what to put into each folder.

After initialization, report created files, skipped files, and next steps. The expected closing message is:

```text
The report project has been initialized.
Next steps:
1. Put problem files into input/problems/.
2. Put reference materials into input/references/.
3. Put template files into input/template/ if any.
4. Edit task_config.yaml.
5. Invoke this skill again to write the report.
```

# Task-End Retrospective Mode

Use this mode when the user says `任务结束`, says the report task is finished, or asks to summarize problems from the current task and update the skill.

Rules:

- First summarize the issues for the user before editing skill files.
- The summary must include: problem, impact, root cause, preventive rule, and the target section/file where the rule should live.
- If the user only asks for a summary or says `任务结束`, stop after the summary and ask whether to apply the proposed skill updates.
- If the user explicitly asks to summarize and then apply changes in the same request, present the summary first in a visible message, then edit the skill.
- Integrate lessons into this `report-workflow` skill. Do not create a separate retrospective skill unless the user explicitly requests a separate skill.
- Update the existing logical locations rather than appending disconnected lessons: core rules in `SKILL.md`, detailed steps in `references/workflow.md`, template-specific behavior in `references/template_handling.md`, validation rules in `references/quality_checklist.md`, and starter checks in `assets/` when future initialized projects should inherit them.
- Avoid duplicate or contradictory instructions. Strengthen the existing rule in place when possible.
- Validate the skill update by searching modified files for stale wording, duplicate headings, obvious placeholders, and missing cross-layer checks.

# Report-Writing Mode

When the project is initialized, execute the workflow in this exact order:

1. Read `task_config.yaml` first.
2. Scan `input/problems/`.
3. Scan `input/references/`.
4. Scan `input/template/` if `has_template` is true or template files exist.
5. If a template or template-like source document will be used, copy it into a working-template area under `work/assets/template_working/` before editing.
6. Create or update `work/task_inventory.md`.
7. Create or update `work/notes.md`.
8. Draft answers in `work/draft.md`.
9. Run a content-first review in `work/checks.md`: coverage, correctness, derivations, computations, citations, assumptions, notation, and formula source.
10. Revise `work/draft.md` until the content review passes.
11. Use Python/code only if helpful or required.
12. Apply the layout pass: decide headings, paragraph flow, lists, tables, equation display, captions, and template placement after content is already correct.
13. Edit the working-template copy in `work/assets/template_working/` and export/copy the finished deliverable to `output/`.
14. Perform final correctness check in `work/checks.md`.
15. Perform formatting check in `work/checks.md`.
16. Write final summary in `work/checks.md`.

Hard requirements:

- Do not write the final report before creating or updating `work/task_inventory.md`.
- Do not write the final report before drafting answers in `work/draft.md`.
- Do not rebuild a template-backed report from scratch when the source template can be copied and edited.
- Do not edit an `input/` file directly; copy the template/source document into `work/assets/template_working/` first and modify that working copy.
- Create or update `work/checks.md` before completion.
- Treat report writing as two passes: content first, layout second. Do not optimize bulleting, spacing, table layout, DOCX styling, or visual polish until the draft content has passed coverage and correctness review.
- Preserve a LaTeX source form for formulas during drafting and checking. Use LaTeX delimiters for formulas only in Markdown/LaTeX outputs. For DOCX, LaTeX is an intermediate source only: convert it into native/compatible Word equations or another clean rendered formula form before final delivery.
- Make every final answer section traceable to exactly one item in `work/task_inventory.md`, unless it is a report-level section such as title page, objective, summary, or references.
- Do not merge multiple requested sub-questions into one answer section. If the source asks for `3.4(a)(b)(c)`, create separate inventory items, draft sections, and final report sections for `3.4(a)`, `3.4(b)`, and `3.4(c)`.
- Do not hide sub-question answers inside a single paragraph, table cell, or broad section. A reader must be able to visually locate the answer to each sub-question by its original label.
- Shared setup, shared definitions, or shared derivations may appear once before related sub-questions, but the answer, result, and verification for each sub-question must remain under that sub-question's own label.
- Preserve the original problem numbering and sub-question labels in headings wherever possible.
- Treat configuration and user instructions as internal process rules unless the user explicitly asks them to appear in the final report. Do not leak phrases such as paraphrase instructions, data-adjustment instructions, "source report", "processed", "baseline", "as requested", or similar workflow/meta language into the final deliverable.
- For template-backed paraphrase or rewrite tasks, preserve the template's information density: section order, figures, tables, appendices, logs, formulas, captions, and important explanatory detail must be matched or deliberately replaced, not summarized away.
- If an appendix, table, code listing, log, or data sheet appears in the template or required references, recreate an equivalent level of detail in the final report. Do not replace a full appendix/log/table with a short summary unless the user explicitly asks for an abridged report.
- Save the final report under `output/`.

# Required Project Structure

The initialized project must contain:

- `README.md`
- `task_config.yaml`
- `input/problems/`
- `input/references/`
- `input/template/`
- `work/task_inventory.md`
- `work/notes.md`
- `work/draft.md`
- `work/checks.md`
- `work/code/`
- `work/assets/`
- `output/`

See `references/project_structure.md` for file purposes and boundaries.

# Directory and File Boundaries

`input/` is read-only. `work/` is for intermediate artifacts. `output/` is for final deliverables only.

Rules:

- Do not modify original problem files.
- Do not modify original reference files.
- Do not modify original template files in place.
- It is allowed and preferred to modify copies of input templates or template-like source documents after they have been copied into `work/assets/template_working/`.
- If a problem or reference file is actually the required answer sheet/template, treat it as a template-like source: copy it to `work/assets/template_working/`, preserve its structure, edit the copy, then save the completed deliverable under `output/`.
- Do not write temporary files to `output/`.
- Do not write final reports outside `output/`.
- Do not delete intermediate files unless explicitly instructed.
- Do not overwrite non-empty user files during initialization.
- Do not invent missing problems.
- Do not silently ignore ambiguity.
- Do not claim code was run unless it was actually run successfully.
- Do not leave TODO, FIXME, placeholder, or internal notes in the final report.

# Configuration Rules

Read `task_config.yaml` before scanning inputs. Respect these keys:

- `task_name`
- `task_type`
- `language`
- `final_format`
- `has_template`
- `template_filename`
- `python_env`
- `allow_web`
- `allow_modify_input`
- `style_requirements`
- `citation_requirements`
- `special_instructions`
- `problem_dir`
- `reference_dir`
- `template_dir`
- `work_dir`
- `output_dir`

If configuration is missing or ambiguous, record the issue in `work/notes.md` and proceed only when a reasonable assumption is safe. If a required decision would change the final answer materially, ask the user.

Configuration privacy rule: `special_instructions`, style notes, transformation rules, anonymization rules, data-adjustment rules, and internal tool choices guide the work but are not report content. Record them in `work/notes.md` or `work/checks.md`, never in the final deliverable, unless the user explicitly requests disclosure.

# Reading Phase

Read problem files from `problem_dir`, reference files from `reference_dir`, and templates from `template_dir` only when configured or present. Preserve source filenames and paths in notes. If a file format cannot be read, record the limitation in `work/notes.md` and `work/checks.md`.

# Task Inventory Phase

Create or update `work/task_inventory.md` before drafting final answers. Include every question, sub-question, required output, source file, relevant references, computations, figures/tables, pitfalls, and status. Preserve original numbering.

Sub-question granularity is mandatory:

- Treat every lettered, numbered, roman-numeral, bullet, or separately requested deliverable as its own inventory item.
- Do not collapse ranges such as `(a)-(f)` into a single item. Expand them into `(a)`, `(b)`, `(c)`, `(d)`, `(e)`, and `(f)`.
- If a handout lists several parts together, split them before drafting and keep the same labels in `work/task_inventory.md`, `work/draft.md`, and the final report.
- If the exact text of a sub-question cannot be read, record that item separately with the unreadability limitation instead of merging it into a neighboring question.
- If a problem has multiple required products under one label, such as a derivation, a plot, a table, and a discussion, keep them tied to that label but list each product explicitly in the inventory item.
- Before final generation, compare the inventory labels against the final report headings or visible labels. Any missing label is a blocking formatting error.

# Notes, Pitfalls, and Ambiguities Phase

Create or update `work/notes.md` with global notes, reference mappings, pitfalls, ambiguities, assumptions, notation, units, and citation notes. Do not silently resolve ambiguous requirements; record the chosen assumption or ask the user when necessary.

# Draft Answer Phase

Draft answers in `work/draft.md` before creating final output. Use the inventory numbering. Include problem restatement, solution, computation or derivation, final result, verification, and notes for the final report.

Each required sub-question must have its own draft subsection. Do not write combined subsections such as `Exercise 3.4(a-c)` unless the original source itself has no separable sub-prompts. Shared setup may be placed before the sub-question subsections, but each sub-question still needs an explicit answer under its own label.

For each sub-question draft subsection, include a short final-answer target such as result, conclusion, proof endpoint, or required artifact. Do not rely on a neighboring subsection to carry the answer.

Formula drafting requirements:

- Write formulas in LaTeX source form in `work/draft.md`.
- Use inline math delimiters such as `$...$` for short formulas and display delimiters such as `$$...$$` or `\(...\)`/`\[...\]` consistently according to the final format.
- Keep equation labels, variable definitions, units, and derivation steps close to the formulas they support.
- Do not assume Word will automatically convert raw LaTeX delimiters into equations. If the final format is DOCX, explicitly convert or render the LaTeX draft formulas during final generation.
- Do not mix ad hoc plain-text math, screenshots, and LaTeX-derived formulas in the same final report unless a tool limitation forces it and the limitation is recorded in `work/checks.md`.

# Content-First Review and Layout Planning

Before final report generation or template placement, perform a content-first review in `work/checks.md` and revise `work/draft.md` until it passes.

Content review must check:

- Every inventory item has a complete draft answer.
- Each answer directly addresses the prompt and has a visible final result, conclusion, proof endpoint, or required artifact.
- Reasoning, derivations, computations, citations, assumptions, units, notation, figures, and tables are correct and sufficient.
- Formulas have a LaTeX source form and consistent notation.
- No internal prompt/config/process language has entered final-facing prose.

Only after the content review passes, perform the layout pass. The layout pass must improve readability without changing meaning:

- Convert rough draft structure into appropriate headings, paragraphs, lists, tables, equation blocks, captions, and appendices.
- Use bullet or numbered lists only when items are parallel, discrete, and easier to scan than prose.
- Avoid excessive fragmented bullets, one-item lists, deeply nested lists, and lists that hide reasoning that should be a paragraph.
- Prefer paragraphs for explanations, methods, and analysis; prefer tables for comparisons, parameters, datasets, or repeated structured results.
- Keep sub-question labels visible even when combining shared setup text.
- Record any layout compromise caused by template or tooling limits in `work/checks.md`.

# Computation and Python Rules

Use code only when it improves correctness, reproducibility, data processing, calculations, figure generation, or format conversion. Place scripts in `work/code/` and generated intermediate assets in `work/assets/`. Record commands run, outputs relied on, and limitations in `work/notes.md` or `work/checks.md`. Do not claim a computation was run unless it actually completed successfully.

# Template Handling Rules

If `has_template` is true, template files exist, `template_filename` names a document, or a problem/reference document is visibly an answer sheet/report shell, follow `references/template_handling.md`. Never edit originals in `input/`. Copy the selected template-like file into `work/assets/template_working/` before making changes, preserve required structure and styling where possible, and export/copy the completed working copy to `output/`.

You may use `scripts/prepare_working_template.py <project-root>` from this skill to create the working copy. The script searches `template_dir`, `problem_dir`, and `reference_dir`, honors `template_filename` when possible, and prints the source and working-copy paths.

If a template contains old report content, first separate template structure from old content. Reuse the template's layout, headings, metadata fields, styles, captions, and placeholders, but do not reuse old answer text unless it is explicitly still applicable or the user asks to keep it. Do not substantially redesign the template unless the user explicitly requests a redesign or the template cannot support the required report.

For template-backed paraphrase or rewrite tasks:

- Create a template fidelity inventory before drafting: list every section, subsection, figure, table, appendix, formula block, log/data listing, and repeated answer pattern that must be preserved or replaced.
- Paraphrase content at comparable depth. Do not compress detailed procedure, analysis, appendix, or discussion sections into short summaries when the user asks to preserve details.
- Keep figures and tables at the same granularity where possible. If a source table/log has many rows or columns, the final report needs an equivalent full table/log, not only selected rows.
- Do not expose transformation rules in the final prose. For example, if values are adjusted, present them as normal report results and keep the adjustment rule only in work notes/checks.

# Final Report Generation

Generate the final report only after `work/task_inventory.md` and `work/draft.md` are updated. Save final deliverables under `output/` using the configured `final_format` when feasible. Ensure every final section maps back to `work/task_inventory.md`.

Do not begin final formatting from an unreviewed draft. First complete the content-first review, revise content issues in `work/draft.md`, then apply the layout pass to produce the final deliverable.

Before writing final prose, separate report content from process metadata. Report content includes experiment objectives, methods, results, analysis, conclusions, citations, appendices, and required answers. Process metadata includes prompt wording, transformation instructions, "paraphrase" requests, data-adjustment rules, tool limitations, file paths, and source/template labels. Process metadata belongs in `work/notes.md` and `work/checks.md`, not in `output/`.

For template-backed reports, the normal final-generation path is:

1. Use the working template copy in `work/assets/template_working/`.
2. Replace placeholders, old answers, blank answer areas, metadata fields, figures, and tables in place.
3. Preserve the template's structure, styles, headers/footers, numbering, and media relationships whenever feasible.
4. Save or copy the finished document from the working area to `output/`.

Only create a new document from scratch when the template cannot be edited with available tools, the format is unsupported, or the user explicitly asks for a rebuilt document. Record that limitation in `work/checks.md`.

In the final report, preserve sub-question granularity from the inventory and draft. A combined high-level exercise introduction is allowed, but answers must still appear under separate headings or labels for each required sub-question.

Final formula requirements:

- Markdown and LaTeX final outputs must keep formulas as LaTeX with consistent inline and display delimiters.
- DOCX final outputs must not show raw `$...$`, `$$...$$`, `\(...\)`, `\[...\]`, or LaTeX commands as ordinary text unless the user explicitly requested LaTeX source text.
- DOCX final outputs should be produced from the LaTeX source equations in the draft and converted to Word-compatible equation objects when feasible.
- If conversion is not feasible, choose the most readable fallback allowed by the requested format and record the limitation in `work/checks.md`.
- Never silently replace formulas with vague prose summaries.

## DOCX Output Standards

When `final_format` is `docx`, when a DOCX template is used, or when the user asks for a Word document, the final document must use a restrained, polished academic/report layout. Do not improvise decorative layouts, random spacing, inconsistent fonts, or ad hoc equation formatting.

Default DOCX layout when no template style is mandatory:

- Use a clean A4 page layout with approximately 2.54 cm margins on all sides.
- Use a readable body font such as Times New Roman, Cambria, Calibri, or the template's body font, at 10.5-12 pt.
- Use consistent heading styles rather than manually bolded paragraphs. Heading levels must reflect the original problem hierarchy.
- Use line spacing around 1.15-1.5 and avoid cramped or overly loose paragraphs.
- Keep paragraph spacing consistent. Do not add repeated blank paragraphs to create layout.
- Use page numbers when the report is longer than one page.
- Keep tables full-width or naturally sized, with readable alignment, header rows, and consistent borders.
- Use numbered captions for figures and tables when figures or tables are present.
- Preserve a visually calm, professional document. Avoid excessive colors, oversized headings, random indentation, text boxes, floating decorative shapes, and mixed font families.

DOCX sub-question layout requirements:

- Each inventory item must appear as a visible heading, numbered heading, labeled paragraph, or table row with the exact original label.
- Do not combine labels such as `(a)-(c)`, `(a-c)`, `Part 1-3`, or `Questions 1 and 2` unless the source itself has a single inseparable prompt.
- If the report uses tables for answers, each sub-question must have its own row or clearly separated block, and formulas/results must remain readable.

DOCX equation and formula standards:

- Use standard Word-compatible equation formatting when possible, such as OMML equations produced by a DOCX library, MathType-compatible objects, or a reliable conversion from LaTeX.
- Treat LaTeX in the draft as the equation source of truth, then convert or render it consistently for the DOCX. The final Word document should look like a polished report with displayed equations, not a LaTeX source file pasted into Word.
- If native equation objects are not feasible, use clean linear math notation consistently and record the limitation in `work/checks.md`.
- Display important equations on their own line, centered or consistently indented, with optional equation numbers aligned consistently when needed.
- Keep inline formulas short and readable. Do not paste raw, unrendered LaTeX into the final DOCX unless the user explicitly requested LaTeX source text.
- Use consistent notation, units, subscripts, superscripts, fractions, vectors, matrices, and significant figures.
- Do not use screenshots of equations unless no editable alternative is feasible; if used, ensure they are high-resolution and aligned with the text.

DOCX generation workflow requirements:

- Prefer reusing a DOCX template's styles when a template is supplied.
- If creating a DOCX from scratch, define or apply stable styles for title, headings, body text, captions, tables, and equations before inserting content.
- Open or inspect the generated DOCX structure when possible, or otherwise verify the produced file exists and is not empty.
- Record DOCX layout, equation handling method, and any conversion limitations in `work/checks.md`.

# Correctness Check

Update `work/checks.md` with coverage and correctness checks. Verify that every problem and sub-question is answered, assumptions are stated, reasoning is complete, computations are reproducible, units and notation are consistent, and referenced figures/tables match the report.

Explicitly check that no required sub-question was merged into a neighboring answer or hidden inside a broad exercise summary.

Before layout work, explicitly record that the content-first review passed or list the remaining content fixes. Do not treat a visually polished report as complete while content issues remain.

For template-backed reports, explicitly compare final report structure against the template fidelity inventory. Any missing section, figure, table, appendix, log/data listing, formula block, or substantial explanation is a correctness issue unless the omission is requested or recorded with a reason.

# Formatting Check

Update `work/checks.md` with formatting checks. Verify the final file exists under `output/`, template formatting is preserved when applicable, headings and numbering are consistent, figures/tables have captions when needed, equations are readable, citations are consistent, and no TODO/FIXME/placeholders/internal notes remain.

Check whether the layout choices are appropriate for the content: lists should be purposeful and parallel, explanatory paragraphs should not be chopped into bullets, tables should not be used to hide long reasoning, and equation blocks should remain readable.

When a template was used, check that the final report preserves the template's main structure and styles and that old template content has been replaced or intentionally retained with a recorded reason.

Perform a prompt/meta leakage scan on the final deliverable. Search or inspect for configuration-only language such as prompt instructions, "paraphrase", "source report", "baseline source", "processed", "offset", "as requested", data-adjustment rules, local file paths, and tool/process notes. Remove such language from the final deliverable unless it is genuinely part of the assignment or explicitly requested by the user.

For DOCX outputs, explicitly check page layout, margins, font consistency, heading styles, paragraph spacing, table readability, figure/table captions, visible sub-question separation, and equation rendering. If any DOCX equation is raw LaTeX, an image fallback, or plain-text math because native equations were not feasible, record that limitation.

# Final Summary

Write the final summary in `work/checks.md` and tell the user:

- Final output path.
- Intermediate files updated.
- Code/assets used.
- Checks performed.
- Known limitations.
- Assumptions made.

# Failure Handling

If initialization fails, report the exact missing or failed operation and do not attempt report writing. If report writing is blocked by missing problems, unreadable inputs, missing required template files, or unresolved high-impact ambiguity, record the blocker in `work/notes.md` or `work/checks.md` when possible and ask the user for the missing information.

# Prohibited Behaviors

- Do not skip project state detection.
- Do not write a report during first-run initialization.
- Do not scan nonexistent problem files during initialization.
- Do not modify files under `input/`.
- Do not treat `input/` read-only status as a reason to rebuild a template-backed report from scratch; copy the file into `work/assets/template_working/` and edit that copy.
- Do not overwrite non-empty user files during initialization.
- Do not write final deliverables outside `output/`.
- Do not leave unchecked final output.
- Do not omit `work/task_inventory.md`, `work/draft.md`, or `work/checks.md`.
- Do not invent missing questions, references, citations, results, or computations.
- Do not leak user prompt text, transformation rules, data-adjustment instructions, internal file paths, or tool/process notes into the final deliverable.
- Do not reduce a detailed template appendix, log, table, or procedure section to a brief summary when the user requested a detailed paraphrase or template-faithful rewrite.

# Completion Criteria

First-run initialization is complete only when required directories and starter files are created or safely skipped, the user receives created/skipped lists, and the next steps are shown.

Report-writing mode is complete only when:

- `work/task_inventory.md` is current.
- `work/notes.md` records pitfalls, ambiguities, and assumptions.
- `work/draft.md` contains drafted answers.
- The final report is saved under `output/`.
- `work/checks.md` contains coverage, correctness, formatting, and final summary sections.
- The final response summarizes outputs, checks, assumptions, and limitations.
