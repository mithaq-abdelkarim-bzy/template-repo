# If changing the max_layers below, you must also update in vw_constants to the same number
max_layers = 6

benchmark_lr = 0.7

coverages_options_number = 10

cob_code_options_number = 3

# This is set to 10 options and by default shows only 3 unless specified by the user to show all options
coverage_options = [
    {"name": f"option_{i}", "label": f"Option {i}"}
    for i in range(1, (coverages_options_number + 1))
]

coverage_options_names = [item["label"] for item in coverage_options]

brokerage = 27.5

coverage_policy_status = ["Submission", "Quote", "Bound"]
