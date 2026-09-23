import hx_data_schema as hxd

from algorithms.rate_utilities import get_field_options
from libraries.common_data_schema.data_schema.utilities import percent_format, thousands_format


def sch_exposure_details(cds):
    cds.extend_node_rater_defined("cds/exposure/aggregate", {
        "total_amounts": hxd.Structure(view={"label": "Total Amounts"}, children={
            "employees": hxd.Int(mode="input", default=0, async_input=["rarc_task"], view={"label": "Employees", "format": thousands_format()}),
            "revenues": hxd.Int(mode="input", default=0, async_input=["rarc_task"], view={"label": "Gross Revenue", "format": thousands_format()}),
            "assets": hxd.Int(mode="input", default=0, async_input=["rarc_task"], view={"label": "Assets", "format": thousands_format()}),
            "aum": hxd.Float(mode="input", default=None, optionality="optional", async_input=["rarc_task"], view={"label": "Total AUM", "format": thousands_format()}),
        }),
        "market_cap": hxd.Int(mode="input", default=None, optionality="optional", async_input=["rarc_task"], view={"label": "Market Cap (if public)", "format": thousands_format()}),
        "market_cap_us": hxd.Float(mode="input", default=0, async_input=["rarc_task"], view={"label": "Market Cap % In US Exchanges", "format": percent_format(mantissa=2)})
    })

    cds.extend_node_rater_defined("cds/exposure/granular", {
        "regions": hxd.Structure(children={
            "splits_entered_as": hxd.Structure(view={"label": "Splits Entered As"}, children={
                "employees": hxd.Str(mode="input", options=get_field_options("exposure_details", "splits_entered_as/employees"), default="Percentage", async_input=["rarc_task"], view={"label": "Employees"}),
                "revenues": hxd.Str(mode="input", options=get_field_options("exposure_details", "splits_entered_as/revenues"), default="Percentage", async_input=["rarc_task"], view={"label": "Gross Revenue"}),
                "assets": hxd.Str(mode="input", options=get_field_options("exposure_details", "splits_entered_as/assets"), default="Percentage", async_input=["rarc_task"], view={"label": "Assets"}),
            }),
            "regions_list": hxd.Structure(children=generate_regions()),
        }),
        "commited_capital": hxd.Float(mode="input", default=None, optionality="optional", view={"label": "Commited Capital", "info": "Enter amount of FUM", "format": thousands_format()}),
        "invested_capital": hxd.Float(mode="input", default=None, optionality="optional", view={"label": "Invested Capital", "info": "Enter as % of FUM", "format": percent_format()}),
        "no_of_directorship": hxd.Float(mode="input", default=None, optionality="optional", view={"label": "Number of outside directorship positions"}),
        "transactions_av_value": hxd.Float(mode="input", default=None, optionality="optional", view={"label": "Average value of transactions", "format": percent_format()}),
        "transactions_av_fee": hxd.Float(mode="input", default=None, optionality="optional", view={"label": "Average fee income from transactions", "format": percent_format()}),
        "investor_split_type": hxd.Structure(children={
            "institutional": hxd.Structure(view={"label": "Institutional / HNW / Accredited"}, children={
                "percent": hxd.Float(mode="input", default=None, optionality="optional", async_input=["rarc_task"], view={"label": "% Split", "format": percent_format()})
            }),
            "retail": hxd.Structure(view={"label": "Retail"}, children={
                "percent": hxd.Float(mode="input", default=None, optionality="optional", async_input=["rarc_task"], view={"label": "% Split", "format": percent_format()})
            }),
            "other": hxd.Structure(view={"label": "Other"}, children={
                "percent": hxd.Float(mode="input", default=None, optionality="optional", async_input=["rarc_task"], view={"label": "% Split", "format": percent_format()})
            })
        }),
        "investor_split_region": hxd.Structure(children={
            "region_1": hxd.Structure(view={"label": "Region 1"}, children={
                "region": hxd.Str(mode="input", default="Europe", optionality="optional", options_data="../../../../../../non_cds/exposure_details/investor_split/region_dropdown", options_field="region", async_input=["rarc_task"], view={"label": "Region"}),
                "percent": hxd.Float(mode="input", default=None, optionality="optional", async_input=["rarc_task"], view={"label": "% Split", "format": percent_format()})
            }),
            "region_2": hxd.Structure(view={"label": "Region 2"}, children={
                "region": hxd.Str(mode="input", default="USA", optionality="optional", options_data="../../../../../../non_cds/exposure_details/investor_split/region_dropdown", options_field="region", async_input=["rarc_task"], view={"label": "Region"}),
                "percent": hxd.Float(mode="input", default=None, optionality="optional", async_input=["rarc_task"], view={"label": "% Split", "format": percent_format()})
            }),
            "region_3": hxd.Structure(view={"label": "Region 3"}, children={
                "region": hxd.Str(mode="input", default="RoW", optionality="optional", options_data="../../../../../../non_cds/exposure_details/investor_split/region_dropdown", options_field="region", async_input=["rarc_task"], view={"label": "Region"}),
                "percent": hxd.Float(mode="input", default=None, optionality="optional", async_input=["rarc_task"], view={"label": "% Split", "format": percent_format()})
            }),
        }),
        "revenue_split_admin": hxd.Structure(children={
            "est_companies": hxd.Structure(view={"label": "Establishment/admin of companies"}, children=get_revenue_split_fields("input")),
            "est_trusts": hxd.Structure(view={"label": "Establishment/admin of trusts"}, children=get_revenue_split_fields("input")),
            "outside_board": hxd.Structure(view={"label": "Outside board positions"}, children=get_revenue_split_fields("input")),
            "legal_advice": hxd.Structure(view={"label": "Legal advice"}, children=get_revenue_split_fields("input")),
            "accountancy": hxd.Structure(view={"label": "Accountancy"}, children=get_revenue_split_fields("input")),
            "tax": hxd.Structure(view={"label": "Tax"}, children=get_revenue_split_fields("input")),
            "other": hxd.Structure(view={"label": "Other"}, children=get_revenue_split_fields("input")),
        }),
        "revenue_split_banks": hxd.Structure(children={
            "interest": hxd.Structure(view={"label": "Interest Income"}, children=get_revenue_split_fields("input")),
            "fee": hxd.Structure(view={"label": "Fee Income"}, children=get_revenue_split_fields("input")),
            "trading": hxd.Structure(view={"label": "Trading Income"}, children=get_revenue_split_fields("input")),
            "other": hxd.Structure(view={"label": "Other Income"}, children=get_revenue_split_fields("input")),
        }),
        "premium_split": hxd.Structure(children={
            "life": hxd.Structure(view={"label": "Life insurance"}, children=get_revenue_split_fields("input")),
            "pc": hxd.Structure(view={"label": "P&C insurance"}, children=get_revenue_split_fields("input")),
            "personal": hxd.Structure(view={"label": "Personal lines"}, children=get_revenue_split_fields("input")),
            "commercial": hxd.Structure(view={"label": "Commercial lines"}, children=get_revenue_split_fields("input")),
            "healthcare": hxd.Structure(view={"label": "Medical/Healthcare"}, children=get_revenue_split_fields("input")),
            "ripc": hxd.Structure(view={"label": "Reinsurance"}, children=get_revenue_split_fields("input")),
            "other": hxd.Structure(view={"label": "Other"}, children=get_revenue_split_fields("input")),
        }),
        "revenue_split_brokers": hxd.Structure(children={
            "institutional_advisory": hxd.Structure(view={"label": "Institutional advisory"}, children=get_revenue_split_fields("input")),
            "institutional_execution": hxd.Structure(view={"label": "Institutional execution only"}, children=get_revenue_split_fields("input")),
            "retail_advisory": hxd.Structure(view={"label": "Retail advisory"}, children=get_revenue_split_fields("input")),
            "retail_execution": hxd.Structure(view={"label": "Retail execution only"}, children=get_revenue_split_fields("input")),
            "retail_discretionary": hxd.Structure(view={"label": "Retail discretionary"}, children=get_revenue_split_fields("input")),
            "other": hxd.Structure(view={"label": "Other"}, children=get_revenue_split_fields("input")),
        }),
        "revenue_split_exchanges": hxd.Structure(children={
            "exchange": hxd.Structure(view={"label": "Exchange"}, children=get_revenue_split_fields("input")),
            "listing": hxd.Structure(view={"label": "Listing"}, children=get_revenue_split_fields("input")),
            "clear_settlement": hxd.Structure(view={"label": "Clearing & Settlement"}, children=get_revenue_split_fields("input")),
            "depositary": hxd.Structure(view={"label": "Depositary"}, children=get_revenue_split_fields("input")),
            "other": hxd.Structure(view={"label": "Other"}, children=get_revenue_split_fields("input")),
        }),
        "revenue_split_investment": hxd.Structure(children={
            "investment_management": hxd.Structure(view={"label": "Investment Management"}, children=get_revenue_split_fields("input")),
            "personal_services": hxd.Structure(view={"label": "Personal Services"}, children=get_revenue_split_fields("input")),
            "legal_advisory_services": hxd.Structure(view={"label": "Legal & Advisory Services"}, children=get_revenue_split_fields("input")),
            "family_group_services": hxd.Structure(view={"label": "Family Group Services"}, children=get_revenue_split_fields("input")),
            "other": hxd.Structure(view={"label": "Other"}, children=get_revenue_split_fields("input")),
        })
    })


def get_missing_amounts_booleans():
    entities = ["employees", "revenues", "assets"]
    switches = ["value", "percent"]
    result = {}
    for switch in switches:
        switch_object = {}        
        for entity in entities:            
            switch_object = {
                **switch_object,
                f"{entity}": hxd.Structure(
                    children = {
                        "show_missing": hxd.Bool(mode="output"),
                        "hide_missing": hxd.Bool(mode="output")
                    }
                )
            }
        result = {
                **result,
                f"{switch}": hxd.Structure(children = switch_object)
        }
    return {"toggles": hxd.Structure(children = result)}


def sch_exposure_details_non_cds():
    return {
        "exposure_details": hxd.Structure(children={
            "no_of_locations_show": hxd.Bool(mode="output"),
            "client_info_public_show": hxd.Bool(mode="output"),
            "market_cap_us_show": hxd.Bool(mode="output"),
            "client_info_show": hxd.Bool(mode="output"),
            "exposure_details_show": hxd.Bool(mode="output"),
            "total_aum_show": hxd.Bool(mode="output"),
            "capital_show": hxd.Bool(mode="output"),
            "no_of_directorship_show": hxd.Bool(mode="output"),
            "transactions_av_show": hxd.Bool(mode="output"),
            "credit_rating_show": hxd.Bool(mode="output"),
            "regions": hxd.Structure(children={
                "show": hxd.Bool(mode="output"),
                "is_value": hxd.Structure(children={
                    "employees": hxd.Bool(mode="output"),
                    "revenues": hxd.Bool(mode="output"),
                    "assets": hxd.Bool(mode="output")
                }),
                "is_percent": hxd.Structure(children={
                    "employees": hxd.Bool(mode="output"),
                    "revenues": hxd.Bool(mode="output"),
                    "assets": hxd.Bool(mode="output")
                }),
                "check_on_totals": hxd.Structure(view={"label": "Check On Totals"}, children={
                    "value": hxd.Structure(children={
                        "employees": hxd.Str(mode="output", view={"label": "Employees"}),
                        "revenues": hxd.Str(mode="output", view={"label": "Gross Revenue"}),
                        "assets": hxd.Str(mode="output", view={"label": "Assets"})
                    }),
                    "percent": hxd.Structure(children={
                        "employees": hxd.Str(mode="output", view={"label": "Employees"}),
                        "revenues": hxd.Str(mode="output", view={"label": "Gross Revenue"}),
                        "assets": hxd.Str(mode="output", view={"label": "Assets"})
                    }),
                }),
                "missing_amounts": hxd.Structure(view={"label": "Missing Amounts"}, children={
                    **get_region_fields("output", "output"), 
                    **get_missing_amounts_booleans(),
                    "missing_amount_text": hxd.Str(mode="input", default="Missing Amounts", view={
                        "options": {"read_only_option": {"read_only": True}}
                     })
                }),
            }),
            "investor_split": hxd.Structure(children={
                "show": hxd.Bool(mode="output"),
                "region_dropdown": hxd.List(mode="output", children={"region": hxd.Str(mode="output")}),
                "type_total": hxd.Structure(view={"label": "Total"}, children={
                    "percent": hxd.Float(mode="output", view={"label": "Total", "format": percent_format()})
                }),
                "region_total": hxd.Structure(view={"label": "Total"}, children={
                    "percent": hxd.Float(mode="output", view={"label": "Total", "format": percent_format()})
                })
            }),
            "revenue_split_admin": hxd.Structure(children={
                "show": hxd.Bool(mode="output"),
                "total": hxd.Structure(view={"label": "Total"}, children=get_revenue_split_fields("output"))
            }),
            "revenue_split_banks": hxd.Structure(children={
                "show": hxd.Bool(mode="output"),
                "total": hxd.Structure(view={"label": "Total"}, children=get_revenue_split_fields("output"))
            }),
            "premium_split": hxd.Structure(children={
                "show": hxd.Bool(mode="output"),
                "total": hxd.Structure(view={"label": "Total"}, children=get_revenue_split_fields("output"))
            }),
            "revenue_split_brokers": hxd.Structure(children={
                "show": hxd.Bool(mode="output"),
                "total": hxd.Structure(view={"label": "Total"}, children=get_revenue_split_fields("output"))
            }),
            "revenue_split_exchanges": hxd.Structure(children={
                "show": hxd.Bool(mode="output"),
                "total": hxd.Structure(view={"label": "Total"}, children=get_revenue_split_fields("output"))
            }),
            "revenue_split_investment": hxd.Structure(children={
                "show": hxd.Bool(mode="output"),
                "total": hxd.Structure(view={"label": "Total"}, children=get_revenue_split_fields("output"))
            })
        })
    }


def generate_regions():
    regions_list = (("africa", "Africa"), ("arab_states", "Arab States"), ("asia", "Asia"), ("oceania", "Oceania"),
                    ("europe", "Europe"), ("former_soviet_republics", "Former Soviet Republics"), ("usa", "USA"),
                    ("canada", "Canada"), ("south_latin_america", "South/Latin America"), ("caribbean", "Caribbean"),
                    ("row","RoW"))

    regions = dict()
    for region, label in regions_list:
        regions[region] = hxd.Structure(view={"label": label}, children=get_region_fields("input", "input"))

    return regions


def get_region_fields(value_mode, percent_mode):
    entities = (("employees", "Employees"), ("revenues", "Gross Revenue"), ("assets", "Assets"))
    view_dict = {}

    value_props = {"mode": value_mode, 'async_input': ["rarc_task"] }
    if value_mode == "input":
        value_props["default"] = 0
    else:
        view_dict["options"] = {"missing_values": {"style_cell": "hx-bad"}}

    percent_props = {"mode": percent_mode, 'async_input': ["rarc_task"] }
    if percent_mode == "input":
        percent_props["default"] = 0

    value_fields = {}
    percent_fields = {}
    for entity, label in entities:
        if value_mode == "input":
            view_dict["label"] = label
        value_field = hxd.Float(**value_props, view={**view_dict, "format": thousands_format()})
        if entity == "employees":
            value_field = hxd.Int(**value_props, view={**view_dict, "format": thousands_format()})

        value_fields[entity] = value_field
        percent_fields[entity] = hxd.Float(**percent_props, view={**view_dict, "format": percent_format(mantissa=2)})

    return {"value": hxd.Structure(children=value_fields), "percent": hxd.Structure(children=percent_fields)}


def get_revenue_split_fields(amount_mode):
    amount_props = {"mode": amount_mode}
    if amount_mode == "input":
        amount_props["default"] = None
        amount_props["optionality"] = "optional"
        amount_props["async_input"] = ["rarc_task"]

    return {
        "amount": hxd.Float(**amount_props, view={"label": "Amounts", "format": thousands_format()}),
        "percent": hxd.Float(mode="output", view={"label": "Percentages", "format": percent_format(mantissa=2)}),
    }
