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

Stop conditions:

- Stop and ask the user if required settings are missing and no safe assumption exists.

Common mistakes:

- Ignoring `has_template`.
- Writing the wrong final format.
- Using web when `allow_web` is false.

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
- If the template contains previous answers or sample content, separate the reusable template shell from old content before drafting. Record which parts are structure and which parts are old content in `work/notes.md`.
- Preserve the working copy's main structure and formatting. Replace old content in place where possible instead of rebuilding the report from scratch.
- Never modify original files under `input/`.

Stop conditions:

- Stop if the required template is missing and exact template compliance is mandatory.

Common mistakes:

- Editing the input template directly.
- Rebuilding a template-backed report from scratch instead of editing a copied working template.
- Ignoring required placeholders.
- Treating old report content in the template as if it were new source material.
- Replacing the template with a newly designed document when the template can be reused.

## Phase 6: Task Inventory Creation

Goal: Build the control list for the report.

Inputs: Problem scan, reference scan, template scan, configuration.

Outputs: Updated `work/task_inventory.md`.

Required actions:

- List every question and sub-question.
- Make every sub-question its own inventory item, even when several parts share one setup or figure.
- Preserve exact labels such as `(a)`, `(b)`, `(i)`, or `Part 1`; do not invent new combined labels such as `(a-c)`.
- Include source file, original prompt, required output, relevant references, needed computation/code, needed figures/tables, potential pitfalls, and status.
- Preserve source numbering.
- Include a `final location` or equivalent mapping field once drafting begins, so every inventory item can be traced to a visible final-report heading, label, or table row.

Stop conditions:

- Do not proceed to final report generation until this file is current.

Common mistakes:

- Creating a shallow inventory that omits sub-questions.
- Creating one inventory item for a whole exercise when the source has lettered parts.
- Failing to map final sections back to inventory items.
- Letting the final report recombine items that were correctly separated in the inventory.

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
- Mark incomplete items clearly in draft and notes.

Stop conditions:

- Do not generate the final report until draft answers exist.

Common mistakes:

- Writing directly to final output.
- Leaving unsupported or unverified draft claims.
- Hiding several sub-question answers inside a single paragraph or exercise-level summary.

## Phase 9: Computation and Asset Generation

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

## Phase 10: Final Report Generation

Goal: Create the final deliverable.

Inputs: `work/task_inventory.md`, `work/notes.md`, `work/draft.md`, templates, assets.

Outputs: Final report under `output/`.

Required actions:

- Save final deliverables only under `output/`.
- Use configured `final_format` when feasible.
- Preserve template requirements when applicable.
- If using a template, edit the copy in `work/assets/template_working/` and then save/copy the completed deliverable to `output/`.
- If using a populated template, keep its layout, section order, styles, fields, and caption conventions as stable as possible while replacing old answer content.
- Do not substantially redesign a template-backed report unless the template is unreadable, unusable, or the user explicitly asks for redesign.
- Use headings or labels that keep every required sub-question visibly separated in the final report.
- For DOCX output, use a polished academic/report layout: clean A4 page setup, consistent margins, readable body font, stable heading styles, restrained spacing, numbered captions where needed, and no decorative or random layout choices.
- For DOCX output, use Word-compatible equations where possible. If native equations are not feasible, use consistent readable linear math and record the limitation.
- For DOCX output, important equations should be displayed cleanly on their own line; do not leave raw LaTeX in the final document unless the user explicitly requested raw LaTeX text.
- Ensure every final section maps to inventory.
- Remove internal notes and placeholders.

Stop conditions:

- Stop and record limitation if final format cannot be produced.

Common mistakes:

- Generating final output before draft and inventory.
- Leaving TODO/FIXME/placeholders in final report.
- Merging sub-questions in final formatting after they were separated in the draft.
- Using old content from a template as filler.
- Creating a new blank document when the copied working template could be edited.
- Producing a DOCX with inconsistent fonts, ugly spacing, unstyled headings, unreadable formulas, or screenshot formulas when an editable equation was feasible.

## Phase 11: Correctness Checking

Goal: Verify content accuracy and completeness.

Inputs: Final report, inventory, notes, draft, references, computations.

Outputs: Updated correctness section in `work/checks.md`.

Required actions:

- Check every question and sub-question.
- Confirm each sub-question has a separately visible answer in the final report.
- Verify assumptions, reasoning, units, notation, computations, figures, tables, and citations.
- Record known limitations.

Stop conditions:

- Do not complete until checks are recorded.

Common mistakes:

- Treating formatting review as correctness review.
- Ignoring pitfalls already listed in notes.

## Phase 12: Formatting Checking

Goal: Verify deliverable presentation.

Inputs: Final report, template requirements, output directory.

Outputs: Updated formatting section in `work/checks.md`.

Required actions:

- Confirm final file exists in `output/`.
- Check headings, numbering, equations, captions, citations, template preservation, and absence of TODO/FIXME/placeholders.
- If a template was used, confirm the final file keeps the template's main structure and that old content was stripped or intentionally retained with a reason recorded in `work/notes.md`.
- For DOCX output, check page margins, fonts, heading styles, paragraph spacing, table readability, caption consistency, visible sub-question separation, and formula rendering.
- Confirm `output/` contains final files only.

Stop conditions:

- Do not complete until formatting checks are recorded.

Common mistakes:

- Leaving temporary files in `output/`.
- Missing captions or inconsistent numbering.

## Phase 13: Final Summary

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
