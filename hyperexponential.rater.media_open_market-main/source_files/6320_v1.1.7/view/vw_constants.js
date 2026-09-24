// If changing the max_layers below, you must also update in rate_constants to the same number
function max_layers() {
  return 11
}

function max_options() {
  return 10
}

function media_exposures() {
  return [
    { datum: "advert_agency", labelAlign: "left" },
    { datum: "public_relations", labelAlign: "left" },
    { datum: "market_research", labelAlign: "left" },
    { datum: "misc_advert", labelAlign: "left" },
    { datum: "other1", labelAlign: "left" },
    null,
    { datum: "production_companies", labelAlign: "left" },
    { datum: "other2", labelAlign: "left" },
    null,
    { datum: "social_low", labelAlign: "left" },
    { datum: "publishing_low", labelAlign: "left" },
    { datum: "radio", labelAlign: "left" },
    { datum: "other3", labelAlign: "left" },
    null,
    { datum: "social_medium", labelAlign: "left" },
    { datum: "publishing_medium", labelAlign: "left" },
    { datum: "other4", labelAlign: "left" },
    null,
    { datum: "social_celeb", labelAlign: "left" },
    { datum: "publishing_high", labelAlign: "left" },
    { datum: "other5", labelAlign: "left" },
    null,
    { datum: "publishing_severe", labelAlign: "left" },
    { datum: "other6", labelAlign: "left" },
  ]
}

function music_exposures() {
  return [
    { datum: "other1", labelAlign: "left" },
    null,
    { datum: "other2", labelAlign: "left" },
    null,
    { datum: "composer_low", labelAlign: "left" },
    { datum: "artist_low", labelAlign: "left" },
    { datum: "record_label_low", labelAlign: "left" },
    { datum: "other3", labelAlign: "left" },
    null,
    { datum: "composer_medium", labelAlign: "left" },
    { datum: "artist_medium", labelAlign: "left" },
    { datum: "record_label_medium", labelAlign: "left" },
    { datum: "music_talent", labelAlign: "left" },
    { datum: "other4", labelAlign: "left" },
    null,
    { datum: "composer_high", labelAlign: "left" },
    { datum: "artist_high", labelAlign: "left" },
    { datum: "record_label_high", labelAlign: "left" },
    { datum: "other5", labelAlign: "left" },
    null,
    { datum: "composer_severe", labelAlign: "left" },
    { datum: "licensing", labelAlign: "left" },
    { datum: "streaming", labelAlign: "left" },
    { datum: "royalties", labelAlign: "left" },
    { datum: "supervision", labelAlign: "left" },
    { datum: "other6", labelAlign: "left" },
  ]
}

function tvfilm_exposures() {
  return [
    { datum: "other1", labelAlign: "left" },
    null,
    { datum: "production2", labelAlign: "left" },
    { datum: "broadcast2", labelAlign: "left" },
    { datum: "distribution_verylow", labelAlign: "left" },
    { datum: "other2", labelAlign: "left" },
    null,
    { datum: "production3", labelAlign: "left" },
    { datum: "broadcast3", labelAlign: "left" },
    { datum: "distribution_low", labelAlign: "left" },
    { datum: "other3", labelAlign: "left" },
    null,
    { datum: "production4", labelAlign: "left" },
    { datum: "broadcast4", labelAlign: "left" },
    { datum: "distribution_medium", labelAlign: "left" },
    { datum: "other4", labelAlign: "left" },
    null,
    { datum: "production5", labelAlign: "left" },
    { datum: "broadcast5", labelAlign: "left" },
    { datum: "distribution_high", labelAlign: "left" },
    { datum: "other5", labelAlign: "left" },
    null,
    { datum: "production6", labelAlign: "left" },
    { datum: "broadcast6", labelAlign: "left" },
    { datum: "distribution_veryhigh", labelAlign: "left" },
    { datum: "other6", labelAlign: "left" },
  ]
}

function media_schedule_mods() {
  return [
    { datum: "media_review_control_procedures", labelAlign: "left" },
    { datum: "qualifications_inhouse_counsel", labelAlign: "left" },
    { datum: "geographical_scope", labelAlign: "left" },
    { datum: "popularity", labelAlign: "left" },
    { datum: "use_of_standard_contracts", labelAlign: "left" },
    { datum: "contract_sizes", labelAlign: "left" },
    { datum: "proportion_of_own_content", labelAlign: "left" },
    { datum: "contingent_bi_pd_exposure", labelAlign: "left" },
    { datum: "us_exposure", labelAlign: "left" },
  ]
}

function music_schedule_mods() {
  return [
    { datum: "contract_sizes", labelAlign: "left" },
    { datum: "us_exposure", labelAlign: "left" },
    { datum: "popularity", labelAlign: "left" },
    { datum: "size_of_back_catalogue", labelAlign: "left" },
    { datum: "high_volume_of_licensing", labelAlign: "left" },
  ]
}

function tvfilm_schedule_mods() {
  return [
    { datum: "three_year_cover", labelAlign: "left" },
    { datum: "popularity", labelAlign: "left" },
    { datum: "average_budget", labelAlign: "left" },
    { datum: "max_budget", labelAlign: "left" },
    { datum: "fair_use_exposure", labelAlign: "left" },
    { datum: "ability_to_subrogate", labelAlign: "left" },
    { datum: "quality_of_legal_clearance", labelAlign: "left" },
    { datum: "acquisition_or_development_only", labelAlign: "left" },
  ]
}

function optional_coverages() {
  return [
    { datum: "info_sec_liability", labelAlign: "left" },
    { datum: "tech_eo", labelAlign: "left" },
    { datum: "false_advertising", labelAlign: "left" },
  ]
}

function annualtv_genre() {
  return [
    { datum: "children_religious", labelAlign: "left" },
    { datum: "drama_chat", labelAlign: "left" },
    { datum: "live", labelAlign: "left" },
    { datum: "entertainment_sitcom", labelAlign: "left" },
    { datum: "factual_investigative", labelAlign: "left" },
    { datum: "factual_non_investigative", labelAlign: "left" },
    { datum: "factual_contentious", labelAlign: "left" },
    { datum: "films_for_tv", labelAlign: "left" },
    { datum: "game_show", labelAlign: "left" },
    { datum: "reality", labelAlign: "left" },
    { datum: "sport_history_nature", labelAlign: "left" },
  ]
}

export {
  max_layers, max_options,
  media_exposures, music_exposures, tvfilm_exposures,
  media_schedule_mods, music_schedule_mods, tvfilm_schedule_mods, optional_coverages,
  annualtv_genre
};