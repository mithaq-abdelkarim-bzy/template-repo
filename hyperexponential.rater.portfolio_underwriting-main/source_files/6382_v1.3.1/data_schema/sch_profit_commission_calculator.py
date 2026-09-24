import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format, percent_format, integer_format

def profit_comission_calcs():
    return{
        # Return Period
        "return_period": hx.Int(mode="input", default=None, optionality="optional", view={"label": "Return Period"}),
        # Expected Loss
        "expected_loss": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Expected Loss", "format": {"thousandSeparated": True, "mantissa": 0}}),
        # Underwriter Profit
        "underwriter_profit": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Underwriter Profit", "format": {"thousandSeparated": True, "mantissa": 0}}),
        # PC Payable
        "pc_payable": hx.Float(mode="input", default=None, optionality="optional", view={"label": "PC Payable", "format": {"thousandSeparated": True, "mantissa": 0}}),
        # Parameter 1 used
        "para_one_used": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Parameter 1 used", "format": {"thousandSeparated": True, "mantissa": 0}}),
        # Parameter 2 used
        "para_two_used": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Parameter 2 used", "format": {"thousandSeparated": True, "mantissa": 0}}),
    }

def sch_profit_commission_calculator(cds):
    cds.extend_node_rater_defined(
        "cds", 
        {
            "profit_commission_table": hx.Structure(
                view={"label":"Profit Commission Output Summary"},
                children={
                    "profit_commission_indicator": hx.Str(mode="input", default=None, optionality="optional", options=["Yes", "No"], view={"label": "Profit Commission Indicator"}),
                    "pc_percent": hx.Float(mode="input", default=None, optionality="optional", view={"label": "PC (%)", "format": {"output": "percent", "mantissa":2}}),
                    "uw_exp_perc": hx.Float(mode="input", default=None, optionality="optional", view={"label": "UW Expense (%)", "format": {"output": "percent", "mantissa":2}}),
                    "uw_exp_basis": hx.Str(mode="input", default=None, optionality="optional", options=["Gross Premium", "Gross Net Premium"], view={"label": "UW Expense Basis"}),
                    "additional_features": hx.Str(mode="input", default=None, optionality="optional", options=["Yes", "No"], view={"label": "Additional Features"}),
                    # Attritional
                    "attritional": hx.Structure(
                        view={"label": "Attritional"},
                        children={
                            **profit_comission_calcs(),
                        },
                    ),
                    # Large
                    "large": hx.Structure(
                        view={"label": "Large"},
                        children={
                            **profit_comission_calcs(),
                        },
                    ),
                    # Non-Natural Catastrophe
                    "non_nat_cat": hx.Structure(
                        view={"label": "Non-Natural Catastrophe"},
                        children={
                            **profit_comission_calcs(),
                        },
                    ),
                    # Natural Catastrophe
                    "nat_cat": hx.Structure(
                        view={"label": "Natural Catastrophe"},
                        children={
                            **profit_comission_calcs(),
                        },
                    ),
                    # Total
                    "total": hx.Structure(
                        view={"label": "Total"},
                        children={
                            **profit_comission_calcs(),
                        },
                    ),
                    "sim_outputs": hx.List(
                        mode="input",
                        default_element_count=10,
                        children={
                            # X
                            "x": hx.Int(
                                mode="input",
                                default=None,
                                optionality="optional",
                                view={"label": "x", "format": {"output": "percent", "mantissa": 0}}
                            ),
                            #  p(X<x)
                            "p_x_x": hx.Str(
                                mode="input",
                                default=None,
                                optionality="optional",
                                view={"label": "p(X<x)", "format": {"output": "percent", "mantissa": 0}}
                            ),
                            #  Frequency
                            "frequency": hx.Int(
                                mode="input",
                                default=None,
                                optionality="optional",
                                view={"label": "Frequency"}
                            ),
                            #  Underwriter Profit
                            "und_pro": hx.Int(
                                mode="input",
                                default=None,
                                optionality="optional",
                                view={"label": "Underwriter Profit", "format": {"thousandSeparated": True, "mantissa": 0}}
                            ),
                            #  PC Payable
                            "pc_payable": hx.Int(
                                mode="input",
                                default=None,
                                optionality="optional",
                                view={"label": "PC Payable", "format": {"thousandSeparated": True, "mantissa": 0}}
                            ),
                            #  CDF (Att)
                            "cdf_att": hx.Str(
                                mode="input",
                                default=None,
                                optionality="optional",
                                view={"label": "CDF (Att)", "format": {"output": "percent", "mantissa": 0}}
                            ),
                            #  PDF (Att)
                            "pdf_att": hx.Str(
                                mode="output",
                                view={"label": "PDF (Att)", "format": {"output": "percent", "mantissa": 0}}
                            ),
                            #  CDF (Large)
                            "cdf_lar": hx.Str(
                                mode="input",
                                default=None,
                                optionality="optional",
                                view={"label": "CDF (Large)", "format": {"output": "percent", "mantissa": 0}}
                            ),
                            #  PDF (Large)
                            "pdf_lar": hx.Str(
                                mode="output",
                                view={"label": "PDF (Large)", "format": {"output": "percent", "mantissa": 0}}
                            ),
                            #  CDF (Non Nat Cat)
                            "cdf_non_nat_cat": hx.Str(
                                mode="input",
                                default=None,
                                optionality="optional",
                                view={"label": "CDF (Non Nat Cat)", "format": {"output": "percent", "mantissa": 0}}
                            ),
                            #  PDF (Non Nat Cat)
                            "pdf_non_nat_cat": hx.Str(
                                mode="output",
                                view={"label": "PDF (Non Nat Cat)", "format": {"output": "percent", "mantissa": 0}}
                            ),
                            #  CDF (Cat)
                            "cdf_cat": hx.Str(
                                mode="input",
                                default=None,
                                optionality="optional",
                                view={"label": "CDF (Cat)", "format": {"output": "percent", "mantissa": 0}}
                            ),
                            #  PDF (Cat)
                            "pdf_cat": hx.Str(
                                mode="output",
                                view={"label": "PDF (Cat)", "format": {"output": "percent", "mantissa": 0}}
                            ),
                            #  CDF (Total)
                            "cdf_tot": hx.Str(
                                mode="input",
                                default=None,
                                optionality="optional",
                                view={"label": "CDF (Total)", "format": {"output": "percent", "mantissa": 0}}
                            ),
                            #  PDF (Total)
                            "pdf_tot": hx.Str(
                                mode="output",
                                view={"label": "PDF (Total)", "format": {"output": "percent", "mantissa": 0}}
                            ),
                        }
                    )
                  
                }),
                }
            ) 



