import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format
from data_schema.sch_utilities import percent_format
from data_schema.sch_utilities import integer_format
from algorithms.rate_constants import max_layers
import data_schema.sch_utilities as utils

def sch_rating_summary_mmp(cds):


    cds.extend_node_rater_defined("cds", {
        "mmp": hx.Structure(view ={"label": "MMP"}, children = {
            "dno": hx.Structure(view ={"label": "Directors and Officers (D&O)"}, children = {
                "coverage": hx.Str(mode="input", default="ABC", optionality="required", options=["ABC", "AB"], view={"label": "Coverage"}, async_input=["rarc_task"]),
                "expiring_appetite_comment": hx.Str(mode="input", default = None, optionality="optional", view={"label": "Expiring \n Appetite \n Comments", "options" : {"read_only": {"read_only" : True}}}, async_output=["expiring_policy_fetch_task", "start_renewal_task"]),
                "agg_aoc_limit": hx.Str(mode="input", default="Agg", optionality="optional",options=["Agg", "AOC"], view={"label": "Agg/AOC Limit"}),
                "appetite_comment": hx.Str(mode="output", view={"label": "Appetite \n Comments"}),
                "limit": hx.Float(mode="input", default=1000000, optionality="optional", view={"label": "Limit", "format": {"thousandSeparated": True, "mantissa": 0}}, async_input=["rarc_task"]),
                "excess": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Excess", "format": {"thousandSeparated": True, "mantissa": 0}}, async_input=["rarc_task"]),
                "deductible": hx.Float(mode="input", default=50000, optionality="optional", view={"label": "Deductible / SIR", "format": {"thousandSeparated": True, "mantissa": 0}}, async_input=["rarc_task"]),
                "section_reference": hx.Str(mode="output", view={"label": "Section \n Reference"}),
                "brokerage": hx.Float(mode="input", default=0.2, optionality="optional", view={"label": "Brokerage", "format": {"output": "percent", "mantissa": 1}}, async_input=["rarc_task"]),
                "written_line": hx.Float(mode="input", default=1, optionality="optional",validation={"min_value": 0, "max_value": 1.0}, view={"label": "Beazley \n Market Share", "format": {"output": "percent", "mantissa": 1}}, async_input=["rarc_task"]),
                "quoted_premium_100": hx.Float(mode="input", default=0, optionality="optional", view={"label": "100% Gross \n Premium", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "status": hx.Str(mode="output", view={"label": "Status"}),
                "slip_leader": hx.Str(mode="output",view={"label": "Slip Leader", "options": {"notSupported": {"style_cell": None}}}),
                "notes": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Notes"}),
                "benchmark_premium": hx.Float(mode="output", optionality="optional", view={"label": "Gross Benchmark \n Premium \n (incl. UW adj)", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "bpi": hx.Float(mode="output", optionality="optional", view={"label": "BPI % \n (incl. UW adj)", "format": {"output": "percent", "mantissa": 1}}),
                "technical_premium": hx.Float(mode="output", optionality="optional", view={"label": "Gross Technical \n Premium \n (incl. UW adj)", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "tpi": hx.Float(mode="output", optionality="optional", view={"label": "TPI % \n (incl. UW adj)", "format": {"output": "percent", "mantissa": 1}}),
                "option_1": hx.Structure(view={"label": "Option 1"}, children={
                    "aggregate_limit": hx.Float(mode="input", default=1e6, optionality="optional", view={"label": "Aggregate Limit", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    "aggregate_excess": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Aggregate Excess", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    "aggregate_deductible": hx.Float(mode="input", default=50000, optionality="optional", view={"label": "Aggregate Deductible", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    "technical_premium": hx.Float(mode="output",view={"label": "Technical Premium", "format": {"thousandSeparated": True, "mantissa": 0}}),
                }),
                "option_2": hx.Structure(view={"label": "Option 2"}, children={
                    "aggregate_limit": hx.Float(mode="input", default=3e6, optionality="optional", view={"label": "Aggregate Limit", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    "aggregate_excess": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Aggregate Excess", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    "aggregate_deductible": hx.Float(mode="input", default=50000, optionality="optional", view={"label": "Aggregate Deductible", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    "technical_premium": hx.Float(mode="output",view={"label": "Technical Premium", "format": {"thousandSeparated": True, "mantissa": 0}}),
                }),
                "option_3": hx.Structure(view={"label": "Option 3"}, children={
                    "aggregate_limit": hx.Float(mode="input", default=5e6, optionality="optional", view={"label": "Aggregate Limit", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    "aggregate_excess": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Aggregate Excess", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    "aggregate_deductible": hx.Float(mode="input", default=50000, optionality="optional", view={"label": "Aggregate Deductible", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    "technical_premium": hx.Float(mode="output",view={"label": "Technical Premium", "format": {"thousandSeparated": True, "mantissa": 0}}),
                }),
                "option_4": hx.Structure(view={"label": "Option 4"}, children={
                    "aggregate_limit": hx.Float(mode="input", default=10e6, optionality="optional", view={"label": "Aggregate Limit", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    "aggregate_excess": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Aggregate Excess", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    "aggregate_deductible": hx.Float(mode="input", default=50000, optionality="optional", view={"label": "Aggregate Deductible", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    "technical_premium": hx.Float(mode="output",view={"label": "Technical Premium", "format": {"thousandSeparated": True, "mantissa": 0}}),
                })
                # "selected_option": hx.Str(mode="input", default=None, optionality="optional", options_data="../../../layers", options_field="option_label", view={"label": "Selected Option"}, async_input=["rarc_task"])
            }),
            "epl": hx.Structure(view ={"label": "Employment Practice Liability (EPL)"}, children = {
                "coverage": hx.Str(mode="output", view={"label": "Coverage"}),
                "expiring_appetite_comment": hx.Str(mode="input", default = None, optionality="optional", view={"label": "Expiring Appetite Comments", "options" : {"read_only": {"read_only" : True}}}, async_output=["expiring_policy_fetch_task", "start_renewal_task"]),
                "agg_aoc_limit": hx.Str(mode="input", default="Agg", optionality="optional",options=["Agg", "AOC"], view={"label": "Agg/AOC Limit"}),
                "appetite_comment": hx.Str(mode="output", view={"label": "Appetite Comments"}),
                "limit": hx.Float(mode="input", default=1000000, optionality="optional", view={"label": "Limit", "format": {"thousandSeparated": True, "mantissa": 0}}, async_input=["rarc_task"]),
                "excess": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Excess", "format": {"thousandSeparated": True, "mantissa": 0}}, async_input=["rarc_task"]),
                "deductible": hx.Float(mode="input", default=50000, optionality="optional", view={"label": "Deductible", "format": {"thousandSeparated": True, "mantissa": 0}}, async_input=["rarc_task"]),
                "section_reference": hx.Str(mode="output", view={"label": "Section Reference"}),
                "brokerage": hx.Float(mode="input", default=0.2, optionality="optional", view={"label": "Brokerage", "format": {"output": "percent", "mantissa": 1}}, async_input=["rarc_task"]),
                "written_line": hx.Float(mode="input", default=1, optionality="optional",validation={"min_value": 0, "max_value": 1.0}, view={"label": "Beazley Market Share", "format": {"output": "percent", "mantissa": 1}}, async_input=["rarc_task"]),
                "quoted_premium_100": hx.Float(mode="input", default=0, optionality="optional", view={"label": "100% Gross Premium", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "status": hx.Str(mode="output", view={"label": "Status"}),
                "slip_leader": hx.Str(mode="output",view={"label": "Slip Leader", "options": {"notSupported": {"style_cell": None}}}),
                "notes": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Notes"}),
                "benchmark_premium": hx.Float(mode="output", optionality="optional", view={"label": "Gross Benchmark Premium (incl. UW adj)", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "bpi": hx.Float(mode="output", optionality="optional", view={"label": "BPI (incl. UW adj)", "format": {"output": "percent", "mantissa": 1}}),
                "technical_premium": hx.Float(mode="output", optionality="optional", view={"label": "Gross Technical Premium (incl. UW adj)", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "tpi": hx.Float(mode="output", optionality="optional", view={"label": "TPI (incl. UW adj)", "format": {"output": "percent", "mantissa": 1}}),
                "option_1": hx.Structure(view={"label": "Option 1"}, children={
                    "aggregate_limit": hx.Float(mode="input", default=1e6, optionality="optional", view={"label": "Aggregate Limit", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    "aggregate_excess": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Aggregate Excess", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    "aggregate_deductible": hx.Float(mode="input", default=50000, optionality="optional", view={"label": "Aggregate Deductible", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    "technical_premium": hx.Float(mode="output",view={"label": "Technical Premium", "format": {"thousandSeparated": True, "mantissa": 0}}),
                }),
                "option_2": hx.Structure(view={"label": "Option 2"}, children={
                    "aggregate_limit": hx.Float(mode="input", default=3e6, optionality="optional", view={"label": "Aggregate Limit", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    "aggregate_excess": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Aggregate Excess", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    "aggregate_deductible": hx.Float(mode="input", default=50000, optionality="optional", view={"label": "Aggregate Deductible", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    "technical_premium": hx.Float(mode="output",view={"label": "Technical Premium", "format": {"thousandSeparated": True, "mantissa": 0}}),
                }),
                "option_3": hx.Structure(view={"label": "Option 3"}, children={
                    "aggregate_limit": hx.Float(mode="input", default=5e6, optionality="optional", view={"label": "Aggregate Limit", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    "aggregate_excess": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Aggregate Excess", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    "aggregate_deductible": hx.Float(mode="input", default=50000, optionality="optional", view={"label": "Aggregate Deductible", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    "technical_premium": hx.Float(mode="output",view={"label": "Technical Premium", "format": {"thousandSeparated": True, "mantissa": 0}}),
                }),
                "option_4": hx.Structure(view={"label": "Option 4"}, children={
                    "aggregate_limit": hx.Float(mode="input", default=10e6, optionality="optional", view={"label": "Aggregate Limit", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    "aggregate_excess": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Aggregate Excess", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    "aggregate_deductible": hx.Float(mode="input", default=50000, optionality="optional", view={"label": "Aggregate Deductible", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    "technical_premium": hx.Float(mode="output",view={"label": "Technical Premium", "format": {"thousandSeparated": True, "mantissa": 0}}),
                })
                # "selected_option": hx.Str(mode="input", default=None, optionality="optional", options_data="../../../layers", options_field="option_label", view={"label": "Selected Option"}, async_input=["rarc_task"])
            }),
            "cll": hx.Structure(view ={"label": "Corporate Legal Liability (CLL)"}, children = {
                "coverage": hx.Str(mode="output", view={"label": "Coverage"}),
                "expiring_appetite_comment": hx.Str(mode="input", default = None, optionality="optional", view={"label": "Expiring Appetite Comments", "options" : {"read_only": {"read_only" : True}}}, async_output=["expiring_policy_fetch_task", "start_renewal_task"]),
                "agg_aoc_limit": hx.Str(mode="input", default="Agg", optionality="optional",options=["Agg", "AOC"], view={"label": "Agg/AOC Limit"}),
                "appetite_comment": hx.Str(mode="output", view={"label": "Appetite Comments"}),
                "limit": hx.Float(mode="input", default=1000000, optionality="optional", view={"label": "Limit", "format": {"thousandSeparated": True, "mantissa": 0}}, async_input=["rarc_task"]),
                "excess": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Excess", "format": {"thousandSeparated": True, "mantissa": 0}}, async_input=["rarc_task"]),
                "deductible": hx.Float(mode="input", default=50000, optionality="optional", view={"label": "Deductible", "format": {"thousandSeparated": True, "mantissa": 0}}, async_input=["rarc_task"]),
                "section_reference": hx.Str(mode="output", view={"label": "Section Reference"}),
                "brokerage": hx.Float(mode="input", default=0.2, optionality="optional", view={"label": "Brokerage", "format": {"output": "percent", "mantissa": 1}}, async_input=["rarc_task"]),
                "written_line": hx.Float(mode="input", default=1, optionality="optional",validation={"min_value": 0, "max_value": 1.0}, view={"label": "Beazley Market Share", "format": {"output": "percent", "mantissa": 1}}, async_input=["rarc_task"]),
                "quoted_premium_100": hx.Float(mode="input", default=0, optionality="optional", view={"label": "100% Gross Premium", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "status": hx.Str(mode="output", view={"label": "Status"}),
                "slip_leader": hx.Str(mode="output",view={"label": "Slip Leader", "options": {"notSupported": {"style_cell": None}}}),
                "notes": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Notes"}),
                "benchmark_premium": hx.Float(mode="output", optionality="optional", view={"label": "Gross Benchmark Premium (incl. UW adj)", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "bpi": hx.Float(mode="output", optionality="optional", view={"label": "BPI (incl. UW adj)", "format": {"output": "percent", "mantissa": 1}}),
                "technical_premium": hx.Float(mode="output", optionality="optional", view={"label": "Gross Technical Premium (incl. UW adj)", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "tpi": hx.Float(mode="output", optionality="optional", view={"label": "TPI (incl. UW adj)", "format": {"output": "percent", "mantissa": 1}}),
                "option_1": hx.Structure(view={"label": "Option 1"}, children={
                    "aggregate_limit": hx.Float(mode="input", default=1e6, optionality="optional", view={"label": "Aggregate Limit", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    "aggregate_excess": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Aggregate Excess", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    "aggregate_deductible": hx.Float(mode="input", default=50000, optionality="optional", view={"label": "Aggregate Deductible", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    "technical_premium": hx.Float(mode="output",view={"label": "Technical Premium", "format": {"thousandSeparated": True, "mantissa": 0}}),
                }),
                "option_2": hx.Structure(view={"label": "Option 2"}, children={
                    "aggregate_limit": hx.Float(mode="input", default=3e6, optionality="optional", view={"label": "Aggregate Limit", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    "aggregate_excess": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Aggregate Excess", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    "aggregate_deductible": hx.Float(mode="input", default=50000, optionality="optional", view={"label": "Aggregate Deductible", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    "technical_premium": hx.Float(mode="output",view={"label": "Technical Premium", "format": {"thousandSeparated": True, "mantissa": 0}}),
                }),
                "option_3": hx.Structure(view={"label": "Option 3"}, children={
                    "aggregate_limit": hx.Float(mode="input", default=5e6, optionality="optional", view={"label": "Aggregate Limit", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    "aggregate_excess": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Aggregate Excess", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    "aggregate_deductible": hx.Float(mode="input", default=50000, optionality="optional", view={"label": "Aggregate Deductible", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    "technical_premium": hx.Float(mode="output",view={"label": "Technical Premium", "format": {"thousandSeparated": True, "mantissa": 0}}),
                }),
                "option_4": hx.Structure(view={"label": "Option 4"}, children={
                    "aggregate_limit": hx.Float(mode="input", default=10e6, optionality="optional", view={"label": "Aggregate Limit", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    "aggregate_excess": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Aggregate Excess", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    "aggregate_deductible": hx.Float(mode="input", default=50000, optionality="optional", view={"label": "Aggregate Deductible", "format": {"thousandSeparated": True, "mantissa": 0}}),
                    "technical_premium": hx.Float(mode="output",view={"label": "Technical Premium", "format": {"thousandSeparated": True, "mantissa": 0}}),
                })
                # "selected_option": hx.Str(mode="input", default=None, optionality="optional", options_data="../../../layers", options_field="option_label", view={"label": "Selected Option"}, async_input=["rarc_task"])
            }),
            "crime": hx.Structure(view ={"label": "Crime"}, children = {
                "coverage": hx.Str(mode="output", view={"label": "Coverage"}),
                "expiring_appetite_comment": hx.Str(mode="output", view={"label": "Expiring Appetite Comments"}),
                "agg_aoc_limit": hx.Str(mode="input", default="Agg", optionality="optional",options=["Agg", "AOC"], view={"label": "Agg/AOC Limit"}),
                "appetite_comment": hx.Str(mode="output", view={"label": "Appetite Comments"}),
                "limit": hx.Float(mode="input", default=1000000, optionality="optional", view={"label": "Limit", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "excess": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Excess", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "deductible": hx.Float(mode="input", default=50000, optionality="optional", view={"label": "Deductible", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "section_reference": hx.Str(mode="output", view={"label": "Section Reference"}),
                "brokerage": hx.Float(mode="input", default=0.2, optionality="optional", view={"label": "Brokerage", "format": {"output": "percent", "mantissa": 1}}),
                "written_line": hx.Float(mode="input", default=1, optionality="optional",validation={"min_value": 0, "max_value": 1.0}, view={"label": "Beazley Market Share", "format": {"output": "percent", "mantissa": 1}}),
                "quoted_premium_100": hx.Float(mode="input", default=0, optionality="optional", view={"label": "100% Gross Premium", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "status": hx.Str(mode="output", view={"label": "Status"}),
                "slip_leader": hx.Str(mode="output",view={"label": "Slip Leader", "options": {"notSupported": {"style_cell": None}}}),
                "notes": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Notes"}),
                "benchmark_premium": hx.Float(mode="output", optionality="optional", view={"label": "Gross Benchmark Premium (incl. UW adj)", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "bpi": hx.Float(mode="output", optionality="optional", view={"label": "BPI (incl. UW adj)", "format": {"output": "percent", "mantissa": 1}}),
                "technical_premium": hx.Float(mode="output", optionality="optional", view={"label": "Gross Technical Premium (incl. UW adj)", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "tpi": hx.Float(mode="output", optionality="optional", view={"label": "TPI (incl. UW adj)", "format": {"output": "percent", "mantissa": 1}}),
                # "selected_option": hx.Str(mode="input", default=None, optionality="optional", options_data="../../../layers", options_field="option_label", view={"label": "Selected Option"}, async_input=["rarc_task"])
            }),
            "ptl": hx.Structure(view ={"label": "Pensions Trustee Liability (PTL)"}, children = {
                "coverage": hx.Str(mode="output", view={"label": "Coverage"}),
                "expiring_appetite_comment": hx.Str(mode="output", view={"label": "Expiring Appetite Comments"}),
                "agg_aoc_limit": hx.Str(mode="input", default="Agg", optionality="optional",options=["Agg", "AOC"], view={"label": "Agg/AOC Limit"}),
                "appetite_comment": hx.Str(mode="output", view={"label": "Appetite Comments"}),
                "limit": hx.Float(mode="input", default=1000000, optionality="optional", view={"label": "Limit", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "excess": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Excess", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "deductible": hx.Float(mode="input", default=50000, optionality="optional", view={"label": "Deductible", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "section_reference": hx.Str(mode="output", view={"label": "Section Reference"}),
                "brokerage": hx.Float(mode="input", default=0.2, optionality="optional", view={"label": "Brokerage", "format": {"output": "percent", "mantissa": 1}}),
                "written_line": hx.Float(mode="input", default=1, optionality="optional",validation={"min_value": 0, "max_value": 1.0}, view={"label": "Beazley Market Share", "format": {"output": "percent", "mantissa": 1}}),
                "quoted_premium_100": hx.Float(mode="input", default=0, optionality="optional", view={"label": "100% Gross Premium", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "status": hx.Str(mode="output", view={"label": "Status"}),
                "slip_leader": hx.Str(mode="output",view={"label": "Slip Leader", "options": {"notSupported": {"style_cell": None}}}),
                "notes": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Notes"}),
                "benchmark_premium": hx.Float(mode="output", optionality="optional", view={"label": "Gross Benchmark Premium (incl. UW adj)", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "bpi": hx.Float(mode="output", optionality="optional", view={"label": "BPI (incl. UW adj)", "format": {"output": "percent", "mantissa": 1}}),
                "technical_premium": hx.Float(mode="output", optionality="optional", view={"label": "Gross Technical Premium (incl. UW adj)", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "tpi": hx.Float(mode="output", optionality="optional", view={"label": "TPI (incl. UW adj)", "format": {"output": "percent", "mantissa": 1}}),
                # "selected_option": hx.Str(mode="input", default=None, optionality="optional", options_data="../../../layers", options_field="option_label", view={"label": "Selected Option"}, async_input=["rarc_task"])
             }),
            "total": hx.Structure(view ={"label": "Total"}, children = {
                "coverage": hx.Str(mode="output", view={"label": "Coverage"}),
                "expiring_appetite_comment": hx.Str(mode="input", default = None, optionality = "optional", view={"label": "Expiring Appetite Comments", "options" : {"read_only": {"read_only" : True}}}),
                "agg_aoc_limit": hx.Str(mode="output", view={"label": "Agg/AOC Limit"}),
                "appetite_comment": hx.Str(mode="output", view={"label": "Appetite Comments"}),
                "limit": hx.Float(mode="output", view={"label": "Limit", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "excess": hx.Float(mode="output", view={"label": "Excess", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "deductible": hx.Float(mode="output", view={"label": "Deductible", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "section_reference": hx.Str(mode="input",default=None, optionality="optional", async_output=["start_renewal_task"], view={"label": "Section Reference", "options" : {"read_only": {"read_only" : True}}}),
                "brokerage": hx.Float(mode="output", view={"label": "Brokerage","format": {"output": "percent", "mantissa": 1}}),
                "written_line": hx.Float(mode="output", view={"label": "Beazley Market Share", "format": {"output": "percent", "mantissa": 1}}),
                "quoted_premium_100": hx.Float(mode="output", view={"label": "100% Gross Premium", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "status": hx.Str(mode="input", default=None, async_output=["start_renewal_task"], optionality="optional", options_table = "lst_deal_status", options_column = "DealStatus", view={"label": "Status", "options" : {"read_only": {"read_only" : True}}}),
                "slip_leader": hx.Str(mode="input", default="Beazley", optionality="required", options_table="lst_slip_lead", options_column="Markets",view={"label": "Slip Leader", "options": {"notSupported": {"style_cell": "hx-neutral"}}}),
                "notes": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Notes"}),
                "benchmark_premium": hx.Float(mode="output", optionality="optional", view={"label": "Gross Benchmark Premium", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "bpi": hx.Float(mode="output", optionality="optional", view={"label": "BPI %", "format": {"output": "percent", "mantissa": 1}}),
                "technical_premium": hx.Float(mode="output", optionality="optional", view={"label": "Gross Technical Premium", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "tpi": hx.Float(mode="output", optionality="optional", view={"label": "TPI %", "format": {"output": "percent", "mantissa": 1}}),
                "validation_note": hx.Str(mode="output", view={"label": "Validation Notes"}),
                # "tpi_pre_uw_adj": hx.Float(mode="output", optionality="optional", view={"label": "TPI (excl. UW adj)", "format": {"output": "percent", "mantissa": 1}}),
                # "bpi_pre_uw_adj": hx.Float(mode="output", optionality="optional", view={"label": "BPI (excl. UW adj)", "format": {"output": "percent", "mantissa": 1}}),
                "pflr": hx.Float(mode="output", optionality="optional", view={"label": "Priced-For-Loss-Ratio", "format": {"output": "percent", "mantissa": 1}}),
                # "pflr_pre_uw_adj": hx.Float(mode="output", optionality="optional", view={"label": "Priced-For-Loss-Ratio (excl. UW adj)", "format": {"output": "percent", "mantissa": 1}}),
                # "uw_adj_impact": hx.Float(mode="output", optionality="optional", view={"label": "Impact of Underwriting Adjustments", "format": {"output": "percent", "mantissa": 1}}),
                "expected_loss_cost": hx.Float(mode="output", optionality="optional", view={"label": "Total Expected \n Losses", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "expected_loss_cost_100": hx.Float(mode="output", optionality="optional", view={"label": "Expected Loss Cost (100%)", "format":utils.thousands_format(0)}),
                "quoted_premium_net": hx.Float(mode="output", optionality="optional", view={"label": "Net Quoted Premium (AFB)", "format":utils.thousands_format(0)}),
                "quoted_premium_net_100": hx.Float(mode="output", optionality="optional", view={"label": "Net Quoted Premium (100%)", "format":utils.thousands_format(0)}),
                "quoted_premium_100": hx.Float(mode="output", optionality="optional", view={"label": "Gross Quoted Premium (100%)", "format":utils.thousands_format(0)}),
                "quoted_premium_annual": hx.Float(mode="output", optionality="optional", view={"label": "Annualised Gross Quoted Premium (AFB)", "format":utils.thousands_format(0)}),
                "quoted_premium_annual_100": hx.Float(mode="output", optionality="optional", view={"label": "Annualised Gross Quoted Premium (100%)", "format":utils.thousands_format(0)}),
                "benchmark_premium_net": hx.Float(mode="output", optionality="optional", view={"label": "Net Benchmark Premium (AFB)", "format":utils.thousands_format(0)}),
                "benchmark_premium_net_100": hx.Float(mode="output", optionality="optional", view={"label": "Net Benchmark Premium (100%)", "format":utils.thousands_format(0)}),
                "benchmark_premium_100": hx.Float(mode="output", optionality="optional", view={"label": "Gross Benchmark Premium (100%)", "format":utils.thousands_format(0)}),
                "benchmark_premium_annual": hx.Float(mode="output", optionality="optional", view={"label": "Annualised Gross Benchmark Premium (AFB)", "format":utils.thousands_format(0)}),
                "benchmark_premium_annual_100": hx.Float(mode="output", optionality="optional", view={"label": "Annualised Gross Benchmark Premium (100%)", "format":utils.thousands_format(0)}),
                "benchmark_premium_pre_uw_adj": hx.Float(mode="output", optionality="optional", view={"label": "Gross Benchmark Premium (Pre-UW Adjustment)", "format":utils.thousands_format(0)}),
                "technical_premium_100": hx.Float(mode="output", optionality="optional", view={"label": "Gross Technical Premium (100%)", "format":utils.thousands_format(0)}),
                "technical_premium_net_100": hx.Float(mode="output", optionality="optional", view={"label": "Net Technical Premium (100%)", "format":utils.thousands_format(0)}),
                "pflr_pre_uw_adj": hx.Float(mode="output", optionality="optional", view={"label": "Priced-for Loss Ratio (Pre-UW Adj.)", "format":utils.thousands_format(0)}),
            })})}),

    # cds.extend_node_items("cds/layers/coverages", {
    #     "mmp_dno": {"label": "D&O"},
    #     "mmp_epl": {"label": "EPL"},
    #     "mmp_cll": {"label": "CLL"},
    #     "mmp_ptl": {"label": "PTL"},
    #     "mmp_crime": {"label": "Crime"}})

    # cds.extend_node_rater_defined("cds/layers/coverages", {
        
        # "selected_option": hx.Str(mode="input", default="Option 1", optionality="optional", options_data="../coverages", options_field="option_label", view={"label": "Selected Option"}, async_input=["rarc_task"])
    # })





    # cds.override_node_properties("cds/layers/coverages", {"default_element_count": 4})

