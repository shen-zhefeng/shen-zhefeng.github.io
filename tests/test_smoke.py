#!/usr/bin/env python3
"""Check that the smoke script cannot leave drafts ready for publication.

Run with: python3 -m unittest discover --start-directory tests --verbose
These tests use temporary sites and a fake Zola command. They need only Python's
standard library and Bash; they neither build the real site nor access networks.
"""

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import textwrap
import unittest


ROOT = Path(__file__).resolve().parents[1]


class SmokeScriptTests(unittest.TestCase):
    def run_fixture(self, mode="success", failing_suite=False):
        temporary = tempfile.TemporaryDirectory(prefix="zola-smoke-test-")
        self.addCleanup(temporary.cleanup)
        directory = Path(temporary.name)
        site = directory / "site"
        site.mkdir()
        (site / "tests").mkdir()
        shutil.copy2(ROOT / "test.sh", site / "test.sh")
        # Supply a real, passing discovery target. Python 3.14 reports empty
        # test discovery as an error; the marker also proves this suite ran.
        (site / "tests" / "test_fixture.py").write_text(textwrap.dedent('''\
            from pathlib import Path
            import unittest

            class FixtureTest(unittest.TestCase):
                def test_production_exists(self):
                    self.assertTrue(Path("public/about/index.html").is_file())
                    Path("regression-ran").touch()
        '''))

        # Use a separate caller directory to also exercise test.sh's directory
        # handling: every generated file should stay inside the fixture site.
        caller = directory / "caller"
        caller.mkdir()
        executables = directory / "bin"
        executables.mkdir()
        zola = executables / "zola"
        zola.write_text("#!" + sys.executable + "\n" + textwrap.dedent('''\
            import json
            import os
            from pathlib import Path
            import sys

            arguments = sys.argv[1:]
            with Path("commands.jsonl").open("a") as log:
                log.write(json.dumps(arguments) + "\\n")
            mode = os.environ["SMOKE_FIXTURE_MODE"]
            if arguments == ["check"]:
                sys.exit(0)
            if not arguments or arguments[0] != "build":
                sys.exit("Unexpected fixture command: " + repr(arguments))

            drafts = "--drafts" in arguments
            output = Path(arguments[arguments.index("--output-dir") + 1]
                          if "--output-dir" in arguments else "public")
            output.mkdir(parents=True, exist_ok=True)
            if drafts and mode == "draft-failure":
                (output / "partial.html").write_text("Incomplete draft build")
                sys.exit(17)

            pages = ["about", "research", "teaching", "cn/about", "ja/about"]
            if not drafts and mode == "missing-production":
                pages.remove("research")
            if (drafts and mode != "missing-draft") or mode == "leaked-draft":
                pages.append("test")
            for page in pages:
                destination = output / page / "index.html"
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_text("Fixture page")
        '''))
        zola.chmod(0o755)

        if failing_suite:
            (site / "tests" / "test_failure.py").write_text(textwrap.dedent('''\
                import unittest

                class RegressionTest(unittest.TestCase):
                    def test_failure(self):
                        self.fail("Fixture regression must block publication")
            '''))

        environment = os.environ.copy()
        environment["PATH"] = str(executables) + os.pathsep + environment["PATH"]
        environment["SMOKE_FIXTURE_MODE"] = mode
        result = subprocess.run(
            ["bash", str(site / "test.sh")], cwd=caller, env=environment,
            text=True, capture_output=True, timeout=30,
        )
        commands = [json.loads(line) for line in
                    (site / "commands.jsonl").read_text().splitlines()]
        self.assertEqual(list(caller.iterdir()), [], "Build output escaped the site directory")
        return result, site, commands

    def assert_drafts_cleaned(self, site, commands):
        self.assertEqual(list(site.glob(".zola-drafts.*")), [],
                         "Temporary draft output survived the smoke script")
        draft_command = next(command for command in commands if "--drafts" in command)
        self.assertIn("--output-dir", draft_command,
                      "Drafts must have their own output directory")
        draft_output = Path(draft_command[draft_command.index("--output-dir") + 1])
        self.assertNotEqual(draft_output.resolve(), (site / "public").resolve())
        self.assertFalse(draft_output.exists(), "Draft build directory was not removed")

    def test_success_keeps_production_and_cleans_drafts(self):
        result, site, commands = self.run_fixture()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual([command[0] for command in commands], ["build", "build", "check"])
        for page in ("about", "research", "teaching", "cn/about", "ja/about"):
            self.assertTrue((site / "public" / page / "index.html").is_file())
        self.assertTrue((site / "regression-ran").is_file(), "The discovered suite did not run")
        self.assertFalse((site / "public" / "test").exists())
        self.assert_drafts_cleaned(site, commands)

    def test_failed_draft_build_cleans_partial_output_and_stops_checks(self):
        result, site, commands = self.run_fixture(mode="draft-failure")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual([command[0] for command in commands], ["build", "build"])
        self.assert_drafts_cleaned(site, commands)

    def test_missing_pages_or_drafts_in_production_fail_validation(self):
        for mode in ("missing-production", "missing-draft", "leaked-draft"):
            with self.subTest(mode=mode):
                result, site, commands = self.run_fixture(mode=mode)
                self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertEqual([command[0] for command in commands], ["build", "build"])
                self.assert_drafts_cleaned(site, commands)

    def test_discovered_regression_failure_stops_later_checks(self):
        result, site, commands = self.run_fixture(failing_suite=True)
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Fixture regression must block publication", result.stderr)
        self.assertEqual([command[0] for command in commands], ["build", "build"])
        self.assert_drafts_cleaned(site, commands)


if __name__ == "__main__":
    unittest.main(verbosity=2)
