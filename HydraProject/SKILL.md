---
name: hydra-project
description: Work inside Hydra-based research engineering projects with strict project-root workspace rules, staged task workflow, decision gates, and reuse-first code navigation. Use for Hydra config changes, component extensions, pipeline assembly, debugging, documentation, and skill/project memory maintenance.
---

# Hydra Project Skill

Use this skill for Hydra-based research codebases where behavior is spread across config defaults, `_target_`
instantiation, trainers, data loaders, losses, wrappers, and checkpoints.

This skill has two responsibilities:

1. Keep the installed skill directory stable.
2. Maintain project-specific task state under the current project root.

## Project Workspace

The installed skill directory contains only stable rules and bundled resources. Runtime task state must live under the
current project root:

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

Do not write project task state, decisions, work logs, project memory, or experiment notes into the installed skill
directory unless the user explicitly asks to modify the skill itself.

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

Keep code, commands, paths, config keys, class names, function names, API names, log snippets, and exact error
messages in their original language when that preserves correctness.

## Project Files

Human-facing entrypoint:

- `<PROJECT_AGENT_HOME>/README.md`: explains the workspace layout and where the user should look after a task.

Short-lived task state:

- `<TASK_HOME>/Instructions.md`: user-maintained current task instructions. This file is mandatory; create it if
  missing. It may be empty when the latest chat request is the task source.
- `<TASK_HOME>/Current.md`: current task boundary.
- `<TASK_HOME>/Decision.md`: blocking user decisions.
- `<TASK_HOME>/Worklog.md`: high-signal current progress.

Long-lived memory:

- `<TASK_HOME>/Done.md`: concise task index.
- `<MEMORY_HOME>/project-map.md`: project layers and key call chains.
- `<MEMORY_HOME>/stable-decisions.md`: choices that should be reused later.
- `<MEMORY_HOME>/open-questions.md`: non-blocking unknowns.
- `<REFERENCE_HOME>/*.md`: stable technical references.

Operational folders:

- `<CHECKLIST_HOME>/`: task and validation checklists.
- `<SNIPPET_HOME>/`: reusable commands or small helper scripts.
- `<DRAFT_HOME>/`: design drafts, usually named by task number plus topic.
- `<SCRATCH_HOME>/`: ad hoc user tests and temporary figures, following the scratch contract below.

Refresh short-lived files at task boundaries. Update long-lived files only after completing a task or confirming reusable
knowledge.

## Project Code Layout

The project should gradually converge toward a stable research-engineering layout. This is a direction of travel, not a
reason to interrupt the task with broad refactors. In a small or new project, create only the folders needed for the
current work, but place new formal files where they would still make sense after the project grows.

Preferred top-level separation:

```text
<PROJECT_ROOT>/
  src/                 # importable reusable library code
  scripts/             # executable entrypoints, Hydra configs, data prep, tests, figures, inference
  CodexWorkspace/      # agent notes, task state, scratch outputs
  runs/                # generated training/eval outputs, never source of truth
  data/ or Data*/      # datasets or local mounts, usually not committed
  playground/          # reference or exploratory external code, not formal project code
```

### `src/` Library Structure

Use `src/` for reusable, importable project code. Prefer domain/stage modules over flat utility piles:

```text
src/
  data/                         # reusable datasets, dataloaders, samplers, data transforms
  stage1/                       # representation/tokenizer/pretraining components
    cosmos/                     # tokenizer/model families and their modules
    discretization/             # quantizers, codecs, entropy/rANS, token collections
    self_supervised/            # proxy/self-supervised objectives and heads
    utilities/                  # stage1-specific losses/train helpers
  stage2/                       # downstream tasks built on frozen or adapted representations
    <task>/                     # e.g. segmentation, pansharpening, denoise, stereo_matching
      data/
      models/ or model/
      loss/
      metrics/
      utils/
    layers/                     # shared downstream layers and wrappers
    utilities/                  # shared downstream helpers
  stage3/                       # later-stage or foundation-model integrations when needed
  utilities/                    # cross-stage config, logging, tracking, IO, metrics, network, optim
  tests/                        # formal pytest-style tests for reusable code
```

Placement rules for `src/`:

- Put reusable classes/functions in `src/`, not under `scripts/` or `CodexWorkspace/scratch/`.
- Put task-specific downstream code under `src/stage2/<task>/...`; put representation/tokenizer code under `src/stage1/...`.
- Put cross-cutting utilities in `src/utilities/` only when they are truly stage-agnostic; otherwise keep them near the
  stage or task that owns the concept.
- Put formal tests in `src/tests/` when they validate library behavior across entrypoints.
- When adopting external/reference code, keep it in `playground/` until it becomes formal; formalized parts should move
  into the appropriate `src/` module with a narrow interface.

### `scripts/` Operational Structure

Use `scripts/` for runnable workflows and Hydra configuration, not for reusable model logic:

```text
scripts/
  trainer/                      # training entrypoints and trainer orchestration classes
  configs/                      # Hydra config roots, grouped by experiment family or task
    <family>/
      dataset/
      model/ or tokenizer/
      accelerator/
      loss/ or vq_loss/
      experiment/
      tracking/
      _legacy/                  # old configs kept only to avoid confusion or preserve history
  dataset/                      # dataset conversion/import scripts grouped by dataset name
  data_prepare/                 # reusable preparation pipelines not tied to one dataset folder
  infer/                        # inference/evaluation entrypoints
  tests/                        # smoke/integration/benchmark scripts that are not library tests
  figs/                         # figure-generation scripts and notebooks
  cmds/                         # shell command snippets or launch helpers that belong in-repo
  utils/                        # small script-only helpers
```

Placement rules for `scripts/`:

- Put Hydra entry configs under `scripts/configs/<family>/`; keep config groups such as `dataset/`, `model/`,
  `tokenizer/`, `accelerator/`, `experiment/`, and `tracking/` rather than one giant config directory.
- Put trainer entrypoints under `scripts/trainer/`; they may orchestrate `src/` modules but should not hide reusable
  model/loss/dataloader logic that belongs in `src/`.
- Put dataset conversion scripts under `scripts/dataset/<dataset-name>/` when tied to one dataset, or
  `scripts/data_prepare/` when the pipeline is reusable across datasets.
- Put generated figures and paper plots under `scripts/figs/`; put temporary diagnostic figures under
  `<SCRATCH_HOME>` instead.
- Put ad hoc launch snippets for the user in `<SNIPPET_HOME>` unless the script is a stable project entrypoint; stable
  project launchers can live under `scripts/cmds/` or an existing project convention.

### Gradual Maintenance Rules

When creating or moving files:

- First follow the existing local convention if one already exists. If the project is small, create the smallest
  compatible slice of the structure above.
- Do not reorganize unrelated folders just to match the ideal layout. Move files only when the current task needs it or
  when a new file would otherwise deepen disorder.
- When a new formal module, config family, trainer, dataset converter, or reusable test is added, update
  `<MEMORY_HOME>/project-map.md` or a nearby reference note with the new location and call chain.
- If a scratch script becomes useful beyond one investigation, promote it into `src/` or `scripts/` and leave a short
  note in the scratch README pointing to the formal location.
- Prefer names that describe the owning layer and task (`stage1`, `stage2/<task>`, `configs/<family>`) over names that
  only describe the current experiment date or one-off run.

## Scratch File Contract

`<SCRATCH_HOME>` is for user-requested ad hoc tests, quick visualization scripts, disposable probes, and their outputs.
It must not become a flat dumping ground.

Allowed files directly under `<SCRATCH_HOME>`:

- `README.md`: human-facing index of scratch experiments.
- `.gitkeep` or equivalent empty marker if needed.

Every ad hoc experiment must live in a dated slug folder:

```text
<SCRATCH_HOME>/<YYYY-MM-DD>-<short-topic>/
  README.md
  scripts/
  figures/
  outputs/
  tmp/
```

Use these meanings:

- `README.md`: purpose, inputs/checkpoints, exact command, important outputs, and one-line interpretation.
- `scripts/`: runnable user-test scripts that may be reused or debugged later.
- `figures/`: final human-facing images.
- `outputs/`: non-image result files worth keeping, such as small CSV/JSON summaries.
- `tmp/`: intermediate files created during execution. Delete `tmp/` contents after successful completion unless the
  user explicitly asks to inspect them.

Rules:

- Do not put reusable project code in `<SCRATCH_HOME>`; move it into `src/`, `scripts/`, or `src/tests/` when it
  becomes formal.
- Do not put pytest tests in `<SCRATCH_HOME>`; formal tests belong in `src/tests/`.
- Do not leave generated `__pycache__`, raw video dumps, temporary arrays, or one-off checkpoints in scratch roots.
- When generating a figure for the user, write or update the experiment `README.md` and the root
  `<SCRATCH_HOME>/README.md`.
- If an older scratch root is flat, reorganize it into dated experiment folders before adding more files.

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
3. Create `<PROJECT_AGENT_HOME>/README.md` if missing. It must explain the workspace layout, user-facing files,
   agent-facing files, and what the user should check after each task.
4. Create `<TASK_HOME>/Instructions.md` if missing. It must explain that users may place current task instructions
   there and that an empty file means the latest chat request is the task source.
5. Locate the active task file: user-specified file first, then `<TASK_HOME>/Instructions.md`, then compatible
   project history files if present.
6. Locate the active done file: user-specified record first, then `<TASK_HOME>/Done.md`, then compatible project
   history files if present.
7. Refresh `Current.md`, `Decision.md`, and `Worklog.md`.

Do not edit code before the active task and done files are understood.

### Stage 1: Define Boundary

Write to `Current.md`:

- task source;
- task mode;
- expected output;
- allowed files/modules;
- out-of-scope items;
- stop conditions.

If the task is still unclear after reading the task file and done record, write the blocking question to `Decision.md`
and ask the user only for the minimum missing information.

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
- New file placement: choose `src/` for reusable importable logic, `scripts/` for runnable workflows/configs/data prep,
  and `<SCRATCH_HOME>` for disposable investigations; create only the smallest folder slice needed.

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

When adding a new component, place it in the canonical layer from `Project Code Layout` and record the location in
`<MEMORY_HOME>/project-map.md` once the task is complete.

## Compatible Legacy Inputs

If present or user-specified, current-project legacy files may be read as compatibility inputs, but they are not the
formal workspace protocol:

```text
Starpansharpening/MindOrganising/*.md
Starpansharpening/Draft/*.md
Notes_Liang/Instructions.MD
Notes_Liang/Done.MD
Notes_Liang/*Overview.md
```

When useful, migrate stable information from these files into `<PROJECT_AGENT_HOME>`.
