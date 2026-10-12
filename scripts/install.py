"""Install the bundled skill without replacing any existing target (Python 3.9+)."""

import argparse
from pathlib import Path
import shutil
import sys

SKILL_NAME = "chatgpt-pro-handoff"


def install(skills_dir, source=None):
    source = Path(source) if source is not None else (
        Path(__file__).resolve().parents[1] / "skills" / SKILL_NAME
    )
    if source.is_symlink() or not source.is_dir():
        raise ValueError("Bundled skill must be a real directory")
    if not (source / "SKILL.md").is_file():
        raise ValueError("Bundled SKILL.md is missing")
    for item in source.rglob("*"):
        if item.is_symlink() or not (item.is_file() or item.is_dir()):
            raise ValueError("Unsupported bundled entry: {}".format(item.name))

    skills_dir = Path(skills_dir).expanduser()
    if skills_dir.is_symlink() or (skills_dir.exists() and not skills_dir.is_dir()):
        raise ValueError("Skills directory conflicts with a file or symbolic link")
    target = skills_dir / SKILL_NAME
    if target.exists() or target.is_symlink():
        raise FileExistsError("Refusing to overwrite existing target: {}".format(target))
    skills_dir.mkdir(parents=True, exist_ok=True)
    # Exclusive creation also refuses a target created after the earlier check.
    target.mkdir()
    try:
        shutil.copytree(source, target, dirs_exist_ok=True)
    except Exception:
        # Only remove the directory created by this installation attempt.
        shutil.rmtree(target)
        raise
    return target


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skills-dir", type=Path, default=Path.home() / ".codex" / "skills")
    args = parser.parse_args()
    try:
        target = install(args.skills_dir)
    except (OSError, ValueError) as exc:
        print("Install failed: {}".format(exc), file=sys.stderr)
        return 1
    print("Installed: {}".format(target))
    return 0


if __name__ == "__main__":
    sys.exit(main())
