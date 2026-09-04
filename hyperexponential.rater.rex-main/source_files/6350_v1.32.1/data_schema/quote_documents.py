import hx_data_schema as hx
from data_schema.utilities import thousands_format, percent_format, run_schedule_rater_async_tasks

def quote_documents():
    # Section Policy Information
    return  {
        "quote_documents": hx.Structure(children={
            "bpro_outputs": hx.Structure(children={
                "insured_name": hx.Str(mode="output", view={"label": "Insured Name"}, async_input=["generate_quote_doc_task", "generate_climate_doc_task"]),
                "underwriter": hx.Str(mode="output", view={"label": "Underwriter"}, async_input=["generate_quote_doc_task"]),
                "tria": hx.Str(mode="output", view={"label": "TRIA"}, async_input=["generate_quote_doc_task"]),
                "equipment_breakdown": hx.Str(mode="output", view={"label": "Equipment Breakdown"}, async_input=["generate_quote_doc_task"]),
                "insured_from": hx.Date(mode="output", view={"label": "Period of Insurance - From"}, async_input=["generate_quote_doc_task", "generate_climate_doc_task"]),
                "insured_until": hx.Date(mode="output", view={"label": "Period of Insurance - To"}, async_input=["generate_quote_doc_task", "generate_climate_doc_task"]),
                "commission": hx.Float(mode="output", view={"label": "Broker Commission", "format": percent_format(2)}, async_input=["generate_quote_doc_task"]),
                "office": hx.Str(mode="output", view={"label": "Office"}, async_input=["generate_quote_doc_task"]),
                "bpro_ref": hx.Str(mode="output", view={"label": "BPro Ref"}, async_input=["generate_quote_doc_task"]),
                "global_rater_id": hx.Str(mode="output", view={"label": "Global Rater ID"}, async_input=["generate_quote_doc_task"]),
                "limit": hx.Float(mode="output", view={"label": "Limit"}, async_input=["generate_quote_doc_task"]),
                "location_per_schedule": hx.Str(mode="input", optionality="optional", options=["On File with UW", "Per Schedule of Locations", "No"], default=None, view={"label": "Location per Schedule"}, async_input=["generate_quote_doc_task"]),
                "num_locs": hx.Int(mode="output", view={"label": "Number of Locations"}, async_input=["generate_quote_doc_task"]),
                "tiv": hx.Float(mode="output", view={"label": "Total Insured Value (TIV)", "format": thousands_format(mantissa=0)}, async_input=["generate_quote_doc_task"]),
                "itv_per_sqft": hx.Float(mode="output", view={"label": "ITV ($) per SQFT"}, async_input=["generate_quote_doc_task"]),
                "prem_rates": hx.Float(mode="output", view={"label": "Premium Rates", "format": percent_format(mantissa=4)}, async_input=["generate_quote_doc_task"]),
                "peril": hx.Str(mode="input", optionality="optional", options_table="quote_doc_types", options_column="peril", default=None, view={"label": "Peril"}, async_input=["generate_quote_doc_task"]),
                "min_earned_pct": hx.Float(mode="input", default=0, optionality="optional", view={"label": "Minimum Earned Percentage", "format": percent_format()}, async_input=["generate_quote_doc_task"]),
                "min_earned": hx.Int(mode="input", default=0, optionality="optional", view={"label": "Minimum Earned $", "format": thousands_format()}, async_input=["generate_quote_doc_task"]),
                "george_occupancy": hx.Str(mode="input", optionality="optional", default=None, view={"label": "GEORGE Occupancy", "read_only": True}, async_input=["generate_quote_doc_task"], async_output=run_schedule_rater_async_tasks(async_input = False)),
                "bpro_occupancy": hx.Str(mode="output", view={"label": "BPro Occupancy"}, async_input=["generate_quote_doc_task"]),
                "risk_class": hx.Str(mode="input", optionality="optional", default=None, view={"label": "Risk Class", "read_only": True}, async_input=["generate_quote_doc_task"], async_output=run_schedule_rater_async_tasks(async_input = False)),
            }),
            "covered_property": hx.Structure(children={
                "covered_property": hx.Structure(view={"label": "Covered Property"}, children={
                    "option_1": hx.Str(mode="input", optionality="optional", options=covered_property_options(), default=None, view={"label": "Option 1"}, async_input=["generate_quote_doc_task"]),
                    "option_2": hx.Str(mode="input", optionality="optional", options=covered_property_options(), default=None, view={"label": "Option 2"}, async_input=["generate_quote_doc_task"]),
                    "option_3": hx.Str(mode="input", optionality="optional", options=covered_property_options(), default=None, view={"label": "Option 3"}, async_input=["generate_quote_doc_task"]),
                }),
                "additional_covered_property": hx.Structure(view={"label": "Additional Covered Property"}, children={
                    "option_1": hx.Str(mode="input", optionality="optional", default=None, view={"label": "Option 1"}, async_input=["generate_quote_doc_task"]),
                    "option_2": hx.Str(mode="input", optionality="optional", default=None, view={"label": "Option 2"}, async_input=["generate_quote_doc_task"]),
                    "option_3": hx.Str(mode="input", optionality="optional", default=None, view={"label": "Option 3"}, async_input=["generate_quote_doc_task"]),
                })
            }),
            "premium": hx.Structure(children={
                "property_only": hx.Float(mode="output", view={"label": "Property Only", "format": thousands_format()}, async_input=["generate_quote_doc_task"]),
                "tria": hx.Float(mode="output", view={"label": "TRIA", "format": thousands_format()}, async_input=["generate_quote_doc_task"]),
                "equipment_breakdown": hx.Float(mode="output", view={"label": "Equipment Breakdown", "format": thousands_format()}, async_input=["generate_quote_doc_task"]),
                "total_exc_fees": hx.Float(mode="output", view={"label": "Total (exc fees)", "format": thousands_format()}, async_input=["generate_quote_doc_task"]),
                "inspection_fees": hx.Float(mode="input", optionality="optional", default=0, view={"label": "Inspection Fees", "format": thousands_format()}, async_input=["generate_quote_doc_task"]),
            }),
            "subjectivities": hx.Structure(children={
                "loss_run": hx.Bool(mode="input", default=True, optionality="optional", async_input=["generate_quote_doc_task"], view={"label": "Loss Run"}),
                "favourable_inspection": hx.Bool(mode="input", default=True, optionality="optional", async_input=["generate_quote_doc_task"], view={"label": "Favourable Inspection"}),
            }),
            "fixed_sublimits": hx.Structure(children={
                "ordinance_and_law": hx.Structure(view={"label": "Ordinance & Law"}, children={
                    "val": hx.Int(mode="input", optionality="optional", default=None, view={"label": "$"}, async_input=["generate_quote_doc_task"]),
                    "comments": hx.Str(mode="input", default="", optionality="optional", view={"label": "Comments"}, async_input=["generate_quote_doc_task"]),
                }),
                "wind": hx.Structure(view={"label": "Wind"}, children={
                    "val": hx.Int(mode="output", view={"label": "$"}, async_input=["generate_quote_doc_task"]),
                    "comments": hx.Str(mode="input", default="", optionality="optional", view={"label": "Comments"}, async_input=["generate_quote_doc_task"]),
                }),
                "wind_2": hx.Structure(view={"label": "Wind 2"}, children={
                    "val": hx.Int(mode="output", view={"label": "$"}, async_input=["generate_quote_doc_task"]),
                    "comments": hx.Str(mode="input", default="", optionality="optional", view={"label": "Comments"}, async_input=["generate_quote_doc_task"]),
                }),
                "quake": hx.Structure(view={"label": "Quake"}, children={
                    "val": hx.Int(mode="output", view={"label": "$"}, async_input=["generate_quote_doc_task"]),
                    "comments": hx.Str(mode="input", default="", optionality="optional", view={"label": "Comments"}, async_input=["generate_quote_doc_task"]),
                }),
                "quake_2": hx.Structure(view={"label": "Quake 2"}, children={
                    "val": hx.Int(mode="output", view={"label": "$"}, async_input=["generate_quote_doc_task"]),
                    "comments": hx.Str(mode="input", default="", view={"label": "Comments"}, async_input=["generate_quote_doc_task"]),
                }),
                "flood": hx.Structure(view={"label": "Flood"}, children={
                    "val": hx.Int(mode="output", view={"label": "$"}, async_input=["generate_quote_doc_task"]),
                    "comments": hx.Str(mode="input", default="", optionality="optional", view={"label": "Comments"}, async_input=["generate_quote_doc_task"]),
                }),
            }),
            "other_sublimits": hx.List(mode="input", max_element_count=3, children={
                "val": hx.Int(mode="input", default=0, optionality="optional", view={"label": "$"}, async_input=["generate_quote_doc_task"]),
                "comments": hx.Str(mode="input", default="", optionality="optional", view={"label": "Comments"}, async_input=["generate_quote_doc_task"]),
            }),
            "deductibles": hx.List(mode="input", max_element_count=7, async_input=["generate_quote_doc_task"], children={
                "peril": hx.Str(mode="input", optionality="optional", options=["Fire/AOP", "Named Storm", "All Other Wind", "Wind/Hail", "Earthquake", "Flood", "Wildfire", "Other"], default=None, view={"label": "Peril"}, async_input=["generate_quote_doc_task"]),
                "ded_pct": hx.Float(mode="input", optionality="optional", default=None, view={"label": "% Deductible", "format": percent_format()}, async_input=["generate_quote_doc_task"]),
                "ded_min": hx.Int(mode="override", view={"label": "$ Deductible (Minimum)", "format": thousands_format()}, async_input=["generate_quote_doc_task"]),
                "comments": hx.Str(mode="input", default="", optionality="optional", view={"label": "Comments"}, async_input=["generate_quote_doc_task"]),
            }),
            "coinsurance": hx.Structure(children={
                "pd": hx.Structure(view={"label": "PD"}, children={
                    "settlement": hx.Str(mode="input", optionality="optional", options=["Replacement Cost", "Actual Cash Value", "Agreed Value"], default_index=0, async_input=["generate_quote_doc_task"], view={"label": "Settlement"}),
                    "pct": hx.Float(mode="input", default=0, optionality="optional", async_input=["generate_quote_doc_task"], view={"label": "%", "format": percent_format()}),
                }),
                "bi": hx.Structure(view={"label": "BI"}, children={
                    "settlement": hx.Str(mode="input", optionality="optional", options=["Actual Losses Sustained", "1/3 Monthly Limitation", "1/4 Monthly Limitation", "1/6 Monthly Limitation", "1/12 Monthly Limitation"], default_index=0, async_input=["generate_quote_doc_task"], view={"label": "Settlement"}),
                    "pct": hx.Float(mode="input", default=0, optionality="optional", async_input=["generate_quote_doc_task"], view={"label": "%", "format": percent_format()}),
                }),
            }),
            "endorsements": hx.Structure(children=endorsements()),
            "deductibles_override_comment": hx.Str(mode="input", default="", optionality="optional", async_input=["generate_quote_doc_task"]),
            "document": hx.File(mode="output", file_name="quote_doc.docx", async_output=["generate_quote_doc_task"], view={"label": "Document"}),
            "issue_date": hx.Date(mode="input", default="2023-01-01", async_input=["generate_quote_doc_task"], view={"label": "Date of Issue"}),
            "key_location": hx.Str(mode="input", optionality="optional", default=None, async_input=["generate_quote_doc_task"], async_output=run_schedule_rater_async_tasks(async_input = False), view={"read_only": True}),
            "red_date": hx.Str(mode="output", async_input=["generate_quote_doc_task"]),
            "schedule_received_date": hx.Date(mode="input", default="2023-01-01", optionality="optional", async_input=["generate_quote_doc_task"], view={"label": "Schedule Received Date"}),
            "layer": hx.Int(mode="input", default=1, async_input=["generate_quote_doc_task"], view={"label": "Layer to Quote"}),
            "inspection_fees": hx.Float(mode="input", default=0, optionality="optional", async_input=["generate_quote_doc_task"], view={"label": "Inspection Fees"}),
            "quote_comments": hx.Str(mode="input", default="", optionality="optional", async_input=["generate_quote_doc_task"], view={"label": "Quote Comments"}),
            "special_form_flag": hx.Bool(mode="output", async_input=["generate_quote_doc_task"]),
            "manuscript_flag": hx.Bool(mode="output", async_input=["generate_quote_doc_task"]),
            "broker_name": hx.Str(mode="input", default="", optionality="optional", async_input=["generate_quote_doc_task"], view={"label": "Broker Name"}),
            "broker_address": hx.Str(mode="input", default="", optionality="optional", async_input=["generate_quote_doc_task"], view={"label": "Broker Address"}),
            "mailing_address": hx.Str(mode="input", default="", optionality="optional", async_input=["generate_quote_doc_task"], view={"label": "Mailing Address"}),
            "excess": hx.Float(mode="output", async_input=["generate_quote_doc_task"]),
            "written_line": hx.Float(mode="output", async_input=["generate_quote_doc_task"]),
            "including_flood": hx.Str(mode="output", async_input=["generate_quote_doc_task"]),
            "including_quake": hx.Str(mode="output", async_input=["generate_quote_doc_task"]),
            "including_eb": hx.Str(mode="output", async_input=["generate_quote_doc_task"]),
            "show_page": hx.Bool(mode="output"),
            # "coinsurance_": hx.Structure(children={
            #     "real_property": hx.Float(mode="input", default=0, async_input=["generate_quote_doc_task"], view={"label": "Coinsurance: Real Property, Personal Property"}),
            #     "business_interruption": hx.Float(mode="input", default=0, async_input=["generate_quote_doc_task"], view={"label": "Coinsurance: Business Interruption & Extra Expenses"}),
            #     "buildings": hx.Float(mode="input", default=0, async_input=["generate_quote_doc_task"], view={"label": "Coinsurance: Buildings, Personal Property"}),
            #     "business_income": hx.Float(mode="input", default=0, async_input=["generate_quote_doc_task"], view={"label": "Coinsurance: Business Income"}),
            # }),
            # "coinsurance_valuation": hx.Structure(children={
            #     "real_property": hx.Str(mode="input", default="", async_input=["generate_quote_doc_task"], view={"label": "Coinsurance: Real Property, Personal Property"}),
            #     "business_interruption": hx.Str(mode="input", default="", async_input=["generate_quote_doc_task"], view={"label": "Coinsurance: Business Interruption & Extra Expenses"}),
            #     "buildings": hx.Str(mode="input", default="", async_input=["generate_quote_doc_task"], view={"label": "Coinsurance: Buildings, Personal Property"}),
            #     "business_income": hx.Str(mode="input", default="", async_input=["generate_quote_doc_task"], view={"label": "Coinsurance: Business Income"}),
            # }),
        })
    }


def covered_property_options():
    return ["Per Application", "Additional Living Expenses", "Appurtenant Structures", "Back-Up of Sewers", "Builders Risk/Course of Construction", "Buildings Undergoing Renovations", "Business Income", "Business Income Exclusing Ordinary Payroll", "Civil or Military Authority", "Condominium Maintenance Fees", "Contingent Business Interruption", "Contingent Extra Expense", "Contractors Equipment", "Cost of Inventory", "Debris Removal", "Demolition", "Electronic Data Processing Hardware", "Electronic Data Processing Media", "Equipment", "Extra Expense", "Fine Arts", "Food Spoilage", "Furniture & Fixtures", "Gold Cart", "Improvments & Betterments", "Increased Cost of Construction", "Ingress/Egress", "Inventory", "Leasehold Interest", "Loss of Earnings", "Machinery & Equipment", "Maintenance Fees", "Mobile Equipment", "Mold", "Newly Aquired Locations", "Ordinance or Law", "Ordinance or Law - Demolition (Cov B)", "Ordinance or Law - Demolition (Cov B) and Increased Cost of Construction (Cov C) combined", "Ordinance or Law - Increased Cost of Construction (Cov C)", "Ordinance or Law - Undamaged Portion (Cov A)", "Ordinance or Law - Undamaged Portion (Cov A), Demolition (Cov B) and Increased Cost of Construction (Cov C) combined", "Ordinary Payroll", "Outdoor Property (including Trees, Shrubs & Plants)", "Personal Property of Others", "Professional Fees", "Property in the Open", "Real Property", "Real Property Undergoing Renovation", "Rental Property", "Rents", "Service Interruption", "Sign", "Soft Costs", "Spoilage", "Stock", "Tenants Relocation", "Transit", "Trees, Shrubs, & Plants", "Tuition and Fees", "Unnamed Location", "Utility Services - Direct Damage", "Utility Services - Time Element", "Valuable Papers", "Vehicles"]

def endorsement_ds(label):
    return hx.Structure(view={"label": label}, children={
        "yesno": hx.Str(mode="input", default="", optionality="optional", async_input=["generate_quote_doc_task"], view={"label": "Yes/No - Limits/days/fill-in"}),
        "comments": hx.Str(mode="input", default="", optionality="optional", async_input=["generate_quote_doc_task"], view={"label": "Comments"}),
    })

def endorsements():
    return {
        "additional_covered_property": endorsement_ds("Additonal Covered Property"),
        "additional_property_not_covered": endorsement_ds("Additional Property Not Covered"),
        "burglary_or_robbery_safeguards": endorsement_ds("Burglary or Robbery Safeguards"),
        "civil_or_military_authority_ext": endorsement_ds("Civil or Military Authority Ext."),
        "condition_of_coverage": endorsement_ds("Condition of Coverage"),
        "condo_maintenance_fees": endorsement_ds("Condo Maintenance Fees"),
        "condo_association_coverage": endorsement_ds("Condo Association Coverage"),
        "endorcements_condo_maintenance_fees": endorsement_ds("Endorsements Condo Maintenance Fees"),
        "damage_to_roof_structure_limitation": endorsement_ds("Damage To Roof Structure Limitation"),
        "fire_and_explosion": endorsement_ds("Fire And Explosion"),
        "first_tier_wind_counties_and_parishes": endorsement_ds("First Tier Wind Counties and Parishes"),
        "hurricane_minimum_earned_premium": endorsement_ds("Hurricane Minimum Earned Premium"),
        "ingress_egress_extension": endorsement_ds("Ingress / Egress Extension"),
        "limitations_on_coverage_for_roof_surfacing": endorsement_ds("Limitations On Coverage For Roof Surfacing"),
        "ordinance_or_law_increased_period_of_restoration": endorsement_ds("Ordinance or Law - Increased Period of Restoration"),
        "outdoor_property_extension": endorsement_ds("Outdoor Property Extension"),
        "prior_loss_clause": endorsement_ds("Prior Loss Clause"),
        "property_enhancement": endorsement_ds("Property Enhancement"),
        "protective_safeguards": endorsement_ds("Protective Safeguards"),
        "second_tier_wind_counties_and_parishes": endorsement_ds("Second Tier Wind Counties and Parishes"),
        "theft_and_resulting_damage_limitation": endorsement_ds("Theft and Resulting Damage Limitation"),
        "vacancy_permit": endorsement_ds("Vacancy Permit"),
        "vacant_or_unoccupied_limitatin": endorsement_ds("Vacant or Unoccupied Limitation"),
        "values_limitation_clause": endorsement_ds("Values Limitation Clause"),
        "wind_limitation": endorsement_ds("Wind Limitation"),
        "windstorm_or_hail_exclusion": endorsement_ds("Windstorm or Hail Exclusion"),
    }