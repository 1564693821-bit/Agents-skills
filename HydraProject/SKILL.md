---
name: hydra-project
description: Work inside Hydra-based research engineering projects with strict project-root workspace rules, staged task workflow, decision gates, and reuse-first code navigation. Use for Hydra config changes, component extensions, pipeline assembly, debugging, documentation, and skill/project memory maintenance.
---

# Hydra Project Skill

Use this skill for Hydra-based research codebases where behavior is spread across config defaults, `_target_` instantiation, trainers, data loaders, losses, wrappers, and checkpoints.

The skill has two jobs:

1. Keep the installed skill stable.
2. Create and maintain a project-root agent workspace for project state.

Do not store project task state inside this skill folder.

## Project Workspace

The installed skill directory only contains stable skill rules and bundled resources. Runtime project state must live under the current project root:

```text
<PROJECT_ROOT>/CodexWorkspace/
  README.md
  references/
  checklists/
  snippets/
  memory/
  taskboard/
  draft/
  scratch/
```

Use these aliases:

- `<PROJECT_AGENT_HOME>` = `<PROJECT_ROOT>/CodexWorkspace/`
- `<REFERENCE_HOME>` = `<PROJECT_AGENT_HOME>/references/`
- `<CHECKLIST_HOME>` = `<PROJECT_AGENT_HOME>/checklists/`
- `<SNIPPET_HOME>` = `<PROJECT_AGENT_HOME>/snippets/`
- `<MEMORY_HOME>` = `<PROJECT_AGENT_HOME>/memory/`
- `<TASK_HOME>` = `<PROJECT_AGENT_HOME>/taskboard/`
- `<DRAFT_HOME>` = `<PROJECT_AGENT_HOME>/draft/`
- `<SCRATCH_HOME>` = `<PROJECT_AGENT_HOME>/scratch/`

If these directories do not exist, create them. This is project setup, not a user-facing design choice.

Do not write task state, decisions, work logs, project memory, or experiment notes into the installed skill directory unless the user explicitly asks to modify the skill itself.

## Language Policy

Use Chinese for descriptive project outputs by default.

This applies to:

- `CodexWorkspace/README.md`;
- task summaries;
- work logs;
- decision notes;
- project memory;
- reference notes;
- checklists;
- final explanations to the user.

Keep code, commands, paths, config keys, class names, function names, API names, log snippets, and exact error messages in their original language when that preserves correctness.

## Project Files

Human-facing overview:

- `<PROJECT_AGENT_HOME>/README.md`: explains what each workspace file is for and where the user's attention should go.

Short-lived task files:

- `<TASK_HOME>/Current.md`: current task boundary.
- `<TASK_HOME>/Decision.md`: blocking user decisions.
- `<TASK_HOME>/Worklog.md`: high-signal current progress.

Long-lived project files:

- `<TASK_HOME>/Done.md`: concise task index.
- `<MEMORY_HOME>/project-map.md`: project layers and key call chains.
- `<MEMORY_HOME>/stable-decisions.md`: choices that should be reused later.
- `<MEMORY_HOME>/open-questions.md`: non-blocking unknowns.
- `<REFERENCE_HOME>/*.md`: stable technical references.

Refresh short-lived files at task boundaries. Update long-lived files only after completing a task or confirming reusable knowledge.

## Task Types

Classify every task before implementation:

- Config recomposition: change existing Hydra composition, dataset, tokenizer config, weights, flags, or checkpoints.
- Component extension: add a narrow capability to an existing loader, trainer, loss, wrapper, tokenizer, or test.
- Pipeline assembly: connect stages or create a new workflow/trainer.
- Diagnosis/explanation: answer why something happens by reading configs and code.
- Documentation/skill maintenance: improve project notes, task records, or skill workflow.

The task type limits what may be changed.

## Staged Workflow

### Stage 0: Initialize Workspace

Required:

1. Locate `<PROJECT_ROOT>`.
2. Create `<PROJECT_AGENT_HOME>` and subdirectories if missing.
3. Create `<PROJECT_AGENT_HOME>/README.md` if missing. It must explain the workspace layout, which files are user-facing, which files are mostly for the agent, and what the user should check after each task.
4. Locate the active task file: user-specified file first, then `<TASK_HOME>/Instructions.md`, then compatible project history files if present.
5. Locate the active done file: user-specified record first, then `<TASK_HOME>/Done.md`, then compatible project history files if present.
6. Refresh `Current.md`, `Decision.md`, and `Worklog.md`.

Do not edit code before the active task and done files are understood.

### Stage 1: Define Boundary

Write to `Current.md`:

- task source;
- task mode;
- expected output;
- allowed files/modules;
- out-of-scope items;
- stop conditions.

If the task is still unclear after reading the task file and done record, write the blocking question to `Decision.md` and ask the user only for the minimum missing information.

### Stage 2: Read Minimal Context

Read in this order:

1. active task file;
2. active done file;
3. `<MEMORY_HOME>/stable-decisions.md` and `<MEMORY_HOME>/project-map.md`;
4. relevant `<REFERENCE_HOME>` documents;
5. code and Hydra configs only when the workspace documents are insufficient.

Avoid unbounded whole-repo searches. Use `rg` first when searching.

### Stage 3: Decision Gate

Must ask the user through `Decision.md` before changing:

- training target or objective;
- dataset semantics or selected data keys;
- input value range;
- latent type or feature semantics;
- loss semantics;
- compression accounting;
- checkpoint, resume, or EMA loading policy;
- public parameter names or test semantics;
- freeze/unfreeze policy or joint-training order;
- long training, downloads, or external access.

May decide and record in `Worklog.md`:

- helper names;
- small local structure;
- minimal test fixture shape;
- whether to extract a small helper;
- whether to add finite/non-finite checks.

May decide silently:

- import order;
- local variable cleanup;
- obvious typos;
- behavior-neutral formatting.

### Stage 4: Execute

Execution rules by type:

- Config recomposition: trace defaults and `_target_`; prefer config-only changes.
- Component extension: stay inside existing component boundaries; add focused tests when behavior changes.
- Pipeline assembly: identify reusable trainers, wrappers, losses, and data paths before adding new files.
- Diagnosis/explanation: read code/configs and answer; do not edit files unless requested.
- Documentation/skill maintenance: improve workflow, boundaries, file protocol, and decision rules without adding unrelated project detail.

Write only high-signal progress to `Worklog.md`.

### Stage 5: Validate

Validation level follows risk:

- docs: check structure, ordering, and stale path semantics;
- config: check defaults, interpolation, `_target_`, and trainer field usage;
- Python: run syntax checks and relevant tests when available;
- training logic: add a minimal test or static check when full training is impractical.

Record verified and unverified points in `Worklog.md`.

### Stage 6: Close Out

Required:

1. Update the active done file with a concise task index.
2. Update `<REFERENCE_HOME>` or `<MEMORY_HOME>` for reusable knowledge.
3. Update `<MEMORY_HOME>/stable-decisions.md` for durable choices.
4. Update `<MEMORY_HOME>/open-questions.md` for non-blocking unknowns.
5. Clear resolved content from `Decision.md`.
6. Mark `Current.md` completed or clear it for the next task.

Final chat response should only summarize what changed, where it lives, what was verified, and what remains unverified.

## Hydra Rules

For any Hydra-driven behavior, inspect:

- main config file;
- `defaults`;
- config group files;
- `_target_`;
- overrides in the main config;
- interpolation such as `${dataset.img_size}`;
- trainer or caller usage of the field.

Never infer model behavior from filename alone.
---
name: hydra-project
description: Work inside Hydra-based research engineering projects with strict project-root workspace rules, staged task workflow, decision gates, and reuse-first code navigation. Use for Hydra config changes, component extensions, pipeline assembly, debugging, documentation, and skill/project memory maintenance.
---

# Hydra Project Skill

Use this skill for Hydra-based research codebases where behavior is spread across config defaults, `_target_` instantiation, trainers, data loaders, losses, wrappers, and checkpoints.

The skill has two jobs:

1. Keep the installed skill stable.
2. Create and maintain a project-root agent workspace for project state.

Do not store project task state inside this skill folder.

## Project Workspace

The installed skill directory only contains stable skill rules and bundled resources. Runtime project state must live under the current project root:

```text
<PROJECT_ROOT>/CodexWorkspace/
  README.md
  references/
  checklists/
  snippets/
  memory/
  taskboard/
  draft/
  scratch/
```

Use these aliases:

- `<PROJECT_AGENT_HOME>` = `<PROJECT_ROOT>/CodexWorkspace/`
- `<REFERENCE_HOME>` = `<PROJECT_AGENT_HOME>/references/`
- `<CHECKLIST_HOME>` = `<PROJECT_AGENT_HOME>/checklists/`
- `<SNIPPET_HOME>` = `<PROJECT_AGENT_HOME>/snippets/`
- `<MEMORY_HOME>` = `<PROJECT_AGENT_HOME>/memory/`
- `<TASK_HOME>` = `<PROJECT_AGENT_HOME>/taskboard/`
- `<DRAFT_HOME>` = `<PROJECT_AGENT_HOME>/draft/`
- `<SCRATCH_HOME>` = `<PROJECT_AGENT_HOME>/scratch/`

If these directories do not exist, create them. This is project setup, not a user-facing design choice.

Do not write task state, decisions, work logs, project memory, or experiment notes into the installed skill directory unless the user explicitly asks to modify the skill itself.

## Language Policy

Use Chinese for descriptive project outputs by default.

This applies to:

- `CodexWorkspace/README.md`;
- task summaries;
- work logs;
- decision notes;
- project memory;
- reference notes;
- checklists;
- final explanations to the user.

Keep code, commands, paths, config keys, class names, function names, API names, log snippets, and exact error messages in their original language when that preserves correctness.

## Project Files

Human-facing overview:

- `<PROJECT_AGENT_HOME>/README.md`: explains what each workspace file is for and where the user's attention should go.

Short-lived task files:

- `<TASK_HOME>/Current.md`: current task boundary.
- `<TASK_HOME>/Decision.md`: blocking user decisions.
- `<TASK_HOME>/Worklog.md`: high-signal current progress.

Long-lived project files:

- `<TASK_HOME>/Done.md`: concise task index.
- `<MEMORY_HOME>/project-map.md`: project layers and key call chains.
- `<MEMORY_HOME>/stable-decisions.md`: choices that should be reused later.
- `<MEMORY_HOME>/open-questions.md`: non-blocking unknowns.
- `<REFERENCE_HOME>/*.md`: stable technical references.

Refresh short-lived files at task boundaries. Update long-lived files only after completing a task or confirming reusable knowledge.

## Task Types

Classify every task before implementation:

- Config recomposition: change existing Hydra composition, dataset, tokenizer config, weights, flags, or checkpoints.
- Component extension: add a narrow capability to an existing loader, trainer, loss, wrapper, tokenizer, or test.
- Pipeline assembly: connect stages or create a new workflow/trainer.
- Diagnosis/explanation: answer why something happens by reading configs and code.
- Documentation/skill maintenance: improve project notes, task records, or skill workflow.

The task type limits what may be changed.

Question-only tasks may be explicitly marked by the user as not counting as a formal task. In that case, do not rewrite
the taskboard as a normal implementation task, but still read enough local context to answer and still preserve new
reusable knowledge in `<REFERENCE_HOME>` or `<MEMORY_HOME>`.

## Staged Workflow

### Stage 0: Initialize Workspace

Required:

1. Locate `<PROJECT_ROOT>`.
2. Create `<PROJECT_AGENT_HOME>` and subdirectories if missing.
3. Create `<PROJECT_AGENT_HOME>/README.md` if missing. It must explain the workspace layout, which files are user-facing, which files are mostly for the agent, and what the user should check after each task.
4. Locate the active task file: user-specified file first, then `<TASK_HOME>/Instructions.md`, then compatible project history files if present.
5. Locate the active done file: user-specified record first, then `<TASK_HOME>/Done.md`, then compatible project history files if present.
6. Refresh `Current.md`, `Decision.md`, and `Worklog.md`.

Do not edit code before the active task and done files are understood.

### Stage 1: Define Boundary

Write to `Current.md`:

- task source;
- task mode;
- expected output;
- allowed files/modules;
- out-of-scope items;
- stop conditions.

If the task is still unclear after reading the task file and done record, write the blocking question to `Decision.md` and ask the user only for the minimum missing information.

### Stage 2: Read Minimal Context

Read in this order:

1. active task file;
2. active done file;
3. `<MEMORY_HOME>/stable-decisions.md` and `<MEMORY_HOME>/project-map.md`;
4. relevant `<REFERENCE_HOME>` documents;
5. code and Hydra configs only when the workspace documents are insufficient.

Avoid unbounded whole-repo searches. Use `rg` first when searching.

### Stage 3: Decision Gate

Must ask the user through `Decision.md` before changing:

- training target or objective;
- dataset semantics or selected data keys;
- input value range;
- latent type or feature semantics;
- loss semantics;
- compression accounting;
- checkpoint, resume, or EMA loading policy;
- public parameter names or test semantics;
- freeze/unfreeze policy or joint-training order;
- long training, downloads, or external access.

May decide and record in `Worklog.md`:

- helper names;
- small local structure;
- minimal test fixture shape;
- whether to extract a small helper;
- whether to add finite/non-finite checks.

May decide silently:

- import order;
- local variable cleanup;
- obvious typos;
- behavior-neutral formatting.

### Stage 4: Execute

Execution rules by type:

- Config recomposition: trace defaults and `_target_`; prefer config-only changes.
- Component extension: stay inside existing component boundaries; add focused tests when behavior changes.
- Pipeline assembly: identify reusable trainers, wrappers, losses, and data paths before adding new files.
- Diagnosis/explanation: read code/configs and answer; do not edit code unless requested.
- Documentation/skill maintenance: improve workflow, boundaries, file protocol, and decision rules without adding unrelated project detail.

Write only high-signal progress to `Worklog.md`.

For diagnosis/explanation or question-only work, if the answer required code/config/log investigation and the result is
not already captured in the project knowledge base, quickly write back the durable point to the closest
`<REFERENCE_HOME>/*.md` or `<MEMORY_HOME>/*.md` file before final response. Keep the note concise and factual.

### Stage 5: Validate

Validation level follows risk:

- docs: check structure, ordering, and stale path semantics;
- config: check defaults, interpolation, `_target_`, and trainer field usage;
- Python: run syntax checks and relevant tests when available;
- training logic: add a minimal test or static check when full training is impractical.

Record verified and unverified points in `Worklog.md`.

### Stage 6: Close Out

Required:

1. Update the active done file with a concise task index.
2. Update `<REFERENCE_HOME>` or `<MEMORY_HOME>` for reusable knowledge.
3. Update `<MEMORY_HOME>/stable-decisions.md` for durable choices.
4. Update `<MEMORY_HOME>/open-questions.md` for non-blocking unknowns.
5. Clear resolved content from `Decision.md`.
6. Mark `Current.md` completed or clear it for the next task.

Final chat response should only summarize what changed, where it lives, what was verified, and what remains unverified.

For user-declared question-only work that should not count as a formal task, skip adding a new done-task index unless
the user asks. Still update the relevant reference or memory note when new reusable knowledge was learned.

## Hydra Rules

For any Hydra-driven behavior, inspect:

- main config file;
- `defaults`;
- config group files;
- `_target_`;
- overrides in the main config;
- interpolation such as `${dataset.img_size}`;
- trainer or caller usage of the field.

Never infer model behavior from filename alone.

## Reuse Rules

Search for existing implementation before adding a new one:

- tokenizer: `src/stage1/cosmos/` and tokenizer configs;
- entropy/rANS: bpp codec code and project references;
- latent downstream: existing tokenizer wrappers and stage2 models;
- PanCollection data: existing PanCollection loaders and dataset configs;
- loss: existing stage1/stage2 loss containers;
- training loop: nearest existing trainer.

Extend existing code when the existing component only lacks a narrow capability. Add a new component only when responsibility genuinely does not fit.

## Compatible Legacy Inputs

If present or user-specified, current-project legacy files may be read as compatibility inputs, but they are not the formal workspace protocol:

```text
Starpansharpening/MindOrganising/*.md
Starpansharpening/Draft/*.md
Notes_Liang/Instructions.MD
Notes_Liang/Done.MD
Notes_Liang/*Overview.md
```

When useful, migrate stable information from these files into `<PROJECT_AGENT_HOME>`.

## Reuse Rules

Search for existing implementation before adding a new one:

- tokenizer: `src/stage1/cosmos/` and tokenizer configs;
- entropy/rANS: bpp codec code and project references;
- latent downstream: existing tokenizer wrappers and stage2 models;
- PanCollection data: existing PanCollection loaders and dataset configs;
- loss: existing stage1/stage2 loss containers;
- training loop: nearest existing trainer.

Extend existing code when the existing component only lacks a narrow capability. Add a new component only when responsibility genuinely does not fit.

## Compatible Legacy Inputs

If present or user-specified, current-project legacy files may be read as compatibility inputs, but they are not the formal workspace protocol:

```text
Starpansharpening/MindOrganising/*.md
Starpansharpening/Draft/*.md
Notes_Liang/Instructions.MD
Notes_Liang/Done.MD
Notes_Liang/*Overview.md
```

When useful, migrate stable information from these files into `<PROJECT_AGENT_HOME>`.
