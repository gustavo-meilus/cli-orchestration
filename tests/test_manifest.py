from __future__ import annotations

import copy
import unittest

from scripts.manifest import ManifestError, load_manifest, validate_manifest
from tests.helpers import REPOSITORY_ROOT


class ManifestContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.manifest = load_manifest(REPOSITORY_ROOT / "manifest.json")

    def test_repository_manifest_is_valid(self) -> None:
        self.assertEqual(self.manifest["schema_version"], 2)

    def test_rejects_supported_adapter_without_smoke_evidence(self) -> None:
        candidate = copy.deepcopy(self.manifest)
        candidate["adapters"]["claude"]["status"] = "supported"
        with self.assertRaisesRegex(ManifestError, "cannot be supported"):
            validate_manifest(candidate)

    def test_accepts_supported_adapter_with_complete_smoke_evidence(self) -> None:
        candidate = copy.deepcopy(self.manifest)
        candidate["adapters"]["codex"]["status"] = "supported"
        verification = candidate["adapters"]["codex"]["verification"]
        verification["fresh_process_smoke"] = "passed"
        verification["cli_version"] = "1.2.3"
        validate_manifest(candidate)

    def test_rejects_malformed_status_types(self) -> None:
        for status in ([], {}, 0):
            with self.subTest(status=status):
                candidate = copy.deepcopy(self.manifest)
                candidate["adapters"]["codex"]["status"] = status
                with self.assertRaisesRegex(ManifestError, "unsupported status"):
                    validate_manifest(candidate)

    def test_rejects_malformed_scope_containers_and_entries(self) -> None:
        invalid_scopes = [
            "user",
            ("user",),
            {"user"},
            {"user": True},
            ["user", []],
            ["project", {}],
        ]
        for scopes in invalid_scopes:
            with self.subTest(scopes=scopes):
                candidate = copy.deepcopy(self.manifest)
                candidate["adapters"]["codex"]["scopes"] = scopes
                with self.assertRaisesRegex(ManifestError, "invalid scopes"):
                    validate_manifest(candidate)

    def test_rejects_missing_generic_agent_mapping(self) -> None:
        candidate = copy.deepcopy(self.manifest)
        candidate["adapters"]["copilot"].pop("generic_agent")
        with self.assertRaisesRegex(ManifestError, "generic_agent"):
            validate_manifest(candidate)

    def test_rejects_wrong_explicit_entry(self) -> None:
        candidate = copy.deepcopy(self.manifest)
        candidate["adapters"]["claude"]["explicit_entry"] = "$orchestrator-work-protocol"
        with self.assertRaisesRegex(ManifestError, "invalid explicit_entry"):
            validate_manifest(candidate)

    def test_rejects_overlapping_adapter_resources(self) -> None:
        candidate = copy.deepcopy(self.manifest)
        candidate["adapters"]["copilot"]["resources"].append(
            candidate["adapters"]["codex"]["resources"][0]
        )
        with self.assertRaisesRegex(ManifestError, "overlaps owned resources"):
            validate_manifest(candidate)

    def test_rejects_missing_or_malformed_canonical_resources(self) -> None:
        invalid_resources = [None, "templates/skills", (), {"templates/skills"}, {"path": True}, []]
        for resources in invalid_resources:
            with self.subTest(resources=resources):
                candidate = copy.deepcopy(self.manifest)
                candidate["canonical_resources"] = resources
                with self.assertRaisesRegex(ManifestError, "canonical_resources has invalid resources"):
                    validate_manifest(candidate)

        candidate = copy.deepcopy(self.manifest)
        candidate["canonical_resources"] = ["templates/skills", 1]
        with self.assertRaisesRegex(ManifestError, "canonical_resources has invalid resources"):
            validate_manifest(candidate)

    def test_rejects_normalized_or_casefolded_duplicate_canonical_resources(self) -> None:
        for duplicate in (
            ".\\templates\\skills\\orchestrator-work-protocol",
            "TEMPLATES/SKILLS/ORCHESTRATOR-WORK-PROTOCOL",
        ):
            with self.subTest(duplicate=duplicate):
                candidate = copy.deepcopy(self.manifest)
                candidate["canonical_resources"].append(duplicate)
                with self.assertRaisesRegex(ManifestError, "canonical_resources has duplicate owned resources"):
                    validate_manifest(candidate)

    def test_rejects_canonical_internal_ancestor_overlap(self) -> None:
        candidate = copy.deepcopy(self.manifest)
        candidate["canonical_resources"].append("templates/skills")
        with self.assertRaisesRegex(ManifestError, "overlaps owned resources"):
            validate_manifest(candidate)

    def test_rejects_canonical_adapter_exact_and_ancestor_collisions_in_both_directions(self) -> None:
        candidate = copy.deepcopy(self.manifest)
        candidate["canonical_resources"].append("templates/adapters/codex.md")
        with self.assertRaisesRegex(ManifestError, "overlaps owned resources"):
            validate_manifest(candidate)

        candidate = copy.deepcopy(self.manifest)
        candidate["adapters"]["codex"]["resources"].append(
            "templates/skills/orchestrator-work-protocol/child"
        )
        with self.assertRaisesRegex(ManifestError, "overlaps owned resources"):
            validate_manifest(candidate)

    def test_rejects_canonical_native_hardening_ancestor_collisions_in_both_directions(self) -> None:
        candidate = copy.deepcopy(self.manifest)
        candidate["canonical_resources"].append("templates/codex")
        with self.assertRaisesRegex(ManifestError, "overlaps owned resources"):
            validate_manifest(candidate)

        candidate = copy.deepcopy(self.manifest)
        candidate["adapters"]["codex"]["native_hardening"]["resources"] = [
            "templates/skills/orchestrator-work-protocol/child"
        ]
        with self.assertRaisesRegex(ManifestError, "overlaps owned resources"):
            validate_manifest(candidate)

    def test_rejects_normalized_duplicate_resource_paths(self) -> None:
        candidate = copy.deepcopy(self.manifest)
        candidate["adapters"]["codex"]["resources"].append(
            ".\\templates\\adapters\\codex.md"
        )
        with self.assertRaisesRegex(ManifestError, "duplicate owned resources"):
            validate_manifest(candidate)

    def test_rejects_casefolded_duplicate_resource_paths(self) -> None:
        candidate = copy.deepcopy(self.manifest)
        candidate["adapters"]["codex"]["resources"].append(
            "TEMPLATES/ADAPTERS/CODEX.MD"
        )
        with self.assertRaisesRegex(ManifestError, "duplicate owned resources"):
            validate_manifest(candidate)

    def test_rejects_casefolded_duplicate_native_hardening_paths(self) -> None:
        candidate = copy.deepcopy(self.manifest)
        candidate["adapters"]["codex"]["native_hardening"]["resources"].append(
            "TEMPLATES/CODEX/AGENTS"
        )
        with self.assertRaisesRegex(ManifestError, "duplicate owned resources"):
            validate_manifest(candidate)

    def test_rejects_adapter_and_native_hardening_ancestor_overlap(self) -> None:
        candidate = copy.deepcopy(self.manifest)
        candidate["adapters"]["claude"]["native_hardening"] = {
            "available": True,
            "resources": ["templates/adapters"],
        }
        with self.assertRaisesRegex(ManifestError, "overlaps owned resources"):
            validate_manifest(candidate)

    def test_rejects_within_adapter_ancestor_resource_overlap(self) -> None:
        candidate = copy.deepcopy(self.manifest)
        candidate["adapters"]["codex"]["resources"].append("templates/adapters")
        with self.assertRaisesRegex(ManifestError, "overlaps owned resources"):
            validate_manifest(candidate)

    def test_rejects_cross_adapter_native_hardening_overlap(self) -> None:
        candidate = copy.deepcopy(self.manifest)
        candidate["adapters"]["claude"]["native_hardening"] = {
            "available": True,
            "resources": ["templates/codex/agents/profile.toml"],
        }
        with self.assertRaisesRegex(ManifestError, "overlaps owned resources"):
            validate_manifest(candidate)

    def test_rejects_cross_adapter_native_hardening_descendant_overlap(self) -> None:
        candidate = copy.deepcopy(self.manifest)
        candidate["adapters"]["copilot"]["native_hardening"] = {
            "available": True,
            "resources": ["TEMPLATES/ADAPTERS/CLAUDE.MD/profiles"],
        }
        with self.assertRaisesRegex(ManifestError, "overlaps owned resources"):
            validate_manifest(candidate)

    def test_rejects_parent_directory_resource_path(self) -> None:
        candidate = copy.deepcopy(self.manifest)
        candidate["adapters"]["codex"]["resources"] = ["../outside"]
        with self.assertRaisesRegex(ManifestError, "must not contain"):
            validate_manifest(candidate)

    def test_rejects_malformed_resource_components_across_ownership_boundaries(self) -> None:
        resource_locations = {
            "canonical": lambda candidate, path: candidate["canonical_resources"].append(path),
            "adapter": lambda candidate, path: candidate["adapters"]["codex"]["resources"].append(path),
            "native hardening": lambda candidate, path: candidate["adapters"]["codex"][
                "native_hardening"
            ]["resources"].append(path),
        }
        malformed_paths = (
            "C:templates\\adapters\\codex.md",
            "C:\\templates\\adapters\\codex.md",
            "templates/adapters/codex?.md",
            "templates/adapters/codex.md.",
        )
        for location, add_resource in resource_locations.items():
            for path in malformed_paths:
                with self.subTest(location=location, path=path):
                    candidate = copy.deepcopy(self.manifest)
                    add_resource(candidate, path)
                    with self.assertRaisesRegex(ManifestError, "invalid path component"):
                        validate_manifest(candidate)

    def test_rejects_drive_relative_canonical_alias_before_adapter_collision_check(self) -> None:
        candidate = copy.deepcopy(self.manifest)
        candidate["canonical_resources"].append("C:templates\\adapters\\codex.md")
        with self.assertRaisesRegex(ManifestError, "invalid path component"):
            validate_manifest(candidate)

    def test_rejects_malformed_verification_metadata(self) -> None:
        candidate = copy.deepcopy(self.manifest)
        candidate["adapters"]["codex"]["verification"]["verified_date"] = "yesterday"
        with self.assertRaisesRegex(ManifestError, "ISO date"):
            validate_manifest(candidate)

    def test_rejects_passed_smoke_without_cli_version(self) -> None:
        candidate = copy.deepcopy(self.manifest)
        candidate["adapters"]["codex"]["verification"]["fresh_process_smoke"] = "passed"
        candidate["adapters"]["codex"]["verification"]["cli_version"] = None
        with self.assertRaisesRegex(ManifestError, "requires cli_version"):
            validate_manifest(candidate)

    def test_accepts_cli_version_with_failed_smoke_for_reproducible_evidence(self) -> None:
        candidate = copy.deepcopy(self.manifest)
        candidate["adapters"]["codex"]["verification"]["cli_version"] = "1.2.3"
        candidate["adapters"]["codex"]["verification"]["fresh_process_smoke"] = "failed"
        validate_manifest(candidate)

    def test_rejects_malformed_fresh_process_smoke_types(self) -> None:
        for smoke in ([], {}, 0):
            with self.subTest(smoke=smoke):
                candidate = copy.deepcopy(self.manifest)
                candidate["adapters"]["codex"]["verification"]["fresh_process_smoke"] = smoke
                with self.assertRaisesRegex(ManifestError, "invalid fresh_process_smoke"):
                    validate_manifest(candidate)

    def test_accepts_complete_fresh_process_evidence(self) -> None:
        candidate = copy.deepcopy(self.manifest)
        verification = candidate["adapters"]["codex"]["verification"]
        verification["fresh_process_smoke"] = "passed"
        verification["cli_version"] = "1.2.3"
        validate_manifest(candidate)

    def test_rejects_unsafe_or_duplicate_legacy_profile_basenames(self) -> None:
        invalid_profiles = [
            "",
            "   ",
            ".toml",
            "nested/profile.toml",
            "nested\\profile.toml",
            "../profile.toml",
            "/profile.toml",
            "\\\\server\\share\\profile.toml",
            "C:profile.toml",
            "profile:copy.toml",
            'profile<copy.toml',
            'profile>copy.toml',
            'profile"copy.toml',
            "profile|copy.toml",
            "profile?copy.toml",
            "profile*copy.toml",
            "profile\x00copy.toml",
            "profile\x1fcopy.toml",
            "CON.toml",
            "prn.toml",
            "Aux.toml",
            "nul.toml",
            "COM1.toml",
            "com9.extra.toml",
            "LPT1.toml",
            "lpt9.extra.toml",
            "cOm¹.ToMl",
            "COM².extra.toml",
            "com³.extra.ToMl",
            "lPt¹.ToMl",
            "LPT².extra.toml",
            "lpt³.extra.ToMl",
            "CON .toml",
            "prn..toml",
            "Aux ...extra.toml",
            "nul...toml",
            "cOm1 .ToMl",
            "COM9...extra.toml",
            "lPt1 .ToMl",
            "LPT9...extra.toml",
            "cOm¹ .ToMl",
            "COM²...extra.toml",
            "lPt¹ .ToMl",
            "LPT³...extra.toml",
        ]
        for profile in invalid_profiles:
            with self.subTest(profile=profile):
                candidate = copy.deepcopy(self.manifest)
                candidate["legacy_codex_profiles"]["resources"][0] = profile
                with self.assertRaisesRegex(ManifestError, "safe TOML basenames"):
                    validate_manifest(candidate)

        candidate = copy.deepcopy(self.manifest)
        candidate["legacy_codex_profiles"]["resources"][1] = "INSPECTOR.toml"
        with self.assertRaisesRegex(ManifestError, "unique case-insensitively"):
            validate_manifest(candidate)

    def test_accepts_portable_non_device_legacy_profile_basenames(self) -> None:
        candidate = copy.deepcopy(self.manifest)
        candidate["legacy_codex_profiles"]["resources"] = [
            *self.manifest["legacy_codex_profiles"]["resources"],
            "profile.toml",
            "profile.extra.toml",
            "COM10.toml",
            "LPT10.extra.toml",
            "auxiliary.toml",
        ]
        validate_manifest(candidate)
