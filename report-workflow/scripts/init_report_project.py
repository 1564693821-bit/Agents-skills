#!/usr/bin/env python3
"""Initialize a standardized report workflow project in the current directory."""

from __future__ import annotations

import shutil
from pathlib import Path


ROOT = Path.cwd()
SKILL_DIR = Path(__file__).resolve().parents[1]
ASSETS_DIR = SKILL_DIR / "assets"

DIRECTORIES = [
    "input/problems",
    "input/references",
    "input/template",
    "work/code",
    "work/assets",
    "output",
]

FILES = {
    "README.md": "README.template.md",
    "task_config.yaml": "task_config.template.yaml",
    "work/task_inventory.md": "task_inventory.template.md",
    "work/notes.md": "notes.template.md",
    "work/draft.md": "draft.template.md",
    "work/checks.md": "checks.template.md",
}


def is_empty_file(path: Path) -> bool:
    return path.exists() and path.is_file() and path.stat().st_size == 0


def copy_template(destination: Path, template_name: str) -> str:
    source = ASSETS_DIR / template_name
    destination.parent.mkdir(parents=True, exist_ok=True)

    if destination.exists() and destination.is_file() and destination.stat().st_size > 0:
        return "skipped"

    if destination.exists() and not destination.is_file():
        return "skipped"

    shutil.copyfile(source, destination)
    return "created"


def main() -> int:
    created_dirs: list[str] = []
    skipped_dirs: list[str] = []
    created_files: list[str] = []
    skipped_files: list[str] = []

    for directory in DIRECTORIES:
        target = ROOT / directory
        if target.exists():
            skipped_dirs.append(directory + "/")
        else:
            target.mkdir(parents=True, exist_ok=True)
            created_dirs.append(directory + "/")

    for relative_path, template_name in FILES.items():
        target = ROOT / relative_path
        result = copy_template(target, template_name)
        if result == "created":
            created_files.append(relative_path)
        else:
            skipped_files.append(relative_path)

    print("The report project has been initialized.")
    print()
    print("Created directories:")
    for item in created_dirs or ["(none)"]:
        print(f"- {item}")
    print()
    print("Created files:")
    for item in created_files or ["(none)"]:
        print(f"- {item}")
    print()
    print("Skipped existing directories:")
    for item in skipped_dirs or ["(none)"]:
        print(f"- {item}")
    print()
    print("Skipped existing non-empty files:")
    for item in skipped_files or ["(none)"]:
        print(f"- {item}")
    print()
    print("Next steps:")
    print("1. Put problem files into input/problems/.")
    print("2. Put reference materials into input/references/.")
    print("3. Put template files into input/template/ if any.")
    print("4. Edit task_config.yaml.")
    print("5. Invoke this skill again to write the report.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
