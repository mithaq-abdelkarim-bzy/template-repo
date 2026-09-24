import hx_data_schema as hx
import data_schema.sch_utilities as utils
import algorithms.rate_constants as const

def sch_tpi_calculations(cds):

    cds.extend_node_rater_defined("cds", {
        "tpi_calculations": hx.Structure(children={
            "selected_option": hx.Int(  mode="input", 
                                        default=1, 
                                        options=[*range(1,const.max_layers + 1)], 
                                        # async_input=['generate_tags_cuap', 'generate_tags_twice'],
                                        view={"label": "Selected Option"}),
            "is_abc": hx.Bool(mode="output", view={"label": "None"}),
            "is_side_a": hx.Bool(mode="output", async_input=["rarc_task"], view={"label": "None"}),
            "sca_base_frequency" : hx.Structure(view={"label": "Sector Base Frequency"}, children={
                "value" :hx.Float(mode="output", view={"label": "Value", "format": {"output": "percent", "mantissa": 2}}),
                "book_average" :hx.Float(mode="output", view={"label": "Book Average", "format": {"output": "percent", "mantissa": 2}}),
                "comment" :hx.Str(mode="output", view={"label": "Comment", "multiline": True}),
                "info" :hx.Str(mode="output", view={"label": "Comment"})
            }),
            "market_cap_factor" : hx.Structure(view={"label": "Market Cap Factor"}, children={
                "value" :hx.Float(mode="output", view={"label": "Value"}),
                "book_average" :hx.Float(mode="output", view={"label": "Book Average"}),
                "comment" :hx.Str(mode="output", view={"label": "Comment", "multiline": True}),
                "info" :hx.Str(mode="output", view={"label": "Comment"})
            }),
            "ipo_factor" : hx.Structure(view={"label": "IPO Factor"}, children={
                "value" :hx.Float(mode="output", view={"label": "Value"}),
                "book_average" :hx.Float(mode="output", view={"label": "Book Average"}),
                "comment" :hx.Str(mode="output", view={"label": "Comment", "multiline": True}),
                "info" :hx.Str(mode="output", view={"label": "Comment"})
            }),
            "minimum_trading_volume_factor" : hx.Structure(view={"label": "Minimum Trading Volume Factor"}, children={
                "value" :hx.Float(mode="output", view={"label": "Value"}),
                "book_average" :hx.Float(mode="output", view={"label": "Book Average"}),
                "comment" :hx.Str(mode="output", view={"label": "Comment", "multiline": True}),
                "info" :hx.Str(mode="output", view={"label": "Comment"})
            }),
            "volatility_of_trading_factor" : hx.Structure(view={"label": "Volatility of Trading During Downturn Factor"}, children={
                "value" :hx.Float(mode="output", view={"label": "Value"}),
                "book_average" :hx.Float(mode="output", view={"label": "Book Average"}),
                "comment" :hx.Str(mode="output", view={"label": "Comment", "multiline": True}),
                "info" :hx.Str(mode="output", view={"label": "Comment"})
            }),
            "execs_under_age_50_factor" : hx.Structure(view={"label": "Percentage of Executives under age 50 Factor"}, children={
                "value" :hx.Float(mode="output", view={"label": "Value"}),
                "book_average" :hx.Float(mode="output", view={"label": "Book Average"}),
                "comment" :hx.Str(mode="output", view={"label": "Comment", "multiline": True}),
                "info" :hx.Str(mode="output", view={"label": "Comment"})
            }), 
            "years_in_business_factor" : hx.Structure(view={"label": "Years in Business Factor"}, children={
                "value" :hx.Float(mode="output", view={"label": "Value"}),
                "book_average" :hx.Float(mode="output", view={"label": "Book Average"}),
                "comment" :hx.Str(mode="output", view={"label": "Comment", "multiline": True}),
                "info" :hx.Str(mode="output", view={"label": "Comment"})
            }),      
            "capiq_total_factor" : hx.Structure(view={"label": "Total Factor"}, children={
                "value" :hx.Float(mode="output", view={"label": "Value"}),
                "book_average" :hx.Float(mode="output", view={"label": "Book Average"}),
                "comment" :hx.Str(mode="output", view={"label": "Comment", "multiline": True}),
                "info" :hx.Str(mode="output", view={"label": "Comment"})
            }),
            "freq_sca_after_capiq" : hx.Structure(view={"label": "Frequency After CapIQ Score"}, children={
                "value" :hx.Float(mode="output", view={"label": "Value", "format": {"output": "percent", "mantissa": 2}}),
                "book_average" :hx.Float(mode="output", view={"label": "Book Average", "format": {"output": "percent", "mantissa": 2}}),
                "comment" :hx.Str(mode="output", view={"label": "Comment", "multiline": True}),
                "info" :hx.Str(mode="output", view={"label": "Comment"})
            }),
            "freq_sca_after_overrides" : hx.Structure(view={"label": "Frequency After Sector SCA Overrides"}, children={
                "value" :hx.Float(mode="output", view={"label": "Value", "format": {"output": "percent", "mantissa": 2}}),
                "book_average" :hx.Float(mode="output", view={"label": "Book Average", "format": {"output": "percent", "mantissa": 2}}),
                "comment" :hx.Str(mode="output", view={"label": "Comment", "multiline": True}),
                "info" :hx.Str(mode="output", view={"label": "Comment"})
            }),
            "freq_sca_after_modifiers" : hx.Structure(view={"label": "Frequency After Modifiers"}, children={
                "value" :hx.Float(mode="output", view={"label": "Value", "format": {"output": "percent", "mantissa": 2}}),
                "book_average" :hx.Float(mode="output", view={"label": "Book Average", "format": {"output": "percent", "mantissa": 2}}),
                "comment" :hx.Str(mode="output", view={"label": "Comment", "multiline": True}),
                "info" :hx.Str(mode="output", view={"label": "Comment"})
            }),
            "ground_up_sca_dismissal" : hx.Structure(view={"label": "Expected Ground-up SCA Dismissal Cost"}, children={
                "value" :hx.Float(mode="output", view={"label": "Value", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "book_average" :hx.Float(mode="output", view={"label": "Book Average", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "comment" :hx.Str(mode="output", view={"label": "Comment", "multiline": True}),
                "info" :hx.Str(mode="output", view={"label": "Comment"})
            }),
            "sca_loss_to_layer" : hx.Structure(view={"label": "Expected SCA Loss to Layer"}, children={
                "value" :hx.Float(mode="output", view={"label": "Value", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "book_average" :hx.Float(mode="output", view={"label": "Book Average", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "comment" :hx.Str(mode="output", view={"label": "Comment", "multiline": True}),
                "info" :hx.Str(mode="output", view={"label": "Comment"})
            }),
            "sca_dismissal_rate" : hx.Structure(view={"label": "SCA Dismissal Rate"}, children={
                "value" :hx.Float(mode="output", view={"label": "Value", "format": {"output": "percent", "mantissa": 1}}),
                "book_average" :hx.Float(mode="output", view={"label": "Book Average"}),
                "comment" :hx.Str(mode="output", view={"label": "Comment", "multiline": True}),
                "info" :hx.Str(mode="output", view={"label": "Comment"})
            }),
            "sca_loss_cost" : hx.Structure(view={"label": "SCA Loss Cost"}, children={
                "value" :hx.Float(mode="output", view={"label": "Value", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "book_average" :hx.Float(mode="output", view={"label": "Book Average"}),
                "comment" :hx.Str(mode="output", view={"label": "Comment", "multiline": True}),
                "info" :hx.Str(mode="output", view={"label": "Comment"})
            }),
            "non_sca_loss_cost" : hx.Structure(view={"label": "Non-SCA Loss Cost"}, children={
                "value" :hx.Float(mode="output", view={"label": "Value", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "book_average" :hx.Float(mode="output", view={"label": "Book Average"}),
                "comment" :hx.Str(mode="output", view={"label": "Comment", "multiline": True}),
                "info" :hx.Str(mode="output", view={"label": "Comment"})
            }),
            "cat_load" : hx.Structure(view={"label": "Non-Modelled Claim Type Load"}, children={
                "value" :hx.Float(mode="output", view={"label": "Value", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "book_average" :hx.Float(mode="output", view={"label": "Book Average"}),
                "comment" :hx.Str(mode="output", view={"label": "Comment", "multiline": True}),
                "info" :hx.Str(mode="output", view={"label": "Comment"})
            }),
            "abc_loss_cost" : hx.Structure(view={"label": "ABC Loss Cost"}, children={
                "value" :hx.Float(mode="output", view={"label": "Value", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "book_average" :hx.Float(mode="output", view={"label": "Book Average"}),
                "comment" :hx.Str(mode="output", view={"label": "Comment", "multiline": True}),
                "info" :hx.Str(mode="output", view={"label": "Comment"})
            }),
            "dic_adjustment" : hx.Structure(view={"label": "DIC Adjustment"}, children={
                "value" :hx.Float(mode="output", view={"label": "Value"}),
                "book_average" :hx.Float(mode="output", view={"label": "Book Average"}),
                "comment" :hx.Str(mode="output", view={"label": "Comment", "multiline": True}),
                "info" :hx.Str(mode="output", view={"label": "Comment"})
            }),
            "bankruptcy_load" : hx.Structure(view={"label": "Bankruptcy Load"}, children={
                "value" :hx.Float(mode="output", view={"label": "Value"}),
                "book_average" :hx.Float(mode="output", view={"label": "Book Average"}),
                "comment" :hx.Str(mode="output", view={"label": "Comment", "multiline": True}),
                "info" :hx.Str(mode="output", view={"label": "Comment"})
            }),
            "side_a_loss_cost" : hx.Structure(view={"label": "Side A Loss Cost"}, children={
                "value" :hx.Float(mode="output", view={"label": "Value", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "book_average" :hx.Float(mode="output", view={"label": "Book Average"}),
                "comment" :hx.Str(mode="output", view={"label": "Comment", "multiline": True}),
                "info" :hx.Str(mode="output", view={"label": "Comment"})
            }),
            "net_premium" : hx.Structure(view={"label": "Net Premium"}, children={
                "value" :hx.Float(mode="output", view={"label": "Value", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "book_average" :hx.Float(mode="output", view={"label": "Book Average"}),
                "comment" :hx.Str(mode="output", view={"label": "Comment", "multiline": True}),
                "info" :hx.Str(mode="output", view={"label": "Comment"})
            }),
            "profit" : hx.Structure(view={"label": "Profit"}, children={
                "value" :hx.Float(mode="output", view={"label": "Value", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "book_average" :hx.Float(mode="output", view={"label": "Book Average"}),
                "comment" :hx.Str(mode="output", view={"label": "Comment", "multiline": True}),
                "info" :hx.Str(mode="output", view={"label": "Comment"})
            }),
            "roc" : hx.Structure(view={"label": "ROC"}, children={
                "value" :hx.Float(mode="output", view={"label": "Value", "format": {"output": "percent", "mantissa": 2}}),
                "book_average" :hx.Float(mode="output", view={"label": "Book Average"}),
                "comment" :hx.Str(mode="output", view={"label": "Comment", "multiline": True}),
                "info" :hx.Str(mode="output", view={"label": "Comment"})
            }),
            "technical_premium" : hx.Structure(view={"label": "Technical Premium"}, children={
                "value" :hx.Float(mode="output", view={"label": "Value", "format": {"thousandSeparated": True, "mantissa": 0}}),
                "book_average" :hx.Float(mode="output", view={"label": "Book Average"}),
                "comment" :hx.Str(mode="output", view={"label": "Comment", "multiline": True}),
                "info" :hx.Str(mode="output", view={"label": "Comment"})
            }),
            "tpi" : hx.Structure(view={"label": "TPI"}, children={
                "value" :hx.Float(mode="output", view={"label": "Value", "format": {"output": "percent", "mantissa": 2}}),
                "book_average" :hx.Float(mode="output", view={"label": "Book Average"}),
                "comment" :hx.Str(mode="output", view={"label": "Comment", "multiline": True}),
                "info" :hx.Str(mode="output", view={"label": "Comment"})
            })                       
        })    
    })

    # cds.override_node_properties('cds/tpi_calculations/selected_option',{'async_input':['generate_tags_cuap','generate_tags_twice']})