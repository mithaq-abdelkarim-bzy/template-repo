# If changing the max_layers below, you must also update in vw_constants to the same number
max_layers = 11
max_options = 10

benchmark_lr = 0.7
priced_to_lr = 0.65

# Defaults for optional coverages [Adjustments tab]
optional_default_yes = 0.15
optional_default_no = 0.0

# Business Plan class, for tp_parameters lookup
bp_class = 'Media'

# Individual Film - Exposure - Coverage Basis modifiers
occurence_modifier_canada= 1.3
occurence_modifier = 1.1
claimsmade_modifier = 1.0

# ILF Map
ilf_mapping = {1.0: "Low", 2.0: "Low", 3.0: "Medium", 4.0: "Medium", 5.0: "High", 6.0: "High"}

def exposure_change_list():
    exposure_change_path = [
        "cds/exposure/aggregate/total_revenue",
        "cds/exposure/aggregate/rateable/revenue",
        "cds/exposure/aggregate/annual_tv/capped_productions",
        "cds/exposure/aggregate/individual_tv/length",
        "cds/exposure/aggregate/individual_tv/number_of_episodes",
        "cds/exposure/aggregate/individual_film/exhibition",

        "cds/exposure/granular/media/advert_agency/base_rate",
        "cds/exposure/granular/media/public_relations/base_rate",
        "cds/exposure/granular/media/market_research/base_rate",
        "cds/exposure/granular/media/misc_advert/base_rate",
        "cds/exposure/granular/media/other1/base_rate",
        "cds/exposure/granular/media/production_companies/base_rate",
        "cds/exposure/granular/media/other2/base_rate",
        "cds/exposure/granular/media/social_low/base_rate",
        "cds/exposure/granular/media/publishing_low/base_rate",
        "cds/exposure/granular/media/radio/base_rate",
        "cds/exposure/granular/media/other3/base_rate",
        "cds/exposure/granular/media/social_medium/base_rate",
        "cds/exposure/granular/media/publishing_medium/base_rate",
        "cds/exposure/granular/media/other4/base_rate",
        "cds/exposure/granular/media/social_celeb/base_rate",
        "cds/exposure/granular/media/publishing_high/base_rate",
        "cds/exposure/granular/media/other5/base_rate",
        "cds/exposure/granular/media/publishing_severe/base_rate",
        "cds/exposure/granular/media/other6/base_rate",

        "cds/exposure/granular/music/other1/base_rate",
        "cds/exposure/granular/music/other2/base_rate",
        "cds/exposure/granular/music/composer_low/base_rate",
        "cds/exposure/granular/music/artist_low/base_rate",
        "cds/exposure/granular/music/record_label_low/base_rate",
        "cds/exposure/granular/music/other3/base_rate",
        "cds/exposure/granular/music/composer_medium/base_rate",
        "cds/exposure/granular/music/artist_medium/base_rate",
        "cds/exposure/granular/music/record_label_medium/base_rate",
        "cds/exposure/granular/music/music_talent/base_rate",
        "cds/exposure/granular/music/other4/base_rate",
        "cds/exposure/granular/music/composer_high/base_rate",
        "cds/exposure/granular/music/artist_high/base_rate",
        "cds/exposure/granular/music/record_label_high/base_rate",
        "cds/exposure/granular/music/other5/base_rate",
        "cds/exposure/granular/music/composer_severe/base_rate",
        "cds/exposure/granular/music/licensing/base_rate",
        "cds/exposure/granular/music/streaming/base_rate",
        "cds/exposure/granular/music/royalties/base_rate",
        "cds/exposure/granular/music/supervision/base_rate",
        "cds/exposure/granular/music/other6/base_rate",

        "cds/exposure/granular/tvfilm/other1/base_rate",
        "cds/exposure/granular/tvfilm/production2/base_rate",
        "cds/exposure/granular/tvfilm/broadcast2/base_rate",
        "cds/exposure/granular/tvfilm/distribution_verylow/base_rate",
        "cds/exposure/granular/tvfilm/other2/base_rate",
        "cds/exposure/granular/tvfilm/production3/base_rate",
        "cds/exposure/granular/tvfilm/broadcast3/base_rate",
        "cds/exposure/granular/tvfilm/distribution_low/base_rate",
        "cds/exposure/granular/tvfilm/other3/base_rate",
        "cds/exposure/granular/tvfilm/production4/base_rate",
        "cds/exposure/granular/tvfilm/broadcast4/base_rate",
        "cds/exposure/granular/tvfilm/distribution_medium/base_rate",
        "cds/exposure/granular/tvfilm/other4/base_rate",
        "cds/exposure/granular/tvfilm/production5/base_rate",
        "cds/exposure/granular/tvfilm/broadcast5/base_rate",
        "cds/exposure/granular/tvfilm/distribution_high/base_rate",
        "cds/exposure/granular/tvfilm/other5/base_rate",
        "cds/exposure/granular/tvfilm/production6/base_rate",
        "cds/exposure/granular/tvfilm/broadcast6/base_rate",
        "cds/exposure/granular/tvfilm/distribution_veryhigh/base_rate",
        "cds/exposure/granular/tvfilm/other6/base_rate",

        # IR: where do these fit in?
        "cds/annual_tv/turnover",
        "cds/annual_tv/annual_budget",

        "cds/exposure/granular/annual_tv/genre/entertainment_sitcom/perc_of_total_turnover",
        "cds/exposure/granular/annual_tv/genre/drama_chat/perc_of_total_turnover",
        "cds/exposure/granular/annual_tv/genre/reality/perc_of_total_turnover",
        "cds/exposure/granular/annual_tv/genre/factual_contentious/perc_of_total_turnover",
        "cds/exposure/granular/annual_tv/genre/factual_non_investigative/perc_of_total_turnover",
        "cds/exposure/granular/annual_tv/genre/game_show/perc_of_total_turnover",
        "cds/exposure/granular/annual_tv/genre/live/perc_of_total_turnover",
        "cds/exposure/granular/annual_tv/genre/factual_investigative/perc_of_total_turnover",
        "cds/exposure/granular/annual_tv/genre/children_religious/perc_of_total_turnover",
        "cds/exposure/granular/annual_tv/genre/sport_history_nature/perc_of_total_turnover",
        "cds/exposure/granular/annual_tv/genre/films_for_tv/perc_of_total_turnover"

    ]
    return(exposure_change_path)

def risk_char_change_list():
    risk_char_change_path = [

        "cds/rating_factors/years_in_business",
        "cds/rating_factors/location",
        "cds/rating_factors/territory_factor",

        "cds/modifiers/longevity_factor",
        "cds/modifiers/experience_factor/output",

        "cds/modifiers/media/media_review_control_procedures/selected",
        "cds/modifiers/media/qualifications_inhouse_counsel/selected",
        "cds/modifiers/media/geographical_scope/selected",
        "cds/modifiers/media/popularity/selected",
        "cds/modifiers/media/use_of_standard_contracts/selected",
        "cds/modifiers/media/contract_sizes/selected",
        "cds/modifiers/media/proportion_of_own_content/selected",
        "cds/modifiers/media/contingent_bi_pd_exposure/selected",
        "cds/modifiers/media/us_exposure/selected",

        "cds/modifiers/music/contract_sizes/selected",
        "cds/modifiers/music/us_exposure/selected",
        "cds/modifiers/music/popularity/selected",
        "cds/modifiers/music/size_of_back_catalogue/selected",
        "cds/modifiers/music/high_volume_of_licensing/selected",

        "cds/modifiers/tvfilm/three_year_cover/selected",
        "cds/modifiers/tvfilm/popularity/selected",
        "cds/modifiers/tvfilm/average_budget/selected",
        "cds/modifiers/tvfilm/max_budget/selected",
        "cds/modifiers/tvfilm/fair_use_exposure/selected",
        "cds/modifiers/tvfilm/ability_to_subrogate/selected",
        "cds/modifiers/tvfilm/quality_of_legal_clearance/selected",
        "cds/modifiers/tvfilm/acquisition_or_development_only/selected",    

        "cds/annual_tv/modifiers/jurisdiction",
        "cds/annual_tv/modifiers/australian",
        "cds/annual_tv/modifiers/lawyers",

        "cds/individual_tv/modifiers/jurisdiction",
        "cds/individual_tv/modifiers/policy_period",
        "cds/individual_tv/modifiers/soundtrack",
        "cds/individual_tv/modifiers/merchandising",
        "cds/individual_tv/modifiers/australian",
        "cds/individual_tv/modifiers/coverage_basis",
        "cds/individual_tv/modifiers/established_format",
        "cds/individual_tv/modifiers/primary_broadcast",
        "cds/individual_tv/modifiers/lawyers",
        "cds/individual_tv/modifiers/webisodes",
        "cds/individual_tv/modifiers/genre",
        "cds/individual_tv/modifiers/number_of_episodes",

        "cds/individual_film/modifiers/budget",
        "cds/individual_film/modifiers/cast",
        "cds/individual_film/modifiers/appeal",
        "cds/individual_film/modifiers/subject_matter",
        "cds/individual_film/modifiers/jurisdiction",
        "cds/individual_film/modifiers/foreign_language",
        "cds/individual_film/modifiers/soundtrack",
        "cds/individual_film/modifiers/merchandising",
        "cds/individual_film/modifiers/policy_period",
        "cds/individual_film/modifiers/australian",
        "cds/individual_film/modifiers/coverage_basis",
        "cds/individual_film/modifiers/established_format",
        "cds/individual_film/modifiers/lawyers",
        "cds/individual_film/modifiers/exhibition"

    ]
    return risk_char_change_path

def deductible_change_list():
    deductible_change_path = [

        "cds/layers/deductible",
        "cds/layers/excess",
        "cds/layers/attachment",
        "cds/options/retention",
        "cds/primary/attachment",

        # For nonstandard coverages:
        "cds/options/aggregate_excess",
        "cds/options/eec_excess",

        # IR: include these here?
        "cds/rating_factors/ilf_curve",
        # "cds/rating_factors/guideline_deductible"

    ]
    return deductible_change_path


def limit_change_list():
    limit_change_path = [

        "cds/layers/limit",
        "cds/layers/aggregate_limit",

        "cds/options/eec_limit",
        "cds/options/aggregate_limit",

        "cds/primary/aggregate_limit_view",

    ]
    return limit_change_path

def t_and_cs_change_list():
    t_and_cs_change_path = [

        "cds/rating_factors/policy_term",

        "cds/modifiers/optional_coverages/info_sec_liability/included",
        "cds/modifiers/optional_coverages/tech_eo/included",
        "cds/modifiers/optional_coverages/info_sec_liability/output",
        "cds/modifiers/optional_coverages/tech_eo/output",

    ]
    return t_and_cs_change_path

def other_change_list():
    other_change_path = [
        "cds/layers/brokerage",
        "cds/modifiers/extended_reporting_period/factor"
    ]
    return other_change_path