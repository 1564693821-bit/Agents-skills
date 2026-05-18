from __future__ import annotations

import argparse
import shutil
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None


TEMPLATE_EXTENSIONS = {
    ".docx",
    ".doc",
    ".pdf",
    ".tex",
    ".md",
    ".txt",
    ".pptx",
    ".xlsx",
    ".csv",
}


def read_config(project_root: Path) -> dict:
    config_path = project_root / "task_config.yaml"
    if not config_path.exists() or yaml is None:
        return {}
    data = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    return data if isinstance(data, dict) else {}


def configured_dirs(project_root: Path, config: dict) -> list[Path]:
    names = [
        config.get("template_dir", "input/template"),
        config.get("problem_dir", "input/problems"),
        config.get("reference_dir", "input/references"),
    ]
    result: list[Path] = []
    for name in names:
        path = project_root / str(name)
        if path.exists() and path.is_dir() and path not in result:
            result.append(path)
    return result


def find_named_template(search_dirs: list[Path], configured_name: str) -> Path | None:
    if not configured_name:
        return None
    configured = Path(configured_name)
    candidates: list[Path] = []
    for directory in search_dirs:
        candidates.extend(path for path in directory.rglob("*") if path.is_file())

    for candidate in candidates:
        if candidate.name == configured.name:
            return candidate
    for candidate in candidates:
        if candidate.stem == configured.stem:
            return candidate
    for candidate in candidates:
        if configured_name.lower() in candidate.name.lower():
            return candidate
    return None


def find_first_template(search_dirs: list[Path]) -> Path | None:
    for directory in search_dirs:
        for candidate in sorted(directory.rglob("*")):
            if candidate.is_file() and candidate.suffix.lower() in TEMPLATE_EXTENSIONS:
                return candidate
    return None


def copy_template(source: Path, project_root: Path, force: bool) -> Path:
    target_dir = project_root / "work" / "assets" / "template_working"
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / source.name
    if target.exists() and not force:
        target = target_dir / f"{source.stem}.working{source.suffix}"
    shutil.copy2(source, target)
    return target


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Copy a report template or template-like input source into work/assets/template_working/."
    )
    parser.add_argument("project_root", nargs="?", default=".")
    parser.add_argument("--force", action="store_true", help="overwrite the direct working-copy target if it exists")
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    config = read_config(project_root)
    search_dirs = configured_dirs(project_root, config)
    source = find_named_template(search_dirs, str(config.get("template_filename", "") or ""))
    if source is None and (
        config.get("has_template")
        or config.get("template_filename")
        or any((project_root / "input" / "template").glob("*"))
    ):
        source = find_first_template(search_dirs)
    if source is None:
        print("No template or template-like source was found.")
        return 2

    target = copy_template(source, project_root, args.force)
    print(f"Source: {source}")
    print(f"Working copy: {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
