import hx_data_schema as hx
import data_schema.sch_utilities as utils
from hx import params as hx_params

def sch_exposure_details(cds):
    
    # Aggregate exposure details ----------------------------------------------------------------------
    cds.extend_node_rater_defined("cds/exposure/aggregate", {
        "total_revenue" : hx.Float(mode="input", default=0, optionality = "optional", validation={"min_value": 0}, view={"label": "Total Revenue", "format": utils.thousands_format(0)}, async_input=["rarc_task"]),
        "rateable" : hx.Structure(children={ #IR: is this the correct structure?
            "revenue" : hx.Float(mode="input", default=0, optionality = "optional", validation={"min_value": 0}, view={"label": "Rateable Revenue", "format": utils.thousands_format(0)}, async_input=["rarc_task"]),
            "base_rate" : hx.Float(mode="output", view={"label": "Base Rate", "format": utils.thousands_format(0)}),
        }),
        "nonrateable" : hx.Structure(children={
            "revenue" : hx.Float(mode="output", view={"label": "Non-Rateable Revenue", "format": utils.thousands_format(0)}),
            "base_rate" : hx.Float(mode="output", view={"label": "Base Rate", "format": utils.thousands_format(0)}),
        }),
        "hazard_group" : hx.Str(mode="output", view={"label": "Hazard Class"}),

        "total_base_premium": hx.Float(mode="output", view={"label": "Total Base Premium", "format":utils.thousands_format(0)}),
        "minimum_premium": hx.Float(mode="output"), # Used for algorithm but not displayed in the view. #IR: Maybe move this! Should this be under cds/primary ?

        # Annual TV exposure
        "annual_tv": hx.Structure(children={
            "number_of_productions": hx.Float(mode="input", optionality="optional", default=None, validation={"min_value": 0, "max_value": 100000000000}, view={"label": "Estimated Number of Productions", "format":utils.integer_format(0)}),
            "capped_productions": hx.Float(mode="output", view={"label": "Capped Productions for Rating", "format":utils.integer_format(0)}, async_input=["rarc_task"]),
        }),

        # Individual TV exposure
        "individual_tv": hx.Structure(children={
            "length": hx.Str(mode="input", optionality="optional", default=None, options_table="tbl_indtv_length", options_column="length", view={"label": "Length Type"}, async_input=["rarc_task"]),
            "number_of_episodes": hx.Float(mode="input", optionality="optional", default=None, validation={"min_value": 0, "max_value": 100000000000}, view={"label": "Number of Episodes", "format":utils.integer_format(0)}, async_input=["rarc_task"]),
        }),

        # Individual Film exposure
        "individual_film": hx.Structure(children={
            "exhibition": hx.Str(mode="input", optionality="optional", default=None, options_table="tbl_film_exhibition", options_column="scope_of_release", view={"label": "Scope of Release"}, async_input=["rarc_task"]), #IR: rename this field?
        })
    })

    # Show / Hides -------------------------------------------------------------------------------------
    cds.extend_node_rater_defined("cds", {
        "media_masking": hx.Bool(mode="output"),
        "music_masking": hx.Bool(mode="output"),
        "tvfilm_masking": hx.Bool(mode="output"),
        "individualtv_masking": hx.Bool(mode="output"),
        "annualtv_masking": hx.Bool(mode="output"),
        "individualfilm_masking": hx.Bool(mode="output"),
        "standard_rater_masking": hx.Bool(mode="output"),
        "nonstandard_rater_masking" : hx.Bool(mode="output"),
    })

    # Granular exposures -------------------------------------------------------------------------------
    cds.extend_node_rater_defined("cds/exposure/granular", {        
        "media": hx.Structure(children={
            **{item: hx.Structure(view = {"label": label}, children = {
            "base_rate": hx.Float(mode="input", optionality="optional", default=0, view={"label": "Base Rate","format":utils.percent_format(2)}, async_input=["rarc_task"]),
            "comment": hx.Str(mode="input", optionality="optional", default=None, view={"label": "Comment"}),
            "show_row": hx.Bool(mode = "output", view = {"label": "Show Row"})
            })
            for item, label in zip(hx_params.table_media_exposures["exposure_name"], hx_params.table_media_exposures["exposure_measure"])}   
        }),
        "music": hx.Structure(children={
            **{item: hx.Structure(view = {"label": label}, children = {
            "base_rate": hx.Float(mode="input", optionality="optional", default=0, view={"label": "Base Rate","format":utils.percent_format(2)}, async_input=["rarc_task"]),
            "comment": hx.Str(mode="input", optionality="optional", default=None, view={"label": "Comment"}),
            "show_row": hx.Bool(mode = "output", view = {"label": "Show Row"})
            })
            for item, label in zip(hx_params.table_music_exposures["exposure_name"], hx_params.table_music_exposures["exposure_measure"])}   
        }),
        "tvfilm": hx.Structure(children={
            **{item: hx.Structure(view = {"label": label}, children = {
            "base_rate": hx.Float(mode="input", optionality="optional", default=0, view={"label": "Base Rate","format":utils.percent_format(2)}, async_input=["rarc_task"]),
            "comment": hx.Str(mode="input", optionality="optional", default=None, view={"label": "Comment"}),
            "show_row": hx.Bool(mode = "output", view = {"label": "Show Row"})
            })
            for item, label in zip(hx_params.table_tvfilm_exposures["exposure_name"], hx_params.table_tvfilm_exposures["exposure_measure"])}   
        }),
        "annual_tv": hx.Structure(children={
            # Genre: Turnover and Base Premium etc. for each genre type
            "genre": hx.Structure(view = {"label" : "Genre"}, children={
                **{item: hx.Structure(view ={"label": label}, children = {
                "perc_of_total_turnover":hx.Str(mode = "input", optionality="optional", default=None, view = {"label": "Percentage of Total Turnover","format":utils.percent_format(0)}, async_input=["rarc_task"]),
                "turnover_amount":hx.Float(mode = "output", view = {"label": "Turnover Amount","format":utils.integer_format(0)}),
                "alloc_production_number":hx.Float(mode = "output", view = {"label": "Allocated Production Number","format":utils.thousands_format(2)}),
                "average_premium":hx.Float(mode = "output", view = {"label": "Average Premium","format":utils.thousands_format(0)}),
                "base_premium":hx.Float(mode = "output", view = {"label": "Base Premium","format":utils.thousands_format(0)}),
                })
                for item, label in zip(hx_params.tbl_annualtv_genre["type_name"], hx_params.tbl_annualtv_genre["exhibition_type"])},       
            }),
        }),
    })


    # Individual TV Rating Factors ---------------------------------------------------------------------
    #IR: should these be inside rating_factors?
    cds.extend_node_rater_defined("cds", {
        "individual_tv": hx.Structure(children={
            # Modifiers:
            "selections": hx.Structure(view={"label":"Selection"}, children={
                # Name in line with options table name (for ease of rating algorithm).
                "jurisdiction": hx.Str(mode="input", optionality="optional", default="WW", options_table="tbl_indtv_jurisdiction", options_column="type", view={"label": "Jurisdiction"}),
                "genre": hx.Str(mode="input", optionality="optional", default=None, options_table="tbl_indtv_genre", options_column="exhibition_type", view={"label": "Genre Type"}),
                "policy_period": hx.Str(mode="input", optionality="optional", default="3 year", options_table="tbl_indtv_policy_period", options_column="period", view={"label": "Policy Period Type"}),
                "soundtrack": hx.Str(mode="input", optionality="optional", default="No", options_table="tbl_indtv_soundtrack", options_column="type", view={"label": "Soundtrack Type"}),
                "merchandising": hx.Str(mode="input", optionality="optional", default="No", options_table="tbl_indtv_merchandising", options_column="type", view={"label": "Merchandising Type"}),
                "australian": hx.Str(mode="input", optionality="optional", default="No", options_table="tbl_indtv_australian", options_column="type", view={"label": "Australian Modifier Type"}),
                "coverage_basis": hx.Str(mode="input", optionality="optional", default="Claims Made", options_table="tbl_indtv_coverage_basis", options_column="type", view={"label": "Coverage Basis"}),
                "established_format": hx.Str(mode="input", optionality="optional", default="No", options_table="tbl_indtv_established_format", options_column="type", view={"label": "Previously Aired Modifier"}),
                "primary_broadcast": hx.Str(mode="input", optionality="optional", default="Included", options_table="tbl_indtv_primary_broadcast", options_column="type", view={"label": "Primary Broadcast Modifier"}),
                "lawyers": hx.Str(mode="input", optionality="optional", default="Recognised media lawyers", options_table="tbl_indtv_lawyers", options_column="type", view={"label": "Lawyers Structure"}),
                "webisodes": hx.Str(mode="input", optionality="optional", default="No", options_table="tbl_indtv_webisodes", options_column="type", view={"label": "Webisodes Modifier"}),
            }),
            "modifiers": hx.Structure(view={"label":"Modifier"}, children={
                # Name in line with selections above.
                "jurisdiction": hx.Float(mode="output", view={"label": "", "format":utils.thousands_format(2)}, async_input=["rarc_task"]),
                "policy_period": hx.Float(mode="output", view={"label": "", "format":utils.thousands_format(2)}, async_input=["rarc_task"]),
                "soundtrack": hx.Float(mode="output", view={"label": "", "format":utils.thousands_format(2)}, async_input=["rarc_task"]),
                "merchandising": hx.Float(mode="output", view={"label": "", "format":utils.thousands_format(2)}, async_input=["rarc_task"]),
                "australian": hx.Float(mode="output", view={"label": "", "format":utils.thousands_format(2)}, async_input=["rarc_task"]),
                "coverage_basis": hx.Float(mode="output", view={"label": "", "format":utils.thousands_format(2)}, async_input=["rarc_task"]),
                "established_format": hx.Float(mode="output", view={"label": "", "format":utils.thousands_format(2)}, async_input=["rarc_task"]),
                "primary_broadcast": hx.Float(mode="output", view={"label": "", "format":utils.thousands_format(2)}, async_input=["rarc_task"]),
                "lawyers": hx.Float(mode="output", view={"label": "", "format":utils.thousands_format(2)}, async_input=["rarc_task"]),
                "webisodes": hx.Float(mode="output", view={"label": "", "format":utils.thousands_format(2)}, async_input=["rarc_task"]),
                # For calcs but not in UI:
                "genre": hx.Float(mode="output", view={"label": "Base Premium", "format":utils.thousands_format(2)}, async_input=["rarc_task"]),
                "number_of_episodes": hx.Float(mode="output", view={"label": "", "format":utils.thousands_format(2)}, async_input=["rarc_task"]),
            }),
        })
    })
    
    # Annual TV Rating Factors ---------------------------------------------------------------------
    cds.extend_node_rater_defined("cds", {
        "annual_tv": hx.Structure(children={
            "turnover" : hx.Float(mode="input", default=0, optionality="optional", validation={"min_value": 0}, view={"label": "Turnover", "format": utils.thousands_format(0)}, async_input=["rarc_task"]),
            "annual_budget":  hx.Float(mode="input", optionality="optional", default=None, validation={"min_value": 0}, view={"label": "Average Production Budget", "format":utils.thousands_format(0)}, async_input=["rarc_task"]),
            # Modifiers:
            "selections": hx.Structure(view={"label":"Selection"}, children={
                # Name in line with options table name (for ease of rating algorithm).
                "jurisdiction": hx.Str(mode="input", optionality="optional", default="WW", options_table="tbl_annualtv_jurisdiction", options_column="type", view={"label": "Jurisdiction Type"}),
                "australian": hx.Str(mode="input", optionality="optional", default="No", options_table="tbl_annualtv_australian", options_column="type", view={"label": "Australian Modifier Type"}),
                "lawyers": hx.Str(mode="input", optionality="optional", default="Recognised media lawyers", options_table="tbl_annualtv_lawyers", options_column="type", view={"label": "Lawyers Structure Modifier Type"}),
            }),
            "modifiers": hx.Structure(view={"label":"Modifier"}, children={
                # Name in line with selections above.
                "jurisdiction": hx.Float(mode="output", view={"label": "", "format":utils.thousands_format(2)}, async_input=["rarc_task"]),
                "australian": hx.Float(mode="output", view={"label": "", "format":utils.thousands_format(2)}, async_input=["rarc_task"]),
                "lawyers": hx.Float(mode="output", view={"label": "", "format":utils.thousands_format(2)}, async_input=["rarc_task"]),
            }),
        })
    })

    # Individual Film Rating Factors --------------------------------------------------------------
    cds.extend_node_rater_defined("cds", {
        "individual_film": hx.Structure(children={
            "selections": hx.Structure(view={"label":"Selection"}, children={
                # Name in line with options table name (for ease of rating algorithm).
                "budget": hx.Str(mode="input", optionality="optional", default=None, options_table="tbl_film_budget", options_column="type", view={"label": "Budget"}),
                "cast": hx.Str(mode="input", optionality="optional", default="Standard Profile (well known actor(s), producers &/or director)", options_table="tbl_film_cast", options_column="type", view={"label": "Profile of Actors and/or Producers/Directions"}),
                "appeal": hx.Str(mode="input", optionality="optional", default="Medium", options_table="tbl_film_appeal", options_column="type", view={"label": "Size of Audience/Popularity"}),
                "subject_matter": hx.Str(mode="input", optionality="optional", default=None, options_table="tbl_film_subject_matter", options_column="nature_of_content", view={"label": "Nature of Content"}),
                "jurisdiction": hx.Str(mode="input", optionality="optional", default="WW", options_table="tbl_film_jurisdiction", options_column="type", view={"label": "Jurisdiction"}),
                "foreign_language": hx.Str(mode="input", optionality="optional", default="No", options_table="tbl_film_foreign_language", options_column="type", view={"label": "Foreign Language"}),
                "soundtrack": hx.Str(mode="input", optionality="optional", default="No", options_table="tbl_film_soundtrack", options_column="type", view={"label": "Soundtrack"}),
                "merchandising": hx.Str(mode="input", optionality="optional", default="No", options_table="tbl_film_merchandising", options_column="type", view={"label": "Merchandising"}),
                "policy_period": hx.Str(mode="input", optionality="optional", default="3 year", options_table="tbl_film_policy_period", options_column="period", view={"label": "Policy Period"}),
                "australian": hx.Str(mode="input", optionality="optional", default="No", options_table="tbl_film_australian", options_column="type", view={"label": "Australian"}),
                "coverage_basis": hx.Str(mode="input", optionality="optional", default="Claims Made", options_table="tbl_film_coverage_basis", options_column="type", view={"label": "Coverage Basis"}),
                "established_format": hx.Str(mode="input", optionality="optional", default="No", options_table="tbl_film_established_format", options_column="type", view={"label": "Previously Aired"}),
                "lawyers": hx.Str(mode="input", optionality="optional", default="Recognised media lawyers", options_table="tbl_film_lawyers", options_column="type", view={"label": "Lawyers Structure"}),
            }),
            "modifiers": hx.Structure(view={"label":"Modifier"}, children={
                # Name in line with selections above.
                "budget": hx.Float(mode="output", view={"label": "", "format":utils.thousands_format(2)}, async_input=["rarc_task"]),
                "cast": hx.Float(mode="output", view={"label": "", "format":utils.thousands_format(2)}, async_input=["rarc_task"]),
                "appeal": hx.Float(mode="output", view={"label": "", "format":utils.thousands_format(2)}, async_input=["rarc_task"]),
                "subject_matter": hx.Float(mode="output", view={"label": "", "format":utils.thousands_format(2)}, async_input=["rarc_task"]),
                "jurisdiction": hx.Float(mode="output", view={"label": "", "format":utils.thousands_format(2)}, async_input=["rarc_task"]),
                "foreign_language": hx.Float(mode="output", view={"label": "", "format":utils.thousands_format(2)}, async_input=["rarc_task"]),
                "soundtrack": hx.Float(mode="output", view={"label": "", "format":utils.thousands_format(2)}, async_input=["rarc_task"]),
                "merchandising": hx.Float(mode="output", view={"label": "", "format":utils.thousands_format(2)}, async_input=["rarc_task"]),
                "policy_period": hx.Float(mode="output", view={"label": "", "format":utils.thousands_format(2)}, async_input=["rarc_task"]),
                "australian": hx.Float(mode="output", view={"label": "", "format":utils.thousands_format(2)}, async_input=["rarc_task"]),
                "coverage_basis": hx.Float(mode="output", view={"label": "", "format":utils.thousands_format(2)}, async_input=["rarc_task"]),
                "established_format": hx.Float(mode="output", view={"label": "", "format":utils.thousands_format(2)}, async_input=["rarc_task"]),
                "lawyers": hx.Float(mode="output", view={"label": "", "format":utils.thousands_format(2)}, async_input=["rarc_task"]),
                # For calcs but not in UI:
                "exhibition": hx.Float(mode="output", view={"label": "", "format":utils.thousands_format(2)}, async_input=["rarc_task"]),
            }),
        })
    })
