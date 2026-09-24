
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
        <HX.Section title="Start Treaty">
          <HX.Pane flow="right">
            <HX.Pane ratio={2}>
              <HX.Notes field="model_state/landing_page_info" />
            </HX.Pane>
            <HX.Pane>
              <HX.Button task="start_renewal_task"
                title="Start Treaty" />
            </HX.Pane>
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Risk Information"
        viewScale={0.7}
        shownBy="model_state/show_after_landing_page">
        <HX.Section title="Rating Methodology">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "cds/standard_fields/rating_methodology",
              {
                "field": "cds/case_pricing_analysis_location",
                "shownBy": "/cds/show_case_priced"
              }
            ]} />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Mandatory Details">
          <HX.Pane>
            <HX.Collection numCols={3}
              fields={[
              "cds/standard_fields/insured_name",
              "cds/standard_fields/underwriter",
              "cds/standard_fields/broker",
              "cds/deadline_date",
              "hx_core/inception_date",
              "hx_core/expiry_date",
              "cds/standard_fields/is_renewal",
              "cds/short_description",
              null,
              {
                "field": "cds/underwriter_location",
                "shownBy": "cds/show_bermuda"
              },
              {
                "field": "cds/discussed_london",
                "shownBy": "cds/show_bermuda"
              },
              {
                "field": "cds/technical_underwriter",
                "shownBy": "cds/show_bermuda"
              }
            ]} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Status">
          <HX.Pane>
            <HX.Collection numCols={3}
              fields={[
              "cds/deal_status",
              "cds/quotation",
              "cds/quoted"
            ]} />
            <HX.Collection numCols={3}
              fields={[
              {
                "field": "cds/declinature_reason",
                "shownBy": "/cds/show_declined_reasons"
              },
              {
                "field": "cds/declinature_comments",
                "shownBy": "/cds/show_declined_reasons"
              },
              null
            ]} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Rating Details">
          <HX.Pane>
            <HX.Collection numCols={3}
              fields={[
              "cds/programme",
              "cds/calc_type",
              "cds/currency",
              "cds/multi_year",
              "cds/brokerage",
              "cds/tax",
              "cds/treaty_basis",
              {
                "field": "cds/second_loss_brokerage",
                "shownBy": "cds/show_bermuda"
              },
              {
                "field": "cds/ceding_commission",
                "shownBy": "cds/show_ceding_commission"
              },
              {
                "field": "cds/other_acq_costs",
                "shownBy": "cds/show_ceding_commission"
              },
              {
                "field": "cds/includes_us_exposure",
                "shownBy": "cds/show_intl_fields"
              }
            ]} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Additional Risk Details">
          <HX.Pane>
            <HX.Collection numCols={3}
              fields={[
              "cds/territory",
              "cds/adj_base",
              "cds/territorial_focus_group",
              "cds/market_share",
              "cds/broker_contact",
              "cds/risk_carrier",
              "cds/personal_commercial",
              "cds/core_account",
              "cds/met_client_last_12_months",
              "cds/carrier_type",
              "cds/hours_clause",
              "cds/cyber_code",
              "cds/sanctions_clause",
              "cds/terrorism_code",
              "cds/named_perils",
              "cds/non_pd_bi",
              "cds/com_disease",
              "cds/am_best_rating",
              null,
              null,
              null,
              {
                "field": "cds/risk_xl_risk_definition",
                "shownBy": "/cds/show_risk_xl"
              },
              {
                "field": "cds/risk_xl_profile",
                "shownBy": "/cds/show_risk_xl"
              },
              {
                "field": "cds/risk_xl_sublimit_wind",
                "shownBy": "/cds/show_risk_xl"
              },
              {
                "field": "cds/risk_xl_sublimit_quake",
                "shownBy": "/cds/show_risk_xl"
              },
              {
                "field": "cds/risk_xl_sublimit_flood",
                "shownBy": "/cds/show_risk_xl"
              },
              {
                "field": "cds/risk_xl_non_cat_lr",
                "shownBy": "/cds/show_risk_xl"
              }
            ]} />
          </HX.Pane>
          <HX.Pane>
            <HX.Notes stretch={true}
              field="cds/application_comments"
              title="Comments" />
          </HX.Pane>
          <HX.Pane>
            <HX.Button task="generate_tags_task"
              title="Generate Tags" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Layer Details This Year">
          <HX.Table data={[
            "cds/layers",
            null,
            "cds/layer_totals"
          ]}
            fields={[
            {
              "field": "renewal_layer"
            },
            {
              "field": "is_facility"
            },
            {
              "field": "section_reference"
            },
            {
              "field": "loss_affected"
            },
            {
              "field": "currency",
              "shownBy": "/cds/show_intl_fields"
            },
            {
              "field": "leader"
            },
            {
              "field": "layer_description"
            },
            {
              "field": "limit"
            },
            {
              "field": "excess"
            },
            {
              "field": "risk_xl_occurrence_limit",
              "shownBy": "/cds/show_risk_xl"
            },
            {
              "field": "limit_cnv",
              "labelBy": "/cds/limit_application_ccy_label",
              "shownBy": "/cds/show_intl_fields"
            },
            {
              "field": "excess_cnv",
              "labelBy": "/cds/excess_application_ccy_label",
              "shownBy": "/cds/show_intl_fields"
            },
            {
              "field": "inner_type",
              "shownBy": "/cds/show_cat_work_comp_input"
            },
            {
              "field": "aggregate_deductible",
              "shownBy": "/cds/show_cat_work_comp_input"
            },
            {
              "field": "aggregate_deductible_cnv",
              "labelBy": "/cds/aggregate_deductible_application_ccy_label",
              "shownBy": "/cds/show_aad_cnv_field"
            },
            {
              "field": "number_reins",
              "shownBy": "/cds/show_cat_work_comp_input"
            },
            {
              "field": "perc_reins_1",
              "shownBy": "/cds/show_cat_work_comp_input"
            },
            {
              "field": "perc_reins_2",
              "shownBy": "/cds/show_cat_work_comp_input"
            },
            {
              "field": "perc_reins_3",
              "shownBy": "/cds/show_cat_work_comp_input"
            },
            null,
            {
              "field": "effective_brokerage"
            },
            null,
            {
              "field": "risk_xl_us_pml_code",
              "shownBy": "/cds/show_risk_xl"
            },
            {
              "field": "risk_xl_intl_pml_code",
              "shownBy": "/cds/show_risk_xl"
            }
          ]}
            kb-interactive={true}
            freezeLeft={0}
            syncColumnWidthsKey="layer_table" />
        </HX.Section>
        <HX.Section title="Layer Details Previous Year">
          <HX.Table data={[
            "cds/layers",
            null,
            "cds/layer_totals"
          ]}
            fields={[
            {
              "field": "renewal_layer_ly"
            },
            {
              "field": "is_facility_ly"
            },
            {
              "field": "section_reference_ly"
            },
            {
              "field": "loss_affected_ly"
            },
            {
              "field": "currency_ly",
              "shownBy": "/cds/show_intl_fields"
            },
            {
              "field": "leader_ly"
            },
            {
              "field": "layer_description_ly"
            },
            {
              "field": "limit_ly"
            },
            {
              "field": "excess_ly"
            },
            {
              "field": "risk_xl_occurrence_limit_ly",
              "shownBy": "/cds/show_risk_xl"
            },
            {
              "field": "limit_cnv_ly",
              "labelBy": "/cds/limit_application_ccy_label",
              "shownBy": "/cds/show_intl_fields"
            },
            {
              "field": "excess_cnv_ly",
              "labelBy": "/cds/excess_application_ccy_label",
              "shownBy": "/cds/show_intl_fields"
            },
            {
              "field": "inner_type_ly",
              "shownBy": "/cds/show_cat_work_comp_input"
            },
            {
              "field": "aggregate_deductible_ly",
              "shownBy": "/cds/show_cat_work_comp_input"
            },
            {
              "field": "aggregate_deductible_cnv_ly",
              "labelBy": "/cds/aggregate_deductible_application_ccy_label",
              "shownBy": "/cds/show_aad_cnv_field"
            },
            {
              "field": "number_reins_ly",
              "shownBy": "/cds/show_cat_work_comp_input"
            },
            {
              "field": "perc_reins_1_ly",
              "shownBy": "/cds/show_cat_work_comp_input"
            },
            {
              "field": "perc_reins_2_ly",
              "shownBy": "/cds/show_cat_work_comp_input"
            },
            {
              "field": "perc_reins_3_ly",
              "shownBy": "/cds/show_cat_work_comp_input"
            },
            null,
            {
              "field": "effective_brokerage_ly"
            },
            null,
            {
              "field": "risk_xl_us_pml_code_ly",
              "shownBy": "/cds/show_risk_xl"
            },
            {
              "field": "risk_xl_intl_pml_code_ly",
              "shownBy": "/cds/show_risk_xl"
            }
          ]}
            kb-interactive={true}
            freezeLeft={0}
            syncColumnWidthsKey="layer_table" />
        </HX.Section>
      </HX.Page>
      <HX.Page title="PML Curves"
        fullWidth={true}
        viewScale={0.6}
        shownBy="cds/show_non_risk_xl">
        <HX.Section title="Peril PML Selection">
          <HX.Pane flow="right"
            reflow={false}>
            <HX.Pane ratio={1}>
              <HX.Collection numCols={1}
                fields={[
                {
                  "field": "cds/modelling_account_level/rms_eq_curve_selection",
                  "shownBy": "/cds/show_us_fields"
                },
                {
                  "field": "cds/modelling_account_level/rms_ws_curve_selection",
                  "shownBy": "/cds/show_us_fields"
                },
                {
                  "field": "cds/modelling_account_level/rms_scs_curve_selection",
                  "shownBy": "/cds/show_us_fields"
                },
                {
                  "field": "cds/modelling_account_level/rms_eu_ws_curve_selection",
                  "shownBy": "/cds/show_intl_fields"
                },
                {
                  "field": "cds/modelling_account_level/rms_jp_eq_curve_selection",
                  "shownBy": "/cds/show_intl_fields"
                },
                {
                  "field": "cds/modelling_account_level/rms_jp_ws_curve_selection",
                  "shownBy": "/cds/show_intl_fields"
                },
                {
                  "field": "cds/modelling_account_level/rms_can_eq_curve_selection",
                  "shownBy": "/cds/show_intl_fields"
                },
                {
                  "field": "cds/modelling_account_level/rms_caribbean_ws_curve_selection",
                  "shownBy": "/cds/show_intl_fields"
                }
              ]}
                stretch={true} />
            </HX.Pane>
            <HX.Pane ratio={3}>
              <HX.Notes field="cds/pml_curves/information"
                title="PML Selection Information" />
            </HX.Pane>
          </HX.Pane>
        </HX.Section>
        <HX.Section title="PML Comments">
          <HX.Notes field="cds/pml_curves/comments" />
        </HX.Section>
        <HX.Section title="PML Entry">
          <HX.Pane flow="right"
            reflow={false}>
            <HX.Table title="                                                                                                                                                                                                    RMS Curves"
              with="cds/pml_curves"
              data={[
              {
                "datum": "curve_aggregator",
                "width": 200
              },
              {
                "datum": "burn_curve",
                "width": 200
              },
              null,
              {
                "datum": "rms_curves",
                "width": 200
              }
            ]}
              fields={[
              "include_in_peril_alloc",
              "peril",
              "curve_description",
              {
                "field": "currency",
                "shownBy": "/cds/show_intl_fields"
              }
            ]}
              transpose={true}
              removeHorizontalScroll={true}
              rowHeaderSettings={{
              "width": 200
            }}
              kb-interactive={true} />
            <HX.Table title="AIR Curves"
              with="cds/pml_curves"
              data={[
              {
                "datum": "air_curves",
                "width": 200
              }
            ]}
              fields={[
              "include_in_peril_alloc",
              "peril",
              "curve_description",
              {
                "field": "currency",
                "shownBy": "/cds/show_intl_fields"
              }
            ]}
              transpose={true}
              removeHorizontalScroll={true}
              rowHeaderSettings={{
              "width": 200
            }}
              kb-interactive={true} />
            <HX.Table title="NMP Curves"
              with="cds/pml_curves"
              data={[
              {
                "datum": "nmp_curves",
                "width": 200
              }
            ]}
              fields={[
              "include_in_peril_alloc",
              "peril",
              "curve_description",
              {
                "field": "currency",
                "shownBy": "/cds/show_intl_fields"
              }
            ]}
              transpose={true}
              removeHorizontalScroll={true}
              rowHeaderSettings={{
              "width": 200
            }}
              kb-interactive={true} />
            <HX.Table title="Other Curves"
              with="cds/pml_curves"
              data={[
              {
                "datum": "other_curves",
                "width": 200
              }
            ]}
              fields={[
              "include_in_peril_alloc",
              "peril",
              "curve_description",
              {
                "field": "currency",
                "shownBy": "/cds/show_intl_fields"
              }
            ]}
              transpose={true}
              removeHorizontalScroll={true}
              rowHeaderSettings={{
              "width": 200
            }}
              kb-interactive={true} />
          </HX.Pane>
          <HX.Pane flow="right"
            reflow={false}>
            <HX.Table title="This Year"
              with="cds/pml_curves"
              data={[
              {
                "datum": "curve_aggregator",
                "width": 200
              },
              {
                "datum": "burn_curve",
                "width": 200
              },
              null,
              {
                "datum": "rms_curves",
                "maxWidth": 200
              }
            ]}
              fields={[
              "rp_loss/rp_10000",
              "rp_loss/rp_5000",
              "rp_loss/rp_1000",
              "rp_loss/rp_500",
              "rp_loss/rp_250",
              "rp_loss/rp_200",
              "rp_loss/rp_100",
              "rp_loss/rp_50",
              "rp_loss/rp_25",
              "rp_loss/rp_10",
              "rp_loss/rp_5",
              "rp_loss/rp_2"
            ]}
              removeHorizontalScroll={true}
              transpose={true}
              rowHeaderSettings={{
              "width": 200
            }}
              kb-interactive={true} />
            <HX.Table title="This Year"
              with="cds/pml_curves"
              data={[
              {
                "datum": "air_curves",
                "maxWidth": 200
              }
            ]}
              fields={[
              "rp_loss/rp_10000",
              "rp_loss/rp_5000",
              "rp_loss/rp_1000",
              "rp_loss/rp_500",
              "rp_loss/rp_250",
              "rp_loss/rp_200",
              "rp_loss/rp_100",
              "rp_loss/rp_50",
              "rp_loss/rp_25",
              "rp_loss/rp_10",
              "rp_loss/rp_5",
              "rp_loss/rp_2"
            ]}
              removeHorizontalScroll={true}
              transpose={true}
              rowHeaderSettings={{
              "width": 200
            }}
              kb-interactive={true} />
            <HX.Table title="This Year"
              with="cds/pml_curves"
              data={[
              {
                "datum": "nmp_curves",
                "maxWidth": 200
              }
            ]}
              fields={[
              "rp_loss/rp_10000",
              "rp_loss/rp_5000",
              "rp_loss/rp_1000",
              "rp_loss/rp_500",
              "rp_loss/rp_250",
              "rp_loss/rp_200",
              "rp_loss/rp_100",
              "rp_loss/rp_50",
              "rp_loss/rp_25",
              "rp_loss/rp_10",
              "rp_loss/rp_5",
              "rp_loss/rp_2"
            ]}
              removeHorizontalScroll={true}
              transpose={true}
              rowHeaderSettings={{
              "width": 200
            }}
              kb-interactive={true} />
            <HX.Table title="This Year"
              with="cds/pml_curves"
              data={[
              {
                "datum": "other_curves",
                "maxWidth": 200
              }
            ]}
              fields={[
              "rp_loss/rp_10000",
              "rp_loss/rp_5000",
              "rp_loss/rp_1000",
              "rp_loss/rp_500",
              "rp_loss/rp_250",
              "rp_loss/rp_200",
              "rp_loss/rp_100",
              "rp_loss/rp_50",
              "rp_loss/rp_25",
              "rp_loss/rp_10",
              "rp_loss/rp_5",
              "rp_loss/rp_2"
            ]}
              removeHorizontalScroll={true}
              transpose={true}
              rowHeaderSettings={{
              "width": 200
            }}
              kb-interactive={true} />
          </HX.Pane>
          <HX.Pane flow="right"
            reflow={false}>
            <HX.Table title="YOY Change"
              with="cds/pml_curves"
              data={[
              {
                "datum": "curve_aggregator",
                "width": 200
              },
              {
                "datum": "burn_curve",
                "width": 200
              },
              null,
              {
                "datum": "rms_curves",
                "maxWidth": 200
              }
            ]}
              fields={[
              "rp_loss_change/rp_10000",
              "rp_loss_change/rp_5000",
              "rp_loss_change/rp_1000",
              "rp_loss_change/rp_500",
              "rp_loss_change/rp_250",
              "rp_loss_change/rp_200",
              "rp_loss_change/rp_100",
              "rp_loss_change/rp_50",
              "rp_loss_change/rp_25",
              "rp_loss_change/rp_10",
              "rp_loss_change/rp_5",
              "rp_loss_change/rp_2"
            ]}
              removeHorizontalScroll={true}
              transpose={true}
              rowHeaderSettings={{
              "width": 200
            }}
              kb-interactive={true} />
            <HX.Table title="YOY Change"
              with="cds/pml_curves"
              data={[
              {
                "datum": "air_curves",
                "maxWidth": 200
              }
            ]}
              fields={[
              "rp_loss_change/rp_10000",
              "rp_loss_change/rp_5000",
              "rp_loss_change/rp_1000",
              "rp_loss_change/rp_500",
              "rp_loss_change/rp_250",
              "rp_loss_change/rp_200",
              "rp_loss_change/rp_100",
              "rp_loss_change/rp_50",
              "rp_loss_change/rp_25",
              "rp_loss_change/rp_10",
              "rp_loss_change/rp_5",
              "rp_loss_change/rp_2"
            ]}
              removeHorizontalScroll={true}
              transpose={true}
              rowHeaderSettings={{
              "width": 200
            }}
              kb-interactive={true} />
            <HX.Table title="YOY Change"
              with="cds/pml_curves"
              data={[
              {
                "datum": "nmp_curves",
                "maxWidth": 200
              }
            ]}
              fields={[
              "rp_loss_change/rp_10000",
              "rp_loss_change/rp_5000",
              "rp_loss_change/rp_1000",
              "rp_loss_change/rp_500",
              "rp_loss_change/rp_250",
              "rp_loss_change/rp_200",
              "rp_loss_change/rp_100",
              "rp_loss_change/rp_50",
              "rp_loss_change/rp_25",
              "rp_loss_change/rp_10",
              "rp_loss_change/rp_5",
              "rp_loss_change/rp_2"
            ]}
              removeHorizontalScroll={true}
              transpose={true}
              rowHeaderSettings={{
              "width": 200
            }}
              kb-interactive={true} />
            <HX.Table title="YOY Change"
              with="cds/pml_curves"
              data={[
              {
                "datum": "other_curves",
                "maxWidth": 200
              }
            ]}
              fields={[
              "rp_loss_change/rp_10000",
              "rp_loss_change/rp_5000",
              "rp_loss_change/rp_1000",
              "rp_loss_change/rp_500",
              "rp_loss_change/rp_250",
              "rp_loss_change/rp_200",
              "rp_loss_change/rp_100",
              "rp_loss_change/rp_50",
              "rp_loss_change/rp_25",
              "rp_loss_change/rp_10",
              "rp_loss_change/rp_5",
              "rp_loss_change/rp_2"
            ]}
              removeHorizontalScroll={true}
              transpose={true}
              rowHeaderSettings={{
              "width": 200
            }}
              kb-interactive={true} />
          </HX.Pane>
          <HX.Pane flow="right"
            reflow={false}>
            <HX.Table title="Previous Year"
              with="cds/pml_curves"
              data={[
              {
                "datum": "curve_aggregator",
                "width": 200
              },
              {
                "datum": "burn_curve",
                "width": 200
              },
              null,
              {
                "datum": "rms_curves",
                "maxWidth": 200
              }
            ]}
              fields={[
              "rp_loss_prev/rp_10000",
              "rp_loss_prev/rp_5000",
              "rp_loss_prev/rp_1000",
              "rp_loss_prev/rp_500",
              "rp_loss_prev/rp_250",
              "rp_loss_prev/rp_200",
              "rp_loss_prev/rp_100",
              "rp_loss_prev/rp_50",
              "rp_loss_prev/rp_25",
              "rp_loss_prev/rp_10",
              "rp_loss_prev/rp_5",
              "rp_loss_prev/rp_2"
            ]}
              removeHorizontalScroll={true}
              transpose={true}
              rowHeaderSettings={{
              "width": 200
            }}
              kb-interactive={true} />
            <HX.Table title="Previous Year"
              with="cds/pml_curves"
              data={[
              {
                "datum": "air_curves",
                "maxWidth": 200
              }
            ]}
              fields={[
              "rp_loss_prev/rp_10000",
              "rp_loss_prev/rp_5000",
              "rp_loss_prev/rp_1000",
              "rp_loss_prev/rp_500",
              "rp_loss_prev/rp_250",
              "rp_loss_prev/rp_200",
              "rp_loss_prev/rp_100",
              "rp_loss_prev/rp_50",
              "rp_loss_prev/rp_25",
              "rp_loss_prev/rp_10",
              "rp_loss_prev/rp_5",
              "rp_loss_prev/rp_2"
            ]}
              removeHorizontalScroll={true}
              transpose={true}
              rowHeaderSettings={{
              "width": 200
            }}
              kb-interactive={true} />
            <HX.Table title="Previous Year"
              with="cds/pml_curves"
              data={[
              {
                "datum": "nmp_curves",
                "maxWidth": 200
              }
            ]}
              fields={[
              "rp_loss_prev/rp_10000",
              "rp_loss_prev/rp_5000",
              "rp_loss_prev/rp_1000",
              "rp_loss_prev/rp_500",
              "rp_loss_prev/rp_250",
              "rp_loss_prev/rp_200",
              "rp_loss_prev/rp_100",
              "rp_loss_prev/rp_50",
              "rp_loss_prev/rp_25",
              "rp_loss_prev/rp_10",
              "rp_loss_prev/rp_5",
              "rp_loss_prev/rp_2"
            ]}
              removeHorizontalScroll={true}
              transpose={true}
              rowHeaderSettings={{
              "width": 200
            }}
              kb-interactive={true} />
            <HX.Table title="Previous Year"
              with="cds/pml_curves"
              data={[
              {
                "datum": "other_curves",
                "maxWidth": 200
              }
            ]}
              fields={[
              "rp_loss_prev/rp_10000",
              "rp_loss_prev/rp_5000",
              "rp_loss_prev/rp_1000",
              "rp_loss_prev/rp_500",
              "rp_loss_prev/rp_250",
              "rp_loss_prev/rp_200",
              "rp_loss_prev/rp_100",
              "rp_loss_prev/rp_50",
              "rp_loss_prev/rp_25",
              "rp_loss_prev/rp_10",
              "rp_loss_prev/rp_5",
              "rp_loss_prev/rp_2"
            ]}
              removeHorizontalScroll={true}
              transpose={true}
              rowHeaderSettings={{
              "width": 200
            }}
              kb-interactive={true} />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="NMP"
        fullWidth={true}
        viewScale={0.7}
        shownBy="cds/show_non_risk_xl">
        <HX.Section title="Summary">
          <HX.Pane flow="right"
            reflow={false}>
            <HX.Pane>
              <HX.Notes field="cds/non_modelled_perils_visual/information"
                title="NMP Information" />
              <HX.Notes field="cds/non_modelled_perils_visual/us_wf_information"
                title="US Wildfire RI Cost" />
            </HX.Pane>
            <HX.Pane />
          </HX.Pane>
          <HX.Pane flow="right"
            reflow={false}>
            <HX.Pane ratio={5}>
              <HX.Table data={[
                {
                  "datum": "cds/layers"
                }
              ]}
                fields={[
                "limit.read_only_option",
                "excess.read_only_option",
                "nmp/non_modelled_perils_total/gross_el",
                "nmp/non_modelled_perils_total/gross_sd",
                "nmp/non_modelled_perils_total/gross_el_uw",
                "nmp/non_modelled_perils_total/gross_sd_uw",
                null,
                "nmp/non_modelled_perils_total/loss_on_line"
              ]}
                kb-interactive={true} />
            </HX.Pane>
            <HX.Pane ratio={1}>
              <HX.Collection fields={[
                "cds/non_modelled_perils_visual/curve_number"
              ]} />
              <HX.Button task="nmp_calc_task"
                title="Run NMP Task" />
            </HX.Pane>
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Curve 1"
          shownBy="cds/non_modelled_perils_visual/show_curve_1">
          <HX.With context={{
            "index": 0,
            "path": "cds/non_modelled_perils",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Table data={[
                {
                  "datum": "curve_selections"
                }
              ]}
                fields={[
                "include_in_summary",
                "broker_pml",
                "peril",
                "description",
                {
                  "field": "curve",
                  "shownBy": "curve_selections/show_market_pml"
                },
                "rp",
                "loss",
                {
                  "field": "currency",
                  "shownBy": "/cds/show_intl_fields"
                }
              ]}
                transpose={true}
                kb-interactive={true} />
              <HX.Pane>
                <HX.Table data={[
                  "rp_labels",
                  {
                    "datum": "pml_broker",
                    "labelBy": "curve_selections/pml_broker_label"
                  },
                  {
                    "datum": "pml_market",
                    "labelBy": "curve_selections/pml_market_label"
                  },
                  "pml_final"
                ]}
                  fields={[
                  "rp_10000",
                  "rp_5000",
                  "rp_1000",
                  "rp_500",
                  "rp_250",
                  "rp_200",
                  "rp_100",
                  "rp_50",
                  "rp_25",
                  "rp_10",
                  "rp_5",
                  "rp_2"
                ]}
                  transpose={true}
                  kb-interactive={true} />
              </HX.Pane>
            </HX.Pane>
          </HX.With>
          <HX.Pane>
            <HX.Table data={[
              {
                "datum": "cds/layers"
              }
            ]}
              fields={[
              "limit.read_only_option",
              "excess.read_only_option",
              "nmp/non_modelled_perils_1/gross_el",
              "nmp/non_modelled_perils_1/loss_on_line",
              "nmp/non_modelled_perils_1/gross_sd",
              "nmp/non_modelled_perils_1/include_curve"
            ]}
              freezeLeft={0}
              kb-interactive={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Curve 2"
          shownBy="cds/non_modelled_perils_visual/show_curve_2">
          <HX.With context={{
            "index": 1,
            "path": "cds/non_modelled_perils",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Table data={[
                {
                  "datum": "curve_selections"
                }
              ]}
                fields={[
                "include_in_summary",
                "broker_pml",
                "peril",
                "description",
                {
                  "field": "curve",
                  "shownBy": "curve_selections/show_market_pml"
                },
                "rp",
                "loss",
                {
                  "field": "currency",
                  "shownBy": "/cds/show_intl_fields"
                }
              ]}
                transpose={true}
                kb-interactive={true} />
              <HX.Pane>
                <HX.Table data={[
                  "rp_labels",
                  {
                    "datum": "pml_broker",
                    "labelBy": "curve_selections/pml_broker_label"
                  },
                  {
                    "datum": "pml_market",
                    "labelBy": "curve_selections/pml_market_label"
                  },
                  "pml_final"
                ]}
                  fields={[
                  "rp_10000",
                  "rp_5000",
                  "rp_1000",
                  "rp_500",
                  "rp_250",
                  "rp_200",
                  "rp_100",
                  "rp_50",
                  "rp_25",
                  "rp_10",
                  "rp_5",
                  "rp_2"
                ]}
                  transpose={true}
                  kb-interactive={true} />
              </HX.Pane>
            </HX.Pane>
          </HX.With>
          <HX.Pane>
            <HX.Table data={[
              {
                "datum": "cds/layers"
              }
            ]}
              fields={[
              "limit.read_only_option",
              "excess.read_only_option",
              "nmp/non_modelled_perils_2/gross_el",
              "nmp/non_modelled_perils_2/loss_on_line",
              "nmp/non_modelled_perils_2/gross_sd",
              "nmp/non_modelled_perils_2/include_curve"
            ]}
              freezeLeft={0}
              kb-interactive={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Curve 3"
          shownBy="cds/non_modelled_perils_visual/show_curve_3">
          <HX.With context={{
            "index": 2,
            "path": "cds/non_modelled_perils",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Table data={[
                {
                  "datum": "curve_selections"
                }
              ]}
                fields={[
                "include_in_summary",
                "broker_pml",
                "peril",
                "description",
                {
                  "field": "curve",
                  "shownBy": "curve_selections/show_market_pml"
                },
                "rp",
                "loss",
                {
                  "field": "currency",
                  "shownBy": "/cds/show_intl_fields"
                }
              ]}
                transpose={true}
                kb-interactive={true} />
              <HX.Pane>
                <HX.Table data={[
                  "rp_labels",
                  {
                    "datum": "pml_broker",
                    "labelBy": "curve_selections/pml_broker_label"
                  },
                  {
                    "datum": "pml_market",
                    "labelBy": "curve_selections/pml_market_label"
                  },
                  "pml_final"
                ]}
                  fields={[
                  "rp_10000",
                  "rp_5000",
                  "rp_1000",
                  "rp_500",
                  "rp_250",
                  "rp_200",
                  "rp_100",
                  "rp_50",
                  "rp_25",
                  "rp_10",
                  "rp_5",
                  "rp_2"
                ]}
                  transpose={true}
                  kb-interactive={true} />
              </HX.Pane>
            </HX.Pane>
          </HX.With>
          <HX.Pane>
            <HX.Table data={[
              {
                "datum": "cds/layers"
              }
            ]}
              fields={[
              "limit.read_only_option",
              "excess.read_only_option",
              "nmp/non_modelled_perils_3/gross_el",
              "nmp/non_modelled_perils_3/loss_on_line",
              "nmp/non_modelled_perils_3/gross_sd",
              "nmp/non_modelled_perils_3/include_curve"
            ]}
              freezeLeft={0}
              kb-interactive={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Curve 4"
          shownBy="cds/non_modelled_perils_visual/show_curve_4">
          <HX.With context={{
            "index": 3,
            "path": "cds/non_modelled_perils",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Table data={[
                {
                  "datum": "curve_selections"
                }
              ]}
                fields={[
                "include_in_summary",
                "broker_pml",
                "peril",
                "description",
                {
                  "field": "curve",
                  "shownBy": "curve_selections/show_market_pml"
                },
                "rp",
                "loss",
                {
                  "field": "currency",
                  "shownBy": "/cds/show_intl_fields"
                }
              ]}
                transpose={true}
                kb-interactive={true} />
              <HX.Pane>
                <HX.Table data={[
                  "rp_labels",
                  {
                    "datum": "pml_broker",
                    "labelBy": "curve_selections/pml_broker_label"
                  },
                  {
                    "datum": "pml_market",
                    "labelBy": "curve_selections/pml_market_label"
                  },
                  "pml_final"
                ]}
                  fields={[
                  "rp_10000",
                  "rp_5000",
                  "rp_1000",
                  "rp_500",
                  "rp_250",
                  "rp_200",
                  "rp_100",
                  "rp_50",
                  "rp_25",
                  "rp_10",
                  "rp_5",
                  "rp_2"
                ]}
                  transpose={true}
                  kb-interactive={true} />
              </HX.Pane>
            </HX.Pane>
          </HX.With>
          <HX.Pane>
            <HX.Table data={[
              {
                "datum": "cds/layers"
              }
            ]}
              fields={[
              "limit.read_only_option",
              "excess.read_only_option",
              "nmp/non_modelled_perils_4/gross_el",
              "nmp/non_modelled_perils_4/loss_on_line",
              "nmp/non_modelled_perils_4/gross_sd",
              "nmp/non_modelled_perils_4/include_curve"
            ]}
              freezeLeft={0}
              kb-interactive={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Curve 5"
          shownBy="cds/non_modelled_perils_visual/show_curve_5">
          <HX.With context={{
            "index": 4,
            "path": "cds/non_modelled_perils",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Table data={[
                {
                  "datum": "curve_selections"
                }
              ]}
                fields={[
                "include_in_summary",
                "broker_pml",
                "peril",
                "description",
                {
                  "field": "curve",
                  "shownBy": "curve_selections/show_market_pml"
                },
                "rp",
                "loss",
                {
                  "field": "currency",
                  "shownBy": "/cds/show_intl_fields"
                }
              ]}
                transpose={true}
                kb-interactive={true} />
              <HX.Pane>
                <HX.Table data={[
                  "rp_labels",
                  {
                    "datum": "pml_broker",
                    "labelBy": "curve_selections/pml_broker_label"
                  },
                  {
                    "datum": "pml_market",
                    "labelBy": "curve_selections/pml_market_label"
                  },
                  "pml_final"
                ]}
                  fields={[
                  "rp_10000",
                  "rp_5000",
                  "rp_1000",
                  "rp_500",
                  "rp_250",
                  "rp_200",
                  "rp_100",
                  "rp_50",
                  "rp_25",
                  "rp_10",
                  "rp_5",
                  "rp_2"
                ]}
                  transpose={true}
                  kb-interactive={true} />
              </HX.Pane>
            </HX.Pane>
          </HX.With>
          <HX.Pane>
            <HX.Table data={[
              {
                "datum": "cds/layers"
              }
            ]}
              fields={[
              "limit.read_only_option",
              "excess.read_only_option",
              "nmp/non_modelled_perils_5/gross_el",
              "nmp/non_modelled_perils_5/loss_on_line",
              "nmp/non_modelled_perils_5/gross_sd",
              "nmp/non_modelled_perils_5/include_curve"
            ]}
              freezeLeft={0}
              kb-interactive={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Curve 6"
          shownBy="cds/non_modelled_perils_visual/show_curve_6">
          <HX.With context={{
            "index": 5,
            "path": "cds/non_modelled_perils",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Table data={[
                {
                  "datum": "curve_selections"
                }
              ]}
                fields={[
                "include_in_summary",
                "broker_pml",
                "peril",
                "description",
                {
                  "field": "curve",
                  "shownBy": "curve_selections/show_market_pml"
                },
                "rp",
                "loss",
                {
                  "field": "currency",
                  "shownBy": "/cds/show_intl_fields"
                }
              ]}
                transpose={true}
                kb-interactive={true} />
              <HX.Pane>
                <HX.Table data={[
                  "rp_labels",
                  {
                    "datum": "pml_broker",
                    "labelBy": "curve_selections/pml_broker_label"
                  },
                  {
                    "datum": "pml_market",
                    "labelBy": "curve_selections/pml_market_label"
                  },
                  "pml_final"
                ]}
                  fields={[
                  "rp_10000",
                  "rp_5000",
                  "rp_1000",
                  "rp_500",
                  "rp_250",
                  "rp_200",
                  "rp_100",
                  "rp_50",
                  "rp_25",
                  "rp_10",
                  "rp_5",
                  "rp_2"
                ]}
                  transpose={true}
                  kb-interactive={true} />
              </HX.Pane>
            </HX.Pane>
          </HX.With>
          <HX.Pane>
            <HX.Table data={[
              {
                "datum": "cds/layers"
              }
            ]}
              fields={[
              "limit.read_only_option",
              "excess.read_only_option",
              "nmp/non_modelled_perils_6/gross_el",
              "nmp/non_modelled_perils_6/loss_on_line",
              "nmp/non_modelled_perils_6/gross_sd",
              "nmp/non_modelled_perils_6/include_curve"
            ]}
              freezeLeft={0}
              kb-interactive={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Curve 7"
          shownBy="cds/non_modelled_perils_visual/show_curve_7">
          <HX.With context={{
            "index": 6,
            "path": "cds/non_modelled_perils",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Table data={[
                {
                  "datum": "curve_selections"
                }
              ]}
                fields={[
                "include_in_summary",
                "broker_pml",
                "peril",
                "description",
                {
                  "field": "curve",
                  "shownBy": "curve_selections/show_market_pml"
                },
                "rp",
                "loss",
                {
                  "field": "currency",
                  "shownBy": "/cds/show_intl_fields"
                }
              ]}
                transpose={true}
                kb-interactive={true} />
              <HX.Pane>
                <HX.Table data={[
                  "rp_labels",
                  {
                    "datum": "pml_broker",
                    "labelBy": "curve_selections/pml_broker_label"
                  },
                  {
                    "datum": "pml_market",
                    "labelBy": "curve_selections/pml_market_label"
                  },
                  "pml_final"
                ]}
                  fields={[
                  "rp_10000",
                  "rp_5000",
                  "rp_1000",
                  "rp_500",
                  "rp_250",
                  "rp_200",
                  "rp_100",
                  "rp_50",
                  "rp_25",
                  "rp_10",
                  "rp_5",
                  "rp_2"
                ]}
                  transpose={true}
                  kb-interactive={true} />
              </HX.Pane>
            </HX.Pane>
          </HX.With>
          <HX.Pane>
            <HX.Table data={[
              {
                "datum": "cds/layers"
              }
            ]}
              fields={[
              "limit.read_only_option",
              "excess.read_only_option",
              "nmp/non_modelled_perils_7/gross_el",
              "nmp/non_modelled_perils_7/loss_on_line",
              "nmp/non_modelled_perils_7/gross_sd",
              "nmp/non_modelled_perils_7/include_curve"
            ]}
              freezeLeft={0}
              kb-interactive={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Curve 8"
          shownBy="cds/non_modelled_perils_visual/show_curve_8">
          <HX.With context={{
            "index": 7,
            "path": "cds/non_modelled_perils",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Table data={[
                {
                  "datum": "curve_selections"
                }
              ]}
                fields={[
                "include_in_summary",
                "broker_pml",
                "peril",
                "description",
                {
                  "field": "curve",
                  "shownBy": "curve_selections/show_market_pml"
                },
                "rp",
                "loss",
                {
                  "field": "currency",
                  "shownBy": "/cds/show_intl_fields"
                }
              ]}
                transpose={true}
                kb-interactive={true} />
              <HX.Pane>
                <HX.Table data={[
                  "rp_labels",
                  {
                    "datum": "pml_broker",
                    "labelBy": "curve_selections/pml_broker_label"
                  },
                  {
                    "datum": "pml_market",
                    "labelBy": "curve_selections/pml_market_label"
                  },
                  "pml_final"
                ]}
                  fields={[
                  "rp_10000",
                  "rp_5000",
                  "rp_1000",
                  "rp_500",
                  "rp_250",
                  "rp_200",
                  "rp_100",
                  "rp_50",
                  "rp_25",
                  "rp_10",
                  "rp_5",
                  "rp_2"
                ]}
                  transpose={true}
                  kb-interactive={true} />
              </HX.Pane>
            </HX.Pane>
          </HX.With>
          <HX.Pane>
            <HX.Table data={[
              {
                "datum": "cds/layers"
              }
            ]}
              fields={[
              "limit.read_only_option",
              "excess.read_only_option",
              "nmp/non_modelled_perils_8/gross_el",
              "nmp/non_modelled_perils_8/loss_on_line",
              "nmp/non_modelled_perils_8/gross_sd",
              "nmp/non_modelled_perils_8/include_curve"
            ]}
              freezeLeft={0}
              kb-interactive={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Curve 9"
          shownBy="cds/non_modelled_perils_visual/show_curve_9">
          <HX.With context={{
            "index": 8,
            "path": "cds/non_modelled_perils",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Table data={[
                {
                  "datum": "curve_selections"
                }
              ]}
                fields={[
                "include_in_summary",
                "broker_pml",
                "peril",
                "description",
                {
                  "field": "curve",
                  "shownBy": "curve_selections/show_market_pml"
                },
                "rp",
                "loss",
                {
                  "field": "currency",
                  "shownBy": "/cds/show_intl_fields"
                }
              ]}
                transpose={true}
                kb-interactive={true} />
              <HX.Pane>
                <HX.Table data={[
                  "rp_labels",
                  {
                    "datum": "pml_broker",
                    "labelBy": "curve_selections/pml_broker_label"
                  },
                  {
                    "datum": "pml_market",
                    "labelBy": "curve_selections/pml_market_label"
                  },
                  "pml_final"
                ]}
                  fields={[
                  "rp_10000",
                  "rp_5000",
                  "rp_1000",
                  "rp_500",
                  "rp_250",
                  "rp_200",
                  "rp_100",
                  "rp_50",
                  "rp_25",
                  "rp_10",
                  "rp_5",
                  "rp_2"
                ]}
                  transpose={true}
                  kb-interactive={true} />
              </HX.Pane>
            </HX.Pane>
          </HX.With>
          <HX.Pane>
            <HX.Table data={[
              {
                "datum": "cds/layers"
              }
            ]}
              fields={[
              "limit.read_only_option",
              "excess.read_only_option",
              "nmp/non_modelled_perils_9/gross_el",
              "nmp/non_modelled_perils_9/loss_on_line",
              "nmp/non_modelled_perils_9/gross_sd",
              "nmp/non_modelled_perils_9/include_curve"
            ]}
              freezeLeft={0}
              kb-interactive={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Curve 10"
          shownBy="cds/non_modelled_perils_visual/show_curve_10">
          <HX.With context={{
            "index": 9,
            "path": "cds/non_modelled_perils",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Table data={[
                {
                  "datum": "curve_selections"
                }
              ]}
                fields={[
                "include_in_summary",
                "broker_pml",
                "peril",
                "description",
                {
                  "field": "curve",
                  "shownBy": "curve_selections/show_market_pml"
                },
                "rp",
                "loss",
                {
                  "field": "currency",
                  "shownBy": "/cds/show_intl_fields"
                }
              ]}
                transpose={true}
                kb-interactive={true} />
              <HX.Pane>
                <HX.Table data={[
                  "rp_labels",
                  {
                    "datum": "pml_broker",
                    "labelBy": "curve_selections/pml_broker_label"
                  },
                  {
                    "datum": "pml_market",
                    "labelBy": "curve_selections/pml_market_label"
                  },
                  "pml_final"
                ]}
                  fields={[
                  "rp_10000",
                  "rp_5000",
                  "rp_1000",
                  "rp_500",
                  "rp_250",
                  "rp_200",
                  "rp_100",
                  "rp_50",
                  "rp_25",
                  "rp_10",
                  "rp_5",
                  "rp_2"
                ]}
                  transpose={true}
                  kb-interactive={true} />
              </HX.Pane>
            </HX.Pane>
          </HX.With>
          <HX.Pane>
            <HX.Table data={[
              {
                "datum": "cds/layers"
              }
            ]}
              fields={[
              "limit.read_only_option",
              "excess.read_only_option",
              "nmp/non_modelled_perils_10/gross_el",
              "nmp/non_modelled_perils_10/loss_on_line",
              "nmp/non_modelled_perils_10/gross_sd",
              "nmp/non_modelled_perils_10/include_curve"
            ]}
              freezeLeft={0}
              kb-interactive={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Curve 11"
          shownBy="cds/non_modelled_perils_visual/show_curve_11">
          <HX.With context={{
            "index": 10,
            "path": "cds/non_modelled_perils",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Table data={[
                {
                  "datum": "curve_selections"
                }
              ]}
                fields={[
                "include_in_summary",
                "broker_pml",
                "peril",
                "description",
                {
                  "field": "curve",
                  "shownBy": "curve_selections/show_market_pml"
                },
                "rp",
                "loss",
                {
                  "field": "currency",
                  "shownBy": "/cds/show_intl_fields"
                }
              ]}
                transpose={true}
                kb-interactive={true} />
              <HX.Pane>
                <HX.Table data={[
                  "rp_labels",
                  {
                    "datum": "pml_broker",
                    "labelBy": "curve_selections/pml_broker_label"
                  },
                  {
                    "datum": "pml_market",
                    "labelBy": "curve_selections/pml_market_label"
                  },
                  "pml_final"
                ]}
                  fields={[
                  "rp_10000",
                  "rp_5000",
                  "rp_1000",
                  "rp_500",
                  "rp_250",
                  "rp_200",
                  "rp_100",
                  "rp_50",
                  "rp_25",
                  "rp_10",
                  "rp_5",
                  "rp_2"
                ]}
                  transpose={true}
                  kb-interactive={true} />
              </HX.Pane>
            </HX.Pane>
          </HX.With>
          <HX.Pane>
            <HX.Table data={[
              {
                "datum": "cds/layers"
              }
            ]}
              fields={[
              "limit.read_only_option",
              "excess.read_only_option",
              "nmp/non_modelled_perils_11/gross_el",
              "nmp/non_modelled_perils_11/loss_on_line",
              "nmp/non_modelled_perils_11/gross_sd",
              "nmp/non_modelled_perils_11/include_curve"
            ]}
              freezeLeft={0}
              kb-interactive={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Curve 12"
          shownBy="cds/non_modelled_perils_visual/show_curve_12">
          <HX.With context={{
            "index": 11,
            "path": "cds/non_modelled_perils",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Table data={[
                {
                  "datum": "curve_selections"
                }
              ]}
                fields={[
                "include_in_summary",
                "broker_pml",
                "peril",
                "description",
                {
                  "field": "curve",
                  "shownBy": "curve_selections/show_market_pml"
                },
                "rp",
                "loss",
                {
                  "field": "currency",
                  "shownBy": "/cds/show_intl_fields"
                }
              ]}
                transpose={true}
                kb-interactive={true} />
              <HX.Pane>
                <HX.Table data={[
                  "rp_labels",
                  {
                    "datum": "pml_broker",
                    "labelBy": "curve_selections/pml_broker_label"
                  },
                  {
                    "datum": "pml_market",
                    "labelBy": "curve_selections/pml_market_label"
                  },
                  "pml_final"
                ]}
                  fields={[
                  "rp_10000",
                  "rp_5000",
                  "rp_1000",
                  "rp_500",
                  "rp_250",
                  "rp_200",
                  "rp_100",
                  "rp_50",
                  "rp_25",
                  "rp_10",
                  "rp_5",
                  "rp_2"
                ]}
                  transpose={true}
                  kb-interactive={true} />
              </HX.Pane>
            </HX.Pane>
          </HX.With>
          <HX.Pane>
            <HX.Table data={[
              {
                "datum": "cds/layers"
              }
            ]}
              fields={[
              "limit.read_only_option",
              "excess.read_only_option",
              "nmp/non_modelled_perils_12/gross_el",
              "nmp/non_modelled_perils_12/loss_on_line",
              "nmp/non_modelled_perils_12/gross_sd",
              "nmp/non_modelled_perils_12/include_curve"
            ]}
              freezeLeft={0}
              kb-interactive={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Curve 13"
          shownBy="cds/non_modelled_perils_visual/show_curve_13">
          <HX.With context={{
            "index": 12,
            "path": "cds/non_modelled_perils",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Table data={[
                {
                  "datum": "curve_selections"
                }
              ]}
                fields={[
                "include_in_summary",
                "broker_pml",
                "peril",
                "description",
                {
                  "field": "curve",
                  "shownBy": "curve_selections/show_market_pml"
                },
                "rp",
                "loss",
                {
                  "field": "currency",
                  "shownBy": "/cds/show_intl_fields"
                }
              ]}
                transpose={true}
                kb-interactive={true} />
              <HX.Pane>
                <HX.Table data={[
                  "rp_labels",
                  {
                    "datum": "pml_broker",
                    "labelBy": "curve_selections/pml_broker_label"
                  },
                  {
                    "datum": "pml_market",
                    "labelBy": "curve_selections/pml_market_label"
                  },
                  "pml_final"
                ]}
                  fields={[
                  "rp_10000",
                  "rp_5000",
                  "rp_1000",
                  "rp_500",
                  "rp_250",
                  "rp_200",
                  "rp_100",
                  "rp_50",
                  "rp_25",
                  "rp_10",
                  "rp_5",
                  "rp_2"
                ]}
                  transpose={true}
                  kb-interactive={true} />
              </HX.Pane>
            </HX.Pane>
          </HX.With>
          <HX.Pane>
            <HX.Table data={[
              {
                "datum": "cds/layers"
              }
            ]}
              fields={[
              "limit.read_only_option",
              "excess.read_only_option",
              "nmp/non_modelled_perils_13/gross_el",
              "nmp/non_modelled_perils_13/loss_on_line",
              "nmp/non_modelled_perils_13/gross_sd",
              "nmp/non_modelled_perils_13/include_curve"
            ]}
              freezeLeft={0}
              kb-interactive={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Curve 14"
          shownBy="cds/non_modelled_perils_visual/show_curve_14">
          <HX.With context={{
            "index": 13,
            "path": "cds/non_modelled_perils",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Table data={[
                {
                  "datum": "curve_selections"
                }
              ]}
                fields={[
                "include_in_summary",
                "broker_pml",
                "peril",
                "description",
                {
                  "field": "curve",
                  "shownBy": "curve_selections/show_market_pml"
                },
                "rp",
                "loss",
                {
                  "field": "currency",
                  "shownBy": "/cds/show_intl_fields"
                }
              ]}
                transpose={true}
                kb-interactive={true} />
              <HX.Pane>
                <HX.Table data={[
                  "rp_labels",
                  {
                    "datum": "pml_broker",
                    "labelBy": "curve_selections/pml_broker_label"
                  },
                  {
                    "datum": "pml_market",
                    "labelBy": "curve_selections/pml_market_label"
                  },
                  "pml_final"
                ]}
                  fields={[
                  "rp_10000",
                  "rp_5000",
                  "rp_1000",
                  "rp_500",
                  "rp_250",
                  "rp_200",
                  "rp_100",
                  "rp_50",
                  "rp_25",
                  "rp_10",
                  "rp_5",
                  "rp_2"
                ]}
                  transpose={true}
                  kb-interactive={true} />
              </HX.Pane>
            </HX.Pane>
          </HX.With>
          <HX.Pane>
            <HX.Table data={[
              {
                "datum": "cds/layers"
              }
            ]}
              fields={[
              "limit.read_only_option",
              "excess.read_only_option",
              "nmp/non_modelled_perils_14/gross_el",
              "nmp/non_modelled_perils_14/loss_on_line",
              "nmp/non_modelled_perils_14/gross_sd",
              "nmp/non_modelled_perils_14/include_curve"
            ]}
              freezeLeft={0}
              kb-interactive={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Curve 15"
          shownBy="cds/non_modelled_perils_visual/show_curve_15">
          <HX.With context={{
            "index": 14,
            "path": "cds/non_modelled_perils",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Table data={[
                {
                  "datum": "curve_selections"
                }
              ]}
                fields={[
                "include_in_summary",
                "broker_pml",
                "peril",
                "description",
                {
                  "field": "curve",
                  "shownBy": "curve_selections/show_market_pml"
                },
                "rp",
                "loss",
                {
                  "field": "currency",
                  "shownBy": "/cds/show_intl_fields"
                }
              ]}
                transpose={true}
                kb-interactive={true} />
              <HX.Pane>
                <HX.Table data={[
                  "rp_labels",
                  {
                    "datum": "pml_broker",
                    "labelBy": "curve_selections/pml_broker_label"
                  },
                  {
                    "datum": "pml_market",
                    "labelBy": "curve_selections/pml_market_label"
                  },
                  "pml_final"
                ]}
                  fields={[
                  "rp_10000",
                  "rp_5000",
                  "rp_1000",
                  "rp_500",
                  "rp_250",
                  "rp_200",
                  "rp_100",
                  "rp_50",
                  "rp_25",
                  "rp_10",
                  "rp_5",
                  "rp_2"
                ]}
                  transpose={true}
                  kb-interactive={true} />
              </HX.Pane>
            </HX.Pane>
          </HX.With>
          <HX.Pane>
            <HX.Table data={[
              {
                "datum": "cds/layers"
              }
            ]}
              fields={[
              "limit.read_only_option",
              "excess.read_only_option",
              "nmp/non_modelled_perils_15/gross_el",
              "nmp/non_modelled_perils_15/loss_on_line",
              "nmp/non_modelled_perils_15/gross_sd",
              "nmp/non_modelled_perils_15/include_curve"
            ]}
              freezeLeft={0}
              kb-interactive={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Curve 16"
          shownBy="cds/non_modelled_perils_visual/show_curve_16">
          <HX.With context={{
            "index": 15,
            "path": "cds/non_modelled_perils",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Table data={[
                {
                  "datum": "curve_selections"
                }
              ]}
                fields={[
                "include_in_summary",
                "broker_pml",
                "peril",
                "description",
                {
                  "field": "curve",
                  "shownBy": "curve_selections/show_market_pml"
                },
                "rp",
                "loss",
                {
                  "field": "currency",
                  "shownBy": "/cds/show_intl_fields"
                }
              ]}
                transpose={true}
                kb-interactive={true} />
              <HX.Pane>
                <HX.Table data={[
                  "rp_labels",
                  {
                    "datum": "pml_broker",
                    "labelBy": "curve_selections/pml_broker_label"
                  },
                  {
                    "datum": "pml_market",
                    "labelBy": "curve_selections/pml_market_label"
                  },
                  "pml_final"
                ]}
                  fields={[
                  "rp_10000",
                  "rp_5000",
                  "rp_1000",
                  "rp_500",
                  "rp_250",
                  "rp_200",
                  "rp_100",
                  "rp_50",
                  "rp_25",
                  "rp_10",
                  "rp_5",
                  "rp_2"
                ]}
                  transpose={true}
                  kb-interactive={true} />
              </HX.Pane>
            </HX.Pane>
          </HX.With>
          <HX.Pane>
            <HX.Table data={[
              {
                "datum": "cds/layers"
              }
            ]}
              fields={[
              "limit.read_only_option",
              "excess.read_only_option",
              "nmp/non_modelled_perils_16/gross_el",
              "nmp/non_modelled_perils_16/loss_on_line",
              "nmp/non_modelled_perils_16/gross_sd",
              "nmp/non_modelled_perils_16/include_curve"
            ]}
              freezeLeft={0}
              kb-interactive={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Curve 17"
          shownBy="cds/non_modelled_perils_visual/show_curve_17">
          <HX.With context={{
            "index": 16,
            "path": "cds/non_modelled_perils",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Table data={[
                {
                  "datum": "curve_selections"
                }
              ]}
                fields={[
                "include_in_summary",
                "broker_pml",
                "peril",
                "description",
                {
                  "field": "curve",
                  "shownBy": "curve_selections/show_market_pml"
                },
                "rp",
                "loss",
                {
                  "field": "currency",
                  "shownBy": "/cds/show_intl_fields"
                }
              ]}
                transpose={true}
                kb-interactive={true} />
              <HX.Pane>
                <HX.Table data={[
                  "rp_labels",
                  {
                    "datum": "pml_broker",
                    "labelBy": "curve_selections/pml_broker_label"
                  },
                  {
                    "datum": "pml_market",
                    "labelBy": "curve_selections/pml_market_label"
                  },
                  "pml_final"
                ]}
                  fields={[
                  "rp_10000",
                  "rp_5000",
                  "rp_1000",
                  "rp_500",
                  "rp_250",
                  "rp_200",
                  "rp_100",
                  "rp_50",
                  "rp_25",
                  "rp_10",
                  "rp_5",
                  "rp_2"
                ]}
                  transpose={true}
                  kb-interactive={true} />
              </HX.Pane>
            </HX.Pane>
          </HX.With>
          <HX.Pane>
            <HX.Table data={[
              {
                "datum": "cds/layers"
              }
            ]}
              fields={[
              "limit.read_only_option",
              "excess.read_only_option",
              "nmp/non_modelled_perils_17/gross_el",
              "nmp/non_modelled_perils_17/loss_on_line",
              "nmp/non_modelled_perils_17/gross_sd",
              "nmp/non_modelled_perils_17/include_curve"
            ]}
              freezeLeft={0}
              kb-interactive={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Curve 18"
          shownBy="cds/non_modelled_perils_visual/show_curve_18">
          <HX.With context={{
            "index": 17,
            "path": "cds/non_modelled_perils",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Table data={[
                {
                  "datum": "curve_selections"
                }
              ]}
                fields={[
                "include_in_summary",
                "broker_pml",
                "peril",
                "description",
                {
                  "field": "curve",
                  "shownBy": "curve_selections/show_market_pml"
                },
                "rp",
                "loss",
                {
                  "field": "currency",
                  "shownBy": "/cds/show_intl_fields"
                }
              ]}
                transpose={true}
                kb-interactive={true} />
              <HX.Pane>
                <HX.Table data={[
                  "rp_labels",
                  {
                    "datum": "pml_broker",
                    "labelBy": "curve_selections/pml_broker_label"
                  },
                  {
                    "datum": "pml_market",
                    "labelBy": "curve_selections/pml_market_label"
                  },
                  "pml_final"
                ]}
                  fields={[
                  "rp_10000",
                  "rp_5000",
                  "rp_1000",
                  "rp_500",
                  "rp_250",
                  "rp_200",
                  "rp_100",
                  "rp_50",
                  "rp_25",
                  "rp_10",
                  "rp_5",
                  "rp_2"
                ]}
                  transpose={true}
                  kb-interactive={true} />
              </HX.Pane>
            </HX.Pane>
          </HX.With>
          <HX.Pane>
            <HX.Table data={[
              {
                "datum": "cds/layers"
              }
            ]}
              fields={[
              "limit.read_only_option",
              "excess.read_only_option",
              "nmp/non_modelled_perils_18/gross_el",
              "nmp/non_modelled_perils_18/loss_on_line",
              "nmp/non_modelled_perils_18/gross_sd",
              "nmp/non_modelled_perils_18/include_curve"
            ]}
              freezeLeft={0}
              kb-interactive={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Curve 19"
          shownBy="cds/non_modelled_perils_visual/show_curve_19">
          <HX.With context={{
            "index": 18,
            "path": "cds/non_modelled_perils",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Table data={[
                {
                  "datum": "curve_selections"
                }
              ]}
                fields={[
                "include_in_summary",
                "broker_pml",
                "peril",
                "description",
                {
                  "field": "curve",
                  "shownBy": "curve_selections/show_market_pml"
                },
                "rp",
                "loss",
                {
                  "field": "currency",
                  "shownBy": "/cds/show_intl_fields"
                }
              ]}
                transpose={true}
                kb-interactive={true} />
              <HX.Pane>
                <HX.Table data={[
                  "rp_labels",
                  {
                    "datum": "pml_broker",
                    "labelBy": "curve_selections/pml_broker_label"
                  },
                  {
                    "datum": "pml_market",
                    "labelBy": "curve_selections/pml_market_label"
                  },
                  "pml_final"
                ]}
                  fields={[
                  "rp_10000",
                  "rp_5000",
                  "rp_1000",
                  "rp_500",
                  "rp_250",
                  "rp_200",
                  "rp_100",
                  "rp_50",
                  "rp_25",
                  "rp_10",
                  "rp_5",
                  "rp_2"
                ]}
                  transpose={true}
                  kb-interactive={true} />
              </HX.Pane>
            </HX.Pane>
          </HX.With>
          <HX.Pane>
            <HX.Table data={[
              {
                "datum": "cds/layers"
              }
            ]}
              fields={[
              "limit.read_only_option",
              "excess.read_only_option",
              "nmp/non_modelled_perils_19/gross_el",
              "nmp/non_modelled_perils_19/loss_on_line",
              "nmp/non_modelled_perils_19/gross_sd",
              "nmp/non_modelled_perils_19/include_curve"
            ]}
              freezeLeft={0}
              kb-interactive={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Curve 20"
          shownBy="cds/non_modelled_perils_visual/show_curve_20">
          <HX.With context={{
            "index": 19,
            "path": "cds/non_modelled_perils",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Table data={[
                {
                  "datum": "curve_selections"
                }
              ]}
                fields={[
                "include_in_summary",
                "broker_pml",
                "peril",
                "description",
                {
                  "field": "curve",
                  "shownBy": "curve_selections/show_market_pml"
                },
                "rp",
                "loss",
                {
                  "field": "currency",
                  "shownBy": "/cds/show_intl_fields"
                }
              ]}
                transpose={true}
                kb-interactive={true} />
              <HX.Pane>
                <HX.Table data={[
                  "rp_labels",
                  {
                    "datum": "pml_broker",
                    "labelBy": "curve_selections/pml_broker_label"
                  },
                  {
                    "datum": "pml_market",
                    "labelBy": "curve_selections/pml_market_label"
                  },
                  "pml_final"
                ]}
                  fields={[
                  "rp_10000",
                  "rp_5000",
                  "rp_1000",
                  "rp_500",
                  "rp_250",
                  "rp_200",
                  "rp_100",
                  "rp_50",
                  "rp_25",
                  "rp_10",
                  "rp_5",
                  "rp_2"
                ]}
                  transpose={true}
                  kb-interactive={true} />
              </HX.Pane>
            </HX.Pane>
          </HX.With>
          <HX.Pane>
            <HX.Table data={[
              {
                "datum": "cds/layers"
              }
            ]}
              fields={[
              "limit.read_only_option",
              "excess.read_only_option",
              "nmp/non_modelled_perils_20/gross_el",
              "nmp/non_modelled_perils_20/loss_on_line",
              "nmp/non_modelled_perils_20/gross_sd",
              "nmp/non_modelled_perils_20/include_curve"
            ]}
              freezeLeft={0}
              kb-interactive={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Curve 21"
          shownBy="cds/non_modelled_perils_visual/show_curve_21">
          <HX.With context={{
            "index": 20,
            "path": "cds/non_modelled_perils",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Table data={[
                {
                  "datum": "curve_selections"
                }
              ]}
                fields={[
                "include_in_summary",
                "broker_pml",
                "peril",
                "description",
                {
                  "field": "curve",
                  "shownBy": "curve_selections/show_market_pml"
                },
                "rp",
                "loss",
                {
                  "field": "currency",
                  "shownBy": "/cds/show_intl_fields"
                }
              ]}
                transpose={true}
                kb-interactive={true} />
              <HX.Pane>
                <HX.Table data={[
                  "rp_labels",
                  {
                    "datum": "pml_broker",
                    "labelBy": "curve_selections/pml_broker_label"
                  },
                  {
                    "datum": "pml_market",
                    "labelBy": "curve_selections/pml_market_label"
                  },
                  "pml_final"
                ]}
                  fields={[
                  "rp_10000",
                  "rp_5000",
                  "rp_1000",
                  "rp_500",
                  "rp_250",
                  "rp_200",
                  "rp_100",
                  "rp_50",
                  "rp_25",
                  "rp_10",
                  "rp_5",
                  "rp_2"
                ]}
                  transpose={true}
                  kb-interactive={true} />
              </HX.Pane>
            </HX.Pane>
          </HX.With>
          <HX.Pane>
            <HX.Table data={[
              {
                "datum": "cds/layers"
              }
            ]}
              fields={[
              "limit.read_only_option",
              "excess.read_only_option",
              "nmp/non_modelled_perils_21/gross_el",
              "nmp/non_modelled_perils_21/loss_on_line",
              "nmp/non_modelled_perils_21/gross_sd",
              "nmp/non_modelled_perils_21/include_curve"
            ]}
              freezeLeft={0}
              kb-interactive={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Curve 22"
          shownBy="cds/non_modelled_perils_visual/show_curve_22">
          <HX.With context={{
            "index": 21,
            "path": "cds/non_modelled_perils",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Table data={[
                {
                  "datum": "curve_selections"
                }
              ]}
                fields={[
                "include_in_summary",
                "broker_pml",
                "peril",
                "description",
                {
                  "field": "curve",
                  "shownBy": "curve_selections/show_market_pml"
                },
                "rp",
                "loss",
                {
                  "field": "currency",
                  "shownBy": "/cds/show_intl_fields"
                }
              ]}
                transpose={true}
                kb-interactive={true} />
              <HX.Pane>
                <HX.Table data={[
                  "rp_labels",
                  {
                    "datum": "pml_broker",
                    "labelBy": "curve_selections/pml_broker_label"
                  },
                  {
                    "datum": "pml_market",
                    "labelBy": "curve_selections/pml_market_label"
                  },
                  "pml_final"
                ]}
                  fields={[
                  "rp_10000",
                  "rp_5000",
                  "rp_1000",
                  "rp_500",
                  "rp_250",
                  "rp_200",
                  "rp_100",
                  "rp_50",
                  "rp_25",
                  "rp_10",
                  "rp_5",
                  "rp_2"
                ]}
                  transpose={true}
                  kb-interactive={true} />
              </HX.Pane>
            </HX.Pane>
          </HX.With>
          <HX.Pane>
            <HX.Table data={[
              {
                "datum": "cds/layers"
              }
            ]}
              fields={[
              "limit.read_only_option",
              "excess.read_only_option",
              "nmp/non_modelled_perils_22/gross_el",
              "nmp/non_modelled_perils_22/loss_on_line",
              "nmp/non_modelled_perils_22/gross_sd",
              "nmp/non_modelled_perils_22/include_curve"
            ]}
              freezeLeft={0}
              kb-interactive={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Curve 23"
          shownBy="cds/non_modelled_perils_visual/show_curve_23">
          <HX.With context={{
            "index": 22,
            "path": "cds/non_modelled_perils",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Table data={[
                {
                  "datum": "curve_selections"
                }
              ]}
                fields={[
                "include_in_summary",
                "broker_pml",
                "peril",
                "description",
                {
                  "field": "curve",
                  "shownBy": "curve_selections/show_market_pml"
                },
                "rp",
                "loss",
                {
                  "field": "currency",
                  "shownBy": "/cds/show_intl_fields"
                }
              ]}
                transpose={true}
                kb-interactive={true} />
              <HX.Pane>
                <HX.Table data={[
                  "rp_labels",
                  {
                    "datum": "pml_broker",
                    "labelBy": "curve_selections/pml_broker_label"
                  },
                  {
                    "datum": "pml_market",
                    "labelBy": "curve_selections/pml_market_label"
                  },
                  "pml_final"
                ]}
                  fields={[
                  "rp_10000",
                  "rp_5000",
                  "rp_1000",
                  "rp_500",
                  "rp_250",
                  "rp_200",
                  "rp_100",
                  "rp_50",
                  "rp_25",
                  "rp_10",
                  "rp_5",
                  "rp_2"
                ]}
                  transpose={true}
                  kb-interactive={true} />
              </HX.Pane>
            </HX.Pane>
          </HX.With>
          <HX.Pane>
            <HX.Table data={[
              {
                "datum": "cds/layers"
              }
            ]}
              fields={[
              "limit.read_only_option",
              "excess.read_only_option",
              "nmp/non_modelled_perils_23/gross_el",
              "nmp/non_modelled_perils_23/loss_on_line",
              "nmp/non_modelled_perils_23/gross_sd",
              "nmp/non_modelled_perils_23/include_curve"
            ]}
              freezeLeft={0}
              kb-interactive={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Curve 24"
          shownBy="cds/non_modelled_perils_visual/show_curve_24">
          <HX.With context={{
            "index": 23,
            "path": "cds/non_modelled_perils",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Table data={[
                {
                  "datum": "curve_selections"
                }
              ]}
                fields={[
                "include_in_summary",
                "broker_pml",
                "peril",
                "description",
                {
                  "field": "curve",
                  "shownBy": "curve_selections/show_market_pml"
                },
                "rp",
                "loss",
                {
                  "field": "currency",
                  "shownBy": "/cds/show_intl_fields"
                }
              ]}
                transpose={true}
                kb-interactive={true} />
              <HX.Pane>
                <HX.Table data={[
                  "rp_labels",
                  {
                    "datum": "pml_broker",
                    "labelBy": "curve_selections/pml_broker_label"
                  },
                  {
                    "datum": "pml_market",
                    "labelBy": "curve_selections/pml_market_label"
                  },
                  "pml_final"
                ]}
                  fields={[
                  "rp_10000",
                  "rp_5000",
                  "rp_1000",
                  "rp_500",
                  "rp_250",
                  "rp_200",
                  "rp_100",
                  "rp_50",
                  "rp_25",
                  "rp_10",
                  "rp_5",
                  "rp_2"
                ]}
                  transpose={true}
                  kb-interactive={true} />
              </HX.Pane>
            </HX.Pane>
          </HX.With>
          <HX.Pane>
            <HX.Table data={[
              {
                "datum": "cds/layers"
              }
            ]}
              fields={[
              "limit.read_only_option",
              "excess.read_only_option",
              "nmp/non_modelled_perils_24/gross_el",
              "nmp/non_modelled_perils_24/loss_on_line",
              "nmp/non_modelled_perils_24/gross_sd",
              "nmp/non_modelled_perils_24/include_curve"
            ]}
              freezeLeft={0}
              kb-interactive={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Curve 25"
          shownBy="cds/non_modelled_perils_visual/show_curve_25">
          <HX.With context={{
            "index": 24,
            "path": "cds/non_modelled_perils",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Table data={[
                {
                  "datum": "curve_selections"
                }
              ]}
                fields={[
                "include_in_summary",
                "broker_pml",
                "peril",
                "description",
                {
                  "field": "curve",
                  "shownBy": "curve_selections/show_market_pml"
                },
                "rp",
                "loss",
                {
                  "field": "currency",
                  "shownBy": "/cds/show_intl_fields"
                }
              ]}
                transpose={true}
                kb-interactive={true} />
              <HX.Pane>
                <HX.Table data={[
                  "rp_labels",
                  {
                    "datum": "pml_broker",
                    "labelBy": "curve_selections/pml_broker_label"
                  },
                  {
                    "datum": "pml_market",
                    "labelBy": "curve_selections/pml_market_label"
                  },
                  "pml_final"
                ]}
                  fields={[
                  "rp_10000",
                  "rp_5000",
                  "rp_1000",
                  "rp_500",
                  "rp_250",
                  "rp_200",
                  "rp_100",
                  "rp_50",
                  "rp_25",
                  "rp_10",
                  "rp_5",
                  "rp_2"
                ]}
                  transpose={true}
                  kb-interactive={true} />
              </HX.Pane>
            </HX.Pane>
          </HX.With>
          <HX.Pane>
            <HX.Table data={[
              {
                "datum": "cds/layers"
              }
            ]}
              fields={[
              "limit.read_only_option",
              "excess.read_only_option",
              "nmp/non_modelled_perils_25/gross_el",
              "nmp/non_modelled_perils_25/loss_on_line",
              "nmp/non_modelled_perils_25/gross_sd",
              "nmp/non_modelled_perils_25/include_curve"
            ]}
              freezeLeft={0}
              kb-interactive={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Curve 26"
          shownBy="cds/non_modelled_perils_visual/show_curve_26">
          <HX.With context={{
            "index": 25,
            "path": "cds/non_modelled_perils",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Table data={[
                {
                  "datum": "curve_selections"
                }
              ]}
                fields={[
                "include_in_summary",
                "broker_pml",
                "peril",
                "description",
                {
                  "field": "curve",
                  "shownBy": "curve_selections/show_market_pml"
                },
                "rp",
                "loss",
                {
                  "field": "currency",
                  "shownBy": "/cds/show_intl_fields"
                }
              ]}
                transpose={true}
                kb-interactive={true} />
              <HX.Pane>
                <HX.Table data={[
                  "rp_labels",
                  {
                    "datum": "pml_broker",
                    "labelBy": "curve_selections/pml_broker_label"
                  },
                  {
                    "datum": "pml_market",
                    "labelBy": "curve_selections/pml_market_label"
                  },
                  "pml_final"
                ]}
                  fields={[
                  "rp_10000",
                  "rp_5000",
                  "rp_1000",
                  "rp_500",
                  "rp_250",
                  "rp_200",
                  "rp_100",
                  "rp_50",
                  "rp_25",
                  "rp_10",
                  "rp_5",
                  "rp_2"
                ]}
                  transpose={true}
                  kb-interactive={true} />
              </HX.Pane>
            </HX.Pane>
          </HX.With>
          <HX.Pane>
            <HX.Table data={[
              {
                "datum": "cds/layers"
              }
            ]}
              fields={[
              "limit.read_only_option",
              "excess.read_only_option",
              "nmp/non_modelled_perils_26/gross_el",
              "nmp/non_modelled_perils_26/loss_on_line",
              "nmp/non_modelled_perils_26/gross_sd",
              "nmp/non_modelled_perils_26/include_curve"
            ]}
              freezeLeft={0}
              kb-interactive={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Curve 27"
          shownBy="cds/non_modelled_perils_visual/show_curve_27">
          <HX.With context={{
            "index": 26,
            "path": "cds/non_modelled_perils",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Table data={[
                {
                  "datum": "curve_selections"
                }
              ]}
                fields={[
                "include_in_summary",
                "broker_pml",
                "peril",
                "description",
                {
                  "field": "curve",
                  "shownBy": "curve_selections/show_market_pml"
                },
                "rp",
                "loss",
                {
                  "field": "currency",
                  "shownBy": "/cds/show_intl_fields"
                }
              ]}
                transpose={true}
                kb-interactive={true} />
              <HX.Pane>
                <HX.Table data={[
                  "rp_labels",
                  {
                    "datum": "pml_broker",
                    "labelBy": "curve_selections/pml_broker_label"
                  },
                  {
                    "datum": "pml_market",
                    "labelBy": "curve_selections/pml_market_label"
                  },
                  "pml_final"
                ]}
                  fields={[
                  "rp_10000",
                  "rp_5000",
                  "rp_1000",
                  "rp_500",
                  "rp_250",
                  "rp_200",
                  "rp_100",
                  "rp_50",
                  "rp_25",
                  "rp_10",
                  "rp_5",
                  "rp_2"
                ]}
                  transpose={true}
                  kb-interactive={true} />
              </HX.Pane>
            </HX.Pane>
          </HX.With>
          <HX.Pane>
            <HX.Table data={[
              {
                "datum": "cds/layers"
              }
            ]}
              fields={[
              "limit.read_only_option",
              "excess.read_only_option",
              "nmp/non_modelled_perils_27/gross_el",
              "nmp/non_modelled_perils_27/loss_on_line",
              "nmp/non_modelled_perils_27/gross_sd",
              "nmp/non_modelled_perils_27/include_curve"
            ]}
              freezeLeft={0}
              kb-interactive={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Curve 28"
          shownBy="cds/non_modelled_perils_visual/show_curve_28">
          <HX.With context={{
            "index": 27,
            "path": "cds/non_modelled_perils",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Table data={[
                {
                  "datum": "curve_selections"
                }
              ]}
                fields={[
                "include_in_summary",
                "broker_pml",
                "peril",
                "description",
                {
                  "field": "curve",
                  "shownBy": "curve_selections/show_market_pml"
                },
                "rp",
                "loss",
                {
                  "field": "currency",
                  "shownBy": "/cds/show_intl_fields"
                }
              ]}
                transpose={true}
                kb-interactive={true} />
              <HX.Pane>
                <HX.Table data={[
                  "rp_labels",
                  {
                    "datum": "pml_broker",
                    "labelBy": "curve_selections/pml_broker_label"
                  },
                  {
                    "datum": "pml_market",
                    "labelBy": "curve_selections/pml_market_label"
                  },
                  "pml_final"
                ]}
                  fields={[
                  "rp_10000",
                  "rp_5000",
                  "rp_1000",
                  "rp_500",
                  "rp_250",
                  "rp_200",
                  "rp_100",
                  "rp_50",
                  "rp_25",
                  "rp_10",
                  "rp_5",
                  "rp_2"
                ]}
                  transpose={true}
                  kb-interactive={true} />
              </HX.Pane>
            </HX.Pane>
          </HX.With>
          <HX.Pane>
            <HX.Table data={[
              {
                "datum": "cds/layers"
              }
            ]}
              fields={[
              "limit.read_only_option",
              "excess.read_only_option",
              "nmp/non_modelled_perils_28/gross_el",
              "nmp/non_modelled_perils_28/loss_on_line",
              "nmp/non_modelled_perils_28/gross_sd",
              "nmp/non_modelled_perils_28/include_curve"
            ]}
              freezeLeft={0}
              kb-interactive={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Curve 29"
          shownBy="cds/non_modelled_perils_visual/show_curve_29">
          <HX.With context={{
            "index": 28,
            "path": "cds/non_modelled_perils",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Table data={[
                {
                  "datum": "curve_selections"
                }
              ]}
                fields={[
                "include_in_summary",
                "broker_pml",
                "peril",
                "description",
                {
                  "field": "curve",
                  "shownBy": "curve_selections/show_market_pml"
                },
                "rp",
                "loss",
                {
                  "field": "currency",
                  "shownBy": "/cds/show_intl_fields"
                }
              ]}
                transpose={true}
                kb-interactive={true} />
              <HX.Pane>
                <HX.Table data={[
                  "rp_labels",
                  {
                    "datum": "pml_broker",
                    "labelBy": "curve_selections/pml_broker_label"
                  },
                  {
                    "datum": "pml_market",
                    "labelBy": "curve_selections/pml_market_label"
                  },
                  "pml_final"
                ]}
                  fields={[
                  "rp_10000",
                  "rp_5000",
                  "rp_1000",
                  "rp_500",
                  "rp_250",
                  "rp_200",
                  "rp_100",
                  "rp_50",
                  "rp_25",
                  "rp_10",
                  "rp_5",
                  "rp_2"
                ]}
                  transpose={true}
                  kb-interactive={true} />
              </HX.Pane>
            </HX.Pane>
          </HX.With>
          <HX.Pane>
            <HX.Table data={[
              {
                "datum": "cds/layers"
              }
            ]}
              fields={[
              "limit.read_only_option",
              "excess.read_only_option",
              "nmp/non_modelled_perils_29/gross_el",
              "nmp/non_modelled_perils_29/loss_on_line",
              "nmp/non_modelled_perils_29/gross_sd",
              "nmp/non_modelled_perils_29/include_curve"
            ]}
              freezeLeft={0}
              kb-interactive={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Curve 30"
          shownBy="cds/non_modelled_perils_visual/show_curve_30">
          <HX.With context={{
            "index": 29,
            "path": "cds/non_modelled_perils",
            "type": "list"
          }}>
            <HX.Pane flow="right">
              <HX.Table data={[
                {
                  "datum": "curve_selections"
                }
              ]}
                fields={[
                "include_in_summary",
                "broker_pml",
                "peril",
                "description",
                {
                  "field": "curve",
                  "shownBy": "curve_selections/show_market_pml"
                },
                "rp",
                "loss",
                {
                  "field": "currency",
                  "shownBy": "/cds/show_intl_fields"
                }
              ]}
                transpose={true}
                kb-interactive={true} />
              <HX.Pane>
                <HX.Table data={[
                  "rp_labels",
                  {
                    "datum": "pml_broker",
                    "labelBy": "curve_selections/pml_broker_label"
                  },
                  {
                    "datum": "pml_market",
                    "labelBy": "curve_selections/pml_market_label"
                  },
                  "pml_final"
                ]}
                  fields={[
                  "rp_10000",
                  "rp_5000",
                  "rp_1000",
                  "rp_500",
                  "rp_250",
                  "rp_200",
                  "rp_100",
                  "rp_50",
                  "rp_25",
                  "rp_10",
                  "rp_5",
                  "rp_2"
                ]}
                  transpose={true}
                  kb-interactive={true} />
              </HX.Pane>
            </HX.Pane>
          </HX.With>
          <HX.Pane>
            <HX.Table data={[
              {
                "datum": "cds/layers"
              }
            ]}
              fields={[
              "limit.read_only_option",
              "excess.read_only_option",
              "nmp/non_modelled_perils_30/gross_el",
              "nmp/non_modelled_perils_30/loss_on_line",
              "nmp/non_modelled_perils_30/gross_sd",
              "nmp/non_modelled_perils_30/include_curve"
            ]}
              freezeLeft={0}
              kb-interactive={true} />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Modelling"
        fullWidth={true}
        viewScale={0.7}
        shownBy="cds/show_non_risk_xl">
        <HX.Section title="Modelling Results">
          <HX.Pane flow="right"
            reflow={false}>
            <HX.Pane ratio={8}>
              <HX.Notes field="cds/modelling_account_level/comments"
                title="Comments" />
            </HX.Pane>
            <HX.Pane ratio={5}
              flow="right"
              reflow={false}>
              <HX.Pane ratio={1} />
              <HX.Pane ratio={1}>
                <HX.Button task="rms_el_allocation_task"
                  title="Run RMS EL Allocation Task" />
                <HX.Collection numCols={1}
                  fields={[
                  "cds/send_rate_change/confirm_rms_el_allocation"
                ]} />
              </HX.Pane>
            </HX.Pane>
            <HX.Pane ratio={2}>
              <HX.Collection fields={[
                null,
                "cds/modelling_account_level/ivor_nmp_selection"
              ]}
                stretch={true} />
            </HX.Pane>
            <HX.Pane ratio={2} />
            <HX.Pane ratio={4} />
          </HX.Pane>
          <HX.Pane flow="right"
            reflow={false}>
            <HX.Pane flow="right"
              reflow={false}
              ratio={3}>
              <HX.Table title="This Year                                                              RMS + NMP (In Application CCY)"
                syncColumnWidthsKey="rms_nmp_table"
                data={[
                {
                  "datum": "cds/layers"
                }
              ]}
                fields={[
                {
                  "field": "layer_structure",
                  "width": 200
                },
                null,
                {
                  "field": "model/total_rms_nmp/gross_el"
                },
                {
                  "field": "model/total_rms_nmp/gross_sd"
                },
                {
                  "field": "model/total_rms_nmp/change_el"
                }
              ]}
                freezeLeft={0}
                kb-interactive={true} />
            </HX.Pane>
            <HX.Pane flow="right"
              reflow={false}
              ratio={5}>
              <HX.Table title="IVOR + NMP (In Application CCY)"
                syncColumnWidthsKey="ivor_nmp_table"
                data={[
                {
                  "datum": "cds/layers"
                }
              ]}
                fields={[
                {
                  "field": "model/total_ivor_nmp/gross_el"
                },
                {
                  "field": "model/total_ivor_nmp/gross_sd"
                },
                {
                  "field": "model/total_ivor_nmp/change_el"
                }
              ]}
                freezeLeft={0}
                kb-interactive={true} />
              <HX.Table title="AIR + NMP (In Application CCY)"
                syncColumnWidthsKey="air_nmp_table"
                data={[
                {
                  "datum": "cds/layers"
                }
              ]}
                fields={[
                {
                  "field": "model/total_air_nmp/gross_el"
                },
                {
                  "field": "model/total_air_nmp/gross_sd"
                },
                {
                  "field": "model/total_air_nmp/change_el"
                }
              ]}
                freezeLeft={0}
                kb-interactive={true} />
            </HX.Pane>
            <HX.Pane flow="right"
              reflow={false}
              ratio={5}>
              <HX.Table title="RMS"
                syncColumnWidthsKey="rms_table"
                data={[
                {
                  "datum": "cds/layers"
                }
              ]}
                fields={[
                {
                  "field": "model/rms/gross_el"
                },
                {
                  "field": "model/rms/gross_sd"
                },
                {
                  "field": "model/rms/change_el"
                },
                {
                  "field": "model/rms/eq_el",
                  "shownBy": "/cds/show_us_fields"
                },
                {
                  "field": "model/rms/ws_el",
                  "shownBy": "/cds/show_us_fields"
                },
                {
                  "field": "model/rms/scs_el",
                  "shownBy": "/cds/show_us_fields"
                },
                {
                  "field": "model/rms/eu_ws_el",
                  "shownBy": "/cds/show_intl_fields"
                },
                {
                  "field": "model/rms/jp_eq_el",
                  "shownBy": "/cds/show_intl_fields"
                },
                {
                  "field": "model/rms/jp_ws_el",
                  "shownBy": "/cds/show_intl_fields"
                },
                {
                  "field": "model/rms/can_eq_el",
                  "shownBy": "/cds/show_intl_fields"
                },
                {
                  "field": "model/rms/caribbean_ws_el",
                  "shownBy": "/cds/show_intl_fields"
                },
                null,
                {
                  "field": "model/rms/perc_us_el",
                  "shownBy": "/cds/show_perc_us_el"
                }
              ]}
                freezeLeft={0}
                kb-interactive={true} />
            </HX.Pane>
            <HX.Pane flow="right"
              reflow={false}
              ratio={2}>
              <HX.Table title="IVOR"
                syncColumnWidthsKey="ivor_table"
                data={[
                {
                  "datum": "cds/layers"
                }
              ]}
                fields={[
                {
                  "field": "model/ivor/gross_el"
                },
                {
                  "field": "model/ivor/gross_sd"
                }
              ]}
                freezeLeft={0}
                kb-interactive={true} />
            </HX.Pane>
            <HX.Pane reflow={false}
              ratio={2}>
              <HX.Table title="AIR"
                syncColumnWidthsKey="air_table"
                data={[
                {
                  "datum": "cds/layers"
                }
              ]}
                fields={[
                {
                  "field": "model/air/gross_el"
                },
                {
                  "field": "model/air/gross_sd"
                },
                {
                  "field": "model/total_air_nmp/change_el"
                }
              ]}
                freezeLeft={0}
                kb-interactive={true} />
            </HX.Pane>
            <HX.Pane flow="right"
              reflow={false}
              ratio={4}>
              <HX.Table title="NMP"
                syncColumnWidthsKey="nmp_table"
                data={[
                {
                  "datum": "cds/layers"
                }
              ]}
                fields={[
                {
                  "field": "model/nmp/gross_el_incl_rol"
                },
                {
                  "field": "model/nmp/gross_sd_incl_rol"
                },
                {
                  "field": "model/nmp/gross_el"
                },
                {
                  "field": "model/nmp/gross_sd"
                },
                {
                  "field": "model/nmp/additional_rol"
                },
                {
                  "field": "model/nmp/description"
                }
              ]}
                freezeLeft={0}
                kb-interactive={true} />
            </HX.Pane>
          </HX.Pane>
          <HX.Pane flow="right"
            reflow={false}>
            <HX.Pane flow="right"
              reflow={false}
              ratio={3}>
              <HX.Table title="Previous Year                                                   RMS + NMP (In Application CCY)"
                syncColumnWidthsKey="rms_nmp_table"
                data={[
                {
                  "datum": "cds/layers"
                }
              ]}
                fields={[
                {
                  "field": "layer_structure_ly"
                },
                null,
                {
                  "field": "model_prev/total_rms_nmp/gross_el"
                },
                {
                  "field": "model_prev/total_rms_nmp/gross_sd"
                }
              ]}
                freezeLeft={0}
                kb-interactive={true} />
            </HX.Pane>
            <HX.Pane flow="right"
              reflow={false}
              ratio={5}>
              <HX.Table title="IVOR + NMP (In Application CCY)"
                syncColumnWidthsKey="ivor_nmp_table"
                data={[
                {
                  "datum": "cds/layers"
                }
              ]}
                fields={[
                {
                  "field": "model_prev/total_ivor_nmp/gross_el"
                },
                {
                  "field": "model_prev/total_ivor_nmp/gross_sd"
                }
              ]}
                freezeLeft={0}
                kb-interactive={true} />
              <HX.Table title="AIR + NMP (In Application CCY)"
                syncColumnWidthsKey="air_nmp_table"
                data={[
                {
                  "datum": "cds/layers"
                }
              ]}
                fields={[
                {
                  "field": "model_prev/total_air_nmp/gross_el"
                },
                {
                  "field": "model_prev/total_air_nmp/gross_sd"
                }
              ]}
                freezeLeft={0}
                kb-interactive={true} />
            </HX.Pane>
            <HX.Pane flow="right"
              reflow={false}
              ratio={5}>
              <HX.Table title="RMS"
                syncColumnWidthsKey="rms_table"
                data={[
                {
                  "datum": "cds/layers"
                }
              ]}
                fields={[
                {
                  "field": "model_prev/rms/gross_el"
                },
                {
                  "field": "model_prev/rms/gross_sd"
                },
                null,
                {
                  "field": "model_prev/rms/eq_el",
                  "shownBy": "/cds/show_us_fields"
                },
                {
                  "field": "model_prev/rms/ws_el",
                  "shownBy": "/cds/show_us_fields"
                },
                {
                  "field": "model_prev/rms/scs_el",
                  "shownBy": "/cds/show_us_fields"
                },
                {
                  "field": "model_prev/rms/eu_ws_el",
                  "shownBy": "/cds/show_intl_fields"
                },
                {
                  "field": "model_prev/rms/jp_eq_el",
                  "shownBy": "/cds/show_intl_fields"
                },
                {
                  "field": "model_prev/rms/jp_ws_el",
                  "shownBy": "/cds/show_intl_fields"
                },
                {
                  "field": "model_prev/rms/can_eq_el",
                  "shownBy": "/cds/show_intl_fields"
                },
                {
                  "field": "model_prev/rms/caribbean_ws_el",
                  "shownBy": "/cds/show_intl_fields"
                },
                null,
                {
                  "field": "model_prev/rms/perc_us_el",
                  "shownBy": "/cds/show_perc_us_el"
                }
              ]}
                freezeLeft={0}
                kb-interactive={true} />
            </HX.Pane>
            <HX.Pane flow="right"
              reflow={false}
              ratio={2}>
              <HX.Table title="IVOR"
                syncColumnWidthsKey="ivor_table"
                data={[
                {
                  "datum": "cds/layers"
                }
              ]}
                fields={[
                {
                  "field": "model_prev/ivor/gross_el"
                },
                {
                  "field": "model_prev/ivor/gross_sd"
                }
              ]}
                freezeLeft={0}
                kb-interactive={true} />
            </HX.Pane>
            <HX.Pane reflow={false}
              ratio={2}>
              <HX.Table title="AIR"
                syncColumnWidthsKey="air_table"
                data={[
                {
                  "datum": "cds/layers"
                }
              ]}
                fields={[
                {
                  "field": "model_prev/air/gross_el"
                },
                {
                  "field": "model_prev/air/gross_sd"
                }
              ]}
                freezeLeft={0}
                kb-interactive={true} />
            </HX.Pane>
            <HX.Pane flow="right"
              reflow={false}
              ratio={4}>
              <HX.Table title="NMP"
                syncColumnWidthsKey="nmp_table"
                data={[
                {
                  "datum": "cds/layers"
                }
              ]}
                fields={[
                {
                  "field": "model_prev/nmp/gross_el_incl_rol"
                },
                {
                  "field": "model_prev/nmp/gross_sd_incl_rol"
                },
                {
                  "field": "model_prev/nmp/gross_el"
                },
                {
                  "field": "model_prev/nmp/gross_sd"
                },
                {
                  "field": "model_prev/nmp/additional_rol"
                },
                {
                  "field": "model_prev/nmp/description"
                }
              ]}
                freezeLeft={0}
                kb-interactive={true} />
            </HX.Pane>
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Cedant RDS Gross Losses"
          shownBy="cds/show_us_exposure_fields">
          <HX.Table with="cds/modelling_account_level/rds_gross_loss"
            data={[
            "this_year",
            "previous_year",
            "yoy_growth"
          ]}
            fields={[
            {
              "field": "carolinas_ws",
              "width": 200
            },
            {
              "field": "miami_dade_ws",
              "width": 200
            },
            {
              "field": "gulf_ws",
              "width": 200
            },
            {
              "field": "ne_ws",
              "width": 200
            },
            {
              "field": "fl_pinnelas_ws",
              "width": 200
            },
            {
              "field": "la_eq",
              "width": 200
            },
            {
              "field": "nm_eq",
              "width": 200
            },
            {
              "field": "nm_stress_eq",
              "width": 200
            },
            {
              "field": "sf_eq",
              "width": 200
            }
          ]}
            kb-interactive={true} />
        </HX.Section>
        <HX.Section title="RMS Regional Entries"
          shownBy="cds/show_us_exposure_fields">
          <HX.Table title="This Year"
            data={[
            {
              "datum": "cds/layers"
            }
          ]}
            fields={[
            {
              "field": "rms_regional/north_east",
              "width": 150
            },
            {
              "field": "rms_regional/mid_atlantic",
              "width": 150
            },
            {
              "field": "rms_regional/carolinas",
              "width": 150
            },
            {
              "field": "rms_regional/fl_se",
              "width": 150
            },
            {
              "field": "rms_regional/fl_non_se",
              "width": 150
            },
            {
              "field": "rms_regional/al_miss",
              "width": 150
            },
            {
              "field": "rms_regional/louisiana",
              "width": 150
            },
            {
              "field": "rms_regional/tx_east",
              "width": 150
            },
            {
              "field": "rms_regional/tx_west",
              "width": 150
            },
            {
              "field": "rms_regional/cal_south",
              "width": 150
            },
            {
              "field": "rms_regional/cal_north",
              "width": 150
            },
            {
              "field": "rms_regional/pnw",
              "width": 150
            },
            {
              "field": "rms_regional/new_madrid",
              "width": 150
            },
            {
              "field": "rms_regional/hawaii",
              "width": 150
            },
            null,
            {
              "field": "rms_regional/mid_west_1",
              "width": 150
            },
            {
              "field": "rms_regional/mid_west_2",
              "width": 150
            },
            {
              "field": "rms_regional/second_event",
              "width": 150
            },
            {
              "field": "rms_regional/ca_wildfire",
              "width": 150
            }
          ]}
            removeHorizontalScroll={true}
            kb-interactive={true} />
          <HX.Table title="Previous Year"
            data={[
            {
              "datum": "cds/layers"
            }
          ]}
            fields={[
            {
              "field": "rms_regional_prev/north_east",
              "width": 150
            },
            {
              "field": "rms_regional_prev/mid_atlantic",
              "width": 150
            },
            {
              "field": "rms_regional_prev/carolinas",
              "width": 150
            },
            {
              "field": "rms_regional_prev/fl_se",
              "width": 150
            },
            {
              "field": "rms_regional_prev/fl_non_se",
              "width": 150
            },
            {
              "field": "rms_regional_prev/al_miss",
              "width": 150
            },
            {
              "field": "rms_regional_prev/louisiana",
              "width": 150
            },
            {
              "field": "rms_regional_prev/tx_east",
              "width": 150
            },
            {
              "field": "rms_regional_prev/tx_west",
              "width": 150
            },
            {
              "field": "rms_regional_prev/cal_south",
              "width": 150
            },
            {
              "field": "rms_regional_prev/cal_north",
              "width": 150
            },
            {
              "field": "rms_regional_prev/pnw",
              "width": 150
            },
            {
              "field": "rms_regional_prev/new_madrid",
              "width": 150
            },
            {
              "field": "rms_regional_prev/hawaii",
              "width": 150
            },
            null,
            {
              "field": "rms_regional_prev/mid_west_1",
              "width": 150
            },
            {
              "field": "rms_regional_prev/mid_west_2",
              "width": 150
            },
            {
              "field": "rms_regional_prev/second_event",
              "width": 150
            },
            {
              "field": "rms_regional_prev/ca_wildfire",
              "width": 150
            }
          ]}
            removeHorizontalScroll={true}
            kb-interactive={true} />
        </HX.Section>
        <HX.Section title="Marginal Impacts">
          <HX.Pane flow="right"
            reflow={false}>
            <HX.Pane ratio={3}>
              <HX.Pane flow="right"
                reflow={false}>
                <HX.Table title="Treaty US marginal portfolio impact"
                  data={[
                  {
                    "datum": "cds/layers"
                  }
                ]}
                  fields={[
                  {
                    "field": "marginal_impacts/treaty_us/mi_250"
                  },
                  {
                    "field": "marginal_impacts/treaty_us/mi_10"
                  }
                ]}
                  freezeLeft={0}
                  kb-interactive={true} />
                <HX.Table title="Treaty Group marginal portfolio impact"
                  data={[
                  {
                    "datum": "cds/layers"
                  }
                ]}
                  fields={[
                  {
                    "field": "marginal_impacts/treaty_group/mi_250"
                  },
                  {
                    "field": "marginal_impacts/treaty_group/mi_10"
                  }
                ]}
                  freezeLeft={0}
                  kb-interactive={true} />
                <HX.Table title="Treaty US Quake marginal portfolio impact"
                  data={[
                  {
                    "datum": "cds/layers"
                  }
                ]}
                  fields={[
                  {
                    "field": "marginal_impacts/treaty_us_quake/mi_250"
                  },
                  {
                    "field": "marginal_impacts/treaty_us_quake/mi_10"
                  }
                ]}
                  freezeLeft={0}
                  kb-interactive={true} />
                <HX.Table title="Treaty Intl marginal portfolio impact"
                  data={[
                  {
                    "datum": "cds/layers"
                  }
                ]}
                  fields={[
                  {
                    "field": "marginal_impacts/treaty_intl/mi_250"
                  },
                  {
                    "field": "marginal_impacts/treaty_intl/mi_10"
                  }
                ]}
                  freezeLeft={0}
                  kb-interactive={true} />
              </HX.Pane>
              <HX.Pane flow="right"
                reflow={false}>
                <HX.Table title="Treaty US marginal portfolio impact"
                  data={[
                  {
                    "datum": "cds/layers"
                  }
                ]}
                  fields={[
                  {
                    "field": "marginal_impacts_prev/treaty_us/mi_250"
                  },
                  {
                    "field": "marginal_impacts_prev/treaty_us/mi_10"
                  }
                ]}
                  freezeLeft={0}
                  kb-interactive={true} />
                <HX.Table title="Treaty Group marginal portfolio impact"
                  data={[
                  {
                    "datum": "cds/layers"
                  }
                ]}
                  fields={[
                  {
                    "field": "marginal_impacts_prev/treaty_group/mi_250"
                  },
                  {
                    "field": "marginal_impacts_prev/treaty_group/mi_10"
                  }
                ]}
                  freezeLeft={0}
                  kb-interactive={true} />
                <HX.Table title="Treaty US Quake marginal portfolio impact"
                  data={[
                  {
                    "datum": "cds/layers"
                  }
                ]}
                  fields={[
                  {
                    "field": "marginal_impacts_prev/treaty_us_quake/mi_250"
                  },
                  {
                    "field": "marginal_impacts_prev/treaty_us_quake/mi_10"
                  }
                ]}
                  freezeLeft={0}
                  kb-interactive={true} />
                <HX.Table title="Treaty Intl marginal portfolio impact"
                  data={[
                  {
                    "datum": "cds/layers"
                  }
                ]}
                  fields={[
                  {
                    "field": "marginal_impacts_prev/treaty_intl/mi_250"
                  },
                  {
                    "field": "marginal_impacts_prev/treaty_intl/mi_10"
                  }
                ]}
                  freezeLeft={0}
                  kb-interactive={true} />
              </HX.Pane>
            </HX.Pane>
            <HX.Pane ratio={1} />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Aggregates"
        fullWidth={true}
        viewScale={0.7}
        shownBy="cds/show_non_risk_xl">
        <HX.Section title="Mandatory Details">
          <HX.Pane flow="right"
            reflow={false}>
            <HX.Pane ratio={3}>
              <HX.Pane flow="right"
                reflow={false}>
                <HX.Pane ratio={1}>
                  <HX.Collection fields={[
                    "cds/exposure/aggregate/exposure_measure"
                  ]} />
                </HX.Pane>
                <HX.Pane ratio={3}>
                  <HX.Notes stretch={true}
                    field="cds/exposure/aggregate/exposure_comments"
                    title="Comments" />
                </HX.Pane>
              </HX.Pane>
            </HX.Pane>
            <HX.Pane ratio={4}>
              <HX.Table with="cds/exposure/aggregate"
                data={[
                "ly_aggregates",
                "ty_aggregates",
                null,
                "value_change",
                "perc_change"
              ]}
                fields={[
                {
                  "field": "exposure_total"
                },
                {
                  "field": "bespoke_total"
                },
                {
                  "field": "key_zone_total"
                }
              ]}
                kb-interactive={true}
                freezeLeft={0}
                transpose={true} />
            </HX.Pane>
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Aggregate Entry">
          <HX.Pane>
            <HX.Table data={[
              "cds/exposure/granular/exposures"
            ]}
              fields={[
              {
                "field": "peril"
              },
              {
                "field": "address_dropdown/country"
              },
              {
                "field": "address_dropdown/state"
              },
              {
                "field": "address_dropdown/county"
              },
              {
                "field": "description"
              },
              {
                "field": "ly_aggregate"
              },
              {
                "field": "ty_aggregate"
              },
              {
                "field": "key_zone_selector"
              },
              null,
              {
                "field": "value_change"
              },
              {
                "field": "perc_change"
              }
            ]}
              kb-interactive={true}
              freezeLeft={0} />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Risk XL Exposure Rating"
        fullWidth={true}
        viewScale={0.7}
        shownBy="cds/show_risk_xl">
        <HX.Section title="Layer Information">
          <HX.Pane>
            <HX.Table title="This Year"
              data={[
              {
                "datum": "cds/layers"
              }
            ]}
              fields={[
              "limit.read_only_option",
              "excess.read_only_option",
              "aggregate_deductible.read_only_option",
              {
                "field": "summary/ty/reinstatement_description"
              },
              null,
              {
                "field": "model/rms/gross_el"
              },
              {
                "field": "model/rms/gross_sd"
              },
              null,
              {
                "field": "model/rms/eq_el",
                "shownBy": "/cds/show_us_fields"
              },
              {
                "field": "model/rms/ws_el",
                "shownBy": "/cds/show_us_fields"
              },
              {
                "field": "model/rms/scs_el",
                "shownBy": "/cds/show_us_fields"
              },
              {
                "field": "model/rms/eu_ws_el",
                "shownBy": "/cds/show_intl_fields"
              },
              {
                "field": "model/rms/jp_eq_el",
                "shownBy": "/cds/show_intl_fields"
              },
              {
                "field": "model/rms/jp_ws_el",
                "shownBy": "/cds/show_intl_fields"
              },
              {
                "field": "model/rms/can_eq_el",
                "shownBy": "/cds/show_intl_fields"
              },
              {
                "field": "model/rms/caribbean_ws_el",
                "shownBy": "/cds/show_intl_fields"
              },
              null,
              {
                "field": "model/rms/perc_us_el",
                "shownBy": "/cds/show_perc_us_el"
              }
            ]}
              freezeLeft={0}
              kb-interactive={true} />
            <HX.Table title="Previous Year"
              data={[
              {
                "datum": "cds/layers"
              }
            ]}
              fields={[
              "limit_ly",
              "excess_ly",
              "aggregate_deductible_ly",
              {
                "field": "summary/ly/reinstatement_description"
              },
              null,
              {
                "field": "model_prev/rms/gross_el"
              },
              {
                "field": "model_prev/rms/gross_sd"
              },
              null,
              {
                "field": "model_prev/rms/eq_el",
                "shownBy": "/cds/show_us_fields"
              },
              {
                "field": "model_prev/rms/ws_el",
                "shownBy": "/cds/show_us_fields"
              },
              {
                "field": "model_prev/rms/scs_el",
                "shownBy": "/cds/show_us_fields"
              },
              {
                "field": "model_prev/rms/eu_ws_el",
                "shownBy": "/cds/show_intl_fields"
              },
              {
                "field": "model_prev/rms/jp_eq_el",
                "shownBy": "/cds/show_intl_fields"
              },
              {
                "field": "model_prev/rms/jp_ws_el",
                "shownBy": "/cds/show_intl_fields"
              },
              {
                "field": "model_prev/rms/can_eq_el",
                "shownBy": "/cds/show_intl_fields"
              },
              {
                "field": "model_prev/rms/caribbean_ws_el",
                "shownBy": "/cds/show_intl_fields"
              },
              null,
              {
                "field": "model_prev/rms/perc_us_el",
                "shownBy": "/cds/show_perc_us_el"
              }
            ]}
              freezeLeft={0}
              kb-interactive={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Coverage">
          <HX.Pane>
            <HX.Table data={[
              {
                "datum": "cds/risk_xl_exposure_rating/exposure_segment_total"
              },
              null,
              {
                "datum": "cds/risk_xl_exposure_rating/exposure_segment_1"
              },
              {
                "datum": "cds/risk_xl_exposure_rating/exposure_segment_2"
              },
              {
                "datum": "cds/risk_xl_exposure_rating/exposure_segment_3"
              },
              {
                "datum": "cds/risk_xl_exposure_rating/exposure_segment_4"
              },
              {
                "datum": "cds/risk_xl_exposure_rating/exposure_segment_5"
              },
              {
                "datum": "cds/risk_xl_exposure_rating/exposure_segment_6"
              },
              {
                "datum": "cds/risk_xl_exposure_rating/exposure_segment_7"
              },
              {
                "datum": "cds/risk_xl_exposure_rating/exposure_segment_8"
              },
              {
                "datum": "cds/risk_xl_exposure_rating/exposure_segment_9"
              },
              {
                "datum": "cds/risk_xl_exposure_rating/exposure_segment_10"
              },
              {
                "datum": "cds/risk_xl_exposure_rating/exposure_segment_11"
              },
              {
                "datum": "cds/risk_xl_exposure_rating/exposure_segment_12"
              },
              {
                "datum": "cds/risk_xl_exposure_rating/exposure_segment_13"
              },
              {
                "datum": "cds/risk_xl_exposure_rating/exposure_segment_14"
              },
              {
                "datum": "cds/risk_xl_exposure_rating/exposure_segment_15"
              },
              {
                "datum": "cds/risk_xl_exposure_rating/exposure_segment_16"
              },
              {
                "datum": "cds/risk_xl_exposure_rating/exposure_segment_17"
              },
              {
                "datum": "cds/risk_xl_exposure_rating/exposure_segment_18"
              },
              {
                "datum": "cds/risk_xl_exposure_rating/exposure_segment_19"
              },
              {
                "datum": "cds/risk_xl_exposure_rating/exposure_segment_20"
              }
            ]}
              fields={[
              "segment_name",
              "ex_cat_ulr",
              "curve_selection",
              "commentary",
              "exposed_limit_ty",
              "exposed_limit_ly",
              "exposed_limit_change"
            ]}
              freezeLeft={0}
              kb-interactive={true}
              transpose={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Exposure Entry">
          <HX.Pane>
            <HX.Collection numCols={5}
              fields={[
              "cds/risk_xl_exposure_rating/gnepi_exposure_adjustment",
              "cds/risk_xl_exposure_rating/gnepi_adj_factor",
              null,
              null,
              null,
              "cds/risk_xl_exposure_rating/gnepi_by_band"
            ]} />
            <HX.Table data={[
              {
                "datum": "cds/risk_xl_exposure_rating/exposure_listing"
              }
            ]}
              fields={[
              "lel_from",
              "lel_to",
              "segment",
              null,
              "location_count",
              "gnepi",
              "tiv",
              null,
              "location_count_adj",
              "gnepi_adj",
              "tiv_adj",
              null,
              "avg_tiv",
              null,
              "ex_cat_ulr_readonly",
              "ex_cat_ulr_override",
              null,
              "gu_el",
              null,
              "swiss_re_c",
              "swiss_re_c_override",
              null,
              "expected_severity_perc",
              "expected_severity",
              "expected_frequency",
              null,
              {
                "field": "loss_layer_1",
                "shownBy": "/cds/risk_xl_exposure_rating/show_loss_layer_1"
              },
              {
                "field": "loss_layer_2",
                "shownBy": "/cds/risk_xl_exposure_rating/show_loss_layer_2"
              },
              {
                "field": "loss_layer_3",
                "shownBy": "/cds/risk_xl_exposure_rating/show_loss_layer_3"
              },
              {
                "field": "loss_layer_4",
                "shownBy": "/cds/risk_xl_exposure_rating/show_loss_layer_4"
              },
              {
                "field": "loss_layer_5",
                "shownBy": "/cds/risk_xl_exposure_rating/show_loss_layer_5"
              },
              {
                "field": "loss_layer_6",
                "shownBy": "/cds/risk_xl_exposure_rating/show_loss_layer_6"
              },
              {
                "field": "loss_layer_7",
                "shownBy": "/cds/risk_xl_exposure_rating/show_loss_layer_7"
              },
              {
                "field": "loss_layer_8",
                "shownBy": "/cds/risk_xl_exposure_rating/show_loss_layer_8"
              },
              {
                "field": "loss_layer_9",
                "shownBy": "/cds/risk_xl_exposure_rating/show_loss_layer_9"
              },
              {
                "field": "loss_layer_10",
                "shownBy": "/cds/risk_xl_exposure_rating/show_loss_layer_10"
              },
              {
                "field": "loss_layer_11",
                "shownBy": "/cds/risk_xl_exposure_rating/show_loss_layer_11"
              },
              {
                "field": "loss_layer_12",
                "shownBy": "/cds/risk_xl_exposure_rating/show_loss_layer_12"
              },
              {
                "field": "loss_layer_13",
                "shownBy": "/cds/risk_xl_exposure_rating/show_loss_layer_13"
              },
              {
                "field": "loss_layer_14",
                "shownBy": "/cds/risk_xl_exposure_rating/show_loss_layer_14"
              },
              {
                "field": "loss_layer_15",
                "shownBy": "/cds/risk_xl_exposure_rating/show_loss_layer_15"
              },
              {
                "field": "loss_layer_16",
                "shownBy": "/cds/risk_xl_exposure_rating/show_loss_layer_16"
              },
              {
                "field": "loss_layer_17",
                "shownBy": "/cds/risk_xl_exposure_rating/show_loss_layer_17"
              },
              {
                "field": "loss_layer_18",
                "shownBy": "/cds/risk_xl_exposure_rating/show_loss_layer_18"
              },
              {
                "field": "loss_layer_19",
                "shownBy": "/cds/risk_xl_exposure_rating/show_loss_layer_19"
              },
              {
                "field": "loss_layer_20",
                "shownBy": "/cds/risk_xl_exposure_rating/show_loss_layer_20"
              }
            ]}
              freezeLeft={0}
              kb-interactive={true}
              maxListVisibleRows={25} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="">
          <HX.Pane flow="right"
            reflow={false}>
            <HX.Button task="run_exposure_simulation_task"
              title="Run Exposure Simulation" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Simulation Output">
          <HX.Table data={[
            {
              "datum": "cds/layers"
            }
          ]}
            fields={[
            {
              "field": "risk_xl_exposure_rating/gross_non_cat_el_deterministic"
            },
            {
              "field": "risk_xl_exposure_rating/gross_total_el_deterministic"
            },
            null,
            {
              "field": "risk_xl_exposure_rating/gross_total_el_sim"
            },
            null,
            {
              "field": "risk_xl_exposure_rating/model_limit_factor",
              "infoBy": "/cds/number_reins_factor_info"
            },
            {
              "field": "risk_xl_exposure_rating/net_el_excl_reins_prem"
            },
            null,
            {
              "field": "risk_xl_exposure_rating/no_expected_reins",
              "infoBy": "/cds/paid_reins_factor_info"
            },
            null,
            {
              "field": "risk_xl_exposure_rating/net_el"
            }
          ]}
            freezeLeft={0}
            kb-interactive={true} />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Burn Input"
        fullWidth={true}
        viewScale={0.7}
        shownBy="model_state/show_after_landing_page">
        <HX.Section title="Coverage">
          <HX.Pane>
            <HX.Table data={[
              {
                "datum": "cds/experience_rating/coverage"
              }
            ]}
              fields={[
              "coverage_1",
              "coverage_2",
              "coverage_3",
              "coverage_4",
              "coverage_5",
              "coverage_6",
              "coverage_7",
              "coverage_8"
            ]}
              freezeLeft={0}
              kb-interactive={true} />
          </HX.Pane>
          <HX.Pane>
            <HX.Table data={[
              {
                "datum": "cds/layers"
              }
            ]}
              fields={[
              "limit_cnv",
              "excess_cnv",
              null,
              {
                "field": "burn/burn_coverage/coverage_1",
                "labelBy": "/cds/experience_rating/coverage/coverage_1"
              },
              {
                "field": "burn/burn_coverage/coverage_2",
                "labelBy": "/cds/experience_rating/coverage/coverage_2"
              },
              {
                "field": "burn/burn_coverage/coverage_3",
                "labelBy": "/cds/experience_rating/coverage/coverage_3"
              },
              {
                "field": "burn/burn_coverage/coverage_4",
                "labelBy": "/cds/experience_rating/coverage/coverage_4"
              },
              {
                "field": "burn/burn_coverage/coverage_5",
                "labelBy": "/cds/experience_rating/coverage/coverage_5"
              },
              {
                "field": "burn/burn_coverage/coverage_6",
                "labelBy": "/cds/experience_rating/coverage/coverage_6"
              },
              {
                "field": "burn/burn_coverage/coverage_7",
                "labelBy": "/cds/experience_rating/coverage/coverage_7"
              },
              {
                "field": "burn/burn_coverage/coverage_8",
                "labelBy": "/cds/experience_rating/coverage/coverage_8"
              }
            ]}
              freezeLeft={0}
              kb-interactive={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Exposure Input">
          <HX.Pane flow="right"
            reflow={false}>
            <HX.Pane ratio={1}>
              <HX.Notes field="cds/experience_rating/exposure/exposure_input_information"
                title="Exposure Input Information" />
              <HX.Collection fields={[
                "cds/experience_rating/exposure/exposure_start_year"
              ]} />
            </HX.Pane>
            <HX.Pane ratio={2} />
          </HX.Pane>
          <HX.With context={{
            "path": "cds/experience_rating/exposure",
            "type": "struct"
          }}>
            <HX.Pane flow="right"
              reflow={false}
              shownBy="/cds/show_non_risk_xl">
              <HX.Table title=" "
                data={[
                "gnepi_exposure_segment",
                null,
                {
                  "datum": "exposure_segment_1"
                },
                {
                  "datum": "exposure_segment_2"
                },
                {
                  "datum": "exposure_segment_3"
                }
              ]}
                fields={[
                "segment_type",
                "segment_name",
                "allow_for_rc",
                "allow_for_other_changes",
                "inflation_option"
              ]}
                transpose={true}
                kb-interactive={true} />
              <HX.Notes stretch={true}
                field="comments"
                title="Comments" />
            </HX.Pane>
            <HX.Pane>
              <HX.Pane flow="right"
                reflow={false}>
                <HX.Table data={[
                  "rate_change_gross_net",
                  null,
                  "exposure_listing"
                ]}
                  fields={[
                  "year",
                  {
                    "field": "pif",
                    "shownBy": "/cds/show_risk_xl"
                  },
                  "gnepi_actual",
                  "gnepi_projected",
                  null,
                  {
                    "field": "exposure_value_1",
                    "labelBy": "/cds/experience_rating/exposure/exposure_segment_1/exposure_label",
                    "shownBy": "/cds/show_non_risk_xl"
                  },
                  {
                    "field": "exposure_value_2",
                    "labelBy": "/cds/experience_rating/exposure/exposure_segment_2/exposure_label",
                    "shownBy": "/cds/show_non_risk_xl"
                  },
                  {
                    "field": "exposure_value_3",
                    "labelBy": "/cds/experience_rating/exposure/exposure_segment_3/exposure_label",
                    "shownBy": "/cds/show_non_risk_xl"
                  },
                  null,
                  "rate_change",
                  "inflation_option_1",
                  {
                    "field": "inflation_option_2",
                    "shownBy": "/cds/show_non_risk_xl"
                  },
                  {
                    "field": "other_changes",
                    "shownBy": "/cds/show_non_risk_xl"
                  },
                  null,
                  "gnepi_exposure_change",
                  {
                    "field": "exposure_change_1",
                    "labelBy": "/cds/experience_rating/exposure/exposure_segment_1/exposure_change_label",
                    "shownBy": "/cds/show_non_risk_xl"
                  },
                  {
                    "field": "exposure_change_2",
                    "labelBy": "/cds/experience_rating/exposure/exposure_segment_2/exposure_change_label",
                    "shownBy": "/cds/show_non_risk_xl"
                  },
                  {
                    "field": "exposure_change_3",
                    "labelBy": "/cds/experience_rating/exposure/exposure_segment_3/exposure_change_label",
                    "shownBy": "/cds/show_non_risk_xl"
                  },
                  null,
                  "gnepi_exposure_index",
                  {
                    "field": "exposure_index_1",
                    "labelBy": "/cds/experience_rating/exposure/exposure_segment_1/exposure_index_label",
                    "shownBy": "/cds/show_non_risk_xl"
                  },
                  {
                    "field": "exposure_index_2",
                    "labelBy": "/cds/experience_rating/exposure/exposure_segment_2/exposure_index_label",
                    "shownBy": "/cds/show_non_risk_xl"
                  },
                  {
                    "field": "exposure_index_3",
                    "labelBy": "/cds/experience_rating/exposure/exposure_segment_3/exposure_index_label",
                    "shownBy": "/cds/show_non_risk_xl"
                  },
                  null,
                  {
                    "field": "gnepi_total_index",
                    "shownBy": "/cds/show_non_risk_xl"
                  },
                  {
                    "field": "total_index_1",
                    "labelBy": "/cds/experience_rating/exposure/exposure_segment_1/total_index_label",
                    "shownBy": "/cds/show_non_risk_xl"
                  },
                  {
                    "field": "total_index_2",
                    "labelBy": "/cds/experience_rating/exposure/exposure_segment_2/total_index_label",
                    "shownBy": "/cds/show_non_risk_xl"
                  },
                  {
                    "field": "total_index_3",
                    "labelBy": "/cds/experience_rating/exposure/exposure_segment_3/total_index_label",
                    "shownBy": "/cds/show_non_risk_xl"
                  },
                  null,
                  {
                    "field": "risk_frequency_index",
                    "shownBy": "/cds/show_risk_xl"
                  },
                  null,
                  {
                    "field": "risk_avg_exposure_index",
                    "shownBy": "/cds/show_risk_xl"
                  },
                  {
                    "field": "risk_inflation_index",
                    "shownBy": "/cds/show_risk_xl"
                  },
                  {
                    "field": "risk_severity_index",
                    "shownBy": "/cds/show_risk_xl"
                  }
                ]}
                  freezeLeft={1}
                  filter="show_row_exposure"
                  kb-interactive={true} />
              </HX.Pane>
            </HX.Pane>
          </HX.With>
        </HX.Section>
        <HX.Section title="Claims Input">
          <HX.With context={{
            "path": "cds/experience_rating",
            "type": "struct"
          }}>
            <HX.Notes stretch={true}
              field="claims_other/comments"
              title="Comments" />
            <HX.Table data={[
              "claims"
            ]}
              fields={[
              "year",
              "currency",
              "description",
              {
                "field": "cat_non_cat",
                "shownBy": "/cds/show_risk_xl"
              },
              {
                "field": "cat_name",
                "shownBy": "/cds/show_risk_xl"
              },
              "large_loss",
              "coverage",
              null,
              "gnepi_loss",
              {
                "field": "loss_segment_1",
                "labelBy": "/cds/experience_rating/claims_other/loss_segment_label_1",
                "shownBy": "/cds/show_non_risk_xl"
              },
              {
                "field": "loss_segment_2",
                "labelBy": "/cds/experience_rating/claims_other/loss_segment_label_2",
                "shownBy": "/cds/show_non_risk_xl"
              },
              {
                "field": "loss_segment_3",
                "labelBy": "/cds/experience_rating/claims_other/loss_segment_label_3",
                "shownBy": "/cds/show_non_risk_xl"
              },
              null,
              "previous_year_total",
              "this_year_total",
              "movement",
              "loss_type",
              "as_if_loss",
              {
                "field": "on_levelled_loss",
                "labelBy": "/cds/burn_ol_ccy_label"
              },
              {
                "field": "return_period",
                "shownBy": "/cds/show_non_risk_xl"
              },
              "comment",
              null,
              {
                "field": "loss_layer_1",
                "shownBy": "/cds/experience_rating/claims_other/show_loss_layer_1"
              },
              {
                "field": "loss_layer_2",
                "shownBy": "/cds/experience_rating/claims_other/show_loss_layer_2"
              },
              {
                "field": "loss_layer_3",
                "shownBy": "/cds/experience_rating/claims_other/show_loss_layer_3"
              },
              {
                "field": "loss_layer_4",
                "shownBy": "/cds/experience_rating/claims_other/show_loss_layer_4"
              },
              {
                "field": "loss_layer_5",
                "shownBy": "/cds/experience_rating/claims_other/show_loss_layer_5"
              },
              {
                "field": "loss_layer_6",
                "shownBy": "/cds/experience_rating/claims_other/show_loss_layer_6"
              },
              {
                "field": "loss_layer_7",
                "shownBy": "/cds/experience_rating/claims_other/show_loss_layer_7"
              },
              {
                "field": "loss_layer_8",
                "shownBy": "/cds/experience_rating/claims_other/show_loss_layer_8"
              },
              {
                "field": "loss_layer_9",
                "shownBy": "/cds/experience_rating/claims_other/show_loss_layer_9"
              },
              {
                "field": "loss_layer_10",
                "shownBy": "/cds/experience_rating/claims_other/show_loss_layer_10"
              },
              {
                "field": "loss_layer_11",
                "shownBy": "/cds/experience_rating/claims_other/show_loss_layer_11"
              },
              {
                "field": "loss_layer_12",
                "shownBy": "/cds/experience_rating/claims_other/show_loss_layer_12"
              },
              {
                "field": "loss_layer_13",
                "shownBy": "/cds/experience_rating/claims_other/show_loss_layer_13"
              },
              {
                "field": "loss_layer_14",
                "shownBy": "/cds/experience_rating/claims_other/show_loss_layer_14"
              },
              {
                "field": "loss_layer_15",
                "shownBy": "/cds/experience_rating/claims_other/show_loss_layer_15"
              },
              {
                "field": "loss_layer_16",
                "shownBy": "/cds/experience_rating/claims_other/show_loss_layer_16"
              },
              {
                "field": "loss_layer_17",
                "shownBy": "/cds/experience_rating/claims_other/show_loss_layer_17"
              },
              {
                "field": "loss_layer_18",
                "shownBy": "/cds/experience_rating/claims_other/show_loss_layer_18"
              },
              {
                "field": "loss_layer_19",
                "shownBy": "/cds/experience_rating/claims_other/show_loss_layer_19"
              },
              {
                "field": "loss_layer_20",
                "shownBy": "/cds/experience_rating/claims_other/show_loss_layer_20"
              }
            ]}
              kb-interactive={true} />
          </HX.With>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Burn Output"
        fullWidth={true}
        viewScale={0.7}
        shownBy="model_state/show_after_landing_page">
        <HX.Section title="Summary">
          <HX.Pane flow="right"
            reflow={false}>
            <HX.Pane ratio={1}>
              <HX.Collection fields={[
                "cds/experience_rating/exposure/burn_start_year"
              ]} />
            </HX.Pane>
            <HX.Pane ratio={2} />
          </HX.Pane>
          <HX.Pane flow="right"
            reflow={false}>
            <HX.Pane ratio={1}>
              <HX.Table data={[
                {
                  "datum": "cds/layers"
                }
              ]}
                fields={[
                {
                  "field": "limit_cnv",
                  "maxWidth": 400
                },
                {
                  "field": "excess_cnv",
                  "maxWidth": 400
                }
              ]}
                freezeLeft={0}
                kb-interactive={true} />
            </HX.Pane>
            <HX.Pane ratio={2}>
              <HX.Table data={[
                {
                  "datum": "cds/experience_rating/claims_other/ten_largest"
                }
              ]}
                fields={[
                {
                  "field": "year",
                  "width": 100
                },
                {
                  "field": "description",
                  "maxWidth": 400
                },
                {
                  "field": "previous_year_total",
                  "maxWidth": 400
                },
                {
                  "field": "this_year_total",
                  "maxWidth": 400
                },
                {
                  "field": "on_levelled_loss",
                  "maxWidth": 400
                }
              ]}
                kb-interactive={true} />
            </HX.Pane>
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Layer Loss Summary">
          <HX.Pane flow="right"
            reflow={false}>
            <HX.Table title=" "
              data={[
              {
                "datum": "cds/experience_rating/claims_other/burn_year_result"
              }
            ]}
              fields={[
              {
                "field": "year",
                "width": 100
              },
              {
                "field": "non_zero_claim_count",
                "maxWidth": 400
              },
              {
                "field": "severity",
                "maxWidth": 400
              },
              {
                "field": "on_levelled_loss",
                "maxWidth": 400
              },
              null,
              {
                "field": "loss_layer_1",
                "maxWidth": 400,
                "shownBy": "/cds/experience_rating/claims_other/show_loss_layer_1"
              },
              {
                "field": "loss_layer_2",
                "maxWidth": 400,
                "shownBy": "/cds/experience_rating/claims_other/show_loss_layer_2"
              },
              {
                "field": "loss_layer_3",
                "maxWidth": 400,
                "shownBy": "/cds/experience_rating/claims_other/show_loss_layer_3"
              },
              {
                "field": "loss_layer_4",
                "maxWidth": 400,
                "shownBy": "/cds/experience_rating/claims_other/show_loss_layer_4"
              },
              {
                "field": "loss_layer_5",
                "maxWidth": 400,
                "shownBy": "/cds/experience_rating/claims_other/show_loss_layer_5"
              },
              {
                "field": "loss_layer_6",
                "maxWidth": 400,
                "shownBy": "/cds/experience_rating/claims_other/show_loss_layer_6"
              },
              {
                "field": "loss_layer_7",
                "maxWidth": 400,
                "shownBy": "/cds/experience_rating/claims_other/show_loss_layer_7"
              },
              {
                "field": "loss_layer_8",
                "maxWidth": 400,
                "shownBy": "/cds/experience_rating/claims_other/show_loss_layer_8"
              },
              {
                "field": "loss_layer_9",
                "maxWidth": 400,
                "shownBy": "/cds/experience_rating/claims_other/show_loss_layer_9"
              },
              {
                "field": "loss_layer_10",
                "maxWidth": 400,
                "shownBy": "/cds/experience_rating/claims_other/show_loss_layer_10"
              },
              {
                "field": "loss_layer_11",
                "maxWidth": 400,
                "shownBy": "/cds/experience_rating/claims_other/show_loss_layer_11"
              },
              {
                "field": "loss_layer_12",
                "maxWidth": 400,
                "shownBy": "/cds/experience_rating/claims_other/show_loss_layer_12"
              },
              {
                "field": "loss_layer_13",
                "maxWidth": 400,
                "shownBy": "/cds/experience_rating/claims_other/show_loss_layer_13"
              },
              {
                "field": "loss_layer_14",
                "maxWidth": 400,
                "shownBy": "/cds/experience_rating/claims_other/show_loss_layer_14"
              },
              {
                "field": "loss_layer_15",
                "maxWidth": 400,
                "shownBy": "/cds/experience_rating/claims_other/show_loss_layer_15"
              },
              {
                "field": "loss_layer_16",
                "maxWidth": 400,
                "shownBy": "/cds/experience_rating/claims_other/show_loss_layer_16"
              },
              {
                "field": "loss_layer_17",
                "maxWidth": 400,
                "shownBy": "/cds/experience_rating/claims_other/show_loss_layer_17"
              },
              {
                "field": "loss_layer_18",
                "maxWidth": 400,
                "shownBy": "/cds/experience_rating/claims_other/show_loss_layer_18"
              },
              {
                "field": "loss_layer_19",
                "maxWidth": 400,
                "shownBy": "/cds/experience_rating/claims_other/show_loss_layer_19"
              },
              {
                "field": "loss_layer_20",
                "maxWidth": 400,
                "shownBy": "/cds/experience_rating/claims_other/show_loss_layer_20"
              }
            ]}
              filter="show_row"
              kb-interactive={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Selection">
          <HX.Pane flow="right"
            reflow={false}>
            <HX.Pane shownBy="cds/show_non_risk_xl"
              ratio={1}>
              <HX.Collection fields={[
                "cds/experience_rating/claims_other/net_or_gross_reins_calc"
              ]} />
            </HX.Pane>
            <HX.Pane shownBy="cds/show_risk_xl"
              ratio={1}>
              <HX.Collection fields={[
                "cds/experience_rating/claims_other/risk_xl_use_rms_cat"
              ]} />
            </HX.Pane>
            <HX.Pane ratio={2} />
          </HX.Pane>
          <HX.Notes stretch={true}
            field="cds/experience_rating/claims_other/burn_output_comments"
            title="Comments" />
          <HX.Table data={[
            {
              "datum": "cds/layers",
              "maxWidth": 400
            }
          ]}
            fields={[
            {
              "field": "burn/burn_result/avg_3_year"
            },
            {
              "field": "burn/burn_result/avg_5_year"
            },
            {
              "field": "burn/burn_result/avg_7_year"
            },
            {
              "field": "burn/burn_result/avg_all_year"
            },
            {
              "field": "burn/burn_result/selection"
            },
            null,
            {
              "field": "burn/burn_result/gross_burn_el",
              "shownBy": "/cds/experience_rating/claims_other/show_gross_fields"
            },
            {
              "field": "burn/burn_result/gross_burn_sd",
              "shownBy": "/cds/experience_rating/claims_other/show_gross_fields"
            },
            {
              "field": "burn/burn_result/gross_burn_lol",
              "shownBy": "/cds/experience_rating/claims_other/show_gross_fields"
            },
            {
              "field": "burn/burn_result/gross_burn_sd_rol",
              "shownBy": "/cds/experience_rating/claims_other/show_gross_fields"
            },
            {
              "field": "burn/burn_result/risk_xl_non_cat_burn_gross_el",
              "shownBy": "/cds/show_risk_xl"
            },
            {
              "field": "burn/burn_result/risk_xl_cat_burn_gross_el",
              "shownBy": "/cds/show_risk_xl"
            },
            {
              "field": "burn/burn_result/risk_xl_rms_gross_el",
              "shownBy": "/cds/show_risk_xl"
            },
            {
              "field": null,
              "shownBy": "/cds/show_risk_xl"
            },
            {
              "field": "burn/burn_result/net_burn_el",
              "shownBy": "/cds/experience_rating/claims_other/show_net_fields"
            },
            {
              "field": "burn/burn_result/net_burn_sd",
              "shownBy": "/cds/experience_rating/claims_other/show_net_fields"
            },
            {
              "field": "burn/burn_result/net_burn_lol",
              "shownBy": "/cds/experience_rating/claims_other/show_net_fields"
            },
            {
              "field": "burn/burn_result/net_burn_sd_rol",
              "shownBy": "/cds/experience_rating/claims_other/show_net_fields"
            }
          ]}
            rowHeaderSettings={{
            "width": 150
          }}
            transpose={true}
            kb-interactive={true} />
        </HX.Section>
        <HX.Section title="Historic Losses">
          <HX.Pane>
            <CustomComponent title="Loss Chart"
              data={[
              {
                "labelBy": "year",
                "list": "cds/experience_rating/claims_other/burn_year_result"
              },
              {
                "labelBy": "year",
                "list": "cds/experience_rating/claims_other/burn_year_result"
              }
            ]}
              traces={[
              {
                "field": "nominal_loss",
                "label": "Nominal Losses"
              },
              {
                "field": "on_levelled_loss",
                "label": "OL Losses (excl. SuperCat)"
              }
            ]}
              series={[
              {
                "points": [
                  {
                    "list": "cds/experience_rating/claims_other/burn_year_result",
                    "x": "year",
                    "y": "freq_per_m_prem"
                  }
                ],
                "seriesLabel": "Frequency Per CCYm Premium (OL)"
              }
            ]} />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Curve Aggregator"
        fullWidth={true}
        viewScale={0.7}
        shownBy="cds/show_non_risk_xl">
        <HX.Section title="Input">
          <HX.Pane>
            <HX.Table data={[
              {
                "datum": "cds/curve_aggregator/pml_selections"
              }
            ]}
              fields={[
              "include_in_aggregator",
              "weight",
              "name"
            ]}
              transpose={true}
              rowHeaderSettings={{
              "width": 250
            }}
              kb-interactive={true}
              syncColumnWidthsKey="curve_agg_input" />
            <HX.Table data={[
              {
                "datum": "cds/curve_aggregator/pml_selections"
              }
            ]}
              fields={[
              "rp_loss/rp_10000",
              "rp_loss/rp_5000",
              "rp_loss/rp_1000",
              "rp_loss/rp_500",
              "rp_loss/rp_250",
              "rp_loss/rp_200",
              "rp_loss/rp_100",
              "rp_loss/rp_50",
              "rp_loss/rp_25",
              "rp_loss/rp_10",
              "rp_loss/rp_5",
              "rp_loss/rp_2"
            ]}
              transpose={true}
              rowHeaderSettings={{
              "width": 250
            }}
              kb-interactive={true}
              syncColumnWidthsKey="curve_agg_input" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Output">
          <HX.Pane flow="right"
            reflow={false}>
            <HX.Pane>
              <HX.Table data={[
                {
                  "datum": "cds/curve_aggregator/aggregator_output/rp_labels",
                  "width": 250
                },
                {
                  "datum": "cds/curve_aggregator/aggregator_output/rp_loss",
                  "maxWidth": 400
                }
              ]}
                fields={[
                "rp_10000",
                "rp_5000",
                "rp_1000",
                "rp_500",
                "rp_250",
                "rp_200",
                "rp_100",
                "rp_50",
                "rp_25",
                "rp_10",
                "rp_5",
                "rp_2"
              ]}
                transpose={true}
                kb-interactive={true} />
            </HX.Pane>
            <HX.Pane>
              <HX.Button task="pull_pml_curves_task"
                title="Pull Curves" />
              <HX.Button task="aggregate_curves_task"
                title="Run Aggregate Curves Task" />
            </HX.Pane>
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Quote"
        fullWidth={true}
        viewScale={0.7}
        shownBy="model_state/show_after_landing_page">
        <HX.Section title="ROL Calc"
          shownBy="cds/show_non_risk_xl">
          <HX.Pane flow="right"
            reflow={false}>
            <HX.Pane ratio={1}>
              <HX.Notes field="cds/tp_comments"
                title="Quote Comments" />
              <HX.Notes field="cds/quote/quote_reins_information"
                title="KPI Basis Information" />
            </HX.Pane>
            <HX.Pane ratio={1} />
          </HX.Pane>
          <HX.Pane flow="right"
            reflow={false}>
            <HX.Pane ratio={8}>
              <HX.Table title="This Year"
                data={[
                "cds/layers",
                null,
                {
                  "datum": "cds",
                  "labelBy": "cds/total_label"
                }
              ]}
                fields={[
                {
                  "field": "layer_structure"
                },
                null,
                {
                  "field": "quote/rol_ty/rol_rms"
                },
                {
                  "field": "quote/rol_ty/weighting_rms"
                },
                {
                  "field": "quote/rol_ty/rol_ivor"
                },
                {
                  "field": "quote/rol_ty/weighting_ivor"
                },
                {
                  "field": "quote/rol_ty/rol_air"
                },
                {
                  "field": "quote/rol_ty/weighting_air"
                },
                {
                  "field": "quote/rol_ty/rol_burn"
                },
                {
                  "field": "quote/rol_ty/rol_burn_override"
                },
                {
                  "field": "quote/rol_ty/weighting_burn"
                },
                null,
                {
                  "field": "quote/rol_ty/rol_afb_tech"
                },
                null,
                {
                  "field": "quote/rol_ty/ulr"
                },
                {
                  "field": "quote/rol_ty/bpi"
                },
                null,
                {
                  "field": "quote/rol_ty/lol_rms"
                },
                {
                  "field": "quote/rol_ty/lol_ivor"
                },
                {
                  "field": "quote/rol_ty/lol_air"
                },
                {
                  "field": "quote/rol_ty/lol_burn"
                },
                {
                  "field": "quote/rol_ty/lol_weighted"
                }
              ]}
                kb-interactive={true}
                syncColumnWidthsKey="rol_calc_table" />
            </HX.Pane>
            <HX.Pane ratio={3}
              flow="right"
              reflow={false}>
              <HX.Table title="All Perils"
                data={[
                "cds/layers"
              ]}
                fields={[
                {
                  "field": "quote/rol_ty/rp_attach"
                },
                {
                  "field": "quote/rol_ty/rp_exit"
                },
                {
                  "field": "quote/rol_ty/rp_pml_selection"
                }
              ]}
                kb-interactive={true}
                syncColumnWidthsKey="all_perils_table" />
              <HX.Table title="Peak Peril"
                data={[
                "cds/layers"
              ]}
                fields={[
                {
                  "field": "quote/rol_ty/rp_attach_peak"
                },
                {
                  "field": "quote/rol_ty/rp_exit_peak"
                },
                {
                  "field": "quote/rol_ty/rp_pml_selection_peak"
                }
              ]}
                kb-interactive={true}
                syncColumnWidthsKey="peak_perils_table" />
            </HX.Pane>
          </HX.Pane>
          <HX.Pane flow="right"
            reflow={false}>
            <HX.Pane ratio={8}>
              <HX.Table title="Previous Year"
                data={[
                "cds/layers",
                null,
                {
                  "datum": "cds",
                  "labelBy": "cds/total_label"
                }
              ]}
                fields={[
                {
                  "field": "layer_structure_ly"
                },
                null,
                {
                  "field": "quote/rol_ly/rol_rms"
                },
                {
                  "field": "quote/rol_ly/weighting_rms"
                },
                {
                  "field": "quote/rol_ly/rol_ivor"
                },
                {
                  "field": "quote/rol_ly/weighting_ivor"
                },
                {
                  "field": "quote/rol_ly/rol_air"
                },
                {
                  "field": "quote/rol_ly/weighting_air"
                },
                {
                  "field": "quote/rol_ly/rol_burn"
                },
                {
                  "field": "quote/rol_ly/rol_burn_override"
                },
                {
                  "field": "quote/rol_ly/weighting_burn"
                },
                null,
                {
                  "field": "quote/rol_ly/rol_afb_tech"
                },
                null,
                {
                  "field": "quote/rol_ly/ulr"
                },
                {
                  "field": "quote/rol_ly/bpi"
                },
                null,
                {
                  "field": "quote/rol_ly/lol_rms"
                },
                {
                  "field": "quote/rol_ly/lol_ivor"
                },
                {
                  "field": "quote/rol_ly/lol_air"
                },
                {
                  "field": "quote/rol_ly/lol_burn"
                },
                {
                  "field": "quote/rol_ly/lol_weighted"
                }
              ]}
                kb-interactive={true}
                syncColumnWidthsKey="rol_calc_table" />
            </HX.Pane>
            <HX.Pane ratio={3}
              flow="right"
              reflow={false}>
              <HX.Table title="All Perils"
                data={[
                "cds/layers"
              ]}
                fields={[
                {
                  "field": "quote/rol_ly/rp_attach"
                },
                {
                  "field": "quote/rol_ly/rp_exit"
                },
                {
                  "field": "quote/rol_ly/rp_pml_selection"
                }
              ]}
                kb-interactive={true}
                syncColumnWidthsKey="all_perils_table" />
              <HX.Table title="Peak Peril"
                data={[
                "cds/layers"
              ]}
                fields={[
                {
                  "field": "quote/rol_ly/rp_attach_peak"
                },
                {
                  "field": "quote/rol_ly/rp_exit_peak"
                },
                {
                  "field": "quote/rol_ly/rp_pml_selection_peak"
                }
              ]}
                kb-interactive={true}
                syncColumnWidthsKey="peak_perils_table" />
            </HX.Pane>
          </HX.Pane>
        </HX.Section>
        <HX.Section title="ROL Calc"
          shownBy="cds/show_risk_xl">
          <HX.Pane flow="right"
            reflow={false}>
            <HX.Pane ratio={1}>
              <HX.Notes field="cds/tp_comments"
                title="Quote Comments" />
              <HX.Notes field="cds/quote/quote_reins_information"
                title="KPI Basis Information" />
            </HX.Pane>
            <HX.Pane ratio={1} />
          </HX.Pane>
          <HX.Pane flow="right"
            reflow={false}>
            <HX.Pane ratio={8}>
              <HX.Table title="This Year"
                data={[
                "cds/layers",
                null,
                {
                  "datum": "cds",
                  "labelBy": "cds/total_label"
                }
              ]}
                fields={[
                {
                  "field": "layer_structure"
                },
                null,
                {
                  "field": "quote/rol_ty/risk_xl_rol_exposure"
                },
                {
                  "field": "quote/rol_ty/risk_xl_weighting_exposure"
                },
                {
                  "field": "quote/rol_ty/rol_burn"
                },
                {
                  "field": "quote/rol_ty/rol_burn_override"
                },
                {
                  "field": "quote/rol_ty/weighting_burn"
                },
                null,
                {
                  "field": "quote/rol_ty/rol_afb_tech"
                },
                null,
                {
                  "field": "quote/rol_ty/layer_exposure"
                },
                {
                  "field": "quote/rol_ty/roev"
                },
                null,
                {
                  "field": "quote/rol_ty/ulr"
                },
                {
                  "field": "quote/rol_ty/bpi"
                },
                null,
                {
                  "field": "quote/rol_ty/risk_xl_lol_exposure"
                },
                {
                  "field": "quote/rol_ty/lol_burn"
                },
                {
                  "field": "quote/rol_ty/lol_weighted"
                }
              ]}
                kb-interactive={true}
                syncColumnWidthsKey="rol_calc_table" />
            </HX.Pane>
          </HX.Pane>
          <HX.Pane flow="right"
            reflow={false}>
            <HX.Pane ratio={8}>
              <HX.Table title="Previous Year"
                data={[
                "cds/layers",
                null,
                {
                  "datum": "cds",
                  "labelBy": "cds/total_label"
                }
              ]}
                fields={[
                {
                  "field": "layer_structure_ly"
                },
                null,
                {
                  "field": "quote/rol_ly/risk_xl_rol_exposure"
                },
                {
                  "field": "quote/rol_ly/risk_xl_weighting_exposure"
                },
                {
                  "field": "quote/rol_ly/rol_burn"
                },
                {
                  "field": "quote/rol_ly/rol_burn_override"
                },
                {
                  "field": "quote/rol_ly/weighting_burn"
                },
                null,
                {
                  "field": "quote/rol_ly/rol_afb_tech"
                },
                null,
                {
                  "field": "quote/rol_ly/layer_exposure"
                },
                {
                  "field": "quote/rol_ly/roev"
                },
                null,
                {
                  "field": "quote/rol_ly/ulr"
                },
                {
                  "field": "quote/rol_ly/bpi"
                },
                null,
                {
                  "field": "quote/rol_ly/risk_xl_lol_exposure"
                },
                {
                  "field": "quote/rol_ly/lol_burn"
                },
                {
                  "field": "quote/rol_ly/lol_weighted"
                }
              ]}
                kb-interactive={true}
                syncColumnWidthsKey="rol_calc_table" />
            </HX.Pane>
          </HX.Pane>
        </HX.Section>
        <HX.Section title="BI Data"
          defaultCollapsed={true}>
          <HX.Pane flow="right"
            reflow={false}>
            <HX.Pane ratio={1}>
              <HX.Button task="bi_data_fetch_task"
                title="Fetch BI Data" />
              <HX.Collection numCols={1}
                fields={[
                "cds/bi_data/profit",
                "cds/bi_data/ilr",
                "cds/bi_data/break_even"
              ]} />
            </HX.Pane>
            <HX.Pane ratio={3}>
              <CustomComponent title="BI Data"
                data={[
                {
                  "labelBy": "yoa",
                  "list": "cds/bi_data/graph_list"
                },
                {
                  "labelBy": "yoa",
                  "list": "cds/bi_data/graph_list"
                },
                {
                  "labelBy": "yoa",
                  "list": "cds/bi_data/graph_list"
                }
              ]}
                traces={[
                {
                  "field": "wep",
                  "label": "WEP"
                },
                {
                  "field": "incurred",
                  "label": "Incurred"
                },
                {
                  "field": "exposure",
                  "label": "Exposure"
                }
              ]}
                series={[
                {
                  "points": [
                    {
                      "list": "cds/bi_data/graph_list",
                      "x": "yoa",
                      "y": "elr"
                    }
                  ],
                  "seriesLabel": "ELR"
                },
                {
                  "points": [
                    {
                      "list": "cds/bi_data/graph_list",
                      "x": "yoa",
                      "y": "cumulative_rate_change"
                    }
                  ],
                  "seriesLabel": "Rate Change"
                }
              ]} />
            </HX.Pane>
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Line Size">
          <HX.Table title="This Year"
            data={[
            "cds/layers",
            null,
            {
              "datum": "cds",
              "labelBy": "cds/total_label"
            },
            null,
            {
              "datum": "cds/quote_total_usd"
            }
          ]}
            fields={[
            {
              "field": "limit_cnv"
            },
            {
              "field": "excess_cnv"
            },
            {
              "field": "layer_description.read_only_option"
            },
            null,
            {
              "field": "quote/rol_ty/rol_quote"
            },
            {
              "field": "quote/rol_ty/rol_fot"
            },
            {
              "field": "summary/ty/risk_adjusted_rate_change"
            },
            {
              "field": "quote/rol_ty/rol_afb_tech"
            },
            {
              "field": "quote/rol_ty/quote_fot_ratio"
            },
            {
              "field": "quote/rol_ty/quote_adequacy"
            },
            {
              "field": "quote/rol_ty/fot_adequacy"
            },
            null,
            {
              "field": "quote/rol_ty/prem_full_line"
            },
            {
              "field": "quote/rol_ty/written_line"
            },
            {
              "field": "quote/rol_ty/written_line_dollar"
            },
            {
              "field": "quote/rol_ty/estimated_signing"
            },
            {
              "field": "quote/rol_ty/estimated_signing_dollar"
            },
            {
              "field": "quote/rol_ty/signed_line"
            },
            {
              "field": "quote/rol_ty/signed_line_dollar"
            },
            null,
            {
              "field": "quote/rol_ty/epi_written"
            },
            {
              "field": "quote/rol_ty/epi_estimated"
            },
            {
              "field": "quote/rol_ty/epi_signed"
            }
          ]}
            kb-interactive={true}
            removeHorizontalScroll={true}
            syncColumnWidthsKey="line_size_table" />
          <HX.Table title="Previous Year"
            data={[
            "cds/layers",
            null,
            {
              "datum": "cds",
              "labelBy": "cds/total_label"
            },
            null,
            {
              "datum": "cds/quote_total_usd"
            }
          ]}
            fields={[
            {
              "field": "limit_cnv_ly"
            },
            {
              "field": "excess_cnv_ly"
            },
            {
              "field": "layer_description_ly"
            },
            null,
            {
              "field": "quote/rol_ly/rol_quote"
            },
            {
              "field": "quote/rol_ly/rol_fot"
            },
            {
              "field": "summary/ly/risk_adjusted_rate_change"
            },
            {
              "field": "quote/rol_ly/rol_afb_tech"
            },
            {
              "field": "quote/rol_ly/quote_fot_ratio"
            },
            {
              "field": "quote/rol_ly/quote_adequacy"
            },
            {
              "field": "quote/rol_ly/fot_adequacy"
            },
            null,
            {
              "field": "quote/rol_ly/prem_full_line"
            },
            {
              "field": "quote/rol_ly/written_line"
            },
            {
              "field": "quote/rol_ly/written_line_dollar"
            },
            {
              "field": "quote/rol_ly/estimated_signing"
            },
            {
              "field": "quote/rol_ly/estimated_signing_dollar"
            },
            {
              "field": "quote/rol_ly/signed_line"
            },
            {
              "field": "quote/rol_ly/signed_line_dollar"
            },
            null,
            {
              "field": "quote/rol_ly/epi_written"
            },
            {
              "field": "quote/rol_ly/epi_estimated"
            },
            {
              "field": "quote/rol_ly/epi_signed"
            }
          ]}
            kb-interactive={true}
            removeHorizontalScroll={true}
            syncColumnWidthsKey="line_size_table" />
        </HX.Section>
        <HX.Section title="RMS TP Calc"
          shownBy="cds/show_non_risk_xl">
          <HX.Pane>
            <HX.Notes field="cds/quote/rms_tp_calc_reins_information"
              title="Net Expected Loss Calculation Information" />
          </HX.Pane>
          <HX.Table title="Net Expected Loss"
            data={[
            "cds/layers"
          ]}
            fields={[
            {
              "field": "quote/rms_tp_calc/gross_lol"
            },
            null,
            {
              "field": "quote/rms_tp_calc/gross_el"
            },
            {
              "field": "quote/rms_tp_calc/gross_sd"
            },
            {
              "field": "quote/rms_tp_calc/model_limit_factor",
              "infoBy": "/cds/number_reins_factor_info"
            },
            {
              "field": "quote/rms_tp_calc/override_limit_factor"
            },
            {
              "field": "quote/rms_tp_calc/net_el_excl_reins_prem"
            },
            {
              "field": "quote/rms_tp_calc/no_expected_reins",
              "infoBy": "/cds/paid_reins_factor_info"
            },
            null,
            {
              "field": "quote/rms_tp_calc/net_el"
            },
            {
              "field": "quote/rms_tp_calc/net_sd"
            },
            null,
            {
              "field": "quote/rms_tp_calc/net_el_incl_bs"
            },
            {
              "field": "quote/rms_tp_calc/net_sd_incl_bs"
            }
          ]}
            kb-interactive={true} />
          <HX.Table title="Technical Premium Components"
            data={[
            "cds/layers"
          ]}
            fields={[
            {
              "field": "quote/rms_tp_calc/afb_net_el"
            },
            {
              "field": "quote/rms_tp_calc/afb_net_sd"
            },
            null,
            {
              "field": "quote/rms_tp_calc/indirect_expenses"
            },
            {
              "field": "quote/rms_tp_calc/direct_expenses"
            },
            {
              "field": "quote/rms_tp_calc/lae"
            },
            {
              "field": "quote/rms_tp_calc/total_expenses"
            },
            null,
            {
              "field": "quote/rms_tp_calc/mi_250"
            },
            {
              "field": "quote/rms_tp_calc/marginal_impact"
            },
            {
              "field": "quote/rms_tp_calc/capital_us"
            },
            {
              "field": "quote/rms_tp_calc/capital_intl"
            },
            {
              "field": "quote/rms_tp_calc/attritional_capital"
            },
            {
              "field": "quote/rms_tp_calc/total_capital"
            },
            {
              "field": "quote/rms_tp_calc/total_coc"
            },
            null,
            {
              "field": "quote/rms_tp_calc/ri_cost"
            }
          ]}
            kb-interactive={true} />
          <HX.Table title="Technical Premium Calculations"
            data={[
            "cds/layers"
          ]}
            fields={[
            {
              "field": "quote/rms_tp_calc/tp_calc_1",
              "infoBy": "/cds/tp_calc_1_info"
            },
            {
              "field": "quote/rms_tp_calc/tp_calc_2",
              "infoBy": "/cds/tp_calc_2_info"
            },
            {
              "field": "quote/rms_tp_calc/tp_calc_3",
              "infoBy": "/cds/tp_calc_3_info"
            },
            null,
            {
              "field": "quote/rms_tp_calc/tp_max_calculation"
            },
            {
              "field": "quote/rms_tp_calc/tp_final"
            },
            null,
            {
              "field": "quote/rms_tp_calc/tp_non_loss_cost"
            },
            null,
            {
              "field": "quote/rol_ty/rol_rms"
            }
          ]}
            kb-interactive={true} />
        </HX.Section>
        <HX.Section title="Other TP Calculations"
          shownBy="cds/show_non_risk_xl">
          <HX.Pane flow="right"
            reflow={false}>
            <HX.Pane ratio={2}>
              <HX.Table title="IVOR"
                data={[
                "cds/layers"
              ]}
                fields={[
                {
                  "field": "quote/ivor_tp_calc/afb_net_el"
                },
                {
                  "field": "quote/ivor_tp_calc/afb_net_sd"
                },
                null,
                {
                  "field": "quote/ivor_tp_calc/tp_final"
                },
                null,
                {
                  "field": "quote/rol_ty/rol_ivor"
                }
              ]}
                kb-interactive={true}
                syncColumnWidthsKey="other_tp_tables" />
            </HX.Pane>
            <HX.Pane ratio={1} />
          </HX.Pane>
          <HX.Pane flow="right"
            reflow={false}>
            <HX.Pane ratio={2}>
              <HX.Table title="AIR"
                data={[
                "cds/layers"
              ]}
                fields={[
                {
                  "field": "quote/air_tp_calc/afb_net_el"
                },
                {
                  "field": "quote/air_tp_calc/afb_net_sd"
                },
                null,
                {
                  "field": "quote/air_tp_calc/tp_final"
                },
                null,
                {
                  "field": "quote/rol_ty/rol_air"
                }
              ]}
                kb-interactive={true}
                syncColumnWidthsKey="other_tp_tables" />
            </HX.Pane>
            <HX.Pane ratio={1} />
          </HX.Pane>
          <HX.Pane flow="right"
            reflow={false}>
            <HX.Pane ratio={2}>
              <HX.Table title="Burn"
                data={[
                "cds/layers"
              ]}
                fields={[
                {
                  "field": "quote/burn_tp_calc/afb_net_el"
                },
                {
                  "field": "quote/burn_tp_calc/afb_net_sd"
                },
                null,
                {
                  "field": "quote/burn_tp_calc/tp_final"
                },
                null,
                {
                  "field": "quote/rol_ty/rol_burn"
                }
              ]}
                kb-interactive={true}
                syncColumnWidthsKey="other_tp_tables" />
            </HX.Pane>
            <HX.Pane ratio={1} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Technical Premium Breakdown"
          shownBy="cds/show_non_risk_xl">
          <HX.Pane flow="right">
            <CustomComponent title="Technical Premium (GN) - Calculation 1"
              data={[
              {
                "labelBy": "layer_index",
                "list": "cds/layers"
              }
            ]}
              traces={[
              {
                "color": "#F7CFEC",
                "field": "quote/rol_ty/weighted_el",
                "label": "EL"
              },
              {
                "color": "#6C0D7A",
                "field": "quote/rms_tp_calc/total_coc",
                "label": "Cost of Capital"
              },
              {
                "color": "#0C6122",
                "field": "quote/rms_tp_calc/ri_cost",
                "label": "RI Cost"
              },
              {
                "color": "#4FADC7",
                "field": "quote/rms_tp_calc/expenses_less_inv_income",
                "label": "Expenses less Inv. Inc."
              }
            ]}
              xAxisTickAngle={-45}
              gapBetweenBarsSize={0.05}
              barMode="stack"
              xAxisLabel="Layer"
              yAxisLabel="TP Component" />
            <CustomComponent title="Technical Premium (GN) - Calculation 2"
              data={[
              {
                "labelBy": "layer_index",
                "list": "cds/layers"
              }
            ]}
              traces={[
              {
                "color": "#F7CFEC",
                "field": "quote/rol_ty/weighted_el",
                "label": "EL"
              },
              {
                "color": "#6C0D7A",
                "field": "quote/rms_tp_calc/sd_load",
                "label": "SD Load"
              },
              {
                "color": "#4FADC7",
                "field": "quote/rms_tp_calc/expenses_less_inv_income",
                "label": "Expenses"
              }
            ]}
              xAxisTickAngle={-45}
              gapBetweenBarsSize={0.05}
              barMode="stack"
              xAxisLabel="Layer"
              yAxisLabel="TP Component" />
            <CustomComponent title="Technical Premium (GN) - Calculation 3"
              data={[
              {
                "labelBy": "layer_index",
                "list": "cds/layers"
              }
            ]}
              traces={[
              {
                "color": "#F7CFEC",
                "field": "quote/rol_ty/weighted_el",
                "label": "EL"
              },
              {
                "color": "#6C0D7A",
                "field": "quote/rms_tp_calc/calc_3_lr_load",
                "label": "LR Load"
              }
            ]}
              xAxisTickAngle={-45}
              gapBetweenBarsSize={0.05}
              barMode="stack"
              xAxisLabel="Layer"
              yAxisLabel="TP Component" />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="TP Notes"
        fullWidth={true}
        viewScale={0.7}
        shownBy="model_state/show_after_landing_page">
        <HX.Section title="TP Notes">
          <HX.Pane>
            <HX.Table data={[
              {
                "datum": "cds/quote/tp_calc_info/description"
              },
              {
                "datum": "cds/quote/tp_calc_info/value"
              },
              {
                "datum": "cds/quote/tp_calc_info/value_ly"
              }
            ]}
              fields={[
              {
                "field": "general_notes"
              },
              {
                "field": "default_line"
              },
              null,
              {
                "field": "tp_calc_1"
              },
              {
                "field": "tp_calc_2"
              },
              {
                "field": "tp_calc_3"
              },
              null,
              {
                "field": "lae"
              },
              {
                "field": "indirect_expenses"
              },
              {
                "field": "direct_expenses"
              },
              {
                "field": "inv_income"
              },
              {
                "field": "ri_cost"
              },
              {
                "field": "capital_alloc"
              },
              {
                "field": "roc"
              },
              {
                "field": "sd_load"
              }
            ]}
              kb-interactive={true}
              transpose={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="RI Loads">
          <HX.Pane>
            <HX.Table data={[
              {
                "datum": "cds/quote/tp_calc_info/ri_cost_ty",
                "width": 250
              },
              {
                "datum": "cds/quote/tp_calc_info/ri_cost_ly",
                "width": 250
              },
              {
                "datum": "cds/quote/tp_calc_info/mvt",
                "width": 250
              }
            ]}
              fields={[
              {
                "field": "north_east"
              },
              {
                "field": "mid_atlantic"
              },
              {
                "field": "carolinas"
              },
              {
                "field": "fl_se"
              },
              {
                "field": "fl_non_se"
              },
              {
                "field": "al_miss"
              },
              {
                "field": "louisiana"
              },
              {
                "field": "tx_east"
              },
              {
                "field": "tx_west"
              },
              {
                "field": "cal_south"
              },
              {
                "field": "cal_north"
              },
              {
                "field": "pnw"
              },
              {
                "field": "new_madrid"
              },
              {
                "field": "hawaii"
              },
              {
                "field": "us_wf"
              },
              null,
              {
                "field": "eu_ws"
              },
              {
                "field": "jp_eq"
              },
              {
                "field": "jp_ws"
              },
              {
                "field": "can_eq"
              },
              {
                "field": "caribbean_ws"
              }
            ]}
              kb-interactive={true}
              transpose={true} />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Peril Allocation"
        fullWidth={true}
        viewScale={0.7}
        shownBy="cds/show_non_risk_xl">
        <HX.Section title="Final Proportions">
          <HX.Table data={[
            "cds/layers"
          ]}
            fields={[
            "peril_allocation/final_proportions/el_eq",
            "peril_allocation/final_proportions/el_ws",
            "peril_allocation/final_proportions/el_scs",
            "peril_allocation/final_proportions/el_wf",
            "peril_allocation/final_proportions/el_winter",
            "peril_allocation/final_proportions/el_fl",
            "peril_allocation/final_proportions/el_other"
          ]}
            freezeLeft={0}
            rowHeaderSettings={{
            "width": 250
          }}
            kb-interactive={true} />
        </HX.Section>
        <HX.Section title="Methodology">
          <HX.Pane flow="right"
            reflow={false}>
            <HX.Pane>
              <HX.Collection numCols={2}
                fields={[
                "cds/peril_allocation_account_level/allocation_methodology",
                "cds/peril_allocation_account_level/include_ivor",
                "cds/peril_allocation_account_level/skip_peril_allocation"
              ]} />
            </HX.Pane>
            <HX.Pane>
              <HX.Button task="peril_allocation_task"
                title="Run Peril Allocation" />
            </HX.Pane>
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Peril Allocation Inputs">
          <HX.Table title="EQ"
            data={[
            "cds/layers"
          ]}
            fields={[
            "peril_allocation/rms_aal/el_eq",
            "peril_allocation/air_aal/el_eq",
            "peril_allocation/rms_el_approx/el_eq",
            "peril_allocation/air_el_approx/el_eq",
            "peril_allocation/ivor_aal/el_eq"
          ]}
            freezeLeft={0}
            rowHeaderSettings={{
            "width": 250
          }}
            kb-interactive={true} />
          <HX.Table title="WS"
            data={[
            "cds/layers"
          ]}
            fields={[
            "peril_allocation/rms_aal/el_ws",
            "peril_allocation/air_aal/el_ws",
            "peril_allocation/rms_el_approx/el_ws",
            "peril_allocation/air_el_approx/el_ws",
            "peril_allocation/ivor_aal/el_ws"
          ]}
            freezeLeft={0}
            rowHeaderSettings={{
            "width": 250
          }}
            kb-interactive={true} />
          <HX.Table title="SCS"
            data={[
            "cds/layers"
          ]}
            fields={[
            "peril_allocation/rms_aal/el_scs",
            "peril_allocation/air_aal/el_scs",
            "peril_allocation/rms_el_approx/el_scs",
            "peril_allocation/air_el_approx/el_scs",
            "peril_allocation/ivor_aal/el_scs"
          ]}
            freezeLeft={0}
            rowHeaderSettings={{
            "width": 250
          }}
            kb-interactive={true} />
          <HX.Table title="WF"
            data={[
            "cds/layers"
          ]}
            fields={[
            "peril_allocation/rms_aal/el_wf",
            "peril_allocation/air_aal/el_wf",
            "peril_allocation/rms_el_approx/el_wf",
            "peril_allocation/air_el_approx/el_wf",
            "peril_allocation/ivor_aal/el_wf"
          ]}
            freezeLeft={0}
            rowHeaderSettings={{
            "width": 250
          }}
            kb-interactive={true} />
          <HX.Table title="Winter"
            data={[
            "cds/layers"
          ]}
            fields={[
            "peril_allocation/rms_aal/el_winter",
            "peril_allocation/air_aal/el_winter",
            "peril_allocation/rms_el_approx/el_winter",
            "peril_allocation/air_el_approx/el_winter",
            "peril_allocation/ivor_aal/el_winter"
          ]}
            freezeLeft={0}
            rowHeaderSettings={{
            "width": 250
          }}
            kb-interactive={true} />
          <HX.Table title="FL"
            data={[
            "cds/layers"
          ]}
            fields={[
            "peril_allocation/rms_aal/el_fl",
            "peril_allocation/air_aal/el_fl",
            "peril_allocation/rms_el_approx/el_fl",
            "peril_allocation/air_el_approx/el_fl",
            "peril_allocation/ivor_aal/el_fl"
          ]}
            freezeLeft={0}
            rowHeaderSettings={{
            "width": 250
          }}
            kb-interactive={true} />
          <HX.Table title="Other"
            data={[
            "cds/layers"
          ]}
            fields={[
            "peril_allocation/rms_aal/el_other",
            "peril_allocation/air_aal/el_other",
            "peril_allocation/rms_el_approx/el_other",
            "peril_allocation/air_el_approx/el_other",
            "peril_allocation/ivor_aal/el_other"
          ]}
            freezeLeft={0}
            rowHeaderSettings={{
            "width": 250
          }}
            kb-interactive={true} />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Rate Change"
        fullWidth={true}
        viewScale={0.7}
        shownBy="model_state/show_after_landing_page">
        <HX.Section title="Rate Change Summary">
          <HX.Table title="This Year"
            data={[
            "cds/layers",
            null,
            {
              "datum": "cds",
              "labelBy": "cds/total_label"
            }
          ]}
            fields={[
            {
              "field": "rate_change/expiring_layer_to_use",
              "width": 200
            },
            {
              "field": "renewal_layer.read_only_option"
            },
            {
              "field": "layer_structure"
            },
            {
              "field": "summary/ty/reinstatement_description"
            },
            {
              "field": "summary/ty/rol_quote"
            },
            {
              "field": "summary/ty/rol_fot"
            },
            null,
            {
              "field": "rate_change/rol_ly_to_use"
            },
            {
              "field": "rate_change/rol_rebased"
            },
            null,
            {
              "field": "rate_change/risk_adjusted_rate_change"
            }
          ]}
            kb-interactive={true}
            syncColumnWidthsKey="rc_table" />
          <HX.Table title="Previous Year"
            data={[
            "cds/layers"
          ]}
            fields={[
            {
              "field": "rate_change/expiring_layer_to_use_ly",
              "width": 200
            },
            {
              "field": "renewal_layer_ly"
            },
            {
              "field": "layer_structure_ly"
            },
            {
              "field": "summary/ly/reinstatement_description"
            },
            {
              "field": "quote/rol_ly/rol_quote"
            },
            {
              "field": "quote/rol_ly/rol_fot"
            }
          ]}
            kb-interactive={true}
            syncColumnWidthsKey="rc_table" />
        </HX.Section>
        <HX.Section title="Rate Change Workings">
          <HX.Pane flow="right"
            reflow={false}>
            <HX.Pane>
              <HX.Notes stretch={true}
                field="cds/rate_change/comments"
                title="Rate Change Comments" />
            </HX.Pane>
            <HX.Pane>
              <HX.Collection numCols={2}
                fields={[
                "cds/send_rate_change/confirm_rate_change",
                null,
                {
                  "field": "cds/rate_change/risk_xl_exposure_selection",
                  "shownBy": "cds/show_risk_xl"
                }
              ]} />
            </HX.Pane>
          </HX.Pane>
          <HX.Button task="rate_change_task"
            title="Run Rate Change" />
          <HX.Table data={[
            "cds/layers"
          ]}
            fields={[
            {
              "field": "rate_change/exposure_selection",
              "shownBy": "cds/show_non_risk_xl"
            },
            {
              "field": "rate_change/exposure_increase",
              "shownBy": "cds/show_non_risk_xl"
            },
            null,
            {
              "field": "rate_change/exposure_change_fixed/model_calculated"
            },
            {
              "field": "rate_change/exposure_change_fixed/uw_selected"
            },
            null,
            {
              "field": "rate_change/limit_change_fixed/model_calculated"
            },
            {
              "field": "rate_change/limit_change_fixed/uw_selected"
            },
            null,
            {
              "field": "rate_change/other_change_fixed/uw_selected"
            },
            null,
            {
              "field": "rate_change/terms_conditions_change_fixed/uw_selected"
            },
            null,
            {
              "field": "rate_change/rebase_factor"
            },
            null,
            {
              "field": "rate_change/comments"
            }
          ]}
            kb-interactive={true} />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Summary"
        fullWidth={true}
        viewScale={0.7}
        shownBy="model_state/show_after_landing_page">
        <HX.Section title="Treaty Details">
          <HX.Pane flow="right"
            reflow={false}>
            <HX.Pane>
              <HX.Collection numCols={1}
                fields={[
                "cds/standard_fields/insured_name.read_only_option",
                "cds/programme.read_only_option",
                "cds/territorial_focus_group.read_only_option",
                "cds/standard_fields/inception_date",
                "cds/standard_fields/expiry_date",
                "cds/currency.read_only_option",
                "cds/standard_fields/is_renewal.read_only_option",
                "cds/calc_type.read_only_option"
              ]} />
            </HX.Pane>
            <HX.Pane>
              <HX.Collection numCols={1}
                fields={[
                "cds/brokerage.read_only_option",
                "cds/adj_base.read_only_option",
                "cds/standard_fields/underwriter.read_only_option",
                "cds/standard_fields/broker.read_only_option",
                "cds/broker_contact.read_only_option",
                "cds/hours_clause.read_only_option",
                "cds/sanctions_clause.read_only_option",
                "cds/core_account.read_only_option",
                "cds/terrorism_code.read_only_option",
                "cds/cyber_code.read_only_option",
                "cds/com_disease.read_only_option"
              ]} />
            </HX.Pane>
            <HX.Pane>
              <HX.Collection numCols={1}
                fields={[
                "cds/currency_policy_financials",
                {
                  "field": "cds/summary_fx_conversion",
                  "labelBy": "/cds/fx_conversion_label"
                },
                {
                  "field": "cds/summary_uwa_exposure",
                  "labelBy": "/cds/uwa_limit_label"
                },
                {
                  "field": "cds/summary_uwa_premium",
                  "labelBy": "/cds/uwa_premium_label"
                },
                {
                  "field": "cds/summary_uwa_warning"
                },
                {
                  "field": "cds/summary_eso_obtained",
                  "shownBy": "/cds/summary_show_eso_obtained"
                }
              ]} />
              <HX.Notes stretch={true}
                field="cds/summary_comments"
                title="Comments" />
            </HX.Pane>
            <HX.Pane>
              <HX.Table title="Historic GNEPI"
                data={[
                {
                  "datum": "cds/experience_rating/exposure/last_eight"
                }
              ]}
                fields={[
                {
                  "field": "year",
                  "width": 100
                },
                {
                  "field": "gnepi_actual",
                  "maxWidth": 400
                },
                {
                  "field": "gnepi_projected",
                  "maxWidth": 400
                }
              ]}
                kb-interactive={true} />
            </HX.Pane>
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Multi-Year"
          shownBy="cds/show_multi_year">
          <HX.Table title="Multi-year Summary"
            data={[
            "cds/summary/multi_year_summary_ty",
            "cds/summary/multi_year_summary_ly"
          ]}
            fields={[
            {
              "field": "line_written_summary_fx"
            },
            {
              "field": "line_estimated_summary_fx"
            },
            {
              "field": "line_signed_summary_fx"
            },
            {
              "field": "epi_written_summary_fx"
            },
            {
              "field": "epi_estimated_summary_fx"
            },
            {
              "field": "epi_signed_summary_fx"
            },
            {
              "field": "mi_250"
            },
            {
              "field": "mi_250_estimate_prem_ratio"
            },
            {
              "field": "mi_250_prem_ratio"
            }
          ]}
            kb-interactive={true} />
          <HX.Table title="Year After Next"
            data={[
            "cds/layers"
          ]}
            fields={[
            {
              "field": "layer_structure"
            },
            {
              "field": "summary/ty/multi_year_period.read_only_option",
              "shownBy": "cds/show_multi_year"
            },
            {
              "field": "summary/year_after_next/section_reference"
            },
            {
              "field": "leader.read_only_option"
            },
            {
              "field": "layer_description.read_only_option"
            },
            {
              "field": "limit_cnv",
              "labelBy": "/cds/limit_application_ccy_label"
            },
            {
              "field": "excess_cnv",
              "labelBy": "/cds/excess_application_ccy_label"
            },
            {
              "field": "quote/rol_ty/rol_quote.read_only_option"
            },
            {
              "field": "quote/rol_ty/rol_fot.read_only_option"
            },
            {
              "field": "quote/rol_ty/rol_afb_tech"
            },
            {
              "field": "summary/ty/reinstatement_description"
            },
            null,
            {
              "field": "summary/year_after_next/roc"
            },
            {
              "field": "summary/year_after_next/risk_adjusted_rate_change"
            },
            {
              "field": "summary/ty/bpi"
            },
            {
              "field": "summary/ty/fot_adequacy"
            },
            {
              "field": "summary/year_after_next/rms_adequacy"
            },
            {
              "field": "summary/ty/ulr"
            },
            {
              "field": "summary/ty/epi_adj_rate"
            },
            {
              "field": "summary/ty/prem_full_line",
              "labelBy": "/cds/prem_100_label"
            },
            null,
            {
              "field": "quote/rol_ty/written_line.read_only_option"
            },
            {
              "field": "summary/ty/line_written_summary_fx",
              "labelBy": "/cds/written_line_label"
            },
            {
              "field": "quote/rol_ty/estimated_signing.read_only_option"
            },
            {
              "field": "summary/ty/line_estimated_summary_fx",
              "labelBy": "/cds/estimated_line_label"
            },
            {
              "field": "quote/rol_ty/signed_line.read_only_option"
            },
            {
              "field": "summary/ty/line_signed_summary_fx",
              "labelBy": "/cds/signed_line_label"
            },
            null,
            {
              "field": "summary/ty/epi_written_summary_fx",
              "labelBy": "/cds/written_epi_label"
            },
            {
              "field": "summary/ty/epi_estimated_summary_fx",
              "labelBy": "/cds/estimated_epi_label"
            },
            {
              "field": "summary/ty/epi_signed_summary_fx",
              "labelBy": "/cds/signed_epi_label"
            },
            null,
            {
              "field": "summary/ty/mi_250"
            },
            {
              "field": "summary/ty/mi_250_prem_ratio"
            },
            {
              "field": "summary/ty/mi_10"
            },
            {
              "field": "summary/ty/mi_10_prem_ratio"
            },
            null,
            {
              "field": "summary/year_after_next/share",
              "shownBy": "cds/show_multi_year"
            }
          ]}
            filter="summary/year_after_next/show_row"
            removeHorizontalScroll={true}
            kb-interactive={true}
            syncColumnWidthsKey="future_year_tables" />
          <HX.Table title="Next Year"
            data={[
            "cds/layers"
          ]}
            fields={[
            {
              "field": "layer_structure"
            },
            {
              "field": "summary/ty/multi_year_period.read_only_option",
              "shownBy": "cds/show_multi_year"
            },
            {
              "field": "summary/next_year/section_reference"
            },
            {
              "field": "leader.read_only_option"
            },
            {
              "field": "layer_description.read_only_option"
            },
            {
              "field": "limit_cnv",
              "labelBy": "/cds/limit_application_ccy_label"
            },
            {
              "field": "excess_cnv",
              "labelBy": "/cds/excess_application_ccy_label"
            },
            {
              "field": "quote/rol_ty/rol_quote.read_only_option"
            },
            {
              "field": "quote/rol_ty/rol_fot.read_only_option"
            },
            {
              "field": "quote/rol_ty/rol_afb_tech"
            },
            {
              "field": "summary/ty/reinstatement_description"
            },
            null,
            {
              "field": "summary/next_year/roc"
            },
            {
              "field": "summary/next_year/risk_adjusted_rate_change"
            },
            {
              "field": "summary/ty/bpi"
            },
            {
              "field": "summary/ty/fot_adequacy"
            },
            {
              "field": "summary/next_year/rms_adequacy"
            },
            {
              "field": "summary/ty/ulr"
            },
            {
              "field": "summary/ty/epi_adj_rate"
            },
            {
              "field": "summary/ty/prem_full_line",
              "labelBy": "/cds/prem_100_label"
            },
            null,
            {
              "field": "quote/rol_ty/written_line.read_only_option"
            },
            {
              "field": "summary/ty/line_written_summary_fx",
              "labelBy": "/cds/written_line_label"
            },
            {
              "field": "quote/rol_ty/estimated_signing.read_only_option"
            },
            {
              "field": "summary/ty/line_estimated_summary_fx",
              "labelBy": "/cds/estimated_line_label"
            },
            {
              "field": "quote/rol_ty/signed_line.read_only_option"
            },
            {
              "field": "summary/ty/line_signed_summary_fx",
              "labelBy": "/cds/signed_line_label"
            },
            null,
            {
              "field": "summary/ty/epi_written_summary_fx",
              "labelBy": "/cds/written_epi_label"
            },
            {
              "field": "summary/ty/epi_estimated_summary_fx",
              "labelBy": "/cds/estimated_epi_label"
            },
            {
              "field": "summary/ty/epi_signed_summary_fx",
              "labelBy": "/cds/signed_epi_label"
            },
            null,
            {
              "field": "summary/ty/mi_250"
            },
            {
              "field": "summary/ty/mi_250_prem_ratio"
            },
            {
              "field": "summary/ty/mi_10"
            },
            {
              "field": "summary/ty/mi_10_prem_ratio",
              "shownBy": "cds/show_multi_year"
            },
            null,
            {
              "field": "summary/next_year/share"
            }
          ]}
            filter="summary/next_year/show_row"
            removeHorizontalScroll={true}
            kb-interactive={true}
            syncColumnWidthsKey="future_year_tables" />
        </HX.Section>
        <HX.Section title="Treaty Financials">
          <HX.Pane>
            <HX.Table title="This Year"
              data={[
              "cds/layers",
              null,
              {
                "datum": "cds",
                "labelBy": "cds/total_label"
              }
            ]}
              fields={[
              {
                "field": "layer_structure"
              },
              {
                "field": "summary/ty/multi_year_period",
                "shownBy": "cds/show_multi_year"
              },
              {
                "field": "section_reference.read_only_option"
              },
              {
                "field": "leader.read_only_option"
              },
              {
                "field": "layer_description.read_only_option"
              },
              {
                "field": "limit_cnv",
                "labelBy": "/cds/limit_application_ccy_label"
              },
              {
                "field": "excess_cnv",
                "labelBy": "/cds/excess_application_ccy_label"
              },
              {
                "field": "summary/ty/rol_quote"
              },
              {
                "field": "summary/ty/rol_fot"
              },
              {
                "field": "quote/rol_ty/rol_afb_tech"
              },
              {
                "field": "summary/ty/reinstatement_description"
              },
              null,
              {
                "field": "quote/rol_ty/roc"
              },
              {
                "field": "summary/ty/risk_adjusted_rate_change"
              },
              {
                "field": "summary/ty/bpi"
              },
              {
                "field": "summary/ty/fot_adequacy"
              },
              {
                "field": "summary/ty/rms_adequacy"
              },
              {
                "field": "summary/ty/ulr"
              },
              {
                "field": "summary/ty/epi_adj_rate"
              },
              {
                "field": "summary/ty/prem_full_line",
                "labelBy": "/cds/prem_100_label"
              },
              null,
              {
                "field": "quote/rol_ty/written_line.read_only_option"
              },
              {
                "field": "summary/ty/line_written_summary_fx",
                "labelBy": "/cds/written_line_label"
              },
              {
                "field": "quote/rol_ty/estimated_signing.read_only_option"
              },
              {
                "field": "summary/ty/line_estimated_summary_fx",
                "labelBy": "/cds/estimated_line_label"
              },
              {
                "field": "quote/rol_ty/signed_line.read_only_option"
              },
              {
                "field": "summary/ty/line_signed_summary_fx",
                "labelBy": "/cds/signed_line_label"
              },
              null,
              {
                "field": "summary/ty/epi_written_summary_fx",
                "labelBy": "/cds/written_epi_label"
              },
              {
                "field": "summary/ty/epi_estimated_summary_fx",
                "labelBy": "/cds/estimated_epi_label"
              },
              {
                "field": "summary/ty/epi_signed_summary_fx",
                "labelBy": "/cds/signed_epi_label"
              },
              null,
              {
                "field": "summary/ty/mi_250",
                "shownBy": "cds/show_non_risk_xl"
              },
              {
                "field": "summary/ty/mi_250_prem_ratio",
                "shownBy": "cds/show_non_risk_xl"
              },
              {
                "field": "summary/ty/mi_10",
                "shownBy": "cds/show_non_risk_xl"
              },
              {
                "field": "summary/ty/mi_10_prem_ratio",
                "shownBy": "cds/show_non_risk_xl"
              },
              null,
              {
                "field": "summary/ty/share",
                "shownBy": "cds/show_multi_year"
              }
            ]}
              kb-interactive={true}
              removeHorizontalScroll={true}
              syncColumnWidthsKey="this_year_and_prior_tables" />
            <HX.Table title="Previous Year"
              data={[
              "cds/layers",
              null,
              {
                "datum": "cds",
                "labelBy": "cds/total_label"
              }
            ]}
              fields={[
              {
                "field": "layer_structure_ly"
              },
              {
                "field": "summary/ly/current_year_section_reference",
                "shownBy": "cds/show_multi_year"
              },
              {
                "field": "section_reference_ly"
              },
              {
                "field": "leader_ly"
              },
              {
                "field": "layer_description_ly"
              },
              {
                "field": "limit_cnv_ly",
                "labelBy": "/cds/limit_application_ccy_label"
              },
              {
                "field": "excess_cnv_ly",
                "labelBy": "/cds/excess_application_ccy_label"
              },
              {
                "field": "quote/rol_ly/rol_quote"
              },
              {
                "field": "quote/rol_ly/rol_fot"
              },
              {
                "field": "quote/rol_ly/rol_afb_tech"
              },
              {
                "field": "summary/ly/reinstatement_description"
              },
              null,
              {
                "field": "quote/rol_ly/roc"
              },
              {
                "field": "summary/ly/risk_adjusted_rate_change"
              },
              {
                "field": "summary/ly/bpi"
              },
              {
                "field": "summary/ly/fot_adequacy"
              },
              {
                "field": "summary/ly/rms_adequacy"
              },
              {
                "field": "summary/ly/ulr"
              },
              {
                "field": "summary/ly/epi_adj_rate"
              },
              {
                "field": "summary/ly/prem_full_line",
                "labelBy": "/cds/prem_100_label"
              },
              null,
              {
                "field": "quote/rol_ly/written_line"
              },
              {
                "field": "summary/ly/line_written_summary_fx",
                "labelBy": "/cds/written_line_label"
              },
              {
                "field": "quote/rol_ly/estimated_signing"
              },
              {
                "field": "summary/ly/line_estimated_summary_fx",
                "labelBy": "/cds/estimated_line_label"
              },
              {
                "field": "quote/rol_ly/signed_line"
              },
              {
                "field": "summary/ly/line_signed_summary_fx",
                "labelBy": "/cds/signed_line_label"
              },
              null,
              {
                "field": "summary/ly/epi_written_summary_fx",
                "labelBy": "/cds/written_epi_label"
              },
              {
                "field": "summary/ly/epi_estimated_summary_fx",
                "labelBy": "/cds/estimated_epi_label"
              },
              {
                "field": "summary/ly/epi_signed_summary_fx",
                "labelBy": "/cds/signed_epi_label"
              },
              null,
              {
                "field": "summary/ly/mi_250",
                "shownBy": "cds/show_non_risk_xl"
              },
              {
                "field": "summary/ly/mi_250_prem_ratio",
                "shownBy": "cds/show_non_risk_xl"
              },
              {
                "field": "summary/ly/mi_10",
                "shownBy": "cds/show_non_risk_xl"
              },
              {
                "field": "summary/ly/mi_10_prem_ratio",
                "shownBy": "cds/show_non_risk_xl"
              },
              null,
              {
                "field": "summary/ly/current_year_share",
                "shownBy": "cds/show_multi_year"
              }
            ]}
              kb-interactive={true}
              removeHorizontalScroll={true}
              syncColumnWidthsKey="this_year_and_prior_tables" />
            <HX.Table title="Year Before Last"
              data={[
              "cds/layers",
              null,
              {
                "datum": "cds",
                "labelBy": "cds/total_label"
              }
            ]}
              fields={[
              {
                "field": "summary/year_before_last/layer_structure_year_before_last"
              },
              {
                "field": "summary/year_before_last/current_year_section_reference",
                "shownBy": "cds/show_multi_year"
              },
              {
                "field": "summary/year_before_last/section_reference"
              },
              {
                "field": "summary/year_before_last/leader"
              },
              {
                "field": "summary/year_before_last/layer_description"
              },
              {
                "field": "summary/year_before_last/limit_cnv",
                "labelBy": "/cds/limit_application_ccy_label"
              },
              {
                "field": "summary/year_before_last/excess_cnv",
                "labelBy": "/cds/excess_application_ccy_label"
              },
              {
                "field": "summary/year_before_last/rol_quote"
              },
              {
                "field": "summary/year_before_last/rol_fot"
              },
              {
                "field": "summary/year_before_last/rol_afb_tech"
              },
              {
                "field": "summary/year_before_last/reinstatement_description"
              },
              null,
              {
                "field": "summary/year_before_last/roc"
              },
              {
                "field": "summary/year_before_last/risk_adjusted_rate_change"
              },
              {
                "field": "summary/year_before_last/bpi"
              },
              {
                "field": "summary/year_before_last/fot_adequacy"
              },
              {
                "field": "summary/year_before_last/rms_adequacy"
              },
              {
                "field": "summary/year_before_last/ulr"
              },
              {
                "field": "summary/year_before_last/epi_adj_rate"
              },
              {
                "field": "summary/year_before_last/prem_full_line",
                "labelBy": "/cds/prem_100_label"
              },
              null,
              {
                "field": "summary/year_before_last/written_line"
              },
              {
                "field": "summary/year_before_last/line_written_summary_fx",
                "labelBy": "/cds/written_line_label"
              },
              {
                "field": "summary/year_before_last/estimated_signing"
              },
              {
                "field": "summary/year_before_last/line_estimated_summary_fx",
                "labelBy": "/cds/estimated_line_label"
              },
              {
                "field": "summary/year_before_last/signed_line"
              },
              {
                "field": "summary/year_before_last/line_signed_summary_fx",
                "labelBy": "/cds/signed_line_label"
              },
              null,
              {
                "field": "summary/year_before_last/epi_written_summary_fx",
                "labelBy": "/cds/written_epi_label"
              },
              {
                "field": "summary/year_before_last/epi_estimated_summary_fx",
                "labelBy": "/cds/estimated_epi_label"
              },
              {
                "field": "summary/year_before_last/epi_signed_summary_fx",
                "labelBy": "/cds/signed_epi_label"
              },
              null,
              {
                "field": "summary/year_before_last/mi_250",
                "shownBy": "cds/show_non_risk_xl"
              },
              {
                "field": "summary/year_before_last/mi_250_prem_ratio",
                "shownBy": "cds/show_non_risk_xl"
              },
              {
                "field": "summary/year_before_last/mi_10",
                "shownBy": "cds/show_non_risk_xl"
              },
              {
                "field": "summary/year_before_last/mi_10_prem_ratio",
                "shownBy": "cds/show_non_risk_xl"
              },
              null,
              {
                "field": "summary/year_before_last/current_year_share",
                "shownBy": "cds/show_multi_year"
              }
            ]}
              kb-interactive={true}
              removeHorizontalScroll={true}
              syncColumnWidthsKey="this_year_and_prior_tables" />
            <HX.Table title="Expiring Year"
              data={[
              "cds/layers",
              null,
              {
                "datum": "cds",
                "labelBy": "cds/total_label"
              }
            ]}
              fields={[
              {
                "field": "summary/expiring_year/layer_structure_expiring_year"
              },
              {
                "field": "summary/expiring_year/current_year_section_reference",
                "shownBy": "cds/show_multi_year"
              },
              {
                "field": "summary/expiring_year/section_reference"
              },
              {
                "field": "summary/expiring_year/leader"
              },
              {
                "field": "summary/expiring_year/layer_description"
              },
              {
                "field": "summary/expiring_year/limit_cnv",
                "labelBy": "/cds/limit_application_ccy_label"
              },
              {
                "field": "summary/expiring_year/excess_cnv",
                "labelBy": "/cds/excess_application_ccy_label"
              },
              {
                "field": "summary/expiring_year/rol_quote"
              },
              {
                "field": "summary/expiring_year/rol_fot"
              },
              {
                "field": "summary/expiring_year/rol_afb_tech"
              },
              {
                "field": "summary/expiring_year/reinstatement_description"
              },
              null,
              {
                "field": "summary/expiring_year/roc"
              },
              {
                "field": "summary/expiring_year/risk_adjusted_rate_change"
              },
              {
                "field": "summary/expiring_year/bpi"
              },
              {
                "field": "summary/expiring_year/fot_adequacy"
              },
              {
                "field": "summary/expiring_year/rms_adequacy"
              },
              {
                "field": "summary/expiring_year/ulr"
              },
              {
                "field": "summary/expiring_year/epi_adj_rate"
              },
              {
                "field": "summary/expiring_year/prem_full_line",
                "labelBy": "/cds/prem_100_label"
              },
              null,
              {
                "field": "summary/expiring_year/written_line"
              },
              {
                "field": "summary/expiring_year/line_written_summary_fx",
                "labelBy": "/cds/written_line_label"
              },
              {
                "field": "summary/expiring_year/estimated_signing"
              },
              {
                "field": "summary/expiring_year/line_estimated_summary_fx",
                "labelBy": "/cds/estimated_line_label"
              },
              {
                "field": "summary/expiring_year/signed_line"
              },
              {
                "field": "summary/expiring_year/line_signed_summary_fx",
                "labelBy": "/cds/signed_line_label"
              },
              null,
              {
                "field": "summary/expiring_year/epi_written_summary_fx",
                "labelBy": "/cds/written_epi_label"
              },
              {
                "field": "summary/expiring_year/epi_estimated_summary_fx",
                "labelBy": "/cds/estimated_epi_label"
              },
              {
                "field": "summary/expiring_year/epi_signed_summary_fx",
                "labelBy": "/cds/signed_epi_label"
              },
              null,
              {
                "field": "summary/expiring_year/mi_250",
                "shownBy": "cds/show_non_risk_xl"
              },
              {
                "field": "summary/expiring_year/mi_250_prem_ratio",
                "shownBy": "cds/show_non_risk_xl"
              },
              {
                "field": "summary/expiring_year/mi_10",
                "shownBy": "cds/show_non_risk_xl"
              },
              {
                "field": "summary/expiring_year/mi_10_prem_ratio",
                "shownBy": "cds/show_non_risk_xl"
              }
            ]}
              kb-interactive={true}
              removeHorizontalScroll={true}
              syncColumnWidthsKey="this_year_and_prior_tables" />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="ESO"
        fullWidth={true}
        viewScale={0.7}
        shownBy="model_state/show_after_landing_page">
        <HX.Section title="Send ESO">
          <HX.Pane flow="right"
            reflow={false}>
            <HX.Pane>
              <HX.Collection fields={[
                "cds/eso_template/email_recipients"
              ]} />
              <HX.Button task="send_eso_task"
                title="Send ESO" />
            </HX.Pane>
            <HX.Pane ratio={2} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Insured Details">
          <HX.Pane flow="right"
            reflow={false}>
            <HX.Pane ratio={1}>
              <HX.Collection numCols={1}
                fields={[
                "cds/standard_fields/insured_name.read_only_option",
                "cds/standard_fields/inception_date",
                "cds/standard_fields/expiry_date",
                null,
                "cds/eso_template/team",
                "cds/standard_fields/underwriter.read_only_option",
                "cds/currency_policy_financials.read_only_option",
                "cds/standard_fields/is_renewal.read_only_option",
                "cds/eso_template/cob_code",
                null,
                "cds/programme.read_only_option",
                "cds/risk_carrier.read_only_option",
                {
                  "field": "cds/discussed_london.read_only_option",
                  "shownBy": "cds/show_bermuda"
                },
                {
                  "field": "cds/technical_underwriter.read_only_option",
                  "shownBy": "cds/show_bermuda"
                }
              ]} />
            </HX.Pane>
            <HX.Pane ratio={2} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Metrics">
          <HX.Table title="This Year"
            data={[
            "cds/layers",
            null,
            {
              "datum": "cds",
              "labelBy": "cds/total_label"
            }
          ]}
            fields={[
            {
              "field": "layer_structure"
            },
            {
              "field": "section_reference.read_only_option"
            },
            {
              "field": "layer_description.read_only_option"
            },
            {
              "field": "limit_cnv",
              "labelBy": "/cds/limit_application_ccy_label"
            },
            {
              "field": "excess_cnv",
              "labelBy": "/cds/excess_application_ccy_label"
            },
            {
              "field": "summary/ty/rol_quote"
            },
            {
              "field": "summary/ty/rol_fot"
            },
            {
              "field": "quote/rol_ty/rol_afb_tech"
            },
            {
              "field": "summary/ty/reinstatement_description"
            },
            null,
            {
              "field": "summary/ty/risk_adjusted_rate_change"
            },
            {
              "field": "summary/ty/fot_adequacy"
            },
            {
              "field": "summary/ty/rms_adequacy"
            },
            {
              "field": "summary/ty/ulr"
            },
            {
              "field": "summary/ty/prem_full_line",
              "labelBy": "/cds/prem_100_label"
            },
            null,
            {
              "field": "quote/rol_ty/written_line.read_only_option"
            },
            {
              "field": "summary/ty/line_written_summary_fx",
              "labelBy": "/cds/written_line_label"
            },
            {
              "field": "quote/rol_ty/estimated_signing.read_only_option"
            },
            {
              "field": "summary/ty/line_estimated_summary_fx",
              "labelBy": "/cds/estimated_line_label"
            },
            null,
            {
              "field": "summary/ty/epi_written_summary_fx",
              "labelBy": "/cds/written_epi_label"
            },
            {
              "field": "summary/ty/epi_estimated_summary_fx",
              "labelBy": "/cds/estimated_epi_label"
            },
            null,
            {
              "field": "summary/ty/mi_250"
            }
          ]}
            kb-interactive={true} />
        </HX.Section>
        <HX.Section title="ESO Details">
          <HX.Pane flow="right"
            reflow={false}>
            <HX.Pane ratio={1}>
              <HX.Collection numCols={1}
                fields={[
                "cds/eso_template/authorising_uw",
                "cds/eso_template/date_of_authorisation"
              ]} />
            </HX.Pane>
            <HX.Pane ratio={2} />
          </HX.Pane>
          <HX.Pane flow="right"
            reflow={false}>
            <HX.Pane ratio={2}>
              <HX.Table title="This Year"
                data={[
                "cds/eso_template/requested",
                "cds/eso_template/uw_authority",
                "cds/eso_template/authorising_uw_authority"
              ]}
                fields={[
                {
                  "field": "request_note"
                },
                null,
                {
                  "field": "loa_premium"
                },
                {
                  "field": "loa_exposure",
                  "shownBy": "cds/show_multi_year"
                },
                {
                  "field": "loa_term"
                },
                {
                  "field": "loa_exposure_stacking"
                },
                {
                  "field": "unauthorised_cob_mop"
                },
                null,
                {
                  "field": "authority_as_at"
                }
              ]}
                kb-interactive={true}
                transpose={true} />
            </HX.Pane>
            <HX.Pane ratio={1} />
          </HX.Pane>
          <HX.Pane flow="right"
            reflow={false}>
            <HX.Pane ratio={1}>
              <HX.Collection numCols={1}
                fields={[
                "cds/eso_template/rag_level",
                "cds/eso_template/rag_triggers",
                {
                  "field": "cds/summary_eso_obtained"
                }
              ]} />
            </HX.Pane>
            <HX.Pane ratio={2} />
          </HX.Pane>
          <HX.Notes stretch={true}
            field="cds/eso_template/commentary"
            title="ESO Commentary" />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Simulation"
        fullWidth={true}
        viewScale={0.7}
        shownBy="cds/show_non_risk_xl">
        <HX.Section title="Simulation Summary">
          <HX.Pane>
            <HX.Table data={[
              {
                "datum": "cds/layers",
                "maxWidth": 250
              }
            ]}
              fields={[
              "limit.read_only_option",
              "excess.read_only_option",
              null,
              "simulation/sim_result/aal",
              "simulation/sim_result/subject_loss",
              null,
              "simulation/sim_result/gross_el_pre_inur",
              "simulation/sim_result/gross_sd_pre_inur",
              null,
              "simulation/sim_result/gross_el",
              "simulation/sim_result/gross_sd",
              null,
              "simulation/sim_result/net_el",
              "simulation/sim_result/net_sd"
            ]}
              freezeLeft={0}
              kb-interactive={true}
              transpose={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Simulation Parameters">
          <HX.Pane flow="right"
            reflow={false}>
            <HX.Pane ratio={2}>
              <HX.Collection numCols={2}
                fields={[
                "cds/simulation/max_sims",
                "cds/simulation/sims_commentary",
                "cds/simulation/exposure_increase",
                null,
                "cds/simulation/subject_lae",
                null,
                "cds/simulation/cut_off"
              ]}
                stretch={true} />
              <HX.Table title="Attritional Sim"
                data={[
                "cds/simulation/attritional_sim"
              ]}
                fields={[
                "mean",
                "sd"
              ]}
                kb-interactive={true} />
            </HX.Pane>
            <HX.Pane ratio={2} />
          </HX.Pane>
          <HX.Pane flow="right"
            reflow={false}>
            <HX.Table title="FHCF"
              data={[
              "cds/simulation/fhcf_1",
              "cds/simulation/fhcf_2"
            ]}
              fields={[
              {
                "field": "limit",
                "width": 250
              },
              {
                "field": "excess",
                "width": 250
              },
              {
                "field": "participation",
                "width": 250
              },
              {
                "field": "lae_cap",
                "width": 250
              },
              null,
              {
                "field": "el",
                "width": 250
              },
              {
                "field": "sd",
                "width": 250
              }
            ]}
              kb-interactive={true} />
          </HX.Pane>
          <HX.Pane flow="right"
            reflow={false}>
            <HX.Table title="Inuring Layers"
              with="cds/simulation/inuring_ri"
              data={[
              "inur_1",
              "inur_2",
              "inur_3",
              "inur_4"
            ]}
              fields={[
              {
                "field": "limit",
                "width": 250
              },
              {
                "field": "excess",
                "width": 250
              },
              {
                "field": "placed",
                "width": 250
              },
              {
                "field": "deductible_type",
                "width": 250
              },
              {
                "field": "reinstatements",
                "width": 250
              },
              {
                "field": "inur_lae",
                "width": 250
              }
            ]}
              kb-interactive={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="File Input">
          <HX.Pane flow="right"
            reflow={false}>
            <HX.Pane>
              <HX.Notes field="cds/simulation/format"
                title="ELT/YLT Required Format" />
            </HX.Pane>
            <HX.Pane />
          </HX.Pane>
          <HX.Pane flow="right"
            reflow={false}>
            <HX.File field="cds/simulation/files/input_file_1"
              title="Input File" />
            <HX.File field="cds/simulation/files/input_file_2"
              title="Input File" />
            <HX.File field="cds/simulation/files/input_file_3"
              title="Input File" />
            <HX.File field="cds/simulation/files/input_file_4"
              title="Input File" />
            <HX.File field="cds/simulation/files/input_file_5"
              title="Input File" />
            <HX.File field="cds/simulation/files/input_file_6"
              title="Input File" />
            <HX.File field="cds/simulation/files/input_file_7"
              title="Input File" />
            <HX.File field="cds/simulation/files/input_file_8"
              title="Input File" />
          </HX.Pane>
          <HX.Pane flow="right"
            reflow={false}>
            <HX.Button task="file_processing_task"
              title="Load Tables" />
            <HX.Button task="run_simulation_task"
              title="Run Simulation" />
          </HX.Pane>
          <HX.Pane>
            <HX.Table title="Table List"
              data={[
              "cds/simulation/file_list"
            ]}
              fields={[
              "file_name",
              "table_type",
              "max_sims",
              "table_el",
              "description",
              null,
              "qualifying_excess",
              "qualifying_limit",
              null,
              "fhcf_1",
              "fhcf_2",
              null,
              "inur_1",
              "inur_2",
              "inur_3",
              "inur_4"
            ]}
              kb-interactive={true} />
          </HX.Pane>
          <HX.Table title="Table Run Selection"
            data={[
            {
              "datum": "cds/layers",
              "width": 250
            }
          ]}
            fields={[
            "limit.read_only_option",
            "excess.read_only_option",
            null,
            "simulation/run_layer",
            null,
            {
              "field": "simulation/sim_coverage/coverage_1"
            },
            {
              "field": "simulation/sim_coverage/coverage_2"
            },
            {
              "field": "simulation/sim_coverage/coverage_3"
            },
            {
              "field": "simulation/sim_coverage/coverage_4"
            },
            {
              "field": "simulation/sim_coverage/coverage_5"
            },
            {
              "field": "simulation/sim_coverage/coverage_6"
            },
            {
              "field": "simulation/sim_coverage/coverage_7"
            },
            {
              "field": "simulation/sim_coverage/coverage_8"
            }
          ]}
            freezeLeft={0}
            kb-interactive={true}
            transpose={true} />
        </HX.Section>
        <HX.Section title="Total PML Comparison">
          <HX.Pane>
            <HX.Table title="OEP Curve Comparison"
              with="cds/simulation/pml_comparison"
              data={[
              "rp_labels",
              null,
              "simulation_gross",
              "simulation_net_inur",
              null,
              "model_gross",
              "model_net_inur",
              null,
              "difference_gross",
              "difference_net_inur"
            ]}
              fields={[
              "rp_10000",
              "rp_5000",
              "rp_1000",
              "rp_500",
              "rp_250",
              "rp_200",
              "rp_100",
              "rp_50",
              "rp_25",
              "rp_10",
              "rp_5",
              "rp_2"
            ]}
              transpose={true}
              kb-interactive={true} />
            <HX.Table title="AEP Curve Comparison"
              with="cds/simulation/pml_comparison"
              data={[
              "rp_labels",
              null,
              "simulation_gross_aep",
              "simulation_net_inur_aep",
              null,
              "model_gross_aep",
              "model_net_inur_aep",
              null,
              "difference_gross_aep",
              "difference_net_inur_aep"
            ]}
              fields={[
              "rp_10000",
              "rp_5000",
              "rp_1000",
              "rp_500",
              "rp_250",
              "rp_200",
              "rp_100",
              "rp_50",
              "rp_25",
              "rp_10",
              "rp_5",
              "rp_2",
              null,
              "aal"
            ]}
              transpose={true}
              kb-interactive={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Table PML Curves">
          <HX.Pane>
            <HX.Table title="OEP Curves"
              data={[
              "cds/simulation/file_list"
            ]}
              fields={[
              "description.read_only_option",
              null,
              "curve/rp_10000",
              "curve/rp_5000",
              "curve/rp_1000",
              "curve/rp_500",
              "curve/rp_250",
              "curve/rp_200",
              "curve/rp_100",
              "curve/rp_50",
              "curve/rp_25",
              "curve/rp_10",
              "curve/rp_5",
              "curve/rp_2",
              null,
              "aal"
            ]}
              transpose={true}
              kb-interactive={true} />
            <HX.Table title="AEP Curves"
              data={[
              "cds/simulation/file_list"
            ]}
              fields={[
              "description.read_only_option",
              null,
              "curve_aep/rp_10000",
              "curve_aep/rp_5000",
              "curve_aep/rp_1000",
              "curve_aep/rp_500",
              "curve_aep/rp_250",
              "curve_aep/rp_200",
              "curve_aep/rp_100",
              "curve_aep/rp_50",
              "curve_aep/rp_25",
              "curve_aep/rp_10",
              "curve_aep/rp_5",
              "curve_aep/rp_2",
              null,
              "aal"
            ]}
              transpose={true}
              kb-interactive={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="RMS Map">
          <HX.Pane flow="right">
            <HX.Pane>
              <HX.Table data={[
                "cds/simulation/choropleth_map",
                null,
                "cds/simulation/choropleth_caribbean",
                null,
                "cds/simulation/choropleth_other",
                null,
                "cds/simulation/total"
              ]}
                fields={[
                "state",
                "value"
              ]}
                freezeLeft={0}
                kb-interactive={true} />
            </HX.Pane>
            <HX.Pane>
              <CustomComponent title="AAL by State"
                list="cds/simulation/choropleth_map"
                text="hi"
                locations="state"
                z="value" />
            </HX.Pane>
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Peril-Layer">
          <HX.Pane>
            <HX.Table title="EL Percentage"
              data={[
              {
                "datum": "cds/layers"
              }
            ]}
              fields={[
              "layer_structure",
              null,
              {
                "field": "peril_allocation/simulation_perc/gross_table_0",
                "labelBy": "/cds/simulation/table_labels/gross_table_0"
              },
              {
                "field": "peril_allocation/simulation_perc/gross_table_1",
                "labelBy": "/cds/simulation/table_labels/gross_table_1"
              },
              {
                "field": "peril_allocation/simulation_perc/gross_table_2",
                "labelBy": "/cds/simulation/table_labels/gross_table_2"
              },
              {
                "field": "peril_allocation/simulation_perc/gross_table_3",
                "labelBy": "/cds/simulation/table_labels/gross_table_3"
              },
              {
                "field": "peril_allocation/simulation_perc/gross_table_4",
                "labelBy": "/cds/simulation/table_labels/gross_table_4"
              },
              {
                "field": "peril_allocation/simulation_perc/gross_table_5",
                "labelBy": "/cds/simulation/table_labels/gross_table_5"
              },
              {
                "field": "peril_allocation/simulation_perc/gross_table_6",
                "labelBy": "/cds/simulation/table_labels/gross_table_6"
              },
              {
                "field": "peril_allocation/simulation_perc/gross_table_7",
                "labelBy": "/cds/simulation/table_labels/gross_table_7"
              }
            ]}
              freezeLeft={0}
              kb-interactive={true}
              syncColumnWidthsKey="peril_layer_tables" />
            <HX.Table title="EL $"
              data={[
              {
                "datum": "cds/layers"
              }
            ]}
              fields={[
              "layer_structure",
              null,
              {
                "field": "peril_allocation/simulation_dollar/gross_table_0",
                "labelBy": "/cds/simulation/table_labels/gross_table_0"
              },
              {
                "field": "peril_allocation/simulation_dollar/gross_table_1",
                "labelBy": "/cds/simulation/table_labels/gross_table_1"
              },
              {
                "field": "peril_allocation/simulation_dollar/gross_table_2",
                "labelBy": "/cds/simulation/table_labels/gross_table_2"
              },
              {
                "field": "peril_allocation/simulation_dollar/gross_table_3",
                "labelBy": "/cds/simulation/table_labels/gross_table_3"
              },
              {
                "field": "peril_allocation/simulation_dollar/gross_table_4",
                "labelBy": "/cds/simulation/table_labels/gross_table_4"
              },
              {
                "field": "peril_allocation/simulation_dollar/gross_table_5",
                "labelBy": "/cds/simulation/table_labels/gross_table_5"
              },
              {
                "field": "peril_allocation/simulation_dollar/gross_table_6",
                "labelBy": "/cds/simulation/table_labels/gross_table_6"
              },
              {
                "field": "peril_allocation/simulation_dollar/gross_table_7",
                "labelBy": "/cds/simulation/table_labels/gross_table_7"
              }
            ]}
              freezeLeft={0}
              kb-interactive={true}
              syncColumnWidthsKey="peril_layer_tables" />
            <HX.Table title="STD $ (NB: Where tables are not independent (event overlap), sum of variances will not equal total variance.)"
              data={[
              {
                "datum": "cds/layers"
              }
            ]}
              fields={[
              "layer_structure",
              null,
              {
                "field": "peril_allocation/simulation_std_dollar/gross_table_0",
                "labelBy": "/cds/simulation/table_labels/gross_table_0"
              },
              {
                "field": "peril_allocation/simulation_std_dollar/gross_table_1",
                "labelBy": "/cds/simulation/table_labels/gross_table_1"
              },
              {
                "field": "peril_allocation/simulation_std_dollar/gross_table_2",
                "labelBy": "/cds/simulation/table_labels/gross_table_2"
              },
              {
                "field": "peril_allocation/simulation_std_dollar/gross_table_3",
                "labelBy": "/cds/simulation/table_labels/gross_table_3"
              },
              {
                "field": "peril_allocation/simulation_std_dollar/gross_table_4",
                "labelBy": "/cds/simulation/table_labels/gross_table_4"
              },
              {
                "field": "peril_allocation/simulation_std_dollar/gross_table_5",
                "labelBy": "/cds/simulation/table_labels/gross_table_5"
              },
              {
                "field": "peril_allocation/simulation_std_dollar/gross_table_6",
                "labelBy": "/cds/simulation/table_labels/gross_table_6"
              },
              {
                "field": "peril_allocation/simulation_std_dollar/gross_table_7",
                "labelBy": "/cds/simulation/table_labels/gross_table_7"
              }
            ]}
              freezeLeft={0}
              kb-interactive={true}
              syncColumnWidthsKey="peril_layer_tables" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Results For Copy">
          <HX.Pane>
            <HX.Table data={[
              {
                "datum": "cds/layers"
              }
            ]}
              fields={[
              {
                "field": "simulation/sim_result/gross_el",
                "width": 250
              },
              {
                "field": "simulation/sim_result/gross_sd",
                "width": 250
              }
            ]}
              freezeLeft={0}
              kb-interactive={true} />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="ELT / YLT File Formatter"
        fullWidth={true}
        viewScale={0.7}
        shownBy="cds/show_non_risk_xl">
        <HX.Section title="File Formatting">
          <HX.Pane flow="right"
            reflow={false}>
            <HX.Notes field="cds/simulation/format"
              title="ELT/YLT Required Format" />
          </HX.Pane>
          <HX.Pane flow="right"
            reflow={false}>
            <HX.Pane ratio={1}>
              <HX.File field="cds/simulation/file_formatter/input_file"
                title="Input File" />
            </HX.Pane>
            <HX.Pane ratio={2} />
          </HX.Pane>
          <HX.Pane>
            <HX.Button task="file_formatter_read_task"
              title="Read Input File" />
            <HX.Table title="Table Run Selection"
              data={[
              {
                "datum": "cds/simulation/file_formatter/file_column_names"
              },
              null,
              {
                "datum": "cds/simulation/file_formatter/override_column_names"
              }
            ]}
              fields={[
              {
                "field": "column_1"
              },
              {
                "field": "column_2"
              },
              {
                "field": "column_3"
              },
              {
                "field": "column_4"
              },
              {
                "field": "column_5"
              },
              {
                "field": "column_6"
              },
              {
                "field": "column_7"
              },
              {
                "field": "column_8"
              },
              {
                "field": "column_9"
              },
              {
                "field": "column_10"
              }
            ]}
              freezeLeft={0}
              kb-interactive={true} />
            <HX.Button task="file_formatter_write_task"
              title="Clean Columns" />
          </HX.Pane>
          <HX.Pane flow="right"
            reflow={false}>
            <HX.Pane ratio={1}>
              <HX.File field="cds/simulation/file_formatter/output_file"
                title="Output File" />
            </HX.Pane>
            <HX.Pane ratio={2} />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Calculator"
        fullWidth={true}
        viewScale={0.7}
        shownBy="model_state/show_after_landing_page">
        <HX.Section title="Calculator">
          <HX.Table data={[
            {
              "datum": "cds/calculator/input_list"
            },
            null,
            {
              "datum": "cds/calculator/results"
            }
          ]}
            fields={[
            {
              "field": "el",
              "maxWidth": 400
            },
            {
              "field": "sd",
              "maxWidth": 400
            }
          ]}
            freezeLeft={0}
            kb-interactive={true} />
        </HX.Section>
        <HX.Section title="Transposer">
          <HX.Table title="Modelling Sheet Output"
            data={[
            {
              "datum": "cds/calculator/transposer"
            }
          ]}
            fields={[
            {
              "field": "el"
            },
            {
              "field": "sd"
            }
          ]}
            freezeLeft={0}
            kb-interactive={true}
            transpose={true} />
          <HX.Table title="Transposed"
            data={[
            {
              "datum": "cds/calculator/transposer"
            }
          ]}
            fields={[
            {
              "field": "el.read_only_option",
              "maxWidth": 400
            },
            {
              "field": "sd.read_only_option",
              "maxWidth": 400
            }
          ]}
            freezeLeft={0}
            kb-interactive={true} />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Rate Change Synergy"
        fullWidth={true}
        viewScale={0.7}
        shownBy="model_state/show_after_landing_page">
        <HX.Section title="Rate Change Synergy">
          <HX.Pane>
            <HX.Table data={[
              "cds/layers"
            ]}
              fields={[
              {
                "field": "section_reference.read_only_option"
              },
              {
                "field": "layer_structure"
              },
              {
                "field": "layer_description.read_only_option"
              },
              null,
              {
                "field": "rate_change/rol_ly_to_use"
              },
              {
                "field": "rate_change/exposure_change_fixed/final"
              },
              {
                "field": "rate_change/risk_characteristics_change_fixed/final"
              },
              {
                "field": "rate_change/deductible_change_fixed/final"
              },
              {
                "field": "rate_change/limit_change_fixed/final"
              },
              {
                "field": "rate_change/terms_conditions_change_fixed/final"
              },
              {
                "field": "rate_change/other_change_fixed/final"
              },
              {
                "field": "rate_change/rol_rebased"
              },
              {
                "field": "quote/rol_ty/rol_fot.read_only_option"
              },
              {
                "field": "rate_change/risk_adjusted_rate_change"
              },
              null,
              {
                "field": "quote/rol_ty/est_sign_written_ratio"
              },
              {
                "field": "quote/rol_ty/ulr"
              },
              {
                "field": "quote/rol_ty/bpi"
              },
              null,
              {
                "field": "rate_change/rationale_outside_plan"
              }
            ]}
              kb-interactive={true}
              transpose={true} />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Rationale"
        fullWidth={false}
        viewScale={0.7}
        shownBy="model_state/show_after_landing_page">
        <HX.Section title=" ">
          <HX.Collection numCols={3}
            fields={[
            "cds/standard_fields/insured_name.read_only_option"
          ]} />
        </HX.Section>
        <HX.Section title="Underwriter Rationale">
          <HX.Notes field="cds/rationale/knowledge_comments"
            title="Knowledge of the reinsured" />
          <HX.Notes field="cds/rationale/portfolio_comments"
            title="Portfolio fit" />
          <HX.Notes field="cds/rationale/basis_comments"
            title="Basis of risk selection" />
          <HX.Notes field="cds/rationale/unusual_comments"
            title="Any unusual or complex considerations" />
          <HX.Notes field="cds/rationale/facts_comments"
            title="Facts which affect the underwriter's decision" />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Area Codes"
        fullWidth={true}
        viewScale={0.7}
        shownBy="model_state/show_after_landing_page">
        <HX.Section title="Summary">
          <HX.Pane>
            <HX.Collection numCols={4}
              fields={[
              "cds/send_rate_change/confirm_area_codes",
              null,
              null,
              null
            ]} />
            <HX.Table title="Total"
              data={[
              {
                "datum": "cds/layers"
              }
            ]}
              fields={[
              "area_codes_summary/europe",
              "area_codes_summary/us_aus",
              "area_codes_summary/can_car",
              "area_codes_summary/far_east_amei",
              null,
              "area_codes_summary/total"
            ]}
              kb-interactive={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Northern Europe, Southern Europe and CEE"
          shownBy="cds/show_intl_fields">
          <HX.Table title="EU EX WS Selector"
            data={[
            {
              "datum": "cds",
              "labelBy": "cds/blank_label",
              "maxWidth": 200
            },
            null,
            {
              "datum": "cds/layers",
              "maxWidth": 200
            }
          ]}
            fields={[
            "area_code_x_eu_ws"
          ]}
            kb-interactive={true}
            transpose={true}
            syncColumnWidthsKey="europe" />
          <HX.Pane>
            <HX.Table title="Northern Europe"
              data={[
              {
                "datum": "cds",
                "labelBy": "cds/area_code_label",
                "maxWidth": 200
              },
              null,
              {
                "datum": "cds/layers",
                "maxWidth": 200
              }
            ]}
              fields={[
              "area_codes_select/eat",
              "area_codes_perc/eat",
              null,
              "area_codes_select/ebe",
              "area_codes_perc/ebe",
              null,
              "area_codes_select/ech",
              "area_codes_perc/ech",
              null,
              "area_codes_select/edk",
              "area_codes_perc/edk",
              null,
              "area_codes_select/emz",
              "area_codes_perc/emz",
              null,
              "area_codes_select/efi",
              "area_codes_perc/efi",
              null,
              "area_codes_select/efr",
              "area_codes_perc/efr",
              null,
              "area_codes_select/ege",
              "area_codes_perc/ege",
              null,
              "area_codes_select/eic",
              "area_codes_perc/eic",
              null,
              "area_codes_select/eie",
              "area_codes_perc/eie",
              null,
              "area_codes_select/enl",
              "area_codes_perc/enl",
              null,
              "area_codes_select/eno",
              "area_codes_perc/eno",
              null,
              "area_codes_select/egf",
              "area_codes_perc/egf",
              null,
              "area_codes_select/ese",
              "area_codes_perc/ese",
              null,
              "area_codes_select/euk",
              "area_codes_perc/euk",
              null,
              "area_codes_select/euf",
              "area_codes_perc/euf"
            ]}
              kb-interactive={true}
              transpose={true}
              syncColumnWidthsKey="europe" />
            <HX.Table title="Southern Europe"
              data={[
              {
                "datum": "cds",
                "labelBy": "cds/area_code_label",
                "maxWidth": 200
              },
              null,
              {
                "datum": "cds/layers",
                "maxWidth": 200
              }
            ]}
              fields={[
              "area_codes_select/ees",
              "area_codes_perc/ees",
              null,
              "area_codes_select/egr",
              "area_codes_perc/egr",
              null,
              "area_codes_select/eit",
              "area_codes_perc/eit",
              null,
              "area_codes_select/ept",
              "area_codes_perc/ept",
              null,
              "area_codes_select/etu",
              "area_codes_perc/etu"
            ]}
              kb-interactive={true}
              transpose={true}
              syncColumnWidthsKey="europe" />
            <HX.Table title="CEE"
              data={[
              {
                "datum": "cds",
                "labelBy": "cds/area_code_label",
                "maxWidth": 200
              },
              null,
              {
                "datum": "cds/layers",
                "maxWidth": 200
              }
            ]}
              fields={[
              "area_codes_select/ebg",
              "area_codes_perc/ebg",
              null,
              "area_codes_select/cef",
              "area_codes_perc/cef",
              null,
              "area_codes_select/ecx",
              "area_codes_perc/ecx",
              null,
              "area_codes_select/ecz",
              "area_codes_perc/ecz",
              null,
              "area_codes_select/ehu",
              "area_codes_perc/ehu",
              null,
              "area_codes_select/epl",
              "area_codes_perc/epl",
              null,
              "area_codes_select/ero",
              "area_codes_perc/ero",
              null,
              "area_codes_select/eru",
              "area_codes_perc/eru",
              null,
              "area_codes_select/esb",
              "area_codes_perc/esb",
              null,
              "area_codes_select/esc",
              "area_codes_perc/esc",
              null,
              "area_codes_select/esr",
              "area_codes_perc/esr"
            ]}
              kb-interactive={true}
              transpose={true}
              syncColumnWidthsKey="europe" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="US, Latin America and Australia">
          <HX.Pane>
            <HX.Table title="US"
              data={[
              {
                "datum": "cds",
                "labelBy": "cds/area_code_label",
                "maxWidth": 200
              },
              null,
              {
                "datum": "cds/layers",
                "maxWidth": 200
              }
            ]}
              fields={[
              "area_codes_select/usa01",
              "area_codes_perc/usa01",
              null,
              "area_codes_select/usa02",
              "area_codes_perc/usa02",
              null,
              "area_codes_select/usa03",
              "area_codes_perc/usa03",
              null,
              "area_codes_select/usa04",
              "area_codes_perc/usa04",
              null,
              "area_codes_select/usa05",
              "area_codes_perc/usa05",
              null,
              "area_codes_select/usa06",
              "area_codes_perc/usa06",
              null,
              "area_codes_select/usa07",
              "area_codes_perc/usa07",
              null,
              "area_codes_select/usa08",
              "area_codes_perc/usa08",
              null,
              "area_codes_select/usa09",
              "area_codes_perc/usa09",
              null,
              "area_codes_select/usa10",
              "area_codes_perc/usa10",
              null,
              "area_codes_select/usa11",
              "area_codes_perc/usa11",
              null,
              "area_codes_select/usa12",
              "area_codes_perc/usa12",
              null,
              "area_codes_select/usa13",
              "area_codes_perc/usa13",
              null,
              "area_codes_select/usa14",
              "area_codes_perc/usa14",
              null,
              "area_codes_select/usa15",
              "area_codes_perc/usa15",
              null,
              "area_codes_select/usa16",
              "area_codes_perc/usa16",
              null,
              "area_codes_select/usa20",
              "area_codes_perc/usa20",
              null,
              "area_codes_select/usa21",
              "area_codes_perc/usa21",
              null,
              "area_codes_select/usa22",
              "area_codes_perc/usa22"
            ]}
              kb-interactive={true}
              transpose={true}
              syncColumnWidthsKey="us" />
            <HX.Table title="Latin America"
              data={[
              {
                "datum": "cds",
                "labelBy": "cds/area_code_label",
                "maxWidth": 200
              },
              null,
              {
                "datum": "cds/layers",
                "maxWidth": 200
              }
            ]}
              fields={[
              "area_codes_select/sar",
              "area_codes_perc/sar",
              null,
              "area_codes_select/sbz",
              "area_codes_perc/sbz",
              null,
              "area_codes_select/sbv",
              "area_codes_perc/sbv",
              null,
              "area_codes_select/sbr",
              "area_codes_perc/sbr",
              null,
              "area_codes_select/scl",
              "area_codes_perc/scl",
              null,
              "area_codes_select/sco",
              "area_codes_perc/sco",
              null,
              "area_codes_select/scr",
              "area_codes_perc/scr",
              null,
              "area_codes_select/sec",
              "area_codes_perc/sec",
              null,
              "area_codes_select/sel",
              "area_codes_perc/sel",
              null,
              "area_codes_select/sgt",
              "area_codes_perc/sgt",
              null,
              "area_codes_select/sgy",
              "area_codes_perc/sgy",
              null,
              "area_codes_select/shn",
              "area_codes_perc/shn",
              null,
              "area_codes_select/smx",
              "area_codes_perc/smx",
              null,
              "area_codes_select/snq",
              "area_codes_perc/snq",
              null,
              "area_codes_select/spa",
              "area_codes_perc/spa",
              null,
              "area_codes_select/spy",
              "area_codes_perc/spy",
              null,
              "area_codes_select/spe",
              "area_codes_perc/spe",
              null,
              "area_codes_select/suy",
              "area_codes_perc/suy",
              null,
              "area_codes_select/sve",
              "area_codes_perc/sve",
              null,
              "area_codes_select/ofg",
              "area_codes_perc/ofg"
            ]}
              kb-interactive={true}
              transpose={true}
              syncColumnWidthsKey="us" />
            <HX.Table title="Australia"
              data={[
              {
                "datum": "cds",
                "labelBy": "cds/area_code_label",
                "maxWidth": 200
              },
              null,
              {
                "datum": "cds/layers",
                "maxWidth": 200
              }
            ]}
              fields={[
              "area_codes_select/oa1",
              "area_codes_perc/oa1",
              null,
              "area_codes_select/oa2",
              "area_codes_perc/oa2",
              null,
              "area_codes_select/oa3",
              "area_codes_perc/oa3",
              null,
              "area_codes_select/oa4",
              "area_codes_perc/oa4",
              null,
              "area_codes_select/oa5",
              "area_codes_perc/oa5",
              null,
              "area_codes_select/oa6",
              "area_codes_perc/oa6",
              null,
              "area_codes_select/ota",
              "area_codes_perc/ota",
              null,
              "area_codes_select/onz",
              "area_codes_perc/onz",
              null,
              "area_codes_select/ofj",
              "area_codes_perc/ofj"
            ]}
              kb-interactive={true}
              transpose={true}
              syncColumnWidthsKey="us" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Caribbean and Canada"
          shownBy="cds/show_intl_fields">
          <HX.Pane>
            <HX.Table title="Caribbean"
              data={[
              {
                "datum": "cds",
                "labelBy": "cds/area_code_label",
                "maxWidth": 200
              },
              null,
              {
                "datum": "cds/layers",
                "maxWidth": 200
              }
            ]}
              fields={[
              "area_codes_select/bag",
              "area_codes_perc/bag",
              null,
              "area_codes_select/bah",
              "area_codes_perc/bah",
              null,
              "area_codes_select/ban",
              "area_codes_perc/ban",
              null,
              "area_codes_select/bbb",
              "area_codes_perc/bbb",
              null,
              "area_codes_select/bbh",
              "area_codes_perc/bbh",
              null,
              "area_codes_select/bbm",
              "area_codes_perc/bbm",
              null,
              "area_codes_select/bcb",
              "area_codes_perc/bcb",
              null,
              "area_codes_select/bcm",
              "area_codes_perc/bcm",
              null,
              "area_codes_select/bcu",
              "area_codes_perc/bcu",
              null,
              "area_codes_select/bdo",
              "area_codes_perc/bdo",
              null,
              "area_codes_select/bdr",
              "area_codes_perc/bdr",
              null,
              "area_codes_select/bgn",
              "area_codes_perc/bgn",
              null,
              "area_codes_select/bgs",
              "area_codes_perc/bgs",
              null,
              "area_codes_select/bgu",
              "area_codes_perc/bgu",
              null,
              "area_codes_select/bht",
              "area_codes_perc/bht",
              null,
              "area_codes_select/bjm",
              "area_codes_perc/bjm",
              null,
              "area_codes_select/bkn",
              "area_codes_perc/bkn",
              null,
              "area_codes_select/bmq",
              "area_codes_perc/bmq",
              null,
              "area_codes_select/bms",
              "area_codes_perc/bms",
              null,
              "area_codes_select/bon",
              "area_codes_perc/bon",
              null,
              "area_codes_select/bpr",
              "area_codes_perc/bpr",
              null,
              "area_codes_select/bsl",
              "area_codes_perc/bsl",
              null,
              "area_codes_select/bsv",
              "area_codes_perc/bsv",
              null,
              "area_codes_select/bv1",
              "area_codes_perc/bv1",
              null,
              "area_codes_select/bvs",
              "area_codes_perc/bvs",
              null,
              "area_codes_select/bx7",
              "area_codes_perc/bx7"
            ]}
              kb-interactive={true}
              transpose={true}
              syncColumnWidthsKey="carr" />
            <HX.Table title="Canada"
              data={[
              {
                "datum": "cds",
                "labelBy": "cds/area_code_label",
                "maxWidth": 200
              },
              null,
              {
                "datum": "cds/layers",
                "maxWidth": 200
              }
            ]}
              fields={[
              "area_codes_select/cbc",
              "area_codes_perc/cbc",
              null,
              "area_codes_select/cqu",
              "area_codes_perc/cqu",
              null,
              "area_codes_select/con",
              "area_codes_perc/con",
              null,
              "area_codes_select/cpr",
              "area_codes_perc/cpr",
              null,
              "area_codes_select/cat",
              "area_codes_perc/cat",
              null,
              "area_codes_select/bpm",
              "area_codes_perc/bpm"
            ]}
              kb-interactive={true}
              transpose={true}
              syncColumnWidthsKey="carr" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Far East and AMEI"
          shownBy="cds/show_intl_fields">
          <HX.Pane>
            <HX.Table title="Far East"
              data={[
              {
                "datum": "cds",
                "labelBy": "cds/area_code_label",
                "maxWidth": 200
              },
              null,
              {
                "datum": "cds/layers",
                "maxWidth": 200
              }
            ]}
              fields={[
              "area_codes_select/fct",
              "area_codes_perc/fct",
              null,
              "area_codes_select/fcq",
              "area_codes_perc/fcq",
              null,
              "area_codes_select/fkr",
              "area_codes_perc/fkr",
              null,
              "area_codes_select/fhk",
              "area_codes_perc/fhk",
              null,
              "area_codes_select/fia",
              "area_codes_perc/fia",
              null,
              "area_codes_select/oph",
              "area_codes_perc/oph",
              null,
              "area_codes_select/fsp",
              "area_codes_perc/fsp",
              null,
              "area_codes_select/fsk",
              "area_codes_perc/fsk",
              null,
              "area_codes_select/fta",
              "area_codes_perc/fta",
              null,
              "area_codes_select/fjq",
              "area_codes_perc/fjq",
              null,
              "area_codes_select/fjw",
              "area_codes_perc/fjw",
              null,
              "area_codes_select/mbd",
              "area_codes_perc/mbd",
              null,
              "area_codes_select/fcy",
              "area_codes_perc/fcy",
              null,
              "area_codes_select/ogm",
              "area_codes_perc/ogm",
              null,
              "area_codes_select/fmy",
              "area_codes_perc/fmy",
              null,
              "area_codes_select/mma",
              "area_codes_perc/mma",
              null,
              "area_codes_select/fby",
              "area_codes_perc/fby",
              null,
              "area_codes_select/fnp",
              "area_codes_perc/fnp",
              null,
              "area_codes_select/mpk",
              "area_codes_perc/mpk",
              null,
              "area_codes_select/opg",
              "area_codes_perc/opg",
              null,
              "area_codes_select/fth",
              "area_codes_perc/fth",
              null,
              "area_codes_select/fvn",
              "area_codes_perc/fvn"
            ]}
              kb-interactive={true}
              transpose={true}
              syncColumnWidthsKey="far_east" />
            <HX.Table title="AMEI"
              data={[
              {
                "datum": "cds",
                "labelBy": "cds/area_code_label",
                "maxWidth": 200
              },
              null,
              {
                "datum": "cds/layers",
                "maxWidth": 200
              }
            ]}
              fields={[
              "area_codes_select/mis",
              "area_codes_perc/mis",
              null,
              "area_codes_select/min",
              "area_codes_perc/min",
              null,
              "area_codes_select/asa",
              "area_codes_perc/asa",
              null,
              "area_codes_select/mae",
              "area_codes_perc/mae",
              null,
              "area_codes_select/mba",
              "area_codes_perc/mba",
              null,
              "area_codes_select/aal",
              "area_codes_perc/aal",
              null,
              "area_codes_select/amo",
              "area_codes_perc/amo",
              null,
              "area_codes_select/aeg",
              "area_codes_perc/aeg",
              null,
              "area_codes_select/ali",
              "area_codes_perc/ali",
              null,
              "area_codes_select/amu",
              "area_codes_perc/amu",
              null,
              "area_codes_select/mjo",
              "area_codes_perc/mjo",
              null,
              "area_codes_select/mom",
              "area_codes_perc/mom",
              null,
              "area_codes_select/mqa",
              "area_codes_perc/mqa",
              null,
              "area_codes_select/ayt",
              "area_codes_perc/ayt",
              null,
              "area_codes_select/agi",
              "area_codes_perc/agi"
            ]}
              kb-interactive={true}
              transpose={true}
              syncColumnWidthsKey="far_east" />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Pre Bind"
        fullWidth={true}
        viewScale={0.7}
        shownBy="model_state/show_after_landing_page">
        <HX.Section title="Pre Bind">
          <HX.Collection numCols={3}
            fields={[
            "cds/standard_fields/insured_name.read_only_option",
            "cds/standard_fields/underwriter.read_only_option"
          ]} />
          <HX.Pane>
            <HX.Table title=" By signing below I confirm that the answer to all of the following questions is "Yes": "
              data={[
              "cds/pre_bind/question",
              {
                "datum": "cds/pre_bind/answer",
                "width": 100
              }
            ]}
              fields={[
              {
                "field": "q_1",
                "labelAlign": "left"
              },
              {
                "field": "q_2",
                "labelAlign": "left"
              },
              {
                "field": "q_3",
                "labelAlign": "left"
              },
              {
                "field": "q_4",
                "labelAlign": "left"
              },
              {
                "field": "q_5",
                "labelAlign": "left"
              },
              {
                "field": "q_6",
                "labelAlign": "left"
              },
              {
                "field": "q_7",
                "labelAlign": "left"
              }
            ]}
              transpose={true}
              kb-interactive={true} />
          </HX.Pane>
          <HX.Collection numCols={1}
            fields={[
            "cds/pre_bind/uw_signature",
            "cds/pre_bind/date"
          ]} />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Post Bind"
        fullWidth={true}
        viewScale={0.7}
        shownBy="model_state/show_after_landing_page">
        <HX.Section title="In Progress">
          <HX.Collection numCols={3}
            fields={[
            "cds/standard_fields/insured_name.read_only_option",
            "cds/standard_fields/underwriter.read_only_option"
          ]} />
          <HX.Pane>
            <HX.Table title="APPLICABLE TO ALL SLIP HEADINGS WITHIN THIS SLIP SECTION:"
              data={[
              {
                "datum": "cds/post_bind/question",
                "maxWidth": 1000
              },
              {
                "datum": "cds/post_bind/answer",
                "width": 250
              },
              {
                "datum": "cds/post_bind/comments",
                "width": 500
              }
            ]}
              fields={[
              {
                "field": "q_1",
                "labelAlign": "left"
              },
              {
                "field": "q_2",
                "labelAlign": "left"
              },
              {
                "field": "q_3",
                "labelAlign": "left"
              }
            ]}
              transpose={true}
              kb-interactive={true} />
            <HX.Table title="APPLICABLE TO WHOLE SLIP: "
              data={[
              {
                "datum": "cds/post_bind/question",
                "maxWidth": 1000
              },
              {
                "datum": "cds/post_bind/answer",
                "width": 250
              },
              {
                "datum": "cds/post_bind/comments",
                "width": 500
              }
            ]}
              fields={[
              {
                "field": "q_4",
                "labelAlign": "left"
              },
              {
                "field": "q_5",
                "labelAlign": "left"
              },
              {
                "field": "q_6",
                "labelAlign": "left"
              }
            ]}
              transpose={true}
              kb-interactive={true} />
            <HX.Table title="CONDITIONS:"
              data={[
              {
                "datum": "cds/post_bind/question",
                "maxWidth": 1000
              },
              {
                "datum": "cds/post_bind/answer",
                "width": 250
              },
              {
                "datum": "cds/post_bind/comments",
                "width": 500
              }
            ]}
              fields={[
              {
                "field": "q_7",
                "labelAlign": "left"
              },
              {
                "field": "q_8",
                "labelAlign": "left"
              }
            ]}
              transpose={true}
              kb-interactive={true} />
            <HX.Table title="SUBJECTIVITIES:"
              data={[
              {
                "datum": "cds/post_bind/question",
                "maxWidth": 1000
              },
              {
                "datum": "cds/post_bind/answer",
                "width": 250
              },
              {
                "datum": "cds/post_bind/comments",
                "width": 500
              }
            ]}
              fields={[
              {
                "field": "q_9",
                "labelAlign": "left"
              }
            ]}
              transpose={true}
              kb-interactive={true} />
            <HX.Table title="CHOICE OF LAW & JURISDICTION/CONDITIONS: "
              data={[
              {
                "datum": "cds/post_bind/question",
                "maxWidth": 1000
              },
              {
                "datum": "cds/post_bind/answer",
                "width": 250
              },
              {
                "datum": "cds/post_bind/comments",
                "width": 500
              }
            ]}
              fields={[
              {
                "field": "q_10",
                "labelAlign": "left"
              }
            ]}
              transpose={true}
              kb-interactive={true} />
            <HX.Table title="PREMIUM"
              data={[
              {
                "datum": "cds/post_bind/question",
                "maxWidth": 1000
              },
              {
                "datum": "cds/post_bind/answer",
                "width": 250
              },
              {
                "datum": "cds/post_bind/comments",
                "width": 500
              }
            ]}
              fields={[
              {
                "field": "q_11",
                "labelAlign": "left"
              },
              {
                "field": "q_12",
                "labelAlign": "left"
              }
            ]}
              transpose={true}
              kb-interactive={true} />
            <HX.Table title="INSURER CONTRACT DOCUMENTATION: "
              data={[
              {
                "datum": "cds/post_bind/question",
                "maxWidth": 1000
              },
              {
                "datum": "cds/post_bind/answer",
                "width": 250
              },
              {
                "datum": "cds/post_bind/comments",
                "width": 500
              }
            ]}
              fields={[
              {
                "field": "q_13",
                "labelAlign": "left"
              }
            ]}
              transpose={true}
              kb-interactive={true} />
            <HX.Table title="INFORMATION"
              data={[
              {
                "datum": "cds/post_bind/question",
                "maxWidth": 1000
              },
              {
                "datum": "cds/post_bind/answer",
                "width": 250
              },
              {
                "datum": "cds/post_bind/comments",
                "width": 500
              }
            ]}
              fields={[
              {
                "field": "q_14",
                "labelAlign": "left"
              }
            ]}
              transpose={true}
              kb-interactive={true} />
            <HX.Table title="(RE)INSURER' S LIABILITY:"
              data={[
              {
                "datum": "cds/post_bind/question",
                "maxWidth": 1000
              },
              {
                "datum": "cds/post_bind/answer",
                "width": 250
              },
              {
                "datum": "cds/post_bind/comments",
                "width": 500
              }
            ]}
              fields={[
              {
                "field": "q_15",
                "labelAlign": "left"
              }
            ]}
              transpose={true}
              kb-interactive={true} />
            <HX.Table title="SIGNING PROVISIONS:"
              data={[
              {
                "datum": "cds/post_bind/question",
                "maxWidth": 1000
              },
              {
                "datum": "cds/post_bind/answer",
                "width": 250
              },
              {
                "datum": "cds/post_bind/comments",
                "width": 500
              }
            ]}
              fields={[
              {
                "field": "q_16",
                "labelAlign": "left"
              }
            ]}
              transpose={true}
              kb-interactive={true} />
            <HX.Table title="INSURER'S WRITTEN LINE: "
              data={[
              {
                "datum": "cds/post_bind/question",
                "maxWidth": 1000
              },
              {
                "datum": "cds/post_bind/answer",
                "width": 250
              },
              {
                "datum": "cds/post_bind/comments",
                "width": 500
              }
            ]}
              fields={[
              {
                "field": "q_17",
                "labelAlign": "left"
              }
            ]}
              transpose={true}
              kb-interactive={true} />
            <HX.Table title="SLIP LEADER:"
              data={[
              {
                "datum": "cds/post_bind/question",
                "maxWidth": 1000
              },
              {
                "datum": "cds/post_bind/answer",
                "width": 250
              },
              {
                "datum": "cds/post_bind/comments",
                "width": 500
              }
            ]}
              fields={[
              {
                "field": "q_18",
                "labelAlign": "left"
              }
            ]}
              transpose={true}
              kb-interactive={true} />
            <HX.Table title="CONTRACT CHANGES:"
              data={[
              {
                "datum": "cds/post_bind/question",
                "maxWidth": 1000
              },
              {
                "datum": "cds/post_bind/answer",
                "width": 250
              },
              {
                "datum": "cds/post_bind/comments",
                "width": 500
              }
            ]}
              fields={[
              {
                "field": "q_19",
                "labelAlign": "left"
              },
              {
                "field": "q_20",
                "labelAlign": "left"
              },
              {
                "field": "q_21",
                "labelAlign": "left"
              }
            ]}
              transpose={true}
              kb-interactive={true} />
            <HX.Table title="CLAIMS:"
              data={[
              {
                "datum": "cds/post_bind/question",
                "maxWidth": 1000
              },
              {
                "datum": "cds/post_bind/answer",
                "width": 250
              },
              {
                "datum": "cds/post_bind/comments",
                "width": 500
              }
            ]}
              fields={[
              {
                "field": "q_22",
                "labelAlign": "left"
              },
              {
                "field": "q_23",
                "labelAlign": "left"
              },
              {
                "field": "q_24",
                "labelAlign": "left"
              }
            ]}
              transpose={true}
              kb-interactive={true} />
            <HX.Table title="RULES AND EXTENT OF ANY OTHER DELEGATED CLAIMS AUTHORITY: "
              data={[
              {
                "datum": "cds/post_bind/question",
                "maxWidth": 1000
              },
              {
                "datum": "cds/post_bind/answer",
                "width": 250
              },
              {
                "datum": "cds/post_bind/comments",
                "width": 500
              }
            ]}
              fields={[
              {
                "field": "q_25",
                "labelAlign": "left"
              }
            ]}
              transpose={true}
              kb-interactive={true} />
            <HX.Table title="EXPERT(S) FEES COLLECTION: "
              data={[
              {
                "datum": "cds/post_bind/question",
                "maxWidth": 1000
              },
              {
                "datum": "cds/post_bind/answer",
                "width": 250
              },
              {
                "datum": "cds/post_bind/comments",
                "width": 500
              }
            ]}
              fields={[
              {
                "field": "q_26",
                "labelAlign": "left"
              }
            ]}
              transpose={true}
              kb-interactive={true} />
            <HX.Table title="OVERSEAS BROKER: "
              data={[
              {
                "datum": "cds/post_bind/question",
                "maxWidth": 1000
              },
              {
                "datum": "cds/post_bind/answer",
                "width": 250
              },
              {
                "datum": "cds/post_bind/comments",
                "width": 500
              }
            ]}
              fields={[
              {
                "field": "q_27",
                "labelAlign": "left"
              }
            ]}
              transpose={true}
              kb-interactive={true} />
            <HX.Table title="US CLASSIFICATION:"
              data={[
              {
                "datum": "cds/post_bind/question",
                "maxWidth": 1000
              },
              {
                "datum": "cds/post_bind/answer",
                "width": 250
              },
              {
                "datum": "cds/post_bind/comments",
                "width": 500
              }
            ]}
              fields={[
              {
                "field": "q_28",
                "labelAlign": "left"
              }
            ]}
              transpose={true}
              kb-interactive={true} />
            <HX.Table title="CLIENT CLASSIFICATION: "
              data={[
              {
                "datum": "cds/post_bind/question",
                "maxWidth": 1000
              },
              {
                "datum": "cds/post_bind/answer",
                "width": 250
              },
              {
                "datum": "cds/post_bind/comments",
                "width": 500
              }
            ]}
              fields={[
              {
                "field": "q_29",
                "labelAlign": "left"
              }
            ]}
              transpose={true}
              kb-interactive={true} />
            <HX.Table title="DISTANCE MARKETING DIRECTIVE: "
              data={[
              {
                "datum": "cds/post_bind/question",
                "maxWidth": 1000
              },
              {
                "datum": "cds/post_bind/answer",
                "width": 250
              },
              {
                "datum": "cds/post_bind/comments",
                "width": 500
              }
            ]}
              fields={[
              {
                "field": "q_30",
                "labelAlign": "left"
              }
            ]}
              transpose={true}
              kb-interactive={true} />
            <HX.Table title="DEDUCTIONS"
              data={[
              {
                "datum": "cds/post_bind/question",
                "maxWidth": 1000
              },
              {
                "datum": "cds/post_bind/answer",
                "width": 250
              },
              {
                "datum": "cds/post_bind/comments",
                "width": 500
              }
            ]}
              fields={[
              {
                "field": "q_31",
                "labelAlign": "left"
              },
              {
                "field": "q_32",
                "labelAlign": "left"
              }
            ]}
              transpose={true}
              kb-interactive={true} />
            <HX.Table title="SYNDICATE SPLIT:"
              data={[
              {
                "datum": "cds/post_bind/question",
                "maxWidth": 1000
              },
              {
                "datum": "cds/post_bind/answer",
                "width": 250
              },
              {
                "datum": "cds/post_bind/comments",
                "width": 500
              }
            ]}
              fields={[
              {
                "field": "q_33",
                "labelAlign": "left"
              }
            ]}
              transpose={true}
              kb-interactive={true} />
            <HX.Table title="Regulatory Risk Location:"
              data={[
              {
                "datum": "cds/post_bind/question",
                "maxWidth": 1000
              },
              {
                "datum": "cds/post_bind/answer",
                "width": 250
              },
              {
                "datum": "cds/post_bind/comments",
                "width": 500
              }
            ]}
              fields={[
              {
                "field": "q_34",
                "labelAlign": "left"
              }
            ]}
              transpose={true}
              kb-interactive={true} />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Automatic Front Sheet"
        fullWidth={false}
        viewScale={0.7}
        shownBy="model_state/show_after_landing_page">
        <HX.Section title="Front Sheet">
          <HX.Pane>
            <HX.Collection numCols={2}
              fields={[
              {
                "field": "synergy_upload/to_user_only"
              },
              null
            ]} />
          </HX.Pane>
          <HX.Pane>
            <HX.Button task="synergy_send_front_sheet_task"
              title="Send Front Sheet" />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Send Rate Change"
        fullWidth={false}
        viewScale={0.7}
        shownBy="model_state/show_after_landing_page">
        <HX.Section title="Send Rate Change Override">
          <HX.Pane>
            <HX.Notes field="cds/send_rate_change/message" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Rate Change"
          shownBy="cds/send_rate_change/show_send_rate_change">
          <HX.Pane>
            <HX.Collection fields={[
              "synergy_upload/rate_change/email_recipients"
            ]} />
            <HX.Button task="synergy_send_rate_change_task"
              title="Send Rate Change" />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Populate Model"
        fullWidth={false}
        viewScale={0.7}
        shownBy="model_state/show_after_landing_page">
        <HX.Section title="Populate Model (Bermuda Focus)">
          <HX.Pane>
            <HX.Collection numCols={2}
              fields={[
              "cds/populate_model/policy_option_id",
              null
            ]} />
            <HX.Button task="populate_model_task"
              title="Populate Model" />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Something Is Broken"
        fullWidth={false}
        viewScale={0.7}
        shownBy="model_state/show_after_landing_page">
        <HX.Section title="Bug Report">
          <HX.Notes field="bug_report_email" />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Standard KPIs"
        shownBy="model_state/show_after_landing_page">
        <HX.Section title="Summary Layer 1"
          shownBy="cds/rate_change/show_layer_1"
          defaultCollapsed={true}>
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "/cds/deal_status.read_only_option",
              "section_reference.read_only_option",
              "brokerage",
              "written_line"
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              {
                "field": "quoted_premium",
                "labelBy": "premium_label"
              },
              null,
              "technical_premium",
              "benchmark_premium",
              "tpi",
              "bpi",
              "tpi_pre_uw_adj",
              "bpi_pre_uw_adj"
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              numCols={3}
              fields={[
              "pflr",
              "pflr_pre_uw_adj",
              "uw_adj_impact"
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
          shownBy="cds/rate_change/show_layer_2"
          defaultCollapsed={true}>
          <HX.With context={{
            "index": 1,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "/cds/deal_status.read_only_option",
              "section_reference.read_only_option",
              "brokerage",
              "written_line"
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              {
                "field": "quoted_premium",
                "labelBy": "premium_label"
              },
              null,
              "technical_premium",
              "benchmark_premium",
              "tpi",
              "bpi",
              "tpi_pre_uw_adj",
              "bpi_pre_uw_adj"
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              numCols={3}
              fields={[
              "pflr",
              "pflr_pre_uw_adj",
              "uw_adj_impact"
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
          shownBy="cds/rate_change/show_layer_3"
          defaultCollapsed={true}>
          <HX.With context={{
            "index": 2,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "/cds/deal_status.read_only_option",
              "section_reference.read_only_option",
              "brokerage",
              "written_line"
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              {
                "field": "quoted_premium",
                "labelBy": "premium_label"
              },
              null,
              "technical_premium",
              "benchmark_premium",
              "tpi",
              "bpi",
              "tpi_pre_uw_adj",
              "bpi_pre_uw_adj"
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              numCols={3}
              fields={[
              "pflr",
              "pflr_pre_uw_adj",
              "uw_adj_impact"
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
          shownBy="cds/rate_change/show_layer_4"
          defaultCollapsed={true}>
          <HX.With context={{
            "index": 3,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "/cds/deal_status.read_only_option",
              "section_reference.read_only_option",
              "brokerage",
              "written_line"
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              {
                "field": "quoted_premium",
                "labelBy": "premium_label"
              },
              null,
              "technical_premium",
              "benchmark_premium",
              "tpi",
              "bpi",
              "tpi_pre_uw_adj",
              "bpi_pre_uw_adj"
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              numCols={3}
              fields={[
              "pflr",
              "pflr_pre_uw_adj",
              "uw_adj_impact"
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
          shownBy="cds/rate_change/show_layer_5"
          defaultCollapsed={true}>
          <HX.With context={{
            "index": 4,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "/cds/deal_status.read_only_option",
              "section_reference.read_only_option",
              "brokerage",
              "written_line"
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              {
                "field": "quoted_premium",
                "labelBy": "premium_label"
              },
              null,
              "technical_premium",
              "benchmark_premium",
              "tpi",
              "bpi",
              "tpi_pre_uw_adj",
              "bpi_pre_uw_adj"
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              numCols={3}
              fields={[
              "pflr",
              "pflr_pre_uw_adj",
              "uw_adj_impact"
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
          shownBy="cds/rate_change/show_layer_6"
          defaultCollapsed={true}>
          <HX.With context={{
            "index": 5,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "/cds/deal_status.read_only_option",
              "section_reference.read_only_option",
              "brokerage",
              "written_line"
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              {
                "field": "quoted_premium",
                "labelBy": "premium_label"
              },
              null,
              "technical_premium",
              "benchmark_premium",
              "tpi",
              "bpi",
              "tpi_pre_uw_adj",
              "bpi_pre_uw_adj"
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              numCols={3}
              fields={[
              "pflr",
              "pflr_pre_uw_adj",
              "uw_adj_impact"
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
          shownBy="cds/rate_change/show_layer_7"
          defaultCollapsed={true}>
          <HX.With context={{
            "index": 6,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "/cds/deal_status.read_only_option",
              "section_reference.read_only_option",
              "brokerage",
              "written_line"
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              {
                "field": "quoted_premium",
                "labelBy": "premium_label"
              },
              null,
              "technical_premium",
              "benchmark_premium",
              "tpi",
              "bpi",
              "tpi_pre_uw_adj",
              "bpi_pre_uw_adj"
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              numCols={3}
              fields={[
              "pflr",
              "pflr_pre_uw_adj",
              "uw_adj_impact"
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
          shownBy="cds/rate_change/show_layer_8"
          defaultCollapsed={true}>
          <HX.With context={{
            "index": 7,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "/cds/deal_status.read_only_option",
              "section_reference.read_only_option",
              "brokerage",
              "written_line"
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              {
                "field": "quoted_premium",
                "labelBy": "premium_label"
              },
              null,
              "technical_premium",
              "benchmark_premium",
              "tpi",
              "bpi",
              "tpi_pre_uw_adj",
              "bpi_pre_uw_adj"
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              numCols={3}
              fields={[
              "pflr",
              "pflr_pre_uw_adj",
              "uw_adj_impact"
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
          shownBy="cds/rate_change/show_layer_9"
          defaultCollapsed={true}>
          <HX.With context={{
            "index": 8,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "/cds/deal_status.read_only_option",
              "section_reference.read_only_option",
              "brokerage",
              "written_line"
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              {
                "field": "quoted_premium",
                "labelBy": "premium_label"
              },
              null,
              "technical_premium",
              "benchmark_premium",
              "tpi",
              "bpi",
              "tpi_pre_uw_adj",
              "bpi_pre_uw_adj"
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              numCols={3}
              fields={[
              "pflr",
              "pflr_pre_uw_adj",
              "uw_adj_impact"
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
          shownBy="cds/rate_change/show_layer_10"
          defaultCollapsed={true}>
          <HX.With context={{
            "index": 9,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "/cds/deal_status.read_only_option",
              "section_reference.read_only_option",
              "brokerage",
              "written_line"
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              {
                "field": "quoted_premium",
                "labelBy": "premium_label"
              },
              null,
              "technical_premium",
              "benchmark_premium",
              "tpi",
              "bpi",
              "tpi_pre_uw_adj",
              "bpi_pre_uw_adj"
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              numCols={3}
              fields={[
              "pflr",
              "pflr_pre_uw_adj",
              "uw_adj_impact"
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
          shownBy="cds/rate_change/show_layer_11"
          defaultCollapsed={true}>
          <HX.With context={{
            "index": 10,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "/cds/deal_status.read_only_option",
              "section_reference.read_only_option",
              "brokerage",
              "written_line"
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              {
                "field": "quoted_premium",
                "labelBy": "premium_label"
              },
              null,
              "technical_premium",
              "benchmark_premium",
              "tpi",
              "bpi",
              "tpi_pre_uw_adj",
              "bpi_pre_uw_adj"
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              numCols={3}
              fields={[
              "pflr",
              "pflr_pre_uw_adj",
              "uw_adj_impact"
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
        <HX.Section title="Summary Layer 12"
          shownBy="cds/rate_change/show_layer_12"
          defaultCollapsed={true}>
          <HX.With context={{
            "index": 11,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "/cds/deal_status.read_only_option",
              "section_reference.read_only_option",
              "brokerage",
              "written_line"
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              {
                "field": "quoted_premium",
                "labelBy": "premium_label"
              },
              null,
              "technical_premium",
              "benchmark_premium",
              "tpi",
              "bpi",
              "tpi_pre_uw_adj",
              "bpi_pre_uw_adj"
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              numCols={3}
              fields={[
              "pflr",
              "pflr_pre_uw_adj",
              "uw_adj_impact"
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
        <HX.Section title="Summary Layer 13"
          shownBy="cds/rate_change/show_layer_13"
          defaultCollapsed={true}>
          <HX.With context={{
            "index": 12,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "/cds/deal_status.read_only_option",
              "section_reference.read_only_option",
              "brokerage",
              "written_line"
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              {
                "field": "quoted_premium",
                "labelBy": "premium_label"
              },
              null,
              "technical_premium",
              "benchmark_premium",
              "tpi",
              "bpi",
              "tpi_pre_uw_adj",
              "bpi_pre_uw_adj"
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              numCols={3}
              fields={[
              "pflr",
              "pflr_pre_uw_adj",
              "uw_adj_impact"
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
        <HX.Section title="Summary Layer 14"
          shownBy="cds/rate_change/show_layer_14"
          defaultCollapsed={true}>
          <HX.With context={{
            "index": 13,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "/cds/deal_status.read_only_option",
              "section_reference.read_only_option",
              "brokerage",
              "written_line"
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              {
                "field": "quoted_premium",
                "labelBy": "premium_label"
              },
              null,
              "technical_premium",
              "benchmark_premium",
              "tpi",
              "bpi",
              "tpi_pre_uw_adj",
              "bpi_pre_uw_adj"
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              numCols={3}
              fields={[
              "pflr",
              "pflr_pre_uw_adj",
              "uw_adj_impact"
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
        <HX.Section title="Summary Layer 15"
          shownBy="cds/rate_change/show_layer_15"
          defaultCollapsed={true}>
          <HX.With context={{
            "index": 14,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "/cds/deal_status.read_only_option",
              "section_reference.read_only_option",
              "brokerage",
              "written_line"
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              {
                "field": "quoted_premium",
                "labelBy": "premium_label"
              },
              null,
              "technical_premium",
              "benchmark_premium",
              "tpi",
              "bpi",
              "tpi_pre_uw_adj",
              "bpi_pre_uw_adj"
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              numCols={3}
              fields={[
              "pflr",
              "pflr_pre_uw_adj",
              "uw_adj_impact"
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
        <HX.Section title="Summary Layer 16"
          shownBy="cds/rate_change/show_layer_16"
          defaultCollapsed={true}>
          <HX.With context={{
            "index": 15,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "/cds/deal_status.read_only_option",
              "section_reference.read_only_option",
              "brokerage",
              "written_line"
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              {
                "field": "quoted_premium",
                "labelBy": "premium_label"
              },
              null,
              "technical_premium",
              "benchmark_premium",
              "tpi",
              "bpi",
              "tpi_pre_uw_adj",
              "bpi_pre_uw_adj"
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              numCols={3}
              fields={[
              "pflr",
              "pflr_pre_uw_adj",
              "uw_adj_impact"
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
        <HX.Section title="Summary Layer 17"
          shownBy="cds/rate_change/show_layer_17"
          defaultCollapsed={true}>
          <HX.With context={{
            "index": 16,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "/cds/deal_status.read_only_option",
              "section_reference.read_only_option",
              "brokerage",
              "written_line"
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              {
                "field": "quoted_premium",
                "labelBy": "premium_label"
              },
              null,
              "technical_premium",
              "benchmark_premium",
              "tpi",
              "bpi",
              "tpi_pre_uw_adj",
              "bpi_pre_uw_adj"
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              numCols={3}
              fields={[
              "pflr",
              "pflr_pre_uw_adj",
              "uw_adj_impact"
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
        <HX.Section title="Summary Layer 18"
          shownBy="cds/rate_change/show_layer_18"
          defaultCollapsed={true}>
          <HX.With context={{
            "index": 17,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "/cds/deal_status.read_only_option",
              "section_reference.read_only_option",
              "brokerage",
              "written_line"
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              {
                "field": "quoted_premium",
                "labelBy": "premium_label"
              },
              null,
              "technical_premium",
              "benchmark_premium",
              "tpi",
              "bpi",
              "tpi_pre_uw_adj",
              "bpi_pre_uw_adj"
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              numCols={3}
              fields={[
              "pflr",
              "pflr_pre_uw_adj",
              "uw_adj_impact"
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
        <HX.Section title="Summary Layer 19"
          shownBy="cds/rate_change/show_layer_19"
          defaultCollapsed={true}>
          <HX.With context={{
            "index": 18,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "/cds/deal_status.read_only_option",
              "section_reference.read_only_option",
              "brokerage",
              "written_line"
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              {
                "field": "quoted_premium",
                "labelBy": "premium_label"
              },
              null,
              "technical_premium",
              "benchmark_premium",
              "tpi",
              "bpi",
              "tpi_pre_uw_adj",
              "bpi_pre_uw_adj"
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              numCols={3}
              fields={[
              "pflr",
              "pflr_pre_uw_adj",
              "uw_adj_impact"
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
        <HX.Section title="Summary Layer 20"
          shownBy="cds/rate_change/show_layer_20"
          defaultCollapsed={true}>
          <HX.With context={{
            "index": 19,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "/cds/deal_status.read_only_option",
              "section_reference.read_only_option",
              "brokerage",
              "written_line"
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              {
                "field": "quoted_premium",
                "labelBy": "premium_label"
              },
              null,
              "technical_premium",
              "benchmark_premium",
              "tpi",
              "bpi",
              "tpi_pre_uw_adj",
              "bpi_pre_uw_adj"
            ]} />
            <HX.Collection title="Expected Loss Ratio"
              numCols={3}
              fields={[
              "pflr",
              "pflr_pre_uw_adj",
              "uw_adj_impact"
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