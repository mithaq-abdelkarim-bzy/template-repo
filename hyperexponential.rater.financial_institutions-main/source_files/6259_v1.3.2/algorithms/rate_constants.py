import numpy as np

# If changing the max_layers below, you must also update in vw_constants to the same number
max_layers = 16
benchmark_lr = 0.7
coverages = (("crime", "Crime"), ("pi", "PI"), ("do", "D&O"))
do_sides = ("A", "B", "C", "Dic")
max_towers = 6
min_uw_adj = -0.3
ilfc = 1.3
ilfp = 1.4
ilfd = 1.5
ilf_log_param = 2
coverage_switch = {
        "Crime": ["crime"],
        "PI": ["pi"],
        "D&O": ["A"],
        "D&O ABC": ["A", "B", "C"],
        "D&O AB": ["A", "B"],
        "D&O A": ["A"],
        "D&O A Dic": ["A", "Dic"],
        "Crime / PI": ["crime", "pi"],
        "Crime / PI / D&O A": ["crime", "pi", "A"],
        "Crime / PI / D&O AB": ["crime", "pi", "A", "B"],
        "Crime / PI / D&O ABC": ["crime", "pi", "A", "B", "C"],
        "Crime / D&O ABC": ["crime", "A", "B", "C"],
        "Crime / D&O AB": ["crime", "A", "B"],
        "Crime / D&O A": ["crime", "A"],
        "PI / D&O ABC": ["pi", "A", "B", "C"],
        "PI / D&O AB": ["pi", "A", "B"],
        "PI / D&O A": ["pi", "A"],
    }
selected_ilf_factor = {
        "crime": {"power_ilf": ilfc, "alpha": np.log(ilfc) / np.log(ilf_log_param)},
        "pi": {"power_ilf": ilfp, "alpha": np.log(ilfp) / np.log(ilf_log_param)},
        "A": {"power_ilf": ilfd, "alpha": np.log(ilfd) / np.log(ilf_log_param)},
        "B": {"power_ilf": ilfd, "alpha": np.log(ilfd) / np.log(ilf_log_param)},
        "C": {"power_ilf": ilfd, "alpha": np.log(ilfd) / np.log(ilf_log_param)},
        "Dic": {"power_ilf": ilfd, "alpha": np.log(ilfd) / np.log(ilf_log_param)},
    }
coverage_types = ["manager", "fund"]

# ============================================================================
# DATA STRUCTURE HELPERS
# ============================================================================

def coverage_dict():
    """Create a standardized coverage dictionary structure."""
    return {
        coverage: {cov_type: 0 for cov_type in coverage_types}
        for coverage in selected_ilf_factor  # keys provide list of coverages
    }


def coverage_type_included_dict():
    """Create a standardized coverage dictionary structure."""
    return {
        coverage[0]: {cov_type: False for cov_type in coverage_types}
        for coverage in coverages  # keys provide list of coverages
    }


def towers_by_fund_manager_dict():
    return {coverage: [] for coverage in coverage_types}


def tower_dict():
    """Create a standardized tower dictionary structure."""
    return {f"tower_{i}": [] for i in range(1, max_towers + 1)}