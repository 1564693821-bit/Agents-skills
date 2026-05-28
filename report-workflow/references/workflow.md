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
- Interpret style requirements as presentation constraints only. Requests such as "simple", "concise", "clean", "brief", or "minimal" must not remove required code, derivations, formulas, figures, tables, verification, citations, or sub-question answers.
- Record ambiguous or missing configuration in `work/notes.md`.

Stop conditions:

- Stop and ask the user if required settings are missing and no safe assumption exists.

Common mistakes:

- Ignoring `has_template`.
- Writing the wrong final format.
- Using web when `allow_web` is false.
- Treating a concise style request as permission to omit required deliverables.

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
- Apply source priority: primary problem files and explicit user instructions define required deliverables; reference books explain and verify; peer/example reports are comparison material unless the user explicitly makes them the target.
- If a peer/example report is present, compare coverage, code approach, figure coverage, numerical results, and conclusions against the primary problem statement.
- Record disagreements between peer reports and the primary problem/theory/computation in `work/notes.md` or a dedicated comparison file under `work/`.
- Do not add extra peer-report sub-questions unless they also appear in the primary problem file or the user approves the addition.
- For code or plot disagreements, plan an independent numerical or theoretical check where feasible.

Stop conditions:

- Continue if references are optional; stop if required references are missing.

Common mistakes:

- Treating references as problem statements.
- Treating peer reports as authoritative without checking the handout.
- Copying extra questions from a peer report that are not assigned.
- Making unsupported claims when citations are required.

## Phase 5: Template Scanning

Goal: Understand required formatting or document structure.

Inputs: `task_config.yaml` and files in configured `template_dir`.

Outputs: Template structure notes and constraints.

Required actions:

- Scan templates if `has_template` is true or template files exist.
- Use `template_filename` when specified.
- Identify headings, placeholders, required sections, styles, numbering, captions, and output format.
- If the template contains previous answers or sample content, separate the reusable template shell from old content before drafting. Record which parts are structure and which parts are old content in `work/notes.md`.
- Preserve the template's main structure and formatting. Replace old content in place where possible instead of rebuilding the report from scratch.
- Treat the template as a fillable shell. Preserve font sizes, font families, run styles, paragraph styles, spacing, margins, headers/footers, numbering, captions, and table styles unless the user explicitly requests redesign or exact preservation is technically impossible.
- Never modify original template files.

Stop conditions:

- Stop if the required template is missing and exact template compliance is mandatory.

Common mistakes:

- Editing the input template directly.
- Ignoring required placeholders.
- Treating old report content in the template as if it were new source material.
- Replacing the template with a newly designed document when the template can be reused.
- Changing template fonts, font sizes, spacing, margins, or heading definitions merely to make the final report look cleaner.

## Phase 6: Task Inventory Creation

Goal: Build the control list for the report.

Inputs: Problem scan, reference scan, template scan, configuration.

Outputs: Updated `work/task_inventory.md`.

Required actions:

- List every question and sub-question.
- Make every sub-question its own inventory item, even when several parts share one setup or figure.
- Preserve exact labels such as `(a)`, `(b)`, `(i)`, or `Part 1`; do not invent new combined labels such as `(a-c)`.
- Include source file, original prompt, required output, relevant references, needed computation/code, needed figures/tables, potential pitfalls, and status.
- Explicitly list every required artifact: code, commands, formulas, derivations, numerical outputs, figures, tables, verification, discussion, and citations. If an artifact type is not required, mark it as not required rather than leaving it implicit.
- Build an artifact traceability matrix for each sub-question: planned final location for code, formulas/derivations, figures/tables, numerical outputs, verification, and discussion.
- For every planned figure/table, include purpose, source data/code, expected axes or columns, caption intent, and the exact sub-question it supports.
- Preserve source numbering.
- Include a `final location` or equivalent mapping field once drafting begins, so every inventory item can be traced to a visible final-report heading, label, or table row.

Stop conditions:

- Do not proceed to final report generation until this file is current.

Common mistakes:

- Creating a shallow inventory that omits sub-questions.
- Creating one inventory item for a whole exercise when the source has lettered parts.
- Failing to map final sections back to inventory items.
- Letting the final report recombine items that were correctly separated in the inventory.
- Leaving required artifacts implicit, which can cause concise output to omit code, derivations, figures, or verification.
- Planning figures at the exercise level without mapping them to the sub-question that requires them.

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
- Preserve all required deliverables in the draft even when the final style should be concise. Brevity is achieved by trimming prose, not by deleting code, calculations, plots, tables, or verification required by the prompt.
- For computational parts, include setup, method, code/command, result, interpretation, and verification.
- For figure parts, explain what the figure shows and how it answers the prompt; do not rely on captions alone.
- For derivation parts, include enough intermediate steps to make the result auditable.
- For comparison or qualitative parts, state the comparison criteria, observation, and conclusion.
- Mark incomplete items clearly in draft and notes.

Stop conditions:

- Do not generate the final report until draft answers exist.

Common mistakes:

- Writing directly to final output.
- Leaving unsupported or unverified draft claims.
- Hiding several sub-question answers inside a single paragraph or exercise-level summary.
- Producing code and plots without explanatory interpretation.

## Phase 9: Computation and Asset Generation

Goal: Run reproducible calculations or produce assets when needed.

Inputs: Draft needs, data, references, problem requirements.

Outputs: Scripts in `work/code/`, generated assets in `work/assets/`, and recorded results.

Required actions:

- Use code only when helpful or required.
- Keep scripts in `work/code/`.
- Keep figures, processed tables, and generated assets in `work/assets/`.
- Record commands and successful outputs used.
- Ensure the code included in the final report matches the code used for reported outputs, or record any intentional difference.
- Generate figures from a planned figure map. Each figure should have a stable descriptive filename tied to the question label.
- Inspect generated figures for correct data, axes, units, legends, ranges, and captions.
- Check for missing, stale, duplicated, or accidentally reused figures using filenames and, where feasible, hashes, dimensions, or visual contact sheets.
- If a peer/example report is supplied, generate comparison artifacts under `work/` when useful: extracted figure list, contact sheet, coverage comparison, or numerical validation notes.
- For DOCX outputs with images, plan a later package check for visible captions, embedded image references, relationships, and media files.

Stop conditions:

- Stop if required computation cannot be completed and no valid manual route exists.

Common mistakes:

- Claiming code ran when it did not.
- Storing temporary files in `output/`.
- Reusing a figure for multiple sub-questions without an explicit reason.
- Trusting generated plots without opening or inspecting them.

## Phase 10: Final Report Generation

Goal: Create the final deliverable.

Inputs: `work/task_inventory.md`, `work/notes.md`, `work/draft.md`, templates, assets.

Outputs: Final report under `output/`.

Required actions:

- Save final deliverables only under `output/`.
- Use configured `final_format` when feasible.
- Preserve template requirements when applicable.
- If using a populated template, keep its layout, section order, styles, fields, typography, spacing, numbering, and caption conventions stable while replacing old answer content.
- Fill placeholders and existing styled regions directly where feasible. Do not rebuild a template-backed report as a newly formatted document if the template can be edited in place.
- Do not substantially redesign a template-backed report unless the template is unreadable, unusable, or the user explicitly asks for redesign.
- Use headings or labels that keep every required sub-question visibly separated in the final report.
- Include required source code, commands, derivations, formulas, generated figures/tables, and verification when the prompt asks for them, even under concise style requirements.
- Apply a content completeness gate before completion: every required artifact listed in `work/task_inventory.md` must appear in the final report or be recorded as impossible with a reason in `work/checks.md`.
- Apply a template fidelity gate before completion: every template formatting deviation must be user-requested, technically unavoidable, or recorded in `work/checks.md`.
- Apply an artifact placement gate before completion: required code, figures, formulas, numerical outputs, and explanations must appear under the correct sub-question, not only in an appendix or neighboring section.
- Apply a figure correctness gate before completion: each final figure must be present, distinct unless documented, correctly captioned, and semantically matched to the sub-question.
- Apply a reference-difference gate before completion when a peer/example report exists: coverage, code, figure, and conclusion differences must be recorded and resolved.
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
- Changing a template's font sizes, fonts, spacing, margins, heading definitions, numbering, captions, or table styles without a user request or recorded technical limitation.
- Omitting required code or derivations because the requested style is concise.
- Producing a DOCX with inconsistent fonts, ugly spacing, unstyled headings, unreadable formulas, or screenshot formulas when an editable equation was feasible.
- Passing checks while code or figures are only present in an appendix.
- Leaving stale or orphaned images inside a DOCX package.

## Phase 11: Correctness Checking

Goal: Verify content accuracy and completeness.

Inputs: Final report, inventory, notes, draft, references, computations.

Outputs: Updated correctness section in `work/checks.md`.

Required actions:

- Check every question and sub-question.
- Confirm each sub-question has a separately visible answer in the final report.
- Verify assumptions, reasoning, units, notation, computations, figures, tables, and citations.
- Verify that style requirements did not remove any required code, command, derivation, formula, figure, table, verification, citation, or discussion point.
- Verify every required artifact appears under the correct sub-question in the final report.
- Verify every final figure matches its prompt, code, caption, axes/units, and surrounding explanation.
- Verify that repeated figures are intentional and documented.
- Verify peer/example report differences, if any, were recorded and resolved using the primary prompt, theory, or reproducible computation.
- Record known limitations.

Stop conditions:

- Do not complete until checks are recorded.

Common mistakes:

- Treating formatting review as correctness review.
- Ignoring pitfalls already listed in notes.
- Checking that images exist without checking what they show.

## Phase 12: Formatting Checking

Goal: Verify deliverable presentation.

Inputs: Final report, template requirements, output directory.

Outputs: Updated formatting section in `work/checks.md`.

Required actions:

- Confirm final file exists in `output/`.
- Check headings, numbering, equations, captions, citations, template preservation, and absence of TODO/FIXME/placeholders.
- If a template was used, confirm the final file keeps the template's main structure and that old content was stripped or intentionally retained with a reason recorded in `work/notes.md`.
- If a template was used, confirm typography, font sizes, paragraph spacing, margins, headers/footers, numbering, captions, and table styles were preserved except for documented exceptions.
- For DOCX output, check page margins, fonts, heading styles, paragraph spacing, table readability, caption consistency, visible sub-question separation, and formula rendering.
- For DOCX output with images, check visible caption count, embedded image references, image relationships, and media files; remove unused template media when feasible.
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
