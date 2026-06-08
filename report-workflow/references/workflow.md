# Report Workflow Runbook

## Phase 0: Project State Detection

Goal: Decide whether to initialize or write the report.

Inputs: Current working directory.

Outputs: Mode decision.

Required actions:

- Check for `task_config.yaml`, `input/`, `work/`, and `output/`.
- If all exist, enter report-writing mode.
- If any are missing, enter initialization mode.

Stop conditions:

- Stop this phase once the mode is known.

Common mistakes:

- Skipping detection.
- Treating unrelated files as report inputs.
- Deleting or moving existing files.

## Phase 1: First-run Initialization

Goal: Create a standard project structure.

Inputs: Skill `assets/` templates and `scripts/init_report_project.py`.

Outputs: `README.md`, `task_config.yaml`, `input/`, `work/`, and `output/`.

Required actions:

- Run the initialization script from the target project root.
- Create missing directories.
- Create missing starter files.
- Skip non-empty existing files.
- Report created and skipped items.

Stop conditions:

- Stop immediately after initialization and user next steps.

Common mistakes:

- Starting to solve the task.
- Scanning empty folders for nonexistent assignments.
- Overwriting user files.

## Phase 2: Configuration Reading

Goal: Establish task settings and boundaries.

Inputs: `task_config.yaml`.

Outputs: Parsed configuration and any notes about missing values.

Required actions:

- Read configuration before scanning inputs.
- Respect directory paths and output format.
- Check template, language, citation, style, web, and Python settings.
- Record ambiguous or missing configuration in `work/notes.md`.
- Classify `special_instructions` and style/citation rules as internal guidance unless the user explicitly asks for them to be printed in the final report.
- If instructions require paraphrasing, data adjustment, anonymization, style mimicry, or avoiding similarity to a source, record the rule in `work/notes.md` but do not let the final report mention that rule.

Stop conditions:

- Stop and ask the user if required settings are missing and no safe assumption exists.

Common mistakes:

- Ignoring `has_template`.
- Writing the wrong final format.
- Using web when `allow_web` is false.
- Leaking configuration or prompt language into the final deliverable.

## Phase 3: Problem Scanning

Goal: Find all questions and required outputs.

Inputs: Files in configured `problem_dir`.

Outputs: Problem source list and extracted question structure.

Required actions:

- Scan all readable problem files.
- Preserve original numbering and wording.
- Identify sub-questions, deliverable requirements, and constraints.
- Expand grouped or ranged sub-question references into separate items. For example, treat `4.3(a)-(f)` as `4.3(a)`, `4.3(b)`, `4.3(c)`, `4.3(d)`, `4.3(e)`, and `4.3(f)`.
- Keep each separately requested figure, table, code block, proof, calculation, or discussion tied to the sub-question that asks for it.
- Treat every separately labeled or separately requested task as its own unit even when several units share the same setup, data, figure, or theorem.
- Record unreadable or ambiguous sub-question text as its own item instead of merging it into a nearby item.
- Record unreadable files or missing problems.

Stop conditions:

- Stop if no problem files exist and the task cannot proceed.

Common mistakes:

- Inventing missing questions.
- Dropping sub-questions.
- Combining several sub-questions into a single broad answer.
- Hiding a small sub-question inside the discussion for a larger question.
- Reordering numbering without reason.

## Phase 4: Reference Scanning

Goal: Gather supporting material.

Inputs: Files in configured `reference_dir`.

Outputs: Reference summary and mapping candidates.

Required actions:

- Scan readable reference files.
- Note which references support which questions.
- Track citation or source requirements.
- Record unreadable files and limitations.

Stop conditions:

- Continue if references are optional; stop if required references are missing.

Common mistakes:

- Treating references as problem statements.
- Making unsupported claims when citations are required.

## Phase 5: Template Scanning

Goal: Understand required formatting or document structure.

Inputs: `task_config.yaml`, files in configured `template_dir`, and any problem/reference files that are actually answer sheets or report shells.

Outputs: Template structure notes, constraints, and a writable working-template copy when a template will be used.

Required actions:

- Scan templates if `has_template` is true or template files exist.
- Use `template_filename` when specified. If the named file is not in `template_dir`, also look in `problem_dir` and `reference_dir` before declaring it missing.
- Treat a problem/reference file as a template-like source when it contains answer spaces, required report structure, old report content to replace, or fields the final report must fill.
- Copy the selected template-like source into `work/assets/template_working/` before any edits. Record both source path and working-copy path in `work/notes.md`.
- Identify headings, placeholders, required sections, styles, numbering, captions, and output format.
- For template-backed paraphrase/rewrite tasks, build a template fidelity map: sections/subsections, figures, tables, appendices, formulas, logs/data listings, captions, metadata fields, and approximate depth/detail for each part.
- If the template contains previous answers or sample content, separate the reusable template shell from old content before drafting. Record which parts are structure and which parts are old content in `work/notes.md`.
- Preserve the working copy's main structure and formatting. Replace old content in place where possible instead of rebuilding the report from scratch.
- Adopt the strict filling mindset: the copied template is the document to complete. The agent's job is not to design a new report that resembles the template; the job is to fill the template as a careful human user would.
- Identify the exact reusable fill locations: title fields, metadata fields, answer paragraphs, code blocks, figure slots, caption patterns, table rows, appendices, headers/footers, and repeated styled blocks.
- Identify the tools needed to edit and verify the actual template. If ordinary text generation is insufficient, plan stronger document tooling instead of abandoning the template.
- Preserve information density. Do not turn detailed procedure, analysis, appendix, log, or table material into a brief summary unless the user requests an abridged deliverable.
- If a template appendix/log/table has many rows/columns, plan an equivalent final appendix/log/table with comparable columns and row coverage.
- Never modify original files under `input/`.

Stop conditions:

- Stop if the required template is missing and exact template compliance is mandatory.

Common mistakes:

- Editing the input template directly.
- Rebuilding a template-backed report from scratch instead of editing a copied working template.
- Ignoring required placeholders.
- Treating old report content in the template as if it were new source material.
- Replacing the template with a newly designed document when the template can be reused.
- Treating a polished custom layout as acceptable when it no longer looks like the supplied template.
- Spending effort on implementing a template-like design instead of filling the copied template.
- Treating a full appendix or data log as optional background and replacing it with a short summary.

## Phase 6: Task Inventory Creation

Goal: Build the control list for the report.

Inputs: Problem scan, reference scan, template scan, configuration.

Outputs: Updated `work/task_inventory.md`.

Required actions:

- List every question and sub-question.
- Make every sub-question its own inventory item, even when several parts share one setup or figure.
- Preserve exact labels such as `(a)`, `(b)`, `(i)`, or `Part 1`; do not invent new combined labels such as `(a-c)`.
- Include source file, original prompt, required output, relevant references, needed computation/code, needed figures/tables, potential pitfalls, and status.
- Include template fidelity items as inventory entries when a template-backed rewrite is requested: each major section, figure, table, appendix, log/data listing, and formula block should have a final location or preservation/replacement note.
- Preserve source numbering.
- Include a `final location` or equivalent mapping field once drafting begins, so every inventory item can be traced to a visible final-report heading, label, or table row.

Stop conditions:

- Do not proceed to final report generation until this file is current.

Common mistakes:

- Creating a shallow inventory that omits sub-questions.
- Creating one inventory item for a whole exercise when the source has lettered parts.
- Failing to map final sections back to inventory items.
- Letting the final report recombine items that were correctly separated in the inventory.
- Omitting template-only deliverables such as appendices, captions, tables, logs, or repeated report sections from the inventory.

## Phase 7: Notes/pitfalls/ambiguities Creation

Goal: Record reasoning hazards and assumptions.

Inputs: Configuration, inventory, problems, references, template findings.

Outputs: Updated `work/notes.md`.

Required actions:

- Record global notes.
- Map references to questions.
- List pitfalls, ambiguities, assumptions, notation, units, and citation notes.
- Ask the user when an ambiguity materially changes the answer.

Stop conditions:

- Stop if a critical ambiguity cannot be resolved safely.

Common mistakes:

- Silently choosing assumptions.
- Forgetting units or notation constraints.

## Phase 8: Draft Writing

Goal: Produce intermediate answers before final formatting.

Inputs: Inventory, notes, problems, references.

Outputs: Updated `work/draft.md`.

Required actions:

- Draft each answer under matching question numbers.
- Draft each sub-question separately using the same labels as the inventory.
- Put shared setup, common definitions, or common code before the sub-question answers only when it improves readability; still provide a separate answer for every sub-question.
- Include restatement, solution, derivation or computation, final result, verification, and final-report notes.
- Include a clear result, conclusion, proof endpoint, or artifact reference for each sub-question. Do not make a sub-question depend on a neighboring subsection for its answer.
- Write formulas in LaTeX source form in the draft. Use consistent inline delimiters for short formulas and display delimiters for important equations.
- Keep variable definitions, units, assumptions, and equation references close to the formulas they explain.
- For template-backed paraphrase/rewrite tasks, draft at comparable depth to the template. Expand procedure, analysis, discussion, appendix notes, and table explanations enough that important detail is not lost.
- Keep internal transformation notes out of final-report draft text. They may appear in "Notes for Final Report" only as instructions to yourself, and must not be copied into the final deliverable.
- Mark incomplete items clearly in draft and notes.

Stop conditions:

- Do not generate the final report until draft answers exist.

Common mistakes:

- Writing directly to final output.
- Leaving unsupported or unverified draft claims.
- Hiding several sub-question answers inside a single paragraph or exercise-level summary.
- Drafting an abridged report when the task requested a detailed paraphrase or template-faithful rewrite.
- Mixing raw plain-text math, screenshots, and LaTeX without a recorded tool limitation.

## Phase 9: Content-First Review and Draft Revision

Goal: Make the report content correct and complete before layout decisions.

Inputs: `work/task_inventory.md`, `work/notes.md`, `work/draft.md`, references, computations, and required assets.

Outputs: Updated content-review section in `work/checks.md` and revised `work/draft.md`.

Required actions:

- Review every inventory item against the draft before final report generation.
- Check coverage, reasoning, derivations, computations, assumptions, citations, units, notation, figures, tables, and final-answer targets.
- Check that each formula has a LaTeX source form and that notation is consistent.
- Revise `work/draft.md` for content defects before doing final layout or template placement.
- Record unresolved content limitations in `work/checks.md`.

Stop conditions:

- Do not move to layout or final generation until the content review passes, unless a limitation is recorded and the user has accepted the risk or the limitation is unavoidable.

Common mistakes:

- Polishing layout before the answers are complete.
- Treating a clean-looking final document as correct without checking derivations and coverage.
- Rewriting content during layout in ways that change results or omit assumptions.

## Phase 10: Computation and Asset Generation

Goal: Run reproducible calculations or produce assets when needed.

Inputs: Draft needs, data, references, problem requirements.

Outputs: Scripts in `work/code/`, generated assets in `work/assets/`, and recorded results.

Required actions:

- Use code only when helpful or required.
- Keep scripts in `work/code/`.
- Keep figures, processed tables, and generated assets in `work/assets/`.
- Record commands and successful outputs used.

Stop conditions:

- Stop if required computation cannot be completed and no valid manual route exists.

Common mistakes:

- Claiming code ran when it did not.
- Storing temporary files in `output/`.

## Phase 11: Layout Pass and Final Report Generation

Goal: Convert checked content into a readable final deliverable.

Inputs: `work/task_inventory.md`, `work/notes.md`, `work/draft.md`, templates, assets.

Outputs: Final report under `output/`.

Required actions:

- Save final deliverables only under `output/`.
- Use configured `final_format` when feasible.
- Start from content that has already passed the content-first review.
- Preserve template requirements when applicable.
- If using a template, edit the copy in `work/assets/template_working/` and then save/copy the completed deliverable to `output/`.
- If using a populated template, keep its layout, section order, styles, fields, and caption conventions as stable as possible while replacing old answer content.
- For template-backed outputs, final generation is a template-filling operation. Replace content in the working template or duplicate existing styled blocks. Do not create a newly designed document unless direct filling is impossible after reasonable tooling attempts.
- Do not substantially redesign a template-backed report unless the template is unreadable, unusable, or the user explicitly asks for redesign.
- Maintain template information density. Include equivalent figures, tables, appendices, formulas, logs/data listings, and explanatory paragraphs unless omission is requested or justified in `work/checks.md`.
- Keep prompt/process metadata out of final prose. Do not write transformation rules, data-adjustment rules, local source paths, "source report", "processed", "baseline", "as requested", or tool notes into the final report unless they are assignment content.
- Use headings or labels that keep every required sub-question visibly separated in the final report.
- Choose layout after content is correct: use paragraphs for explanations and analysis, lists for parallel discrete points, tables for structured comparison or repeated values, and display equation blocks for important formulas.
- Remove rough-draft bullet clutter. Merge one-item lists, fragmented bullets, and non-parallel list items into coherent paragraphs when prose is clearer.
- Avoid deep nested lists unless the source structure requires them. Do not hide reasoning inside cramped bullets or table cells.
- For Markdown and LaTeX output, preserve formulas as LaTeX with consistent delimiters.
- For DOCX output, use the LaTeX source from the draft to create Word-compatible equations or another clean rendered formula form when feasible. Do not rely on Word to automatically convert raw LaTeX text.
- For DOCX output, use a polished academic/report layout: clean A4 page setup, consistent margins, readable body font, stable heading styles, restrained spacing, numbered captions where needed, and no decorative or random layout choices.
- For DOCX output, use Word-compatible equations where possible. If native equations are not feasible, use consistent readable linear math and record the limitation.
- For DOCX output, important equations should be displayed cleanly on their own line; do not leave raw `$...$`, `$$...$$`, `\(...\)`, `\[...\]`, or LaTeX commands in the final document unless the user explicitly requested LaTeX source text.
- Ensure every final section maps to inventory.
- Remove internal notes and placeholders.

Stop conditions:

- Stop and record limitation if final format cannot be produced.
- Stop and record a blocking formatting issue if a template-backed final output is visibly a redesign rather than the supplied template filled in.

Common mistakes:

- Generating final output before draft and inventory.
- Leaving TODO/FIXME/placeholders in final report.
- Leaving prompt wording, transformation instructions, data-adjustment rules, or internal file/tool notes in final report.
- Merging sub-questions in final formatting after they were separated in the draft.
- Using old content from a template as filler.
- Replacing detailed appendices/logs/tables with a short summary.
- Creating a new blank document when the copied working template could be edited.
- Using code to recreate a "nice" template-inspired document instead of filling the actual working template.
- Accepting major differences in cover, section spacing, code block width, captions, table layout, headers/footers, or repeated answer patterns because the new document looks clean.
- Producing a DOCX with inconsistent fonts, ugly spacing, unstyled headings, unreadable formulas, or screenshot formulas when an editable equation was feasible.
- Leaving the draft's rough bullet structure unchanged when it makes the final report harder to read.
- Pasting LaTeX source into DOCX and assuming Word will convert it automatically.

## Phase 12: Correctness Checking

Goal: Verify content accuracy and completeness.

Inputs: Final report, inventory, notes, draft, references, computations.

Outputs: Updated correctness section in `work/checks.md`.

Required actions:

- Check every question and sub-question.
- Confirm each sub-question has a separately visible answer in the final report.
- Verify assumptions, reasoning, units, notation, computations, figures, tables, and citations.
- Verify formulas against the LaTeX source in the draft and check that no formula was dropped, mistranscribed, or replaced by vague prose.
- For template-backed reports, compare the final deliverable against the template fidelity map. Check that sections, figures, tables, appendices, formulas, logs/data listings, captions, and depth/detail are preserved or explicitly accounted for.
- For template-backed reports, also compare content after layout edits against the reviewed draft. Confirm that template fitting did not change numerical values, stability conclusions, bandwidth statements, formulas, assumptions, or required labels.
- For appendices/logs/tables, compare row counts, column meanings, and coverage against the template/reference. Summaries are insufficient when the source contains detailed raw or tabular material and the user requested detail preservation.
- Record known limitations.

Stop conditions:

- Do not complete until checks are recorded.

Common mistakes:

- Treating formatting review as correctness review.
- Ignoring pitfalls already listed in notes.

## Phase 13: Formatting Checking

Goal: Verify deliverable presentation.

Inputs: Final report, template requirements, output directory.

Outputs: Updated formatting section in `work/checks.md`.

Required actions:

- Confirm final file exists in `output/`.
- Check headings, numbering, equations, captions, citations, template preservation, and absence of TODO/FIXME/placeholders.
- Check layout choices after content correctness: lists are parallel and purposeful, paragraphs carry explanations cleanly, tables improve readability, and equation blocks are readable.
- Search or inspect the final deliverable for prompt/meta leakage: prompt wording, "paraphrase", "source report", "baseline source", "processed", "offset", "as requested", data-adjustment rules, local paths, and tool/process notes.
- If a template was used, confirm the final file keeps the template's main structure and that old content was stripped or intentionally retained with a reason recorded in `work/notes.md`.
- If a template was used, perform a serious template-fidelity inspection before completion. Compare original template and final output visually or structurally, focusing on cover pages, metadata areas, section order, heading hierarchy, paragraph width/indentation, code blocks, tables, figures, captions, headers/footers, and page flow.
- If the final output is DOCX and visual fidelity matters, render or open the original template and final DOCX when feasible. Use LibreOffice/soffice, Word, screenshots, PDF/PNG conversion, or another reliable renderer. If no renderer is available, record that limitation and use the strongest structural inspection possible.
- Record template mismatches found and fixes made. Do not finish with a major mismatch merely because the output is aesthetically acceptable.
- If wide appendices or data tables are present, use readable formatting such as landscape pages, smaller but legible fonts, repeated headers, or split tables rather than dropping columns.
- For DOCX output, check page margins, fonts, heading styles, paragraph spacing, table readability, caption consistency, visible sub-question separation, and formula rendering.
- Confirm `output/` contains final files only.

Stop conditions:

- Do not complete until formatting checks are recorded.

Common mistakes:

- Leaving temporary files in `output/`.
- Missing captions or inconsistent numbering.
- Passing checks without a prompt/meta leakage scan.
- Passing a template-backed report without a high-effort template-fidelity comparison.
- Treating "pretty" as equivalent to "matches the template."
- Allowing appendices or logs to become less detailed than the template/reference without recording a user-approved reason.
- Overusing bullets because the draft used bullets, even when paragraph prose would be clearer.

## Phase 14: Final Summary

Goal: Leave a durable completion record.

Inputs: Final report, checks, notes, code, assets.

Outputs: Final summary in `work/checks.md` and user-facing completion message.

Required actions:

- Record final output path.
- Record intermediate files updated.
- Record code/assets used.
- Record checks performed.
- Record known limitations and assumptions.
- Tell the user where the final deliverable is.

Stop conditions:

- Complete only after final summary is written.

Common mistakes:

- Omitting limitations.
- Reporting success without file paths.

## Phase 15: Task-End Retrospective and Skill Integration

Goal: Convert real failures, user corrections, and near-misses from a completed report task into durable improvements to this skill.

Trigger: The user says `任务结束`, says the report task is finished, or asks to summarize task problems and fold them into the skill.

Required actions:

- Start with a user-visible retrospective summary before editing skill files.
- Include each issue's problem, impact, root cause, preventive rule, and target skill location.
- If the user did not explicitly ask to apply the changes immediately, stop after the summary and ask whether to proceed.
- When applying changes, integrate them into `report-workflow`; do not create a separate skill unless explicitly requested.
- Update all relevant layers:
  - `SKILL.md` for hard requirements and mode-level behavior.
  - `references/workflow.md` for phase-by-phase execution steps.
  - `references/template_handling.md` for template-specific lessons.
  - `references/quality_checklist.md` for validation lessons.
  - `assets/*.template.*` for starter files that future initialized projects should inherit.
- Strengthen existing rules in place instead of adding duplicate or disconnected "lessons learned" notes.
- Preserve the existing initialization and report-writing behavior unless the lesson explicitly corrects it.
- Validate modified skill files with text search for duplicate headings, stale wording, obvious placeholders, and missing checklist coverage.

Stop conditions:

- Complete only after the summary has been presented and, if edits were requested, the relevant skill files have been updated and validated.

Common mistakes:

- Editing the skill before showing the retrospective summary.
- Creating a separate retrospective skill when the user wanted the behavior inside `report-workflow`.
- Adding a new note that is not connected to the workflow phase, template handling rule, or quality check where it should be enforced.
- Updating `SKILL.md` but forgetting the runbook, quality checklist, or starter templates.
