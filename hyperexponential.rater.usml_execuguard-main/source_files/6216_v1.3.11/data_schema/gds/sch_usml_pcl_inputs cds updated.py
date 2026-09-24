# import hx_data_schema as hx
# from algorithms.json_parameter_files.parameters import get_parameters

# def modifiers_selection():
#     return {
#             "rationale": hx.Str(mode="output", view={"label": "Rationale"}),
#             "factor_selection": hx.Float(mode="input", default=0, view={"label": "Factor Selection"}),
#             "min": hx.Float(mode="input", default=0, view={"label": "Min","format": {"output": "percent", "mantissa": 0}}),
#             "max": hx.Float(mode="input", default=0, view={"label": "Max","format": {"output": "percent", "mantissa": 0}}),
#             "out_of_range": hx.Str(mode="input", default="", view={"label": "Out of Range"}),
#     }

# def modifiers_factor_selection():
#     return {
#             "factor_selection_nm": hx.Float(mode="input", default=1, view={"label": "Factor Selection", "group":"Non-Admitted"}, validation={"min_value": 1.00, "max_value": 1.15}),
#             "min_nm": hx.Float(mode="input", default=0.95, view={"label": "Min", "group": "Non-Admitted"}),
#             "max_nm": hx.Float(mode="input", default=1.25, view={"label": "Max", "group": "Non-Admitted"}),
#     }

# def quotegrid():
#     return {
#             "option_1": hx.Str(mode="input", default="", view={"label": "Option 1"}),
#             "option_2": hx.Str(mode="input", default="", view={"label": "Option 2"}),
#             "option_3": hx.Str(mode="input", default="", view={"label": "Option 3"}),
#     }

#     # cds.extend_node_items("cds/layers/coverages",{
#     #     "pcl": {"label": "Private Company Liability"}
#     # }),

#     cds.extend_node_rater_defined("cds/layers/coverages/pcl",{
#         "base_rate": hx.Structure(view={"label": "Base Rate"}, children={
#             # Asset Size
#             "asset_size": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Asset Size", "format": {"thousandSeparated": True, "mantissa": 0}}),
#             # Revenue
#             "revenue": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Revenue", "format": {"thousandSeparated": True, "mantissa": 0}}),
#             # Admitted Minimum Premium
#             "admitted_minimum_premium": hx.Float(mode="output", view={"label": "Admitted Minimum Premium", "format": {"thousandSeparated": True, "mantissa": 0}}),
#             # Admitted Minimum Limit
#             "admitted_minimum_limit": hx.Float(mode="output", view={"label": "Admitted Minimum Limit", "format": {"thousandSeparated": True, "mantissa": 0}}),
#         }),
#         # Financial Condition
#         "modifiers_table": hx.Structure(view={"label": "Modifiers"}, children={
#             "financial_condition": hx.Structure(view={"label": "Financial Condition"}, children={
#                     "description": hx.Str(mode="input", default= "Average", optionality="optional", options=["Above Average", "Average", "Below Average"], view={"label": "Description"}),
#                     **modifiers_selection(),
#                     **modifiers_factor_selection()
#             }),
#             # Merger & Acquisition Activity
#             "mergers_and_acquisition_activity": hx.Structure(view={"label": "Merger & Acquisition Activity"}, children={
#                     "description": hx.Str(mode="input", default= "None", optionality="optional", options=["None", "Some", "Significant"], view={"label": "Description"}),
#                     **modifiers_selection(),
#                     **modifiers_factor_selection()
#             }),
#             # Ownership
#             "ownership": hx.Structure(view={"label": "Ownership"}, children={
#                     "description": hx.Str(mode="input", default= "> 50 Shareholders", optionality="optional", options=["< 10 shareholders", "11-25 shareholders", "25-50 shareholders", "> 50 Shareholders", "Major shareholder/family exclusion"], view={"label": "Description"}),
#                     **modifiers_selection(),
#                     **modifiers_factor_selection()
#             }),
#             # Length of Time in Busniess
#             "length_of_time_in_business": hx.Structure(view={"label": "Length of Time in Busniess"}, children={
#                     "description": hx.Str(mode="input", default= "> 10 Years", optionality="optional", options=["< 3 Years", "3-10 Years", "> 10 Years"], view={"label": "Description"}),
#                     **modifiers_selection(),
#                     **modifiers_factor_selection()
#             }),
#             # Layoffs, Downsizing or Spin-offs
#             "layoffs_downsizing_or_spinoffs": hx.Structure(view={"label": "Layoffs, Downsizing or Spin-offs"}, children={
#                     "description": hx.Str(mode="input", default="None in prior two years and none anticipated during the next year", optionality="optional", options=["None in prior two years and none anticipated during the next year", "5% or more in prior two years or anticipated during the next year"], view={"label": "Description"}),
#                     **modifiers_selection()
#             }),
#             # Profitability
#             "profitability": hx.Structure(view={"label": "Profitability"}, children={
#                     "description": hx.Str(mode="input", default="Average", optionality="optional", options=["Above Average", "Average", "Below Average"], view={"label": "Description"}),
#                     **modifiers_selection()
#             }),
#             # Quality of Management
#             "quality_of_management": hx.Structure(view={"label": "Quality of Management"}, children={
#                     "description": hx.Str(mode="input", default="Experienced Professional Team", optionality="optional", options=["Experienced Professional Team", "Family Members/Limited Experience"], view={"label": "Description"}),
#                     **modifiers_selection()
#             }),
#             # Litigation
#             "litigation": hx.Structure(view={"label": "Litigation"}, children={
#                     "description": hx.Str(mode="input", default="No D&O claims", optionality="optional", options=["No D&O claims", "Insured involved in any litigation that could impact earnings or financial position"], view={"label": "Description"}),
#                     **modifiers_selection()
#             }),
#             # Removal of Punitive Damages
#             "removal_of_punitive_damages": hx.Structure(view={"label": "Removal of Punitive Damages"}, children={
#                     "description": hx.Str(mode="input", default="No", optionality="optional", options=["Yes", "No"], view={"label": "Description"}),
#                     **modifiers_selection()
#             }),
#         }),
#         # Class of Business
#         "class_of_business": hx.Str(mode="output", view={"label": "Class of Business"}),
#         # Prior Claim Activity
#         "bnch_prior_claim_activity_selection": hx.Structure(view={"label": "Prior Claim Activity"}, children={
#             "factor_selection": hx.Float(mode="input", default=1, view={"label": "Factor Selection", "group":"Non-Admitted"}, validation={"min_value": 1.00, "max_value": 1.15}),
#             "min": hx.Float(mode="input", default=-0.25, view={"label": "Min", "group": "Non-Admitted", "format": {"output": "percent", "mantissa": 0}}),
#             "max": hx.Float(mode="input", default=3.00, view={"label": "Max", "group": "Non-Admitted", "format": {"output": "percent", "mantissa": 0}}),
#         }),
#         # NE Deviation Factor
#         "ne_devi_fac": hx.Structure(view={"label": "NE Deviation Factor"}, children={
#             **modifiers_selection()
#         }),

#         # Surplus Deviation
#         "surplus_deviation": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Surplus Deviation", "format": {"thousandSeparated": True, "mantissa": 0}}),

#         # Schedule Rating Table
#         "schedule_rating": hx.List(mode="input", children={
#             "sch_rating1": hx.Str(mode="output", view={"label": "Schedule Rating 1"}),
#             **modifiers_selection(),
#         }),
#         "quote_grid": hx.Structure(view={"label": "Quote Grid"}, children={
#             "qb_options": hx.List(mode="input", default_element_count=1, children={
#                 # Aggregate Limit
#                 "limit": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Aggregate Limit", "format": {"thousandSeparated": True, "mantissa": 0}}),
#                 # Retention
#                 "deductible": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Retention", "format": {"thousandSeparated": True, "mantissa": 0}}),
#                 # Limit/Retention Factor
#                 "limit_retention": hx.Float(mode="output", view={"label": "Limit/Retention Factor", "format": {"thousandSeparated": True, "mantissa": 0}}),
#                 # Admitted Premium
#                 "admitted_premium": hx.Float(mode="output", view={"label": "Admitted Premium", "format": {"thousandSeparated": True, "mantissa": 0}}),
#                 # Internal Benchmark
#                 "internal_benchmark": hx.Float(mode="output", view={"label": "Internal Benchmark", "format": {"thousandSeparated": True, "mantissa": 0}}),
#                 # Guideline Minimum Premium
#                 "guideline_minimum_premium": hx.Float(mode="output", view={"label": "Guideline Minimum Premium", "format": {"thousandSeparated": True, "mantissa": 0}}),
#                 # BPI%
#                 "bpi": hx.Float(mode="output", view={"label": "BPI%", "format": {"output": "percent", "mantissa": 1}}),
#                 # Select Option?
#                 "option_selected": hx.Bool(mode="input", default=True, view={"label": "Select Option?"}),
#             })
#         }),
#     })
