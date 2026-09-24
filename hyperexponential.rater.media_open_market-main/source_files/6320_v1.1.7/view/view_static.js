
throw new Error(`This file is generated

Do not edit manually as all of the changes will be lost.
This is the static version of your View that will allow easier debugging.
`);

import * as HX from "hx-model-components";


function hx_calculation_legacy_initial_premium_view(props) {
  return (
    <HX.Root>
      <HX.Page title="Landing Page"
        shownBy="model_state/show_landing_page">
        <HX.Section title="Start Policy">
          <HX.Pane flow="right">
            <HX.Pane ratio={2}>
              <HX.Notes field="model_state/landing_page_info" />
            </HX.Pane>
            <HX.Pane>
              <HX.Button task="start_renewal_task"
                title="Start Policy" />
            </HX.Pane>
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Risk Information"
        shownBy="model_state/show_after_landing_page">
        <HX.Section title="Account Details">
          <HX.Pane>
            <HX.Collection fields={[
              "hx_core/inception_date",
              "hx_core/expiry_date",
              "cds/retroactive_date",
              "cds/application_date"
            ]}
              horizontal={true} />
            <HX.Collection fields={[
              "underwriter",
              "insured_name"
            ]}
              with="cds/standard_fields"
              horizontal={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Risk Details">
          <HX.Pane>
            <HX.Collection fields={[
              "cds/currencies/source_currency",
              "cds/standard_fields/is_renewal"
            ]}
              horizontal={true} />
            <HX.Collection fields={[
              "clearance_status",
              "coverage_name"
            ]}
              with="cds"
              horizontal={true} />
            <HX.Collection fields={[
              "clearance_date",
              "is_binder"
            ]}
              with="cds"
              horizontal={true} />
            <HX.Collection fields={[
              null,
              "cyber_code"
            ]}
              with="cds"
              horizontal={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Broker Details">
          <HX.Collection fields={[
            "cds/standard_fields/broker",
            "cds/broker_contact"
          ]}
            horizontal={true} />
        </HX.Section>
        <HX.Section title="Comments">
          <HX.Collection fields={[
            "cds/riskinfo_comments"
          ]} />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Exposure Details"
        fullWidth={true}
        viewScale={1}
        shownBy="model_state/show_after_landing_page">
        <HX.Section title="Exposure Details">
          <HX.Pane shownBy="/cds/standard_rater_masking">
            <HX.Collection fields={[
              "years_in_business",
              null,
              null,
              null
            ]}
              with="cds/rating_factors"
              horizontal={true} />
            <HX.Collection fields={[
              "location",
              "territory_factor",
              null,
              null
            ]}
              with="cds/rating_factors"
              horizontal={true} />
            <HX.Collection fields={[
              "total_revenue",
              null,
              null,
              null
            ]}
              with="cds/exposure/aggregate"
              horizontal={true} />
            <HX.Collection fields={[
              "revenue",
              "base_rate",
              null,
              null
            ]}
              with="cds/exposure/aggregate/rateable"
              horizontal={true} />
            <HX.Collection fields={[
              "nonrateable/revenue",
              "nonrateable/base_rate",
              "hazard_group",
              null
            ]}
              with="cds/exposure/aggregate"
              horizontal={true} />
          </HX.Pane>
          <HX.Table shownBy="/cds/media_masking"
            title=""
            data={[
            {
              "datum": "advert_agency",
              "labelAlign": "left"
            },
            {
              "datum": "public_relations",
              "labelAlign": "left"
            },
            {
              "datum": "market_research",
              "labelAlign": "left"
            },
            {
              "datum": "misc_advert",
              "labelAlign": "left"
            },
            {
              "datum": "other1",
              "labelAlign": "left"
            },
            null,
            {
              "datum": "production_companies",
              "labelAlign": "left"
            },
            {
              "datum": "other2",
              "labelAlign": "left"
            },
            null,
            {
              "datum": "social_low",
              "labelAlign": "left"
            },
            {
              "datum": "publishing_low",
              "labelAlign": "left"
            },
            {
              "datum": "radio",
              "labelAlign": "left"
            },
            {
              "datum": "other3",
              "labelAlign": "left"
            },
            null,
            {
              "datum": "social_medium",
              "labelAlign": "left"
            },
            {
              "datum": "publishing_medium",
              "labelAlign": "left"
            },
            {
              "datum": "other4",
              "labelAlign": "left"
            },
            null,
            {
              "datum": "social_celeb",
              "labelAlign": "left"
            },
            {
              "datum": "publishing_high",
              "labelAlign": "left"
            },
            {
              "datum": "other5",
              "labelAlign": "left"
            },
            null,
            {
              "datum": "publishing_severe",
              "labelAlign": "left"
            },
            {
              "datum": "other6",
              "labelAlign": "left"
            }
          ]}
            fields={[
            {
              "field": "base_rate",
              "maxWidth": 300
            },
            {
              "field": "comment",
              "maxWidth": 900
            }
          ]}
            with="cds/exposure/granular/media"
            kb-interactive={true} />
          <HX.Table shownBy="/cds/music_masking"
            title=""
            data={[
            {
              "datum": "other1",
              "labelAlign": "left"
            },
            null,
            {
              "datum": "other2",
              "labelAlign": "left"
            },
            null,
            {
              "datum": "composer_low",
              "labelAlign": "left"
            },
            {
              "datum": "artist_low",
              "labelAlign": "left"
            },
            {
              "datum": "record_label_low",
              "labelAlign": "left"
            },
            {
              "datum": "other3",
              "labelAlign": "left"
            },
            null,
            {
              "datum": "composer_medium",
              "labelAlign": "left"
            },
            {
              "datum": "artist_medium",
              "labelAlign": "left"
            },
            {
              "datum": "record_label_medium",
              "labelAlign": "left"
            },
            {
              "datum": "music_talent",
              "labelAlign": "left"
            },
            {
              "datum": "other4",
              "labelAlign": "left"
            },
            null,
            {
              "datum": "composer_high",
              "labelAlign": "left"
            },
            {
              "datum": "artist_high",
              "labelAlign": "left"
            },
            {
              "datum": "record_label_high",
              "labelAlign": "left"
            },
            {
              "datum": "other5",
              "labelAlign": "left"
            },
            null,
            {
              "datum": "composer_severe",
              "labelAlign": "left"
            },
            {
              "datum": "licensing",
              "labelAlign": "left"
            },
            {
              "datum": "streaming",
              "labelAlign": "left"
            },
            {
              "datum": "royalties",
              "labelAlign": "left"
            },
            {
              "datum": "supervision",
              "labelAlign": "left"
            },
            {
              "datum": "other6",
              "labelAlign": "left"
            }
          ]}
            fields={[
            {
              "field": "base_rate",
              "maxWidth": 300
            },
            {
              "field": "comment",
              "maxWidth": 900
            }
          ]}
            with="cds/exposure/granular/music"
            kb-interactive={true} />
          <HX.Table shownBy="/cds/tvfilm_masking"
            title=""
            data={[
            {
              "datum": "other1",
              "labelAlign": "left"
            },
            null,
            {
              "datum": "production2",
              "labelAlign": "left"
            },
            {
              "datum": "broadcast2",
              "labelAlign": "left"
            },
            {
              "datum": "distribution_verylow",
              "labelAlign": "left"
            },
            {
              "datum": "other2",
              "labelAlign": "left"
            },
            null,
            {
              "datum": "production3",
              "labelAlign": "left"
            },
            {
              "datum": "broadcast3",
              "labelAlign": "left"
            },
            {
              "datum": "distribution_low",
              "labelAlign": "left"
            },
            {
              "datum": "other3",
              "labelAlign": "left"
            },
            null,
            {
              "datum": "production4",
              "labelAlign": "left"
            },
            {
              "datum": "broadcast4",
              "labelAlign": "left"
            },
            {
              "datum": "distribution_medium",
              "labelAlign": "left"
            },
            {
              "datum": "other4",
              "labelAlign": "left"
            },
            null,
            {
              "datum": "production5",
              "labelAlign": "left"
            },
            {
              "datum": "broadcast5",
              "labelAlign": "left"
            },
            {
              "datum": "distribution_high",
              "labelAlign": "left"
            },
            {
              "datum": "other5",
              "labelAlign": "left"
            },
            null,
            {
              "datum": "production6",
              "labelAlign": "left"
            },
            {
              "datum": "broadcast6",
              "labelAlign": "left"
            },
            {
              "datum": "distribution_veryhigh",
              "labelAlign": "left"
            },
            {
              "datum": "other6",
              "labelAlign": "left"
            }
          ]}
            fields={[
            {
              "field": "base_rate",
              "maxWidth": 300
            },
            {
              "field": "comment",
              "maxWidth": 900
            }
          ]}
            with="cds/exposure/granular/tvfilm"
            kb-interactive={true} />
          <HX.Pane shownBy="/cds/individualtv_masking">
            <HX.Collection fields={[
              "location",
              "territory_factor",
              null,
              null
            ]}
              with="cds/rating_factors"
              horizontal={true} />
            <HX.Collection fields={[
              "length",
              "number_of_episodes",
              null,
              null
            ]}
              with="cds/exposure/aggregate/individual_tv"
              horizontal={true} />
            <HX.Collection fields={[
              "individual_tv/selections/genre",
              "exposure/aggregate/total_base_premium",
              null,
              null
            ]}
              with="cds"
              horizontal={true} />
            <HX.Table title="Individual TV Modifiers"
              data={[
              {
                "datum": "selections",
                "maxWidth": 400
              },
              {
                "datum": "modifiers",
                "maxWidth": 400
              }
            ]}
              with="cds/individual_tv"
              fields={[
              {
                "field": "jurisdiction",
                "labelAlign": "left"
              },
              {
                "field": "policy_period",
                "labelAlign": "left"
              },
              {
                "field": "soundtrack",
                "labelAlign": "left"
              },
              {
                "field": "merchandising",
                "labelAlign": "left"
              },
              {
                "field": "australian",
                "labelAlign": "left"
              },
              {
                "field": "coverage_basis",
                "labelAlign": "left"
              },
              {
                "field": "established_format",
                "labelAlign": "left"
              },
              {
                "field": "primary_broadcast",
                "labelAlign": "left"
              },
              {
                "field": "lawyers",
                "labelAlign": "left"
              },
              {
                "field": "webisodes",
                "labelAlign": "left"
              }
            ]}
              kb-interactive={true}
              transpose={true}
              syncColumnWidthsKey="mySyncedTables1" />
          </HX.Pane>
          <HX.Pane shownBy="/cds/annualtv_masking">
            <HX.Collection horizontal={true}
              syncColumnWidthsKey="mySyncedTables1"
              fields={[
              "location",
              "territory_factor",
              null,
              null
            ]}
              with="cds/rating_factors" />
            <HX.Collection syncColumnWidthsKey="mySyncedTables1"
              fields={[
              "turnover",
              "annual_budget"
            ]}
              with="cds/annual_tv" />
            <HX.Collection horizontal={true}
              syncColumnWidthsKey="mySyncedTables1"
              fields={[
              "number_of_productions",
              "capped_productions"
            ]}
              with="cds/exposure/aggregate/annual_tv" />
            <HX.Table title="Genre"
              data={[
              {
                "datum": "children_religious",
                "labelAlign": "left"
              },
              {
                "datum": "drama_chat",
                "labelAlign": "left"
              },
              {
                "datum": "live",
                "labelAlign": "left"
              },
              {
                "datum": "entertainment_sitcom",
                "labelAlign": "left"
              },
              {
                "datum": "factual_investigative",
                "labelAlign": "left"
              },
              {
                "datum": "factual_non_investigative",
                "labelAlign": "left"
              },
              {
                "datum": "factual_contentious",
                "labelAlign": "left"
              },
              {
                "datum": "films_for_tv",
                "labelAlign": "left"
              },
              {
                "datum": "game_show",
                "labelAlign": "left"
              },
              {
                "datum": "reality",
                "labelAlign": "left"
              },
              {
                "datum": "sport_history_nature",
                "labelAlign": "left"
              }
            ]}
              with="cds/exposure/granular/annual_tv/genre"
              fields={[
              {
                "field": "perc_of_total_turnover",
                "width": 250
              },
              {
                "field": "turnover_amount",
                "width": 180
              },
              {
                "field": "alloc_production_number",
                "width": 250
              },
              {
                "field": "average_premium",
                "width": 180
              },
              {
                "field": "base_premium",
                "width": 180
              }
            ]}
              kb-interactive={true} />
            <HX.Collection horizontal={true}
              syncColumnWidthsKey="mySyncedTables1"
              fields={[
              "total_base_premium",
              null,
              null,
              null
            ]}
              with="cds/exposure/aggregate" />
            <HX.Table title="Annual TV Modifiers"
              data={[
              {
                "datum": "selections",
                "maxWidth": 400
              },
              {
                "datum": "modifiers",
                "maxWidth": 400
              }
            ]}
              with="cds/annual_tv"
              fields={[
              {
                "field": "jurisdiction",
                "labelAlign": "left"
              },
              {
                "field": "australian",
                "labelAlign": "left"
              },
              {
                "field": "lawyers",
                "labelAlign": "left"
              }
            ]}
              kb-interactive={true}
              transpose={true} />
          </HX.Pane>
          <HX.Pane shownBy="/cds/individualfilm_masking">
            <HX.Collection fields={[
              "location",
              "territory_factor",
              null,
              null
            ]}
              with="cds/rating_factors"
              horizontal={true} />
            <HX.Collection fields={[
              "individual_film/exhibition",
              "total_base_premium",
              null,
              null
            ]}
              with="cds/exposure/aggregate"
              horizontal={true} />
            <HX.Table title="Individual Film Modifiers"
              data={[
              {
                "datum": "selections",
                "maxWidth": 400
              },
              {
                "datum": "modifiers",
                "maxWidth": 400
              }
            ]}
              with="cds/individual_film"
              fields={[
              {
                "field": "budget",
                "labelAlign": "left"
              },
              {
                "field": "cast",
                "labelAlign": "left"
              },
              {
                "field": "appeal",
                "labelAlign": "left"
              },
              {
                "field": "subject_matter",
                "labelAlign": "left"
              },
              {
                "field": "jurisdiction",
                "labelAlign": "left"
              },
              {
                "field": "foreign_language",
                "labelAlign": "left"
              },
              {
                "field": "soundtrack",
                "labelAlign": "left"
              },
              {
                "field": "merchandising",
                "labelAlign": "left"
              },
              {
                "field": "policy_period",
                "labelAlign": "left"
              },
              {
                "field": "australian",
                "labelAlign": "left"
              },
              {
                "field": "coverage_basis",
                "labelAlign": "left"
              },
              {
                "field": "established_format",
                "labelAlign": "left"
              },
              {
                "field": "lawyers",
                "labelAlign": "left"
              }
            ]}
              kb-interactive={true}
              transpose={true}
              syncColumnWidthsKey="mySyncedTables1" />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Adjustments"
        fullWidth={true}
        viewScale={1}
        shownBy="cds/standard_rater_masking">
        <HX.Section title="Longevity and Experience Factors">
          <HX.Pane>
            <HX.Collection fields={[
              "longevity_factor",
              null,
              null
            ]}
              horizontal={true}
              with="cds/modifiers" />
            <HX.Collection title="Experience Factor"
              fields={[
              "response",
              "selected",
              "min",
              "max"
            ]}
              horizontal={true}
              with="cds/modifiers/experience_factor" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Schedule Rating">
          <HX.Pane>
            <HX.Table shownBy="/cds/media_masking"
              data={[
              {
                "datum": "media_review_control_procedures",
                "labelAlign": "left"
              },
              {
                "datum": "qualifications_inhouse_counsel",
                "labelAlign": "left"
              },
              {
                "datum": "geographical_scope",
                "labelAlign": "left"
              },
              {
                "datum": "popularity",
                "labelAlign": "left"
              },
              {
                "datum": "use_of_standard_contracts",
                "labelAlign": "left"
              },
              {
                "datum": "contract_sizes",
                "labelAlign": "left"
              },
              {
                "datum": "proportion_of_own_content",
                "labelAlign": "left"
              },
              {
                "datum": "contingent_bi_pd_exposure",
                "labelAlign": "left"
              },
              {
                "datum": "us_exposure",
                "labelAlign": "left"
              }
            ]}
              fields={[
              {
                "field": "selected",
                "width": 180
              },
              {
                "field": "min",
                "width": 180
              },
              {
                "field": "max",
                "width": 180
              }
            ]}
              with="cds/modifiers/media"
              kb-interactive={true} />
            <HX.Table shownBy="/cds/music_masking"
              data={[
              {
                "datum": "contract_sizes",
                "labelAlign": "left"
              },
              {
                "datum": "us_exposure",
                "labelAlign": "left"
              },
              {
                "datum": "popularity",
                "labelAlign": "left"
              },
              {
                "datum": "size_of_back_catalogue",
                "labelAlign": "left"
              },
              {
                "datum": "high_volume_of_licensing",
                "labelAlign": "left"
              }
            ]}
              fields={[
              {
                "field": "selected",
                "width": 180
              },
              {
                "field": "min",
                "width": 180
              },
              {
                "field": "max",
                "width": 180
              }
            ]}
              with="cds/modifiers/music"
              kb-interactive={true} />
            <HX.Table shownBy="/cds/tvfilm_masking"
              data={[
              {
                "datum": "three_year_cover",
                "labelAlign": "left"
              },
              {
                "datum": "popularity",
                "labelAlign": "left"
              },
              {
                "datum": "average_budget",
                "labelAlign": "left"
              },
              {
                "datum": "max_budget",
                "labelAlign": "left"
              },
              {
                "datum": "fair_use_exposure",
                "labelAlign": "left"
              },
              {
                "datum": "ability_to_subrogate",
                "labelAlign": "left"
              },
              {
                "datum": "quality_of_legal_clearance",
                "labelAlign": "left"
              },
              {
                "datum": "acquisition_or_development_only",
                "labelAlign": "left"
              }
            ]}
              fields={[
              {
                "field": "selected",
                "width": 180
              },
              {
                "field": "min",
                "width": 180
              },
              {
                "field": "max",
                "width": 180
              }
            ]}
              with="cds/modifiers/tvfilm"
              kb-interactive={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Optional Coverages">
          <HX.Pane>
            <HX.Table data={[
              {
                "datum": "info_sec_liability",
                "labelAlign": "left"
              },
              {
                "datum": "tech_eo",
                "labelAlign": "left"
              },
              {
                "datum": "false_advertising",
                "labelAlign": "left"
              }
            ]}
              fields={[
              "included",
              "selected",
              "min",
              "max",
              "comment"
            ]}
              with="cds/modifiers/optional_coverages"
              kb-interactive={true} />
            <HX.Collection title="Extended Reporting Period"
              fields={[
              "length",
              "factor"
            ]}
              horizontal={true}
              with="cds/modifiers/extended_reporting_period" />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Rating Summary"
        fullWidth={true}
        viewScale={1}
        shownBy="model_state/show_after_landing_page">
        <HX.Section title="Rating Methodology">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "cds/standard_fields/rating_methodology"
            ]} />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Coverage Options"
          shownBy="cds/standard_fields/is_case_priced">
          <HX.Table title="Priced Quotes"
            data={[
            {
              "datum": "cds/layers",
              "elementLabelBy": "layer_label",
              "labelAlign": "left"
            }
          ]}
            fields={[
            {
              "field": "status_view",
              "width": 200
            },
            {
              "field": "section_reference_view",
              "width": 200
            },
            {
              "field": "brokerage_input",
              "width": 200
            },
            {
              "field": "written_line_input",
              "width": 200
            },
            null,
            {
              "field": "quoted_premium_view",
              "width": 200
            },
            {
              "field": "technical_premium",
              "width": 200
            },
            {
              "field": "benchmark_premium",
              "width": 200
            },
            null,
            {
              "field": "tpi",
              "width": 200
            },
            {
              "field": "bpi_case_priced",
              "shownBy": "cds/standard_fields/is_case_priced",
              "width": 200
            },
            null,
            {
              "field": "pflr",
              "width": 200
            },
            {
              "field": "roc",
              "width": 200
            }
          ]}
            freezeLeft={0}
            kb-interactive={true} />
        </HX.Section>
        <HX.Section title="Case Pricing Analysis Filepath"
          shownBy="cds/standard_fields/is_case_priced">
          <HX.Notes field="cds/case_pricing_analysis_location" />
        </HX.Section>
        <HX.Section title="Primary Layer Options"
          shownBy="cds/standard_fields/is_rater_priced">
          <HX.Table title="Coverages"
            syncColumnWidthsKey="mySyncedTables1"
            data={[
            {
              "datum": "cds/options",
              "elementLabelBy": "option_label"
            }
          ]}
            fields={[
            {
              "field": "eec_limit",
              "labelAlign": "left"
            },
            {
              "field": "aggregate_limit",
              "labelAlign": "left"
            },
            {
              "field": "retention",
              "labelAlign": "left"
            }
          ]}
            kb-interactive={true}
            transpose={true}
            shownBy="cds/rater_priced_standard" />
          <HX.Table title="Coverages"
            syncColumnWidthsKey="mySyncedTables1"
            data={[
            {
              "datum": "cds/options",
              "elementLabelBy": "option_label"
            }
          ]}
            fields={[
            {
              "field": "eec_limit",
              "labelAlign": "left"
            },
            {
              "field": "aggregate_limit",
              "labelAlign": "left"
            },
            {
              "field": "eec_excess",
              "labelAlign": "left"
            }
          ]}
            kb-interactive={true}
            transpose={true}
            shownBy="cds/rater_priced_nonstandard" />
          <HX.Collection fields={[
            "cds/rating_factors/guideline_deductible",
            null,
            null,
            null,
            null
          ]}
            horizontal={true}
            syncColumnWidthsKey="mySyncedTables1"
            shownBy="cds/rater_priced_standard" />
          <HX.Collection fields={[
            "cds/rating_factors/ilf_curve",
            null,
            null,
            null,
            null
          ]}
            horizontal={true}
            syncColumnWidthsKey="mySyncedTables1"
            shownBy="cds/rater_priced_standard" />
          <HX.Table title="Primary Layer Details"
            syncColumnWidthsKey="mySyncedTables1"
            data={[
            {
              "datum": "cds/options",
              "elementLabelBy": "option_label"
            }
          ]}
            fields={[
            {
              "field": "technical_premium",
              "labelAlign": "left"
            },
            {
              "field": "benchmark_premium",
              "labelAlign": "left"
            },
            {
              "field": "quoted_premium",
              "labelAlign": "left"
            },
            {
              "field": "quoted_bpi",
              "labelAlign": "left"
            }
          ]}
            kb-interactive={true}
            transpose={true} />
          <HX.Collection syncColumnWidthsKey="mySyncedTables1"
            fields={[
            "cds/option_selected"
          ]} />
        </HX.Section>
        <HX.Section title="Primary Layer"
          shownBy="cds/standard_fields/is_rater_priced">
          <HX.Pane>
            <HX.Table syncColumnWidthsKey="mySyncedTables1"
              data={[
              {
                "datum": "primary",
                "elementLabelBy": "layer_label",
                "labelAlign": "left"
              }
            ]}
              with="cds"
              fields={[
              "brokerage",
              "quoted_premium_view",
              "bound_premium_input",
              "status",
              "section_reference",
              "benchmark_premium",
              "technical_premium",
              "bpi",
              "tpi"
            ]} />
          </HX.Pane>
          <HX.Pane shownBy="cds/coverage_selected_flag">
            <HX.Collection horizontal={true}
              syncColumnWidthsKey="mySyncedTables1"
              fields={[
              "cds/price_excess_flag"
            ]} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Excess Pricing"
          shownBy="cds/rater_priced_excess">
          <HX.Table title=""
            syncColumnWidthsKey="mySyncedTables1"
            data={[
            {
              "datum": "cds/primary",
              "elementLabelBy": "layer_label",
              "labelAlign": "left"
            },
            {
              "datum": "cds/layers",
              "elementLabelBy": "layer_label",
              "labelAlign": "left"
            }
          ]}
            fields={[
            "aggregate_limit_view",
            "attachment",
            "quoted_premium_view",
            "bound_premium",
            "status_view",
            "section_reference_view"
          ]}
            kb-interactive={true}
            freezeLeft={0}
            filter="excess_flag" />
          <HX.Table title=""
            syncColumnWidthsKey="mySyncedTables1"
            data={[
            {
              "datum": "cds/layers",
              "elementLabelBy": "layer_label",
              "labelAlign": "left"
            }
          ]}
            fields={[
            "benchmark_premium",
            "technical_premium",
            "implied_price_per_m",
            "implied_ilf",
            "brokerage_input",
            "carrier",
            "quoted_price_per_m",
            "quoted_ilf",
            "bpi",
            "tpi"
          ]}
            kb-interactive={true}
            freezeLeft={0} />
          <HX.Notes field="cds/excess_pricing_note"
            title="Excess Pricing Notes" />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Rate Change"
        fullWidth={false}
        shownBy="model_state/show_rate_change">
        <HX.Section title="Fetch Expiring Policy">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "cds/rate_change/expiring_policy_option_id",
              null
            ]}
              horizontal={true} />
          </HX.Pane>
          <HX.Pane>
            <HX.Table title="Deal Status by Renewal Layers"
              data={[
              {
                "datum": "cds/layers",
                "width": 200
              }
            ]}
              fields={[
              {
                "field": "status"
              }
            ]}
              transpose={true} />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Button task="expiring_policy_fetch_task"
              title="Fetch Expiring Data"
              shownBy="cds/rate_change/has_rarc_not_run" />
            <HX.Pane shownBy="cds/standard_fields/is_case_priced" />
            <HX.Pane shownBy="cds/rate_change/has_rarc_run" />
            <HX.Button title="Calculate Rate Change"
              task="rarc_task"
              shownBy="cds/standard_fields/is_rater_priced" />
          </HX.Pane>
          <HX.Pane>
            <HX.Notes with="cds/rate_change"
              field="rarc_run_again_message"
              shownBy="rarc_message_show" />
          </HX.Pane>
          <HX.Section title="Rate Change Instructions and Key"
            defaultCollapsed={true}>
            <HX.Pane flow="right">
              <HX.Notes field="cds/rate_change/instructions" />
            </HX.Pane>
          </HX.Section>
        </HX.Section>
        <HX.Section title="Renewal Layer 1"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_1">
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Collection fields={[
                "rate_change/expiring_layer",
                null,
                null
              ]}
                horizontal={true} />
              <HX.Table data={[
                "premium/line_100pct/annualised",
                "premium/beazley_line/annualised",
                "attachment",
                "aggregate_limit",
                "brokerage",
                "currency"
              ]}
                fields={[
                {
                  "field": "expiring",
                  "width": 160
                },
                {
                  "field": "expiring_revalued",
                  "shownBy": "show_expiring_revalued",
                  "width": 160
                },
                {
                  "field": "renewal",
                  "width": 160
                }
              ]}
                with="rate_change" />
              <HX.Table shownBy="/cds/standard_fields/is_rater_priced"
                data={[
                "exposure_change",
                "risk_characteristics_change",
                "deductible_change",
                "limit_change",
                "terms_conditions_change",
                "other_change",
                null,
                "rate_change"
              ]}
                fields={[
                {
                  "field": "model_calculated",
                  "width": 140
                },
                {
                  "field": "uw_override",
                  "width": 140
                },
                {
                  "field": "final",
                  "width": 140
                },
                {
                  "field": "comments",
                  "width": 250
                }
              ]}
                with="rate_change"
                syncColumnWidthsKey="syncRateChange"
                kb-interactive={true} />
              <HX.Collection title="Final Rate Change"
                fields={[
                {
                  "field": "rate_change/risk_adjusted_rate_change",
                  "shownBy": "/cds/standard_fields/is_rater_priced"
                },
                {
                  "field": "rate_change/risk_adjusted_rate_change_case_priced",
                  "shownBy": "/cds/standard_fields/is_case_priced"
                },
                null,
                null
              ]}
                horizontal={true} />
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Renewal Layer 2"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_2">
          <HX.With context={{
            "index": 1,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Collection fields={[
                "rate_change/expiring_layer",
                null,
                null
              ]}
                horizontal={true} />
              <HX.Table data={[
                "premium/line_100pct/annualised",
                "premium/beazley_line/annualised",
                "attachment",
                "aggregate_limit",
                "brokerage",
                "currency"
              ]}
                fields={[
                {
                  "field": "expiring",
                  "width": 160
                },
                {
                  "field": "expiring_revalued",
                  "shownBy": "show_expiring_revalued",
                  "width": 160
                },
                {
                  "field": "renewal",
                  "width": 160
                }
              ]}
                with="rate_change" />
              <HX.Table shownBy="/cds/standard_fields/is_rater_priced"
                data={[
                "exposure_change",
                "risk_characteristics_change",
                "deductible_change",
                "limit_change",
                "terms_conditions_change",
                "other_change",
                null,
                "rate_change"
              ]}
                fields={[
                {
                  "field": "model_calculated",
                  "width": 140
                },
                {
                  "field": "uw_override",
                  "width": 140
                },
                {
                  "field": "final",
                  "width": 140
                },
                {
                  "field": "comments",
                  "width": 250
                }
              ]}
                with="rate_change"
                syncColumnWidthsKey="syncRateChange"
                kb-interactive={true} />
              <HX.Collection title="Final Rate Change"
                fields={[
                {
                  "field": "rate_change/risk_adjusted_rate_change",
                  "shownBy": "/cds/standard_fields/is_rater_priced"
                },
                {
                  "field": "rate_change/risk_adjusted_rate_change_case_priced",
                  "shownBy": "/cds/standard_fields/is_case_priced"
                },
                null,
                null
              ]}
                horizontal={true} />
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Renewal Layer 3"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_3">
          <HX.With context={{
            "index": 2,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Collection fields={[
                "rate_change/expiring_layer",
                null,
                null
              ]}
                horizontal={true} />
              <HX.Table data={[
                "premium/line_100pct/annualised",
                "premium/beazley_line/annualised",
                "attachment",
                "aggregate_limit",
                "brokerage",
                "currency"
              ]}
                fields={[
                {
                  "field": "expiring",
                  "width": 160
                },
                {
                  "field": "expiring_revalued",
                  "shownBy": "show_expiring_revalued",
                  "width": 160
                },
                {
                  "field": "renewal",
                  "width": 160
                }
              ]}
                with="rate_change" />
              <HX.Table shownBy="/cds/standard_fields/is_rater_priced"
                data={[
                "exposure_change",
                "risk_characteristics_change",
                "deductible_change",
                "limit_change",
                "terms_conditions_change",
                "other_change",
                null,
                "rate_change"
              ]}
                fields={[
                {
                  "field": "model_calculated",
                  "width": 140
                },
                {
                  "field": "uw_override",
                  "width": 140
                },
                {
                  "field": "final",
                  "width": 140
                },
                {
                  "field": "comments",
                  "width": 250
                }
              ]}
                with="rate_change"
                syncColumnWidthsKey="syncRateChange"
                kb-interactive={true} />
              <HX.Collection title="Final Rate Change"
                fields={[
                {
                  "field": "rate_change/risk_adjusted_rate_change",
                  "shownBy": "/cds/standard_fields/is_rater_priced"
                },
                {
                  "field": "rate_change/risk_adjusted_rate_change_case_priced",
                  "shownBy": "/cds/standard_fields/is_case_priced"
                },
                null,
                null
              ]}
                horizontal={true} />
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Renewal Layer 4"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_4">
          <HX.With context={{
            "index": 3,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Collection fields={[
                "rate_change/expiring_layer",
                null,
                null
              ]}
                horizontal={true} />
              <HX.Table data={[
                "premium/line_100pct/annualised",
                "premium/beazley_line/annualised",
                "attachment",
                "aggregate_limit",
                "brokerage",
                "currency"
              ]}
                fields={[
                {
                  "field": "expiring",
                  "width": 160
                },
                {
                  "field": "expiring_revalued",
                  "shownBy": "show_expiring_revalued",
                  "width": 160
                },
                {
                  "field": "renewal",
                  "width": 160
                }
              ]}
                with="rate_change" />
              <HX.Table shownBy="/cds/standard_fields/is_rater_priced"
                data={[
                "exposure_change",
                "risk_characteristics_change",
                "deductible_change",
                "limit_change",
                "terms_conditions_change",
                "other_change",
                null,
                "rate_change"
              ]}
                fields={[
                {
                  "field": "model_calculated",
                  "width": 140
                },
                {
                  "field": "uw_override",
                  "width": 140
                },
                {
                  "field": "final",
                  "width": 140
                },
                {
                  "field": "comments",
                  "width": 250
                }
              ]}
                with="rate_change"
                syncColumnWidthsKey="syncRateChange"
                kb-interactive={true} />
              <HX.Collection title="Final Rate Change"
                fields={[
                {
                  "field": "rate_change/risk_adjusted_rate_change",
                  "shownBy": "/cds/standard_fields/is_rater_priced"
                },
                {
                  "field": "rate_change/risk_adjusted_rate_change_case_priced",
                  "shownBy": "/cds/standard_fields/is_case_priced"
                },
                null,
                null
              ]}
                horizontal={true} />
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Renewal Layer 5"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_5">
          <HX.With context={{
            "index": 4,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Collection fields={[
                "rate_change/expiring_layer",
                null,
                null
              ]}
                horizontal={true} />
              <HX.Table data={[
                "premium/line_100pct/annualised",
                "premium/beazley_line/annualised",
                "attachment",
                "aggregate_limit",
                "brokerage",
                "currency"
              ]}
                fields={[
                {
                  "field": "expiring",
                  "width": 160
                },
                {
                  "field": "expiring_revalued",
                  "shownBy": "show_expiring_revalued",
                  "width": 160
                },
                {
                  "field": "renewal",
                  "width": 160
                }
              ]}
                with="rate_change" />
              <HX.Table shownBy="/cds/standard_fields/is_rater_priced"
                data={[
                "exposure_change",
                "risk_characteristics_change",
                "deductible_change",
                "limit_change",
                "terms_conditions_change",
                "other_change",
                null,
                "rate_change"
              ]}
                fields={[
                {
                  "field": "model_calculated",
                  "width": 140
                },
                {
                  "field": "uw_override",
                  "width": 140
                },
                {
                  "field": "final",
                  "width": 140
                },
                {
                  "field": "comments",
                  "width": 250
                }
              ]}
                with="rate_change"
                syncColumnWidthsKey="syncRateChange"
                kb-interactive={true} />
              <HX.Collection title="Final Rate Change"
                fields={[
                {
                  "field": "rate_change/risk_adjusted_rate_change",
                  "shownBy": "/cds/standard_fields/is_rater_priced"
                },
                {
                  "field": "rate_change/risk_adjusted_rate_change_case_priced",
                  "shownBy": "/cds/standard_fields/is_case_priced"
                },
                null,
                null
              ]}
                horizontal={true} />
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Renewal Layer 6"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_6">
          <HX.With context={{
            "index": 5,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Collection fields={[
                "rate_change/expiring_layer",
                null,
                null
              ]}
                horizontal={true} />
              <HX.Table data={[
                "premium/line_100pct/annualised",
                "premium/beazley_line/annualised",
                "attachment",
                "aggregate_limit",
                "brokerage",
                "currency"
              ]}
                fields={[
                {
                  "field": "expiring",
                  "width": 160
                },
                {
                  "field": "expiring_revalued",
                  "shownBy": "show_expiring_revalued",
                  "width": 160
                },
                {
                  "field": "renewal",
                  "width": 160
                }
              ]}
                with="rate_change" />
              <HX.Table shownBy="/cds/standard_fields/is_rater_priced"
                data={[
                "exposure_change",
                "risk_characteristics_change",
                "deductible_change",
                "limit_change",
                "terms_conditions_change",
                "other_change",
                null,
                "rate_change"
              ]}
                fields={[
                {
                  "field": "model_calculated",
                  "width": 140
                },
                {
                  "field": "uw_override",
                  "width": 140
                },
                {
                  "field": "final",
                  "width": 140
                },
                {
                  "field": "comments",
                  "width": 250
                }
              ]}
                with="rate_change"
                syncColumnWidthsKey="syncRateChange"
                kb-interactive={true} />
              <HX.Collection title="Final Rate Change"
                fields={[
                {
                  "field": "rate_change/risk_adjusted_rate_change",
                  "shownBy": "/cds/standard_fields/is_rater_priced"
                },
                {
                  "field": "rate_change/risk_adjusted_rate_change_case_priced",
                  "shownBy": "/cds/standard_fields/is_case_priced"
                },
                null,
                null
              ]}
                horizontal={true} />
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Renewal Layer 7"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_7">
          <HX.With context={{
            "index": 6,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Collection fields={[
                "rate_change/expiring_layer",
                null,
                null
              ]}
                horizontal={true} />
              <HX.Table data={[
                "premium/line_100pct/annualised",
                "premium/beazley_line/annualised",
                "attachment",
                "aggregate_limit",
                "brokerage",
                "currency"
              ]}
                fields={[
                {
                  "field": "expiring",
                  "width": 160
                },
                {
                  "field": "expiring_revalued",
                  "shownBy": "show_expiring_revalued",
                  "width": 160
                },
                {
                  "field": "renewal",
                  "width": 160
                }
              ]}
                with="rate_change" />
              <HX.Table shownBy="/cds/standard_fields/is_rater_priced"
                data={[
                "exposure_change",
                "risk_characteristics_change",
                "deductible_change",
                "limit_change",
                "terms_conditions_change",
                "other_change",
                null,
                "rate_change"
              ]}
                fields={[
                {
                  "field": "model_calculated",
                  "width": 140
                },
                {
                  "field": "uw_override",
                  "width": 140
                },
                {
                  "field": "final",
                  "width": 140
                },
                {
                  "field": "comments",
                  "width": 250
                }
              ]}
                with="rate_change"
                syncColumnWidthsKey="syncRateChange"
                kb-interactive={true} />
              <HX.Collection title="Final Rate Change"
                fields={[
                {
                  "field": "rate_change/risk_adjusted_rate_change",
                  "shownBy": "/cds/standard_fields/is_rater_priced"
                },
                {
                  "field": "rate_change/risk_adjusted_rate_change_case_priced",
                  "shownBy": "/cds/standard_fields/is_case_priced"
                },
                null,
                null
              ]}
                horizontal={true} />
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Renewal Layer 8"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_8">
          <HX.With context={{
            "index": 7,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Collection fields={[
                "rate_change/expiring_layer",
                null,
                null
              ]}
                horizontal={true} />
              <HX.Table data={[
                "premium/line_100pct/annualised",
                "premium/beazley_line/annualised",
                "attachment",
                "aggregate_limit",
                "brokerage",
                "currency"
              ]}
                fields={[
                {
                  "field": "expiring",
                  "width": 160
                },
                {
                  "field": "expiring_revalued",
                  "shownBy": "show_expiring_revalued",
                  "width": 160
                },
                {
                  "field": "renewal",
                  "width": 160
                }
              ]}
                with="rate_change" />
              <HX.Table shownBy="/cds/standard_fields/is_rater_priced"
                data={[
                "exposure_change",
                "risk_characteristics_change",
                "deductible_change",
                "limit_change",
                "terms_conditions_change",
                "other_change",
                null,
                "rate_change"
              ]}
                fields={[
                {
                  "field": "model_calculated",
                  "width": 140
                },
                {
                  "field": "uw_override",
                  "width": 140
                },
                {
                  "field": "final",
                  "width": 140
                },
                {
                  "field": "comments",
                  "width": 250
                }
              ]}
                with="rate_change"
                syncColumnWidthsKey="syncRateChange"
                kb-interactive={true} />
              <HX.Collection title="Final Rate Change"
                fields={[
                {
                  "field": "rate_change/risk_adjusted_rate_change",
                  "shownBy": "/cds/standard_fields/is_rater_priced"
                },
                {
                  "field": "rate_change/risk_adjusted_rate_change_case_priced",
                  "shownBy": "/cds/standard_fields/is_case_priced"
                },
                null,
                null
              ]}
                horizontal={true} />
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Renewal Layer 9"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_9">
          <HX.With context={{
            "index": 8,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Collection fields={[
                "rate_change/expiring_layer",
                null,
                null
              ]}
                horizontal={true} />
              <HX.Table data={[
                "premium/line_100pct/annualised",
                "premium/beazley_line/annualised",
                "attachment",
                "aggregate_limit",
                "brokerage",
                "currency"
              ]}
                fields={[
                {
                  "field": "expiring",
                  "width": 160
                },
                {
                  "field": "expiring_revalued",
                  "shownBy": "show_expiring_revalued",
                  "width": 160
                },
                {
                  "field": "renewal",
                  "width": 160
                }
              ]}
                with="rate_change" />
              <HX.Table shownBy="/cds/standard_fields/is_rater_priced"
                data={[
                "exposure_change",
                "risk_characteristics_change",
                "deductible_change",
                "limit_change",
                "terms_conditions_change",
                "other_change",
                null,
                "rate_change"
              ]}
                fields={[
                {
                  "field": "model_calculated",
                  "width": 140
                },
                {
                  "field": "uw_override",
                  "width": 140
                },
                {
                  "field": "final",
                  "width": 140
                },
                {
                  "field": "comments",
                  "width": 250
                }
              ]}
                with="rate_change"
                syncColumnWidthsKey="syncRateChange"
                kb-interactive={true} />
              <HX.Collection title="Final Rate Change"
                fields={[
                {
                  "field": "rate_change/risk_adjusted_rate_change",
                  "shownBy": "/cds/standard_fields/is_rater_priced"
                },
                {
                  "field": "rate_change/risk_adjusted_rate_change_case_priced",
                  "shownBy": "/cds/standard_fields/is_case_priced"
                },
                null,
                null
              ]}
                horizontal={true} />
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Renewal Layer 10"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_10">
          <HX.With context={{
            "index": 9,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Collection fields={[
                "rate_change/expiring_layer",
                null,
                null
              ]}
                horizontal={true} />
              <HX.Table data={[
                "premium/line_100pct/annualised",
                "premium/beazley_line/annualised",
                "attachment",
                "aggregate_limit",
                "brokerage",
                "currency"
              ]}
                fields={[
                {
                  "field": "expiring",
                  "width": 160
                },
                {
                  "field": "expiring_revalued",
                  "shownBy": "show_expiring_revalued",
                  "width": 160
                },
                {
                  "field": "renewal",
                  "width": 160
                }
              ]}
                with="rate_change" />
              <HX.Table shownBy="/cds/standard_fields/is_rater_priced"
                data={[
                "exposure_change",
                "risk_characteristics_change",
                "deductible_change",
                "limit_change",
                "terms_conditions_change",
                "other_change",
                null,
                "rate_change"
              ]}
                fields={[
                {
                  "field": "model_calculated",
                  "width": 140
                },
                {
                  "field": "uw_override",
                  "width": 140
                },
                {
                  "field": "final",
                  "width": 140
                },
                {
                  "field": "comments",
                  "width": 250
                }
              ]}
                with="rate_change"
                syncColumnWidthsKey="syncRateChange"
                kb-interactive={true} />
              <HX.Collection title="Final Rate Change"
                fields={[
                {
                  "field": "rate_change/risk_adjusted_rate_change",
                  "shownBy": "/cds/standard_fields/is_rater_priced"
                },
                {
                  "field": "rate_change/risk_adjusted_rate_change_case_priced",
                  "shownBy": "/cds/standard_fields/is_case_priced"
                },
                null,
                null
              ]}
                horizontal={true} />
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Renewal Layer 11"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_11">
          <HX.With context={{
            "index": 10,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Collection fields={[
                "rate_change/expiring_layer",
                null,
                null
              ]}
                horizontal={true} />
              <HX.Table data={[
                "premium/line_100pct/annualised",
                "premium/beazley_line/annualised",
                "attachment",
                "aggregate_limit",
                "brokerage",
                "currency"
              ]}
                fields={[
                {
                  "field": "expiring",
                  "width": 160
                },
                {
                  "field": "expiring_revalued",
                  "shownBy": "show_expiring_revalued",
                  "width": 160
                },
                {
                  "field": "renewal",
                  "width": 160
                }
              ]}
                with="rate_change" />
              <HX.Table shownBy="/cds/standard_fields/is_rater_priced"
                data={[
                "exposure_change",
                "risk_characteristics_change",
                "deductible_change",
                "limit_change",
                "terms_conditions_change",
                "other_change",
                null,
                "rate_change"
              ]}
                fields={[
                {
                  "field": "model_calculated",
                  "width": 140
                },
                {
                  "field": "uw_override",
                  "width": 140
                },
                {
                  "field": "final",
                  "width": 140
                },
                {
                  "field": "comments",
                  "width": 250
                }
              ]}
                with="rate_change"
                syncColumnWidthsKey="syncRateChange"
                kb-interactive={true} />
              <HX.Collection title="Final Rate Change"
                fields={[
                {
                  "field": "rate_change/risk_adjusted_rate_change",
                  "shownBy": "/cds/standard_fields/is_rater_priced"
                },
                {
                  "field": "rate_change/risk_adjusted_rate_change_case_priced",
                  "shownBy": "/cds/standard_fields/is_case_priced"
                },
                null,
                null
              ]}
                horizontal={true} />
            </HX.Pane>
          </HX.With>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Rationale"
        fullWidth={false}
        viewScale={1}
        shownBy="model_state/show_after_landing_page">
        <HX.Section title="Underwriter Rationale">
          <CustomComponent textNode="cds/standard_fields/uw_rationale"
            label="Click to view/edit Rationale" />
        </HX.Section>
        <HX.Section title="Policy Document">
          <HX.Button task="policy_to_excel_task"
            title="Generate Policy Document"
            shownBy="policy_doc/show_generate_button" />
          <HX.Notes field="policy_doc/premium_check"
            shownBy="policy_doc/show_premium_check" />
          <HX.File with="policy_doc"
            field="output_file"
            title="Click on the icon below to download the policy document"
            shownBy="show_download" />
          <HX.Button task="generate_email_task"
            title="Generate Rationale Email"
            shownBy="policy_doc/show_generate_button" />
          <HX.File field="cds/email/rationale_file"
            title="Click on the icon below to download the policy email document"
            shownBy="cds/email/show_download" />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Standard KPIs">
        <HX.Section title="Summary Layer 1"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_1">
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "status",
              "section_reference",
              "brokerage",
              "written_line"
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              {
                "field": "quoted_premium_100",
                "labelBy": "premium_label"
              },
              null,
              "technical_premium",
              "benchmark_premium",
              "tpi",
              "bpi",
              {
                "field": "tpi_pre_uw_adj",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "bpi_pre_uw_adj",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              }
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              shownBy="/cds/standard_fields/is_rater_priced"
              numCols={3}
              fields={[
              "pflr",
              "pflr_pre_uw_adj",
              "uw_adj_impact"
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              shownBy="/cds/standard_fields/is_case_priced"
              numCols={3}
              fields={[
              "pflr",
              null,
              null
            ]} />
            <HX.Collection title="Rate Change"
              shownBy="/cds/standard_fields/is_renewal"
              numCols={3}
              fields={[
              {
                "field": "rate_change/risk_adjusted_rate_change",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "rate_change/risk_adjusted_rate_change_case_priced.read_only",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              null,
              null
            ]} />
          </HX.With>
        </HX.Section>
        <HX.Section title="Summary Layer 2"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_2">
          <HX.With context={{
            "index": 1,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "status",
              "section_reference",
              "brokerage",
              "written_line"
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              {
                "field": "quoted_premium_100",
                "labelBy": "premium_label"
              },
              null,
              "technical_premium",
              "benchmark_premium",
              "tpi",
              "bpi",
              {
                "field": "tpi_pre_uw_adj",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "bpi_pre_uw_adj",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              }
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              shownBy="/cds/standard_fields/is_rater_priced"
              numCols={3}
              fields={[
              "pflr",
              "pflr_pre_uw_adj",
              "uw_adj_impact"
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              shownBy="/cds/standard_fields/is_case_priced"
              numCols={3}
              fields={[
              "pflr",
              null,
              null
            ]} />
            <HX.Collection title="Rate Change"
              shownBy="/cds/standard_fields/is_renewal"
              numCols={3}
              fields={[
              {
                "field": "rate_change/risk_adjusted_rate_change",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "rate_change/risk_adjusted_rate_change_case_priced.read_only",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              null,
              null
            ]} />
          </HX.With>
        </HX.Section>
        <HX.Section title="Summary Layer 3"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_3">
          <HX.With context={{
            "index": 2,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "status",
              "section_reference",
              "brokerage",
              "written_line"
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              {
                "field": "quoted_premium_100",
                "labelBy": "premium_label"
              },
              null,
              "technical_premium",
              "benchmark_premium",
              "tpi",
              "bpi",
              {
                "field": "tpi_pre_uw_adj",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "bpi_pre_uw_adj",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              }
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              shownBy="/cds/standard_fields/is_rater_priced"
              numCols={3}
              fields={[
              "pflr",
              "pflr_pre_uw_adj",
              "uw_adj_impact"
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              shownBy="/cds/standard_fields/is_case_priced"
              numCols={3}
              fields={[
              "pflr",
              null,
              null
            ]} />
            <HX.Collection title="Rate Change"
              shownBy="/cds/standard_fields/is_renewal"
              numCols={3}
              fields={[
              {
                "field": "rate_change/risk_adjusted_rate_change",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "rate_change/risk_adjusted_rate_change_case_priced.read_only",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              null,
              null
            ]} />
          </HX.With>
        </HX.Section>
        <HX.Section title="Summary Layer 4"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_4">
          <HX.With context={{
            "index": 3,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "status",
              "section_reference",
              "brokerage",
              "written_line"
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              {
                "field": "quoted_premium_100",
                "labelBy": "premium_label"
              },
              null,
              "technical_premium",
              "benchmark_premium",
              "tpi",
              "bpi",
              {
                "field": "tpi_pre_uw_adj",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "bpi_pre_uw_adj",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              }
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              shownBy="/cds/standard_fields/is_rater_priced"
              numCols={3}
              fields={[
              "pflr",
              "pflr_pre_uw_adj",
              "uw_adj_impact"
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              shownBy="/cds/standard_fields/is_case_priced"
              numCols={3}
              fields={[
              "pflr",
              null,
              null
            ]} />
            <HX.Collection title="Rate Change"
              shownBy="/cds/standard_fields/is_renewal"
              numCols={3}
              fields={[
              {
                "field": "rate_change/risk_adjusted_rate_change",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "rate_change/risk_adjusted_rate_change_case_priced.read_only",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              null,
              null
            ]} />
          </HX.With>
        </HX.Section>
        <HX.Section title="Summary Layer 5"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_5">
          <HX.With context={{
            "index": 4,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "status",
              "section_reference",
              "brokerage",
              "written_line"
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              {
                "field": "quoted_premium_100",
                "labelBy": "premium_label"
              },
              null,
              "technical_premium",
              "benchmark_premium",
              "tpi",
              "bpi",
              {
                "field": "tpi_pre_uw_adj",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "bpi_pre_uw_adj",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              }
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              shownBy="/cds/standard_fields/is_rater_priced"
              numCols={3}
              fields={[
              "pflr",
              "pflr_pre_uw_adj",
              "uw_adj_impact"
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              shownBy="/cds/standard_fields/is_case_priced"
              numCols={3}
              fields={[
              "pflr",
              null,
              null
            ]} />
            <HX.Collection title="Rate Change"
              shownBy="/cds/standard_fields/is_renewal"
              numCols={3}
              fields={[
              {
                "field": "rate_change/risk_adjusted_rate_change",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "rate_change/risk_adjusted_rate_change_case_priced.read_only",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              null,
              null
            ]} />
          </HX.With>
        </HX.Section>
        <HX.Section title="Summary Layer 6"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_6">
          <HX.With context={{
            "index": 5,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "status",
              "section_reference",
              "brokerage",
              "written_line"
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              {
                "field": "quoted_premium_100",
                "labelBy": "premium_label"
              },
              null,
              "technical_premium",
              "benchmark_premium",
              "tpi",
              "bpi",
              {
                "field": "tpi_pre_uw_adj",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "bpi_pre_uw_adj",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              }
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              shownBy="/cds/standard_fields/is_rater_priced"
              numCols={3}
              fields={[
              "pflr",
              "pflr_pre_uw_adj",
              "uw_adj_impact"
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              shownBy="/cds/standard_fields/is_case_priced"
              numCols={3}
              fields={[
              "pflr",
              null,
              null
            ]} />
            <HX.Collection title="Rate Change"
              shownBy="/cds/standard_fields/is_renewal"
              numCols={3}
              fields={[
              {
                "field": "rate_change/risk_adjusted_rate_change",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "rate_change/risk_adjusted_rate_change_case_priced.read_only",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              null,
              null
            ]} />
          </HX.With>
        </HX.Section>
        <HX.Section title="Summary Layer 7"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_7">
          <HX.With context={{
            "index": 6,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "status",
              "section_reference",
              "brokerage",
              "written_line"
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              {
                "field": "quoted_premium_100",
                "labelBy": "premium_label"
              },
              null,
              "technical_premium",
              "benchmark_premium",
              "tpi",
              "bpi",
              {
                "field": "tpi_pre_uw_adj",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "bpi_pre_uw_adj",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              }
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              shownBy="/cds/standard_fields/is_rater_priced"
              numCols={3}
              fields={[
              "pflr",
              "pflr_pre_uw_adj",
              "uw_adj_impact"
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              shownBy="/cds/standard_fields/is_case_priced"
              numCols={3}
              fields={[
              "pflr",
              null,
              null
            ]} />
            <HX.Collection title="Rate Change"
              shownBy="/cds/standard_fields/is_renewal"
              numCols={3}
              fields={[
              {
                "field": "rate_change/risk_adjusted_rate_change",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "rate_change/risk_adjusted_rate_change_case_priced.read_only",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              null,
              null
            ]} />
          </HX.With>
        </HX.Section>
        <HX.Section title="Summary Layer 8"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_8">
          <HX.With context={{
            "index": 7,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "status",
              "section_reference",
              "brokerage",
              "written_line"
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              {
                "field": "quoted_premium_100",
                "labelBy": "premium_label"
              },
              null,
              "technical_premium",
              "benchmark_premium",
              "tpi",
              "bpi",
              {
                "field": "tpi_pre_uw_adj",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "bpi_pre_uw_adj",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              }
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              shownBy="/cds/standard_fields/is_rater_priced"
              numCols={3}
              fields={[
              "pflr",
              "pflr_pre_uw_adj",
              "uw_adj_impact"
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              shownBy="/cds/standard_fields/is_case_priced"
              numCols={3}
              fields={[
              "pflr",
              null,
              null
            ]} />
            <HX.Collection title="Rate Change"
              shownBy="/cds/standard_fields/is_renewal"
              numCols={3}
              fields={[
              {
                "field": "rate_change/risk_adjusted_rate_change",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "rate_change/risk_adjusted_rate_change_case_priced.read_only",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              null,
              null
            ]} />
          </HX.With>
        </HX.Section>
        <HX.Section title="Summary Layer 9"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_9">
          <HX.With context={{
            "index": 8,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "status",
              "section_reference",
              "brokerage",
              "written_line"
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              {
                "field": "quoted_premium_100",
                "labelBy": "premium_label"
              },
              null,
              "technical_premium",
              "benchmark_premium",
              "tpi",
              "bpi",
              {
                "field": "tpi_pre_uw_adj",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "bpi_pre_uw_adj",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              }
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              shownBy="/cds/standard_fields/is_rater_priced"
              numCols={3}
              fields={[
              "pflr",
              "pflr_pre_uw_adj",
              "uw_adj_impact"
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              shownBy="/cds/standard_fields/is_case_priced"
              numCols={3}
              fields={[
              "pflr",
              null,
              null
            ]} />
            <HX.Collection title="Rate Change"
              shownBy="/cds/standard_fields/is_renewal"
              numCols={3}
              fields={[
              {
                "field": "rate_change/risk_adjusted_rate_change",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "rate_change/risk_adjusted_rate_change_case_priced.read_only",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              null,
              null
            ]} />
          </HX.With>
        </HX.Section>
        <HX.Section title="Summary Layer 10"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_10">
          <HX.With context={{
            "index": 9,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "status",
              "section_reference",
              "brokerage",
              "written_line"
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              {
                "field": "quoted_premium_100",
                "labelBy": "premium_label"
              },
              null,
              "technical_premium",
              "benchmark_premium",
              "tpi",
              "bpi",
              {
                "field": "tpi_pre_uw_adj",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "bpi_pre_uw_adj",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              }
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              shownBy="/cds/standard_fields/is_rater_priced"
              numCols={3}
              fields={[
              "pflr",
              "pflr_pre_uw_adj",
              "uw_adj_impact"
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              shownBy="/cds/standard_fields/is_case_priced"
              numCols={3}
              fields={[
              "pflr",
              null,
              null
            ]} />
            <HX.Collection title="Rate Change"
              shownBy="/cds/standard_fields/is_renewal"
              numCols={3}
              fields={[
              {
                "field": "rate_change/risk_adjusted_rate_change",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "rate_change/risk_adjusted_rate_change_case_priced.read_only",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              null,
              null
            ]} />
          </HX.With>
        </HX.Section>
        <HX.Section title="Summary Layer 11"
          defaultCollapsed={true}
          shownBy="cds/rate_change/show_layer_11">
          <HX.With context={{
            "index": 10,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "status",
              "section_reference",
              "brokerage",
              "written_line"
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              {
                "field": "quoted_premium_100",
                "labelBy": "premium_label"
              },
              null,
              "technical_premium",
              "benchmark_premium",
              "tpi",
              "bpi",
              {
                "field": "tpi_pre_uw_adj",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "bpi_pre_uw_adj",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              }
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              shownBy="/cds/standard_fields/is_rater_priced"
              numCols={3}
              fields={[
              "pflr",
              "pflr_pre_uw_adj",
              "uw_adj_impact"
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              shownBy="/cds/standard_fields/is_case_priced"
              numCols={3}
              fields={[
              "pflr",
              null,
              null
            ]} />
            <HX.Collection title="Rate Change"
              shownBy="/cds/standard_fields/is_renewal"
              numCols={3}
              fields={[
              {
                "field": "rate_change/risk_adjusted_rate_change",
                "shownBy": "/cds/standard_fields/is_rater_priced"
              },
              {
                "field": "rate_change/risk_adjusted_rate_change_case_priced.read_only",
                "shownBy": "/cds/standard_fields/is_case_priced"
              },
              null,
              null
            ]} />
          </HX.With>
        </HX.Section>
      </HX.Page>
    </HX.Root>
  );
}

export default {
  hx_calculation_legacy_initial_premium: hx_calculation_legacy_initial_premium_view,
};