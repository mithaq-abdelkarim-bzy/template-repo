import hx_data_schema as hxd

from algorithms.rate_constants import max_towers
from algorithms.rate_utilities import get_field_options
from libraries.common_data_schema.data_schema.utilities import percent_format, thousands_format


def sch_rating_factors(cds):
    cds.extend_node_rater_defined("cds", {
        "rating_factors": hxd.Structure(children={
            "policy_term": hxd.Float(mode="output"),

            "risk_info": hxd.Structure(children={
                "region": hxd.Str(mode="input", default="Europe", optionality="optional", options_data="../../../../non_cds/risk_info/region_dropdown", options_field="region", async_input=["rarc_task"], view={"label": "Region of Domicile"}),
                "sub_industry": hxd.Str(mode="input", default=None, optionality="optional", options_data="../../../../non_cds/risk_info/sub_industry_dropdown", options_field="sub_industry", async_input=["rarc_task", "generate_tags"], view={"label": "Sub Industry"}),
                "ownership_type": hxd.Str(mode="input", options=get_field_options("risk_information", "ownership_type"), default="Public", async_input=["rarc_task"], view={"label": "Ownership Type"}),
                "crime_coverage_required": hxd.Bool(mode="input", default=True, async_input=["rarc_task"], view={"label": "Crime"}),
                "pi_coverage_required": hxd.Bool(mode="input", default=True, async_input=["rarc_task"], view={"label": "PI"}),
                "do_coverage_required": hxd.Bool(mode="input", default=True, async_input=["rarc_task"], view={"label": "D&O"}),
            }),
            "exposure_details": hxd.Structure(children={
                "no_of_locations": hxd.Int(mode="input", default=None, optionality="optional", view={"label": "Number Of Locations"}),
                "currency": hxd.Str(mode="input", optionality="optional", options_column="Currency code", options_table="table_ccy_base", default="USD", async_input=["rarc_task"], view={"label": "Currency For Exposure Details"}),
                "main_listing": hxd.Str(mode="input", default="", optionality="optional", view={"label": "Main Listing (if public)"}),
                "ipo_date": hxd.Date(mode="input", default=None, optionality="optional", view={"label": "IPO Date"}),
                "us_listing": hxd.Str(mode="input", default=None, optionality="optional", options=get_field_options("exposure_details", "us_listing"), async_input=["rarc_task"], view={"label": "US Listing"}),
                "cr_s_and_p": hxd.Str(mode="input", optionality="optional", options_column="SP", options_table="table_cr_sp", default=None, view={"label": "S&P"}),
                "cr_moodys": hxd.Str(mode="input", optionality="optional", options_column="Moody", options_table="table_cr_moody", default=None, view={"label": "Moody's"}),
                "cr_fitch": hxd.Str(mode="input", optionality="optional", options_column="Fitch", options_table="table_cr_fitch", default=None, view={"label": "Fitch"}),
                "combined_ratio": hxd.Float(mode="input", default=None, optionality="optional", view={"label": "Combined Ratio", "format": percent_format()}),
                "solvency_ratio": hxd.Float(mode="input", default=None, optionality="optional", view={"label": "Solvency Ratio", "info": "Enter as a % of regulatory target", "format": percent_format()}),
                "short_tail_pc": hxd.Float(mode="input", default=None, optionality="optional", view={"label": "Short/Long tail", "info": "Enter % of short tail business over total)", "format": percent_format()}),
                "direct_business_pc": hxd.Float(mode="input", default=None, optionality="optional", view={"label": "Direct or via Intermediaries", "info": "Distribution method - enter % of direct business over total", "format": percent_format()}),
            }),
            "cover_details": hxd.Structure(children={
                "primary_layer": hxd.Structure(children={
                    "do_type": hxd.Str(mode="input", default=None, optionality="optional", options=get_field_options("cover_details", "do_type"), async_input=["rarc_task"], view={"label": "D&O Type"}),
                    "towers_all_manager": hxd.Structure(view={"label": "Towers", "options": {"manager": {"label": "Towers (Manager)"}}}, children={
                        "crime": hxd.Str(mode="input", options=get_towers_options(), default="NA", async_input=["rarc_task"], view={"label": "Crime"}),
                        "pi": hxd.Str(mode="input", options=get_towers_options(), default="NA", async_input=["rarc_task"], view={"label": "PI"}),
                        "do": hxd.Str(mode="input", options=get_towers_options(), default="NA", async_input=["rarc_task"], view={"label": "D&O"}),
                    }),
                    "towers_fund": hxd.Structure(view={"label": "Towers (Fund)"}, children={
                        "crime": hxd.Str(mode="input", options=get_towers_options(), default="NA", async_input=["rarc_task"], view={"label": "Crime"}),
                        "pi": hxd.Str(mode="input", options=get_towers_options(), default="NA", async_input=["rarc_task"], view={"label": "PI"}),
                        "do": hxd.Str(mode="input", options=get_towers_options(), default="NA", async_input=["rarc_task"], view={"label": "D&O"}),
                    }),
                    "sir_all_manager": hxd.Structure(view={"label": "SIR", "options": {"manager": {"label": "SIR (Manager)"}}}, children={
                        "crime": hxd.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0}, async_input=["rarc_task"], view={"label": "Crime", "format": thousands_format()}),
                        "pi": hxd.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0}, async_input=["rarc_task"], view={"label": "PI", "format": thousands_format()}),
                        "do": hxd.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0}, async_input=["rarc_task"], view={
                            "label": "D&O", "format": thousands_format(),
                            "options": {"side_b": {"label": "D&O - Side B", "format": thousands_format()}}
                        }),
                        "do_side_c": hxd.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0}, async_input=["rarc_task"], view={"label": "D&O - Side C", "format": thousands_format()}),
                    }),
                    "sir_fund": hxd.Structure(view={"label": "SIR (Fund)"}, children={
                        "crime": hxd.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0}, async_input=["rarc_task"], view={"label": "Crime", "format": thousands_format()}),
                        "pi": hxd.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0}, async_input=["rarc_task"], view={"label": "PI", "format": thousands_format()}),
                        "do": hxd.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0}, async_input=["rarc_task"], view={
                            "label": "D&O", "format": thousands_format(),
                            "options": {"side_b": {"label": "D&O - Side B", "format": thousands_format()}}
                        }),
                        "do_side_c": hxd.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0}, async_input=["rarc_task"], view={"label": "D&O - Side C", "format": thousands_format()}),
                    }),
                }),
                "sublimits_req": hxd.Bool(mode="input", default=False, async_input=["rarc_task"], view={"label": "Different sub-limits required?"}),
                "crime_retroactive_date": hxd.Str(mode="input", options=get_field_options("cover_details", "crime_retroactive_date"), default="Full Retro", async_input=["rarc_task"], view={"label": "Retroactive date - Crime"}),
                "pi_retroactive_date": hxd.Str(mode="input", options=get_field_options("cover_details", "pi_retroactive_date"), default="Full Retro", async_input=["rarc_task"], view={"label": "Retroactive date - PI"}),
                "do_retroactive_date": hxd.Str(mode="input", options=get_field_options("cover_details", "do_retroactive_date"), default="Full Retro", async_input=["rarc_task"], view={"label": "Retroactive date - D&O"}),
                "details_reinstatements": hxd.Str(mode="input", options=get_field_options("cover_details", "details_reinstatements"), default="NA", async_input=["rarc_task"], view={"label": "Reinstatements"}),
                "reinst_rtc_program_limit": hxd.Int(mode="input", default=None, optionality="optional", async_input=["rarc_task"], view={"label": "Total Program Limit for RTC"}),
                "no_direct_reinstatements": hxd.Int(mode="input", default=None, optionality="optional", validation={"min_value": 0, "max_value": 10000}, async_input=["rarc_task"], view={"label": "Number of Direct Reinstatements"}),
                "brokerage_all_layers": hxd.Structure(children={
                    "brk": hxd.Float(mode="input", default=0, async_input=["rarc_task"], view={"options":{"input":{"label": "Brokerage", "format": percent_format(mantissa=2)},
                                                                                                        "read_only": {"label": "Brokerage","format": percent_format(mantissa=1), "read_only": True}}}),
                    "ncb": hxd.Float(mode="input", default=0, async_input=["rarc_task"], view={"label": "NCB", "format": percent_format(mantissa=2)}),
                    "lta": hxd.Float(mode="input", default=0, async_input=["rarc_task"], view={"label": "LTA", "format": percent_format(mantissa=2)}),
                }),
                "premium_split_all_layers": hxd.Structure(children={
                    "eea": hxd.Float(mode="input", default=0, optionality="optional", view={"label": "EEA", "format": percent_format(mantissa=2)}),
                    "non_eea": hxd.Float(mode="output", view={"label": "Non EEA", "format": percent_format(mantissa=2)}),
                    "crime": hxd.Float(mode="input", default=None, optionality="optional", async_input=["rarc_task"], view={"label": "Crime", "format": percent_format(mantissa=2)}),
                    "pi": hxd.Float(mode="input", default=None, optionality="optional", async_input=["rarc_task"], view={"label": "PI", "format": percent_format(mantissa=2)}),
                    "do": hxd.Float(mode="input", default=None, optionality="optional", async_input=["rarc_task"], view={"label": "D&O", "format": percent_format(mantissa=2)}),
                }),
            }),
        })
    })


def get_towers_options():
    return [f"Tower {i}" for i in range(1, max_towers+1)] + ["NA"]
