#!/usr/bin/env python3
"""Read and validate the package manifest without third-party dependencies."""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


TOOLS = frozenset({"codex", "claude", "copilot"})
EXPECTED_GENERIC_AGENTS = {"codex": "default", "claude": "general-purpose", "copilot": "general-purpose"}
EXPECTED_ENTRIES = {"codex": "$orchestrator-work-protocol", "claude": "/orchestrator-work-protocol", "copilot": "orchestrator-work-protocol"}
STATUSES = frozenset({"experimental", "supported"})
SMOKE_STATUSES = frozenset({"not-run", "passed", "failed"})
WINDOWS_RESERVED_DEVICE_STEMS = frozenset(
    {"con", "prn", "aux", "nul"}
    | {f"com{number}" for number in range(1, 10)}
    | {f"lpt{number}" for number in range(1, 10)}
    | {f"com{number}" for number in "¹²³"}
    | {f"lpt{number}" for number in "¹²³"}
)


class ManifestError(ValueError):
    """The manifest does not satisfy the package metadata contract."""


def load_manifest(path: Path) -> dict[str, Any]:
    """Load *path* and return validated manifest data."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ManifestError(f"cannot read manifest {path}: {exc}") from exc
    validate_manifest(data)
    return data


def validate_manifest(data: Any) -> None:
    """Validate the versioned adapter metadata used by installer and verifier."""
    if not isinstance(data, dict):
        raise ManifestError("manifest must be an object")
    if data.get("schema_version") != 2:
        raise ManifestError("schema_version must be 2")
    _require_string(data.get("version"), "manifest missing version")
    if data.get("default_tools") != ["codex"]:
        raise ManifestError("default_tools must contain exactly codex")
    if data.get("public_entries") != ["orchestrator-work-protocol", "openspec-orchestrated-apply"]:
        raise ManifestError("public_entries must preserve the two logical skill names")
    adapters = data.get("adapters")
    if not isinstance(adapters, dict) or set(adapters) != TOOLS:
        raise ManifestError("adapters must contain exactly codex, claude, and copilot")

    owned_resources: list[tuple[str, str]] = []
    canonical_resources = _validate_resources(
        data.get("canonical_resources"), "canonical_resources"
    )
    _claim_resources(owned_resources, canonical_resources, "canonical_resources")
    for tool in sorted(TOOLS):
        adapter = adapters[tool]
        if not isinstance(adapter, dict):
            raise ManifestError(f"adapter {tool} must be an object")
        status = adapter.get("status")
        if not isinstance(status, str) or status not in STATUSES:
            raise ManifestError(f"adapter {tool} has unsupported status {status!r}")
        if adapter.get("generic_agent") != EXPECTED_GENERIC_AGENTS[tool]:
            raise ManifestError(f"adapter {tool} has invalid generic_agent mapping")
        if adapter.get("explicit_entry") != EXPECTED_ENTRIES[tool]:
            raise ManifestError(f"adapter {tool} has invalid explicit_entry")
        scopes = adapter.get("scopes")
        if (
            not isinstance(scopes, list)
            or not scopes
            or not all(isinstance(scope, str) for scope in scopes)
            or not set(scopes) <= {"user", "project"}
        ):
            raise ManifestError(f"adapter {tool} has invalid scopes")
        resources = _validate_resources(adapter.get("resources"), f"adapter {tool}")
        _claim_resources(owned_resources, resources, f"adapter {tool}")
        native_resources = _validate_native_hardening(tool, adapter.get("native_hardening"))
        _claim_resources(owned_resources, native_resources, f"adapter {tool} native_hardening")
        _validate_verification(tool, status, adapter.get("verification"))

    legacy = data.get("legacy_codex_profiles")
    if not isinstance(legacy, dict) or legacy.get("ownership") != "preserve-on-upgrade":
        raise ManifestError("legacy_codex_profiles must preserve ownership on upgrade")
    _validate_legacy_profiles(legacy.get("resources"))


def _validate_native_hardening(tool: str, value: Any) -> list[str]:
    if not isinstance(value, dict) or not isinstance(value.get("available"), bool):
        raise ManifestError(f"adapter {tool} has invalid native_hardening metadata")
    resources = _validate_resources(value.get("resources"), f"adapter {tool} native_hardening", allow_empty=True)
    if value["available"] != bool(resources):
        raise ManifestError(f"adapter {tool} native_hardening availability disagrees with resources")
    return resources


def _validate_resources(value: Any, owner: str, *, allow_empty: bool = False) -> list[str]:
    if not isinstance(value, list) or (not allow_empty and not value):
        raise ManifestError(f"{owner} has invalid resources")
    normalized = [_normalize_resource_path(item, owner) for item in value]
    if len(set(normalized)) != len(normalized):
        raise ManifestError(f"{owner} has duplicate owned resources")
    _claim_resources([], normalized, owner)
    return normalized


def _normalize_resource_path(value: Any, owner: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ManifestError(f"{owner} has invalid resources")
    candidate = value.replace("\\", "/")
    if candidate.startswith("/") or candidate.startswith("//"):
        raise ManifestError(f"{owner} resource must be a relative path: {value!r}")
    parts: list[str] = []
    for part in candidate.split("/"):
        if not part or part == ".":
            continue
        if part == "..":
            raise ManifestError(f"{owner} resource must not contain '..': {value!r}")
        if _is_invalid_resource_component(part):
            raise ManifestError(f"{owner} resource has invalid path component: {value!r}")
        parts.append(part)
    if not parts:
        raise ManifestError(f"{owner} resource must be a relative path: {value!r}")
    return "/".join(parts).casefold()


def _is_invalid_resource_component(part: str) -> bool:
    """Return whether *part* is not portable as a package resource component."""
    return (
        any(character in '<>:"|?*' or ord(character) < 32 for character in part)
        or part.endswith((".", " "))
    )


def _validate_legacy_profiles(value: Any) -> None:
    if not isinstance(value, list) or not value:
        raise ManifestError("legacy_codex_profiles resources must list unique safe TOML basenames")
    profiles: list[str] = []
    for profile in value:
        if not _is_safe_legacy_profile_basename(profile):
            raise ManifestError("legacy_codex_profiles resources must list unique safe TOML basenames")
        profiles.append(profile.casefold())
    if len(set(profiles)) != len(profiles):
        raise ManifestError("legacy_codex_profiles resources must be unique case-insensitively")


def _is_safe_legacy_profile_basename(value: Any) -> bool:
    """Return whether *value* is a portable non-device TOML basename."""
    if (
        not isinstance(value, str)
        or not value
        or value != value.strip()
        or not value.endswith(".toml")
        or value == ".toml"
        or any(character in '<>:"/\\|?*' or ord(character) < 32 for character in value)
    ):
        return False
    comparison_stem = value.split(".", 1)[0].rstrip(" .").casefold()
    return comparison_stem not in WINDOWS_RESERVED_DEVICE_STEMS


def _claim_resources(owned_resources: list[tuple[str, str]], resources: list[str], owner: str) -> None:
    for resource in resources:
        for existing, existing_owner in owned_resources:
            if _paths_overlap(existing, resource):
                raise ManifestError(
                    "resource ownership overlaps owned resources: "
                    f"{existing_owner} {existing!r} and {owner} {resource!r}"
                )
        owned_resources.append((resource, owner))


def _paths_overlap(first: str, second: str) -> bool:
    return first == second or first.startswith(second + "/") or second.startswith(first + "/")


def _validate_verification(tool: str, status: str, value: Any) -> None:
    if not isinstance(value, dict):
        raise ManifestError(f"adapter {tool} has malformed verification metadata")
    urls = value.get("source_urls")
    if not isinstance(urls, list) or not urls or not all(_is_url(item) for item in urls):
        raise ManifestError(f"adapter {tool} verification source_urls must contain absolute URLs")
    _validate_date(value.get("verified_date"), f"adapter {tool} verification verified_date")
    _require_string(value.get("evidence_gap"), f"adapter {tool} verification missing evidence_gap")
    smoke = value.get("fresh_process_smoke")
    if not isinstance(smoke, str) or smoke not in SMOKE_STATUSES:
        raise ManifestError(f"adapter {tool} has invalid fresh_process_smoke status")
    version = value.get("cli_version")
    if version is not None and (not isinstance(version, str) or not version.strip()):
        raise ManifestError(f"adapter {tool} has invalid cli_version")
    if smoke == "passed" and not version:
        raise ManifestError(f"adapter {tool} passed fresh_process_smoke requires cli_version")
    if status == "supported" and (smoke != "passed" or not version):
        raise ManifestError(f"adapter {tool} cannot be supported without passed smoke evidence and cli_version")


def _validate_date(value: Any, label: str) -> None:
    if not isinstance(value, str):
        raise ManifestError(f"{label} must be an ISO date")
    try:
        dt.date.fromisoformat(value)
    except ValueError as exc:
        raise ManifestError(f"{label} must be an ISO date") from exc


def _is_url(value: Any) -> bool:
    return isinstance(value, str) and urlparse(value).scheme == "https" and bool(urlparse(value).netloc)


def _require_string(value: Any, message: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ManifestError(message)
