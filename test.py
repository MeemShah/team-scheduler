import unittest
from datetime import date
from config import INITIAL_DATE, TEAM_PAIRS 
from main import get_todays_working_pair

class TestGetTodaysWorkingPair(unittest.TestCase):
    def setUp(self):
        self.team_pairs = TEAM_PAIRS
        self.initial_date = INITIAL_DATE

    def test_get_todays_working_pair(self):
        test_cases = [
            {
                "test_name": "Same Date",
                "mock_input": (date(2025, 4, 28), date(2025, 4, 28)),
                "expected_output": (self.team_pairs[0], 1)
            },
            {
                "test_name": "Friday to Monday",
                "mock_input": (date(2025, 4, 25), date(2025, 4, 28)),
                "expected_output": (self.team_pairs[1], 2)
            },
            {
                "test_name": "Thursday to Monday",
                "mock_input": (date(2025, 4, 24), date(2025, 4, 28)),
                "expected_output": (self.team_pairs[1], 2)
            },
            {
                "test_name": "Full Month Comparison",
                "mock_input": (date(2025, 4, 1), date(2025, 4, 28)),
                "expected_output": (self.team_pairs[3], 16)
            },
            {
                "test_name": "Initial Date Is Bigger Than Todays Date",
                "mock_input": (date(2025, 5, 1), date(2025, 4, 28)),
                "expected_output": (None, -1)
            },
            {
                "test_name": "Happy Weekend (Friday)",
                "mock_input": (date(2025, 4, 28), date(2025, 5, 2)),
                "expected_output": (None, -1)
            },
        ]
        
        for case in test_cases:
            with self.subTest(case=case["test_name"]):
                mock_input = case["mock_input"]
                expected_output = case["expected_output"]

                result_team_pair, result_working_days_count = get_todays_working_pair(mock_input[0], mock_input[1])

                if result_team_pair == expected_output[0] and result_working_days_count == expected_output[1]:
                    print(f"{case['test_name']} - OK")
                else:
                    mismatched_fields = []
                    if result_team_pair != expected_output[0]:
                        mismatched_fields.append("team_pair")
                    if result_working_days_count != expected_output[1]:
                        mismatched_fields.append("working_days_count")
                    print(f"{case['test_name']} - FAILED - Mismatched fields: {', '.join(mismatched_fields)}")

if __name__ == '__main__':
    unittest.main()
