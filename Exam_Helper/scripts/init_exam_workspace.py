#!/usr/bin/env python3
"""Initialize an Exam_Helper review workspace."""

from __future__ import annotations

import shutil
import sys
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
ASSET_ROOT = SKILL_ROOT / "assets" / "starter_files"

DIRS = [
    "input/diagnosis",
    "input/ppt",
    "input/past_papers",
    "input/homework",
    "input/textbook",
    "input/notes",
    "input/online_course",
    "input/teacher_hints",
    "work/assets",
    "output",
]

FILES = {
    "README.md": "README.md",
    "exam_config.yaml": "exam_config.yaml",
    "input/diagnosis/00_课程诊断表.md": "00_课程诊断表.md",
    "work/resource_inventory.md": "resource_inventory.md",
    "work/exam_diagnosis.md": "exam_diagnosis.md",
    "work/strategy.md": "strategy.md",
    "work/knowledge_map.md": "knowledge_map.md",
    "work/question_type_map.md": "question_type_map.md",
    "work/active_recall_bank.md": "active_recall_bank.md",
    "work/mistake_log.md": "mistake_log.md",
    "work/daily_plan.md": "daily_plan.md",
    "work/review_log.md": "review_log.md",
    "work/sprint_plan.md": "sprint_plan.md",
    "work/generated_questions.md": "generated_questions.md",
}


def copy_if_safe(src: Path, dst: Path) -> str:
    if dst.exists() and dst.stat().st_size > 0:
        return "skipped"
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)
    return "created"


def main() -> int:
    if len(sys.argv) > 2:
        print("Usage: init_exam_workspace.py [project-root]", file=sys.stderr)
        return 2

    root = Path(sys.argv[1]).resolve() if len(sys.argv) == 2 else Path.cwd()
    root.mkdir(parents=True, exist_ok=True)

    created_dirs = []
    for rel in DIRS:
        path = root / rel
        if not path.exists():
            path.mkdir(parents=True)
            created_dirs.append(rel)

    created_files = []
    skipped_files = []
    for rel, asset_name in FILES.items():
        status = copy_if_safe(ASSET_ROOT / asset_name, root / rel)
        if status == "created":
            created_files.append(rel)
        else:
            skipped_files.append(rel)

    print("Exam review workspace initialized.")
    if created_dirs:
        print("\nCreated directories:")
        for item in created_dirs:
            print(f"- {item}")
    if created_files:
        print("\nCreated files:")
        for item in created_files:
            print(f"- {item}")
    if skipped_files:
        print("\nSkipped non-empty files:")
        for item in skipped_files:
            print(f"- {item}")

    print(
        "\nNext steps:\n"
        "1. Fill input/diagnosis/00_课程诊断表.md.\n"
        "2. Put PPT files into input/ppt/.\n"
        "3. Put past papers and answers into input/past_papers/.\n"
        "4. Put homework, textbook, notes, online course materials, and teacher hints into matching folders.\n"
        "5. Invoke Exam_Helper again for diagnosis."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
