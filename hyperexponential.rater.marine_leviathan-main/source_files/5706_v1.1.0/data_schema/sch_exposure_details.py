import hx_data_schema as hx
import data_schema.sch_utilities as utils

def thousands_format(mantissa=0):
    return{"thousandSeparated": True, "mantissa":mantissa}


def percent_format(mantissa=0):
    return{"output": "percent", "mantissa":mantissa}

# Replace / remove examples with your models exposures

def sch_exposure_details(cds):
    
       
    # For aggregate exposure e.g. total revenue, sum insured etc. please add to the aggregate exposures node
    cds.extend_node_rater_defined("cds/exposure/aggregate", {
        # PLACEHOLDER value used in experience rating, the experience rating should connect to the total exposure value of the model
        "example_aggregate_exposure": hx.Float(mode="input", default=0, view={"label": "Agg Exposure", "format": utils.thousands_format(0)}),
        
    })

    # For granular exposure lists e.g. aircrafts, hospitals etc, please add to the granular node
    cds.extend_node_rater_defined("cds/exposure/granular", {        
        # Replace the below with your models exposures
        "example_exposure": hx.List(mode="input",  async_input=["rarc_task"], children={
            "country": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Country"}),
            "city": hx.Str(mode="input", default=None, optionality="optional", view={"label": "City"}),
            "type": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Type"}),
            "tiv": hx.Float(mode="input", default=None, optionality="optional", view={"label": "TIV", "format": utils.thousands_format(0)}),
        }),

    # Vessel Details

    #Dynamic labels for Vessel Details table
    "total_sum_insured_label": hx.Str(mode = "output"),
    "average_sum_insured_label": hx.Str(mode = "output"),
    "benchmark_premium_label": hx.Str(mode = "output"),
    "rov_hovertext": hx.Str(mode = "output"),

   "number_of_units": hx.Structure(view={"label": "Number of Units"}, children={
        "rov": hx.Int(mode="input", async_input=["rarc_task"], default=0, validation={"min_value": 0}, view ={"label": "ROV", "format": thousands_format(0)}),
        "auv": hx.Int(mode="input", async_input=["rarc_task"], default=0, validation={"min_value": 0},view ={"label": "AUV", "format": thousands_format(0)}),
        "seismic_towed": hx.Int(mode="input", async_input=["rarc_task"], default=0, validation={"min_value": 0},view ={"label": "Seismic-Towed", "format": thousands_format(0)}),
        "seismic_ocean_bottom": hx.Int(mode="input", async_input=["rarc_task"], default=0, validation={"min_value": 0},view ={"label": "Seismic-Ocean Bottom", "format": thousands_format(0)}),
        "diving_oceanographic": hx.Int(mode="input", async_input=["rarc_task"], default=0, validation={"min_value": 0},view ={"label": "Diving & Oceanographic", "format": thousands_format(0)}),
        "submersibles": hx.Int(mode="input", async_input=["rarc_task"], default=0, validation={"min_value": 0},view ={"label": "Submersibles", "format": thousands_format(0)}),
        "other": hx.Int(mode="input", async_input=["rarc_task"], default=0, validation={"min_value": 0},view ={"label": "Other", "format": thousands_format(0)}),
        "total": hx.Float(mode="output",view ={"label": "Total", "format": thousands_format(0)}),
        
   }),

    "total_sum_insured": hx.Structure(view={"label": "Total Sum Insured"}, children={
        "rov": hx.Float(mode="input", async_input=["rarc_task"], default=0, validation={"min_value": 0.0},view ={"label": "ROV", "format": thousands_format(0)}),
        "auv": hx.Float(mode="input", async_input=["rarc_task"], default=0, validation={"min_value": 0.0},view ={"label": "AUV", "format": thousands_format(0)}),
        "seismic_towed": hx.Float(mode="input", async_input=["rarc_task"], default=0, validation={"min_value": 0.0},view ={"label": "Seismic-Towed", "format": thousands_format(0)}),
        "seismic_ocean_bottom": hx.Float(mode="input", async_input=["rarc_task"], default=0, validation={"min_value": 0.0},view ={"label": "Seismic-Ocean Bottom", "format": thousands_format(0)}),
        "diving_oceanographic": hx.Float(mode="input", async_input=["rarc_task"], default=0, validation={"min_value": 0.0},view ={"label": "Diving & Oceanographic", "format": thousands_format(0)}),
        "submersibles": hx.Float(mode="input", async_input=["rarc_task"], default=0, validation={"min_value": 0.0},view ={"label": "Submersibles", "format": thousands_format(0)}),
        "other": hx.Float(mode="input", async_input=["rarc_task"], default=0, validation={"min_value": 0.0},view ={"label": "Other", "format": thousands_format(0)}),
        "total": hx.Float(mode="output",view ={"label": "Total", "format": thousands_format(0)}),
        
     }),

   "average_sum_insured_per_unit": hx.Structure(view={"label": "Average Sum Insured per Unit"}, children={
        "rov": hx.Float(mode="output", view ={"label": "ROV", "format": thousands_format(0)}),
        "auv": hx.Float(mode="output", view ={"label": "AUV", "format": thousands_format(0)}),
        "seismic_towed": hx.Float(mode="output", view ={"label": "Seismic-Towed", "format": thousands_format(0)}),
        "seismic_ocean_bottom": hx.Float(mode="output", view ={"label": "Seismic-Ocean Bottom", "format": thousands_format(0)}),
        "diving_oceanographic": hx.Float(mode="output", view ={"label": "Diving & Oceanographic", "format": thousands_format(0)}),
        "submersibles": hx.Float(mode="output", view ={"label": "Submersibles", "format": thousands_format(0)}),
        "other": hx.Float(mode="output", view ={"label": "Other", "format": thousands_format(0)}),
                
        }),

   "excess_per_loss": hx.Structure(view={"label": "Excess (per loss)"}, children={
        "rov": hx.Float(mode="input",  async_input=["rarc_task"], default=0, validation={"min_value": 0.0},view ={"label": "ROV", "format": thousands_format(0)}),
        "auv": hx.Float(mode="output",  async_input=["rarc_task"], validation={"min_value": 0.0},view ={"label": "AUV", "format": thousands_format(0)}),
        "seismic_towed": hx.Float(mode="input",  async_input=["rarc_task"], default=0, validation={"min_value": 0.0},view ={"label": "Seismic-Towed", "format": thousands_format(0)}),
        "seismic_ocean_bottom": hx.Float(mode="input",  async_input=["rarc_task"], default=0, validation={"min_value": 0.0},view ={"label": "Seismic-Ocean Bottom", "format": thousands_format(0)}),
        "diving_oceanographic": hx.Float(mode="input",  async_input=["rarc_task"], default=0, validation={"min_value": 0.0},view ={"label": "Diving & Oceanographic", "format": thousands_format(0)}),
        "submersibles": hx.Float(mode="input",  async_input=["rarc_task"], default=0, validation={"min_value": 0.0},view ={"label": "Submersibles", "format": thousands_format(0)}),
        "other": hx.Float(mode="input", default=0,  async_input=["rarc_task"], validation={"min_value": 0.0},view ={"label": "Other", "format": thousands_format(0)}),
     }),

    "excess_per_loss_auv": hx.Structure(view={"label": "Excess (per loss)"}, children={ 
    "normal_ops": hx.Float(mode="input",  async_input=["rarc_task"], default=50000, validation={"min_value": 0.0}, view ={"label": "Normal Operation", "format": thousands_format(0)}),
    "launch_recovery": hx.Float(mode="input",  async_input=["rarc_task"], default=100000, validation={"min_value": 0.0}, view ={"label": "Launch & recovery", "format": thousands_format(0)}),
     }),
       
    "benchmark_premium": hx.Structure(view={"label": "Benchmark Premium"}, children={
        "rov": hx.Float(mode="output", view ={"label": "ROV", "format": thousands_format(0)}),
        "auv": hx.Float(mode="output", view ={"label": "AUV", "format": thousands_format(0)}),
        "seismic_towed": hx.Float(mode="output", view ={"label": "Seismic-Towed", "format": thousands_format(0)}),
        "seismic_ocean_bottom": hx.Float(mode="output", view ={"label": "Seismic-Ocean Bottom", "format": thousands_format(0)}),
        "diving_oceanographic": hx.Float(mode="output", view ={"label": "Diving & Oceanographic", "format": thousands_format(0)}),
        "submersibles": hx.Float(mode="output", view ={"label": "Submersibles", "format": thousands_format(0)}),
        "other": hx.Float(mode="output", view ={"label": "Other", "format": thousands_format(0)}),
        "total": hx.Float(mode="output",view ={"label": "Total", "format": thousands_format(0)}),
    }),   

    # End of Vessel Details 

    #Other (Policy-Level) Risk Factors
    "type_of_work": hx.Str(mode="input",  async_input=["rarc_task"], default ="Oil & Gas", view={"label": "Type of Work"}, options_table = "lst_type_of_work", options_column = "Type of Work"),
    "ice_debris_other_traffic": hx.Str(mode="input",  async_input=["rarc_task"], default ="None", view={"label": "Will there be ice, debris or other marine traffic?"}, options_table = "lst_ice_debris_traffic", options_column = "Ice, debris, other marine traffic"),
    "experience_level": hx.Str(mode="input",  async_input=["rarc_task"], default ="Average", view={"label": "Experience of people operating the vessels"}, options_table = "lst_experience_category", options_column = "Experience Category"),
    "usage_factor": hx.Float(mode="input",  async_input=["rarc_task"], default =0.6, view={"label": "Usage %", "format":{"output": "percent", "mantissa":1}}),


    #Underwriter adjustment to benchmark
    "uw_adjustment": hx.Float(mode="input",  async_input=["rarc_task"], default = 0, view={"label": "Adjustment (%)", "format":{"output": "percent", "mantissa":1}}),
    "uw_adjustment_rationale": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Adjustment Rationale"}),
        
    
    #Total expected loss for storage only
    "total_expected_loss_gbp": hx.Float(mode="output"),
    "total_expected_loss": hx.Float(mode="output")
    
    
    })

