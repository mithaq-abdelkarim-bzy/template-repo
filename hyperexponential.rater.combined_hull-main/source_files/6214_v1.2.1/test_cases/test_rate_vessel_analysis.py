import hx
import unittest
import sys
import os

# Add the parent directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from algorithms.rate_vessel_analysis import get_vessel_analysis_criteria_percentage


class TestVesselAnalysisCriteriaPercentage(unittest.TestCase):

    def test_get_vessel_analysis_criteria_percentage_normal_case(self):
        result = get_vessel_analysis_criteria_percentage(
            vessel_type="Fishing (General) - FFS",
            coverage_factor=1,
            vessels_percentile_table=hx.params.table_vessel_percentile_type,
            achieved_rate=0.09,
            commission=0,
        )
        self.assertAlmostEqual(result, 76399.12, places=2)


if __name__ == "__main__":
    unittest.main()
