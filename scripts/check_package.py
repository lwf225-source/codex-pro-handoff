"""Check package structure and common private-data patterns, using only stdlib."""

import argparse
from pathlib import Path
import re
import sys

REQUIRED = (
    "README.md", "docs/usage.md", "examples/prompts.md",
    "skills/chatgpt-pro-handoff/SKILL.md", "scripts/install.py",
    "scripts/check_package.py", "tests/test_package.py", ".gitignore",
    ".github/workflows/check.yml",
)
PATTERNS = {
    "personal home path": re.compile(r"/" + r"Users/[^/\s]+", re.I),
    "email address": re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.I),
    "conversation URL": re.compile(r"chatgpt\.com/c/", re.I),
    "UUID": re.compile(r"\b[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}\b", re.I),
    "key-like token": re.compile(r"\bsk-[A-Za-z0-9_-]{16,}\b"),
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "credential assignment": re.compile(
        r"\b(?:api_key|access_token|password)\s*[:=]\s*['\"][^'\"\s]{8,}['\"]", re.I
    ),
}


def privacy_findings(text):
    # Report categories, never print matched secrets.
    return [name for name, pattern in PATTERNS.items() if pattern.search(text)]


def check_package(root):
    root = Path(root)
    errors = []
    for relative in REQUIRED:
        if not (root / relative).is_file():
            errors.append("Missing required file: " + relative)
    for item in sorted(root.rglob("*")):
        relative = item.relative_to(root)
        if any(part in (".git", "__pycache__") for part in relative.parts):
            continue
        if item.is_symlink():
            errors.append("Symbolic link: " + str(relative))
            continue
        if item.is_file():
            try:
                content = item.read_text(encoding="utf-8")
            except (OSError, UnicodeError):
                errors.append("Unreadable or non-text file: " + str(relative))
                continue
            for category in privacy_findings(content):
                errors.append("{}: {}".format(relative, category))
    skill = root / "skills/chatgpt-pro-handoff/SKILL.md"
    if skill.is_file() and not skill.is_symlink():
        content = skill.read_text(encoding="utf-8")
        match = re.match(r"\A---\n(.*?)\n---\n", content, re.S)
        if not match:
            errors.append("Missing skill frontmatter")
        else:
            fields = match.group(1).splitlines()
            if "name: chatgpt-pro-handoff" not in fields:
                errors.append("Wrong skill name")
            if not any(line.startswith("description: ") and line[13:].strip() for line in fields):
                errors.append("Missing skill description")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    errors = check_package(args.root)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("Package structure and privacy-pattern checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
