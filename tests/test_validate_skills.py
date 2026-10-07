import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "validate_skills", ROOT / "scripts" / "validate_skills.py"
)
validate_skills = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validate_skills)


class ValidationHarnessTests(unittest.TestCase):
    def test_case_prompt_excludes_expected_behavior_and_scoring_criteria(self):
        cases = validate_skills.load_cases(ROOT)

        self.assertEqual([case["id"] for case in cases], ["E1", "E2", "R1", "X1", "L1", "C1"])
        for case in cases:
            for stage in case["stages"]:
                self.assertNotIn("Required behavior", stage["prompt"])
                self.assertNotIn("Scoring criteria", stage["prompt"])
            self.assertTrue(case["criteria"], case["id"])

    def test_latex_prompt_contains_fixture_bodies_without_rubric(self):
        cases = validate_skills.load_cases(ROOT)
        latex = next(case for case in cases if case["id"] == "L1")

        self.assertEqual(len(latex["stages"]), 2)
        self.assertIn(r"ref{sec:missing}", latex["stages"][0]["prompt"])
        self.assertIn("fragment-unresolved-reference.tex", latex["stages"][1]["prompt"])
        self.assertTrue(any("complete-unresolved-reference.tex" in path for path in latex["stages"][0]["artifacts"]))
        self.assertTrue(all("""NOT EVALUATED""" not in c for c in latex["criteria"]))

    def test_combined_cases_include_all_target_skills(self):
        cases = validate_skills.load_cases(ROOT)
        by_id = {case["id"]: case for case in cases}

        self.assertEqual(by_id["X1"]["skills"], ["experiment-designer", "result-analyzer"])
        self.assertEqual(by_id["C1"]["skills"], ["citation-verifier", "result-analyzer"])
        for case_id in ("X1", "C1"):
            prompt = by_id[case_id]["stages"][0]["prompt"]
            self.assertIn("skills/result-analyzer/SKILL.md", prompt)

    def test_score_record_requires_every_criterion_and_evidence(self):
        case = validate_skills.load_cases(ROOT)[0]
        incomplete = {"scores": []}

        with self.assertRaises(ValueError):
            validate_skills.validate_score_record(case, incomplete)

        complete = {
            "scores": [
                {"criterion": criterion["id"], "status": "PASS", "evidence": "quoted output"}
                for criterion in case["criteria"]
            ]
        }
        validate_skills.validate_score_record(case, complete)


if __name__ == "__main__":
    unittest.main()
