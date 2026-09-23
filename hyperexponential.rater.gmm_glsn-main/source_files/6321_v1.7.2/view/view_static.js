
throw new Error(`This file is generated

Do not edit manually as all of the changes will be lost.
This is the static version of your View that will allow easier debugging.
`);

import * as HX from "hx-model-components";


function hx_calculation_legacy_initial_premium_view(props) {
  return (
    <HX.Root>
      <HX.Page title="Landing Page"
        shownBy="model_state/show_initialisation_page">
        <HX.Section title="Initialise Model">
          <HX.Pane shownBy="model_state/show_landing_page">
            <HX.Collection fields={[
              {
                "field": "model_state/landing_page_info"
              }
            ]} />
          </HX.Pane>
          <HX.Pane flow="right"
            shownBy="model_state/show_initialise_model_button">
            <HX.Pane>
              <HX.Button task="initialise_model"
                title="Initialise Model" />
            </HX.Pane>
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Risk Information">
        <HX.Section title="Account Details">
          <HX.Pane>
            <HX.Collection fields={[
              "hx_core/inception_date",
              "hx_core/expiry_date",
              {
                "field": "cds/standard_fields/is_renewal",
                "shownBy": "/model_state/show_rate_change"
              }
            ]}
              horizontal={true} />
            <HX.Collection fields={[
              "underwriter",
              "insured_name"
            ]}
              with="cds/standard_fields"
              horizontal={true} />
            <HX.Button task="save_uw_to_pas_reference"
              title="Save UW Name to PAS Reference" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Broker Details">
          <HX.Collection fields={[
            "cds/standard_fields/broker",
            "cds/broker_contact"
          ]}
            horizontal={true} />
        </HX.Section>
        <HX.Section title="Rater Selection">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "cds/rater_selection"
            ]} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Risk Details">
          <HX.Pane flow="right">
            <HX.Table title="Operating Region"
              data={[
              "cds/rating_factors/us_international_choice_of_law"
            ]}
              fields={[
              "us_international",
              "choice_of_law"
            ]} />
            <HX.Collection fields={[
              "cds/rating_factors/currency"
            ]}
              horizontal={true} />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Collection fields={[
              {
                "field": "cds/exposure/aggregate/revenue",
                "shownBy": "cds/exposure/aggregate/revenue_filled"
              },
              {
                "field": "cds/exposure/aggregate/revenue.mandatory",
                "infoBy": "cds/exposure/aggregate/revenue_info",
                "shownBy": "cds/exposure/aggregate/revenue_empty"
              }
            ]} />
            <HX.Collection fields={[
              "cds/rating_factors/profit_status"
            ]} />
            <HX.Collection shownBy="cds/glsn_masking"
              fields={[
              "cds/rating_factors/glsn/brag_status"
            ]} />
            <HX.Collection shownBy="cds/gmm_masking"
              fields={[
              "cds/rating_factors/gmm/product_override"
            ]} />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "cds/rating_factors/business_segment"
            ]} />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Table shownBy="cds/gmm_masking"
              title="COB Selection"
              data={[
              "cds/exposure/granular/gmm_product"
            ]}
              fields={[
              "product",
              "cob_code_description",
              "cob_class"
            ]} />
            <HX.Table shownBy="cds/glsn_masking"
              title="COB Selection"
              data={[
              "cds/exposure/granular/glsn_product"
            ]}
              fields={[
              "product",
              "cob_code_description"
            ]} />
            <HX.Collection shownBy="cds/glsn_masking"
              fields={[
              "cds/rating_factors/glsn/form"
            ]} />
          </HX.Pane>
          <HX.Button task="clear_exposures_task"
            title="Clear Exposure Inputs (current and prior years): Run if changing COB selection" />
          <HX.Pane flow="right">
            <HX.Collection shownBy="cds/glsn_masking"
              fields={[
              "cds/rating_factors/glsn/supply_chain"
            ]} />
            <HX.Collection shownBy="cds/glsn_masking"
              fields={[
              "cds/rating_factors/glsn/supply_chain_factor"
            ]} />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Collection shownBy="cds/glsn_masking"
              fields={[
              "cds/rating_factors/glsn/clinical_trial"
            ]} />
            <HX.Collection shownBy="cds/glsn_masking"
              fields={[
              "cds/rating_factors/glsn/clinical_trial_factor"
            ]} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Account Scorings">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "cds/rating_factors/total_net_score/value"
            ]} />
            <HX.Collection fields={[
              "cds/rating_factors/account_score"
            ]} />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Table data={[
              {
                "datum": "financials_quality",
                "labelAlign": "left"
              },
              {
                "datum": "claims_handling",
                "labelAlign": "left"
              },
              {
                "datum": "claims_experience",
                "labelAlign": "left"
              },
              {
                "datum": "jurisdiction_venue",
                "labelAlign": "left"
              },
              {
                "datum": "wordings",
                "labelAlign": "left"
              },
              {
                "datum": "level_of_service",
                "labelAlign": "left"
              },
              {
                "datum": "knowledge_of_account",
                "labelAlign": "left"
              },
              {
                "datum": "nfp_gov_fp",
                "labelAlign": "left"
              },
              {
                "datum": "broker",
                "labelAlign": "left"
              },
              {
                "datum": "corporate_integrity",
                "labelAlign": "left"
              }
            ]}
              fields={[
              "value",
              "comment"
            ]}
              title="Account Scorings"
              with="cds/rating_factors/account_scoring"
              kb-interactive={true} />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "cds/rating_factors/total_net_score/comment"
            ]} />
            <HX.Collection fields={[
              "cds/rating_factors/account_scoring_details/show_account_scoring"
            ]} />
          </HX.Pane>
          <HX.Pane>
            <HX.Table shownBy="/cds/rating_factors/account_scoring_details/show_account_scoring"
              data={[
              {
                "datum": "financials_quality",
                "labelAlign": "left"
              },
              {
                "datum": "claims_handling",
                "labelAlign": "left"
              },
              {
                "datum": "claims_experience",
                "labelAlign": "left"
              },
              {
                "datum": "jurisdiction_venue",
                "labelAlign": "left"
              },
              {
                "datum": "wordings",
                "labelAlign": "left"
              },
              {
                "datum": "level_of_service",
                "labelAlign": "left"
              },
              {
                "datum": "knowledge_of_account",
                "labelAlign": "left"
              },
              {
                "datum": "nfp_gov_fp",
                "labelAlign": "left"
              },
              {
                "datum": "broker",
                "labelAlign": "left"
              },
              {
                "datum": "corporate_integrity",
                "labelAlign": "left"
              }
            ]}
              fields={[
              {
                "field": "pro_example",
                "maxWidth": 700
              },
              {
                "field": "neutral_example",
                "maxWidth": 700
              },
              {
                "field": "con_example",
                "maxWidth": 700
              }
            ]}
              title="Account Scoring Key"
              with="cds/rating_factors/account_scoring_details"
              kb-interactive={true} />
            <HX.Table shownBy="/cds/rating_factors/account_scoring_details/show_account_scoring"
              data={[
              {
                "datum": "cds/rating_factors/account_scoring_details/parameters"
              }
            ]}
              fields={[
              "five_or_more",
              "three_or_more",
              "two_or_fewer",
              "three_or_more_cons",
              "five_or_more_cons"
            ]}
              title="Parameters"
              kb-interactive={true}
              filter="show_row" />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Venue Factors"
        fullWidth={true}
        viewScale={1}>
        <HX.Section title="Venue Factors">
          <HX.Pane flow="right">
            <HX.Button task="venue_factors_select_all"
              title="Select All Venues" />
            <HX.Button task="venue_calculation_with_override"
              title="Calculate Selected Venues" />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Collection fields={[
              "cds/exposure/aggregate/total_venue_factor"
            ]} />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Button task="venue_factors_clear_all"
              title="Clear All Venues" />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Collection fields={[
              "cds/exposure/aggregate/total_venue_international_factor"
            ]}
              shownBy="/cds/international_masking" />
            <HX.Collection fields={[
              "cds/exposure/aggregate/total_venue_us_factor"
            ]}
              shownBy="/cds/us_masking" />
            <HX.Collection fields={[
              "cds/exposure/aggregate/total_percentage_selected"
            ]} />
          </HX.Pane>
          <HX.Pane>
            <HX.Table shownBy="/cds/us_masking"
              syncColumnWidthsKey="mySyncedTables1"
              data={[
              {
                "datum": "alaska",
                "labelAlign": "left"
              },
              {
                "datum": "alabama",
                "labelAlign": "left"
              },
              {
                "datum": "arkansas",
                "labelAlign": "left"
              },
              {
                "datum": "arizona",
                "labelAlign": "left"
              },
              {
                "datum": "california_counties",
                "labelAlign": "left"
              },
              {
                "datum": "california_rest",
                "labelAlign": "left"
              },
              {
                "datum": "colorado",
                "labelAlign": "left"
              },
              {
                "datum": "connecticut",
                "labelAlign": "left"
              },
              {
                "datum": "district_of_columbia",
                "labelAlign": "left"
              },
              {
                "datum": "delaware",
                "labelAlign": "left"
              },
              {
                "datum": "florida_counties",
                "labelAlign": "left"
              },
              {
                "datum": "florida_rest",
                "labelAlign": "left"
              },
              {
                "datum": "georgia",
                "labelAlign": "left"
              },
              {
                "datum": "hawaii",
                "labelAlign": "left"
              },
              {
                "datum": "iowa",
                "labelAlign": "left"
              },
              {
                "datum": "idaho",
                "labelAlign": "left"
              },
              {
                "datum": "illinois_counties",
                "labelAlign": "left"
              },
              {
                "datum": "illinois_rest",
                "labelAlign": "left"
              },
              {
                "datum": "indiana",
                "labelAlign": "left"
              },
              {
                "datum": "international",
                "labelAlign": "left"
              },
              {
                "datum": "kansas",
                "labelAlign": "left"
              },
              {
                "datum": "kentucky",
                "labelAlign": "left"
              },
              {
                "datum": "louisiana",
                "labelAlign": "left"
              },
              {
                "datum": "massachusetts",
                "labelAlign": "left"
              },
              {
                "datum": "maryland_counties",
                "labelAlign": "left"
              },
              {
                "datum": "maryland_rest",
                "labelAlign": "left"
              },
              {
                "datum": "maine",
                "labelAlign": "left"
              },
              {
                "datum": "michigan_rest",
                "labelAlign": "left"
              },
              {
                "datum": "michigan_counties",
                "labelAlign": "left"
              },
              {
                "datum": "minnesota_counties",
                "labelAlign": "left"
              },
              {
                "datum": "minnesota_rest",
                "labelAlign": "left"
              },
              {
                "datum": "missouri_rest",
                "labelAlign": "left"
              },
              {
                "datum": "missouri_counties",
                "labelAlign": "left"
              },
              {
                "datum": "mississippi",
                "labelAlign": "left"
              },
              {
                "datum": "montana",
                "labelAlign": "left"
              },
              {
                "datum": "north_carolina",
                "labelAlign": "left"
              },
              {
                "datum": "north_dakota",
                "labelAlign": "left"
              },
              {
                "datum": "nebraska",
                "labelAlign": "left"
              },
              {
                "datum": "new_hampshire",
                "labelAlign": "left"
              },
              {
                "datum": "new_jersey",
                "labelAlign": "left"
              },
              {
                "datum": "new_mexico",
                "labelAlign": "left"
              },
              {
                "datum": "nevada",
                "labelAlign": "left"
              },
              {
                "datum": "new_york_city_counties",
                "labelAlign": "left"
              },
              {
                "datum": "new_york_rest",
                "labelAlign": "left"
              },
              {
                "datum": "ohio_counties",
                "labelAlign": "left"
              },
              {
                "datum": "ohio_rest",
                "labelAlign": "left"
              },
              {
                "datum": "oklahoma",
                "labelAlign": "left"
              },
              {
                "datum": "oregon",
                "labelAlign": "left"
              },
              {
                "datum": "pennsylvania_counties",
                "labelAlign": "left"
              },
              {
                "datum": "pennsylvania_rest",
                "labelAlign": "left"
              },
              {
                "datum": "puerto_rico_usa",
                "labelAlign": "left"
              },
              {
                "datum": "rhode_island",
                "labelAlign": "left"
              },
              {
                "datum": "south_carolina",
                "labelAlign": "left"
              },
              {
                "datum": "south_dakota",
                "labelAlign": "left"
              },
              {
                "datum": "tennessee",
                "labelAlign": "left"
              },
              {
                "datum": "texas_rest",
                "labelAlign": "left"
              },
              {
                "datum": "texas_counties",
                "labelAlign": "left"
              },
              {
                "datum": "utah",
                "labelAlign": "left"
              },
              {
                "datum": "virginia",
                "labelAlign": "left"
              },
              {
                "datum": "vermont",
                "labelAlign": "left"
              },
              {
                "datum": "washington",
                "labelAlign": "left"
              },
              {
                "datum": "wisconsin",
                "labelAlign": "left"
              },
              {
                "datum": "west_virginia",
                "labelAlign": "left"
              },
              {
                "datum": "wyoming",
                "labelAlign": "left"
              }
            ]}
              fields={[
              {
                "field": "factor",
                "maxWidth": 300
              },
              {
                "field": "percentage",
                "maxWidth": 300
              },
              {
                "field": "selection",
                "maxWidth": 300
              }
            ]}
              title="US Venue Factors"
              with="cds/exposure/granular"
              kb-interactive={true} />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "cds/exposure/granular/include_international_venues"
            ]}
              shownBy="/cds/us_masking" />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
          <HX.Pane>
            <HX.Table shownBy="/cds/international_masking"
              syncColumnWidthsKey="mySyncedTables1"
              data={[
              {
                "datum": "asia",
                "labelAlign": "left"
              },
              {
                "datum": "australia",
                "labelAlign": "left"
              },
              {
                "datum": "brazil",
                "labelAlign": "left"
              },
              {
                "datum": "canada",
                "labelAlign": "left"
              },
              {
                "datum": "chile",
                "labelAlign": "left"
              },
              {
                "datum": "china",
                "labelAlign": "left"
              },
              {
                "datum": "colombia",
                "labelAlign": "left"
              },
              {
                "datum": "france",
                "labelAlign": "left"
              },
              {
                "datum": "germany",
                "labelAlign": "left"
              },
              {
                "datum": "hong_kong",
                "labelAlign": "left"
              },
              {
                "datum": "ireland",
                "labelAlign": "left"
              },
              {
                "datum": "island_economies",
                "labelAlign": "left"
              },
              {
                "datum": "israel",
                "labelAlign": "left"
              },
              {
                "datum": "italy",
                "labelAlign": "left"
              },
              {
                "datum": "malaysia",
                "labelAlign": "left"
              },
              {
                "datum": "mexico",
                "labelAlign": "left"
              },
              {
                "datum": "middle_east",
                "labelAlign": "left"
              },
              {
                "datum": "netherlands",
                "labelAlign": "left"
              },
              {
                "datum": "peru",
                "labelAlign": "left"
              },
              {
                "datum": "puerto_rico_international",
                "labelAlign": "left"
              },
              {
                "datum": "row_high",
                "labelAlign": "left"
              },
              {
                "datum": "row_low",
                "labelAlign": "left"
              },
              {
                "datum": "row_medium",
                "labelAlign": "left"
              },
              {
                "datum": "singapore",
                "labelAlign": "left"
              },
              {
                "datum": "south_africa",
                "labelAlign": "left"
              },
              {
                "datum": "spain",
                "labelAlign": "left"
              },
              {
                "datum": "taiwan",
                "labelAlign": "left"
              },
              {
                "datum": "thailand",
                "labelAlign": "left"
              },
              {
                "datum": "uk",
                "labelAlign": "left"
              },
              {
                "datum": "usa",
                "labelAlign": "left"
              }
            ]}
              fields={[
              {
                "field": "factor",
                "maxWidth": 300
              },
              {
                "field": "percentage",
                "maxWidth": 300
              },
              {
                "field": "selection",
                "maxWidth": 300
              }
            ]}
              title="International Venue Factors"
              with="cds/exposure/granular"
              kb-interactive={true} />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "cds/exposure/granular/include_us_venues"
            ]}
              shownBy="/cds/international_masking" />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
          <HX.Pane>
            <HX.Pane flow="right">
              <HX.Pane />
              <HX.Pane />
              <HX.Pane />
              <HX.Pane />
              <HX.Collection fields={[
                "cds/exposure/aggregate/total_venue_international_factor"
              ]}
                shownBy="/cds/us_and_international_masking" />
            </HX.Pane>
            <HX.Table shownBy="/cds/us_and_international_masking"
              syncColumnWidthsKey="mySyncedTables1"
              data={[
              {
                "datum": "asia",
                "labelAlign": "left"
              },
              {
                "datum": "australia",
                "labelAlign": "left"
              },
              {
                "datum": "brazil",
                "labelAlign": "left"
              },
              {
                "datum": "canada",
                "labelAlign": "left"
              },
              {
                "datum": "chile",
                "labelAlign": "left"
              },
              {
                "datum": "china",
                "labelAlign": "left"
              },
              {
                "datum": "colombia",
                "labelAlign": "left"
              },
              {
                "datum": "france",
                "labelAlign": "left"
              },
              {
                "datum": "germany",
                "labelAlign": "left"
              },
              {
                "datum": "hong_kong",
                "labelAlign": "left"
              },
              {
                "datum": "ireland",
                "labelAlign": "left"
              },
              {
                "datum": "island_economies",
                "labelAlign": "left"
              },
              {
                "datum": "israel",
                "labelAlign": "left"
              },
              {
                "datum": "italy",
                "labelAlign": "left"
              },
              {
                "datum": "malaysia",
                "labelAlign": "left"
              },
              {
                "datum": "mexico",
                "labelAlign": "left"
              },
              {
                "datum": "middle_east",
                "labelAlign": "left"
              },
              {
                "datum": "netherlands",
                "labelAlign": "left"
              },
              {
                "datum": "peru",
                "labelAlign": "left"
              },
              {
                "datum": "puerto_rico_international",
                "labelAlign": "left"
              },
              {
                "datum": "row_high",
                "labelAlign": "left"
              },
              {
                "datum": "row_low",
                "labelAlign": "left"
              },
              {
                "datum": "row_medium",
                "labelAlign": "left"
              },
              {
                "datum": "singapore",
                "labelAlign": "left"
              },
              {
                "datum": "south_africa",
                "labelAlign": "left"
              },
              {
                "datum": "spain",
                "labelAlign": "left"
              },
              {
                "datum": "taiwan",
                "labelAlign": "left"
              },
              {
                "datum": "thailand",
                "labelAlign": "left"
              },
              {
                "datum": "uk",
                "labelAlign": "left"
              },
              {
                "datum": "usa",
                "labelAlign": "left"
              }
            ]}
              fields={[
              {
                "field": "factor",
                "maxWidth": 300
              },
              {
                "field": "percentage",
                "maxWidth": 300
              },
              {
                "field": "selection",
                "maxWidth": 300
              }
            ]}
              title="International Venue Factors"
              with="cds/exposure/granular"
              kb-interactive={true} />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Collection fields={[
              "cds/exposure/aggregate/total_venue_us_factor"
            ]}
              shownBy="/cds/international_and_us_masking" />
          </HX.Pane>
          <HX.Pane>
            <HX.Table shownBy="/cds/international_and_us_masking"
              syncColumnWidthsKey="mySyncedTables1"
              data={[
              {
                "datum": "alaska",
                "labelAlign": "left"
              },
              {
                "datum": "alabama",
                "labelAlign": "left"
              },
              {
                "datum": "arkansas",
                "labelAlign": "left"
              },
              {
                "datum": "arizona",
                "labelAlign": "left"
              },
              {
                "datum": "california_counties",
                "labelAlign": "left"
              },
              {
                "datum": "california_rest",
                "labelAlign": "left"
              },
              {
                "datum": "colorado",
                "labelAlign": "left"
              },
              {
                "datum": "connecticut",
                "labelAlign": "left"
              },
              {
                "datum": "district_of_columbia",
                "labelAlign": "left"
              },
              {
                "datum": "delaware",
                "labelAlign": "left"
              },
              {
                "datum": "florida_counties",
                "labelAlign": "left"
              },
              {
                "datum": "florida_rest",
                "labelAlign": "left"
              },
              {
                "datum": "georgia",
                "labelAlign": "left"
              },
              {
                "datum": "hawaii",
                "labelAlign": "left"
              },
              {
                "datum": "iowa",
                "labelAlign": "left"
              },
              {
                "datum": "idaho",
                "labelAlign": "left"
              },
              {
                "datum": "illinois_counties",
                "labelAlign": "left"
              },
              {
                "datum": "illinois_rest",
                "labelAlign": "left"
              },
              {
                "datum": "indiana",
                "labelAlign": "left"
              },
              {
                "datum": "international",
                "labelAlign": "left"
              },
              {
                "datum": "kansas",
                "labelAlign": "left"
              },
              {
                "datum": "kentucky",
                "labelAlign": "left"
              },
              {
                "datum": "louisiana",
                "labelAlign": "left"
              },
              {
                "datum": "massachusetts",
                "labelAlign": "left"
              },
              {
                "datum": "maryland_counties",
                "labelAlign": "left"
              },
              {
                "datum": "maryland_rest",
                "labelAlign": "left"
              },
              {
                "datum": "maine",
                "labelAlign": "left"
              },
              {
                "datum": "michigan_rest",
                "labelAlign": "left"
              },
              {
                "datum": "michigan_counties",
                "labelAlign": "left"
              },
              {
                "datum": "minnesota_counties",
                "labelAlign": "left"
              },
              {
                "datum": "minnesota_rest",
                "labelAlign": "left"
              },
              {
                "datum": "missouri_rest",
                "labelAlign": "left"
              },
              {
                "datum": "missouri_counties",
                "labelAlign": "left"
              },
              {
                "datum": "mississippi",
                "labelAlign": "left"
              },
              {
                "datum": "montana",
                "labelAlign": "left"
              },
              {
                "datum": "north_carolina",
                "labelAlign": "left"
              },
              {
                "datum": "north_dakota",
                "labelAlign": "left"
              },
              {
                "datum": "nebraska",
                "labelAlign": "left"
              },
              {
                "datum": "new_hampshire",
                "labelAlign": "left"
              },
              {
                "datum": "new_jersey",
                "labelAlign": "left"
              },
              {
                "datum": "new_mexico",
                "labelAlign": "left"
              },
              {
                "datum": "nevada",
                "labelAlign": "left"
              },
              {
                "datum": "new_york_city_counties",
                "labelAlign": "left"
              },
              {
                "datum": "new_york_rest",
                "labelAlign": "left"
              },
              {
                "datum": "ohio_counties",
                "labelAlign": "left"
              },
              {
                "datum": "ohio_rest",
                "labelAlign": "left"
              },
              {
                "datum": "oklahoma",
                "labelAlign": "left"
              },
              {
                "datum": "oregon",
                "labelAlign": "left"
              },
              {
                "datum": "pennsylvania_counties",
                "labelAlign": "left"
              },
              {
                "datum": "pennsylvania_rest",
                "labelAlign": "left"
              },
              {
                "datum": "puerto_rico_usa",
                "labelAlign": "left"
              },
              {
                "datum": "rhode_island",
                "labelAlign": "left"
              },
              {
                "datum": "south_carolina",
                "labelAlign": "left"
              },
              {
                "datum": "south_dakota",
                "labelAlign": "left"
              },
              {
                "datum": "tennessee",
                "labelAlign": "left"
              },
              {
                "datum": "texas_rest",
                "labelAlign": "left"
              },
              {
                "datum": "texas_counties",
                "labelAlign": "left"
              },
              {
                "datum": "utah",
                "labelAlign": "left"
              },
              {
                "datum": "virginia",
                "labelAlign": "left"
              },
              {
                "datum": "vermont",
                "labelAlign": "left"
              },
              {
                "datum": "washington",
                "labelAlign": "left"
              },
              {
                "datum": "wisconsin",
                "labelAlign": "left"
              },
              {
                "datum": "west_virginia",
                "labelAlign": "left"
              },
              {
                "datum": "wyoming",
                "labelAlign": "left"
              }
            ]}
              fields={[
              {
                "field": "factor",
                "maxWidth": 300
              },
              {
                "field": "percentage",
                "maxWidth": 300
              },
              {
                "field": "selection",
                "maxWidth": 300
              }
            ]}
              title="US Venue Factors"
              with="cds/exposure/granular" />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Exposure Details"
        fullWidth={true}
        viewScale={1}
        shownBy="cds/exposure_masking">
        <HX.Section title="Total Base Premium">
          <HX.Pane flow="right">
            <HX.Pane />
            <HX.Pane />
            <HX.Collection shownBy="cds/gmm_masking"
              fields={[
              {
                "field": "cds/rating_factors/mix_of_exposure_measures_message",
                "shownBy": "cds/rating_factors/exposure_measures_message_show"
              },
              "cds/show_prior_exposure_years",
              {
                "field": "cds/exposure/aggregate/gmm_total_base_premium_one_years_ago",
                "infoBy": "cds/exposure/aggregate/gmm_total_base_premium_one_years_ago_info_by"
              },
              "cds/exposure/aggregate/gmm_total_base_premium_current_year"
            ]}
              horizontal={true} />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Pane />
            <HX.Pane />
            <HX.Collection shownBy="cds/glsn_masking"
              fields={[
              {
                "field": "cds/rating_factors/mix_of_exposure_measures_message",
                "shownBy": "cds/rating_factors/exposure_measures_message_show"
              },
              "cds/show_prior_exposure_years",
              "cds/rating_factors/glsn/size_discount_selection",
              {
                "field": "cds/exposure/aggregate/glsn_total_base_premium_one_years_ago",
                "infoBy": "cds/exposure/aggregate/glsn_total_base_premium_one_years_ago_info_by"
              },
              "cds/exposure/aggregate/glsn_total_base_premium_current_year"
            ]}
              horizontal={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Primary Exposure Class">
          <HX.Pane>
            <HX.Table shownBy="cds/gmm_masking"
              syncColumnWidthsKey="mySyncedTables1"
              data={[
              "cds/exposure/granular/gmm_primary_exposure_details"
            ]}
              fields={[
              "exposure_class",
              "exposure_measure",
              "formatted_base_rate",
              {
                "field": "five_years_ago",
                "labelBy": "cds/rating_factors/five_years_ago_label",
                "shownBy": "cds/show_prior_exposure_years"
              },
              {
                "field": "four_years_ago",
                "labelBy": "cds/rating_factors/four_years_ago_label",
                "shownBy": "cds/show_prior_exposure_years"
              },
              {
                "field": "three_years_ago",
                "labelBy": "cds/rating_factors/three_years_ago_label",
                "shownBy": "cds/show_prior_exposure_years"
              },
              {
                "field": "two_years_ago",
                "labelBy": "cds/rating_factors/two_years_ago_label",
                "shownBy": "cds/show_prior_exposure_years"
              },
              {
                "field": "one_years_ago",
                "labelBy": "cds/rating_factors/one_years_ago_label"
              },
              {
                "field": "current_year",
                "labelBy": "cds/rating_factors/current_year_label"
              },
              "selection",
              "base_premium"
            ]}
              filter="show_row"
              title="Exposure Calculation - Primary Class"
              kb-interactive={true} />
            <HX.Table shownBy="cds/glsn_masking"
              syncColumnWidthsKey="mySyncedTables1"
              data={[
              "cds/exposure/granular/glsn_primary_exposure_details"
            ]}
              fields={[
              "cob",
              "exposure_base",
              "exposure_measure",
              "formatted_base_rate",
              {
                "field": "five_years_ago",
                "labelBy": "cds/rating_factors/five_years_ago_label",
                "shownBy": "cds/show_prior_exposure_years"
              },
              {
                "field": "four_years_ago",
                "labelBy": "cds/rating_factors/four_years_ago_label",
                "shownBy": "cds/show_prior_exposure_years"
              },
              {
                "field": "three_years_ago",
                "labelBy": "cds/rating_factors/three_years_ago_label",
                "shownBy": "cds/show_prior_exposure_years"
              },
              {
                "field": "two_years_ago",
                "labelBy": "cds/rating_factors/two_years_ago_label",
                "shownBy": "cds/show_prior_exposure_years"
              },
              {
                "field": "one_years_ago",
                "labelBy": "cds/rating_factors/one_years_ago_label"
              },
              {
                "field": "current_year",
                "labelBy": "cds/rating_factors/current_year_label"
              },
              "selection",
              "base_premium"
            ]}
              filter="show_row"
              title="Exposure Calculation - Primary Class"
              kb-interactive={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Secondary Exposure Class">
          <HX.Pane>
            <HX.Table shownBy="cds/gmm_masking"
              syncColumnWidthsKey="mySyncedTables1"
              data={[
              "cds/exposure/granular/gmm_secondary_exposure_details"
            ]}
              fields={[
              "gmm_secondary_exposure/exposure_class",
              "gmm_secondary_exposure/exposure_measure",
              "formatted_base_rate",
              {
                "field": "five_years_ago",
                "labelBy": "cds/rating_factors/five_years_ago_label",
                "shownBy": "cds/show_prior_exposure_years"
              },
              {
                "field": "four_years_ago",
                "labelBy": "cds/rating_factors/four_years_ago_label",
                "shownBy": "cds/show_prior_exposure_years"
              },
              {
                "field": "three_years_ago",
                "labelBy": "cds/rating_factors/three_years_ago_label",
                "shownBy": "cds/show_prior_exposure_years"
              },
              {
                "field": "two_years_ago",
                "labelBy": "cds/rating_factors/two_years_ago_label",
                "shownBy": "cds/show_prior_exposure_years"
              },
              {
                "field": "one_years_ago",
                "labelBy": "cds/rating_factors/one_years_ago_label"
              },
              {
                "field": "current_year",
                "labelBy": "cds/rating_factors/current_year_label"
              },
              "selection",
              "base_premium"
            ]}
              title="Exposure Calculation - Secondary Class"
              kb-interactive={true} />
            <HX.Table shownBy="cds/glsn_masking"
              syncColumnWidthsKey="mySyncedTables1"
              data={[
              "cds/exposure/granular/glsn_secondary_exposure_details"
            ]}
              fields={[
              "glsn_secondary_exposure/cob",
              "glsn_secondary_exposure/exposure_base",
              "glsn_secondary_exposure/exposure_measure",
              "formatted_base_rate",
              {
                "field": "five_years_ago",
                "labelBy": "cds/rating_factors/five_years_ago_label",
                "shownBy": "cds/show_prior_exposure_years"
              },
              {
                "field": "four_years_ago",
                "labelBy": "cds/rating_factors/four_years_ago_label",
                "shownBy": "cds/show_prior_exposure_years"
              },
              {
                "field": "three_years_ago",
                "labelBy": "cds/rating_factors/three_years_ago_label",
                "shownBy": "cds/show_prior_exposure_years"
              },
              {
                "field": "two_years_ago",
                "labelBy": "cds/rating_factors/two_years_ago_label",
                "shownBy": "cds/show_prior_exposure_years"
              },
              {
                "field": "one_years_ago",
                "labelBy": "cds/rating_factors/one_years_ago_label"
              },
              {
                "field": "current_year",
                "labelBy": "cds/rating_factors/current_year_label"
              },
              "selection",
              "base_premium"
            ]}
              title="Exposure Calculation - Secondary Class"
              kb-interactive={true} />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Triage"
        fullWidth={true}
        viewScale={1}
        shownBy="cds/triage_masking">
        <HX.Section title="Running Total OBE">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "cds/show_prior_triage_years"
            ]}
              horizontal={true} />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Table data={[
              "cds/exposure/aggregate/triage_running_total_obe"
            ]}
              fields={[
              {
                "field": "four_years_ago",
                "shownBy": "cds/show_prior_triage_years"
              },
              {
                "field": "three_years_ago",
                "shownBy": "cds/show_prior_triage_years"
              },
              {
                "field": "two_years_ago",
                "shownBy": "cds/show_prior_triage_years"
              },
              "one_years_ago",
              "current_year"
            ]}
              title="Runnng Total OBE" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Doctors and Residents"
          defaultCollapsed={true}>
          <HX.Pane>
            <HX.Table data={[
              "cds/exposure/granular/triage_doctors_residents"
            ]}
              fields={[
              "specialty",
              "iso_code",
              "iso_class",
              null,
              "obe_per_doctor",
              {
                "field": "doc_four_years_ago",
                "shownBy": "cds/show_prior_triage_years"
              },
              {
                "field": "doc_three_years_ago",
                "shownBy": "cds/show_prior_triage_years"
              },
              {
                "field": "doc_two_years_ago",
                "shownBy": "cds/show_prior_triage_years"
              },
              "doc_one_years_ago",
              "doc_current_year",
              null,
              "obe_per_resident",
              {
                "field": "resident_four_years_ago",
                "shownBy": "cds/show_prior_triage_years"
              },
              {
                "field": "resident_three_years_ago",
                "shownBy": "cds/show_prior_triage_years"
              },
              {
                "field": "resident_two_years_ago",
                "shownBy": "cds/show_prior_triage_years"
              },
              "resident_one_years_ago",
              "resident_current_year"
            ]}
              kb-interactive={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Procedures - Outpatient Surgery"
          defaultCollapsed={true}>
          <HX.Pane>
            <HX.Table data={[
              "cds/exposure/granular/triage_procedures"
            ]}
              fields={[
              "category",
              "exposure_measure",
              "formatted_obe_or_fte",
              {
                "field": "four_years_ago",
                "labelBy": "cds/rating_factors/four_years_ago_label",
                "shownBy": "cds/show_prior_triage_years"
              },
              {
                "field": "three_years_ago",
                "labelBy": "cds/rating_factors/three_years_ago_label",
                "shownBy": "cds/show_prior_triage_years"
              },
              {
                "field": "two_years_ago",
                "labelBy": "cds/rating_factors/two_years_ago_label",
                "shownBy": "cds/show_prior_triage_years"
              },
              {
                "field": "one_years_ago",
                "labelBy": "cds/rating_factors/one_years_ago_label"
              },
              {
                "field": "current_year",
                "labelBy": "cds/rating_factors/current_year_label"
              }
            ]}
              kb-interactive={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Historical Bed, Procedure, Doctor and Resident Calculation"
          defaultCollapsed={true}>
          <HX.Pane>
            <HX.Table data={[
              "cds/exposure/granular/triage_historical_obe"
            ]}
              fields={[
              "category",
              "exposure_measure",
              "obe_or_fte",
              "obe_equivalent",
              "overall_obe",
              {
                "field": "four_years_ago",
                "labelBy": "cds/rating_factors/four_years_ago_label",
                "shownBy": "cds/show_prior_triage_years"
              },
              {
                "field": "three_years_ago",
                "labelBy": "cds/rating_factors/three_years_ago_label",
                "shownBy": "cds/show_prior_triage_years"
              },
              {
                "field": "two_years_ago",
                "labelBy": "cds/rating_factors/two_years_ago_label",
                "shownBy": "cds/show_prior_triage_years"
              },
              {
                "field": "one_years_ago",
                "labelBy": "cds/rating_factors/one_years_ago_label"
              },
              {
                "field": "current_year",
                "labelBy": "cds/rating_factors/current_year_label"
              }
            ]} />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Aggregation"
        fullWidth={true}
        viewScale={1}
        shownBy="/cds/glsn_masking">
        <HX.Section title="Potential Aggregation From Overlapping Entities">
          <HX.Pane>
            <HX.Table data={[
              "cds/exposure/granular/glsn_aggregation_details"
            ]}
              fields={[
              "type",
              "name",
              "beazley_insured",
              "aggregated_capacity",
              "notes"
            ]} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Dangerous Ingredients Exception">
          <HX.Pane>
            <HX.Table syncColumnWidthsKey="mySyncedTables1"
              data={[
              {
                "datum": "dimethylamylamine_dmaa",
                "labelAlign": "left"
              },
              {
                "datum": "aconite",
                "labelAlign": "left"
              },
              {
                "datum": "aegeline",
                "labelAlign": "left"
              },
              {
                "datum": "amp_citrate_1_3_dimethylbutylamine_citrate_1_3_dimethylbutylamine_hcl_methylpentanamine",
                "labelAlign": "left"
              },
              {
                "datum": "androsteredione",
                "labelAlign": "left"
              },
              {
                "datum": "aristolochic_acid",
                "labelAlign": "left"
              },
              {
                "datum": "bitter_orange_synephrine",
                "labelAlign": "left"
              },
              {
                "datum": "chaparral",
                "labelAlign": "left"
              },
              {
                "datum": "colloidal_silver",
                "labelAlign": "left"
              },
              {
                "datum": "comfrey",
                "labelAlign": "left"
              },
              {
                "datum": "dendrobium",
                "labelAlign": "left"
              },
              {
                "datum": "ephedra_ephedrine",
                "labelAlign": "left"
              },
              {
                "datum": "germander",
                "labelAlign": "left"
              },
              {
                "datum": "jin_bu_huan",
                "labelAlign": "left"
              },
              {
                "datum": "kava_kava_kava",
                "labelAlign": "left"
              },
              {
                "datum": "lobelia",
                "labelAlign": "left"
              },
              {
                "datum": "over_the_counter_drugs_otc",
                "labelAlign": "left"
              },
              {
                "datum": "pennyroyal_oil",
                "labelAlign": "left"
              },
              {
                "datum": "picamilon_n_nicotinoyl_gaba_pycamilon_pikamilon",
                "labelAlign": "left"
              },
              {
                "datum": "r_beta_methylphenylethylamine_n_methyl_beta_methylphenylethylamine",
                "labelAlign": "left"
              },
              {
                "datum": "stephania",
                "labelAlign": "left"
              },
              {
                "datum": "tiratricol",
                "labelAlign": "left"
              },
              {
                "datum": "vinpocetine_cavinton_intelectol_ethyl_apovincaminate",
                "labelAlign": "left"
              },
              {
                "datum": "yohimbe",
                "labelAlign": "left"
              }
            ]}
              fields={[
              "exposed",
              "revenue",
              "notes"
            ]}
              with="cds/exposure/granular" />
          </HX.Pane>
          <HX.Pane>
            <HX.Table syncColumnWidthsKey="mySyncedTables1"
              data={[
              {
                "datum": "baby_formula",
                "labelAlign": "left"
              },
              {
                "datum": "benzodiazepines",
                "labelAlign": "left"
              },
              {
                "datum": "blood_pressure_pharmaceutcials",
                "labelAlign": "left"
              },
              {
                "datum": "blood_derived_products",
                "labelAlign": "left"
              },
              {
                "datum": "birth_control",
                "labelAlign": "left"
              },
              {
                "datum": "cannabidiol_cbd",
                "labelAlign": "left"
              },
              {
                "datum": "cochlear_implants",
                "labelAlign": "left"
              },
              {
                "datum": "cold_therapy_cryotherapy_products",
                "labelAlign": "left"
              },
              {
                "datum": "cpap_bipap_machines",
                "labelAlign": "left"
              },
              {
                "datum": "diabetes_pharmaceuticals",
                "labelAlign": "left"
              },
              {
                "datum": "ear_plugs",
                "labelAlign": "left"
              },
              {
                "datum": "energy_drinks",
                "labelAlign": "left"
              },
              {
                "datum": "generic_or_off_patent_pharmaceuticals",
                "labelAlign": "left"
              },
              {
                "datum": "hip_implants_metal_on_metal",
                "labelAlign": "left"
              },
              {
                "datum": "ivc_filters",
                "labelAlign": "left"
              },
              {
                "datum": "intrauterine_devices_iuds",
                "labelAlign": "left"
              },
              {
                "datum": "medical_marijuana",
                "labelAlign": "left"
              },
              {
                "datum": "morcellators",
                "labelAlign": "left"
              },
              {
                "datum": "mri_contrast_agents",
                "labelAlign": "left"
              },
              {
                "datum": "neurovascular_stents",
                "labelAlign": "left"
              },
              {
                "datum": "opioids",
                "labelAlign": "left"
              },
              {
                "datum": "pain_pumps",
                "labelAlign": "left"
              },
              {
                "datum": "proton_pump_inhibitors_ppis_antacids",
                "labelAlign": "left"
              },
              {
                "datum": "sexual_enhancement_pharmaceuticals",
                "labelAlign": "left"
              },
              {
                "datum": "silicone_breast_implants",
                "labelAlign": "left"
              },
              {
                "datum": "surgical_mesh",
                "labelAlign": "left"
              },
              {
                "datum": "talcum_powder",
                "labelAlign": "left"
              },
              {
                "datum": "thalidomide",
                "labelAlign": "left"
              },
              {
                "datum": "weight_loss_pharmaceuticals",
                "labelAlign": "left"
              }
            ]}
              fields={[
              "exposed",
              "revenue",
              "notes"
            ]}
              with="cds/exposure/granular" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Other Dangerous Ingredient">
          <HX.Pane>
            <HX.Collection fields={[
              "cds/exposure/granular/glsn_dangerous_ingredient_other_selection"
            ]}
              horizontal={true} />
          </HX.Pane>
          <HX.Pane shownBy="cds/exposure/granular/glsn_dangerous_ingredient_other_selection">
            <HX.Table data={[
              "cds/exposure/granular/glsn_dangerous_ingredient_other"
            ]}
              fields={[
              "name",
              "exposed",
              "revenue",
              "notes"
            ]} />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Pricing"
        fullWidth={true}
        viewScale={1}>
        <HX.Section title="Coverage Selection">
          <HX.Table shownBy="cds/gmm_masking"
            data={[
            {
              "datum": "cds/rating_factors/pricing/professional_liability",
              "labelBy": "cds/rating_factors/pricing/professional_liability/label"
            },
            {
              "datum": "cds/rating_factors/pricing/general_liability",
              "labelBy": "cds/rating_factors/pricing/general_liability/label"
            },
            "cds/rating_factors/pricing/product_liability",
            {
              "datum": "cds/rating_factors/pricing/eo",
              "labelBy": "cds/rating_factors/pricing/eo/label"
            },
            "cds/rating_factors/pricing/sexual_abuse",
            "cds/rating_factors/pricing/employee_benefits_liability",
            "cds/rating_factors/pricing/employers_liability",
            "cds/rating_factors/pricing/tech_eo_products_media"
          ]}
            fields={[
            {
              "field": "include_primary",
              "labelAlign": "left"
            },
            {
              "field": "include_excess",
              "labelAlign": "left"
            },
            {
              "field": "claims_basis",
              "labelAlign": "left"
            },
            {
              "field": "retroactive_date",
              "labelAlign": "left"
            }
          ]}
            title="Coverage Selection"
            filter="show_row"
            kb-interactive={true}
            transpose={true} />
          <HX.Table shownBy="cds/glsn_masking"
            data={[
            "cds/rating_factors/pricing/product_liability",
            "cds/rating_factors/pricing/eo",
            "cds/rating_factors/pricing/healthcare_professional_liability",
            "cds/rating_factors/pricing/general_liability",
            "cds/rating_factors/pricing/sexual_abuse",
            "cds/rating_factors/pricing/employee_benefits_liability",
            "cds/rating_factors/pricing/product_recall",
            "cds/rating_factors/pricing/well_tech_eo_media"
          ]}
            fields={[
            {
              "field": "include_primary",
              "labelAlign": "left"
            },
            {
              "field": "include_excess",
              "labelAlign": "left"
            },
            {
              "field": "claims_basis",
              "labelAlign": "left"
            },
            {
              "field": "retroactive_date",
              "labelAlign": "left"
            },
            {
              "field": "significant_coverage",
              "labelAlign": "left"
            }
          ]}
            title="Coverage Selection"
            filter="show_row"
            kb-interactive={true}
            transpose={true} />
        </HX.Section>
        <HX.Section title="Set Defaults and Copy Options">
          <HX.Pane flow="right">
            <HX.Pane>
              <HX.Collection fields={[
                "cds/default_retention",
                "cds/default_per_claim_limit",
                "cds/default_aggregate_limit"
              ]}
                numCols={3} />
            </HX.Pane>
            <HX.Pane flow="right">
              <HX.Button task="set_defaults_button"
                title="Set Default Inputs" />
              <HX.Collection fields={[
                null
              ]} />
            </HX.Pane>
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Pane>
              <HX.Collection fields={[
                "cds/copy_option_from",
                "cds/copy_option_to",
                null
              ]}
                numCols={3} />
            </HX.Pane>
            <HX.Pane flow="right">
              <HX.Button task="pricing_copy_option"
                title="Copy Option" />
              <HX.Collection fields={[
                null
              ]} />
            </HX.Pane>
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Coverage Details"
          shownBy="cds/gmm_masking">
          <HX.Table shownBy="cds/rating_factors/pricing/professional_liability/include_primary"
            syncColumnWidthsKey="mySyncedTables1"
            data={[
            {
              "datum": "cds/options",
              "elementLabelBy": "option_label"
            }
          ]}
            fields={[
            {
              "field": "coverages/professional_liability/retention",
              "labelAlign": "left"
            },
            {
              "field": "coverages/professional_liability/per_claim_limit",
              "labelAlign": "left"
            },
            {
              "field": "coverages/professional_liability/aggregate_limit",
              "labelAlign": "left"
            }
          ]}
            title="Professional Liability"
            kb-interactive={true}
            transpose={true} />
          <HX.Table shownBy="cds/rating_factors/pricing/general_liability/include_primary"
            syncColumnWidthsKey="mySyncedTables1"
            data={[
            {
              "datum": "cds/options",
              "elementLabelBy": "option_label"
            }
          ]}
            fields={[
            {
              "field": "coverages/general_liability/retention",
              "labelAlign": "left"
            },
            {
              "field": "coverages/general_liability/per_claim_limit",
              "labelAlign": "left"
            },
            {
              "field": "coverages/general_liability/aggregate_limit",
              "labelAlign": "left"
            }
          ]}
            title="General Liability"
            kb-interactive={true}
            transpose={true} />
          <HX.Table shownBy="cds/rating_factors/pricing/product_liability/include_primary"
            syncColumnWidthsKey="mySyncedTables1"
            data={[
            {
              "datum": "cds/options",
              "elementLabelBy": "option_label"
            }
          ]}
            fields={[
            {
              "field": "coverages/product_liability/retention",
              "labelAlign": "left"
            },
            {
              "field": "coverages/product_liability/per_claim_limit",
              "labelAlign": "left"
            },
            {
              "field": "coverages/product_liability/aggregate_limit",
              "labelAlign": "left"
            }
          ]}
            title="Product Liability"
            kb-interactive={true}
            transpose={true} />
          <HX.Table shownBy="cds/rating_factors/pricing/eo/include_primary"
            syncColumnWidthsKey="mySyncedTables1"
            data={[
            {
              "datum": "cds/options",
              "elementLabelBy": "option_label"
            }
          ]}
            fields={[
            {
              "field": "coverages/eo/retention",
              "labelAlign": "left"
            },
            {
              "field": "coverages/eo/per_claim_limit",
              "labelAlign": "left"
            },
            {
              "field": "coverages/eo/aggregate_limit",
              "labelAlign": "left"
            }
          ]}
            title="E&O"
            kb-interactive={true}
            transpose={true} />
          <HX.Table shownBy="cds/rating_factors/pricing/sexual_abuse/include_primary"
            syncColumnWidthsKey="mySyncedTables1"
            data={[
            {
              "datum": "cds/options",
              "elementLabelBy": "option_label"
            }
          ]}
            fields={[
            {
              "field": "coverages/sexual_abuse/retention",
              "labelAlign": "left"
            },
            {
              "field": "coverages/sexual_abuse/per_claim_limit",
              "labelAlign": "left"
            },
            {
              "field": "coverages/sexual_abuse/aggregate_limit",
              "labelAlign": "left"
            }
          ]}
            title="Sexual Abuse"
            kb-interactive={true}
            transpose={true} />
          <HX.Table shownBy="cds/rating_factors/pricing/employee_benefits_liability/include_primary"
            syncColumnWidthsKey="mySyncedTables1"
            data={[
            {
              "datum": "cds/options",
              "elementLabelBy": "option_label"
            }
          ]}
            fields={[
            {
              "field": "coverages/employee_benefits_liability/retention",
              "labelAlign": "left"
            },
            {
              "field": "coverages/employee_benefits_liability/per_claim_limit",
              "labelAlign": "left"
            },
            {
              "field": "coverages/employee_benefits_liability/aggregate_limit",
              "labelAlign": "left"
            }
          ]}
            title="Employee Benefits Liability"
            kb-interactive={true}
            transpose={true} />
          <HX.Table shownBy="cds/rating_factors/pricing/employers_liability/include_primary"
            syncColumnWidthsKey="mySyncedTables1"
            data={[
            {
              "datum": "cds/options",
              "elementLabelBy": "option_label"
            }
          ]}
            fields={[
            {
              "field": "coverages/employers_liability/retention",
              "labelAlign": "left"
            },
            {
              "field": "coverages/employers_liability/per_claim_limit",
              "labelAlign": "left"
            },
            {
              "field": "coverages/employers_liability/aggregate_limit",
              "labelAlign": "left"
            }
          ]}
            title="Employers Liability"
            kb-interactive={true}
            transpose={true} />
          <HX.Table shownBy="cds/rating_factors/pricing/tech_eo_products_media/include_primary"
            syncColumnWidthsKey="mySyncedTables1"
            data={[
            {
              "datum": "cds/options",
              "elementLabelBy": "option_label"
            }
          ]}
            fields={[
            {
              "field": "coverages/tech_eo_products_media/retention",
              "labelAlign": "left"
            },
            {
              "field": "coverages/tech_eo_products_media/per_claim_limit",
              "labelAlign": "left"
            },
            {
              "field": "coverages/tech_eo_products_media/aggregate_limit",
              "labelAlign": "left"
            }
          ]}
            title="Tech E&O/Products/Media"
            kb-interactive={true}
            transpose={true} />
        </HX.Section>
        <HX.Section title="Coverage Details"
          shownBy="cds/glsn_masking">
          <HX.Table shownBy="cds/rating_factors/pricing/product_liability/include_primary"
            syncColumnWidthsKey="mySyncedTables1"
            data={[
            {
              "datum": "cds/options",
              "elementLabelBy": "option_label"
            }
          ]}
            fields={[
            {
              "field": "coverages/product_liability/retention",
              "labelAlign": "left"
            },
            {
              "field": "coverages/product_liability/per_claim_limit",
              "labelAlign": "left"
            },
            {
              "field": "coverages/product_liability/aggregate_limit",
              "labelAlign": "left"
            }
          ]}
            title="Product Liability"
            kb-interactive={true}
            transpose={true} />
          <HX.Table shownBy="cds/rating_factors/pricing/eo/include_primary"
            syncColumnWidthsKey="mySyncedTables1"
            data={[
            {
              "datum": "cds/options",
              "elementLabelBy": "option_label"
            }
          ]}
            fields={[
            {
              "field": "coverages/eo/retention",
              "labelAlign": "left"
            },
            {
              "field": "coverages/eo/per_claim_limit",
              "labelAlign": "left"
            },
            {
              "field": "coverages/eo/aggregate_limit",
              "labelAlign": "left"
            }
          ]}
            title="E&O"
            kb-interactive={true}
            transpose={true} />
          <HX.Table shownBy="cds/rating_factors/pricing/healthcare_professional_liability/include_primary"
            syncColumnWidthsKey="mySyncedTables1"
            data={[
            {
              "datum": "cds/options",
              "elementLabelBy": "option_label"
            }
          ]}
            fields={[
            {
              "field": "coverages/healthcare_professional_liability/retention",
              "labelAlign": "left"
            },
            {
              "field": "coverages/healthcare_professional_liability/per_claim_limit",
              "labelAlign": "left"
            },
            {
              "field": "coverages/healthcare_professional_liability/aggregate_limit",
              "labelAlign": "left"
            }
          ]}
            title="Healthcare Professional Liability"
            kb-interactive={true}
            transpose={true} />
          <HX.Table shownBy="cds/rating_factors/pricing/general_liability/include_primary"
            syncColumnWidthsKey="mySyncedTables1"
            data={[
            {
              "datum": "cds/options",
              "elementLabelBy": "option_label"
            }
          ]}
            fields={[
            {
              "field": "coverages/general_liability/retention",
              "labelAlign": "left"
            },
            {
              "field": "coverages/general_liability/per_claim_limit",
              "labelAlign": "left"
            },
            {
              "field": "coverages/general_liability/aggregate_limit",
              "labelAlign": "left"
            }
          ]}
            title="General Liability"
            kb-interactive={true}
            transpose={true} />
          <HX.Table shownBy="cds/rating_factors/pricing/sexual_abuse/include_primary"
            syncColumnWidthsKey="mySyncedTables1"
            data={[
            {
              "datum": "cds/options",
              "elementLabelBy": "option_label"
            }
          ]}
            fields={[
            {
              "field": "coverages/sexual_abuse/retention",
              "labelAlign": "left"
            },
            {
              "field": "coverages/sexual_abuse/per_claim_limit",
              "labelAlign": "left"
            },
            {
              "field": "coverages/sexual_abuse/aggregate_limit",
              "labelAlign": "left"
            }
          ]}
            title="Sexual Abuse"
            kb-interactive={true}
            transpose={true} />
          <HX.Table shownBy="cds/rating_factors/pricing/employee_benefits_liability/include_primary"
            syncColumnWidthsKey="mySyncedTables1"
            data={[
            {
              "datum": "cds/options",
              "elementLabelBy": "option_label"
            }
          ]}
            fields={[
            {
              "field": "coverages/employee_benefits_liability/retention",
              "labelAlign": "left"
            },
            {
              "field": "coverages/employee_benefits_liability/per_claim_limit",
              "labelAlign": "left"
            },
            {
              "field": "coverages/employee_benefits_liability/aggregate_limit",
              "labelAlign": "left"
            }
          ]}
            title="Employee Benefits Liability"
            kb-interactive={true}
            transpose={true} />
          <HX.Table shownBy="cds/rating_factors/pricing/product_recall/include_primary"
            syncColumnWidthsKey="mySyncedTables1"
            data={[
            {
              "datum": "cds/options",
              "elementLabelBy": "option_label"
            }
          ]}
            fields={[
            {
              "field": "coverages/product_recall/retention",
              "labelAlign": "left"
            },
            {
              "field": "coverages/product_recall/per_claim_limit",
              "labelAlign": "left"
            },
            {
              "field": "coverages/product_recall/aggregate_limit",
              "labelAlign": "left"
            }
          ]}
            title="Product Recall Expenses"
            kb-interactive={true}
            transpose={true} />
          <HX.Table shownBy="cds/rating_factors/pricing/well_tech_eo_media/include_primary"
            syncColumnWidthsKey="mySyncedTables1"
            data={[
            {
              "datum": "cds/options",
              "elementLabelBy": "option_label"
            }
          ]}
            fields={[
            {
              "field": "coverages/well_tech_eo_media/retention",
              "labelAlign": "left"
            },
            {
              "field": "coverages/well_tech_eo_media/per_claim_limit",
              "labelAlign": "left"
            },
            {
              "field": "coverages/well_tech_eo_media/aggregate_limit",
              "labelAlign": "left"
            }
          ]}
            title="Well Tech E&O and Media"
            kb-interactive={true}
            transpose={true} />
        </HX.Section>
        <HX.Section title="Policy Aggregates">
          <HX.Table shownBy="cds/gmm_masking"
            syncColumnWidthsKey="mySyncedTables1"
            data={[
            {
              "datum": "cds/options",
              "elementLabelBy": "option_label"
            }
          ]}
            fields={[
            {
              "field": "agg_limit",
              "labelAlign": "left"
            },
            {
              "field": "indemnity_only",
              "labelAlign": "left",
              "shownBy": "cds/international_masking"
            }
          ]}
            kb-interactive={true}
            transpose={true} />
          <HX.Table shownBy="cds/glsn_masking"
            syncColumnWidthsKey="mySyncedTables1"
            data={[
            {
              "datum": "cds/options",
              "elementLabelBy": "option_label"
            }
          ]}
            fields={[
            {
              "field": "agg_retention",
              "labelAlign": "left"
            },
            {
              "field": "agg_limit",
              "labelAlign": "left"
            },
            {
              "field": "indemnity_only",
              "labelAlign": "left",
              "shownBy": "cds/international_masking"
            }
          ]}
            kb-interactive={true}
            transpose={true} />
        </HX.Section>
        <HX.Section title="Coverage Enhancements - Primary">
          <HX.Table syncColumnWidthsKey="mySyncedTables1"
            data={[
            {
              "datum": "cds/options",
              "elementLabelBy": "option_label"
            }
          ]}
            fields={[
            {
              "field": "include_stop_gap_primary",
              "labelAlign": "left",
              "shownBy": "cds/us_masking"
            },
            {
              "field": "include_tria_primary",
              "labelAlign": "left",
              "shownBy": "cds/us_masking"
            },
            {
              "field": "include_punitive_damages_primary",
              "labelAlign": "left",
              "shownBy": "/cds/punitive_damages_masking"
            }
          ]}
            kb-interactive={true}
            transpose={true} />
          <HX.Table syncColumnWidthsKey="mySyncedTables1"
            data={[
            {
              "datum": "cds/options",
              "elementLabelBy": "option_label"
            }
          ]}
            fields={[
            {
              "field": "include_costs_in_addition_primary",
              "labelAlign": "left"
            },
            {
              "field": "costs_in_addition_selection",
              "labelAlign": "left"
            }
          ]}
            kb-interactive={true}
            transpose={true} />
          <HX.Table syncColumnWidthsKey="mySyncedTables1"
            data={[
            {
              "datum": "cds/options",
              "elementLabelBy": "option_label"
            }
          ]}
            fields={[
            {
              "field": "include_auto_primary",
              "labelAlign": "left"
            },
            {
              "field": "auto_measure",
              "labelAlign": "left"
            },
            {
              "field": "auto_amount",
              "labelAlign": "left"
            }
          ]}
            kb-interactive={true}
            transpose={true} />
        </HX.Section>
        <HX.Section title="Coverage Enhancements - Excess">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              {
                "field": "cds/rating_factors/pricing/include_stop_gap_excess",
                "shownBy": "cds/us_masking"
              },
              {
                "field": "cds/rating_factors/pricing/include_tria_excess",
                "shownBy": "cds/us_masking"
              },
              {
                "field": "cds/rating_factors/pricing/include_punitive_damages_excess",
                "shownBy": "/cds/punitive_damages_masking"
              },
              "cds/rating_factors/pricing/include_costs_in_addition_excess",
              "cds/rating_factors/pricing/include_auto_excess"
            ]} />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Primary Layer">
          <HX.Table syncColumnWidthsKey="mySyncedTables1"
            data={[
            {
              "datum": "cds/options",
              "elementLabelBy": "option_label"
            }
          ]}
            fields={[
            {
              "field": "brokerage_primary",
              "labelAlign": "left"
            },
            {
              "field": "cyber_premium_primary",
              "labelAlign": "left"
            },
            {
              "field": "model_premium_primary",
              "labelAlign": "left"
            },
            {
              "field": "minimum_premium_primary",
              "labelAlign": "left"
            },
            {
              "field": "gross_premium_primary",
              "labelAlign": "left"
            },
            {
              "field": "quoted_premium_primary",
              "labelAlign": "left"
            },
            {
              "field": "bpi_primary",
              "labelAlign": "left"
            }
          ]}
            kb-interactive={true}
            transpose={true} />
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "cds/add_excess_1"
            ]}
              horizontal={true} />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Excess Layers"
          shownBy="cds/add_excess_1">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "cds/rating_factors/pricing/claims_basis_1_excess",
              "cds/rating_factors/pricing/retroactive_date_1_excess"
            ]}
              horizontal={true} />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
          <HX.Table syncColumnWidthsKey="mySyncedTables1"
            data={[
            {
              "datum": "cds/options",
              "elementLabelBy": "option_label"
            }
          ]}
            fields={[
            {
              "field": "per_claim_limit_1_excess",
              "labelAlign": "left"
            },
            {
              "field": "aggregate_limit_1_excess",
              "labelAlign": "left"
            },
            {
              "field": "brokerage_1_excess",
              "labelAlign": "left"
            },
            {
              "field": "supported_excess_premium_1_excess",
              "labelAlign": "left"
            },
            {
              "field": "umbrella_premium_1_excess",
              "labelAlign": "left"
            },
            {
              "field": "model_premium_1_excess",
              "labelAlign": "left"
            },
            {
              "field": "minimum_premium_1_excess",
              "labelAlign": "left"
            },
            {
              "field": "gross_premium_1_excess",
              "labelAlign": "left"
            },
            {
              "field": "quoted_premium_1_excess",
              "labelAlign": "left"
            },
            {
              "field": "bpi_1_excess",
              "labelAlign": "left"
            },
            {
              "field": "comment_1_excess",
              "labelAlign": "left"
            }
          ]}
            title="1st Excess Layer"
            kb-interactive={true}
            transpose={true} />
          <HX.Pane flow="right">
            <HX.Collection shownBy="cds/add_excess_1"
              fields={[
              "cds/add_excess_2"
            ]}
              horizontal={true} />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Collection shownBy="cds/add_excess_2"
              fields={[
              "cds/rating_factors/pricing/claims_basis_2_excess",
              "cds/rating_factors/pricing/retroactive_date_2_excess"
            ]}
              horizontal={true} />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
          <HX.Table shownBy="cds/add_excess_2"
            syncColumnWidthsKey="mySyncedTables1"
            data={[
            {
              "datum": "cds/options",
              "elementLabelBy": "option_label"
            }
          ]}
            fields={[
            {
              "field": "per_claim_limit_2_excess",
              "labelAlign": "left"
            },
            {
              "field": "aggregate_limit_2_excess",
              "labelAlign": "left"
            },
            {
              "field": "brokerage_2_excess",
              "labelAlign": "left"
            },
            {
              "field": "supported_excess_premium_2_excess",
              "labelAlign": "left"
            },
            {
              "field": "umbrella_premium_2_excess",
              "labelAlign": "left"
            },
            {
              "field": "model_premium_2_excess",
              "labelAlign": "left"
            },
            {
              "field": "minimum_premium_2_excess",
              "labelAlign": "left"
            },
            {
              "field": "gross_premium_2_excess",
              "labelAlign": "left"
            },
            {
              "field": "quoted_premium_2_excess",
              "labelAlign": "left"
            },
            {
              "field": "bpi_2_excess",
              "labelAlign": "left"
            },
            {
              "field": "comment_2_excess",
              "labelAlign": "left"
            }
          ]}
            title="2nd Excess Layer"
            kb-interactive={true}
            transpose={true} />
          <HX.Pane flow="right">
            <HX.Collection shownBy="cds/add_excess_2"
              fields={[
              "cds/add_excess_3"
            ]}
              horizontal={true} />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Collection shownBy="cds/add_excess_3"
              fields={[
              "cds/rating_factors/pricing/claims_basis_3_excess",
              "cds/rating_factors/pricing/retroactive_date_3_excess"
            ]}
              horizontal={true} />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
          <HX.Table shownBy="cds/add_excess_3"
            syncColumnWidthsKey="mySyncedTables1"
            data={[
            {
              "datum": "cds/options",
              "elementLabelBy": "option_label"
            }
          ]}
            fields={[
            {
              "field": "per_claim_limit_3_excess",
              "labelAlign": "left"
            },
            {
              "field": "aggregate_limit_3_excess",
              "labelAlign": "left"
            },
            {
              "field": "brokerage_3_excess",
              "labelAlign": "left"
            },
            {
              "field": "supported_excess_premium_3_excess",
              "labelAlign": "left"
            },
            {
              "field": "umbrella_premium_3_excess",
              "labelAlign": "left"
            },
            {
              "field": "model_premium_3_excess",
              "labelAlign": "left"
            },
            {
              "field": "minimum_premium_3_excess",
              "labelAlign": "left"
            },
            {
              "field": "gross_premium_3_excess",
              "labelAlign": "left"
            },
            {
              "field": "quoted_premium_3_excess",
              "labelAlign": "left"
            },
            {
              "field": "bpi_3_excess",
              "labelAlign": "left"
            },
            {
              "field": "comment_3_excess",
              "labelAlign": "left"
            }
          ]}
            title="3rd Excess Layer"
            kb-interactive={true}
            transpose={true} />
          <HX.Pane flow="right">
            <HX.Collection shownBy="cds/add_excess_3"
              fields={[
              "cds/add_excess_4"
            ]}
              horizontal={true} />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Collection shownBy="cds/add_excess_4"
              fields={[
              "cds/rating_factors/pricing/claims_basis_4_excess",
              "cds/rating_factors/pricing/retroactive_date_4_excess"
            ]}
              horizontal={true} />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
          <HX.Table shownBy="cds/add_excess_4"
            syncColumnWidthsKey="mySyncedTables1"
            data={[
            {
              "datum": "cds/options",
              "elementLabelBy": "option_label"
            }
          ]}
            fields={[
            {
              "field": "per_claim_limit_4_excess",
              "labelAlign": "left"
            },
            {
              "field": "aggregate_limit_4_excess",
              "labelAlign": "left"
            },
            {
              "field": "brokerage_4_excess",
              "labelAlign": "left"
            },
            {
              "field": "supported_excess_premium_4_excess",
              "labelAlign": "left"
            },
            {
              "field": "umbrella_premium_4_excess",
              "labelAlign": "left"
            },
            {
              "field": "model_premium_4_excess",
              "labelAlign": "left"
            },
            {
              "field": "minimum_premium_4_excess",
              "labelAlign": "left"
            },
            {
              "field": "gross_premium_4_excess",
              "labelAlign": "left"
            },
            {
              "field": "quoted_premium_4_excess",
              "labelAlign": "left"
            },
            {
              "field": "bpi_4_excess",
              "labelAlign": "left"
            },
            {
              "field": "comment_4_excess",
              "labelAlign": "left"
            }
          ]}
            title="4th Excess Layer"
            kb-interactive={true}
            transpose={true} />
          <HX.Pane flow="right">
            <HX.Collection shownBy="cds/add_excess_4"
              fields={[
              "cds/add_excess_5"
            ]}
              horizontal={true} />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Collection shownBy="cds/add_excess_5"
              fields={[
              "cds/rating_factors/pricing/claims_basis_5_excess",
              "cds/rating_factors/pricing/retroactive_date_5_excess"
            ]}
              horizontal={true} />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
          <HX.Table shownBy="cds/add_excess_5"
            syncColumnWidthsKey="mySyncedTables1"
            data={[
            {
              "datum": "cds/options",
              "elementLabelBy": "option_label"
            }
          ]}
            fields={[
            {
              "field": "per_claim_limit_5_excess",
              "labelAlign": "left"
            },
            {
              "field": "aggregate_limit_5_excess",
              "labelAlign": "left"
            },
            {
              "field": "brokerage_5_excess",
              "labelAlign": "left"
            },
            {
              "field": "supported_excess_premium_5_excess",
              "labelAlign": "left"
            },
            {
              "field": "umbrella_premium_5_excess",
              "labelAlign": "left"
            },
            {
              "field": "model_premium_5_excess",
              "labelAlign": "left"
            },
            {
              "field": "minimum_premium_5_excess",
              "labelAlign": "left"
            },
            {
              "field": "gross_premium_5_excess",
              "labelAlign": "left"
            },
            {
              "field": "quoted_premium_5_excess",
              "labelAlign": "left"
            },
            {
              "field": "bpi_5_excess",
              "labelAlign": "left"
            },
            {
              "field": "comment_5_excess",
              "labelAlign": "left"
            }
          ]}
            title="5th Excess Layer"
            kb-interactive={true}
            transpose={true} />
          <HX.Pane flow="right">
            <HX.Collection shownBy="cds/add_excess_5"
              fields={[
              "cds/add_excess_6"
            ]}
              horizontal={true} />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Collection shownBy="cds/add_excess_6"
              fields={[
              "cds/rating_factors/pricing/claims_basis_6_excess",
              "cds/rating_factors/pricing/retroactive_date_6_excess"
            ]}
              horizontal={true} />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
          <HX.Table shownBy="cds/add_excess_6"
            syncColumnWidthsKey="mySyncedTables1"
            data={[
            {
              "datum": "cds/options",
              "elementLabelBy": "option_label"
            }
          ]}
            fields={[
            {
              "field": "per_claim_limit_6_excess",
              "labelAlign": "left"
            },
            {
              "field": "aggregate_limit_6_excess",
              "labelAlign": "left"
            },
            {
              "field": "brokerage_6_excess",
              "labelAlign": "left"
            },
            {
              "field": "supported_excess_premium_6_excess",
              "labelAlign": "left"
            },
            {
              "field": "umbrella_premium_6_excess",
              "labelAlign": "left"
            },
            {
              "field": "model_premium_6_excess",
              "labelAlign": "left"
            },
            {
              "field": "minimum_premium_6_excess",
              "labelAlign": "left"
            },
            {
              "field": "gross_premium_6_excess",
              "labelAlign": "left"
            },
            {
              "field": "quoted_premium_6_excess",
              "labelAlign": "left"
            },
            {
              "field": "bpi_6_excess",
              "labelAlign": "left"
            },
            {
              "field": "comment_6_excess",
              "labelAlign": "left"
            }
          ]}
            title="6th Excess Layer"
            kb-interactive={true}
            transpose={true} />
          <HX.Pane flow="right">
            <HX.Collection shownBy="cds/add_excess_6"
              fields={[
              "cds/add_excess_7"
            ]}
              horizontal={true} />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Collection shownBy="cds/add_excess_7"
              fields={[
              "cds/rating_factors/pricing/claims_basis_7_excess",
              "cds/rating_factors/pricing/retroactive_date_7_excess"
            ]}
              horizontal={true} />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
          <HX.Table shownBy="cds/add_excess_7"
            syncColumnWidthsKey="mySyncedTables1"
            data={[
            {
              "datum": "cds/options",
              "elementLabelBy": "option_label"
            }
          ]}
            fields={[
            {
              "field": "per_claim_limit_7_excess",
              "labelAlign": "left"
            },
            {
              "field": "aggregate_limit_7_excess",
              "labelAlign": "left"
            },
            {
              "field": "brokerage_7_excess",
              "labelAlign": "left"
            },
            {
              "field": "supported_excess_premium_7_excess",
              "labelAlign": "left"
            },
            {
              "field": "umbrella_premium_7_excess",
              "labelAlign": "left"
            },
            {
              "field": "model_premium_7_excess",
              "labelAlign": "left"
            },
            {
              "field": "minimum_premium_7_excess",
              "labelAlign": "left"
            },
            {
              "field": "gross_premium_7_excess",
              "labelAlign": "left"
            },
            {
              "field": "quoted_premium_7_excess",
              "labelAlign": "left"
            },
            {
              "field": "bpi_7_excess",
              "labelAlign": "left"
            },
            {
              "field": "comment_7_excess",
              "labelAlign": "left"
            }
          ]}
            title="7th Excess Layer"
            kb-interactive={true}
            transpose={true} />
          <HX.Pane flow="right">
            <HX.Collection shownBy="cds/add_excess_7"
              fields={[
              "cds/add_excess_8"
            ]}
              horizontal={true} />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Collection shownBy="cds/add_excess_8"
              fields={[
              "cds/rating_factors/pricing/claims_basis_8_excess",
              "cds/rating_factors/pricing/retroactive_date_8_excess"
            ]}
              horizontal={true} />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
          <HX.Table shownBy="cds/add_excess_8"
            syncColumnWidthsKey="mySyncedTables1"
            data={[
            {
              "datum": "cds/options",
              "elementLabelBy": "option_label"
            }
          ]}
            fields={[
            {
              "field": "per_claim_limit_8_excess",
              "labelAlign": "left"
            },
            {
              "field": "aggregate_limit_8_excess",
              "labelAlign": "left"
            },
            {
              "field": "brokerage_8_excess",
              "labelAlign": "left"
            },
            {
              "field": "supported_excess_premium_8_excess",
              "labelAlign": "left"
            },
            {
              "field": "umbrella_premium_8_excess",
              "labelAlign": "left"
            },
            {
              "field": "model_premium_8_excess",
              "labelAlign": "left"
            },
            {
              "field": "minimum_premium_8_excess",
              "labelAlign": "left"
            },
            {
              "field": "gross_premium_8_excess",
              "labelAlign": "left"
            },
            {
              "field": "quoted_premium_8_excess",
              "labelAlign": "left"
            },
            {
              "field": "bpi_8_excess",
              "labelAlign": "left"
            },
            {
              "field": "comment_8_excess",
              "labelAlign": "left"
            }
          ]}
            title="8th Excess Layer"
            kb-interactive={true}
            transpose={true} />
          <HX.Pane flow="right">
            <HX.Collection shownBy="cds/add_excess_8"
              fields={[
              "cds/add_excess_9"
            ]}
              horizontal={true} />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Collection shownBy="cds/add_excess_9"
              fields={[
              "cds/rating_factors/pricing/claims_basis_9_excess",
              "cds/rating_factors/pricing/retroactive_date_9_excess"
            ]}
              horizontal={true} />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
          <HX.Table shownBy="cds/add_excess_9"
            syncColumnWidthsKey="mySyncedTables1"
            data={[
            {
              "datum": "cds/options",
              "elementLabelBy": "option_label"
            }
          ]}
            fields={[
            {
              "field": "per_claim_limit_9_excess",
              "labelAlign": "left"
            },
            {
              "field": "aggregate_limit_9_excess",
              "labelAlign": "left"
            },
            {
              "field": "brokerage_9_excess",
              "labelAlign": "left"
            },
            {
              "field": "supported_excess_premium_9_excess",
              "labelAlign": "left"
            },
            {
              "field": "umbrella_premium_9_excess",
              "labelAlign": "left"
            },
            {
              "field": "model_premium_9_excess",
              "labelAlign": "left"
            },
            {
              "field": "minimum_premium_9_excess",
              "labelAlign": "left"
            },
            {
              "field": "gross_premium_9_excess",
              "labelAlign": "left"
            },
            {
              "field": "quoted_premium_9_excess",
              "labelAlign": "left"
            },
            {
              "field": "bpi_9_excess",
              "labelAlign": "left"
            },
            {
              "field": "comment_9_excess",
              "labelAlign": "left"
            }
          ]}
            title="9th Excess Layer"
            kb-interactive={true}
            transpose={true} />
          <HX.Pane flow="right">
            <HX.Collection shownBy="cds/add_excess_9"
              fields={[
              "cds/add_excess_10"
            ]}
              horizontal={true} />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Collection shownBy="cds/add_excess_10"
              fields={[
              "cds/rating_factors/pricing/claims_basis_10_excess",
              "cds/rating_factors/pricing/retroactive_date_10_excess"
            ]}
              horizontal={true} />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
          <HX.Table shownBy="cds/add_excess_10"
            syncColumnWidthsKey="mySyncedTables1"
            data={[
            {
              "datum": "cds/options",
              "elementLabelBy": "option_label"
            }
          ]}
            fields={[
            {
              "field": "per_claim_limit_10_excess",
              "labelAlign": "left"
            },
            {
              "field": "aggregate_limit_10_excess",
              "labelAlign": "left"
            },
            {
              "field": "brokerage_10_excess",
              "labelAlign": "left"
            },
            {
              "field": "supported_excess_premium_10_excess",
              "labelAlign": "left"
            },
            {
              "field": "umbrella_premium_10_excess",
              "labelAlign": "left"
            },
            {
              "field": "model_premium_10_excess",
              "labelAlign": "left"
            },
            {
              "field": "minimum_premium_10_excess",
              "labelAlign": "left"
            },
            {
              "field": "gross_premium_10_excess",
              "labelAlign": "left"
            },
            {
              "field": "quoted_premium_10_excess",
              "labelAlign": "left"
            },
            {
              "field": "bpi_10_excess",
              "labelAlign": "left"
            },
            {
              "field": "comment_10_excess",
              "labelAlign": "left"
            }
          ]}
            title="10th Excess Layer"
            kb-interactive={true}
            transpose={true} />
        </HX.Section>
        <HX.Section title="Selected Option">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "cds/option_selected"
            ]}
              horizontal={true} />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Tech E&O"
        fullWidth={true}
        viewScale={1}>
        <HX.Section title="Tech E&O">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "cds/exposure/aggregate/tech_eo_rateble_revenue"
            ]} />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Collection fields={[
              "cds/exposure/aggregate/tech_eo_total_revenue"
            ]} />
          </HX.Pane>
          <HX.Pane>
            <HX.Table data={[
              {
                "datum": "reseller_distributor",
                "labelAlign": "left"
              },
              {
                "datum": "training_education",
                "labelAlign": "left"
              },
              {
                "datum": "prepackaged_software_products_services",
                "labelAlign": "left"
              },
              {
                "datum": "live_video_mobile_health_store_forward",
                "labelAlign": "left"
              },
              {
                "datum": "teleneurology_or_teleradiology",
                "labelAlign": "left"
              },
              {
                "datum": "technology_companies_platform_hosts",
                "labelAlign": "left"
              },
              {
                "datum": "software_hardware_management_systems_non_medical",
                "labelAlign": "left"
              },
              {
                "datum": "custom_software_development",
                "labelAlign": "left"
              },
              {
                "datum": "internet_based_services_products",
                "labelAlign": "left"
              },
              {
                "datum": "other",
                "labelAlign": "left"
              },
              {
                "datum": "custom_hardware_development",
                "labelAlign": "left"
              },
              {
                "datum": "software_hardware_medical_management",
                "labelAlign": "left"
              }
            ]}
              fields={[
              "tech_eo_percent_rateble_revenue",
              "tech_eo_class",
              "tech_eo_revenue"
            ]}
              title="Revenue by Class"
              with="cds/exposure/granular"
              kb-interactive={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Contingent BI/PD"
          shownBy="cds/glsn_masking">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "cds/rating_factors/tech_eo/contingent_bi_pd",
              "cds/rating_factors/tech_eo/contingent_bi_pd_factor"
            ]}
              horizontal={true} />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Cyber"
        fullWidth={true}
        viewScale={1}>
        <HX.Section title="Product">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "cds/rating_factors/cyber/first_or_third_party",
              "cds/rating_factors/cyber/first_or_third_party_note",
              null
            ]}
              numCols={3} />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "cds/rating_factors/cyber/product",
              "cds/rating_factors/cyber/include_excess",
              "cds/rating_factors/cyber/excess_cyber_note"
            ]}
              numCols={3} />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "cds/rating_factors/cyber/excess_cyber_calc_note"
            ]} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Copy Options">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "cds/cyber_copy_option_from"
            ]} />
            <HX.Collection fields={[
              "cds/cyber_copy_option_to"
            ]} />
            <HX.Button task="cyber_copy_option"
              title="Copy Option" />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Limits">
          <HX.Table shownBy="cds/bbr_masking"
            syncColumnWidthsKey="mySyncedTables1"
            data={[
            {
              "datum": "cds/cyber_options",
              "elementLabelBy": "option_label"
            }
          ]}
            fields={[
            {
              "field": "notified_individuals_limit",
              "labelAlign": "left"
            },
            {
              "field": "legal_forensic_limit",
              "labelAlign": "left"
            },
            {
              "field": "additional_breach_costs_limit",
              "labelAlign": "left"
            }
          ]}
            title="Breach Response"
            kb-interactive={true}
            transpose={true} />
          <HX.Table syncColumnWidthsKey="mySyncedTables1"
            data={[
            {
              "datum": "cds/cyber_options",
              "elementLabelBy": "option_label"
            }
          ]}
            fields={[
            {
              "field": "policy_agg_limit",
              "labelAlign": "left"
            },
            {
              "field": "infosec_breach_response_limit",
              "labelAlign": "left",
              "shownBy": "/cds/infosec_masking"
            }
          ]}
            title="Aggregate"
            kb-interactive={true}
            transpose={true} />
          <HX.Table syncColumnWidthsKey="mySyncedTables1"
            data={[
            {
              "datum": "cds/cyber_options",
              "elementLabelBy": "option_label"
            }
          ]}
            fields={[
            {
              "field": "data_network_limit",
              "labelAlign": "left"
            },
            {
              "field": "defense_penalties_limit",
              "labelAlign": "left"
            },
            {
              "field": "payment_card_limit",
              "labelAlign": "left"
            }
          ]}
            title="Liability"
            kb-interactive={true}
            transpose={true} />
        </HX.Section>
        <HX.Section title="Retentions">
          <HX.Table shownBy="cds/bbr_masking"
            syncColumnWidthsKey="mySyncedTables1"
            data={[
            {
              "datum": "cds/cyber_options",
              "elementLabelBy": "option_label"
            }
          ]}
            fields={[
            {
              "field": "legal_forensic_retention",
              "labelAlign": "left"
            },
            {
              "field": "legal_forensic_subretention",
              "labelAlign": "left"
            }
          ]}
            title="Breach response"
            kb-interactive={true}
            transpose={true} />
          <HX.Table syncColumnWidthsKey="mySyncedTables1"
            data={[
            {
              "datum": "cds/cyber_options",
              "elementLabelBy": "option_label"
            }
          ]}
            fields={[
            {
              "field": "policy_agg_retention",
              "labelAlign": "left"
            }
          ]}
            title="Aggregate"
            kb-interactive={true}
            transpose={true} />
          <HX.Table syncColumnWidthsKey="mySyncedTables1"
            data={[
            {
              "datum": "cds/cyber_options",
              "elementLabelBy": "option_label"
            }
          ]}
            fields={[
            {
              "field": "breach_response_retention",
              "labelAlign": "left",
              "shownBy": "/cds/infosec_masking"
            },
            {
              "field": "data_network_retention",
              "labelAlign": "left"
            },
            {
              "field": "defense_penalties_retention",
              "labelAlign": "left"
            },
            {
              "field": "payment_card_retention",
              "labelAlign": "left"
            }
          ]}
            title="Liability"
            kb-interactive={true}
            transpose={true} />
        </HX.Section>
        <HX.Section title="Loss Rating">
          <HX.Table syncColumnWidthsKey="mySyncedTables2"
            data={[
            "cds/modifiers/cyber/cyber_loss_rating"
          ]}
            fields={[
            "cyber_loss_ratio",
            "cyber_loss_ratio_min",
            "cyber_loss_ratio_max",
            "cyber_loss_ratio_selected"
          ]}
            kb-interactive={true} />
        </HX.Section>
        <HX.Section title="Schedule Rating">
          <HX.Table syncColumnWidthsKey="mySyncedTables2"
            data={[
            {
              "datum": "cyber_financial_condition",
              "labelAlign": "left"
            },
            {
              "datum": "cyber_maturity_of_business",
              "labelAlign": "left"
            },
            {
              "datum": "cyber_quality_of_management",
              "labelAlign": "left"
            },
            {
              "datum": "cyber_volume_of_information_stored",
              "labelAlign": "left"
            }
          ]}
            fields={[
            "min",
            "max",
            "value",
            "comment"
          ]}
            with="cds/modifiers/cyber"
            kb-interactive={true} />
        </HX.Section>
        <HX.Section title="Cyber Summary">
          <HX.Table syncColumnWidthsKey="mySyncedTables1"
            data={[
            {
              "datum": "cds/cyber_options",
              "elementLabelBy": "option_label"
            }
          ]}
            fields={[
            {
              "field": "brokerage",
              "labelAlign": "left"
            },
            {
              "field": "model_premium_third_party",
              "infoBy": "/cds/rating_factors/cyber/third_party_only_info_by",
              "labelAlign": "left",
              "shownBy": "/cds/rating_factors/cyber/third_party_only_show"
            },
            {
              "field": "model_premium_bbr_rater",
              "infoBy": "/cds/rating_factors/cyber/bbr_rater_info_by",
              "labelAlign": "left",
              "shownBy": "/cds/rating_factors/cyber/first_and_third_party_show"
            }
          ]}
            kb-interactive={true}
            transpose={true} />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Umbrella"
        fullWidth={true}
        viewScale={1}>
        <HX.Section title="Umbrella Coverages">
          <HX.Pane>
            <HX.Table shownBy="/cds/gmm_masking"
              data={[
              {
                "datum": "auto_liability",
                "labelAlign": "left"
              },
              {
                "datum": "employers_liability",
                "labelAlign": "left"
              },
              {
                "datum": "general_liability",
                "labelAlign": "left"
              },
              {
                "datum": "foreign_liability",
                "labelAlign": "left"
              },
              {
                "datum": "aircraft_nonowned",
                "labelAlign": "left"
              },
              {
                "datum": "aircraft_owned",
                "labelAlign": "left"
              },
              {
                "datum": "auto_ambulance",
                "labelAlign": "left"
              },
              {
                "datum": "educators_liability",
                "labelAlign": "left"
              },
              {
                "datum": "garage_keepers_liability",
                "labelAlign": "left"
              },
              {
                "datum": "helipad",
                "labelAlign": "left"
              },
              {
                "datum": "liquor_law_liability",
                "labelAlign": "left"
              },
              {
                "datum": "managed_care_eo_health_plan",
                "labelAlign": "left"
              },
              {
                "datum": "managed_care_eo_nonhealth_plan",
                "labelAlign": "left"
              },
              {
                "datum": "watercraft_nonowned",
                "labelAlign": "left"
              },
              {
                "datum": "watercraft_owned",
                "labelAlign": "left"
              }
            ]}
              fields={[
              "underlying_ee",
              "underlying_agg",
              "underlying_premium",
              "occurrence_cover"
            ]}
              with="cds/rating_factors/gmm/umbrella"
              kb-interactive={true} />
            <HX.Table shownBy="/cds/glsn_masking"
              data={[
              {
                "datum": "auto_liability",
                "labelAlign": "left"
              },
              {
                "datum": "employers_liability",
                "labelAlign": "left"
              },
              {
                "datum": "general_liability",
                "labelAlign": "left"
              },
              {
                "datum": "foreign_liability",
                "labelAlign": "left"
              },
              {
                "datum": "aircraft_nonowned",
                "labelAlign": "left"
              },
              {
                "datum": "aircraft_owned",
                "labelAlign": "left"
              },
              {
                "datum": "garage_keepers_liability",
                "labelAlign": "left"
              },
              {
                "datum": "liquor_law_liability",
                "labelAlign": "left"
              },
              {
                "datum": "watercraft_non_owned",
                "labelAlign": "left"
              },
              {
                "datum": "watercraft_owned",
                "labelAlign": "left"
              },
              {
                "datum": "foreign_employers_liability",
                "labelAlign": "left"
              },
              {
                "datum": "foreign_general_liability",
                "labelAlign": "left"
              },
              {
                "datum": "foreign_auto_liability",
                "labelAlign": "left"
              }
            ]}
              fields={[
              "underlying_ee",
              "underlying_agg",
              "underlying_premium",
              "occurrence_cover"
            ]}
              with="cds/rating_factors/glsn/umbrella"
              kb-interactive={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Umbrella Calculations Option 1"
          shownBy="cds/show_option_1">
          <HX.With context={{
            "index": 0,
            "path": "cds/options",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Table kb-interactive={true}
                shownBy="/cds/gmm_masking"
                data={[
                {
                  "datum": "gmm_auto_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_employers_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_general_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_foreign_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_aircraft_nonowned",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_aircraft_owned",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_auto_ambulance",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_educators_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_garage_keepers_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_helipad",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_liquor_law_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_managed_care_eo_health_plan",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_managed_care_eo_nonhealth_plan",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_watercraft_nonowned",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_watercraft_owned",
                  "labelAlign": "left"
                },
                null,
                {
                  "datum": "umbrella_eel",
                  "labelAlign": "left"
                },
                null,
                {
                  "datum": "umbrella_unsupported_net_premium",
                  "labelAlign": "left"
                },
                {
                  "datum": "umbrella_total_excess_net_premium",
                  "labelAlign": "left"
                },
                null,
                {
                  "datum": "umbrella_munich_cession_net",
                  "labelAlign": "left"
                },
                {
                  "datum": "umbrella_munich_cession_gross",
                  "labelAlign": "left"
                }
              ]}
                fields={[
                "premium_primary",
                {
                  "field": "premium_1_excess",
                  "shownBy": "/cds/add_excess_1"
                },
                {
                  "field": "premium_2_excess",
                  "shownBy": "/cds/add_excess_2"
                },
                {
                  "field": "premium_3_excess",
                  "shownBy": "/cds/add_excess_3"
                },
                {
                  "field": "premium_4_excess",
                  "shownBy": "/cds/add_excess_4"
                },
                {
                  "field": "premium_5_excess",
                  "shownBy": "/cds/add_excess_5"
                },
                {
                  "field": "premium_6_excess",
                  "shownBy": "/cds/add_excess_6"
                },
                {
                  "field": "premium_7_excess",
                  "shownBy": "/cds/add_excess_7"
                },
                {
                  "field": "premium_8_excess",
                  "shownBy": "/cds/add_excess_8"
                },
                {
                  "field": "premium_9_excess",
                  "shownBy": "/cds/add_excess_9"
                },
                {
                  "field": "premium_10_excess",
                  "shownBy": "/cds/add_excess_10"
                }
              ]}
                title="Option 1" />
              <HX.Table kb-interactive={true}
                shownBy="/cds/gmm_masking"
                data={[
                {
                  "datum": "gmm_auto_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_employers_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_general_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_foreign_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_aircraft_nonowned",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_aircraft_owned",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_auto_ambulance",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_educators_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_garage_keepers_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_helipad",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_liquor_law_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_managed_care_eo_health_plan",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_managed_care_eo_nonhealth_plan",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_watercraft_nonowned",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_watercraft_owned",
                  "labelAlign": "left"
                }
              ]}
                fields={[
                {
                  "field": "cession_premium_split_1_excess",
                  "shownBy": "/cds/add_excess_1"
                },
                {
                  "field": "cession_premium_split_2_excess",
                  "shownBy": "/cds/add_excess_2"
                },
                {
                  "field": "cession_premium_split_3_excess",
                  "shownBy": "/cds/add_excess_3"
                },
                {
                  "field": "cession_premium_split_4_excess",
                  "shownBy": "/cds/add_excess_4"
                },
                {
                  "field": "cession_premium_split_5_excess",
                  "shownBy": "/cds/add_excess_5"
                },
                {
                  "field": "cession_premium_split_6_excess",
                  "shownBy": "/cds/add_excess_6"
                },
                {
                  "field": "cession_premium_split_7_excess",
                  "shownBy": "/cds/add_excess_7"
                },
                {
                  "field": "cession_premium_split_8_excess",
                  "shownBy": "/cds/add_excess_8"
                },
                {
                  "field": "cession_premium_split_9_excess",
                  "shownBy": "/cds/add_excess_9"
                },
                {
                  "field": "cession_premium_split_10_excess",
                  "shownBy": "/cds/add_excess_10"
                }
              ]}
                title="Cession Premium Splits Option 1" />
            </HX.Pane>
            <HX.Pane flow="right">
              <HX.Table kb-interactive={true}
                shownBy="/cds/glsn_masking"
                data={[
                {
                  "datum": "glsn_auto_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_employers_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_general_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_foreign_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_aircraft_nonowned",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_aircraft_owned",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_garage_keepers_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_liquor_law_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_watercraft_non_owned",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_watercraft_owned",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_foreign_employers_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_foreign_general_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_foreign_auto_liability",
                  "labelAlign": "left"
                },
                null,
                {
                  "datum": "umbrella_eel",
                  "labelAlign": "left"
                },
                null,
                {
                  "datum": "umbrella_unsupported_net_premium",
                  "labelAlign": "left"
                },
                {
                  "datum": "umbrella_total_excess_net_premium",
                  "labelAlign": "left"
                },
                null,
                {
                  "datum": "umbrella_munich_cession_net",
                  "labelAlign": "left"
                },
                {
                  "datum": "umbrella_munich_cession_gross",
                  "labelAlign": "left"
                }
              ]}
                fields={[
                "premium_primary",
                {
                  "field": "premium_1_excess",
                  "shownBy": "/cds/add_excess_1"
                },
                {
                  "field": "premium_2_excess",
                  "shownBy": "/cds/add_excess_2"
                },
                {
                  "field": "premium_3_excess",
                  "shownBy": "/cds/add_excess_3"
                },
                {
                  "field": "premium_4_excess",
                  "shownBy": "/cds/add_excess_4"
                },
                {
                  "field": "premium_5_excess",
                  "shownBy": "/cds/add_excess_5"
                },
                {
                  "field": "premium_6_excess",
                  "shownBy": "/cds/add_excess_6"
                },
                {
                  "field": "premium_7_excess",
                  "shownBy": "/cds/add_excess_7"
                },
                {
                  "field": "premium_8_excess",
                  "shownBy": "/cds/add_excess_8"
                },
                {
                  "field": "premium_9_excess",
                  "shownBy": "/cds/add_excess_9"
                },
                {
                  "field": "premium_10_excess",
                  "shownBy": "/cds/add_excess_10"
                }
              ]}
                title="Option 1" />
              <HX.Table kb-interactive={true}
                shownBy="/cds/glsn_masking"
                data={[
                {
                  "datum": "glsn_auto_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_employers_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_general_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_foreign_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_aircraft_nonowned",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_aircraft_owned",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_garage_keepers_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_liquor_law_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_watercraft_non_owned",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_watercraft_owned",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_foreign_employers_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_foreign_general_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_foreign_auto_liability",
                  "labelAlign": "left"
                }
              ]}
                fields={[
                {
                  "field": "cession_premium_split_1_excess",
                  "shownBy": "/cds/add_excess_1"
                },
                {
                  "field": "cession_premium_split_2_excess",
                  "shownBy": "/cds/add_excess_2"
                },
                {
                  "field": "cession_premium_split_3_excess",
                  "shownBy": "/cds/add_excess_3"
                },
                {
                  "field": "cession_premium_split_4_excess",
                  "shownBy": "/cds/add_excess_4"
                },
                {
                  "field": "cession_premium_split_5_excess",
                  "shownBy": "/cds/add_excess_5"
                },
                {
                  "field": "cession_premium_split_6_excess",
                  "shownBy": "/cds/add_excess_6"
                },
                {
                  "field": "cession_premium_split_7_excess",
                  "shownBy": "/cds/add_excess_7"
                },
                {
                  "field": "cession_premium_split_8_excess",
                  "shownBy": "/cds/add_excess_8"
                },
                {
                  "field": "cession_premium_split_9_excess",
                  "shownBy": "/cds/add_excess_9"
                },
                {
                  "field": "cession_premium_split_10_excess",
                  "shownBy": "/cds/add_excess_10"
                }
              ]}
                title="Cession Premium Splits Option 1" />
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Umbrella Calculations Option 2"
          shownBy="cds/show_option_2">
          <HX.With context={{
            "index": 1,
            "path": "cds/options",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Table kb-interactive={true}
                shownBy="/cds/gmm_masking"
                data={[
                {
                  "datum": "gmm_auto_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_employers_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_general_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_foreign_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_aircraft_nonowned",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_aircraft_owned",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_auto_ambulance",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_educators_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_garage_keepers_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_helipad",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_liquor_law_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_managed_care_eo_health_plan",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_managed_care_eo_nonhealth_plan",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_watercraft_nonowned",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_watercraft_owned",
                  "labelAlign": "left"
                },
                null,
                {
                  "datum": "umbrella_eel",
                  "labelAlign": "left"
                },
                null,
                {
                  "datum": "umbrella_unsupported_net_premium",
                  "labelAlign": "left"
                },
                {
                  "datum": "umbrella_total_excess_net_premium",
                  "labelAlign": "left"
                },
                null,
                {
                  "datum": "umbrella_munich_cession_net",
                  "labelAlign": "left"
                },
                {
                  "datum": "umbrella_munich_cession_gross",
                  "labelAlign": "left"
                }
              ]}
                fields={[
                "premium_primary",
                {
                  "field": "premium_1_excess",
                  "shownBy": "/cds/add_excess_1"
                },
                {
                  "field": "premium_2_excess",
                  "shownBy": "/cds/add_excess_2"
                },
                {
                  "field": "premium_3_excess",
                  "shownBy": "/cds/add_excess_3"
                },
                {
                  "field": "premium_4_excess",
                  "shownBy": "/cds/add_excess_4"
                },
                {
                  "field": "premium_5_excess",
                  "shownBy": "/cds/add_excess_5"
                },
                {
                  "field": "premium_6_excess",
                  "shownBy": "/cds/add_excess_6"
                },
                {
                  "field": "premium_7_excess",
                  "shownBy": "/cds/add_excess_7"
                },
                {
                  "field": "premium_8_excess",
                  "shownBy": "/cds/add_excess_8"
                },
                {
                  "field": "premium_9_excess",
                  "shownBy": "/cds/add_excess_9"
                },
                {
                  "field": "premium_10_excess",
                  "shownBy": "/cds/add_excess_10"
                }
              ]}
                title="Option 2" />
              <HX.Table kb-interactive={true}
                shownBy="/cds/gmm_masking"
                data={[
                {
                  "datum": "gmm_auto_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_employers_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_general_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_foreign_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_aircraft_nonowned",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_aircraft_owned",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_auto_ambulance",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_educators_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_garage_keepers_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_helipad",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_liquor_law_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_managed_care_eo_health_plan",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_managed_care_eo_nonhealth_plan",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_watercraft_nonowned",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_watercraft_owned",
                  "labelAlign": "left"
                }
              ]}
                fields={[
                {
                  "field": "cession_premium_split_1_excess",
                  "shownBy": "/cds/add_excess_1"
                },
                {
                  "field": "cession_premium_split_2_excess",
                  "shownBy": "/cds/add_excess_2"
                },
                {
                  "field": "cession_premium_split_3_excess",
                  "shownBy": "/cds/add_excess_3"
                },
                {
                  "field": "cession_premium_split_4_excess",
                  "shownBy": "/cds/add_excess_4"
                },
                {
                  "field": "cession_premium_split_5_excess",
                  "shownBy": "/cds/add_excess_5"
                },
                {
                  "field": "cession_premium_split_6_excess",
                  "shownBy": "/cds/add_excess_6"
                },
                {
                  "field": "cession_premium_split_7_excess",
                  "shownBy": "/cds/add_excess_7"
                },
                {
                  "field": "cession_premium_split_8_excess",
                  "shownBy": "/cds/add_excess_8"
                },
                {
                  "field": "cession_premium_split_9_excess",
                  "shownBy": "/cds/add_excess_9"
                },
                {
                  "field": "cession_premium_split_10_excess",
                  "shownBy": "/cds/add_excess_10"
                }
              ]}
                title="Cession Premium Splits Option 2" />
            </HX.Pane>
            <HX.Pane flow="right">
              <HX.Table kb-interactive={true}
                shownBy="/cds/glsn_masking"
                data={[
                {
                  "datum": "glsn_auto_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_employers_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_general_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_foreign_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_aircraft_nonowned",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_aircraft_owned",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_garage_keepers_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_liquor_law_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_watercraft_non_owned",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_watercraft_owned",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_foreign_employers_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_foreign_general_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_foreign_auto_liability",
                  "labelAlign": "left"
                },
                null,
                {
                  "datum": "umbrella_eel",
                  "labelAlign": "left"
                },
                null,
                {
                  "datum": "umbrella_unsupported_net_premium",
                  "labelAlign": "left"
                },
                {
                  "datum": "umbrella_total_excess_net_premium",
                  "labelAlign": "left"
                },
                null,
                {
                  "datum": "umbrella_munich_cession_net",
                  "labelAlign": "left"
                },
                {
                  "datum": "umbrella_munich_cession_gross",
                  "labelAlign": "left"
                }
              ]}
                fields={[
                "premium_primary",
                {
                  "field": "premium_1_excess",
                  "shownBy": "/cds/add_excess_1"
                },
                {
                  "field": "premium_2_excess",
                  "shownBy": "/cds/add_excess_2"
                },
                {
                  "field": "premium_3_excess",
                  "shownBy": "/cds/add_excess_3"
                },
                {
                  "field": "premium_4_excess",
                  "shownBy": "/cds/add_excess_4"
                },
                {
                  "field": "premium_5_excess",
                  "shownBy": "/cds/add_excess_5"
                },
                {
                  "field": "premium_6_excess",
                  "shownBy": "/cds/add_excess_6"
                },
                {
                  "field": "premium_7_excess",
                  "shownBy": "/cds/add_excess_7"
                },
                {
                  "field": "premium_8_excess",
                  "shownBy": "/cds/add_excess_8"
                },
                {
                  "field": "premium_9_excess",
                  "shownBy": "/cds/add_excess_9"
                },
                {
                  "field": "premium_10_excess",
                  "shownBy": "/cds/add_excess_10"
                }
              ]}
                title="Option 2" />
              <HX.Table kb-interactive={true}
                shownBy="/cds/glsn_masking"
                data={[
                {
                  "datum": "glsn_auto_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_employers_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_general_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_foreign_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_aircraft_nonowned",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_aircraft_owned",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_garage_keepers_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_liquor_law_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_watercraft_non_owned",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_watercraft_owned",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_foreign_employers_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_foreign_general_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_foreign_auto_liability",
                  "labelAlign": "left"
                }
              ]}
                fields={[
                {
                  "field": "cession_premium_split_1_excess",
                  "shownBy": "/cds/add_excess_1"
                },
                {
                  "field": "cession_premium_split_2_excess",
                  "shownBy": "/cds/add_excess_2"
                },
                {
                  "field": "cession_premium_split_3_excess",
                  "shownBy": "/cds/add_excess_3"
                },
                {
                  "field": "cession_premium_split_4_excess",
                  "shownBy": "/cds/add_excess_4"
                },
                {
                  "field": "cession_premium_split_5_excess",
                  "shownBy": "/cds/add_excess_5"
                },
                {
                  "field": "cession_premium_split_6_excess",
                  "shownBy": "/cds/add_excess_6"
                },
                {
                  "field": "cession_premium_split_7_excess",
                  "shownBy": "/cds/add_excess_7"
                },
                {
                  "field": "cession_premium_split_8_excess",
                  "shownBy": "/cds/add_excess_8"
                },
                {
                  "field": "cession_premium_split_9_excess",
                  "shownBy": "/cds/add_excess_9"
                },
                {
                  "field": "cession_premium_split_10_excess",
                  "shownBy": "/cds/add_excess_10"
                }
              ]}
                title="Cession Premium Splits Option 2" />
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Umbrella Calculations Option 3"
          shownBy="cds/show_option_3">
          <HX.With context={{
            "index": 2,
            "path": "cds/options",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Table kb-interactive={true}
                shownBy="/cds/gmm_masking"
                data={[
                {
                  "datum": "gmm_auto_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_employers_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_general_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_foreign_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_aircraft_nonowned",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_aircraft_owned",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_auto_ambulance",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_educators_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_garage_keepers_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_helipad",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_liquor_law_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_managed_care_eo_health_plan",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_managed_care_eo_nonhealth_plan",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_watercraft_nonowned",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_watercraft_owned",
                  "labelAlign": "left"
                },
                null,
                {
                  "datum": "umbrella_eel",
                  "labelAlign": "left"
                },
                null,
                {
                  "datum": "umbrella_unsupported_net_premium",
                  "labelAlign": "left"
                },
                {
                  "datum": "umbrella_total_excess_net_premium",
                  "labelAlign": "left"
                },
                null,
                {
                  "datum": "umbrella_munich_cession_net",
                  "labelAlign": "left"
                },
                {
                  "datum": "umbrella_munich_cession_gross",
                  "labelAlign": "left"
                }
              ]}
                fields={[
                "premium_primary",
                {
                  "field": "premium_1_excess",
                  "shownBy": "/cds/add_excess_1"
                },
                {
                  "field": "premium_2_excess",
                  "shownBy": "/cds/add_excess_2"
                },
                {
                  "field": "premium_3_excess",
                  "shownBy": "/cds/add_excess_3"
                },
                {
                  "field": "premium_4_excess",
                  "shownBy": "/cds/add_excess_4"
                },
                {
                  "field": "premium_5_excess",
                  "shownBy": "/cds/add_excess_5"
                },
                {
                  "field": "premium_6_excess",
                  "shownBy": "/cds/add_excess_6"
                },
                {
                  "field": "premium_7_excess",
                  "shownBy": "/cds/add_excess_7"
                },
                {
                  "field": "premium_8_excess",
                  "shownBy": "/cds/add_excess_8"
                },
                {
                  "field": "premium_9_excess",
                  "shownBy": "/cds/add_excess_9"
                },
                {
                  "field": "premium_10_excess",
                  "shownBy": "/cds/add_excess_10"
                }
              ]}
                title="Option 3" />
              <HX.Table kb-interactive={true}
                shownBy="/cds/gmm_masking"
                data={[
                {
                  "datum": "gmm_auto_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_employers_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_general_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_foreign_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_aircraft_nonowned",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_aircraft_owned",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_auto_ambulance",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_educators_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_garage_keepers_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_helipad",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_liquor_law_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_managed_care_eo_health_plan",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_managed_care_eo_nonhealth_plan",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_watercraft_nonowned",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_watercraft_owned",
                  "labelAlign": "left"
                }
              ]}
                fields={[
                {
                  "field": "cession_premium_split_1_excess",
                  "shownBy": "/cds/add_excess_1"
                },
                {
                  "field": "cession_premium_split_2_excess",
                  "shownBy": "/cds/add_excess_2"
                },
                {
                  "field": "cession_premium_split_3_excess",
                  "shownBy": "/cds/add_excess_3"
                },
                {
                  "field": "cession_premium_split_4_excess",
                  "shownBy": "/cds/add_excess_4"
                },
                {
                  "field": "cession_premium_split_5_excess",
                  "shownBy": "/cds/add_excess_5"
                },
                {
                  "field": "cession_premium_split_6_excess",
                  "shownBy": "/cds/add_excess_6"
                },
                {
                  "field": "cession_premium_split_7_excess",
                  "shownBy": "/cds/add_excess_7"
                },
                {
                  "field": "cession_premium_split_8_excess",
                  "shownBy": "/cds/add_excess_8"
                },
                {
                  "field": "cession_premium_split_9_excess",
                  "shownBy": "/cds/add_excess_9"
                },
                {
                  "field": "cession_premium_split_10_excess",
                  "shownBy": "/cds/add_excess_10"
                }
              ]}
                title="Cession Premium Splits Option 3" />
            </HX.Pane>
            <HX.Pane flow="right">
              <HX.Table kb-interactive={true}
                shownBy="/cds/glsn_masking"
                data={[
                {
                  "datum": "glsn_auto_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_employers_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_general_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_foreign_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_aircraft_nonowned",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_aircraft_owned",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_garage_keepers_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_liquor_law_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_watercraft_non_owned",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_watercraft_owned",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_foreign_employers_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_foreign_general_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_foreign_auto_liability",
                  "labelAlign": "left"
                },
                null,
                {
                  "datum": "umbrella_eel",
                  "labelAlign": "left"
                },
                null,
                {
                  "datum": "umbrella_unsupported_net_premium",
                  "labelAlign": "left"
                },
                {
                  "datum": "umbrella_total_excess_net_premium",
                  "labelAlign": "left"
                },
                null,
                {
                  "datum": "umbrella_munich_cession_net",
                  "labelAlign": "left"
                },
                {
                  "datum": "umbrella_munich_cession_gross",
                  "labelAlign": "left"
                }
              ]}
                fields={[
                "premium_primary",
                {
                  "field": "premium_1_excess",
                  "shownBy": "/cds/add_excess_1"
                },
                {
                  "field": "premium_2_excess",
                  "shownBy": "/cds/add_excess_2"
                },
                {
                  "field": "premium_3_excess",
                  "shownBy": "/cds/add_excess_3"
                },
                {
                  "field": "premium_4_excess",
                  "shownBy": "/cds/add_excess_4"
                },
                {
                  "field": "premium_5_excess",
                  "shownBy": "/cds/add_excess_5"
                },
                {
                  "field": "premium_6_excess",
                  "shownBy": "/cds/add_excess_6"
                },
                {
                  "field": "premium_7_excess",
                  "shownBy": "/cds/add_excess_7"
                },
                {
                  "field": "premium_8_excess",
                  "shownBy": "/cds/add_excess_8"
                },
                {
                  "field": "premium_9_excess",
                  "shownBy": "/cds/add_excess_9"
                },
                {
                  "field": "premium_10_excess",
                  "shownBy": "/cds/add_excess_10"
                }
              ]}
                title="Option 3" />
              <HX.Table kb-interactive={true}
                shownBy="/cds/glsn_masking"
                data={[
                {
                  "datum": "glsn_auto_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_employers_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_general_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_foreign_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_aircraft_nonowned",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_aircraft_owned",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_garage_keepers_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_liquor_law_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_watercraft_non_owned",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_watercraft_owned",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_foreign_employers_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_foreign_general_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_foreign_auto_liability",
                  "labelAlign": "left"
                }
              ]}
                fields={[
                {
                  "field": "cession_premium_split_1_excess",
                  "shownBy": "/cds/add_excess_1"
                },
                {
                  "field": "cession_premium_split_2_excess",
                  "shownBy": "/cds/add_excess_2"
                },
                {
                  "field": "cession_premium_split_3_excess",
                  "shownBy": "/cds/add_excess_3"
                },
                {
                  "field": "cession_premium_split_4_excess",
                  "shownBy": "/cds/add_excess_4"
                },
                {
                  "field": "cession_premium_split_5_excess",
                  "shownBy": "/cds/add_excess_5"
                },
                {
                  "field": "cession_premium_split_6_excess",
                  "shownBy": "/cds/add_excess_6"
                },
                {
                  "field": "cession_premium_split_7_excess",
                  "shownBy": "/cds/add_excess_7"
                },
                {
                  "field": "cession_premium_split_8_excess",
                  "shownBy": "/cds/add_excess_8"
                },
                {
                  "field": "cession_premium_split_9_excess",
                  "shownBy": "/cds/add_excess_9"
                },
                {
                  "field": "cession_premium_split_10_excess",
                  "shownBy": "/cds/add_excess_10"
                }
              ]}
                title="Cession Premium Splits Option 3" />
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Umbrella Calculations Option 4"
          shownBy="cds/show_option_4">
          <HX.With context={{
            "index": 3,
            "path": "cds/options",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Table kb-interactive={true}
                shownBy="/cds/gmm_masking"
                data={[
                {
                  "datum": "gmm_auto_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_employers_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_general_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_foreign_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_aircraft_nonowned",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_aircraft_owned",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_auto_ambulance",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_educators_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_garage_keepers_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_helipad",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_liquor_law_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_managed_care_eo_health_plan",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_managed_care_eo_nonhealth_plan",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_watercraft_nonowned",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_watercraft_owned",
                  "labelAlign": "left"
                },
                null,
                {
                  "datum": "umbrella_eel",
                  "labelAlign": "left"
                },
                null,
                {
                  "datum": "umbrella_unsupported_net_premium",
                  "labelAlign": "left"
                },
                {
                  "datum": "umbrella_total_excess_net_premium",
                  "labelAlign": "left"
                },
                null,
                {
                  "datum": "umbrella_munich_cession_net",
                  "labelAlign": "left"
                },
                {
                  "datum": "umbrella_munich_cession_gross",
                  "labelAlign": "left"
                }
              ]}
                fields={[
                "premium_primary",
                {
                  "field": "premium_1_excess",
                  "shownBy": "/cds/add_excess_1"
                },
                {
                  "field": "premium_2_excess",
                  "shownBy": "/cds/add_excess_2"
                },
                {
                  "field": "premium_3_excess",
                  "shownBy": "/cds/add_excess_3"
                },
                {
                  "field": "premium_4_excess",
                  "shownBy": "/cds/add_excess_4"
                },
                {
                  "field": "premium_5_excess",
                  "shownBy": "/cds/add_excess_5"
                },
                {
                  "field": "premium_6_excess",
                  "shownBy": "/cds/add_excess_6"
                },
                {
                  "field": "premium_7_excess",
                  "shownBy": "/cds/add_excess_7"
                },
                {
                  "field": "premium_8_excess",
                  "shownBy": "/cds/add_excess_8"
                },
                {
                  "field": "premium_9_excess",
                  "shownBy": "/cds/add_excess_9"
                },
                {
                  "field": "premium_10_excess",
                  "shownBy": "/cds/add_excess_10"
                }
              ]}
                title="Option 4" />
              <HX.Table kb-interactive={true}
                shownBy="/cds/gmm_masking"
                data={[
                {
                  "datum": "gmm_auto_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_employers_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_general_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_foreign_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_aircraft_nonowned",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_aircraft_owned",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_auto_ambulance",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_educators_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_garage_keepers_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_helipad",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_liquor_law_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_managed_care_eo_health_plan",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_managed_care_eo_nonhealth_plan",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_watercraft_nonowned",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_watercraft_owned",
                  "labelAlign": "left"
                }
              ]}
                fields={[
                {
                  "field": "cession_premium_split_1_excess",
                  "shownBy": "/cds/add_excess_1"
                },
                {
                  "field": "cession_premium_split_2_excess",
                  "shownBy": "/cds/add_excess_2"
                },
                {
                  "field": "cession_premium_split_3_excess",
                  "shownBy": "/cds/add_excess_3"
                },
                {
                  "field": "cession_premium_split_4_excess",
                  "shownBy": "/cds/add_excess_4"
                },
                {
                  "field": "cession_premium_split_5_excess",
                  "shownBy": "/cds/add_excess_5"
                },
                {
                  "field": "cession_premium_split_6_excess",
                  "shownBy": "/cds/add_excess_6"
                },
                {
                  "field": "cession_premium_split_7_excess",
                  "shownBy": "/cds/add_excess_7"
                },
                {
                  "field": "cession_premium_split_8_excess",
                  "shownBy": "/cds/add_excess_8"
                },
                {
                  "field": "cession_premium_split_9_excess",
                  "shownBy": "/cds/add_excess_9"
                },
                {
                  "field": "cession_premium_split_10_excess",
                  "shownBy": "/cds/add_excess_10"
                }
              ]}
                title="Cession Premium Splits Option 4" />
            </HX.Pane>
            <HX.Pane flow="right">
              <HX.Table kb-interactive={true}
                shownBy="/cds/glsn_masking"
                data={[
                {
                  "datum": "glsn_auto_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_employers_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_general_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_foreign_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_aircraft_nonowned",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_aircraft_owned",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_garage_keepers_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_liquor_law_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_watercraft_non_owned",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_watercraft_owned",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_foreign_employers_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_foreign_general_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_foreign_auto_liability",
                  "labelAlign": "left"
                },
                null,
                {
                  "datum": "umbrella_eel",
                  "labelAlign": "left"
                },
                null,
                {
                  "datum": "umbrella_unsupported_net_premium",
                  "labelAlign": "left"
                },
                {
                  "datum": "umbrella_total_excess_net_premium",
                  "labelAlign": "left"
                },
                null,
                {
                  "datum": "umbrella_munich_cession_net",
                  "labelAlign": "left"
                },
                {
                  "datum": "umbrella_munich_cession_gross",
                  "labelAlign": "left"
                }
              ]}
                fields={[
                "premium_primary",
                {
                  "field": "premium_1_excess",
                  "shownBy": "/cds/add_excess_1"
                },
                {
                  "field": "premium_2_excess",
                  "shownBy": "/cds/add_excess_2"
                },
                {
                  "field": "premium_3_excess",
                  "shownBy": "/cds/add_excess_3"
                },
                {
                  "field": "premium_4_excess",
                  "shownBy": "/cds/add_excess_4"
                },
                {
                  "field": "premium_5_excess",
                  "shownBy": "/cds/add_excess_5"
                },
                {
                  "field": "premium_6_excess",
                  "shownBy": "/cds/add_excess_6"
                },
                {
                  "field": "premium_7_excess",
                  "shownBy": "/cds/add_excess_7"
                },
                {
                  "field": "premium_8_excess",
                  "shownBy": "/cds/add_excess_8"
                },
                {
                  "field": "premium_9_excess",
                  "shownBy": "/cds/add_excess_9"
                },
                {
                  "field": "premium_10_excess",
                  "shownBy": "/cds/add_excess_10"
                }
              ]}
                title="Option 4" />
              <HX.Table kb-interactive={true}
                shownBy="/cds/glsn_masking"
                data={[
                {
                  "datum": "glsn_auto_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_employers_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_general_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_foreign_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_aircraft_nonowned",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_aircraft_owned",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_garage_keepers_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_liquor_law_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_watercraft_non_owned",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_watercraft_owned",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_foreign_employers_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_foreign_general_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_foreign_auto_liability",
                  "labelAlign": "left"
                }
              ]}
                fields={[
                {
                  "field": "cession_premium_split_1_excess",
                  "shownBy": "/cds/add_excess_1"
                },
                {
                  "field": "cession_premium_split_2_excess",
                  "shownBy": "/cds/add_excess_2"
                },
                {
                  "field": "cession_premium_split_3_excess",
                  "shownBy": "/cds/add_excess_3"
                },
                {
                  "field": "cession_premium_split_4_excess",
                  "shownBy": "/cds/add_excess_4"
                },
                {
                  "field": "cession_premium_split_5_excess",
                  "shownBy": "/cds/add_excess_5"
                },
                {
                  "field": "cession_premium_split_6_excess",
                  "shownBy": "/cds/add_excess_6"
                },
                {
                  "field": "cession_premium_split_7_excess",
                  "shownBy": "/cds/add_excess_7"
                },
                {
                  "field": "cession_premium_split_8_excess",
                  "shownBy": "/cds/add_excess_8"
                },
                {
                  "field": "cession_premium_split_9_excess",
                  "shownBy": "/cds/add_excess_9"
                },
                {
                  "field": "cession_premium_split_10_excess",
                  "shownBy": "/cds/add_excess_10"
                }
              ]}
                title="Cession Premium Splits Option 4" />
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Umbrella Calculations Option 5"
          shownBy="cds/show_option_5">
          <HX.With context={{
            "index": 4,
            "path": "cds/options",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Table kb-interactive={true}
                shownBy="/cds/gmm_masking"
                data={[
                {
                  "datum": "gmm_auto_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_employers_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_general_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_foreign_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_aircraft_nonowned",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_aircraft_owned",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_auto_ambulance",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_educators_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_garage_keepers_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_helipad",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_liquor_law_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_managed_care_eo_health_plan",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_managed_care_eo_nonhealth_plan",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_watercraft_nonowned",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_watercraft_owned",
                  "labelAlign": "left"
                },
                null,
                {
                  "datum": "umbrella_eel",
                  "labelAlign": "left"
                },
                null,
                {
                  "datum": "umbrella_unsupported_net_premium",
                  "labelAlign": "left"
                },
                {
                  "datum": "umbrella_total_excess_net_premium",
                  "labelAlign": "left"
                },
                null,
                {
                  "datum": "umbrella_munich_cession_net",
                  "labelAlign": "left"
                },
                {
                  "datum": "umbrella_munich_cession_gross",
                  "labelAlign": "left"
                }
              ]}
                fields={[
                "premium_primary",
                {
                  "field": "premium_1_excess",
                  "shownBy": "/cds/add_excess_1"
                },
                {
                  "field": "premium_2_excess",
                  "shownBy": "/cds/add_excess_2"
                },
                {
                  "field": "premium_3_excess",
                  "shownBy": "/cds/add_excess_3"
                },
                {
                  "field": "premium_4_excess",
                  "shownBy": "/cds/add_excess_4"
                },
                {
                  "field": "premium_5_excess",
                  "shownBy": "/cds/add_excess_5"
                },
                {
                  "field": "premium_6_excess",
                  "shownBy": "/cds/add_excess_6"
                },
                {
                  "field": "premium_7_excess",
                  "shownBy": "/cds/add_excess_7"
                },
                {
                  "field": "premium_8_excess",
                  "shownBy": "/cds/add_excess_8"
                },
                {
                  "field": "premium_9_excess",
                  "shownBy": "/cds/add_excess_9"
                },
                {
                  "field": "premium_10_excess",
                  "shownBy": "/cds/add_excess_10"
                }
              ]}
                title="Option 5" />
              <HX.Table kb-interactive={true}
                shownBy="/cds/gmm_masking"
                data={[
                {
                  "datum": "gmm_auto_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_employers_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_general_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_foreign_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_aircraft_nonowned",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_aircraft_owned",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_auto_ambulance",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_educators_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_garage_keepers_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_helipad",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_liquor_law_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_managed_care_eo_health_plan",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_managed_care_eo_nonhealth_plan",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_watercraft_nonowned",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_watercraft_owned",
                  "labelAlign": "left"
                }
              ]}
                fields={[
                {
                  "field": "cession_premium_split_1_excess",
                  "shownBy": "/cds/add_excess_1"
                },
                {
                  "field": "cession_premium_split_2_excess",
                  "shownBy": "/cds/add_excess_2"
                },
                {
                  "field": "cession_premium_split_3_excess",
                  "shownBy": "/cds/add_excess_3"
                },
                {
                  "field": "cession_premium_split_4_excess",
                  "shownBy": "/cds/add_excess_4"
                },
                {
                  "field": "cession_premium_split_5_excess",
                  "shownBy": "/cds/add_excess_5"
                },
                {
                  "field": "cession_premium_split_6_excess",
                  "shownBy": "/cds/add_excess_6"
                },
                {
                  "field": "cession_premium_split_7_excess",
                  "shownBy": "/cds/add_excess_7"
                },
                {
                  "field": "cession_premium_split_8_excess",
                  "shownBy": "/cds/add_excess_8"
                },
                {
                  "field": "cession_premium_split_9_excess",
                  "shownBy": "/cds/add_excess_9"
                },
                {
                  "field": "cession_premium_split_10_excess",
                  "shownBy": "/cds/add_excess_10"
                }
              ]}
                title="Cession Premium Splits Option 5" />
            </HX.Pane>
            <HX.Pane flow="right">
              <HX.Table kb-interactive={true}
                shownBy="/cds/glsn_masking"
                data={[
                {
                  "datum": "glsn_auto_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_employers_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_general_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_foreign_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_aircraft_nonowned",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_aircraft_owned",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_garage_keepers_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_liquor_law_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_watercraft_non_owned",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_watercraft_owned",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_foreign_employers_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_foreign_general_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_foreign_auto_liability",
                  "labelAlign": "left"
                },
                null,
                {
                  "datum": "umbrella_eel",
                  "labelAlign": "left"
                },
                null,
                {
                  "datum": "umbrella_unsupported_net_premium",
                  "labelAlign": "left"
                },
                {
                  "datum": "umbrella_total_excess_net_premium",
                  "labelAlign": "left"
                },
                null,
                {
                  "datum": "umbrella_munich_cession_net",
                  "labelAlign": "left"
                },
                {
                  "datum": "umbrella_munich_cession_gross",
                  "labelAlign": "left"
                }
              ]}
                fields={[
                "premium_primary",
                {
                  "field": "premium_1_excess",
                  "shownBy": "/cds/add_excess_1"
                },
                {
                  "field": "premium_2_excess",
                  "shownBy": "/cds/add_excess_2"
                },
                {
                  "field": "premium_3_excess",
                  "shownBy": "/cds/add_excess_3"
                },
                {
                  "field": "premium_4_excess",
                  "shownBy": "/cds/add_excess_4"
                },
                {
                  "field": "premium_5_excess",
                  "shownBy": "/cds/add_excess_5"
                },
                {
                  "field": "premium_6_excess",
                  "shownBy": "/cds/add_excess_6"
                },
                {
                  "field": "premium_7_excess",
                  "shownBy": "/cds/add_excess_7"
                },
                {
                  "field": "premium_8_excess",
                  "shownBy": "/cds/add_excess_8"
                },
                {
                  "field": "premium_9_excess",
                  "shownBy": "/cds/add_excess_9"
                },
                {
                  "field": "premium_10_excess",
                  "shownBy": "/cds/add_excess_10"
                }
              ]}
                title="Option 5" />
              <HX.Table kb-interactive={true}
                shownBy="/cds/glsn_masking"
                data={[
                {
                  "datum": "glsn_auto_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_employers_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_general_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_foreign_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_aircraft_nonowned",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_aircraft_owned",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_garage_keepers_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_liquor_law_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_watercraft_non_owned",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_watercraft_owned",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_foreign_employers_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_foreign_general_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_foreign_auto_liability",
                  "labelAlign": "left"
                }
              ]}
                fields={[
                {
                  "field": "cession_premium_split_1_excess",
                  "shownBy": "/cds/add_excess_1"
                },
                {
                  "field": "cession_premium_split_2_excess",
                  "shownBy": "/cds/add_excess_2"
                },
                {
                  "field": "cession_premium_split_3_excess",
                  "shownBy": "/cds/add_excess_3"
                },
                {
                  "field": "cession_premium_split_4_excess",
                  "shownBy": "/cds/add_excess_4"
                },
                {
                  "field": "cession_premium_split_5_excess",
                  "shownBy": "/cds/add_excess_5"
                },
                {
                  "field": "cession_premium_split_6_excess",
                  "shownBy": "/cds/add_excess_6"
                },
                {
                  "field": "cession_premium_split_7_excess",
                  "shownBy": "/cds/add_excess_7"
                },
                {
                  "field": "cession_premium_split_8_excess",
                  "shownBy": "/cds/add_excess_8"
                },
                {
                  "field": "cession_premium_split_9_excess",
                  "shownBy": "/cds/add_excess_9"
                },
                {
                  "field": "cession_premium_split_10_excess",
                  "shownBy": "/cds/add_excess_10"
                }
              ]}
                title="Cession Premium Splits Option 5" />
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Umbrella Calculations Option 6"
          shownBy="cds/show_option_6">
          <HX.With context={{
            "index": 5,
            "path": "cds/options",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Table kb-interactive={true}
                shownBy="/cds/gmm_masking"
                data={[
                {
                  "datum": "gmm_auto_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_employers_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_general_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_foreign_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_aircraft_nonowned",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_aircraft_owned",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_auto_ambulance",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_educators_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_garage_keepers_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_helipad",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_liquor_law_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_managed_care_eo_health_plan",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_managed_care_eo_nonhealth_plan",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_watercraft_nonowned",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_watercraft_owned",
                  "labelAlign": "left"
                },
                null,
                {
                  "datum": "umbrella_eel",
                  "labelAlign": "left"
                },
                null,
                {
                  "datum": "umbrella_unsupported_net_premium",
                  "labelAlign": "left"
                },
                {
                  "datum": "umbrella_total_excess_net_premium",
                  "labelAlign": "left"
                },
                null,
                {
                  "datum": "umbrella_munich_cession_net",
                  "labelAlign": "left"
                },
                {
                  "datum": "umbrella_munich_cession_gross",
                  "labelAlign": "left"
                }
              ]}
                fields={[
                "premium_primary",
                {
                  "field": "premium_1_excess",
                  "shownBy": "/cds/add_excess_1"
                },
                {
                  "field": "premium_2_excess",
                  "shownBy": "/cds/add_excess_2"
                },
                {
                  "field": "premium_3_excess",
                  "shownBy": "/cds/add_excess_3"
                },
                {
                  "field": "premium_4_excess",
                  "shownBy": "/cds/add_excess_4"
                },
                {
                  "field": "premium_5_excess",
                  "shownBy": "/cds/add_excess_5"
                },
                {
                  "field": "premium_6_excess",
                  "shownBy": "/cds/add_excess_6"
                },
                {
                  "field": "premium_7_excess",
                  "shownBy": "/cds/add_excess_7"
                },
                {
                  "field": "premium_8_excess",
                  "shownBy": "/cds/add_excess_8"
                },
                {
                  "field": "premium_9_excess",
                  "shownBy": "/cds/add_excess_9"
                },
                {
                  "field": "premium_10_excess",
                  "shownBy": "/cds/add_excess_10"
                }
              ]}
                title="Option 6" />
              <HX.Table kb-interactive={true}
                shownBy="/cds/gmm_masking"
                data={[
                {
                  "datum": "gmm_auto_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_employers_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_general_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_foreign_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_aircraft_nonowned",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_aircraft_owned",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_auto_ambulance",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_educators_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_garage_keepers_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_helipad",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_liquor_law_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_managed_care_eo_health_plan",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_managed_care_eo_nonhealth_plan",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_watercraft_nonowned",
                  "labelAlign": "left"
                },
                {
                  "datum": "gmm_watercraft_owned",
                  "labelAlign": "left"
                }
              ]}
                fields={[
                {
                  "field": "cession_premium_split_1_excess",
                  "shownBy": "/cds/add_excess_1"
                },
                {
                  "field": "cession_premium_split_2_excess",
                  "shownBy": "/cds/add_excess_2"
                },
                {
                  "field": "cession_premium_split_3_excess",
                  "shownBy": "/cds/add_excess_3"
                },
                {
                  "field": "cession_premium_split_4_excess",
                  "shownBy": "/cds/add_excess_4"
                },
                {
                  "field": "cession_premium_split_5_excess",
                  "shownBy": "/cds/add_excess_5"
                },
                {
                  "field": "cession_premium_split_6_excess",
                  "shownBy": "/cds/add_excess_6"
                },
                {
                  "field": "cession_premium_split_7_excess",
                  "shownBy": "/cds/add_excess_7"
                },
                {
                  "field": "cession_premium_split_8_excess",
                  "shownBy": "/cds/add_excess_8"
                },
                {
                  "field": "cession_premium_split_9_excess",
                  "shownBy": "/cds/add_excess_9"
                },
                {
                  "field": "cession_premium_split_10_excess",
                  "shownBy": "/cds/add_excess_10"
                }
              ]}
                title="Cession Premium Splits Option 6" />
            </HX.Pane>
            <HX.Pane flow="right">
              <HX.Table kb-interactive={true}
                shownBy="/cds/glsn_masking"
                data={[
                {
                  "datum": "glsn_auto_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_employers_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_general_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_foreign_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_aircraft_nonowned",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_aircraft_owned",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_garage_keepers_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_liquor_law_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_watercraft_non_owned",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_watercraft_owned",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_foreign_employers_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_foreign_general_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_foreign_auto_liability",
                  "labelAlign": "left"
                },
                null,
                {
                  "datum": "umbrella_eel",
                  "labelAlign": "left"
                },
                null,
                {
                  "datum": "umbrella_unsupported_net_premium",
                  "labelAlign": "left"
                },
                {
                  "datum": "umbrella_total_excess_net_premium",
                  "labelAlign": "left"
                },
                null,
                {
                  "datum": "umbrella_munich_cession_net",
                  "labelAlign": "left"
                },
                {
                  "datum": "umbrella_munich_cession_gross",
                  "labelAlign": "left"
                }
              ]}
                fields={[
                "premium_primary",
                {
                  "field": "premium_1_excess",
                  "shownBy": "/cds/add_excess_1"
                },
                {
                  "field": "premium_2_excess",
                  "shownBy": "/cds/add_excess_2"
                },
                {
                  "field": "premium_3_excess",
                  "shownBy": "/cds/add_excess_3"
                },
                {
                  "field": "premium_4_excess",
                  "shownBy": "/cds/add_excess_4"
                },
                {
                  "field": "premium_5_excess",
                  "shownBy": "/cds/add_excess_5"
                },
                {
                  "field": "premium_6_excess",
                  "shownBy": "/cds/add_excess_6"
                },
                {
                  "field": "premium_7_excess",
                  "shownBy": "/cds/add_excess_7"
                },
                {
                  "field": "premium_8_excess",
                  "shownBy": "/cds/add_excess_8"
                },
                {
                  "field": "premium_9_excess",
                  "shownBy": "/cds/add_excess_9"
                },
                {
                  "field": "premium_10_excess",
                  "shownBy": "/cds/add_excess_10"
                }
              ]}
                title="Option 6" />
              <HX.Table kb-interactive={true}
                shownBy="/cds/glsn_masking"
                data={[
                {
                  "datum": "glsn_auto_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_employers_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_general_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_foreign_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_aircraft_nonowned",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_aircraft_owned",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_garage_keepers_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_liquor_law_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_watercraft_non_owned",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_watercraft_owned",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_foreign_employers_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_foreign_general_liability",
                  "labelAlign": "left"
                },
                {
                  "datum": "glsn_foreign_auto_liability",
                  "labelAlign": "left"
                }
              ]}
                fields={[
                {
                  "field": "cession_premium_split_1_excess",
                  "shownBy": "/cds/add_excess_1"
                },
                {
                  "field": "cession_premium_split_2_excess",
                  "shownBy": "/cds/add_excess_2"
                },
                {
                  "field": "cession_premium_split_3_excess",
                  "shownBy": "/cds/add_excess_3"
                },
                {
                  "field": "cession_premium_split_4_excess",
                  "shownBy": "/cds/add_excess_4"
                },
                {
                  "field": "cession_premium_split_5_excess",
                  "shownBy": "/cds/add_excess_5"
                },
                {
                  "field": "cession_premium_split_6_excess",
                  "shownBy": "/cds/add_excess_6"
                },
                {
                  "field": "cession_premium_split_7_excess",
                  "shownBy": "/cds/add_excess_7"
                },
                {
                  "field": "cession_premium_split_8_excess",
                  "shownBy": "/cds/add_excess_8"
                },
                {
                  "field": "cession_premium_split_9_excess",
                  "shownBy": "/cds/add_excess_9"
                },
                {
                  "field": "cession_premium_split_10_excess",
                  "shownBy": "/cds/add_excess_10"
                }
              ]}
                title="Cession Premium Splits Option 6" />
            </HX.Pane>
          </HX.With>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Rating Summary"
        fullWidth={true}
        viewScale={1}>
        <HX.Section title="Rating Methodology">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "cds/standard_fields/rating_methodology"
            ]} />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Collection fields={[
              {
                "field": "cds/override_terms_to_display",
                "shownBy": "cds/glsn_masking"
              }
            ]} />
            <HX.Collection fields={[
              {
                "field": "cds/cips",
                "shownBy": "cds/international_masking"
              }
            ]} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Layer Details">
          <HX.Table shownBy="cds/standard_fields/is_rater_priced"
            title="Priced Quotes (Beazley Share)"
            data={[
            {
              "datum": "cds/rating_factors/retention",
              "labelAlign": "left"
            },
            {
              "datum": "cds/layers",
              "elementLabelBy": "layer_label",
              "labelAlign": "left"
            }
          ]}
            fields={[
            "limit",
            "aggregate_limit",
            "brokerage",
            "model_premium",
            "quoted_premium",
            {
              "field": "quoted_rate",
              "shownBy": "cds/glsn_masking"
            },
            null,
            "bound_premium",
            {
              "field": "bound_rate",
              "shownBy": "cds/glsn_masking"
            },
            "section_reference",
            "status.input",
            null,
            "bpi",
            "tpi",
            "net_written_premium",
            "benchmark_premium",
            "technical_premium"
          ]}
            filter="show_row"
            freezeLeft={0}
            kb-interactive={true} />
          <HX.Table shownBy="cds/standard_fields/is_case_priced"
            title="Priced Quotes (Beazley Share)"
            data={[
            {
              "datum": "cds/rating_factors/retention",
              "labelAlign": "left"
            },
            {
              "datum": "cds/layers",
              "elementLabelBy": "layer_label",
              "labelAlign": "left"
            }
          ]}
            fields={[
            "limit_case_priced",
            "excess_case_priced",
            "brokerage_case_priced",
            null,
            "bound_premium",
            "section_reference",
            "status.input",
            null,
            "bpi_case_priced",
            "tpi",
            "net_written_premium",
            "benchmark_premium",
            "technical_premium"
          ]}
            filter="show_row"
            freezeLeft={0}
            kb-interactive={true} />
        </HX.Section>
        <HX.Section title="Case Pricing Analysis Filepath"
          shownBy="cds/standard_fields/is_case_priced">
          <HX.Notes field="cds/case_pricing_analysis_location" />
        </HX.Section>
        <HX.Section title="Schedule Modifiers"
          shownBy="cds/standard_fields/is_rater_priced">
          <HX.Table shownBy="/cds/gmm_masking"
            data={[
            {
              "datum": "loss_experience",
              "labelAlign": "left"
            },
            {
              "datum": "claims_handling_cooperation_experience",
              "labelAlign": "left"
            },
            {
              "datum": "risk_management_protocols_in_place",
              "labelAlign": "left"
            },
            {
              "datum": "use_of_standardized_written_contract",
              "labelAlign": "left"
            },
            {
              "datum": "accreditations",
              "labelAlign": "left"
            },
            {
              "datum": "hiring_credentialing_practices",
              "labelAlign": "left"
            },
            {
              "datum": "management_and_financial_condition",
              "labelAlign": "left"
            },
            {
              "datum": "shared_limit_with_physicians",
              "labelAlign": "left"
            },
            {
              "datum": "entity_only_vicarious_liability",
              "labelAlign": "left"
            },
            {
              "datum": "per_location_limit_increased_aggregate",
              "labelAlign": "left"
            },
            {
              "datum": "per_physician_limit_increased_aggregate",
              "labelAlign": "left"
            },
            {
              "datum": "sublimited_coverages_not_those_shown_on_pricing_tab",
              "labelAlign": "left"
            },
            {
              "datum": "transportation_exposure",
              "labelAlign": "left"
            },
            {
              "datum": "pediatric_senior_care_dd_exposure",
              "labelAlign": "left"
            },
            {
              "datum": "pcf_state_required_limits",
              "labelAlign": "left"
            },
            {
              "datum": "sexual_abuse_sublimit",
              "labelAlign": "left"
            },
            {
              "datum": "media_content_review_and_control_procedures_vc_only",
              "labelAlign": "left"
            },
            {
              "datum": "privacy_controls_and_procedures_vc_only",
              "labelAlign": "left"
            },
            {
              "datum": "total_schedule_rating",
              "labelAlign": "left"
            }
          ]}
            fields={[
            "min",
            "max",
            "value",
            "comment"
          ]}
            with="cds/modifiers/gmm"
            kb-interactive={true} />
          <HX.Table shownBy="/cds/glsn_masking"
            data={[
            {
              "datum": "loss_history",
              "labelAlign": "left"
            },
            {
              "datum": "contractual_agreements",
              "labelAlign": "left"
            },
            {
              "datum": "protocol_and_informed_consent",
              "labelAlign": "left"
            },
            {
              "datum": "fda_inspections",
              "labelAlign": "left"
            },
            {
              "datum": "product_type_litigation_history",
              "labelAlign": "left"
            },
            {
              "datum": "management_quality_and_financial_condition",
              "labelAlign": "left"
            },
            {
              "datum": "risk_management_protocols_in_place",
              "labelAlign": "left"
            },
            {
              "datum": "vulnerable_populations",
              "labelAlign": "left"
            },
            {
              "datum": "drug_of_last_resort",
              "labelAlign": "left"
            },
            {
              "datum": "foreign_sales",
              "labelAlign": "left"
            },
            {
              "datum": "exceptions_to_dangerous_ingredients",
              "labelAlign": "left"
            },
            {
              "datum": "imported_api_and_or_imported_finished_products",
              "labelAlign": "left"
            },
            {
              "datum": "gl_exposure_retail_locations_warehouses_wet_labs_etc",
              "labelAlign": "left"
            },
            {
              "datum": "sublimited_coverages_not_shown_on_pricing_page",
              "labelAlign": "left"
            },
            {
              "datum": "per_location_limit_increased_aggregate",
              "labelAlign": "left"
            },
            {
              "datum": "hiring_credentialing",
              "labelAlign": "left"
            },
            {
              "datum": "other",
              "labelAlign": "left"
            },
            {
              "datum": "total_schedule_rating",
              "labelAlign": "left"
            }
          ]}
            fields={[
            "min",
            "max",
            "value",
            "comment"
          ]}
            with="cds/modifiers/glsn"
            kb-interactive={true} />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Rate Change"
        fullWidth={true}
        shownBy="cds/is_real_renewal">
        <HX.Section title="Fetch Expiring Policy">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "cds/rate_change/expiring_policy_option_id",
              null
            ]}
              horizontal={true} />
          </HX.Pane>
          <HX.Pane>
            <HX.Table title=""
              data={[
              {
                "datum": "cds/layers",
                "elementLabelBy": "layer_label",
                "width": 200
              }
            ]}
              fields={[
              {
                "field": "status.read_only"
              }
            ]}
              transpose={true}
              filter="show_row"
              kb-interactive={true} />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Button task="expiring_policy_fetch_task"
              title="Fetch Expiring Data" />
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
        </HX.Section>
        <HX.Section title="Rate Change Instructions and Key"
          defaultCollapsed={true}>
          <HX.Pane flow="right">
            <HX.Notes field="cds/rate_change/instructions" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Primary Layer">
          <HX.With context={{
            "index": 1,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Collection fields={[
                "rate_change/expiring_layer_dropdown"
              ]} />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
            <HX.Pane flow="right">
              <HX.Notes field="rate_change/renewal_premium_warning"
                shownBy="rate_change/renewal_premium_warning_show" />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
          </HX.With>
          <HX.With context={{
            "index": 1,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Table shownBy="/cds/standard_fields/is_rater_priced"
                data={[
                "exposure_change",
                "risk_characteristics_change",
                "deductible_change",
                "limit_change",
                "terms_conditions_change",
                "brokerage_change",
                "other_change"
              ]}
                fields={[
                {
                  "field": "model_calculated",
                  "width": 150
                },
                {
                  "field": "uw_selected",
                  "width": 150
                },
                {
                  "field": "comments",
                  "width": 150
                }
              ]}
                with="rate_change"
                kb-interactive={true}
                syncColumnWidthsKey="mySyncedTables1" />
            </HX.Pane>
          </HX.With>
          <HX.With context={{
            "index": 1,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Table data={[
                "premium_annualized_100pct"
              ]}
                fields={[
                {
                  "field": "expiring",
                  "width": 220
                },
                {
                  "field": "implied",
                  "width": 220
                },
                {
                  "field": "renewal",
                  "width": 220
                }
              ]}
                with="rate_change"
                kb-interactive={true}
                syncColumnWidthsKey="mySyncedTables1" />
            </HX.Pane>
          </HX.With>
          <HX.With context={{
            "index": 1,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Collection title="Final Rate Change (Gross Brokerage)"
                fields={[
                "rate_change/risk_adjusted_rate_change/uw_selected"
              ]}
                shownBy="/cds/standard_fields/is_rater_priced" />
              <HX.Collection title="Final Rate Change (Gross Brokerage)"
                fields={[
                "rate_change/risk_adjusted_rate_change_case_priced/uw_selected"
              ]}
                shownBy="/cds/standard_fields/is_case_priced" />
              <HX.Collection title=" "
                fields={[
                "rate_change/risk_adjusted_rate_change_case_priced/comments"
              ]}
                shownBy="/cds/standard_fields/is_case_priced" />
              <HX.Pane shownBy="/cds/standard_fields/is_rater_priced" />
              <HX.Pane />
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Renewal Excess Layer 1"
          defaultCollapsed={true}
          shownBy="cds/add_excess_1">
          <HX.With context={{
            "index": 2,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Collection fields={[
                "rate_change/expiring_layer_dropdown"
              ]} />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
            <HX.Pane flow="right">
              <HX.Notes field="rate_change/renewal_premium_warning"
                shownBy="rate_change/renewal_premium_warning_show" />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
          </HX.With>
          <HX.With context={{
            "index": 2,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Table shownBy="/cds/standard_fields/is_rater_priced"
                data={[
                "exposure_change",
                "risk_characteristics_change",
                "deductible_change",
                "limit_change",
                "terms_conditions_change",
                "brokerage_change",
                "other_change"
              ]}
                fields={[
                {
                  "field": "model_calculated",
                  "width": 150
                },
                {
                  "field": "uw_selected",
                  "width": 150
                },
                {
                  "field": "comments",
                  "width": 150
                }
              ]}
                with="rate_change"
                syncColumnWidthsKey="mySyncedTables1"
                kb-interactive={true} />
            </HX.Pane>
          </HX.With>
          <HX.With context={{
            "index": 2,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Table data={[
                "premium_annualized_100pct"
              ]}
                fields={[
                {
                  "field": "expiring",
                  "width": 220
                },
                {
                  "field": "implied",
                  "width": 220
                },
                {
                  "field": "renewal",
                  "width": 220
                }
              ]}
                with="rate_change"
                syncColumnWidthsKey="mySyncedTables1" />
            </HX.Pane>
          </HX.With>
          <HX.With context={{
            "index": 2,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Collection title="Final Rate Change (Gross Brokerage)"
                fields={[
                "rate_change/risk_adjusted_rate_change/uw_selected"
              ]}
                shownBy="/cds/standard_fields/is_rater_priced" />
              <HX.Collection title="Final Rate Change (Gross Brokerage)"
                fields={[
                "rate_change/risk_adjusted_rate_change_case_priced/uw_selected"
              ]}
                shownBy="/cds/standard_fields/is_case_priced" />
              <HX.Collection title=" "
                fields={[
                "rate_change/risk_adjusted_rate_change_case_priced/comments"
              ]}
                shownBy="/cds/standard_fields/is_case_priced" />
              <HX.Pane shownBy="/cds/standard_fields/is_rater_priced" />
              <HX.Pane />
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Renewal Excess Layer 2"
          defaultCollapsed={true}
          shownBy="cds/add_excess_2">
          <HX.With context={{
            "index": 3,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Collection fields={[
                "rate_change/expiring_layer_dropdown"
              ]} />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
            <HX.Pane flow="right">
              <HX.Notes field="rate_change/renewal_premium_warning"
                shownBy="rate_change/renewal_premium_warning_show" />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
          </HX.With>
          <HX.With context={{
            "index": 3,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Table shownBy="/cds/standard_fields/is_rater_priced"
                data={[
                "exposure_change",
                "risk_characteristics_change",
                "deductible_change",
                "limit_change",
                "terms_conditions_change",
                "brokerage_change",
                "other_change"
              ]}
                fields={[
                {
                  "field": "model_calculated",
                  "width": 150
                },
                {
                  "field": "uw_selected",
                  "width": 150
                },
                {
                  "field": "comments",
                  "width": 150
                }
              ]}
                with="rate_change"
                syncColumnWidthsKey="mySyncedTables1"
                kb-interactive={true} />
            </HX.Pane>
          </HX.With>
          <HX.With context={{
            "index": 3,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Table data={[
                "premium_annualized_100pct"
              ]}
                fields={[
                {
                  "field": "expiring",
                  "width": 220
                },
                {
                  "field": "implied",
                  "width": 220
                },
                {
                  "field": "renewal",
                  "width": 220
                }
              ]}
                with="rate_change"
                syncColumnWidthsKey="mySyncedTables1" />
            </HX.Pane>
          </HX.With>
          <HX.With context={{
            "index": 3,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Collection title="Final Rate Change (Gross Brokerage)"
                fields={[
                "rate_change/risk_adjusted_rate_change/uw_selected"
              ]}
                shownBy="/cds/standard_fields/is_rater_priced" />
              <HX.Collection title="Final Rate Change (Gross Brokerage)"
                fields={[
                "rate_change/risk_adjusted_rate_change_case_priced/uw_selected"
              ]}
                shownBy="/cds/standard_fields/is_case_priced" />
              <HX.Collection title=" "
                fields={[
                "rate_change/risk_adjusted_rate_change_case_priced/comments"
              ]}
                shownBy="/cds/standard_fields/is_case_priced" />
              <HX.Pane shownBy="/cds/standard_fields/is_rater_priced" />
              <HX.Pane />
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Renewal Excess Layer 3"
          defaultCollapsed={true}
          shownBy="cds/add_excess_3">
          <HX.With context={{
            "index": 4,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Collection fields={[
                "rate_change/expiring_layer_dropdown"
              ]} />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
            <HX.Pane flow="right">
              <HX.Notes field="rate_change/renewal_premium_warning"
                shownBy="rate_change/renewal_premium_warning_show" />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
          </HX.With>
          <HX.With context={{
            "index": 4,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Table shownBy="/cds/standard_fields/is_rater_priced"
                data={[
                "exposure_change",
                "risk_characteristics_change",
                "deductible_change",
                "limit_change",
                "terms_conditions_change",
                "brokerage_change",
                "other_change"
              ]}
                fields={[
                {
                  "field": "model_calculated",
                  "width": 150
                },
                {
                  "field": "uw_selected",
                  "width": 150
                },
                {
                  "field": "comments",
                  "width": 150
                }
              ]}
                with="rate_change"
                syncColumnWidthsKey="mySyncedTables1"
                kb-interactive={true} />
            </HX.Pane>
          </HX.With>
          <HX.With context={{
            "index": 4,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Table data={[
                "premium_annualized_100pct"
              ]}
                fields={[
                {
                  "field": "expiring",
                  "width": 220
                },
                {
                  "field": "implied",
                  "width": 220
                },
                {
                  "field": "renewal",
                  "width": 220
                }
              ]}
                with="rate_change"
                syncColumnWidthsKey="mySyncedTables1" />
            </HX.Pane>
          </HX.With>
          <HX.With context={{
            "index": 4,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Collection title="Final Rate Change (Gross Brokerage)"
                fields={[
                "rate_change/risk_adjusted_rate_change/uw_selected"
              ]}
                shownBy="/cds/standard_fields/is_rater_priced" />
              <HX.Collection title="Final Rate Change (Gross Brokerage)"
                fields={[
                "rate_change/risk_adjusted_rate_change_case_priced/uw_selected"
              ]}
                shownBy="/cds/standard_fields/is_case_priced" />
              <HX.Collection title=" "
                fields={[
                "rate_change/risk_adjusted_rate_change_case_priced/comments"
              ]}
                shownBy="/cds/standard_fields/is_case_priced" />
              <HX.Pane shownBy="/cds/standard_fields/is_rater_priced" />
              <HX.Pane />
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Renewal Excess Layer 4"
          defaultCollapsed={true}
          shownBy="cds/add_excess_4">
          <HX.With context={{
            "index": 5,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Collection fields={[
                "rate_change/expiring_layer_dropdown"
              ]} />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
            <HX.Pane flow="right">
              <HX.Notes field="rate_change/renewal_premium_warning"
                shownBy="rate_change/renewal_premium_warning_show" />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
          </HX.With>
          <HX.With context={{
            "index": 5,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Table shownBy="/cds/standard_fields/is_rater_priced"
                data={[
                "exposure_change",
                "risk_characteristics_change",
                "deductible_change",
                "limit_change",
                "terms_conditions_change",
                "brokerage_change",
                "other_change"
              ]}
                fields={[
                {
                  "field": "model_calculated",
                  "width": 150
                },
                {
                  "field": "uw_selected",
                  "width": 150
                },
                {
                  "field": "comments",
                  "width": 150
                }
              ]}
                with="rate_change"
                syncColumnWidthsKey="mySyncedTables1"
                kb-interactive={true} />
            </HX.Pane>
          </HX.With>
          <HX.With context={{
            "index": 5,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Table data={[
                "premium_annualized_100pct"
              ]}
                fields={[
                {
                  "field": "expiring",
                  "width": 220
                },
                {
                  "field": "implied",
                  "width": 220
                },
                {
                  "field": "renewal",
                  "width": 220
                }
              ]}
                with="rate_change"
                syncColumnWidthsKey="mySyncedTables1" />
            </HX.Pane>
          </HX.With>
          <HX.With context={{
            "index": 5,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Collection title="Final Rate Change (Gross Brokerage)"
                fields={[
                "rate_change/risk_adjusted_rate_change/uw_selected"
              ]}
                shownBy="/cds/standard_fields/is_rater_priced" />
              <HX.Collection title="Final Rate Change (Gross Brokerage)"
                fields={[
                "rate_change/risk_adjusted_rate_change_case_priced/uw_selected"
              ]}
                shownBy="/cds/standard_fields/is_case_priced" />
              <HX.Collection title=" "
                fields={[
                "rate_change/risk_adjusted_rate_change_case_priced/comments"
              ]}
                shownBy="/cds/standard_fields/is_case_priced" />
              <HX.Pane shownBy="/cds/standard_fields/is_rater_priced" />
              <HX.Pane />
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Renewal Excess Layer 5"
          defaultCollapsed={true}
          shownBy="cds/add_excess_5">
          <HX.With context={{
            "index": 6,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Collection fields={[
                "rate_change/expiring_layer_dropdown"
              ]} />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
            <HX.Pane flow="right">
              <HX.Notes field="rate_change/renewal_premium_warning"
                shownBy="rate_change/renewal_premium_warning_show" />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
          </HX.With>
          <HX.With context={{
            "index": 6,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Table shownBy="/cds/standard_fields/is_rater_priced"
                data={[
                "exposure_change",
                "risk_characteristics_change",
                "deductible_change",
                "limit_change",
                "terms_conditions_change",
                "brokerage_change",
                "other_change"
              ]}
                fields={[
                {
                  "field": "model_calculated",
                  "width": 150
                },
                {
                  "field": "uw_selected",
                  "width": 150
                },
                {
                  "field": "comments",
                  "width": 150
                }
              ]}
                with="rate_change"
                syncColumnWidthsKey="mySyncedTables1"
                kb-interactive={true} />
            </HX.Pane>
          </HX.With>
          <HX.With context={{
            "index": 6,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Table data={[
                "premium_annualized_100pct"
              ]}
                fields={[
                {
                  "field": "expiring",
                  "width": 220
                },
                {
                  "field": "implied",
                  "width": 220
                },
                {
                  "field": "renewal",
                  "width": 220
                }
              ]}
                with="rate_change"
                syncColumnWidthsKey="mySyncedTables1" />
            </HX.Pane>
          </HX.With>
          <HX.With context={{
            "index": 6,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Collection title="Final Rate Change (Gross Brokerage)"
                fields={[
                "rate_change/risk_adjusted_rate_change/uw_selected"
              ]}
                shownBy="/cds/standard_fields/is_rater_priced" />
              <HX.Collection title="Final Rate Change (Gross Brokerage)"
                fields={[
                "rate_change/risk_adjusted_rate_change_case_priced/uw_selected"
              ]}
                shownBy="/cds/standard_fields/is_case_priced" />
              <HX.Collection title=" "
                fields={[
                "rate_change/risk_adjusted_rate_change_case_priced/comments"
              ]}
                shownBy="/cds/standard_fields/is_case_priced" />
              <HX.Pane shownBy="/cds/standard_fields/is_rater_priced" />
              <HX.Pane />
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Renewal Excess Layer 6"
          defaultCollapsed={true}
          shownBy="cds/add_excess_6">
          <HX.With context={{
            "index": 7,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Collection fields={[
                "rate_change/expiring_layer_dropdown"
              ]} />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
            <HX.Pane flow="right">
              <HX.Notes field="rate_change/renewal_premium_warning"
                shownBy="rate_change/renewal_premium_warning_show" />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
          </HX.With>
          <HX.With context={{
            "index": 7,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Table shownBy="/cds/standard_fields/is_rater_priced"
                data={[
                "exposure_change",
                "risk_characteristics_change",
                "deductible_change",
                "limit_change",
                "terms_conditions_change",
                "brokerage_change",
                "other_change"
              ]}
                fields={[
                {
                  "field": "model_calculated",
                  "width": 150
                },
                {
                  "field": "uw_selected",
                  "width": 150
                },
                {
                  "field": "comments",
                  "width": 150
                }
              ]}
                with="rate_change"
                syncColumnWidthsKey="mySyncedTables1"
                kb-interactive={true} />
            </HX.Pane>
          </HX.With>
          <HX.With context={{
            "index": 7,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Table data={[
                "premium_annualized_100pct"
              ]}
                fields={[
                {
                  "field": "expiring",
                  "width": 220
                },
                {
                  "field": "implied",
                  "width": 220
                },
                {
                  "field": "renewal",
                  "width": 220
                }
              ]}
                with="rate_change"
                syncColumnWidthsKey="mySyncedTables1" />
            </HX.Pane>
          </HX.With>
          <HX.With context={{
            "index": 7,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Collection title="Final Rate Change (Gross Brokerage)"
                fields={[
                "rate_change/risk_adjusted_rate_change/uw_selected"
              ]}
                shownBy="/cds/standard_fields/is_rater_priced" />
              <HX.Collection title="Final Rate Change (Gross Brokerage)"
                fields={[
                "rate_change/risk_adjusted_rate_change_case_priced/uw_selected"
              ]}
                shownBy="/cds/standard_fields/is_case_priced" />
              <HX.Collection title=" "
                fields={[
                "rate_change/risk_adjusted_rate_change_case_priced/comments"
              ]}
                shownBy="/cds/standard_fields/is_case_priced" />
              <HX.Pane shownBy="/cds/standard_fields/is_rater_priced" />
              <HX.Pane />
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Renewal Excess Layer 7"
          defaultCollapsed={true}
          shownBy="cds/add_excess_7">
          <HX.With context={{
            "index": 8,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Collection fields={[
                "rate_change/expiring_layer_dropdown"
              ]} />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
            <HX.Pane flow="right">
              <HX.Notes field="rate_change/renewal_premium_warning"
                shownBy="rate_change/renewal_premium_warning_show" />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
          </HX.With>
          <HX.With context={{
            "index": 8,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Table shownBy="/cds/standard_fields/is_rater_priced"
                data={[
                "exposure_change",
                "risk_characteristics_change",
                "deductible_change",
                "limit_change",
                "terms_conditions_change",
                "brokerage_change",
                "other_change"
              ]}
                fields={[
                {
                  "field": "model_calculated",
                  "width": 150
                },
                {
                  "field": "uw_selected",
                  "width": 150
                },
                {
                  "field": "comments",
                  "width": 150
                }
              ]}
                with="rate_change"
                syncColumnWidthsKey="mySyncedTables1"
                kb-interactive={true} />
            </HX.Pane>
          </HX.With>
          <HX.With context={{
            "index": 8,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Table data={[
                "premium_annualized_100pct"
              ]}
                fields={[
                {
                  "field": "expiring",
                  "width": 220
                },
                {
                  "field": "implied",
                  "width": 220
                },
                {
                  "field": "renewal",
                  "width": 220
                }
              ]}
                with="rate_change"
                syncColumnWidthsKey="mySyncedTables1" />
            </HX.Pane>
          </HX.With>
          <HX.With context={{
            "index": 8,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Collection title="Final Rate Change (Gross Brokerage)"
                fields={[
                "rate_change/risk_adjusted_rate_change/uw_selected"
              ]}
                shownBy="/cds/standard_fields/is_rater_priced" />
              <HX.Collection title="Final Rate Change (Gross Brokerage)"
                fields={[
                "rate_change/risk_adjusted_rate_change_case_priced/uw_selected"
              ]}
                shownBy="/cds/standard_fields/is_case_priced" />
              <HX.Collection title=" "
                fields={[
                "rate_change/risk_adjusted_rate_change_case_priced/comments"
              ]}
                shownBy="/cds/standard_fields/is_case_priced" />
              <HX.Pane shownBy="/cds/standard_fields/is_rater_priced" />
              <HX.Pane />
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Renewal Excess Layer 8"
          defaultCollapsed={true}
          shownBy="cds/add_excess_8">
          <HX.With context={{
            "index": 9,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Collection fields={[
                "rate_change/expiring_layer_dropdown"
              ]} />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
            <HX.Pane flow="right">
              <HX.Notes field="rate_change/renewal_premium_warning"
                shownBy="rate_change/renewal_premium_warning_show" />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
          </HX.With>
          <HX.With context={{
            "index": 9,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Table shownBy="/cds/standard_fields/is_rater_priced"
                data={[
                "exposure_change",
                "risk_characteristics_change",
                "deductible_change",
                "limit_change",
                "terms_conditions_change",
                "brokerage_change",
                "other_change"
              ]}
                fields={[
                {
                  "field": "model_calculated",
                  "width": 150
                },
                {
                  "field": "uw_selected",
                  "width": 150
                },
                {
                  "field": "comments",
                  "width": 150
                }
              ]}
                with="rate_change"
                syncColumnWidthsKey="mySyncedTables1"
                kb-interactive={true} />
            </HX.Pane>
          </HX.With>
          <HX.With context={{
            "index": 9,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Table data={[
                "premium_annualized_100pct"
              ]}
                fields={[
                {
                  "field": "expiring",
                  "width": 220
                },
                {
                  "field": "implied",
                  "width": 220
                },
                {
                  "field": "renewal",
                  "width": 220
                }
              ]}
                with="rate_change"
                syncColumnWidthsKey="mySyncedTables1" />
            </HX.Pane>
          </HX.With>
          <HX.With context={{
            "index": 9,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Collection title="Final Rate Change (Gross Brokerage)"
                fields={[
                "rate_change/risk_adjusted_rate_change/uw_selected"
              ]}
                shownBy="/cds/standard_fields/is_rater_priced" />
              <HX.Collection title="Final Rate Change (Gross Brokerage)"
                fields={[
                "rate_change/risk_adjusted_rate_change_case_priced/uw_selected"
              ]}
                shownBy="/cds/standard_fields/is_case_priced" />
              <HX.Collection title=" "
                fields={[
                "rate_change/risk_adjusted_rate_change_case_priced/comments"
              ]}
                shownBy="/cds/standard_fields/is_case_priced" />
              <HX.Pane shownBy="/cds/standard_fields/is_rater_priced" />
              <HX.Pane />
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Renewal Excess Layer 9"
          defaultCollapsed={true}
          shownBy="cds/add_excess_9">
          <HX.With context={{
            "index": 10,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Collection fields={[
                "rate_change/expiring_layer_dropdown"
              ]} />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
            <HX.Pane flow="right">
              <HX.Notes field="rate_change/renewal_premium_warning"
                shownBy="rate_change/renewal_premium_warning_show" />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
          </HX.With>
          <HX.With context={{
            "index": 10,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Table shownBy="/cds/standard_fields/is_rater_priced"
                data={[
                "exposure_change",
                "risk_characteristics_change",
                "deductible_change",
                "limit_change",
                "terms_conditions_change",
                "brokerage_change",
                "other_change"
              ]}
                fields={[
                {
                  "field": "model_calculated",
                  "width": 150
                },
                {
                  "field": "uw_selected",
                  "width": 150
                },
                {
                  "field": "comments",
                  "width": 150
                }
              ]}
                with="rate_change"
                syncColumnWidthsKey="mySyncedTables1"
                kb-interactive={true} />
            </HX.Pane>
          </HX.With>
          <HX.With context={{
            "index": 10,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Table data={[
                "premium_annualized_100pct"
              ]}
                fields={[
                {
                  "field": "expiring",
                  "width": 220
                },
                {
                  "field": "implied",
                  "width": 220
                },
                {
                  "field": "renewal",
                  "width": 220
                }
              ]}
                with="rate_change"
                syncColumnWidthsKey="mySyncedTables1" />
            </HX.Pane>
          </HX.With>
          <HX.With context={{
            "index": 10,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Collection title="Final Rate Change (Gross Brokerage)"
                fields={[
                "rate_change/risk_adjusted_rate_change/uw_selected"
              ]}
                shownBy="/cds/standard_fields/is_rater_priced" />
              <HX.Collection title="Final Rate Change (Gross Brokerage)"
                fields={[
                "rate_change/risk_adjusted_rate_change_case_priced/uw_selected"
              ]}
                shownBy="/cds/standard_fields/is_case_priced" />
              <HX.Collection title=" "
                fields={[
                "rate_change/risk_adjusted_rate_change_case_priced/comments"
              ]}
                shownBy="/cds/standard_fields/is_case_priced" />
              <HX.Pane shownBy="/cds/standard_fields/is_rater_priced" />
              <HX.Pane />
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Renewal Excess Layer 10"
          defaultCollapsed={true}
          shownBy="cds/add_excess_10">
          <HX.With context={{
            "index": 11,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Collection fields={[
                "rate_change/expiring_layer_dropdown"
              ]} />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
            <HX.Pane flow="right">
              <HX.Notes field="rate_change/renewal_premium_warning"
                shownBy="rate_change/renewal_premium_warning_show" />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
          </HX.With>
          <HX.With context={{
            "index": 11,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Table shownBy="/cds/standard_fields/is_rater_priced"
                data={[
                "exposure_change",
                "risk_characteristics_change",
                "deductible_change",
                "limit_change",
                "terms_conditions_change",
                "brokerage_change",
                "other_change"
              ]}
                fields={[
                {
                  "field": "model_calculated",
                  "width": 150
                },
                {
                  "field": "uw_selected",
                  "width": 150
                },
                {
                  "field": "comments",
                  "width": 150
                }
              ]}
                with="rate_change"
                syncColumnWidthsKey="mySyncedTables1"
                kb-interactive={true} />
            </HX.Pane>
          </HX.With>
          <HX.With context={{
            "index": 11,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane>
              <HX.Table data={[
                "premium_annualized_100pct"
              ]}
                fields={[
                {
                  "field": "expiring",
                  "width": 220
                },
                {
                  "field": "implied",
                  "width": 220
                },
                {
                  "field": "renewal",
                  "width": 220
                }
              ]}
                with="rate_change"
                syncColumnWidthsKey="mySyncedTables1" />
            </HX.Pane>
          </HX.With>
          <HX.With context={{
            "index": 11,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Collection title="Final Rate Change (Gross Brokerage)"
                fields={[
                "rate_change/risk_adjusted_rate_change/uw_selected"
              ]}
                shownBy="/cds/standard_fields/is_rater_priced" />
              <HX.Collection title="Final Rate Change (Gross Brokerage)"
                fields={[
                "rate_change/risk_adjusted_rate_change_case_priced/uw_selected"
              ]}
                shownBy="/cds/standard_fields/is_case_priced" />
              <HX.Collection title=" "
                fields={[
                "rate_change/risk_adjusted_rate_change_case_priced/comments"
              ]}
                shownBy="/cds/standard_fields/is_case_priced" />
              <HX.Pane shownBy="/cds/standard_fields/is_rater_priced" />
              <HX.Pane />
            </HX.Pane>
          </HX.With>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Rationale"
        fullWidth={false}
        viewScale={1}>
        <HX.Section title="Underwriter Notes">
          <CustomComponent textNode="cds/uw_notes"
            label="Current Year Notes" />
        </HX.Section>
        <HX.Section title="Mid Term Adjustments">
          <CustomComponent textNode="cds/mid_term_adjustments"
            label="Mid Term Adjustments" />
        </HX.Section>
        <HX.Section title="Historical Comments">
          <CustomComponent textNode="cds/historical_comments"
            label="Historical Comments" />
        </HX.Section>
        <HX.Section title="Additional Information - File Uploads">
          <HX.Pane flow="right">
            <HX.Pane>
              <HX.File field="cds/file_upload_1" />
            </HX.Pane>
            <HX.Pane>
              <HX.File field="cds/file_upload_2" />
            </HX.Pane>
            <HX.Pane>
              <HX.File field="cds/file_upload_3" />
            </HX.Pane>
            <HX.Pane>
              <HX.File field="cds/file_upload_4" />
            </HX.Pane>
            <HX.Pane>
              <HX.File field="cds/file_upload_5" />
            </HX.Pane>
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Generate Email Rationale">
          <HX.Pane flow="right">
            <HX.Button task="generate_email_task"
              title="Generate Rationale Email" />
            <HX.File field="cds/email/rationale_file" />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Button task="generate_referral_email_task"
              title="Generate Referral Email" />
            <HX.File field="cds/email/referral_file" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Generate Email Proposal">
          <HX.Pane flow="right">
            <HX.Button task="generate_primary_proposal_template_task"
              title="Generate Primary Proposal Template" />
            <HX.File field="cds/primary_proposal_template_file" />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Button task="generate_excess_proposal_template_task"
              title="Generate Excess Proposal Template" />
            <HX.File field="cds/excess_proposal_template_file" />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Something is Broken">
        <HX.With context={{
          "path": "bug_report",
          "type": "struct"
        }}>
          <HX.Section title="Log a New Incident">
            <HX.Notes field="helper_text" />
            <HX.Pane>
              <HX.Button task="new_bug_report_task"
                title="Log a New Incident" />
            </HX.Pane>
          </HX.Section>
          <HX.Section title="Incident Details"
            shownBy="commenced_flag">
            <HX.Pane>
              <HX.Collection fields={[
                "summary"
              ]}
                title="Summary" />
              <HX.Notes field="email_body"
                title="Details" />
              <HX.Pane flow="right"
                ratio={2}>
                <HX.Pane shownBy="inputs_outputs_file_show">
                  <HX.File field="inputs_outputs_file"
                    title="Inputs/Outputs Attachment" />
                  <HX.Button task="generate_bug_report_task"
                    title="Generate Inputs/Outputs" />
                </HX.Pane>
                <HX.With context={{
                  "path": "screenshot_files",
                  "type": "struct"
                }}>
                  <HX.Notes field="/bug_report/file_helper_text.read_only"
                    shownBy="f1/show_text" />
                  <HX.File field="f1/file"
                    title="Screenshot Attachment"
                    shownBy="f1/show_file" />
                  <HX.Notes field="/bug_report/file_helper_text.read_only"
                    shownBy="f2/show_text" />
                  <HX.File field="f2/file"
                    title="Screenshot Attachment 2"
                    shownBy="f2/show_file" />
                  <HX.Notes field="/bug_report/file_helper_text.read_only"
                    shownBy="f3/show_text" />
                  <HX.File field="f3/file"
                    title="Screenshot Attachment 3"
                    shownBy="f3/show_file" />
                  <HX.Notes field="/bug_report/file_helper_text.read_only"
                    shownBy="f4/show_text" />
                  <HX.File field="f4/file"
                    title="Screenshot Attachment 4"
                    shownBy="f4/show_file" />
                  <HX.Notes field="/bug_report/file_helper_text.read_only"
                    shownBy="f5/show_text" />
                  <HX.File field="f5/file"
                    title="Screenshot Attachment 5"
                    shownBy="f5/show_file" />
                </HX.With>
              </HX.Pane>
              <HX.Button task="add_additional_file_task"
                title="Upload Additional Screenshots" />
            </HX.Pane>
            <HX.Pane flow="right">
              <HX.Button task="send_bug_report_task"
                title="Send Incident" />
              <HX.Button task="cancel_bug_report_task"
                title="Cancel Incident" />
            </HX.Pane>
          </HX.Section>
        </HX.With>
      </HX.Page>
    </HX.Root>
  );
}

export default {
  hx_calculation_legacy_initial_premium: hx_calculation_legacy_initial_premium_view,
};