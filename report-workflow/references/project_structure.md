# Project Structure

## `README.md`

User-facing summary of the report workflow project and where to place materials.

## `task_config.yaml`

Configuration file. Read it before scanning inputs. It defines task name, language, final format, template settings, web/code permissions, style/citation rules, special instructions, and directory paths.

## `input/problems/`

Read-only folder for problem statements, assignment prompts, question files, rubrics, and required deliverable instructions.

## `input/references/`

Read-only folder for lecture notes, papers, datasets, manuals, examples, source readings, or any material that supports answers.

## `input/template/`

Read-only folder for report templates, answer sheets, required formatting examples, or provided document shells.

## `work/task_inventory.md`

Intermediate file listing every problem, sub-question, required output, source mapping, relevant references, computations, figures/tables, pitfalls, and status.

## `work/notes.md`

Intermediate notes for reference mapping, pitfalls, ambiguities, assumptions, notation, units, citation requirements, and limitations.

## `work/draft.md`

Intermediate draft answers. The final report must not be generated before this file is created or updated.

## `work/checks.md`

Coverage, correctness, formatting, and final summary record. Completion requires this file to be updated.

## `work/code/`

Writable folder for scripts used during analysis, computation, parsing, conversion, figure generation, or reproducibility.

## `work/assets/`

Writable folder for generated figures, tables, processed data, temporary exports, and other intermediate assets.

## `output/`

Final-only folder. Store final deliverables here and avoid temporary files.

## Boundary Summary

- `input/` is read-only.
- `work/` is writable and stores intermediate artifacts.
- `output/` is final-only.
