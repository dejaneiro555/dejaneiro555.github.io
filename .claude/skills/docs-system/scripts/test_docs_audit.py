"""Run: python3 -m unittest discover -s scripts   (from the skill folder)"""
import subprocess
import tempfile
import unittest
from pathlib import Path

import docs_audit


def levels(root, level):
    return [(p, m) for lv, p, m in docs_audit.audit(root) if lv == level]


class DocsAuditTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.addCleanup(self.tmp.cleanup)

    def test_empty_repo_fails_and_init_fixes_structure(self):
        self.assertTrue(levels(self.root, "ERROR"))
        (self.root / "README.md").write_text("# X\n")  # init never writes the project README
        created = docs_audit.init(self.root)
        self.assertIn("docs/decisions/adr-template.md", created)
        self.assertEqual(levels(self.root, "ERROR"), [])
        # scaffold placeholders are reported, so a fresh scaffold cannot pass as documented
        self.assertTrue(any("placeholder" in m for _, m in levels(self.root, "WARN")))

    def test_init_never_overwrites_and_respects_existing_layout(self):
        (self.root / "GOVERNANCE.md").write_text("# Rules\n")
        (self.root / "CHANGELOG.md").write_text("mine\n")
        created = docs_audit.init(self.root)
        self.assertEqual((self.root / "CHANGELOG.md").read_text(), "mine\n")
        self.assertFalse(any(c.startswith("docs/governance") for c in created))
        self.assertEqual(docs_audit.init(self.root), [])  # second run creates nothing

    def test_broken_link_orphan_and_adr_checks(self):
        (self.root / "README.md").write_text("# X\n")
        docs_audit.init(self.root)
        d = self.root / "docs"
        (d / "how-to" / "lost.md").write_text("# How to\n[gone](nope.md) `[code](skip.md)`\n")
        (d / "decisions" / "0001-x.md").write_text("# X\n")
        (d / "decisions" / "0002-y.md").write_text("---\nstatus: accepted\n---\n# Y\n")
        (d / "decisions" / "README.md").write_text("[y](0002-y.md)\n")
        docs_audit.write_map(self.root)  # the map links every file; it must not hide orphans
        errors, warns = levels(self.root, "ERROR"), levels(self.root, "WARN")
        self.assertEqual(errors, [("docs/how-to/lost.md", "broken link: nope.md")])
        self.assertIn(("docs/how-to/lost.md", "orphan: no other Markdown file links to it"), warns)
        self.assertIn(("docs/decisions/0001-x.md", "ADR has no status"), warns)
        self.assertTrue(any(p == "docs/decisions/0001-x.md" and "index" in m for p, m in warns))
        self.assertFalse(any(p == "docs/decisions/0002-y.md" for p, _ in warns))


class MapTest(unittest.TestCase):
    """docs/MAP.md: generated, checked for staleness, never overriding a repo's own generator."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.addCleanup(self.tmp.cleanup)
        (self.root / "README.md").write_text("# Project\nSee [the ADR](docs/adr/0001-x.md).\n")
        adr = self.root / "docs" / "adr"
        adr.mkdir(parents=True)
        (adr / "0001-x.md").write_text("# 0001. Use *stars* [x]\n\n**Status:** Accepted, 2026-11-18. Owner said so.\n")
        (adr / "0002-y.md").write_text("---\nstatus: proposed\n---\n# Y\n")
        (self.root / "docs" / "b.md").write_text("---\nstatus: draft\n---\n# B\n```\n[fenced](adr/0001-x.md)\n```\n")

    def map_errors(self):
        return [(p, m) for p, m in levels(self.root, "ERROR") if p == "docs/MAP.md"]

    def test_map_lists_titles_status_backlinks_and_escapes(self):
        text = docs_audit.generate_map(self.root)
        self.assertIn("- [README.md](../README.md): Project", text)
        self.assertIn(r"[docs/adr/0001-x.md](adr/0001-x.md): 0001. Use \*stars\* \[x\] (status: Accepted)", text)
        self.assertIn("  - Linked from: [README.md](../README.md)", text)
        self.assertIn("[docs/adr/0002-y.md](adr/0002-y.md): Y (status: proposed)", text)  # front-matter form
        self.assertIn("- [docs/b.md](b.md): B\n", text)  # status is read for ADRs only
        self.assertEqual(text.count("Linked from"), 1)  # the fenced link does not count
        self.assertNotIn("](MAP.md)", text)  # the map does not list itself

    def test_missing_then_current_then_stale(self):
        self.assertTrue(self.map_errors())  # missing
        docs_audit.write_map(self.root)
        self.assertEqual(self.map_errors(), [])
        (self.root / "docs" / "b.md").write_text("# B renamed\n")
        self.assertTrue(any("stale" in m for _, m in self.map_errors()))

    def test_repo_with_its_own_generator_is_left_alone(self):
        (self.root / "docs" / "MAP.md").write_text("# Knowledge map\nmade by the repo's own tool\n")
        self.assertEqual(self.map_errors(), [])
        self.assertNotIn("docs/MAP.md", docs_audit.init(self.root))
        self.assertIn("own tool", (self.root / "docs" / "MAP.md").read_text())

    def test_init_creates_the_map(self):
        self.assertIn("docs/MAP.md", docs_audit.init(self.root))
        self.assertEqual(self.map_errors(), [])

    def git(self, *a):
        return subprocess.run(["git", "-C", str(self.root), "-c", "user.name=t", "-c", "user.email=t@t", *a],
                              check=True, capture_output=True, text=True).stdout

    def commit_all(self, msg):
        self.git("add", "-A")
        self.git("commit", "-q", "-m", msg)

    def test_stop_hook_regenerates_a_stale_map_without_blocking(self):
        docs_audit.write_map(self.root)
        self.git("init", "-q")
        self.commit_all("base")
        (self.root / "docs" / "b.md").write_text("# B renamed\n")  # a docs-only change: no changelog needed
        hook = Path(docs_audit.__file__).with_name("stop_hook.sh")
        r = subprocess.run([str(hook)], input='{"cwd": "%s", "stop_hook_active": false}' % self.root,
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(self.map_errors(), [])  # current again, with nobody running --map

    def test_init_installs_a_pre_commit_hook_that_keeps_the_map_current(self):
        self.git("init", "-q")
        docs_audit.init(self.root)
        hook = self.root / ".git" / "hooks" / "pre-commit"
        self.assertTrue(hook.is_file() and hook.stat().st_mode & 0o111)
        self.commit_all("base")
        (self.root / "docs" / "b.md").write_text("# B renamed\n")
        self.git("add", "docs/b.md")  # only the doc is staged; the hook adds the map
        self.git("commit", "-q", "-m", "rename b")
        self.assertIn("docs/MAP.md", self.git("show", "--name-only", "--format=", "HEAD").split())
        self.assertIn("B renamed", self.git("show", "HEAD:docs/MAP.md"))
        self.assertEqual(self.git("status", "--porcelain"), "")

    def test_init_leaves_an_existing_pre_commit_hook_alone(self):
        self.git("init", "-q")
        hook = self.root / ".git" / "hooks" / "pre-commit"
        hook.write_text("#!/bin/sh\necho mine\n")
        docs_audit.init(self.root)
        self.assertEqual(hook.read_text(), "#!/bin/sh\necho mine\n")

    def test_map_in_a_git_repo_lists_only_files_git_tracks(self):
        self.git("init", "-q")
        self.commit_all("base")
        (self.root / "scratch-report.md").write_text("# Local report, never committed\n")
        self.assertNotIn("scratch-report.md", docs_audit.generate_map(self.root))
        self.git("add", "scratch-report.md")  # staged files count: the pre-commit hook runs after staging
        self.assertIn("scratch-report.md", docs_audit.generate_map(self.root))

    def test_long_readme_is_flagged(self):
        readme = lambda: [m for p, m in levels(self.root, "WARN") if p == "README.md"]
        self.assertEqual(readme(), [])
        (self.root / "README.md").write_text("# Project\n" + "line\n" * 200)
        self.assertTrue(any("landing page" in m for m in readme()))


class RolloutTest(unittest.TestCase):
    """setup installs the CI check; audit notices a stale copy; the Stop hook finds the repo."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.addCleanup(self.tmp.cleanup)

    def test_init_installs_script_and_workflow(self):
        created = docs_audit.init(self.root)
        self.assertIn("scripts/docs_audit.py", created)
        self.assertIn(".github/workflows/docs-check.yml", created)
        self.assertEqual((self.root / "scripts/docs_audit.py").read_bytes(), Path(docs_audit.__file__).read_bytes())
        self.assertIn("--changed", (self.root / ".github/workflows/docs-check.yml").read_text())

    def test_init_skips_workflow_when_ci_already_runs_the_check(self):
        wf = self.root / ".github/workflows/ci.yml"
        wf.parent.mkdir(parents=True)
        wf.write_text("- run: python3 scripts/docs_audit.py --changed x\n")
        self.assertNotIn(".github/workflows/docs-check.yml", docs_audit.init(self.root))

    def test_audit_warns_when_repo_copy_is_stale(self):
        (self.root / "scripts").mkdir()
        (self.root / "scripts/docs_audit.py").write_text("# old\n")
        self.assertTrue(any(p == "scripts/docs_audit.py" for p, _ in levels(self.root, "WARN")))
        (self.root / "scripts/docs_audit.py").write_bytes(Path(docs_audit.__file__).read_bytes())
        self.assertFalse(any(p == "scripts/docs_audit.py" for p, _ in levels(self.root, "WARN")))

    def test_stop_hook_runs_in_repo_indexed_by_map_md(self):
        git = lambda *a: subprocess.run(["git", "-C", str(self.root), "-c", "user.name=t", "-c", "user.email=t@t", *a],
                                        check=True, capture_output=True)
        git("init", "-q")
        (self.root / "docs").mkdir()
        (self.root / "docs/MAP.md").write_text("# Map\n")
        (self.root / "a.py").write_text("1\n")
        git("add", "-A")
        git("commit", "-q", "-m", "base")
        (self.root / "a.py").write_text("2\n")
        hook = Path(docs_audit.__file__).with_name("stop_hook.sh")
        r = subprocess.run([str(hook)], input='{"cwd": "%s", "stop_hook_active": false}' % self.root,
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 2, r.stderr)
        # with the changelog updated, old structure errors (missing sections here) never block
        (self.root / "CHANGELOG.md").write_text("## [Unreleased]\n- a\n")
        r = subprocess.run([str(hook)], input='{"cwd": "%s", "stop_hook_active": false}' % self.root,
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertTrue([f for f in docs_audit.audit(self.root) if f[0] == "ERROR"])  # they do exist


class ChangedTest(unittest.TestCase):
    """--changed BASE: docs that must move when code moves."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.addCleanup(self.tmp.cleanup)
        self.git("init", "-q")
        self.write("CHANGELOG.md", "## [Unreleased]\n")
        self.write("src/app.py", "x = 1\n")
        self.commit("base")

    def git(self, *args):
        return subprocess.run(["git", "-C", str(self.root), "-c", "user.name=t", "-c", "user.email=t@t",
                               *args], check=True, capture_output=True, text=True).stdout

    def write(self, rel, text):
        p = self.root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)

    def commit(self, msg):
        self.git("add", "-A")
        self.git("commit", "-q", "-m", msg)

    def changed(self, level=None):
        out = docs_audit.changed(self.root, "HEAD")
        return [(p, m) for lv, p, m in out if level is None or lv == level]

    def test_code_change_needs_changelog(self):
        self.write("src/app.py", "x = 2\n")
        self.assertEqual([p for p, _ in self.changed("ERROR")], ["CHANGELOG.md"])
        self.write("CHANGELOG.md", "## [Unreleased]\n- changed x\n")
        self.assertEqual(self.changed("ERROR"), [])

    def test_adr_in_docs_adr_counts(self):
        self.write("CHANGELOG.md", "## [Unreleased]\n- add dep\n")
        self.write("package.json", "{}\n")
        self.write("docs/adr/0011-new-dep.md", "status: accepted\n")
        self.assertEqual(self.changed("ERROR"), [])

    def test_docs_only_change_needs_nothing(self):
        self.write("docs/how-to/x.md", "# X\n")  # untracked files count as changed
        self.assertEqual(self.changed(), [])

    def test_manifest_change_needs_new_adr(self):
        self.write("CHANGELOG.md", "## [Unreleased]\n- add dep\n")
        self.write("requirements.txt", "requests==2.32.3\n")
        self.assertIn("docs/decisions/", [p for p, _ in self.changed("ERROR")])
        self.write("docs/decisions/README.md", "index\n")  # the index alone is not an ADR
        self.assertIn("docs/decisions/", [p for p, _ in self.changed("ERROR")])
        self.write("docs/decisions/0002-requests.md", "status: accepted\n")
        self.assertEqual(self.changed("ERROR"), [])

    def test_sensitive_path_warns_about_threat_model(self):
        self.write("CHANGELOG.md", "## [Unreleased]\n- login\n")
        self.write("src/auth/login.py", "pass\n")
        self.assertIn("docs/security/threat-model.md", [p for p, _ in self.changed("WARN")])

    def test_escape_hatch_in_commit_message_downgrades_errors(self):
        self.write("src/app.py", "x = 3\n")
        self.commit("fix: typo\n\nDocs: none needed - comment typo only")
        out = docs_audit.changed(self.root, "HEAD~1")
        self.assertFalse([f for f in out if f[0] == "ERROR"])
        self.assertTrue(any("none needed" in m for lv, _, m in out if lv == "INFO"))

    def test_bad_base_is_an_error_not_a_pass(self):
        with self.assertRaises(ValueError):
            docs_audit.changed(self.root, "no-such-ref")


if __name__ == "__main__":
    unittest.main()
