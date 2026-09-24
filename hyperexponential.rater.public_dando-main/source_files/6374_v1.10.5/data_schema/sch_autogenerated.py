import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format
from data_schema.sch_utilities import percent_format
from data_schema.sch_utilities import integer_format

def sch_rater_defined(cds):
    cds.extend_node_items("cds/layers/coverages", {
        "abc": {"label": "ABC"},
        "side_a": {"label": "Side A"},
    })
    cds.extend_node_rater_defined("cds", {
        "rw_broker": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Retail/Wholesale Broker"}),
        "uw_location": hx.Str(mode="output", view={"label": "None"}),
        "company_name": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Company Name"}),
        "company_search": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Company Search"}),
        "ticker": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Ticker"}),
        "company_country": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Country"}),
        "company_state": hx.Str(mode="input", default=None, optionality="optional", view={"label": "State"}),
        "incorporated_state": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Incorporated State"}),
        "hq_state": hx.Str(mode="input", default=None, optionality="optional", view={"label": "HQ State"}),
        "hq_city": hx.Str(mode="input", default=None, optionality="optional", view={"label": "HQ City"}),
        "airport_city": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Airport City"}),
        "coverage": hx.Str(mode="input", default="ABC", view={"label": "ABC, Side A or Armour"}),
        "is_abc": hx.Bool(mode="output", view={"label": "None"}),
        "is_side_a": hx.Bool(mode="output", view={"label": "None"}, async_input=["generate_tags_cuap", "rarc_task"]),
        "pipeline_premium": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Pipeline Premium"}),
        "opportunity_code": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Opportunity Code"}),
        "under_jobs_act": hx.Bool(mode="input", default=True, view={"label": "Tick if Issued Under Jobs Act"}),
        "core_account": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Core Account"}),
        "company_description": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Company Description"}),
        "comment": hx.Str(mode="input", default=None, optionality="optional", view={"label": "General Comments"}),
        "claims_history": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Claims History"}),
        "t_and_c_comment": hx.Str(mode="input", default=None, optionality="optional", view={"label": "T&C"}),
        "frequency": hx.Structure(children={
            "sca_unity_freq": hx.Float(mode="output", view={"label": "SCA Unity Frequency"}),
            "sca_sector_freq": hx.Float(mode="output", view={"label": "SCA Sector Frequency"}),
            "sca_model_freq": hx.Float(mode="output", view={"label": "SCA Model Frequency"}),
            "sca_freq_override": hx.Float(mode="input", default=None, optionality="optional", view={"label": "SCA Frequency Override"}),
            "sca_freq_override_comment": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Override Comment"}),
            "sca_used_freq": hx.Float(mode="output", view={"label": "SCA Used Frequency"}),
            "s_unity_freq": hx.Float(mode="output", view={"label": "S Unity Frequency"}),
            "s_sector_freq": hx.Float(mode="output", view={"label": "S Sector Frequency"}),
            "s_model_freq": hx.Float(mode="output", view={"label": "S Model Frequency"}),
            "s_used_freq": hx.Float(mode="output", view={"label": "S Used Frequency"}),
            "sd_unity_freq": hx.Float(mode="output", view={"label": "SD Unity Frequency"}),
            "sd_sector_freq": hx.Float(mode="output", view={"label": "SD Sector Frequency"}),
            "sd_model_freq": hx.Float(mode="output", view={"label": "SD Model Frequency"}),
            "sd_used_freq": hx.Float(mode="output", view={"label": "SD Used Frequency"}),
            "d_unity_freq": hx.Float(mode="output", view={"label": "Derivative Unity Frequency"}),
            "d_sector_freq": hx.Float(mode="output", view={"label": "Derivative Sector Frequency"}),
            "d_model_freq": hx.Float(mode="output", view={"label": "Derivative Model Frequency"}),
            "d_used_freq": hx.Float(mode="output", view={"label": "Derivative Frequency"}),
            "ma_unity_freq": hx.Float(mode="output", view={"label": "M&A Unity Frequency"}),
            "ma_sector_freq": hx.Float(mode="output", view={"label": "M&A Sector Frequency"}),
            "ma_model_freq": hx.Float(mode="output", view={"label": "M&A Model Frequency"}),
            "ma_used_freq": hx.Float(mode="output", view={"label": "M&A Frequency"}),
            "total_freq": hx.Float(mode="output", view={"label": "Total Frequency"}),

        }),
        "experian_sector_quartile": hx.Float(mode="output", view={"label": "Experian Sector Quartile"}),
        "lowest_adj_factor": hx.Float(mode="output", view={"label": "Lowest Adj Factor Allowed"}),
        "bridge_premium": hx.Float(mode="override", view={"label": "Bridge Premium"}),
        "bridge_comment": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Bridge Comment"}),
        "historic_frequencies": hx.Structure(children={
            "base": hx.Float(mode="output", view={"label": "Base"}),
            "claims": hx.Float(mode="output", view={"label": "Claims"}),
            "exposure": hx.Float(mode="output", view={"label": "Exposure"}),
            "mc_frequency": hx.Float(mode="output", view={"label": "Market Cap frequency"}),
            "relative_year": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Relative Year"}),
            "year": hx.Float(mode="output", view={"label": "Year"}),

        }),
        "esg": hx.Structure(children={
            "esg_total_score": hx.Float(mode="input", default=None, optionality="optional", view={"label": "ESG Total Score"}),
            "esg_environmental_score": hx.Float(mode="input", default=None, optionality="optional", view={"label": "ESG Environmental Score"}),
            "esg_social_score": hx.Float(mode="input", default=None, optionality="optional", view={"label": "ESG Social Score"}),
            "esg_governance_score": hx.Float(mode="input", default=None, optionality="optional", view={"label": "ESG Governance Score"}),
            "esg_industry_average_score": hx.Float(mode="input", default=None, optionality="optional", view={"label": "ESG Industry Average Score"}),

        }),
    })
    cds.extend_node_rater_defined("cds/layers", {
        "profit": hx.Float(mode="output", view={"label": "Profit"}),
        "total_capital": hx.Float(mode="output", view={"label": "Total Capital"}),
        "ei_limit": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Underlying EI Limit"}),
        "ei_price": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Entity Investigation Price"}),
        "ei_premium": hx.Float(mode="output", view={"label": "E/I Premium"}),
    })
    cds.extend_node_rater_defined("cds/exposure/aggregate", {
        "market_cap": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Market Cap"}),
        "market_cap_info": hx.Str(mode="output", view={"label": "None"}),
        "insider_share": hx.Float(mode="input", default=0.0, view={"label": "Insider Share %"}),
        "insider_share_info": hx.Str(mode="output", view={"label": "None"}),
        "revised_market_cap": hx.Float(mode="output", view={"label": "Revised Market Cap"}),
        "revised_market_cap_comment": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Market Cap Comment"}),
        "total_assets": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Total Assets"}),
        "ipo_date": hx.Date(mode="input", default=None, optionality="optional", view={"label": "IPO Date"}),
        "ipo_date_comment": hx.Str(mode="input", default=None, optionality="optional", view={"label": "IPO Date Comment"}),
        "credit_rating": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Credit Rating"}),
        "credit_rating_estimated": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Credit Rating Estimated?"}),
        "credit_rating_override": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Credit Rating Override?"}),
        "minimum_trading_volume": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Minimum Trading Volume"}),
        "volatility_of_trading": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Volatility of Trading During Downturn"}),
        "execs_under_age_50": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Percentage of Execturives under age 50"}),
        "year_founded": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Year Founded"}),
        "ebit": hx.Float(mode="input", default=None, optionality="optional", view={"label": "EBIT"}),
        "total_assets_output": hx.Float(mode="output", view={"label": "Total Assets"}),
        "period": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Period"}),
        "source": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Source"}),
        "net_sales": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Net Sales"}),
        "dic_loading_factor": hx.Float(mode="input", default=None, optionality="optional", view={"label": "DIC Loading Factor"}),
        "market_value_of_equity": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Market Capitalization"}),
        "z_score": hx.Float(mode="output", view={"label": "Z-Score"}),
        "total_liabilities": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Total Liabilities"}),
        "bankruptcy_score": hx.Float(mode="output", view={"label": "Bankruptcy Score"}),
        "current_assets": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Current Assets"}),
        "average_bankruptcy_score": hx.Float(mode="output", view={"label": "Average Bankruptcy Score"}),
        "current_liabilities": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Current Liabilities"}),
        "retained_earnings": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Retained Earnings"}),
    })
    cds.extend_node_rater_defined("cds/key_industry", {
        "sector_name": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Sector"}),
        "sic_percentage": hx.Float(mode="input", default=1.0, view={"label": "SIC Percentage"}),
        "sector_id": hx.Float(mode="output", view={"label": "None"}),
        "sector_message": hx.Str(mode="output", view={"label": "Sector Message"}),
        "sector_base_frequency": hx.Float(mode="output", view={"label": "None"}),
        "sector_uw_override": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Underwriter Override"}),
        "sector_uw_override_comment": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Underwriter Override Comment"}),
        "sector_unity_frequency": hx.Float(mode="output", view={"label": "Sector Base Frequency"}),
        "sic_code_2": hx.Str(mode="output", view={"label": "SIC Code 2"}),
        "sic_description_2": hx.Str(mode="input", default=None, optionality="optional", view={"label": "SIC Description 2"}),
        "sector_2": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Sector 2"}),
        "sic_percentage_2": hx.Float(mode="input", default=None, optionality="optional", view={"label": "SIC Percentage 2"}),
        "sector_id_2": hx.Float(mode="output", view={"label": "None"}),
        "sector_message_2": hx.Str(mode="output", view={"label": "Sector Message"}),
        "sector_base_frequency_2": hx.Float(mode="output", view={"label": "None"}),
        "sector_uw_override_2": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Underwriter Override 2"}),
        "sector_uw_override_comment_2": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Underwriter Override Comment 2"}),
        "sector_unity_frequency_2": hx.Float(mode="output", view={"label": "Sector Base Frequency 2"}),
        "sic_code_3": hx.Str(mode="output", view={"label": "SIC Code 3"}),
        "sic_description_3": hx.Str(mode="input", default=None, optionality="optional", view={"label": "SIC Description 3"}),
        "sector_3": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Sector 3"}),
        "sic_percentage_3": hx.Float(mode="input", default=None, optionality="optional", view={"label": "SIC Percentage 3"}),
        "sector_id_3": hx.Float(mode="output", view={"label": "None"}),
        "sector_message_3": hx.Str(mode="output", view={"label": "Sector Message"}),
        "sector_base_frequency_3": hx.Float(mode="output", view={"label": "None"}),
        "sector_uw_override_3": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Underwriter Override 3"}),
        "sector_uw_override_comment_3": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Underwriter Override Comment 3"}),
        "sector_unity_frequency_3": hx.Float(mode="output", view={"label": "Sector Base Frequency 3"}),
    })
    cds.extend_node_rater_defined("cds/layers/coverages/abc", {
        "quoted_market_share": hx.Float(mode="output", view={"label": "ABC Quoted Market Share"}),
        "elr": hx.Float(mode="output", view={"label": "PFLR"}),
        "ma_retention": hx.Float(mode="input", default=None, optionality="optional", view={"label": "M&A Retention"}),
        "total_excess": hx.Float(mode="output", view={"label": "Total Excess"}),
        "bridge_countries": hx.Bool(mode="input", default=None, optionality="optional", view={"label": "Bridge Countries?"}),
        "at_cost_75": hx.Float(mode="output", view={"label": "75th at Cost"}),
        "incl_dimissals_75": hx.Float(mode="output", view={"label": "75th Incl Dismissals"}),
        "selected": hx.Bool(mode="input", default=False, view={"label":"Selected for Tags"}, async_input=["generate_tags_cuap"])
    })
    cds.extend_node_rater_defined("cds/layers/coverages/side_a", {
        "quoted_market_share": hx.Float(mode="output", view={"label": "Side A Quoted Market Share"}),
        "tower": hx.Float(mode="input", default=None, optionality="optional", view={"label": "ABC Tower"}),
        "total_excess": hx.Float(mode="output", view={"label": "Total Excess"}),
        "non_rescindable_coverage": hx.Bool(mode="input", default=None, optionality="optional", view={"label": "Provides non-rescindable side A coverage"}),
        "director_limit": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Ind. Director Limit"}),
        "elr": hx.Float(mode="output", view={"label": "PFLR"}),
        "at_cost_75": hx.Float(mode="output", view={"label": "75th at Cost"}),
        "incl_dimissals_75": hx.Float(mode="output", view={"label": "75th Incl Dismissals"}),
        "selected": hx.Bool(mode="input", default=False, view={"label":"Selected for Tags"}, async_input=["generate_tags_cuap"])
    })
    cds.override_node_properties("cds/layers/coverages/abc/quoted_premium", {
        "view": {"label": "ABC Quoted Premium"},
    })
    cds.override_node_properties("cds/layers/coverages/abc/benchmark_premium", {
        "view": {"label": "Benchmark Premium"},
    })
    cds.override_node_properties("cds/layers/coverages/abc/technical_premium", {
        "view": {"label": "Technical Premium"},
    })
    cds.override_node_properties("cds/layers/coverages/abc/technical_premium_pre_uw_adj", {
        "view": {"label": "Technical Premium (Pre-UW Adjustment)"},
    })
    cds.override_node_properties("cds/layers/coverages/abc/written_line", {
        "view": {"label": "Beazley Market Share"},
        "default": 1.0,
    })
    cds.override_node_properties("cds/layers/coverages/abc/roc", {
        "view": {"label": "ROC"},
    })
    cds.override_node_properties("cds/layers/coverages/side_a/quoted_premium", {
        "view": {"label": "Side A Quoted Premium"},
    })
    cds.override_node_properties("cds/layers/coverages/side_a/benchmark_premium", {
        "view": {"label": "Side A Benchmark Premium"},
    })
    cds.override_node_properties("cds/layers/coverages/side_a/technical_premium", {
        "view": {"label": "Technical Premium"},
    })
    cds.override_node_properties("cds/layers/coverages/side_a/technical_premium_pre_uw_adj", {
        "view": {"label": "Technical Premium (Pre-UW Adjustment)"},
    })
    cds.override_node_properties("cds/layers/coverages/side_a/written_line", {
        "view": {"label": "Beazley Market Share"},
        "default": 1.0,
    })
    cds.override_node_properties("cds/layers/coverages/side_a/limit", {
        "view": {"label": "Side A Limit"},
    })
    cds.override_node_properties("cds/layers/coverages/side_a/excess", {
        "view": {"label": "Side A Excess"},
        "default": 0
    })
    cds.override_node_properties("cds/layers/coverages/side_a/deductible", {
        "view": {"label": "ABC Deductible"},
        "default": 0
    })
    cds.override_node_properties("cds/layers/coverages/side_a/roc", {
        "view": {"label": "ROC"},
    })

    # selected async_input
    cds.override_node_properties("cds/layers/coverages/side_a/selected", {"async_input": ["generate_tags_cuap"]})
    cds.override_node_properties("cds/layers/coverages/abc/selected", {"async_input": ["generate_tags_cuap"]})
