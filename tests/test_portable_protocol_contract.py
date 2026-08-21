"""Cross-document contracts for the release 2.0 portable protocol."""

from __future__ import annotations

import json
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
CURRENT_DOCS = [
    ROOT / "README.md", ROOT / "USAGE.md", ROOT / "INSTALL.md",
    *sorted((ROOT / "docs").glob("*.md")),
    *sorted((ROOT / "templates/project").glob("*.md")),
]


class PortableProtocolContractTests(unittest.TestCase):
    def test_shipped_current_docs_do_not_claim_the_legacy_pipeline_is_default(self) -> None:
        forbidden = ("inspect -> plan -> execute", "aggregate COMPLETE` = Validator", "full six-role workflow")
        for path in CURRENT_DOCS:
            text = path.read_text(encoding="utf-8")
            for phrase in forbidden:
                self.assertNotIn(phrase, text, path)

    def test_core_docs_name_direct_and_orchestrated_modes(self) -> None:
        for relative in ("README.md", "USAGE.md", "docs/WORKFLOW.md", "docs/ARCHITECTURE.md", "templates/project/AGENTS.block.md"):
            text = (ROOT / relative).read_text(encoding="utf-8").lower()
            self.assertIn("direct", text, relative)
            self.assertIn("orchestration", text, relative)

    def test_framework_and_openspec_docs_preserve_ownership_boundary(self) -> None:
        for relative in ("README.md", "docs/GOVERNANCE.md", "docs/OPENSPEC-INTEGRATION.md", "templates/skills/openspec-orchestrated-apply/references/workflow.md"):
            text = (ROOT / relative).read_text(encoding="utf-8")
            self.assertIn("OpenSpec", text)
            self.assertTrue("canonical" in text.lower() or "owns" in text.lower())

    def test_manifest_support_matrix_matches_readme(self) -> None:
        manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        for tool, adapter in manifest["adapters"].items():
            self.assertIn(f"`{adapter['status']}`", readme, tool)
            self.assertIn(f"`{adapter['generic_agent']}`", readme, tool)
        self.assertNotIn("`unsupported`", readme)

    def test_all_local_markdown_links_resolve(self) -> None:
        failures = []
        for path in [item for item in ROOT.rglob("*.md") if "archive" not in item.parts and "graphify-out" not in item.parts]:
            for target in re.findall(r"(?<!!)\[[^]]+\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
                target = target.split("#", 1)[0]
                if target and "://" not in target and not (path.parent / target).resolve().exists():
                    failures.append(f"{path.relative_to(ROOT)} -> {target}")
        self.assertEqual(failures, [])

    def test_canonical_openspec_paths_are_not_package_resources(self) -> None:
        manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
        owned = json.dumps({"canonical": manifest["canonical_resources"], "adapters": manifest["adapters"]})
        self.assertNotIn(".agents/skills/openspec-", owned)
        self.assertFalse(any((ROOT / "templates").rglob("openspec-apply-change")))
        self.assertFalse(any((ROOT / "templates").rglob("openspec-verify-change")))


if __name__ == "__main__":
    unittest.main()
