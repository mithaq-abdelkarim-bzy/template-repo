# v0.5.0
import hx_data_schema as hx
import data_schema.sch_utilities as utils
from data_schema.sch_rate_change import rarc_task_name
from algorithms.data_schema.sch_rater_defined import RARC_COVERAGE_USE, RARC_INSURED_ASSET_USE
from algorithms.rate_constants                import NUMBER_OF_SIMS
if RARC_COVERAGE_USE:
    from algorithms.data_schema.sch_rater_defined import COVERAGES_LIST


ec_coverages_dict = {"all_risks"                :"All Risks",
                     "adverse_weather"          :"Adverse Weather",
                     "earthquake"               :"Earthquake",
                     "windstorm"                :"Windstorm",
                     "wildfire"                 :"Wildfire",
                     "terrorism"                :"Terrorism",
                     "cyber"                    :"Cyber",
                     "national_mourning"        :"National Mourning",
                     "riots_and_civil_commotion":"Riots and Civil Commotion",
                     "strike"                   :"Strike",
                     "war"                      :"War",
                     "catastrophic_non_app"     :"Catastrophic Non-App",
                     "ec_total"                 :"Event Cancellation Total" }



def cvg_financials():
    return {    "net_el_usd":   hx.Float(mode="output",    view={"label": "Expected Loss USD",                  "format": utils.thousands_format(0)}),
                "net_prem_usd": hx.Float(mode="output",    view={"label": "GN Benchmark Premium USD",           "format": utils.thousands_format(0)}),
                "net_el":       hx.Float(mode="output",    view={"label": "Expected Loss",                      "format": utils.thousands_format(0)},  async_input=["task_simulation"]),
                "net_prem":     hx.Float(mode="output",    view={"label": "GN Benchmark Premium",               "format": utils.thousands_format(0)}),
                "net_el_mod":   hx.Float(mode="output",    view={"label": "Expected Loss after UW Adj",         "format": utils.thousands_format(0)}),
                "net_prem_mod": hx.Float(mode="output",    view={"label": "GN Benchmark Premium after UW Adj",  "format": utils.thousands_format(0)}) }


def cvg_adjustments():
    return {    "uw_adj_min":  hx.Float(mode="output",                                       view={"label": "Minimum",          "format": utils.percent_format(0)}),
                "uw_adj_max":  hx.Float(mode="output",                                       view={"label": "Maximum",          "format": utils.percent_format(0)}),
                "uw_adj_sel":  hx.Float(mode="input", default=0,     optionality="required", view={"label": "Selected",         "format": utils.percent_format(0)},  async_input=['rarc_task']),
                "uw_adj_fin":  hx.Float(mode="output",                                       view={"label": "Selected - Final", "format": utils.percent_format(0)},  async_input=["task_simulation"]),
                "uw_comment":  hx.Str(  mode="input", default=None,  optionality="optional", view={"label": "UW Comment"}                     )}



def ec_coverage(coverage):
    bool_trigger    = coverage in ["Cyber", "National Mourning","Catastrophic Non-App"]
    bool_delegates  = coverage in ["Catastrophic Non-App"]
    bool_specifics  = coverage not in ["All Risks", "Event Cancellation Total"]
    bool_x_total    = coverage not in ["Event Cancellation Total"]

    lst_cyb_trigger = ["LMA5591", "LMA5592"]                        
    lst_nm_trigger  = ["Less than 70 y/o", "Greater than 70 y/o"]   
    lst_cat_non_app_trigger = ["Common accident", "Illness", "Travel delay", "Common accident / Illness", "Common accident / Travel delay", "Illness / Travel delay", "Common accident / Illness / Travel delay"] # NB not actually used in rating algorithm
    lst_trigger     = (         lst_cyb_trigger          if coverage =="Cyber" 
                        else    lst_cat_non_app_trigger  if coverage =="Catastrophic Non-App" 
                        else    lst_nm_trigger                                                  )

    return {**({} if not bool_specifics else {"covered":  hx.Bool( mode="input", default=True,  optionality="required", view={"label": "Covered" },                                             async_input=['rarc_task',"task_simulation"])}),
            **({} if not bool_specifics else {"sublimit": hx.Float(mode="input", default=None,  optionality="optional", view={"label": "Sublimit",       "format": utils.thousands_format(0)},  async_input=['rarc_task',"task_simulation"])}),
            **({} if not bool_trigger   else {"trigger":  hx.Str(  mode="input", default=None,  optionality="optional", view={"label": "Trigger" }, options=lst_trigger,                        async_input=['rarc_task'])}),
            **({} if not bool_delegates else {"delegates":hx.Float(mode="input", default=None,  optionality="optional", view={"label": "% of Delegates", "format": utils.percent_format(0)},    async_input=['rarc_task'])}),
            **({} if not bool_x_total   else cvg_adjustments()),
            **cvg_financials()}


def sch_exposure_details(cds):
    
    lst_gender = ["Male", "Female", "Unknown"]
    lst_curve  = ["Attritional", "Large"]
    lst_layers = list(range(1, 7))
    grp_ec     = "Event Cancellation sub-coverages"

    # For aggregate exposure e.g. total revenue, sum insured etc. please add to the aggregate exposures node
    cds.extend_node_rater_defined("cds/exposure/aggregate", {
        # PLACEHOLDER value used in experience rating, the experience rating should connect to the total exposure value of the model
        "exposure": hx.Float(mode="output", view={"label": "Agg Exposure", "format": utils.thousands_format(0)}),
        
    })

    # For granular exposure lists e.g. aircrafts, hospitals etc, please add to the granular node
    cds.extend_node_rater_defined("cds/exposure/granular", {        
        # NOTE: Replace the below with your models exposures
        "event_cancel"  : hx.Structure(children={
            "event_type":              hx.Str(  mode="input", default=None,       optionality="optional", view={"label": "Type of Event"},           options_table="tbl_event_rates", options_column="event_type"   ,   async_input=['rarc_task']),
            "exposure_curve":          hx.Str(  mode="input", default="Standard", optionality="required", view={"label": "Exposure Curve Selected"}, options_table="tbl_exposure_curve_attr", options_column="curve",   async_input=['rarc_task']),
            "exposure_curve_comments": hx.Str(  mode="input", default=None,       optionality="optional", view={"label": "Exposure Curve Comments"},                                                                    async_input=['rarc_task']),
            "exposure_curve_warning":  hx.Str(  mode="output",                                            view={"label": "Exposure Curve Warning"}),

            "experience":              hx.Bool( mode="input", default=False,      optionality="required", view={"label": "Experience"}                                                                              ,   async_input=['rarc_task']),
            "experience_ratio":        hx.Str(  mode="input", default=None,       optionality="optional", view={"label": "Incurred Loss Ratio"},     options_table="tbl_experience_adj_lr", options_column="loss_ratio",async_input=['rarc_task']),
            "experience_factor":       hx.Float(mode="output",                                            view={"label": "Experience Factor"}     ),

            "ncb":                     hx.Bool( mode="input", default=False,      optionality="required", view={"label": "NCB"},                                                                                        async_input=['rarc_task']),
            "ncb_offered":             hx.Float(mode="input", default=None,       optionality="optional", view={"label": "NCB % Offered", "format": utils.percent_format(0)},                                           async_input=['rarc_task']),
            "ncb_factor":              hx.Float(mode="output",                                            view={"label": "NCB Factor"}      ),

            "agg_tiv_calc":            hx.Float(mode="output",                                            view={"label": "Aggregate TIV Calculated", "format": utils.thousands_format(0)} ),
            "agg_tiv_uw":              hx.Float(mode="input", default=None,       optionality="optional", view={"label": "Aggregate TIV Entered",    "format": utils.thousands_format(0)} ),
            "agg_tiv_warning":         hx.Str(  mode="output",                                            view={"label": "Aggregate TIV Warning"}                                         ),



            "base_coverages"  : hx.Structure(children={    k: hx.Structure(view={"label": v}, children=ec_coverage(v))    for k,v in ec_coverages_dict.items()   }),

            "terrorism_terms" : hx.Structure(children={ 
                "city_load":     hx.Str( mode="input", default=None,  optionality="optional", view={"label": "City Load"}        ,options_table="tbl_event_terror_cityload",     options_column="city_load",        async_input=['rarc_task']),
                "event_profile": hx.Str( mode="input", default=None,  optionality="optional", view={"label": "Profile of Events"},options_table="tbl_event_terror_eventprofile", options_column="event_profile",    async_input=['rarc_task']),
                "time_distance": hx.Str( mode="input", default=None,  optionality="optional", view={"label": "Time/Distance"},    options_table="tbl_event_terror_timedistance", options_column="time_distance",    async_input=['rarc_task']),
                "terrorism_show":hx.Bool(mode="output")
            }),

            "national_mourning" : hx.Structure(children={ 
                "cover_level":     hx.Str(  mode="input", default="Mourning Period",optionality="optional", view={"label": "Level of Cover"}        ,options_table="lst_event_national_mourning_level_of_cover",   options_column="level_of_cover",async_input=['rarc_task']),
                "mourning_period": hx.Int(  mode="input", default=10,               optionality="optional", view={"label": "Mourning Period", "format": utils.thousands_format(0)},                                                                async_input=['rarc_task']),

                "over_75" :       hx.List(mode="input",  async_input=["rarc_task"], default_element_count=3, children={
                    "label":            hx.Str(  mode="output",                                        view={"label": "Label"}),
                    "include":          hx.Bool( mode="input", default=False,  optionality="required", view={"label": "Model?"},                                                                                                        async_input=['rarc_task']),
                    "name":             hx.Str(  mode="input", default=None,   optionality="optional", view={"label": "Name", "options": {"uw_view": {"read_only": False}}},                                                            async_input=['rarc_task']),
                    "country":          hx.Str(  mode="input", default=None,   optionality="optional", view={"label": "Country", "options": {"uw_view": {"read_only": False}}}, options_table="lst_country", options_column="country",  async_input=['rarc_task']),
                    "gender":           hx.Str(  mode="input", default=None,   optionality="optional", view={"label": "Gender", "options": {"uw_view": {"read_only": False}} }, options=lst_gender,                                     async_input=['rarc_task']),
                    "date_of_birth":    hx.Date( mode="input",  default=None,  optionality="optional", view={"label": "Date of Birth", "options": {"uw_view": {"read_only": False}}},                                                   async_input=['rarc_task']),
                    "age":              hx.Float(mode="output",                                        view={"label": "Age",                          "format": utils.thousands_format(2)}),
                    "prob_die":         hx.Float(mode="output",                                        view={"label": "Annual\nProbability\nDeath",   "format": utils.percent_format(3)}),
                    "prob_live":        hx.Float(mode="output",                                        view={"label": "Annual\nProbability\nSurvive", "format": utils.percent_format(3)}),
                    "mod_affluence":    hx.Float(mode="input", default=1,      optionality="required", view={"label": "Affluence\nAdjustment",        "format": utils.percent_format(0)},                                               async_input=['rarc_task']),
                    "mod_health":       hx.Float(mode="input", default=1,      optionality="required", view={"label": "Health\nAdjustment",           "format": utils.percent_format(0)},                                               async_input=['rarc_task']),
                    "prob_die_mod":     hx.Float(mode="output",                                        view={"label": "Adjusted Annual\nProbability\nDeath",   "format": utils.percent_format(3)}),
                    "prob_live_mod":    hx.Float(mode="output",                                        view={"label": "Adjusted Annual\nProbability\nSurvive", "format": utils.percent_format(3)}),
                    "check":            hx.Str(  mode="output",                                        view={"label": "Check"})
                }),

                "under_75" :      hx.Structure(children={ 
                    "label":            hx.Str(  mode="output",                                        view={"label": "Label"}),
                    "include":          hx.Bool( mode="input", default=False,  optionality="required", view={"label": "Model?"},                                                                                                        async_input=['rarc_task']),
                    # "name":             hx.Str(  mode="output",                                        view={"label": "Name"}), 
                    "country":          hx.Str(  mode="output",                                        view={"label": "Country"}),
                    # "gender":           hx.Str(  mode="output",                                        view={"label": "Gender" }),
                    "age":              hx.Float(mode="output",                                        view={"label": "Age",                          "format": utils.thousands_format(2)}),
                    "prob_die":         hx.Float(mode="output",                                        view={"label": "Annual\nProbability\nDeath",   "format": utils.percent_format(3)}),
                    "prob_live":        hx.Float(mode="output",                                        view={"label": "Annual\nProbability\nSurvive", "format": utils.percent_format(3)}),
                    "mod_affluence":    hx.Float(mode="input", default=1,      optionality="required", view={"label": "Affluence\nAdjustment",        "format": utils.percent_format(0)},                                               async_input=['rarc_task']),
                    "mod_health":       hx.Float(mode="input", default=1,      optionality="required", view={"label": "Health\nAdjustment",           "format": utils.percent_format(0)},                                               async_input=['rarc_task']),
                    "prob_die_mod":     hx.Float(mode="output",                                        view={"label": "Adjusted Annual\nProbability\nDeath",   "format": utils.percent_format(3)}),
                    "prob_live_mod":    hx.Float(mode="output",                                        view={"label": "Adjusted Annual\nProbability\nSurvive", "format": utils.percent_format(3)}),
                    "check":            hx.Str(  mode="output",                                        view={"label": "Check"})
                }),


                "bespoke_1" :       hx.Structure(children={
                    "label":            hx.Str(  mode="output",                                        view={"label": "Label"}),
                    "include":          hx.Bool( mode="input", default=False,           optionality="required", view={"label": "Model?"},                                                                                               async_input=['rarc_task']),
                    "name":             hx.Str(  mode="input", default="Trump",         optionality="optional", view={"label": "Name", "options": {"uw_view": {"read_only": True}}},                                                    async_input=['rarc_task']),
                    "country":          hx.Str(  mode="input", default="US",            optionality="optional", view={"label": "Country", "options": {"uw_view": {"read_only": True}}}, options_table="lst_country", options_column="country", async_input=['rarc_task']),
                    "gender":           hx.Str(  mode="input", default="Male",          optionality="optional", view={"label": "Gender", "options": {"uw_view": {"read_only": True}} }, options=lst_gender,                             async_input=['rarc_task']),
                    "date_of_birth":    hx.Date( mode="input",  default="1946-06-14",   optionality="optional", view={"label": "Date of Birth", "options": {"uw_view": {"read_only": True}}},                                           async_input=['rarc_task']),
                    "age":              hx.Float(mode="output",                                        view={"label": "Age",                          "format": utils.thousands_format(2)}),
                    "prob_die":         hx.Float(mode="output",                                        view={"label": "Annual\nProbability\nDeath",   "format": utils.percent_format(3)}),
                    "prob_live":        hx.Float(mode="output",                                        view={"label": "Annual\nProbability\nSurvive", "format": utils.percent_format(3)}),
                    "mod_affluence":    hx.Float(mode="input", default=1,      optionality="required", view={"label": "Affluence\nAdjustment",        "format": utils.percent_format(0)},                                               async_input=['rarc_task']),
                    "mod_health":       hx.Float(mode="input", default=1,      optionality="required", view={"label": "Health\nAdjustment",           "format": utils.percent_format(0)},                                               async_input=['rarc_task']),
                    "prob_die_mod":     hx.Float(mode="output",                                        view={"label": "Adjusted Annual\nProbability\nDeath",   "format": utils.percent_format(3)}),
                    "prob_live_mod":    hx.Float(mode="output",                                        view={"label": "Adjusted Annual\nProbability\nSurvive", "format": utils.percent_format(3)}),
                    "check":            hx.Str(  mode="output",                                        view={"label": "Check"})
                }),

                "bespoke_2" :       hx.Structure(children={
                    "label":            hx.Str(  mode="output",                                        view={"label": "Label"}),
                    "include":          hx.Bool( mode="input", default=False,           optionality="required", view={"label": "Model?"},                                                                                               async_input=['rarc_task']),
                    "name":             hx.Str(  mode="input", default="Charles III",   optionality="optional", view={"label": "Name", "options": {"uw_view": {"read_only": True}}},                                                    async_input=['rarc_task']),
                    "country":          hx.Str(  mode="input", default="UK",            optionality="optional", view={"label": "Country", "options": {"uw_view": {"read_only": True}}}, options_table="lst_country", options_column="country", async_input=['rarc_task']),
                    "gender":           hx.Str(  mode="input", default="Male",          optionality="optional", view={"label": "Gender", "options": {"uw_view": {"read_only": True}} }, options=lst_gender,                             async_input=['rarc_task']),
                    "date_of_birth":    hx.Date( mode="input",  default="1948-11-14",   optionality="optional", view={"label": "Date of Birth", "options": {"uw_view": {"read_only": True}}},                                           async_input=['rarc_task']),
                    "age":              hx.Float(mode="output",                                        view={"label": "Age",                          "format": utils.thousands_format(2)}),
                    "prob_die":         hx.Float(mode="output",                                        view={"label": "Annual\nProbability\nDeath",   "format": utils.percent_format(3)}),
                    "prob_live":        hx.Float(mode="output",                                        view={"label": "Annual\nProbability\nSurvive", "format": utils.percent_format(3)}),
                    "mod_affluence":    hx.Float(mode="input", default=1,      optionality="required", view={"label": "Affluence\nAdjustment",        "format": utils.percent_format(0)},                                               async_input=['rarc_task']),
                    "mod_health":       hx.Float(mode="input", default=1,      optionality="required", view={"label": "Health\nAdjustment",           "format": utils.percent_format(0)},                                               async_input=['rarc_task']),
                    "prob_die_mod":     hx.Float(mode="output",                                        view={"label": "Adjusted Annual\nProbability\nDeath",   "format": utils.percent_format(3)}),
                    "prob_live_mod":    hx.Float(mode="output",                                        view={"label": "Adjusted Annual\nProbability\nSurvive", "format": utils.percent_format(3)}),
                    "check":            hx.Str(  mode="output",                                        view={"label": "Check"})
                }),
            }),


            # relating to the simulation task
            "simulation"  : hx.Structure(children={
                "last_run_status"           : hx.Str( mode="output", view={"label": "Status - Last run of Simulation"},       async_output=["task_simulation"]),
                "last_run_date"             : hx.Str( mode="output", view={"label": "Date - Last run of Simulation"},         async_output=["task_simulation"]),
                "last_run_value"            : hx.Str( mode="output", view={"label": "Check Value - Last run of Simulation"},  async_output=["task_simulation"]),
                "calc_run_value"            : hx.Str( mode="output", view={"label": "Check Value - Prospective Simulation"},  async_input =["task_simulation"]),
                "check_run_consistent"      : hx.Str( mode="output", view={"label": "Does simulation need to be rerun:"}),
                "num_sims"                  : hx.Int( mode="input",  default=NUMBER_OF_SIMS, optionality="optional",  view={"label": "Number of Sims", "format": utils.thousands_format(0)},  async_input =["task_simulation"]),
                "total_det_loss_before_agg" : hx.Float(mode="output",                               view={"label": "Deterministic Loss Amount - uncapped",    "format": utils.thousands_format(0)}),
                "total_det_loss_after_agg"  : hx.Float(mode="output",                               view={"label": "Deterministic Loss Amount - capped","format": utils.thousands_format(0)}), # adj: exper_adj * ncb_adj  * agg_discount_pct * ded_discount_pct
                "total_det_loss_after_agg_adj": hx.Float(mode="output",                             view={"label": "Deterministic Loss Amount - capped & adj","format": utils.thousands_format(0)}), # adj: exper_adj * ncb_adj  * agg_discount_pct * ded_discount_pct

                "total_sim_claim_number"              : hx.Float(mode="input", default=0,                              view={"label": "Total Claim Number - Simulation Output","format":utils.thousands_format(2)},  async_output=[{"task":"task_simulation", "reset": False}]),
                "total_sim_claim_number_override"     : hx.Float(mode="input", default=None, optionality= "optional",  view={"label": "Total Claim Number  - Override",       "format": utils.thousands_format(2)},  async_input=["task_simulation"]),
                "total_sim_claim_number_calc"         : hx.Float(mode="output",                                        view={"label": "Total Claim Number - Before Override", "format": utils.thousands_format(2)},  async_input=["task_simulation"]),
                "total_sim_loss_before_agg"           : hx.Float(mode="input", default=0,                     view={"label": "Simulated Loss Amount - uncapped",              "format": utils.thousands_format(0)},  async_output=["task_simulation"]),
                "total_sim_loss_after_agg"            : hx.Float(mode="input", default=0,                     view={"label": "Simulated Loss Amount - capped",                "format": utils.thousands_format(0)},  async_output=["task_simulation"]),
                "total_sim_loss_after_agg_adj"        : hx.Float(mode="output",                               view={"label": "Simulated Loss Amount - capped & adj",          "format": utils.thousands_format(0)}),
                "total_sim_loss_after_agg_adj_scaled" : hx.Float(mode="output",                               view={"label": "Simulated Loss Amount - capped & adj & scaled", "format": utils.thousands_format(0)}),

                "sim_agg_adj"                         : hx.Float(mode="output",                               view={"label": "Simulation Agg Adj, incorp. wgt to simulation", "format": utils.percent_format(3)}),
                "sim_error"                           : hx.Float(mode="output",                               view={"label": "Simulation Error vs Deterministic",             "format": utils.percent_format(3)}),
                "simulation_required"                 : hx.Float(mode="output",                               view={"label": "Simulation Required"}),


            }),



            "factors" : hx.Structure(children={ 
                "fx_rate":                  hx.Float(mode="output",   view={"label": "fx_rate"}                         ),
                "cyber_rate":               hx.Float(mode="output",   view={"label": "cyber_rate"}                      ),
                "national_mourning_rate":   hx.Float(mode="output",   view={"label": "national_mourning_rate"}          ),
                "terrorism_city_load":      hx.Float(mode="output",   view={"label": "terrorism_city_load"}             ),
                "terrorism_event_profile":  hx.Float(mode="output",   view={"label": "terrorism_event_profile"}         ),
                "terrorism_time_distance":  hx.Float(mode="output",   view={"label": "terrorism_time_distance"}         ),
                "cap_tiv_total_usd":        hx.Float(mode="output",   view={"label": "cap_tiv_total_usd"}               ),
                "cap_tiv_to_agg_pct":       hx.Float(mode="output",   view={"label": "cap_tiv_to_agg_pct"}              ),
                "cap_tiv_to_ded_pct":       hx.Float(mode="output",   view={"label": "cap_tiv_to_ded_pct"}              ),
                "agg_discount_pct":         hx.Float(mode="output",   view={"label": "agg_discount_pct"}                ),
                "ded_discount_pct":         hx.Float(mode="output",   view={"label": "ded_discount_pct"}                ),
                "exp_cve_attr_b":           hx.Float(mode="output",   view={"label": "exp_cve_attr_b"},  async_input=["task_simulation"]  ),
                "exp_cve_attr_g":           hx.Float(mode="output",   view={"label": "exp_cve_attr_g"},  async_input=["task_simulation"]  ),
                "exp_cve_eq_b":             hx.Float(mode="output",   view={"label": "exp_cve_eq_b"},    async_input=["task_simulation"]  ),
                "exp_cve_eq_g":             hx.Float(mode="output",   view={"label": "exp_cve_eq_g"},    async_input=["task_simulation"]  ),
                "exp_cve_ws_b":             hx.Float(mode="output",   view={"label": "exp_cve_ws_b"},    async_input=["task_simulation"]  ),
                "exp_cve_ws_g":             hx.Float(mode="output",   view={"label": "exp_cve_ws_g"},    async_input=["task_simulation"]  ),
                "freq_adj":                 hx.Float(mode="output",   view={"label": "freq_adj"} ),

            }),


            "events": hx.List(mode="input",  async_input=["rarc_task", "task_simulation"], default_element_count=20, children={
                "event_name":hx.Str( mode="input", default=None, optionality="optional", view={"label": "Event Name"},                                                                          async_input=['rarc_task']),
                "country":   hx.Str( mode="input", default=None, optionality="optional", view={"label": "Country"},     options_table="tbl_ihs_country_codes",       options_column="country",  async_input=['rarc_task']),
                "state":     hx.Str( mode="input", default=None, optionality="optional", view={"label": "State (US)"},  options_table="tbl_country_us_states_codes", options_column="state",    async_input=['rarc_task']),
                "date_start":hx.Date(mode="input", default=None, optionality="optional", view={"label": "Date Start"},                                                                          async_input=['rarc_task']),
                "date_end":  hx.Date(mode="input", default=None, optionality="optional", view={"label": "Date End"},                                                                            async_input=['rarc_task']),
                "tiv":       hx.Float(mode="input",default=None, optionality="optional", view={"label": "Insured Value", "format": utils.thousands_format(0)},                                  async_input=['rarc_task',"task_simulation"]),
                "venue":     hx.Str( mode="input", default=None, optionality="optional", view={"label": "Venue"},       options_table="tbl_event_venue",            options_column="venue",     async_input=['rarc_task']),
                "ihs_terrorism":                    hx.Float(mode="input",default=None, optionality="optional",  view={"label": "IHS Terrorism",                 "format": utils.thousands_format(4)}, async_output=["task_fetch_ihs_data"], async_input=['rarc_task']),
                "ihs_riots_and_civil_commotion":    hx.Float(mode="input",default=None, optionality="optional",  view={"label": "IHS Riots and Civil Commotion", "format": utils.thousands_format(4)}, async_output=["task_fetch_ihs_data"], async_input=['rarc_task']),
                "ihs_strike":                       hx.Float(mode="input",default=None, optionality="optional",  view={"label": "IHS Strike",                    "format": utils.thousands_format(4)}, async_output=["task_fetch_ihs_data"], async_input=['rarc_task']),
                "ihs_war":                          hx.Float(mode="input",default=None, optionality="optional",  view={"label": "IHS War",                       "format": utils.thousands_format(4)}, async_output=["task_fetch_ihs_data"], async_input=['rarc_task']),
                "check":     hx.Str( mode="output",                            async_input=["task_simulation"],  view={"label": "Check"}),
                "country_code"                        : hx.Str(  mode="output", async_input=["task_fetch_ihs_data"], view={"label": "Country Code OR Region"}),
                "date_cover_start"                    : hx.Date( mode="output",                                  view={"label": "Cover Start Date (calculated)"}),
                "mths_diff"                           : hx.Float(mode="output",                                  view={"label": "Absolute months between Cover Start Date and End Date (round up)", "format": utils.thousands_format(4)}),
                "venue_multiplier"                    : hx.Float(mode="output",                                  view={"label": "Venue Multiplier", "format": utils.thousands_format(4)}),
                "tiv_usd"                             : hx.Float(mode="output", async_input=["task_simulation"], view={"label": "TIV USD", "format": utils.thousands_format(4)}),
                "cap_tiv_usd"                         : hx.Float(mode="output",                                  view={"label": "TIV in Limit (USD)", "format": utils.thousands_format(4)}),
                "m_terrorism"                         : hx.Float(mode="output",                                  view={"label": "Terrorism m", "format": utils.thousands_format(4)}),
                "c_terrorism"                         : hx.Float(mode="output",                                  view={"label": "Terrorism C", "format": utils.thousands_format(4)}),
                "m_riots_and_civil_commotion"         : hx.Float(mode="output",                                  view={"label": "Riot m", "format": utils.thousands_format(4)}),
                "c_riots_and_civil_commotion"         : hx.Float(mode="output",                                  view={"label": "Riot C", "format": utils.thousands_format(4)}),
                "m_strike"                            : hx.Float(mode="output",                                  view={"label": "Strike m", "format": utils.thousands_format(4)}),
                "c_strike"                            : hx.Float(mode="output",                                  view={"label": "Strike C", "format": utils.thousands_format(4)}),
                "m_war"                               : hx.Float(mode="output",                                  view={"label": "War m ", "format": utils.thousands_format(4)}),
                "c_war"                               : hx.Float(mode="output",                                  view={"label": "War C", "format": utils.thousands_format(4)}),
                "base_rate_adverse_weather"           : hx.Float(mode="output",                                  view={"label": "Base Rate Adverse Weather", "format": utils.thousands_format(4)}),
                "pat_adverse_weather"                 : hx.Str(  mode="output",                                  view={"label": "Pattern Adverse Weather"}),
                "base_rate_windstorm"                 : hx.Float(mode="output",                                  view={"label": "Base Rate Windstorm", "format": utils.thousands_format(4)}),
                "pat_windstorm"                       : hx.Str(  mode="output",                                  view={"label": "Pattern Windstorm"}),
                "base_rate_wildfire"                  : hx.Float(mode="output",                                  view={"label": "Base Rate Wildfire", "format": utils.thousands_format(4)}),
                "pat_wildfire"                        : hx.Str(  mode="output",                                  view={"label": "Pattern Wildfire"}),
                "base_rate_earthquake"                : hx.Float(mode="output",                                  view={"label": "Base Rate Earthquake", "format": utils.thousands_format(4)}),
                "pat_earthquake"                      : hx.Str(  mode="output",                                  view={"label": "Pattern Earthquake"}),
                "season_adverse_weather"              : hx.Float(mode="output",                                  view={"label": "Seasonality Adjustment Adverse Weather", "format": utils.thousands_format(4)}),
                "season_windstorm"                    : hx.Float(mode="output",                                  view={"label": "Seasonality Adjustment Windstorm", "format": utils.thousands_format(4)}),
                "season_wildfire"                     : hx.Float(mode="output",                                  view={"label": "Seasonality Adjustment Wildfire", "format": utils.thousands_format(4)}),
                "nm_o75_sx"                           : hx.Float(mode="output",                                  view={"label": "Over 75s Annual Survival Probability", "format": utils.thousands_format(4)}),
                "nm_o75_sx_mod"                       : hx.Float(mode="output",                                  view={"label": "Over 75s Annual Survival Probability (adjusted)", "format": utils.thousands_format(4)}),
                "nm_u75_sx"                           : hx.Float(mode="output",                                  view={"label": "Under 75s Annual Survival Probability", "format": utils.thousands_format(4)}),
                "nm_sx"                               : hx.Float(mode="output",                                  view={"label": "Cohort Annual Survival Rate", "format": utils.thousands_format(4)}),
                "nm_qx"                               : hx.Float(mode="output",                                  view={"label": "Cohort Annual Mortality Rate", "format": utils.thousands_format(4)}),
                "nm_qx_daily"                         : hx.Float(mode="output",                                  view={"label": "Daily Mortality Rate", "format": utils.thousands_format(4)}),
                "nm_u75_sx_mod"                       : hx.Float(mode="output",                                  view={"label": "Under 75s Annual Survival Probability (adjusted)", "format": utils.thousands_format(4)}),
                "nm_sx_mod"                           : hx.Float(mode="output",                                  view={"label": "Cohort Annual Survival Rate (adjusted)", "format": utils.thousands_format(4)}),
                "nm_qx_mod"                           : hx.Float(mode="output",                                  view={"label": "Cohort Annual Mortality Rate (adjusted)", "format": utils.thousands_format(4)}),
                "nm_qx_daily_mod"                     : hx.Float(mode="output",                                  view={"label": "Daily Mortality Rate (adjusted)", "format": utils.thousands_format(4)}),
                "nm_death_rate"                       : hx.Float(mode="output",                                  view={"label": "Death Day Rate", "format": utils.thousands_format(4)}),
                "nm_funeral_rate"                     : hx.Float(mode="output",                                  view={"label": "Funeral Day Rate", "format": utils.thousands_format(4)}),
                "nm_mourning_rate"                    : hx.Float(mode="output",                                  view={"label": "Mourning Period Rate", "format": utils.thousands_format(4)}),
                "nm_rate"                             : hx.Float(mode="output",                                  view={"label": "National Mourning Selected Rate", "format": utils.thousands_format(4)}),
                "nm_death_rate_mod"                   : hx.Float(mode="output",                                  view={"label": "Death Day Rate (adjusted)", "format": utils.thousands_format(4)}),
                "nm_funeral_rate_mod"                 : hx.Float(mode="output",                                  view={"label": "Funeral Day Rate (adjusted)", "format": utils.thousands_format(4)}),
                "nm_mourning_rate_mod"                : hx.Float(mode="output",                                  view={"label": "Mourning Period Rate (adjusted)", "format": utils.thousands_format(4)}),
                "nm_rate_mod"                         : hx.Float(mode="output",                                  view={"label": "National Mourning Selected Rate (adjusted)", "format": utils.thousands_format(4)}),
                "rate_all_risks"                      : hx.Float(mode="output", async_input=["task_simulation"], view={"label": "Total Rate Standard Cover", "format": utils.thousands_format(4)}),
                "rate_adverse_weather"                : hx.Float(mode="output", async_input=["task_simulation"], view={"label": "Total Rate Adverse Weather", "format": utils.thousands_format(4)}),
                "rate_windstorm"                      : hx.Float(mode="output", async_input=["task_simulation"], view={"label": "Total Rate Windstorm", "format": utils.thousands_format(4)}),
                "rate_wildfire"                       : hx.Float(mode="output", async_input=["task_simulation"], view={"label": "Total Rate Wildfire", "format": utils.thousands_format(4)}),
                "rate_earthquake"                     : hx.Float(mode="output", async_input=["task_simulation"], view={"label": "Total Rate Earthquake", "format": utils.thousands_format(4)}),
                "rate_cyber"                          : hx.Float(mode="output", async_input=["task_simulation"], view={"label": "Total Rate Cyber", "format": utils.thousands_format(4)}),
                "rate_national_mourning"              : hx.Float(mode="output", async_input=["task_simulation"], view={"label": "Total Rate National Mourning", "format": utils.thousands_format(4)}),
                "rate_national_mourning_mod"          : hx.Float(mode="output", async_input=["task_simulation"], view={"label": "Total Rate National Mourning (after uw mods)", "format": utils.thousands_format(4)}),
                "rate_terrorism"                      : hx.Float(mode="output", async_input=["task_simulation"], view={"label": "Total Rate Terrorism", "format": utils.thousands_format(4)}),
                "rate_riots_and_civil_commotion"      : hx.Float(mode="output", async_input=["task_simulation"], view={"label": "Total Rate Riots and Civil Commotion", "format": utils.thousands_format(4)}),
                "rate_strike"                         : hx.Float(mode="output", async_input=["task_simulation"], view={"label": "Total Rate Strike", "format": utils.thousands_format(4)}),
                "rate_war"                            : hx.Float(mode="output", async_input=["task_simulation"], view={"label": "Total Rate War", "format": utils.thousands_format(4)}),
                "rate_catastrophic_non_app"           : hx.Float(mode="output", async_input=["task_simulation"], view={"label": "Total Rate Catastrophic Non - App", "format": utils.thousands_format(4)}),
                "el_usd_total"                        : hx.Float(mode="output",                                  view={"label": "FGU Expected Loss Total", "format": utils.thousands_format(4)}),
                "net_el_usd_total"                    : hx.Float(mode="output",                                  view={"label": "Layer 1 Expected Loss Total", "format": utils.thousands_format(4)}),
                "struct_pct_all_risks"                : hx.Float(mode="output",                                  view={"label": "Layer 1 FLC Standard Cover", "format": utils.thousands_format(4)}),
                "el_usd_all_risks"                    : hx.Float(mode="output",                                  view={"label": "FGU Expected Loss Standard Cover", "format": utils.thousands_format(4)}),
                "net_el_usd_all_risks"                : hx.Float(mode="output",                                  view={"label": "Layer 1 Expected Loss Standard Cover", "format": utils.thousands_format(4)}),
                "struct_pct_terrorism"                : hx.Float(mode="output",                                  view={"label": "Layer 1 FLC Terrorism", "format": utils.thousands_format(4)}),
                "el_usd_terrorism"                    : hx.Float(mode="output",                                  view={"label": "FGU Expected Loss Terrorism", "format": utils.thousands_format(4)}),
                "net_el_usd_terrorism"                : hx.Float(mode="output",                                  view={"label": "Layer 1 Expected Loss Terrorism", "format": utils.thousands_format(4)}),
                "struct_pct_cyber"                    : hx.Float(mode="output",                                  view={"label": "Layer 1 FLC Cyber", "format": utils.thousands_format(4)}),
                "el_usd_cyber"                        : hx.Float(mode="output",                                  view={"label": "FGU Expected Loss Cyber", "format": utils.thousands_format(4)}),
                "net_el_usd_cyber"                    : hx.Float(mode="output",                                  view={"label": "Layer 1 Expected Loss Cyber", "format": utils.thousands_format(4)}),
                "struct_pct_national_mourning"        : hx.Float(mode="output",                                  view={"label": "Layer 1 FLC National Mourning", "format": utils.thousands_format(4)}),
                "el_usd_national_mourning"            : hx.Float(mode="output",                                  view={"label": "FGU Expected Loss National Mourning", "format": utils.thousands_format(4)}),
                "net_el_usd_national_mourning"        : hx.Float(mode="output",                                  view={"label": "Layer 1 Expected Loss National Mourning", "format": utils.thousands_format(4)}),
                "struct_pct_riots_and_civil_commotion": hx.Float(mode="output",                                  view={"label": "Layer 1 FLC Riots and Civil Commotion", "format": utils.thousands_format(4)}),
                "el_usd_riots_and_civil_commotion"    : hx.Float(mode="output",                                  view={"label": "FGU Expected Loss Riots and Civil Commotion", "format": utils.thousands_format(4)}),
                "net_el_usd_riots_and_civil_commotion": hx.Float(mode="output",                                  view={"label": "Layer 1 Expected Loss Riots and Civil Commotion", "format": utils.thousands_format(4)}),
                "struct_pct_strike"                   : hx.Float(mode="output",                                  view={"label": "Layer 1 FLC Strike", "format": utils.thousands_format(4)}),
                "el_usd_strike"                       : hx.Float(mode="output",                                  view={"label": "FGU Expected Loss Strike", "format": utils.thousands_format(4)}),
                "net_el_usd_strike"                   : hx.Float(mode="output",                                  view={"label": "Layer 1 Expected Loss Strike", "format": utils.thousands_format(4)}),
                "struct_pct_war"                      : hx.Float(mode="output",                                  view={"label": "Layer 1 FLC War", "format": utils.thousands_format(4)}),
                "el_usd_war"                          : hx.Float(mode="output",                                  view={"label": "FGU Expected Loss War", "format": utils.thousands_format(4)}),
                "net_el_usd_war"                      : hx.Float(mode="output",                                  view={"label": "Layer 1 Expected Loss War", "format": utils.thousands_format(4)}),
                "struct_pct_catastrophic_non_app"     : hx.Float(mode="output",                                  view={"label": "Layer 1 FLC Catastrophic Non App", "format": utils.thousands_format(4)}),
                "el_usd_catastrophic_non_app"         : hx.Float(mode="output",                                  view={"label": "FGU Expected Loss Catastrophic Non App", "format": utils.thousands_format(4)}),
                "net_el_usd_catastrophic_non_app"     : hx.Float(mode="output",                                  view={"label": "Layer 1 Expected Loss Catastrophic Non App", "format": utils.thousands_format(4)}),
                "struct_pct_adverse_weather"          : hx.Float(mode="output",                                  view={"label": "Layer 1 FLC Adverse Weather", "format": utils.thousands_format(4)}),
                "el_usd_adverse_weather"              : hx.Float(mode="output",                                  view={"label": "FGU Expected Loss Adverse Weather", "format": utils.thousands_format(4)}),
                "net_el_usd_adverse_weather"          : hx.Float(mode="output",                                  view={"label": "Layer 1 Expected Loss Adverse Weather", "format": utils.thousands_format(4)}),
                "struct_pct_windstorm"                : hx.Float(mode="output",                                  view={"label": "Layer 1 FLC Windstorm", "format": utils.thousands_format(4)}),
                "el_usd_windstorm"                    : hx.Float(mode="output",                                  view={"label": "FGU Expected Loss Windstorm", "format": utils.thousands_format(4)}),
                "net_el_usd_windstorm"                : hx.Float(mode="output",                                  view={"label": "Layer 1 Expected Loss Windstorm", "format": utils.thousands_format(4)}),
                "struct_pct_wildfire"                 : hx.Float(mode="output",                                  view={"label": "Layer 1 FLC Wildfire", "format": utils.thousands_format(4)}),
                "el_usd_wildfire"                     : hx.Float(mode="output",                                  view={"label": "FGU Expected Loss Wildfire", "format": utils.thousands_format(4)}),
                "net_el_usd_wildfire"                 : hx.Float(mode="output",                                  view={"label": "Layer 1 Expected Loss Wildfire", "format": utils.thousands_format(4)}),
                "struct_pct_earthquake"               : hx.Float(mode="output",                                  view={"label": "Layer 1 FLC Earthquake", "format": utils.thousands_format(4)}),
                "el_usd_earthquake"                   : hx.Float(mode="output",                                  view={"label": "FGU Expected Loss Earthquake", "format": utils.thousands_format(4)}),
                "net_el_usd_earthquake"               : hx.Float(mode="output",                                  view={"label": "Layer 1 Expected Loss Earthquake", "format": utils.thousands_format(4)}),
                "el_usd_national_mourning_mod"        : hx.Float(mode="output",                                  view={"label": "FGU Expected Loss National Mourning (after uw mods)", "format": utils.thousands_format(4)}),
                "net_el_usd_national_mourning_mod"    : hx.Float(mode="output",                                  view={"label": "Layer 1 Expected Loss National Mourning (after uw mods)", "format": utils.thousands_format(4)}),

            }),
        }),



        "non_appearance"  : hx.Structure(children={
            "genre":                hx.Str(  mode="input", default=None,       optionality="optional", view={"label": "Genre"          },           options_table="tbl_non_app_base_rates", options_column="genre", async_input=['rarc_task']),
            "base_rate":            hx.Float(mode="output",                                            view={"label": "Base Rate",                    "format": utils.percent_format(2)}  ),
            "num_shows":            hx.Int(  mode="input", default=None,       optionality="optional", view={"label": "Number of Shows",              "format": utils.thousands_format(0)},                         async_input=['rarc_task']),
            "avg_show_value":       hx.Float(mode="output",                                            view={"label": "Average Show Value",           "format": utils.thousands_format(0)}),
            "agg_show_value":       hx.Float(mode="input", default=None,       optionality="optional", view={"label": "Aggregate Insured Value",      "format": utils.thousands_format(0)},                         async_input=['rarc_task']),
            "el_fgu":               hx.Float(mode="output",                                            view={"label": "Expected Loss - FGU",   "format": utils.thousands_format(0)}),


            "num_band_members":     hx.Str(  mode="input", default=None,       optionality="optional", view={"label": "Number of Band Members"},    options_table="tbl_non_app_num_band_members_mod", options_column="num_band_members", async_input=['rarc_task']),
            "claim_experience":     hx.Str(  mode="input", default=None,       optionality="optional", view={"label": "Claims Experience"},         options_table="tbl_non_app_claim_experience_mod", options_column="claim_experience", async_input=['rarc_task']),
            "num_band_members_mod": hx.Float(mode="output",                                            view={"label": "Number of Band Members Rate Modifier",   "format": utils.percent_format(2)}  ),
            "claim_experience_mod": hx.Float(mode="output",                                            view={"label": "Claims Experience Rate Modifier",        "format": utils.percent_format(2)}  ),
            "nmp_mod":              hx.Float(mode="output",                                            view={"label": "Non Modelled Perils Load Rate Modifier", "format": utils.percent_format(2)}  ),
            "total_mod":            hx.Float(mode="output",                                            view={"label": "Total Modifier Factor",                  "format": utils.percent_format(2)}  ),
            "el_fgu_mod":           hx.Float(mode="output",                                            view={"label": "Expected Loss - FGU Modified",             "format": utils.thousands_format(0)}),

            "num_layers":           hx.Int(  mode="input", default=1,          optionality="required", view={"label": "Number of Shows"},           options=lst_layers,                                     async_input=['rarc_task']),
            "fl_curve":             hx.Str(  mode="input", default="Attritional",optionality="optional", view={"label": "First Loss Curve"},        options=lst_curve,                                      async_input=['rarc_task']),

            **cvg_adjustments(),

            "fgu"  : hx.Structure(children={
                "description":          hx.Str(  mode="output", view={"label": "Description"}),
                # "fgu_pct":              hx.Float(mode="output", view={"label": "Proportion of\nFGU Loss to\nthe Layer", "format": utils.percent_format(2)}),
                "el_fgu_mod":           hx.Float(mode="output", view={"label": "Expected Loss\nModified",               "format": utils.thousands_format(0)}),
                "el_fgu_mod_adj":       hx.Float(mode="output", view={"label": "Expected Loss\nModified &\nUW Adjusted",   "format": utils.thousands_format(0)})   }),

            "total"  : hx.Structure(children={
                "description":          hx.Str(  mode="output", view={"label": "Description"}),
                "fgu_pct":              hx.Float(mode="output", view={"label": "Proportion of\nFGU Loss to\nthe Layer", "format": utils.percent_format(2)}),
                "el_fgu_mod":           hx.Float(mode="output", view={"label": "Expected Loss\nModified",               "format": utils.thousands_format(0)}),
                "el_fgu_mod_adj":       hx.Float(mode="output", view={"label": "Expected Loss\nModified &\nUW Adjusted",   "format": utils.thousands_format(0)})   }),

        }),

    })


    # cds.extend_node_rater_defined("cds/layers", { 
    #     "description":          hx.Str(  mode="output", view={"label": "Description"}),
    #     "fgu_pct":              hx.Float(mode="output", view={"label": "Proportion of\nFGU Loss to\nthe Layer", "format": utils.percent_format(2)}),
    #     "el_fgu_mod":           hx.Float(mode="output", view={"label": "Expected Loss\nModified",               "format": utils.thousands_format(0)}),
    #     "el_fgu_mod_adj":       hx.Float(mode="output", view={"label": "Expected Loss\nModified &\nUW Adjusted","format": utils.thousands_format(0)})           
    # }),

