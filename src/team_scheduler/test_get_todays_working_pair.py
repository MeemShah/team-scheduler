import unittest
from datetime import date
from ..dto.config import INITIAL_DATE, TEAM_PAIRS, PAIR_SEQUENCE
from ..exceptions import WeekendError, InitialDateAfterTodayError
from ..team_scheduler.service import TeamScheduler

class TestGetTodaysWorkingPair(unittest.TestCase):
    def setUp(self):
        self.team_scheduler = TeamScheduler()
        self.team_pairs = TEAM_PAIRS
        self.initial_date = INITIAL_DATE

    def test_get_todays_working_pair(self):
        test_cases = [
            {
                "test_name": "Same Date",
                "mock_input": (date(2025, 4, 28), date(2025, 4, 28), TEAM_PAIRS, PAIR_SEQUENCE),
                "expected_output": (self.team_pairs[0], 1),
                "expect_exception": None,
            },
            {
                "test_name": "Friday to Monday",
                "mock_input": (date(2025, 4, 25), date(2025, 4, 28), TEAM_PAIRS, PAIR_SEQUENCE),
                "expected_output": (self.team_pairs[1], 2),
                "expect_exception": None,
            },
            {
                "test_name": "Thursday to Monday",
                "mock_input": (date(2025, 4, 24), date(2025, 4, 28), TEAM_PAIRS, PAIR_SEQUENCE),
                "expected_output": (self.team_pairs[1], 2),
                "expect_exception": None,
            },
            {
                "test_name": "Full Month Comparison",
                "mock_input": (date(2025, 4, 1), date(2025, 4, 28), TEAM_PAIRS, PAIR_SEQUENCE),
                "expected_output": (self.team_pairs[3], 16),
                "expect_exception": None,
            },
            {
                "test_name": "Initial Date Is Bigger Than Todays Date",
                "mock_input": (date(2025, 5, 1), date(2025, 4, 28), TEAM_PAIRS, PAIR_SEQUENCE),
                "expected_output": None,
                "expect_exception": InitialDateAfterTodayError,
            },
            {
                "test_name": "Happy Weekend (Friday)",
                "mock_input": (date(2025, 4, 28), date(2025, 5, 2), TEAM_PAIRS, PAIR_SEQUENCE),
                "expected_output": None,
                "expect_exception": WeekendError,
            },
        ]

        for case in test_cases:
            with self.subTest(case=case["test_name"]):
                mock_input = case["mock_input"]
                expected_output = case["expected_output"]
                expect_exception = case["expect_exception"]

                if expect_exception:
                    with self.assertRaises(expect_exception):
                        self.team_scheduler.get_todays_working_pair(*mock_input)
                    print(f"{case['test_name']} - OK (Exception Raised)")
                else:
                    result = self.team_scheduler.get_todays_working_pair(*mock_input)
                    result_team_pair, result_working_days_count = result

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
