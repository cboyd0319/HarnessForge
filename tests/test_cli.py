from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from harnessforge.cli import main


class CliTests(unittest.TestCase):
    def test_help_returns_zero(self) -> None:
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            code = main(["--help"])

        self.assertEqual(code, 0)
        self.assertIn("harnessforge", stdout.getvalue())

    def test_missing_subcommand_returns_usage_error(self) -> None:
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            code = main([])

        self.assertEqual(code, 2)
        self.assertIn("harnessforge", stdout.getvalue())

    def test_init_and_audit_commands(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            stdout = io.StringIO()
            with contextlib.redirect_stdout(stdout):
                init_code = main(["init", "--target", str(root)])
            with contextlib.redirect_stdout(io.StringIO()):
                audit_code = main(["audit", "--target", str(root), "--min-score", "85"])

        self.assertEqual(init_code, 0)
        self.assertEqual(audit_code, 0)
        self.assertIn("Detected stack", stdout.getvalue())

    def test_inspect_command_reports_profile_without_writing_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "pyproject.toml").write_text(
                "[project]\nname='demo'\n",
                encoding="utf-8",
            )
            stdout = io.StringIO()
            with contextlib.redirect_stdout(stdout):
                code = main(["inspect", "--target", str(root)])

            agents_exists = (root / "AGENTS.md").exists()

        self.assertEqual(code, 0)
        self.assertFalse(agents_exists)
        self.assertIn("Detected stack: python", stdout.getvalue())
        self.assertIn("Verification commands:", stdout.getvalue())

    def test_inspect_json_reports_detected_profile(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "Cargo.toml").write_text(
                "[workspace]\nmembers = ['crates/*']\n",
                encoding="utf-8",
            )
            (root / "justfile").write_text(
                "ci:\n\tcargo test --workspace\n",
                encoding="utf-8",
            )
            stdout = io.StringIO()
            with contextlib.redirect_stdout(stdout):
                code = main(["inspect", "--target", str(root), "--json"])

            payload = json.loads(stdout.getvalue())

        self.assertEqual(code, 0)
        self.assertEqual(payload["detectedStack"], "rust")
        self.assertIn("just", payload["packageManagers"])
        self.assertIn("just ci", payload["verificationCommands"])
        self.assertIn("justfile", payload["routingMarkers"])

    def test_init_can_scaffold_optional_workflows(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            stdout = io.StringIO()
            with contextlib.redirect_stdout(stdout):
                code = main(
                    [
                        "init",
                        "--target",
                        str(root),
                        "--with-ci-workflow",
                        "--with-self-heal-workflow",
                    ]
                )

            ci = root / ".github/workflows/harnessforge.yml"
            self_heal = root / ".github/workflows/harness-self-heal.yml"
            ci_exists = ci.exists()
            self_heal_exists = self_heal.exists()

        self.assertEqual(code, 0)
        self.assertTrue(ci_exists)
        self.assertTrue(self_heal_exists)
        self.assertIn("Optional workflow scaffold review required", stdout.getvalue())
        self.assertIn("<reviewed-commit-sha>", stdout.getvalue())
        self.assertIn("permissions", stdout.getvalue())

    def test_init_can_generate_macos_only_contract(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with contextlib.redirect_stdout(io.StringIO()):
                code = main(
                    [
                        "init",
                        "--target",
                        str(root),
                        "--platform-contract",
                        "macos-only",
                    ]
                )

            manifest = json.loads(
                (root / "docs/harness/manifest.json").read_text(encoding="utf-8")
            )
            init_sh_exists = (root / "init.sh").exists()
            init_ps1_exists = (root / "init.ps1").exists()

        self.assertEqual(code, 0)
        self.assertTrue(init_sh_exists)
        self.assertFalse(init_ps1_exists)
        self.assertIn("macosOnly", manifest["supportedPlatforms"])
        self.assertNotIn("init.ps1", manifest["requiredFiles"])

    def test_update_drift_report_detects_modified_generated_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with contextlib.redirect_stdout(io.StringIO()):
                init_code = main(["init", "--target", str(root)])
            (root / "AGENTS.md").write_text(
                "# edited\n\nlocal change\n",
                encoding="utf-8",
            )
            stdout = io.StringIO()
            with contextlib.redirect_stdout(stdout):
                report_code = main(
                    [
                        "update",
                        "--target",
                        str(root),
                        "--drift-report",
                        "--json",
                    ]
                )
            payload = json.loads(stdout.getvalue())
            claude_text = (root / "CLAUDE.md").read_text(encoding="utf-8")

        self.assertEqual(init_code, 0)
        self.assertEqual(report_code, 0)
        drift = {item["path"]: item for item in payload["drift"]}
        self.assertEqual(drift["AGENTS.md"]["fileStatus"], "modified")
        self.assertEqual(drift["AGENTS.md"]["ownership"], "generated")
        self.assertFalse(claude_text.startswith("# edited"))

    def test_init_records_existing_files_as_project_owned_without_initial_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "AGENTS.md").write_text(
                "# Existing\n\nKeep local instructions.\n",
                encoding="utf-8",
            )
            init_stdout = io.StringIO()
            with contextlib.redirect_stdout(init_stdout):
                init_code = main(["init", "--target", str(root)])
            stdout = io.StringIO()
            with contextlib.redirect_stdout(stdout):
                report_code = main(
                    [
                        "update",
                        "--target",
                        str(root),
                        "--drift-report",
                        "--json",
                    ]
                )
            payload = json.loads(stdout.getvalue())

        self.assertEqual(init_code, 0)
        self.assertEqual(report_code, 0)
        self.assertIn("Existing files preserved", init_stdout.getvalue())
        self.assertIn("HARNESSFORGE_AGENTS.md", init_stdout.getvalue())
        drift = {item["path"]: item for item in payload["drift"]}
        self.assertEqual(drift["AGENTS.md"]["ownership"], "project")
        self.assertEqual(drift["AGENTS.md"]["fileStatus"], "unchanged")

    def test_init_can_enhance_existing_instruction_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "pyproject.toml").write_text(
                "[project]\nname='demo'\n",
                encoding="utf-8",
            )
            (root / "AGENTS.md").write_text(
                "# Existing\n\nKeep local instructions.\n",
                encoding="utf-8",
            )
            stdout = io.StringIO()
            with contextlib.redirect_stdout(stdout):
                init_code = main(
                    ["init", "--target", str(root), "--enhance-existing"]
                )
            with contextlib.redirect_stdout(io.StringIO()):
                audit_code = main(
                    ["audit", "--target", str(root), "--min-score", "100"]
                )
            agents = (root / "AGENTS.md").read_text(encoding="utf-8")

        self.assertEqual(init_code, 0)
        self.assertEqual(audit_code, 0)
        self.assertIn("ENHANCED AGENTS.md", stdout.getvalue())
        self.assertIn("Keep local instructions.", agents)
        self.assertIn("HarnessForge Quality Addendum", agents)

    def test_audit_requires_explicit_override_for_local_absolute_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with contextlib.redirect_stdout(io.StringIO()):
                init_code = main(["init", "--target", str(root)])
            (root / "README.md").write_text(
                "Local checkout was /Users/person/private/repo\n",
                encoding="utf-8",
            )
            stdout = io.StringIO()
            with contextlib.redirect_stdout(stdout):
                strict_code = main(
                    ["audit", "--target", str(root), "--min-score", "100"]
                )
            with contextlib.redirect_stdout(io.StringIO()):
                allowed_code = main(
                    [
                        "audit",
                        "--target",
                        str(root),
                        "--min-score",
                        "85",
                        "--allow-local-absolute-paths",
                    ]
                )

        self.assertEqual(init_code, 0)
        self.assertEqual(strict_code, 1)
        self.assertEqual(allowed_code, 0)
        self.assertIn("Durable harness text avoids local absolute paths", stdout.getvalue())

    def test_update_without_apply_does_not_write(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            stdout = io.StringIO()
            with contextlib.redirect_stdout(stdout):
                code = main(["update", "--target", str(root)])

            self.assertEqual(code, 0)
            self.assertFalse((root / "AGENTS.md").exists())
            self.assertIn("No files changed", stdout.getvalue())

    def test_init_rejects_unsafe_agent_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            stderr = io.StringIO()
            with contextlib.redirect_stderr(stderr):
                code = main(["init", "--target", tmp, "--agent-file", "../AGENTS.md"])

        self.assertEqual(code, 2)
        self.assertIn("--agent-file", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
