import importlib.util
import contextlib
import io
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]


def load_script(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


installer = load_script("install")
checker = load_script("check_package")


class PackageTests(unittest.TestCase):
    def test_package_checks(self):
        self.assertEqual(checker.check_package(ROOT), [])

    def test_cli_install_and_refuse_repeat(self):
        with tempfile.TemporaryDirectory() as directory:
            dest = Path(directory) / "custom skills"
            command = [sys.executable, str(ROOT / "scripts/install.py"), "--skills-dir", str(dest)]
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            installed = dest / installer.SKILL_NAME / "SKILL.md"
            self.assertEqual(installed.read_bytes(), (ROOT / "skills" / installer.SKILL_NAME / "SKILL.md").read_bytes())
            original = installed.read_bytes()
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(installed.read_bytes(), original)

    def test_default_location_in_temporary_home(self):
        with tempfile.TemporaryDirectory() as directory:
            with mock.patch.object(installer.Path, "home", return_value=Path(directory)):
                with mock.patch.object(sys, "argv", ["install.py"]):
                    with contextlib.redirect_stdout(io.StringIO()):
                        self.assertEqual(installer.main(), 0)
            installed = Path(directory) / ".codex" / "skills" / installer.SKILL_NAME / "SKILL.md"
            self.assertEqual(installed.read_bytes(), (ROOT / "skills" / installer.SKILL_NAME / "SKILL.md").read_bytes())

    def test_target_conflicts(self):
        for kind in ("directory", "file", "link", "dangling_link"):
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as directory:
                dest = Path(directory)
                target = dest / installer.SKILL_NAME
                if kind == "directory":
                    target.mkdir()
                elif kind == "file":
                    target.write_text("keep", encoding="utf-8")
                else:
                    other = dest / "other"
                    if kind == "link":
                        other.mkdir()
                    target.symlink_to(other, target_is_directory=True)
                with self.assertRaises(FileExistsError):
                    installer.install(dest)
                if kind == "file":
                    self.assertEqual(target.read_text(), "keep")
                elif kind.endswith("link"):
                    self.assertTrue(target.is_symlink())
                else:
                    self.assertEqual(list(target.iterdir()), [])

    def test_skills_root_conflicts(self):
        for kind in ("file", "link"):
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as directory:
                dest = Path(directory) / "skills"
                if kind == "file":
                    dest.write_text("keep", encoding="utf-8")
                else:
                    dest.symlink_to(Path(directory) / "missing", target_is_directory=True)
                with self.assertRaises(ValueError):
                    installer.install(dest)

    def test_source_link_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "source"
            source.mkdir()
            (source / "SKILL.md").symlink_to(ROOT / "skills" / installer.SKILL_NAME / "SKILL.md")
            dest = Path(directory) / "dest"
            with self.assertRaises(ValueError):
                installer.install(dest, source)
            self.assertFalse(dest.exists())

    def test_privacy_categories(self):
        samples = {
            "personal home path": "/" + "Users/" + "example/private",
            "email address": "person" + "@" + "example.org",
            "conversation URL": "https://chatgpt.com/" + "c/" + "example",
            "UUID": "12345678" + "-1234" * 3 + "-123456789abc",
            "key-like token": "sk-" + "x" * 24,
            "private key": "-----BEGIN " + "PRIVATE KEY-----",
            "credential assignment": "password" + " = " + "'" + "x" * 12 + "'",
        }
        for category, sample in samples.items():
            with self.subTest(category=category):
                self.assertIn(category, checker.privacy_findings(sample))
        self.assertEqual(checker.privacy_findings("https://chatgpt.com/ ordinary Chat"), [])

    def test_privacy_scan_covers_extra_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "extra.md").write_text("person" + "@" + "example.org", encoding="utf-8")
            self.assertIn("extra.md: email address", checker.check_package(root))


if __name__ == "__main__":
    unittest.main()
