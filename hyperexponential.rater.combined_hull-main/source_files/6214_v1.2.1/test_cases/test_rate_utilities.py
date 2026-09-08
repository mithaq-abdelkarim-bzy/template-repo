import unittest
import sys
import os
from datetime import date

# Add the parent directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from algorithms.rate_utilities import year_diff


class TestYearDiff(unittest.TestCase):
    def test_normal_case(self):
        start_date = date(2020, 1, 1)
        end_date = date(2021, 1, 1)
        self.assertAlmostEqual(
            year_diff(start_date, end_date, False), 1.00137, places=5
        )

    def test_leap_year(self):
        start_date = date(2020, 2, 29)
        end_date = date(2021, 2, 28)
        self.assertAlmostEqual(
            year_diff(start_date, end_date, False), 0.99863, places=5
        )

    def test_for_term_true(self):
        start_date = date(2020, 1, 1)
        end_date = date(2021, 1, 1)
        self.assertAlmostEqual(year_diff(start_date, end_date, True), 1.00410, places=5)

    def test_start_date_after_end_date(self):
        start_date = date(2021, 1, 1)
        end_date = date(2020, 1, 1)
        self.assertEqual(year_diff(start_date, end_date, False), 0)

    def test_same_day(self):
        start_date = date(2020, 1, 1)
        end_date = date(2020, 1, 1)
        self.assertAlmostEqual(year_diff(start_date, end_date, False), 0.0)

    def test_six_years(self):
        start_date = date(2015, 1, 1)
        end_date = date(2021, 1, 1)
        self.assertAlmostEqual(
            year_diff(start_date, end_date, False), 6.00078, places=5
        )


if __name__ == "__main__":
    unittest.main()
