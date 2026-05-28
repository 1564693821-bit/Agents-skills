---
name: report-workflow
description: A self-initializing report-writing workflow. Use this skill when the user wants Codex to create or use a standardized report project for homework reports, experiment reports, course reports, technical reports, or template-based answer files. On first use, the skill detects whether the current directory is initialized; if not, it creates input/, work/, output/, task_config.yaml, and starter files, then stops. On later use, it reads problems, references, templates, drafts answers, generates the final report, and performs correctness and formatting checks.
---

# Purpose

Use this skill to manage a standardized report-writing project from initialization through final checked deliverable. The skill has two modes:

- First-run initialization mode: create the project structure and starter files, then stop.
- Report-writing mode: read configuration, problems, references, and templates; inventory tasks; draft answers; generate the final report; and check correctness and formatting.

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

# Report-Writing Mode

When the project is initialized, execute the workflow in this exact order:

1. Read `task_config.yaml` first.
2. Scan `input/problems/`.
3. Scan `input/references/`.
4. Scan `input/template/` if `has_template` is true or template files exist.
5. Create or update `work/task_inventory.md`.
6. Create or update `work/notes.md`.
7. Draft answers in `work/draft.md`.
8. Use Python/code only if helpful or required.
9. Generate the final report in `output/`.
10. Perform correctness check in `work/checks.md`.
11. Perform formatting check in `work/checks.md`.
12. Write final summary in `work/checks.md`.

Hard requirements:

- Do not write the final report before creating or updating `work/task_inventory.md`.
- Do not write the final report before drafting answers in `work/draft.md`.
- Create or update `work/checks.md` before completion.
- Make every final answer section traceable to exactly one item in `work/task_inventory.md`, unless it is a report-level section such as title page, objective, summary, or references.
- Do not merge multiple requested sub-questions into one answer section. If the source asks for `3.4(a)(b)(c)`, create separate inventory items, draft sections, and final report sections for `3.4(a)`, `3.4(b)`, and `3.4(c)`.
- Do not hide sub-question answers inside a single paragraph, table cell, or broad section. A reader must be able to visually locate the answer to each sub-question by its original label.
- Shared setup, shared definitions, or shared derivations may appear once before related sub-questions, but the answer, result, and verification for each sub-question must remain under that sub-question's own label.
- Preserve the original problem numbering and sub-question labels in headings wherever possible.
- Save the final report under `output/`.
- Style requirements, including requests such as "simple", "concise", "clean", or "brief", may only affect wording density and visual restraint. They must never remove required problem statements, code, derivations, formulas, figures, tables, verification, citations, or any deliverable named in the prompt or inventory.
- When a template is used, treat the task as filling the template, not redesigning it. Preserve the template's existing styles, font sizes, font families, margins, spacing, heading definitions, numbering, headers/footers, captions, tables, placeholders, and section order unless the user explicitly asks to redesign them or exact preservation is technically impossible.
- If exact template formatting cannot be preserved, record the specific limitation in `work/checks.md`; do not silently substitute a newly styled document.

Observed failure prevention requirements:

- Build an artifact traceability matrix before final generation. For every inventory item, record whether code, commands, formulas, derivations, numerical outputs, figures/tables, verification, and discussion are required, where they are drafted, and where they appear in the final report.
- Code required by a prompt must appear under the corresponding sub-question in the final report. A consolidated appendix is allowed only as a supplement, not as a replacement for per-question code.
- Plot- or image-heavy tasks require a figure plan before generation. The plan must map each figure filename to exactly one sub-question unless a shared figure is explicitly justified in `work/notes.md`.
- Do not reuse the same figure for multiple sub-questions unless the source prompt explicitly asks for one shared figure or the reuse is documented and clearly correct.
- Generated figures must be semantically checked against their captions, code, axes, legends, source data, and the sub-question prompt. Duplicate filenames, duplicate captions, repeated images, stale images, or figures showing the wrong quantity are blocking errors.
- Explanations must be deep enough to answer the question, interpret the output, and connect the result to the relevant theory. A report is incomplete if it contains only code and figures without interpretation, even when all artifacts are present.
- When a reference or peer report is provided, compare it against the primary problem statement and theory before adopting its content. Record differences and decide which source is authoritative.
- For DOCX outputs, verify both visible content and package hygiene: the number of visible figure captions, embedded images, image relationships, and media files should agree unless a documented template artifact requires otherwise.

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

Interpret `style_requirements` as presentation guidance only. For example, requests for a concise, simple, clean, or minimal style mean concise prose and restrained formatting; they do not permit omitting required code listings, calculations, derivations, plots, explanations, checks, or sub-question answers.

# Reading Phase

Read problem files from `problem_dir`, reference files from `reference_dir`, and templates from `template_dir` only when configured or present. Preserve source filenames and paths in notes. If a file format cannot be read, record the limitation in `work/notes.md` and `work/checks.md`.

Source priority:

- Primary problem files define the required questions and deliverables.
- Course handouts, rubrics, and explicit user instructions outrank peer reports, old reports, solution examples, and generated drafts.
- Reference books and official course materials are used to interpret and verify the primary problem statement.
- Peer reports or previous submissions are comparison material, not the task source, unless the user explicitly says to copy their structure or content.
- If a peer report includes extra sub-questions not present in the primary problem file, record the difference and do not add those questions to the final report without user approval.
- If a peer report disagrees with the primary problem file, theory, or reproducible computation, record the disagreement and prefer the primary problem file plus verified theory/computation.

Reference comparison requirements:

- When a peer/example report is supplied, create or update a comparison note in `work/` that lists differences in problem coverage, code approach, figure coverage, numerical results, and conclusions.
- For code-driven or plot-driven disagreements, run an independent calculation when feasible and record the numerical evidence.
- Do not treat visual similarity to a peer report as proof of correctness. Check whether the plot is required, distinct, labeled correctly, and generated from the right data.

# Task Inventory Phase

Create or update `work/task_inventory.md` before drafting final answers. Include every question, sub-question, required output, source file, relevant references, computations, figures/tables, pitfalls, and status. Preserve original numbering.

Sub-question granularity is mandatory:

- Treat every lettered, numbered, roman-numeral, bullet, or separately requested deliverable as its own inventory item.
- Do not collapse ranges such as `(a)-(f)` into a single item. Expand them into `(a)`, `(b)`, `(c)`, `(d)`, `(e)`, and `(f)`.
- If a handout lists several parts together, split them before drafting and keep the same labels in `work/task_inventory.md`, `work/draft.md`, and the final report.
- If the exact text of a sub-question cannot be read, record that item separately with the unreadability limitation instead of merging it into a neighboring question.
- If a problem has multiple required products under one label, such as a derivation, a plot, a table, and a discussion, keep them tied to that label but list each product explicitly in the inventory item.
- Before final generation, compare the inventory labels against the final report headings or visible labels. Any missing label is a blocking formatting error.
- For each inventory item, explicitly list required artifacts such as code, commands, formulas, derivations, figures, tables, numerical outputs, verification, discussion, and citations. If none are required, state that explicitly.
- For each inventory item, include a final-report artifact map with planned locations for code, figures/tables, formulas/derivations, numerical outputs, verification, and discussion. Use `not required` only after checking the prompt.
- For each planned figure/table, include a short purpose statement, expected axes or columns, source data/code, and the sub-question label it supports.
- Before final generation, verify that every listed required artifact appears in `work/draft.md`. Missing required artifacts are a blocking correctness error, even if the requested style is concise.

# Notes, Pitfalls, and Ambiguities Phase

Create or update `work/notes.md` with global notes, reference mappings, pitfalls, ambiguities, assumptions, notation, units, and citation notes. Do not silently resolve ambiguous requirements; record the chosen assumption or ask the user when necessary.

# Draft Answer Phase

Draft answers in `work/draft.md` before creating final output. Use the inventory numbering. Include problem restatement, solution, computation or derivation, final result, verification, and notes for the final report.

Each required sub-question must have its own draft subsection. Do not write combined subsections such as `Exercise 3.4(a-c)` unless the original source itself has no separable sub-prompts. Shared setup may be placed before the sub-question subsections, but each sub-question still needs an explicit answer under its own label.

For each sub-question draft subsection, include a short final-answer target such as result, conclusion, proof endpoint, or required artifact. Do not rely on a neighboring subsection to carry the answer.

Completeness overrides brevity. If the user asks for a concise style, compress wording after all required content is present; do not omit code, equations, derivation steps needed for correctness, generated figures/tables, or verification required by the problem.

Depth requirements:

- For computational questions, include the setup, method, code or command, result, and interpretation of the result.
- For figure questions, explain what the figure shows and how it answers the prompt. A caption alone is not enough.
- For proof or derivation questions, include enough intermediate steps to make the conclusion auditable.
- For comparison questions, explicitly state the comparison criteria and the conclusion.
- For listening, visual, or qualitative tasks, describe the observed result and connect it to the relevant mathematical property.

# Computation and Python Rules

Use code only when it improves correctness, reproducibility, data processing, calculations, figure generation, or format conversion. Place scripts in `work/code/` and generated intermediate assets in `work/assets/`. Record commands run, outputs relied on, and limitations in `work/notes.md` or `work/checks.md`. Do not claim a computation was run unless it actually completed successfully.

Computation validation requirements:

- For every generated figure, keep the code or command that generated it in `work/code/` or the relevant draft section.
- For every numerical claim that can be verified cheaply, run an independent check or record the formula-based verification.
- When comparing two implementations or reports, verify the disagreement with theory, a small numerical test, or both.
- If generated code is included in the final report, ensure the included code matches the code used to generate the reported results, or record any intentional difference.

Figure and asset validation requirements:

- Store generated figures under `work/assets/` with stable, descriptive filenames tied to question labels.
- After figure generation, inspect the figure list and ensure no required figure is missing and no stale figure is being referenced.
- For multi-figure reports, check for repeated images using filenames and, where feasible, file hashes or image dimensions/content summaries.
- Check captions against the actual image content. The caption must name the correct question, quantity, signal/system, and comparison.
- For plots, verify axes labels, units, legends, ranges, and whether magnitude/phase/time-domain data match the prompt.
- If final DOCX/PDF embeds images, verify visible figure count and embedded media count. Orphaned media from templates or previous outputs must be removed when feasible.

# Template Handling Rules

If `has_template` is true or template files exist, follow `references/template_handling.md`. Never edit originals in `input/template/`. Copy or generate a final file in `output/`, preserve required structure and styling by default, and record unsupported template limitations in `work/checks.md`.

If a template contains old report content, first separate template structure from old content. Reuse the template's layout, headings, metadata fields, styles, captions, and placeholders, but do not reuse old answer text unless it is explicitly still applicable or the user asks to keep it. Do not substantially redesign the template unless the user explicitly requests a redesign or the template cannot support the required report.

Template filling is an in-place content replacement task. The default operation is to replace placeholder text, old answer text, table cell content, figure slots, and metadata field values while keeping the containing paragraph/run/table/caption/heading style unchanged. Do not change font size, font family, bold/italic state, paragraph spacing, alignment, margins, page size, heading style definitions, numbering style, or table style merely to make the document look cleaner.

# Final Report Generation

Generate the final report only after `work/task_inventory.md` and `work/draft.md` are updated. Save final deliverables under `output/` using the configured `final_format` when feasible. Ensure every final section maps back to `work/task_inventory.md`.

In the final report, preserve sub-question granularity from the inventory and draft. A combined high-level exercise introduction is allowed, but answers must still appear under separate headings or labels for each required sub-question.

Do not shorten the final report by deleting required artifacts. Required source code, command snippets, parameter values, plots, tables, derivations, and verification text must appear in the final report when the prompt asks for them, even under a concise style requirement.

Before considering the final report complete, apply two blocking gates:

- Content completeness gate: every required artifact listed in `work/task_inventory.md` must appear in the final report or be documented as impossible with a reason in `work/checks.md`.
- Template fidelity gate: when a template is used, the final report must preserve the template shell's structure and formatting, with every unavoidable deviation documented in `work/checks.md`.
- Artifact placement gate: required code, figures, formulas, and explanations must appear under the correct sub-question, not only in an appendix, summary, or neighboring section.
- Figure correctness gate: every final figure must be present, distinct unless documented, correctly captioned, and visually/semantically matched to the sub-question.
- Reference-difference gate: if a supplied peer/example report differs from the current report in coverage, code, figures, or conclusions, the difference must be recorded and resolved before completion.

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
- If native equation objects are not feasible, use clean linear math notation consistently and record the limitation in `work/checks.md`.
- Display important equations on their own line, centered or consistently indented, with optional equation numbers aligned consistently when needed.
- Keep inline formulas short and readable. Do not paste raw, unrendered LaTeX into the final DOCX unless the user explicitly requested LaTeX source text.
- Use consistent notation, units, subscripts, superscripts, fractions, vectors, matrices, and significant figures.
- Do not use screenshots of equations unless no editable alternative is feasible; if used, ensure they are high-resolution and aligned with the text.

DOCX generation workflow requirements:

- Prefer reusing a DOCX template's styles when a template is supplied.
- When a DOCX template is supplied, copy the template and replace content inside existing styled containers where feasible. Preserve run-level and paragraph-level formatting of placeholders/old content unless a specific content type requires a minimal local adjustment, such as inserting a readable equation object or a generated figure into an existing figure slot.
- Do not globally redefine DOCX styles, normalize fonts, change heading sizes, alter margins, or rebuild the document from scratch when the template can be edited in place.
- If creating a DOCX from scratch, define or apply stable styles for title, headings, body text, captions, tables, and equations before inserting content.
- Open or inspect the generated DOCX structure when possible, or otherwise verify the produced file exists and is not empty.
- Record DOCX layout, equation handling method, and any conversion limitations in `work/checks.md`.

# Correctness Check

Update `work/checks.md` with coverage and correctness checks. Verify that every problem and sub-question is answered, assumptions are stated, reasoning is complete, computations are reproducible, units and notation are consistent, and referenced figures/tables match the report.

Explicitly check that no required sub-question was merged into a neighboring answer or hidden inside a broad exercise summary.

Explicitly check that brevity or style requirements did not cause omission of required code, derivations, formulas, figures, tables, computations, verification, citations, or other deliverables.

Explicitly check that every code block, formula, numerical result, figure, and table listed in the inventory appears under the correct final-report sub-question.

Explicitly check that figures are not repeated by mistake, do not show stale outputs, and match their captions and discussion.

If a peer/example report was supplied, explicitly check and record where the current report intentionally follows it, intentionally differs from it, or corrects it.

# Formatting Check

Update `work/checks.md` with formatting checks. Verify the final file exists under `output/`, template formatting is preserved when applicable, headings and numbering are consistent, figures/tables have captions when needed, equations are readable, citations are consistent, and no TODO/FIXME/placeholders/internal notes remain.

When a template was used, check that the final report preserves the template's main structure and styles and that old template content has been replaced or intentionally retained with a recorded reason.

When a template was used, explicitly check that font sizes, font families, paragraph spacing, margins, heading style definitions, numbering, headers/footers, captions, and table styles were preserved except for documented technical limitations or user-requested redesign.

For DOCX outputs, explicitly check page layout, margins, font consistency, heading styles, paragraph spacing, table readability, figure/table captions, visible sub-question separation, and equation rendering. If any DOCX equation is raw LaTeX, an image fallback, or plain-text math because native equations were not feasible, record that limitation.

For DOCX outputs with images, explicitly check visible captions, embedded image references, image relationships, and media files. Remove unused template images or record why they remain.

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
- Do not overwrite non-empty user files during initialization.
- Do not write final deliverables outside `output/`.
- Do not leave unchecked final output.
- Do not omit `work/task_inventory.md`, `work/draft.md`, or `work/checks.md`.
- Do not invent missing questions, references, citations, results, or computations.
- Do not interpret concise/simple style requests as permission to omit required content.
- Do not change template typography, spacing, margins, heading definitions, numbering, or table styles merely for aesthetics.

# Completion Criteria

First-run initialization is complete only when required directories and starter files are created or safely skipped, the user receives created/skipped lists, and the next steps are shown.

Report-writing mode is complete only when:

- `work/task_inventory.md` is current.
- `work/notes.md` records pitfalls, ambiguities, and assumptions.
- `work/draft.md` contains drafted answers.
- The final report is saved under `output/`.
- `work/checks.md` contains coverage, correctness, formatting, and final summary sections.
- The final response summarizes outputs, checks, assumptions, and limitations.
