import unittest
import sys
import os

# Add the parent directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from algorithms.helpers.rate_common import calculate_technical_premium


class TestCalculateTechnicalPremium(unittest.TestCase):

    def test_calculate_technical_premium_normal_case(self):
        premium = 72652.1361019668
        written_line = 0.3
        commission = 0.205
        result = calculate_technical_premium(premium, written_line, commission)
        self.assertAlmostEqual(result, 76399.12, places=2)


if __name__ == "__main__":
    unittest.main()
