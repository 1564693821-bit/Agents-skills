# Initialization Runbook

First-run initialization is not report writing. After initialization, stop and wait for the user to add files and configure the task.

## Detecting an Uninitialized Project

Begin every invocation by inspecting the current working directory. The project is initialized only when all of these exist:

- `task_config.yaml`
- `input/`
- `work/`
- `output/`

If any required item is missing, treat the project as uninitialized or incomplete.

## Creating Missing Directories

Create only missing directories:

- `input/problems/`
- `input/references/`
- `input/template/`
- `work/code/`
- `work/assets/`
- `output/`

Do not move, rename, or delete unrelated files already present in the directory.

## Creating Starter Files

Create these files from `assets/` templates:

- `README.md`
- `task_config.yaml`
- `work/task_inventory.md`
- `work/notes.md`
- `work/draft.md`
- `work/checks.md`

If a file does not exist, create it. If a file exists but is empty, fill it with the template. If a file exists and is non-empty, skip it.

## Avoiding Overwrites

Never overwrite non-empty user files during initialization unless the user explicitly asks. Report skipped files so the user can inspect them.

## Why Stop After Initialization

The first run prepares a reliable workspace. It must not infer the assignment from unrelated files, scan for answers, write draft content, or create a final report. Stopping avoids accidental work before the user has placed problems, references, templates, and configuration.

## User Message After Initialization

Report:

- Created project structure.
- Files created.
- Files skipped because they already existed.
- Next steps.

Use this closing text:

```text
The report project has been initialized.
Next steps:
1. Put problem files into input/problems/.
2. Put reference materials into input/references/.
3. Put template files into input/template/ if any.
4. Edit task_config.yaml.
5. Invoke this skill again to write the report.
```
