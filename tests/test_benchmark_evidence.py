"""Contracts for the recorded matched A/B/C field evidence."""

from __future__ import annotations

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "benchmarks/results/codex-0.148.0-2026-08-20.json"


class BenchmarkEvidenceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.data = json.loads(RESULT.read_text(encoding="utf-8"))

    def test_three_matched_routes_and_required_metrics_are_recorded(self) -> None:
        routes = self.data["routes"]
        self.assertEqual([item["route"] for item in routes], ["A_DIRECT", "B_IMPLEMENTER_VERIFIER", "C_SCOUT_IMPLEMENTER_VERIFIER"])
        required = {
            "status", "correctness_test_passed", "elapsed_seconds", "turns", "tool_calls",
            "observable_test_runs", "observable_repeated_file_reads", "rework_cycles",
            "changed_files", "diff_churn_file_count", "user_interventions",
            "verifier_caught_defects", "telemetry", "final_message_or_blocker",
        }
        for route in routes:
            self.assertTrue(required <= route.keys(), route["route"])
            self.assertEqual(set(route["telemetry"]), {"input_tokens", "output_tokens", "cached_input_tokens", "cost"})

    def test_field_outcomes_are_honest_and_fail_closed(self) -> None:
        direct, implementer_verifier, scout_route = self.data["routes"]
        self.assertEqual(direct["status"], "COMPLETED")
        self.assertTrue(direct["correctness_test_passed"])
        self.assertEqual(direct["changed_files"], ["calculator.py"])
        for route, missing_role in ((implementer_verifier, "Implementer"), (scout_route, "Scout")):
            self.assertEqual(route["status"], "BLOCKED")
            self.assertFalse(route["correctness_test_passed"])
            self.assertEqual(route["changed_files"], [])
            self.assertIn(missing_role, route["final_message_or_blocker"])
            self.assertIn("collab spawn failed", route["final_message_or_blocker"])

    def test_benchmark_harness_uses_its_running_python(self) -> None:
        source = (ROOT / "scripts/run_route_benchmarks.py").read_text(encoding="utf-8")
        self.assertIn("python = sys.executable", source)


if __name__ == "__main__":
    unittest.main()
