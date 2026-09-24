
throw new Error(`This file is generated

Do not edit manually as all of the changes will be lost.
This is the static version of your View that will allow easier debugging.
`);

import * as HX from "hx-model-components";


function hx_calculation_legacy_initial_premium_view(props) {
  return (
    <HX.Root>
      <HX.Page title="Landing Page"
        viewScale={0.8}
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
        viewScale={0.8}
        shownBy="model_state/show_after_landing_page">
        <HX.Section title="Rating Model">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "cds/standard_fields/rating_methodology",
              "cds/metadata/rater"
            ]}
              horizontal={true} />
          </HX.Pane>
        </HX.Section>
        <HX.With context={{
          "path": "cds",
          "type": "struct"
        }}>
          <HX.Section title="Account Details">
            <HX.Pane>
              <HX.Collection fields={[
                "inception_date",
                "expiry_date"
              ]}
                with="/hx_core"
                horizontal={true} />
              <HX.Collection fields={[
                "underwriter",
                "benchmark_class"
              ]}
                with="standard_fields"
                horizontal={true} />
              <HX.Collection fields={[
                "standard_fields/insured_name"
              ]}
                horizontal={true} />
              <HX.Collection fields={[
                "standard_fields/policy_reference",
                "currencies/source_currency",
                "standard_fields/is_renewal"
              ]}
                horizontal={true} />
              <HX.Collection fields={[
                "select_class",
                "cob_reference",
                null
              ]}
                with="technical_price_assumptions"
                horizontal={true} />
            </HX.Pane>
          </HX.Section>
          <HX.Section title="Other Account Details"
            shownBy="/model_state/is_steer">
            <HX.Pane>
              <HX.Collection fields={[
                "basis"
              ]}
                with="steer/risk_information"
                horizontal={true} />
            </HX.Pane>
          </HX.Section>
          <HX.Section title="Advanced Features"
            shownBy="/model_state/show_rater_priced">
            <HX.Pane>
              <HX.Collection fields={[
                "include_aad",
                "include_loss_corridor",
                "include_ncb",
                {
                  "field": "include_swing_rates",
                  "infoBy": "/model_state/info_by_include_swing_rates"
                },
                {
                  "field": "include_profit_commission",
                  "infoBy": "/model_state/info_by_include_pc"
                }
              ]}
                with="/cds/risk_information"
                horizontal={true} />
            </HX.Pane>
          </HX.Section>
        </HX.With>
        <HX.Section title="Broker Details">
          <HX.Collection fields={[
            "cds/standard_fields/broker",
            "cds/risk_information/broker_contact"
          ]}
            horizontal={true} />
        </HX.Section>
        <HX.Section title="Comments">
          <HX.Notes field="cds/risk_information/comments" />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Pricing Assumptions"
        viewScale={0.8}
        shownBy="model_state/show_after_landing_page">
        <HX.Section title="Layer (Up to 5 layers)">
          <HX.Pane shownBy="model_state/is_steer">
            <HX.Collection fields={[
              "model_state/is_steer_experience_rating",
              null,
              null
            ]}
              horizontal={true} />
          </HX.Pane>
          <HX.Pane>
            <HX.Table title="Quoted Layers"
              with="cds"
              data={[
              {
                "datum": "layers",
                "width": 250
              }
            ]}
              fields={[
              "status",
              null,
              "currency",
              "epi_100",
              null,
              "limit",
              "excess",
              null,
              "rate",
              "upfront_premium_gross_100",
              null,
              "brokerage",
              "ceding_commission",
              {
                "field": "ncb",
                "shownBy": "/cds/risk_information/include_ncb"
              },
              {
                "field": "profit_commission_rate",
                "shownBy": "/cds/risk_information/include_profit_commission"
              },
              {
                "field": "expense_allowance",
                "shownBy": "/cds/risk_information/include_profit_commission"
              },
              "bkg_gross_or_net",
              null,
              "written_line",
              "line_size",
              null,
              "cap_gross_pct",
              "loss_cap_used",
              null,
              "no_reinstatement",
              "reinstatement_pct_1",
              "reinstatement_pct_2",
              "reinstatement_pct_3",
              "reinstatement_pct_4",
              "reinstatement_pct_5",
              "reinstatement_pct_6",
              "reinstatement_pct_7",
              "reinstatement_pct_8",
              "reinstatement_pct_9",
              "reinstatement_pct_10"
            ]}
              kb-interactive={true}
              transpose={true} />
            <HX.Pane shownBy="/cds/risk_information/include_aad">
              <HX.Table title="AAD"
                with="cds"
                data={[
                {
                  "datum": "layers",
                  "width": 250
                }
              ]}
                fields={[
                "advanced_features_input/aad"
              ]}
                kb-interactive={true}
                transpose={true}
                rowHeaderSettings={{
                "width": 260
              }}
                syncColumnWidthsKey="field" />
            </HX.Pane>
            <HX.Pane shownBy="/cds/risk_information/include_loss_corridor">
              <HX.Table title="Loss Corridor"
                with="cds"
                data={[
                {
                  "datum": "layers",
                  "width": 250
                }
              ]}
                fields={[
                "loss_corridor/min_rate",
                "loss_corridor/max_rate",
                "loss_corridor/insured_participation"
              ]}
                kb-interactive={true}
                transpose={true}
                rowHeaderSettings={{
                "width": 260
              }}
                syncColumnWidthsKey="field" />
            </HX.Pane>
            <HX.Pane shownBy="/cds/risk_information/include_swing_rates">
              <HX.Table title="Swing Rates"
                with="cds"
                data={[
                {
                  "datum": "layers",
                  "width": 250
                }
              ]}
                fields={[
                "swing_rates/swing_brokerage",
                "swing_rates/use_swing_brokerage",
                "swing_rates/deposit_rate",
                "swing_rates/min_rate",
                "swing_rates/max_rate",
                "swing_rates/margin",
                "swing_rates/loading_factor",
                "swing_rates/claims_cap_pct"
              ]}
                kb-interactive={true}
                transpose={true}
                rowHeaderSettings={{
                "width": 260
              }}
                syncColumnWidthsKey="field" />
            </HX.Pane>
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="On-Levelling"
        viewScale={0.8}
        shownBy="model_state/show_steer_experience_rating">
        <HX.With context={{
          "path": "cds/steer/experience_rating",
          "type": "struct"
        }}>
          <HX.Section title="On Level Assumptions">
            <HX.Pane flow="right">
              <HX.Pane flow="down">
                <HX.Collection fields={[
                  "measure",
                  "/cds/risk_information/inception_year"
                ]}
                  syncColumnWidthsKey="measure"
                  with="on_levelling" />
              </HX.Pane>
              <HX.Pane />
              <HX.Pane />
              <HX.Pane />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
            <HX.Pane>
              <HX.Table title="Exposure Assumptions"
                with="on_levelling"
                data={[
                {
                  "datum": "exposure_assumptions",
                  "elementLabelBy": "display_yoa"
                }
              ]}
                fields={[
                null,
                {
                  "field": "exposure",
                  "maxWidth": 150,
                  "shownBy": null
                },
                {
                  "field": "annual_rate_change",
                  "maxWidth": 150,
                  "shownBy": null
                },
                {
                  "field": "rate_change_index",
                  "maxWidth": 150,
                  "shownBy": null
                },
                {
                  "field": "exposure_on_level",
                  "maxWidth": 150,
                  "shownBy": null
                },
                {
                  "field": "claims_inflation",
                  "maxWidth": 150,
                  "shownBy": null
                },
                {
                  "field": "inflation_index",
                  "maxWidth": 150,
                  "shownBy": null
                },
                null,
                {
                  "field": "exposure_adjusted_layer_01",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_layer_01"
                },
                {
                  "field": "exposure_adjusted_layer_02",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_layer_02"
                },
                {
                  "field": "exposure_adjusted_layer_03",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_layer_03"
                },
                {
                  "field": "exposure_adjusted_layer_04",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_layer_04"
                },
                {
                  "field": "exposure_adjusted_layer_05",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_layer_05"
                }
              ]}
                kb-interactive={true} />
            </HX.Pane>
          </HX.Section>
        </HX.With>
      </HX.Page>
      <HX.Page title="Raw Data"
        fullWidth={true}
        viewScale={0.8}
        shownBy="model_state/show_steer_experience_rating">
        <HX.With context={{
          "path": "cds/steer/experience_rating",
          "type": "struct"
        }}>
          <HX.Section title="Raw Data Input">
            <HX.Pane>
              <HX.Collection fields={[
                "on_levelling/raw_data_comment",
                null,
                null
              ]}
                horizontal={true} />
              <HX.Pane flow="right">
                <HX.Pane ratio={1}>
                  <HX.Button task="steer_clear_raw_data_task"
                    title="Clear Raw Data" />
                </HX.Pane>
                <HX.Pane ratio={3} />
              </HX.Pane>
              <HX.Table title="Raw Data"
                data={[
                {
                  "datum": "raw_data"
                }
              ]}
                fields={[
                {
                  "field": "column_01",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_02",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_03",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_04",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_05",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_06",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_07",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_08",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_09",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_10",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_11",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_12",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_13",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_14",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_15",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_16",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_17",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_18",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_19",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_20",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_21",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_22",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_23",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_24",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_25",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_26",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_27",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_28",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_29",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_30",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_31",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_32",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_33",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_34",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_35",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_36",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_37",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_38",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_39",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_40",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_41",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_42",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_43",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_44",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_45",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_46",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_47",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_48",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_49",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_50",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_51",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_52",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_53",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_54",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_55",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_56",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_57",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_58",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_59",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_60",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_61",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_62",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_63",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_64",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_65",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_66",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_67",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_68",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_69",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_70",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_71",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_72",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_73",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_74",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_75",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_76",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_77",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_78",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_79",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_80",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_81",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_82",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_83",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_84",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_85",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_86",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_87",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_88",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_89",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_90",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_91",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_92",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_93",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_94",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_95",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_96",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_97",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_98",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_99",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_100",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_101",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_102",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_103",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_104",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_105",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_106",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_107",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_108",
                  "maxWidth": 250,
                  "shownBy": null
                },
                {
                  "field": "column_109",
                  "maxWidth": 250,
                  "shownBy": null
                }
              ]}
                kb-interactive={true} />
            </HX.Pane>
          </HX.Section>
        </HX.With>
      </HX.Page>
      <HX.Page title="Data Format"
        fullWidth={true}
        viewScale={0.8}
        shownBy="model_state/show_steer_experience_rating">
        <HX.With context={{
          "path": "cds/steer/experience_rating",
          "type": "struct"
        }}>
          <HX.Section title="Misc Parameters">
            <HX.Pane flow="right"
              reflow={false}>
              <HX.Pane ratio={1}>
                <HX.Pane flow="down">
                  <HX.Collection fields={[
                    {
                      "field": "target_year",
                      "infoBy": "target_year_info"
                    },
                    {
                      "field": "closed_indicator",
                      "infoBy": "closed_indicator_info"
                    }
                  ]}
                    syncColumnWidthsKey="target_year"
                    with="misc_parameters" />
                </HX.Pane>
              </HX.Pane>
              <HX.Pane ratio={1}>
                <HX.Table with="other_fields"
                  data={[
                  {
                    "datum": "fvy",
                    "elementInfoBy": "description"
                  },
                  {
                    "datum": "lvy",
                    "elementInfoBy": "description"
                  },
                  {
                    "datum": "data_as_at_date",
                    "elementInfoBy": "description"
                  },
                  {
                    "datum": "coverage_basis",
                    "elementInfoBy": "description"
                  },
                  {
                    "datum": "bcost_measure",
                    "elementInfoBy": "description"
                  }
                ]}
                  fields={[
                  "value"
                ]}
                  kb-interactive={true}
                  syncColumnWidthsKey="field" />
              </HX.Pane>
              <HX.Pane ratio={1}>
                <HX.Button task="steer_clear_raw_data_task"
                  title="Clear Raw Data" />
                <HX.Button task="steer_format_raw_data_task"
                  title="Format Raw Data" />
              </HX.Pane>
              <HX.Pane ratio={2}>
                <HX.Notes field="raw_data_error/pre_val_err_messages.warning"
                  shownBy="raw_data_error/show_pre_val_err_messages" />
              </HX.Pane>
            </HX.Pane>
          </HX.Section>
        </HX.With>
        <HX.With context={{
          "path": "cds/steer/experience_rating",
          "type": "struct"
        }}>
          <HX.Section title="Data Mapping & Other Fields">
            <HX.Pane>
              <HX.Pane flow="right"
                ratio={4}
                reflow={false}>
                <HX.Pane ratio={3}>
                  <HX.Pane>
                    <HX.Table title="Raw Data Mapping"
                      with="data_mapping"
                      data={[
                      {
                        "datum": "field_01",
                        "elementLabelBy": "field"
                      },
                      {
                        "datum": "field_02",
                        "elementLabelBy": "field"
                      },
                      {
                        "datum": "field_03",
                        "elementLabelBy": "field"
                      },
                      {
                        "datum": "field_04",
                        "elementLabelBy": "field"
                      },
                      {
                        "datum": "field_05",
                        "elementLabelBy": "field"
                      },
                      {
                        "datum": "field_06",
                        "elementLabelBy": "field"
                      },
                      {
                        "datum": "field_07",
                        "elementLabelBy": "field"
                      },
                      {
                        "datum": "field_08",
                        "elementLabelBy": "field"
                      },
                      {
                        "datum": "field_09",
                        "elementLabelBy": "field"
                      },
                      {
                        "datum": "field_10",
                        "elementLabelBy": "field"
                      },
                      {
                        "datum": "field_11",
                        "elementLabelBy": "field"
                      },
                      {
                        "datum": "field_12",
                        "elementLabelBy": "field"
                      },
                      {
                        "datum": "field_13",
                        "elementLabelBy": "field"
                      },
                      {
                        "datum": "field_14",
                        "elementLabelBy": "field"
                      },
                      {
                        "datum": "field_15",
                        "elementLabelBy": "field"
                      },
                      {
                        "datum": "field_16",
                        "elementLabelBy": "field"
                      },
                      {
                        "datum": "field_17",
                        "elementLabelBy": "field"
                      },
                      {
                        "datum": "field_18",
                        "elementLabelBy": "field"
                      }
                    ]}
                      fields={[
                      {
                        "field": "field",
                        "maxWidth": 250,
                        "shownBy": null
                      },
                      {
                        "field": "field_name",
                        "maxWidth": 250,
                        "shownBy": null
                      },
                      {
                        "field": "description",
                        "maxWidth": 250,
                        "shownBy": null
                      },
                      {
                        "field": "mandatory_column",
                        "maxWidth": 250,
                        "shownBy": null
                      },
                      {
                        "field": "specify_column",
                        "maxWidth": 250,
                        "shownBy": null
                      },
                      {
                        "field": "accept_missing",
                        "maxWidth": 250,
                        "shownBy": null
                      },
                      {
                        "field": "field_type",
                        "maxWidth": 250,
                        "shownBy": null
                      },
                      {
                        "field": "value_within_range",
                        "maxWidth": 250,
                        "shownBy": null
                      },
                      {
                        "field": "replace_missing_with_default",
                        "maxWidth": 250,
                        "shownBy": null
                      }
                    ]}
                      kb-interactive={true} />
                  </HX.Pane>
                  <HX.Pane flow="right">
                    <HX.Pane />
                  </HX.Pane>
                </HX.Pane>
                <HX.Pane flow="right"
                  ratio={2}
                  reflow={false}>
                  <HX.Pane>
                    <HX.Table title="Raw Data Column Name"
                      data={[
                      {
                        "datum": "/steer/experience_rating/raw_data_column_names",
                        "width": 350
                      }
                    ]}
                      fields={[
                      "column_01",
                      "column_02",
                      "column_03",
                      "column_04",
                      "column_05",
                      "column_06",
                      "column_07",
                      "column_08",
                      "column_09",
                      "column_10",
                      "column_11",
                      "column_12",
                      "column_13",
                      "column_14",
                      "column_15",
                      "column_16",
                      "column_17",
                      "column_18",
                      "column_19",
                      "column_20",
                      "column_21",
                      "column_22",
                      "column_23",
                      "column_24",
                      "column_25",
                      "column_26",
                      "column_27",
                      "column_28",
                      "column_29",
                      "column_30",
                      "column_31",
                      "column_32",
                      "column_33",
                      "column_34",
                      "column_35",
                      "column_36",
                      "column_37",
                      "column_38",
                      "column_39",
                      "column_40",
                      "column_41",
                      "column_42",
                      "column_43",
                      "column_44",
                      "column_45",
                      "column_46",
                      "column_47",
                      "column_48",
                      "column_49",
                      "column_50",
                      "column_51",
                      "column_52",
                      "column_53",
                      "column_54",
                      "column_55",
                      "column_56",
                      "column_57",
                      "column_58",
                      "column_59",
                      "column_60",
                      "column_61",
                      "column_62",
                      "column_63",
                      "column_64",
                      "column_65",
                      "column_66",
                      "column_67",
                      "column_68",
                      "column_69",
                      "column_70",
                      "column_71",
                      "column_72",
                      "column_73",
                      "column_74",
                      "column_75",
                      "column_76",
                      "column_77",
                      "column_78",
                      "column_79",
                      "column_80",
                      "column_81",
                      "column_82",
                      "column_83",
                      "column_84",
                      "column_85",
                      "column_86",
                      "column_87",
                      "column_88",
                      "column_89",
                      "column_90",
                      "column_91",
                      "column_92",
                      "column_93",
                      "column_94",
                      "column_95",
                      "column_96",
                      "column_97",
                      "column_98",
                      "column_99",
                      "column_100",
                      "column_101",
                      "column_102",
                      "column_103",
                      "column_104",
                      "column_105",
                      "column_106",
                      "column_107",
                      "column_108",
                      "column_109"
                    ]}
                      kb-interactive={true}
                      transpose={true} />
                  </HX.Pane>
                  <HX.Pane>
                    <HX.Table title="Display"
                      with="/steer/experience_rating/column_display"
                      data={[
                      "reference",
                      "claimant",
                      "insured",
                      "status",
                      "incident_date",
                      "report_date",
                      "closed_date",
                      "incident_year",
                      "policy_year",
                      "closed_year",
                      "policy_limit",
                      "policy_excess",
                      "incurred_claims",
                      "inflated_claims",
                      "incurred_capped",
                      "trended_claim",
                      "trended_expenses",
                      "claim_ranking",
                      "row_number",
                      "ri_claim",
                      "ri_claim_on_levelled",
                      "ri_claim_count",
                      "ri_claim_count_on_levelled"
                    ]}
                      fields={[
                      {
                        "field": "show",
                        "maxWidth": 250
                      }
                    ]}
                      kb-interactive={true} />
                  </HX.Pane>
                </HX.Pane>
              </HX.Pane>
            </HX.Pane>
          </HX.Section>
        </HX.With>
      </HX.Page>
      <HX.Page title="Raw Data Error"
        fullWidth={true}
        viewScale={0.8}
        shownBy="model_state/is_steer_raw_data_not_validated">
        <HX.With context={{
          "path": "cds/steer/experience_rating",
          "type": "struct"
        }}>
          <HX.Section title="Raw Data Error">
            <HX.Pane flow="right">
              <HX.Pane>
                <HX.Table title="Accepted Missing Value"
                  with="raw_data_error"
                  data={[
                  "accepted_missing_value"
                ]}
                  fields={[
                  {
                    "field": "requirement",
                    "maxWidth": 250,
                    "shownBy": null
                  },
                  {
                    "field": "column_name",
                    "maxWidth": 250,
                    "shownBy": null
                  },
                  {
                    "field": "cell_address",
                    "maxWidth": 250,
                    "shownBy": null
                  },
                  {
                    "field": "value_found",
                    "maxWidth": 250,
                    "shownBy": null
                  }
                ]}
                  kb-interactive={true} />
              </HX.Pane>
              <HX.Pane>
                <HX.Table title="Field Type"
                  with="raw_data_error"
                  data={[
                  "field_type"
                ]}
                  fields={[
                  {
                    "field": "requirement",
                    "maxWidth": 250,
                    "shownBy": null
                  },
                  {
                    "field": "column_name",
                    "maxWidth": 250,
                    "shownBy": null
                  },
                  {
                    "field": "cell_address",
                    "maxWidth": 250,
                    "shownBy": null
                  },
                  {
                    "field": "value_found",
                    "maxWidth": 250,
                    "shownBy": null
                  }
                ]}
                  kb-interactive={true} />
              </HX.Pane>
              <HX.Pane>
                <HX.Table title="Value Within Range"
                  with="raw_data_error"
                  data={[
                  "value_within_range"
                ]}
                  fields={[
                  {
                    "field": "requirement",
                    "maxWidth": 250,
                    "shownBy": null
                  },
                  {
                    "field": "column_name",
                    "maxWidth": 250,
                    "shownBy": null
                  },
                  {
                    "field": "cell_address",
                    "maxWidth": 250,
                    "shownBy": null
                  },
                  {
                    "field": "value_found",
                    "maxWidth": 250,
                    "shownBy": null
                  }
                ]}
                  kb-interactive={true} />
              </HX.Pane>
            </HX.Pane>
          </HX.Section>
        </HX.With>
      </HX.Page>
      <HX.Page title="Experience"
        fullWidth={true}
        viewScale={0.8}
        shownBy="model_state/show_steer_experience_rating">
        <HX.With context={{
          "path": "cds/steer/experience_rating",
          "type": "struct"
        }}>
          <HX.Section title="Processed Claims">
            <HX.Pane flow="right">
              <HX.Table data={[
                "processed_claims"
              ]}
                fields={[
                {
                  "field": "reference",
                  "maxWidth": 150,
                  "shownBy": "/steer/experience_rating/column_display/reference/show"
                },
                {
                  "field": "claimant",
                  "maxWidth": 150,
                  "shownBy": "/steer/experience_rating/column_display/claimant/show"
                },
                {
                  "field": "insured",
                  "maxWidth": 150,
                  "shownBy": "/steer/experience_rating/column_display/insured/show"
                },
                {
                  "field": "status",
                  "maxWidth": 150,
                  "shownBy": "/steer/experience_rating/column_display/status/show"
                },
                {
                  "field": "incident_date",
                  "maxWidth": 150,
                  "shownBy": "/steer/experience_rating/column_display/incident_date/show"
                },
                {
                  "field": "report_date",
                  "maxWidth": 150,
                  "shownBy": "/steer/experience_rating/column_display/report_date/show"
                },
                {
                  "field": "closed_date",
                  "maxWidth": 150,
                  "shownBy": "/steer/experience_rating/column_display/closed_date/show"
                },
                {
                  "field": "incident_year",
                  "maxWidth": 150,
                  "shownBy": "/steer/experience_rating/column_display/incident_year/show"
                },
                {
                  "field": "policy_year",
                  "maxWidth": 150,
                  "shownBy": "/steer/experience_rating/column_display/policy_year/show"
                },
                {
                  "field": "closed_year",
                  "maxWidth": 150,
                  "shownBy": "/steer/experience_rating/column_display/closed_year/show"
                },
                {
                  "field": "policy_limit",
                  "maxWidth": 150,
                  "shownBy": "/steer/experience_rating/column_display/policy_limit/show"
                },
                {
                  "field": "policy_excess",
                  "maxWidth": 150,
                  "shownBy": "/steer/experience_rating/column_display/policy_excess/show"
                },
                null,
                {
                  "field": "incurred_claims",
                  "maxWidth": 150,
                  "shownBy": "/steer/experience_rating/column_display/incurred_claims/show"
                },
                {
                  "field": "inflated_claims",
                  "maxWidth": 150,
                  "shownBy": "/steer/experience_rating/column_display/inflated_claims/show"
                },
                {
                  "field": "incurred_capped",
                  "maxWidth": 150,
                  "shownBy": "/steer/experience_rating/column_display/incurred_capped/show"
                },
                {
                  "field": "trended_claim",
                  "maxWidth": 150,
                  "shownBy": "/steer/experience_rating/column_display/trended_claim/show"
                },
                {
                  "field": "trended_expenses",
                  "maxWidth": 150,
                  "shownBy": "/steer/experience_rating/column_display/trended_expenses/show"
                },
                {
                  "field": "claim_ranking",
                  "maxWidth": 150,
                  "shownBy": "/steer/experience_rating/column_display/claim_ranking/show"
                },
                {
                  "field": "row_number",
                  "maxWidth": 150,
                  "shownBy": "/steer/experience_rating/column_display/row_number/show"
                },
                null,
                {
                  "field": "ri_claim_layer_01",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_layer_01"
                },
                {
                  "field": "ri_claim_layer_02",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_layer_02"
                },
                {
                  "field": "ri_claim_layer_03",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_layer_03"
                },
                {
                  "field": "ri_claim_layer_04",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_layer_04"
                },
                {
                  "field": "ri_claim_layer_05",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_layer_05"
                },
                {
                  "field": "ri_claim_on_levelled_layer_01",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_layer_01"
                },
                {
                  "field": "ri_claim_on_levelled_layer_02",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_layer_02"
                },
                {
                  "field": "ri_claim_on_levelled_layer_03",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_layer_03"
                },
                {
                  "field": "ri_claim_on_levelled_layer_04",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_layer_04"
                },
                {
                  "field": "ri_claim_on_levelled_layer_05",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_layer_05"
                },
                null,
                {
                  "field": "ri_claim_count_layer_01",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_layer_01"
                },
                {
                  "field": "ri_claim_count_layer_02",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_layer_02"
                },
                {
                  "field": "ri_claim_count_layer_03",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_layer_03"
                },
                {
                  "field": "ri_claim_count_layer_04",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_layer_04"
                },
                {
                  "field": "ri_claim_count_layer_05",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_layer_05"
                },
                {
                  "field": "ri_claim_count_on_levelled_layer_01",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_layer_01"
                },
                {
                  "field": "ri_claim_count_on_levelled_layer_02",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_layer_02"
                },
                {
                  "field": "ri_claim_count_on_levelled_layer_03",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_layer_03"
                },
                {
                  "field": "ri_claim_count_on_levelled_layer_04",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_layer_04"
                },
                {
                  "field": "ri_claim_count_on_levelled_layer_05",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_layer_05"
                },
                null,
                {
                  "field": "paid_dy_01",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_01"
                },
                {
                  "field": "paid_dy_02",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_02"
                },
                {
                  "field": "paid_dy_03",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_03"
                },
                {
                  "field": "paid_dy_04",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_04"
                },
                {
                  "field": "paid_dy_05",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_05"
                },
                {
                  "field": "paid_dy_06",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_06"
                },
                {
                  "field": "paid_dy_07",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_07"
                },
                {
                  "field": "paid_dy_08",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_08"
                },
                {
                  "field": "paid_dy_09",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_09"
                },
                {
                  "field": "paid_dy_10",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_10"
                },
                {
                  "field": "paid_dy_11",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_11"
                },
                {
                  "field": "paid_dy_12",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_12"
                },
                {
                  "field": "paid_dy_13",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_13"
                },
                {
                  "field": "paid_dy_14",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_14"
                },
                {
                  "field": "paid_dy_15",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_15"
                },
                {
                  "field": "paid_dy_16",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_16"
                },
                {
                  "field": "paid_dy_17",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_17"
                },
                {
                  "field": "paid_dy_18",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_18"
                },
                {
                  "field": "paid_dy_19",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_19"
                },
                {
                  "field": "paid_dy_20",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_20"
                },
                {
                  "field": "paid_dy_21",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_21"
                },
                {
                  "field": "paid_dy_22",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_22"
                },
                {
                  "field": "paid_dy_23",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_23"
                },
                {
                  "field": "paid_dy_24",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_24"
                },
                {
                  "field": "paid_dy_25",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_25"
                },
                null,
                {
                  "field": "incurred_dy_01",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_01"
                },
                {
                  "field": "incurred_dy_02",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_02"
                },
                {
                  "field": "incurred_dy_03",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_03"
                },
                {
                  "field": "incurred_dy_04",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_04"
                },
                {
                  "field": "incurred_dy_05",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_05"
                },
                {
                  "field": "incurred_dy_06",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_06"
                },
                {
                  "field": "incurred_dy_07",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_07"
                },
                {
                  "field": "incurred_dy_08",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_08"
                },
                {
                  "field": "incurred_dy_09",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_09"
                },
                {
                  "field": "incurred_dy_10",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_10"
                },
                {
                  "field": "incurred_dy_11",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_11"
                },
                {
                  "field": "incurred_dy_12",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_12"
                },
                {
                  "field": "incurred_dy_13",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_13"
                },
                {
                  "field": "incurred_dy_14",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_14"
                },
                {
                  "field": "incurred_dy_15",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_15"
                },
                {
                  "field": "incurred_dy_16",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_16"
                },
                {
                  "field": "incurred_dy_17",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_17"
                },
                {
                  "field": "incurred_dy_18",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_18"
                },
                {
                  "field": "incurred_dy_19",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_19"
                },
                {
                  "field": "incurred_dy_20",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_20"
                },
                {
                  "field": "incurred_dy_21",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_21"
                },
                {
                  "field": "incurred_dy_22",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_22"
                },
                {
                  "field": "incurred_dy_23",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_23"
                },
                {
                  "field": "incurred_dy_24",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_24"
                },
                {
                  "field": "incurred_dy_25",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_25"
                },
                null,
                {
                  "field": "paid_expenses_dy_01",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_01"
                },
                {
                  "field": "paid_expenses_dy_02",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_02"
                },
                {
                  "field": "paid_expenses_dy_03",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_03"
                },
                {
                  "field": "paid_expenses_dy_04",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_04"
                },
                {
                  "field": "paid_expenses_dy_05",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_05"
                },
                {
                  "field": "paid_expenses_dy_06",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_06"
                },
                {
                  "field": "paid_expenses_dy_07",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_07"
                },
                {
                  "field": "paid_expenses_dy_08",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_08"
                },
                {
                  "field": "paid_expenses_dy_09",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_09"
                },
                {
                  "field": "paid_expenses_dy_10",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_10"
                },
                {
                  "field": "paid_expenses_dy_11",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_11"
                },
                {
                  "field": "paid_expenses_dy_12",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_12"
                },
                {
                  "field": "paid_expenses_dy_13",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_13"
                },
                {
                  "field": "paid_expenses_dy_14",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_14"
                },
                {
                  "field": "paid_expenses_dy_15",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_15"
                },
                {
                  "field": "paid_expenses_dy_16",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_16"
                },
                {
                  "field": "paid_expenses_dy_17",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_17"
                },
                {
                  "field": "paid_expenses_dy_18",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_18"
                },
                {
                  "field": "paid_expenses_dy_19",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_19"
                },
                {
                  "field": "paid_expenses_dy_20",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_20"
                },
                {
                  "field": "paid_expenses_dy_21",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_21"
                },
                {
                  "field": "paid_expenses_dy_22",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_22"
                },
                {
                  "field": "paid_expenses_dy_23",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_23"
                },
                {
                  "field": "paid_expenses_dy_24",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_24"
                },
                {
                  "field": "paid_expenses_dy_25",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_25"
                },
                null,
                {
                  "field": "incurred_expenses_dy_01",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_01"
                },
                {
                  "field": "incurred_expenses_dy_02",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_02"
                },
                {
                  "field": "incurred_expenses_dy_03",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_03"
                },
                {
                  "field": "incurred_expenses_dy_04",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_04"
                },
                {
                  "field": "incurred_expenses_dy_05",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_05"
                },
                {
                  "field": "incurred_expenses_dy_06",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_06"
                },
                {
                  "field": "incurred_expenses_dy_07",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_07"
                },
                {
                  "field": "incurred_expenses_dy_08",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_08"
                },
                {
                  "field": "incurred_expenses_dy_09",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_09"
                },
                {
                  "field": "incurred_expenses_dy_10",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_10"
                },
                {
                  "field": "incurred_expenses_dy_11",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_11"
                },
                {
                  "field": "incurred_expenses_dy_12",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_12"
                },
                {
                  "field": "incurred_expenses_dy_13",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_13"
                },
                {
                  "field": "incurred_expenses_dy_14",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_14"
                },
                {
                  "field": "incurred_expenses_dy_15",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_15"
                },
                {
                  "field": "incurred_expenses_dy_16",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_16"
                },
                {
                  "field": "incurred_expenses_dy_17",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_17"
                },
                {
                  "field": "incurred_expenses_dy_18",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_18"
                },
                {
                  "field": "incurred_expenses_dy_19",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_19"
                },
                {
                  "field": "incurred_expenses_dy_20",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_20"
                },
                {
                  "field": "incurred_expenses_dy_21",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_21"
                },
                {
                  "field": "incurred_expenses_dy_22",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_22"
                },
                {
                  "field": "incurred_expenses_dy_23",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_23"
                },
                {
                  "field": "incurred_expenses_dy_24",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_24"
                },
                {
                  "field": "incurred_expenses_dy_25",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_25"
                },
                null,
                {
                  "field": "paid_claim_indemnity_dy_01",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_01"
                },
                {
                  "field": "paid_claim_indemnity_dy_02",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_02"
                },
                {
                  "field": "paid_claim_indemnity_dy_03",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_03"
                },
                {
                  "field": "paid_claim_indemnity_dy_04",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_04"
                },
                {
                  "field": "paid_claim_indemnity_dy_05",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_05"
                },
                {
                  "field": "paid_claim_indemnity_dy_06",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_06"
                },
                {
                  "field": "paid_claim_indemnity_dy_07",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_07"
                },
                {
                  "field": "paid_claim_indemnity_dy_08",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_08"
                },
                {
                  "field": "paid_claim_indemnity_dy_09",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_09"
                },
                {
                  "field": "paid_claim_indemnity_dy_10",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_10"
                },
                {
                  "field": "paid_claim_indemnity_dy_11",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_11"
                },
                {
                  "field": "paid_claim_indemnity_dy_12",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_12"
                },
                {
                  "field": "paid_claim_indemnity_dy_13",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_13"
                },
                {
                  "field": "paid_claim_indemnity_dy_14",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_14"
                },
                {
                  "field": "paid_claim_indemnity_dy_15",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_15"
                },
                {
                  "field": "paid_claim_indemnity_dy_16",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_16"
                },
                {
                  "field": "paid_claim_indemnity_dy_17",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_17"
                },
                {
                  "field": "paid_claim_indemnity_dy_18",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_18"
                },
                {
                  "field": "paid_claim_indemnity_dy_19",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_19"
                },
                {
                  "field": "paid_claim_indemnity_dy_20",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_20"
                },
                {
                  "field": "paid_claim_indemnity_dy_21",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_21"
                },
                {
                  "field": "paid_claim_indemnity_dy_22",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_22"
                },
                {
                  "field": "paid_claim_indemnity_dy_23",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_23"
                },
                {
                  "field": "paid_claim_indemnity_dy_24",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_24"
                },
                {
                  "field": "paid_claim_indemnity_dy_25",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_25"
                },
                null,
                {
                  "field": "incurred_claim_indemnity_dy_01",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_01"
                },
                {
                  "field": "incurred_claim_indemnity_dy_02",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_02"
                },
                {
                  "field": "incurred_claim_indemnity_dy_03",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_03"
                },
                {
                  "field": "incurred_claim_indemnity_dy_04",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_04"
                },
                {
                  "field": "incurred_claim_indemnity_dy_05",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_05"
                },
                {
                  "field": "incurred_claim_indemnity_dy_06",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_06"
                },
                {
                  "field": "incurred_claim_indemnity_dy_07",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_07"
                },
                {
                  "field": "incurred_claim_indemnity_dy_08",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_08"
                },
                {
                  "field": "incurred_claim_indemnity_dy_09",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_09"
                },
                {
                  "field": "incurred_claim_indemnity_dy_10",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_10"
                },
                {
                  "field": "incurred_claim_indemnity_dy_11",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_11"
                },
                {
                  "field": "incurred_claim_indemnity_dy_12",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_12"
                },
                {
                  "field": "incurred_claim_indemnity_dy_13",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_13"
                },
                {
                  "field": "incurred_claim_indemnity_dy_14",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_14"
                },
                {
                  "field": "incurred_claim_indemnity_dy_15",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_15"
                },
                {
                  "field": "incurred_claim_indemnity_dy_16",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_16"
                },
                {
                  "field": "incurred_claim_indemnity_dy_17",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_17"
                },
                {
                  "field": "incurred_claim_indemnity_dy_18",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_18"
                },
                {
                  "field": "incurred_claim_indemnity_dy_19",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_19"
                },
                {
                  "field": "incurred_claim_indemnity_dy_20",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_20"
                },
                {
                  "field": "incurred_claim_indemnity_dy_21",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_21"
                },
                {
                  "field": "incurred_claim_indemnity_dy_22",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_22"
                },
                {
                  "field": "incurred_claim_indemnity_dy_23",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_23"
                },
                {
                  "field": "incurred_claim_indemnity_dy_24",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_24"
                },
                {
                  "field": "incurred_claim_indemnity_dy_25",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_25"
                },
                null,
                {
                  "field": "paid_claim_count_dy_01",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_01"
                },
                {
                  "field": "paid_claim_count_dy_02",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_02"
                },
                {
                  "field": "paid_claim_count_dy_03",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_03"
                },
                {
                  "field": "paid_claim_count_dy_04",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_04"
                },
                {
                  "field": "paid_claim_count_dy_05",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_05"
                },
                {
                  "field": "paid_claim_count_dy_06",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_06"
                },
                {
                  "field": "paid_claim_count_dy_07",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_07"
                },
                {
                  "field": "paid_claim_count_dy_08",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_08"
                },
                {
                  "field": "paid_claim_count_dy_09",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_09"
                },
                {
                  "field": "paid_claim_count_dy_10",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_10"
                },
                {
                  "field": "paid_claim_count_dy_11",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_11"
                },
                {
                  "field": "paid_claim_count_dy_12",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_12"
                },
                {
                  "field": "paid_claim_count_dy_13",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_13"
                },
                {
                  "field": "paid_claim_count_dy_14",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_14"
                },
                {
                  "field": "paid_claim_count_dy_15",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_15"
                },
                {
                  "field": "paid_claim_count_dy_16",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_16"
                },
                {
                  "field": "paid_claim_count_dy_17",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_17"
                },
                {
                  "field": "paid_claim_count_dy_18",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_18"
                },
                {
                  "field": "paid_claim_count_dy_19",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_19"
                },
                {
                  "field": "paid_claim_count_dy_20",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_20"
                },
                {
                  "field": "paid_claim_count_dy_21",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_21"
                },
                {
                  "field": "paid_claim_count_dy_22",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_22"
                },
                {
                  "field": "paid_claim_count_dy_23",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_23"
                },
                {
                  "field": "paid_claim_count_dy_24",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_24"
                },
                {
                  "field": "paid_claim_count_dy_25",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_25"
                },
                null,
                {
                  "field": "incurred_claim_count_dy_01",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_01"
                },
                {
                  "field": "incurred_claim_count_dy_02",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_02"
                },
                {
                  "field": "incurred_claim_count_dy_03",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_03"
                },
                {
                  "field": "incurred_claim_count_dy_04",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_04"
                },
                {
                  "field": "incurred_claim_count_dy_05",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_05"
                },
                {
                  "field": "incurred_claim_count_dy_06",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_06"
                },
                {
                  "field": "incurred_claim_count_dy_07",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_07"
                },
                {
                  "field": "incurred_claim_count_dy_08",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_08"
                },
                {
                  "field": "incurred_claim_count_dy_09",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_09"
                },
                {
                  "field": "incurred_claim_count_dy_10",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_10"
                },
                {
                  "field": "incurred_claim_count_dy_11",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_11"
                },
                {
                  "field": "incurred_claim_count_dy_12",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_12"
                },
                {
                  "field": "incurred_claim_count_dy_13",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_13"
                },
                {
                  "field": "incurred_claim_count_dy_14",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_14"
                },
                {
                  "field": "incurred_claim_count_dy_15",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_15"
                },
                {
                  "field": "incurred_claim_count_dy_16",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_16"
                },
                {
                  "field": "incurred_claim_count_dy_17",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_17"
                },
                {
                  "field": "incurred_claim_count_dy_18",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_18"
                },
                {
                  "field": "incurred_claim_count_dy_19",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_19"
                },
                {
                  "field": "incurred_claim_count_dy_20",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_20"
                },
                {
                  "field": "incurred_claim_count_dy_21",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_21"
                },
                {
                  "field": "incurred_claim_count_dy_22",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_22"
                },
                {
                  "field": "incurred_claim_count_dy_23",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_23"
                },
                {
                  "field": "incurred_claim_count_dy_24",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_24"
                },
                {
                  "field": "incurred_claim_count_dy_25",
                  "maxWidth": 150,
                  "shownBy": "/model_state/show_data_year_25"
                }
              ]}
                title="Processed Claims"
                kb-interactive={true} />
            </HX.Pane>
          </HX.Section>
        </HX.With>
      </HX.Page>
      <HX.Page title="Claim Movements"
        viewScale={0.8}
        shownBy="model_state/show_steer_experience_rating">
        <HX.With context={{
          "path": "cds/steer/experience_rating",
          "type": "struct"
        }}>
          <HX.Section title="Claim Movements">
            <HX.Pane flow="right">
              <HX.Table data={[
                "claim_movements"
              ]}
                fields={[
                {
                  "field": "claim_ranking",
                  "maxWidth": 150,
                  "shownBy": null
                },
                {
                  "field": "claim_reference",
                  "maxWidth": 150,
                  "shownBy": null
                },
                {
                  "field": "yoa",
                  "maxWidth": 150,
                  "shownBy": null
                },
                {
                  "field": "status",
                  "maxWidth": 150,
                  "shownBy": null
                },
                null,
                {
                  "field": "last_year",
                  "maxWidth": 150,
                  "shownBy": null
                },
                {
                  "field": "this_year",
                  "maxWidth": 150,
                  "shownBy": null
                },
                {
                  "field": "incurred_movement",
                  "maxWidth": 150,
                  "shownBy": null
                },
                null,
                {
                  "field": "last_year_on_levelled",
                  "maxWidth": 150,
                  "shownBy": null
                },
                {
                  "field": "this_year_on_levelled",
                  "maxWidth": 150,
                  "shownBy": null
                },
                {
                  "field": "incurred_movement_on_levelled",
                  "maxWidth": 150,
                  "shownBy": null
                }
              ]}
                title="Claim Movements"
                kb-interactive={true}
                syncColumnWidthsKey="field" />
            </HX.Pane>
          </HX.Section>
        </HX.With>
      </HX.Page>
      <HX.Page title="Triangle Projection"
        fullWidth={true}
        viewScale={0.7200000000000001}
        shownBy="model_state/show_steer_experience_rating">
        <HX.Section title="Triangle Instructions"
          defaultCollapsed={true}>
          <HX.Pane flow="right">
            <HX.Notes field="model_state/triangle_fgu_instructions" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Triangle - Raw Data"
          defaultCollapsed={true}>
          <HX.Pane flow="right">
            <HX.Pane ratio={1}>
              <HX.Collection fields={[
                "cds/steer/experience_rating/layers/fgu/triangle_projection/tri_1_basis"
              ]} />
            </HX.Pane>
            <HX.Pane ratio={3}>
              <HX.Collection fields={[
                null
              ]} />
            </HX.Pane>
          </HX.Pane>
          <HX.TriangleData title="Triangle Data"
            triangle="tri_1_raw_data"
            with="cds/steer/experience_rating/layers/fgu/triangle_projection"
            syncColumnWidthsKey="align_tri_2"
            defaultMode="cumulative" />
        </HX.Section>
        <HX.Section title="Triangle - Manual Input"
          defaultCollapsed={true}>
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "override_triangle_date",
              "override_triangle_years",
              null,
              null
            ]}
              with="cds/steer/experience_rating/layers/fgu/triangle_projection"
              horizontal={true} />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Pane ratio={1}>
              <HX.Button task="steer_tri_override_setup_task"
                title="Setup Override Triangle" />
            </HX.Pane>
            <HX.Pane ratio={3}>
              <HX.Collection fields={[
                "async_override_triangle_status",
                null,
                null
              ]}
                with="cds/steer/experience_rating/layers/fgu/triangle_projection"
                horizontal={true} />
            </HX.Pane>
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "override_triangle",
              "assign_override_triangle_status",
              null,
              null
            ]}
              with="cds/steer/experience_rating/layers/fgu/triangle_projection"
              horizontal={true} />
          </HX.Pane>
          <HX.TriangleData title="Triangle Data"
            triangle="tri_2_manual_input"
            with="cds/steer/experience_rating/layers/fgu/triangle_projection"
            syncColumnWidthsKey="align_tri_2"
            defaultMode="cumulative" />
        </HX.Section>
        <HX.Section title="Triangle - Selected"
          defaultCollapsed={false}>
          <HX.TriangleData title="Triangle Data"
            triangle="tri_3_selected"
            with="cds/steer/experience_rating/layers/fgu/triangle_projection"
            syncColumnWidthsKey="align_tri_2"
            defaultMode="cumulative" />
          <HX.TriangleDevFactors title="Triangle Incurred Development Factors"
            triangle="tri_3_selected"
            with="cds/steer/experience_rating/layers/fgu/triangle_projection"
            syncColumnWidthsKey="align_tri_2" />
        </HX.Section>
        <HX.Section title="Triangle - Exclusions"
          defaultCollapsed={true}>
          <HX.Pane flow="right">
            <HX.Pane ratio={1}>
              <HX.Button task="steer_tri_exclusions_setup_task"
                title="Setup Exclusions Triangle For Use" />
            </HX.Pane>
            <HX.Pane ratio={1}>
              <HX.Pane flow="down">
                <HX.Notes field="cds/steer/experience_rating/layers/fgu/triangle_projection/tri_exclusions_setup_task_status" />
                <HX.Notes field="cds/steer/experience_rating/layers/fgu/triangle_projection/tri_exclusions_dimensions_status" />
              </HX.Pane>
            </HX.Pane>
            <HX.Pane ratio={2}>
              <HX.Collection fields={[
                null
              ]} />
            </HX.Pane>
          </HX.Pane>
          <HX.TriangleData title="Triangle - Exclusions"
            triangle="tri_3a_exclusions"
            with="cds/steer/experience_rating/layers/fgu/triangle_projection"
            syncColumnWidthsKey="align_tri_2"
            defaultMode="cumulative" />
        </HX.Section>
        <HX.Section title="Triangle - Averages"
          defaultCollapsed={true}>
          <HX.TriangleAverages title="Triangle Averages"
            triangle="tri_3_selected"
            with="cds/steer/experience_rating/layers/fgu/triangle_projection"
            syncColumnWidthsKey="align_tri_2" />
        </HX.Section>
        <HX.Section title="Algorithmic Development and Overrides"
          defaultCollapsed={false}>
          <HX.Collection fields={[
            "selected_average_option_input",
            null,
            null,
            null
          ]}
            with="cds/steer/experience_rating/layers/fgu/triangle_projection"
            horizontal={true}
            syncColumnWidthsKey="align_tri_2" />
          <HX.Table title="Experience Analysis - Incremental Development Factors"
            data={[
            {
              "datum": "incremental_dev_factor",
              "elementLabelBy": "development_label"
            },
            null,
            "tail_factor"
          ]}
            fields={[
            "experience_default",
            "experience_override",
            "experience_selected"
          ]}
            with="cds/steer/experience_rating/layers/fgu/triangle_projection"
            kb-interactive={true}
            transpose={true}
            syncColumnWidthsKey="align_tri_2"
            filter="show_idf_row" />
          <HX.Pane flow="right">
            <HX.Pane ratio={1}>
              <HX.Button task="steer_populate_bc_patterns_task"
                title="Update Burning Cost Pattern" />
            </HX.Pane>
            <HX.Pane ratio={1}>
              <HX.Collection fields={[
                "triangle_projection/update_pattern_message"
              ]}
                shownBy="triangle_projection/is_not_experience_selected_updated"
                with="cds/steer/experience_rating/layers/fgu"
                horizontal={true} />
            </HX.Pane>
            <HX.Pane ratio={2}>
              <HX.Collection fields={[
                null
              ]} />
            </HX.Pane>
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Projection"
          defaultCollapsed={false}>
          <HX.TriangleProjections title="Triangle Projections"
            triangle="tri_4_result"
            with="cds/steer/experience_rating/layers/fgu/triangle_projection"
            syncColumnWidthsKey="align_tri_2" />
          <HX.TriangleChart title="Triangle Graphing"
            triangle="tri_4_result"
            with="cds/steer/experience_rating/layers/fgu/triangle_projection" />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Claim Count"
        fullWidth={true}
        viewScale={0.7200000000000001}
        shownBy="model_state/show_steer_experience_rating">
        <HX.Section title="Triangle Instructions"
          defaultCollapsed={true}>
          <HX.Pane flow="right">
            <HX.Notes field="model_state/triangle_claim_count_instructions" />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Claim Count - Raw Data (Incurred only) "
          defaultCollapsed={true}>
          <HX.TriangleData title="Triangle Data"
            triangle="tri_1_raw_data"
            with="cds/steer/experience_rating/layers/fgu/claim_count"
            syncColumnWidthsKey="align_tri_2"
            defaultMode="cumulative" />
        </HX.Section>
        <HX.Section title="Claim Count - Selected"
          defaultCollapsed={false}>
          <HX.TriangleData title="Triangle Data"
            triangle="tri_3_selected"
            with="cds/steer/experience_rating/layers/fgu/claim_count"
            syncColumnWidthsKey="align_tri_2"
            defaultMode="cumulative" />
          <HX.TriangleDevFactors title="Triangle Incurred Development Factors"
            triangle="tri_3_selected"
            with="cds/steer/experience_rating/layers/fgu/claim_count"
            syncColumnWidthsKey="align_tri_2" />
        </HX.Section>
        <HX.Section title="Claim Count - Exclusions"
          defaultCollapsed={true}>
          <HX.Pane flow="right">
            <HX.Pane ratio={1}>
              <HX.Button task="steer_tri_count_exclusions_setup_task"
                title="Setup Exclusions Triangle For Use" />
            </HX.Pane>
            <HX.Pane ratio={1}>
              <HX.Pane flow="down">
                <HX.Notes field="cds/steer/experience_rating/layers/fgu/claim_count/tri_exclusions_setup_task_status" />
                <HX.Notes field="cds/steer/experience_rating/layers/fgu/claim_count/tri_exclusions_dimensions_status" />
              </HX.Pane>
            </HX.Pane>
            <HX.Pane ratio={2}>
              <HX.Collection fields={[
                null
              ]} />
            </HX.Pane>
          </HX.Pane>
          <HX.TriangleData title="Claim Count - Exclusions"
            triangle="tri_3a_exclusions"
            with="cds/steer/experience_rating/layers/fgu/claim_count"
            syncColumnWidthsKey="align_tri_2"
            defaultMode="cumulative" />
        </HX.Section>
        <HX.Section title="Claim Count - Averages"
          defaultCollapsed={true}>
          <HX.TriangleAverages title="Claim Count Averages"
            triangle="tri_3_selected"
            with="cds/steer/experience_rating/layers/fgu/claim_count"
            syncColumnWidthsKey="align_tri_2" />
        </HX.Section>
        <HX.Section title="Algorithmic Development and Overrides"
          defaultCollapsed={false}>
          <HX.Collection fields={[
            "selected_average_option_input",
            null,
            null,
            null
          ]}
            with="cds/steer/experience_rating/layers/fgu/claim_count"
            horizontal={true}
            syncColumnWidthsKey="align_tri_2" />
          <HX.Table title="Experience Analysis - Incremental Development Factors"
            data={[
            {
              "datum": "incremental_dev_factor",
              "elementLabelBy": "development_label"
            },
            null,
            "tail_factor"
          ]}
            fields={[
            "experience_default",
            "experience_override",
            "experience_selected"
          ]}
            with="cds/steer/experience_rating/layers/fgu/claim_count"
            kb-interactive={true}
            transpose={true}
            syncColumnWidthsKey="align_tri_2"
            filter="show_idf_row" />
          <HX.Pane flow="right">
            <HX.Pane ratio={1}>
              <HX.Button task="steer_populate_bc_patterns_task"
                title="Populate Burning Cost Pattern" />
            </HX.Pane>
            <HX.Pane ratio={1}>
              <HX.Collection fields={[
                "claim_count/update_pattern_message"
              ]}
                shownBy="claim_count/is_not_experience_selected_updated"
                with="cds/steer/experience_rating/layers/fgu"
                horizontal={true} />
            </HX.Pane>
            <HX.Pane ratio={2}>
              <HX.Collection fields={[
                null
              ]} />
            </HX.Pane>
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Projection"
          defaultCollapsed={false}>
          <HX.TriangleProjections title="Claim Count Projections"
            triangle="tri_4_result"
            with="cds/steer/experience_rating/layers/fgu/claim_count"
            syncColumnWidthsKey="align_tri_2" />
          <HX.TriangleChart title="Claim Count Graphing"
            triangle="tri_4_result"
            with="cds/steer/experience_rating/layers/fgu/claim_count" />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Triangle Projection Per Layer"
        fullWidth={true}
        viewScale={0.7200000000000001}
        shownBy="model_state/show_steer_experience_rating">
        <HX.Selector with="cds/steer/experience_rating/layers"
          data={[
          "layer_01",
          "layer_02",
          "layer_03",
          "layer_04",
          "layer_05"
        ]}
          dropdown="layer_name">
          <HX.Section title="Triangle Instructions"
            defaultCollapsed={true}>
            <HX.Pane flow="right">
              <HX.Notes field="/model_state/triangle_per_layer_instructions" />
            </HX.Pane>
          </HX.Section>
          <HX.Section title="Triangle - Raw Data"
            defaultCollapsed={true}>
            <HX.Pane flow="right">
              <HX.Pane ratio={1}>
                <HX.Collection fields={[
                  "triangle_projection/tri_1_basis"
                ]} />
              </HX.Pane>
              <HX.Pane ratio={3}>
                <HX.Collection fields={[
                  null
                ]} />
              </HX.Pane>
            </HX.Pane>
            <HX.TriangleData title="Triangle Data"
              triangle="tri_1_raw_data"
              with="triangle_projection"
              syncColumnWidthsKey="align_tri_2"
              defaultMode="cumulative" />
          </HX.Section>
          <HX.Section title="Triangle - Selected"
            defaultCollapsed={false}>
            <HX.TriangleData title="Triangle Data"
              triangle="tri_3_selected"
              with="triangle_projection"
              syncColumnWidthsKey="align_tri_2"
              defaultMode="cumulative" />
            <HX.TriangleDevFactors title="Triangle Incurred Development Factors"
              triangle="tri_3_selected"
              with="triangle_projection"
              syncColumnWidthsKey="align_tri_2" />
          </HX.Section>
          <HX.Section title="Triangle - Exclusions"
            defaultCollapsed={true}>
            <HX.Pane flow="right">
              <HX.Pane ratio={1}>
                <HX.Button task="steer_tri_exclusions_setup_task"
                  title="Setup Exclusions Triangle For Use" />
              </HX.Pane>
              <HX.Pane ratio={1}>
                <HX.Pane flow="down">
                  <HX.Notes field="triangle_projection/tri_exclusions_setup_task_status" />
                  <HX.Notes field="triangle_projection/tri_exclusions_dimensions_status" />
                </HX.Pane>
              </HX.Pane>
              <HX.Pane ratio={2}>
                <HX.Collection fields={[
                  null
                ]} />
              </HX.Pane>
            </HX.Pane>
            <HX.TriangleData title="Triangle - Exclusions"
              triangle="tri_3a_exclusions"
              with="triangle_projection"
              syncColumnWidthsKey="align_tri_2"
              defaultMode="cumulative" />
          </HX.Section>
          <HX.Section title="Triangle - Averages"
            defaultCollapsed={true}>
            <HX.TriangleAverages title="Triangle Averages"
              triangle="tri_3_selected"
              with="triangle_projection"
              syncColumnWidthsKey="align_tri_2" />
          </HX.Section>
          <HX.Section title="Algorithmic Development and Overrides"
            defaultCollapsed={false}>
            <HX.Table title="Experience Analysis - Incremental Development Factors"
              data={[
              {
                "datum": "incremental_dev_factor",
                "elementLabelBy": "development_label"
              },
              null,
              "tail_factor"
            ]}
              fields={[
              "experience_default",
              "experience_override",
              "experience_selected"
            ]}
              with="triangle_projection"
              kb-interactive={true}
              transpose={true}
              syncColumnWidthsKey="align_tri_2"
              filter="show_idf_row" />
            <HX.Pane flow="right">
              <HX.Pane ratio={1}>
                <HX.Button task="steer_populate_bc_patterns_task"
                  title="Populate Burning Cost Pattern" />
              </HX.Pane>
              <HX.Pane ratio={1}>
                <HX.Collection fields={[
                  "triangle_projection/update_pattern_message"
                ]}
                  shownBy="triangle_projection/is_not_experience_selected_updated"
                  horizontal={true} />
              </HX.Pane>
              <HX.Pane ratio={2}>
                <HX.Collection fields={[
                  null
                ]} />
              </HX.Pane>
            </HX.Pane>
          </HX.Section>
          <HX.Section title="Projection"
            defaultCollapsed={false}>
            <HX.TriangleProjections title="Triangle Projections"
              triangle="tri_4_result"
              with="triangle_projection"
              syncColumnWidthsKey="align_tri_2" />
            <HX.TriangleChart title="Triangle Graphing"
              triangle="tri_4_result"
              with="triangle_projection" />
          </HX.Section>
        </HX.Selector>
      </HX.Page>
      <HX.Page title="Burning Cost"
        fullWidth={true}
        viewScale={0.8}
        shownBy="model_state/show_steer_experience_rating">
        <HX.Selector with="cds/steer/experience_rating/layers"
          data={[
          "layer_01",
          "layer_02",
          "layer_03",
          "layer_04",
          "layer_05",
          "fgu"
        ]}
          dropdown="layer_name">
          <HX.Section title="Burning Cost">
            <HX.Pane>
              <HX.Pane flow="right">
                <HX.Pane ratio={1}>
                  <HX.Button task="steer_populate_bc_patterns_task"
                    title="Update Burning Cost Pattern" />
                </HX.Pane>
                <HX.Pane ratio={1}>
                  <HX.Collection fields={[
                    "triangle_projection/update_pattern_message"
                  ]}
                    shownBy="triangle_projection/is_not_experience_selected_updated"
                    horizontal={true} />
                </HX.Pane>
                <HX.Pane ratio={4} />
              </HX.Pane>
              <HX.Pane>
                <HX.Table data={[
                  {
                    "datum": "burning_cost",
                    "elementLabelBy": "policy_year_label"
                  },
                  null,
                  "selected_years_wa",
                  "all_years_wa"
                ]}
                  fields={[
                  {
                    "field": "weighting",
                    "maxWidth": 120,
                    "shownBy": null
                  },
                  {
                    "field": "onlevelled_exposure",
                    "maxWidth": 120,
                    "shownBy": null
                  },
                  {
                    "field": "incurred_claims",
                    "maxWidth": 120,
                    "shownBy": null
                  },
                  {
                    "field": "incurred_no_of_claims",
                    "maxWidth": 120,
                    "shownBy": null
                  },
                  {
                    "field": "inflated_claims",
                    "maxWidth": 120,
                    "shownBy": null
                  },
                  {
                    "field": "inflated_no_of_claims",
                    "maxWidth": 120,
                    "shownBy": null
                  },
                  {
                    "field": "ultimate_claims_developed",
                    "maxWidth": 120,
                    "shownBy": null
                  },
                  {
                    "field": "ultimate_claims_developed_and_inflated",
                    "maxWidth": 120,
                    "shownBy": null
                  },
                  {
                    "field": "ibnr",
                    "maxWidth": 120,
                    "shownBy": null
                  },
                  {
                    "field": "ultimate_no_of_claims_developed",
                    "maxWidth": 120,
                    "shownBy": null
                  },
                  {
                    "field": "frequency_per_m_exposure",
                    "maxWidth": 120,
                    "shownBy": null
                  },
                  {
                    "field": "average_cost_per_claim",
                    "maxWidth": 120,
                    "shownBy": null
                  },
                  {
                    "field": "loss_cost_per_m_exposure",
                    "maxWidth": 120,
                    "shownBy": null
                  },
                  {
                    "field": "rate_pct",
                    "maxWidth": 120,
                    "shownBy": null
                  },
                  {
                    "field": "expected_loss_cost",
                    "maxWidth": 120,
                    "shownBy": null
                  },
                  null,
                  {
                    "field": "premium",
                    "maxWidth": 120,
                    "shownBy": null
                  },
                  {
                    "field": "ulr",
                    "maxWidth": 120,
                    "shownBy": null
                  },
                  null,
                  {
                    "field": "claim_dev_pct",
                    "maxWidth": 120,
                    "shownBy": null
                  },
                  {
                    "field": "claim_count_dev_pct",
                    "maxWidth": 120,
                    "shownBy": null
                  },
                  {
                    "field": "claim_dev_method",
                    "maxWidth": 120,
                    "shownBy": null
                  },
                  {
                    "field": "claim_count_dev_method",
                    "maxWidth": 120,
                    "shownBy": null
                  },
                  null,
                  {
                    "field": "cl_incurred_claims_developed",
                    "maxWidth": 120,
                    "shownBy": null
                  },
                  {
                    "field": "cl_inflated_claims_developed",
                    "maxWidth": 120,
                    "shownBy": null
                  },
                  {
                    "field": "cl_claim_count_developed",
                    "maxWidth": 120,
                    "shownBy": null
                  },
                  {
                    "field": "cl_freq",
                    "maxWidth": 120,
                    "shownBy": null
                  },
                  {
                    "field": "cl_acpc",
                    "maxWidth": 120,
                    "shownBy": null
                  },
                  {
                    "field": "cl_acpc_inflated",
                    "maxWidth": 120,
                    "shownBy": null
                  },
                  null,
                  {
                    "field": "bf_claim_amount",
                    "maxWidth": 120,
                    "shownBy": null
                  },
                  {
                    "field": "bf_claim_amount_inflated",
                    "maxWidth": 120,
                    "shownBy": null
                  },
                  {
                    "field": "bf_claim_count",
                    "maxWidth": 120,
                    "shownBy": null
                  }
                ]}
                  title="Burning Cost"
                  kb-interactive={true}
                  syncColumnWidthsKey="field"
                  rowHeaderSettings={{
                  "width": 160
                }} />
              </HX.Pane>
              <HX.Pane flow="right">
                <HX.Pane ratio={1}>
                  <CustomComponent textNode="bc_comment"
                    placeholderText="Comment on manual adjustments, selected claims pattern..." />
                </HX.Pane>
                <HX.Pane ratio={1}>
                  <HX.Collection fields={[
                    "bc_ulr_message"
                  ]}
                    horizontal={true} />
                </HX.Pane>
                <HX.Pane ratio={1}>
                  <HX.Pane>
                    <HX.Pane flow="right">
                      <HX.Pane ratio={1} />
                      <HX.Pane ratio={1}>
                        <HX.Collection fields={[
                          "pattern_type"
                        ]} />
                      </HX.Pane>
                    </HX.Pane>
                    <HX.Table title="Expected Pick from Experience (for years using CL)"
                      data={[
                      "bf_expected/incurred_claim",
                      "bf_expected/inflated_claim"
                    ]}
                      fields={[
                      {
                        "field": "frequency_per_m_exposure",
                        "maxWidth": 250,
                        "shownBy": null
                      },
                      {
                        "field": "acpc",
                        "maxWidth": 250,
                        "shownBy": null
                      },
                      {
                        "field": "loss_cost_per_m_revenue",
                        "maxWidth": 250,
                        "shownBy": null
                      },
                      {
                        "field": "offset_rows",
                        "maxWidth": 250,
                        "shownBy": null
                      }
                    ]}
                      kb-interactive={true} />
                  </HX.Pane>
                </HX.Pane>
              </HX.Pane>
              <HX.Pane flow="right">
                <HX.Pane ratio={1}>
                  <CustomComponent title="Expected Loss Cost"
                    xAxisLabel="Year"
                    yAxisLabel="Expected Loss"
                    yAxis2Label=""
                    xAxisStep={1}
                    xAxisTickFormat=".0f"
                    yAxisTickFormat=",.0f"
                    y2AxisTickFormat=",.0f"
                    series={[
                    {
                      "colour": "#000000",
                      "label": "Expected Loss",
                      "line_type": "lines+marker",
                      "points": [
                        {
                          "list": "burning_cost",
                          "x": "policy_year_label",
                          "y": "average_expected_loss_cost"
                        }
                      ],
                      "yaxis": "y"
                    },
                    {
                      "colour": "#CA3397",
                      "label": "Average Expected Loss",
                      "line_type": "lines",
                      "points": [
                        {
                          "list": "burning_cost",
                          "x": "policy_year_label",
                          "y": "expected_loss_cost"
                        }
                      ],
                      "yaxis": "y"
                    }
                  ]} />
                </HX.Pane>
                <HX.Pane ratio={1}>
                  <CustomComponent title="Frequency per M of Exposure"
                    xAxisLabel="Year"
                    yAxisLabel="Frequency"
                    yAxis2Label=""
                    xAxisStep={1}
                    xAxisTickFormat=".0f"
                    yAxisTickFormat=",.2f"
                    y2AxisTickFormat=",.0f"
                    series={[
                    {
                      "colour": "#000000",
                      "label": "Average Freq/m of Exposure",
                      "line_type": "lines+marker",
                      "points": [
                        {
                          "list": "burning_cost",
                          "x": "policy_year_label",
                          "y": "average_freq_per_m_exposure"
                        }
                      ],
                      "yaxis": "y"
                    },
                    {
                      "colour": "#CA3397",
                      "label": "Frequency/m of Exposure",
                      "line_type": "lines",
                      "points": [
                        {
                          "list": "burning_cost",
                          "x": "policy_year_label",
                          "y": "frequency_per_m_exposure"
                        }
                      ],
                      "yaxis": "y"
                    }
                  ]} />
                </HX.Pane>
                <HX.Pane ratio={1}>
                  <CustomComponent title="Loss Cost per M of Exposure"
                    xAxisLabel="Year"
                    yAxisLabel="Loss Cost"
                    yAxis2Label=""
                    xAxisStep={1}
                    xAxisTickFormat=".0f"
                    yAxisTickFormat=",.0f"
                    y2AxisTickFormat=",.0f"
                    series={[
                    {
                      "colour": "#000000",
                      "label": "Average Loss Cost/m of Exposure",
                      "line_type": "lines+marker",
                      "points": [
                        {
                          "list": "burning_cost",
                          "x": "policy_year_label",
                          "y": "average_loss_cost_per_m_exposure"
                        }
                      ],
                      "yaxis": "y"
                    },
                    {
                      "colour": "#CA3397",
                      "label": "Loss Cost/m of Exposure",
                      "line_type": "lines",
                      "points": [
                        {
                          "list": "burning_cost",
                          "x": "policy_year_label",
                          "y": "loss_cost_per_m_exposure"
                        }
                      ],
                      "yaxis": "y"
                    }
                  ]} />
                </HX.Pane>
              </HX.Pane>
            </HX.Pane>
          </HX.Section>
        </HX.Selector>
        <HX.Section title="Summary">
          <HX.Pane>
            <HX.Pane>
              <HX.With context={{
                "path": "/cds/steer/experience_rating/layers/fgu/selected_years_wa",
                "type": "struct"
              }}>
                <HX.Collection title="FGU"
                  fields={[
                  null,
                  null,
                  null,
                  "rate_pct",
                  "ulr",
                  null,
                  null,
                  null,
                  null
                ]}
                  horizontal={true}
                  syncColumnWidthsKey="field" />
              </HX.With>
            </HX.Pane>
            <HX.Pane>
              <HX.Table title="Summary"
                with="/cds"
                data={[
                "layers"
              ]}
                fields={[
                {
                  "field": "excess",
                  "maxWidth": 120,
                  "shownBy": null
                },
                {
                  "field": "limit",
                  "maxWidth": 120,
                  "shownBy": null
                },
                {
                  "field": "pricing_selection/burning_cost/pure_rate",
                  "maxWidth": 120,
                  "shownBy": null
                },
                {
                  "field": "pricing_selection/burning_cost/ulr",
                  "maxWidth": 120,
                  "shownBy": null
                }
              ]}
                kb-interactive={true}
                syncColumnWidthsKey="field"
                rowHeaderSettings={{
                "width": 150
              }} />
            </HX.Pane>
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Curve Descriptions"
        viewScale={0.8}
        shownBy="model_state/show_steer_risk_bdx">
        <HX.Section title="All Curves">
          <HX.Pane>
            <HX.Table with="steer/exposure_rating/curve_descriptions"
              data={[
              "all_curves"
            ]}
              fields={[
              "description",
              "parametric",
              "curve_description",
              "source"
            ]}
              kb-interactive={true}
              dynamic={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Commercial Auto State Groupings">
          <HX.Pane>
            <HX.Table with="steer/exposure_rating/curve_descriptions"
              data={[
              "commercial_auto_state"
            ]}
              fields={[
              "group_1",
              "group_2",
              "group_3",
              "group_4",
              "group_5",
              "group_6",
              "group_7",
              "group_8"
            ]}
              kb-interactive={true}
              dynamic={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Cyber Groupings">
          <HX.Pane>
            <HX.Table with="steer/exposure_rating/curve_descriptions"
              data={[
              "cyber"
            ]}
              fields={[
              "low",
              "high"
            ]}
              kb-interactive={true}
              dynamic={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Healthcare Groupings">
          <HX.Pane>
            <HX.Table with="steer/exposure_rating/curve_descriptions"
              data={[
              "healthcare"
            ]}
              fields={[
              "low",
              "medium",
              "medium_high",
              "high",
              "very_high"
            ]}
              kb-interactive={true}
              dynamic={true} />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Private D&O Groupings">
          <HX.Pane>
            <HX.Table with="steer/exposure_rating/curve_descriptions"
              data={[
              "private_d_o"
            ]}
              fields={[
              "low",
              "medium",
              "high",
              "very_high"
            ]}
              kb-interactive={true}
              dynamic={true} />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Risk Profile Bdx"
        fullWidth={true}
        viewScale={0.8}
        shownBy="model_state/show_steer_risk_bdx">
        <HX.With context={{
          "path": "cds/steer/exposure_rating/risk_profile_bdx",
          "type": "struct"
        }}>
          <HX.Section title="Risk Profile Bdx">
            <HX.Pane flow="down">
              <HX.Pane flow="right">
                <HX.Pane flow="right"
                  ratio={2}>
                  <HX.Pane ratio={1}>
                    <HX.Collection fields={[
                      "exposure_lr",
                      "exposure_profile_gross_premium",
                      "no_of_risk",
                      "curve"
                    ]} />
                    <HX.Notes field="message"
                      shownBy="/model_state/is_bdx_input_issue" />
                  </HX.Pane>
                  <HX.Pane ratio={1}>
                    <HX.Table title="Layers Assumptions"
                      with="/cds"
                      data={[
                      "layers"
                    ]}
                      fields={[
                      {
                        "field": "limit",
                        "maxWidth": 170,
                        "shownBy": null
                      },
                      {
                        "field": "excess",
                        "maxWidth": 170,
                        "shownBy": null
                      },
                      {
                        "field": "pricing_selection/risk_profile_bdx/pure_rate",
                        "maxWidth": 170,
                        "shownBy": null
                      }
                    ]}
                      kb-interactive={true} />
                  </HX.Pane>
                </HX.Pane>
                <HX.Pane ratio={2}>
                  <HX.Pane>
                    <HX.Table title="Layers"
                      with="/cds"
                      data={[
                      {
                        "datum": "layers",
                        "width": 220
                      }
                    ]}
                      fields={[
                      "risk_profile_bdx/pro_rata_premium",
                      {
                        "field": "risk_profile_bdx/exposure_premium",
                        "infoBy": "/model_state/info_by_risk_bdx_exposure_prem"
                      },
                      "risk_profile_bdx/glr_pick",
                      "risk_profile_bdx/exposure_lr",
                      "risk_profile_bdx/el_at_loss_ratio",
                      "risk_profile_bdx/rate_on_npi",
                      "risk_profile_bdx/loss_premium"
                    ]}
                      transpose={true} />
                  </HX.Pane>
                </HX.Pane>
              </HX.Pane>
              <HX.Pane>
                <HX.Table title="Risk profiles"
                  data={[
                  "risk_profiles"
                ]}
                  fields={[
                  {
                    "field": "cob",
                    "maxWidth": 350
                  },
                  {
                    "field": "curve",
                    "maxWidth": 350
                  },
                  {
                    "field": "insured",
                    "maxWidth": 150,
                    "shownBy": null
                  },
                  {
                    "field": "limit",
                    "maxWidth": 150,
                    "shownBy": null
                  },
                  {
                    "field": "excess",
                    "maxWidth": 150,
                    "shownBy": null
                  },
                  {
                    "field": "net_premium",
                    "maxWidth": 150,
                    "shownBy": null
                  },
                  {
                    "field": "share",
                    "maxWidth": 150,
                    "shownBy": null
                  },
                  {
                    "field": "linkage",
                    "maxWidth": 150,
                    "shownBy": null
                  },
                  {
                    "field": "exposure",
                    "maxWidth": 150,
                    "shownBy": null
                  },
                  {
                    "field": "currency",
                    "maxWidth": 150,
                    "shownBy": null
                  },
                  {
                    "field": "fx_rate_to_usd",
                    "maxWidth": 150,
                    "shownBy": null
                  },
                  null,
                  {
                    "field": "parametric",
                    "maxWidth": 150,
                    "shownBy": null
                  },
                  {
                    "field": "curve_type",
                    "maxWidth": 150,
                    "shownBy": null
                  },
                  {
                    "field": "first_loss",
                    "maxWidth": 150,
                    "shownBy": null
                  },
                  {
                    "field": "first_loss_factor",
                    "maxWidth": 150,
                    "shownBy": null
                  },
                  {
                    "field": "param_1",
                    "maxWidth": 150,
                    "shownBy": null
                  },
                  {
                    "field": "param_2",
                    "maxWidth": 150,
                    "shownBy": null
                  },
                  {
                    "field": "param_3",
                    "maxWidth": 150,
                    "shownBy": null
                  },
                  {
                    "field": "param_4",
                    "maxWidth": 150,
                    "shownBy": null
                  },
                  null,
                  {
                    "field": "layer_01/expo_pct",
                    "maxWidth": 150,
                    "shownBy": null
                  },
                  {
                    "field": "layer_01/expo_premium",
                    "maxWidth": 150,
                    "shownBy": null
                  },
                  {
                    "field": "layer_01/excess",
                    "maxWidth": 150,
                    "shownBy": null
                  },
                  {
                    "field": "layer_01/sum_insured",
                    "maxWidth": 150,
                    "shownBy": null
                  },
                  {
                    "field": "layer_01/ilf_xs_and_xm",
                    "maxWidth": 150,
                    "shownBy": null
                  },
                  {
                    "field": "layer_01/ilf_xs_and_xl",
                    "maxWidth": 150,
                    "shownBy": null
                  },
                  {
                    "field": "layer_01/ilf_xs_and_lmt",
                    "maxWidth": 150,
                    "shownBy": null
                  },
                  {
                    "field": "layer_01/ilf_xs",
                    "maxWidth": 150,
                    "shownBy": null
                  },
                  {
                    "field": "layer_01/pr_pct",
                    "maxWidth": 150,
                    "shownBy": null
                  },
                  {
                    "field": "layer_01/pr_net_premium",
                    "maxWidth": 150,
                    "shownBy": null
                  },
                  {
                    "field": "layer_02/expo_pct",
                    "maxWidth": 150,
                    "shownBy": null
                  },
                  {
                    "field": "layer_02/expo_premium",
                    "maxWidth": 150,
                    "shownBy": null
                  },
                  {
                    "field": "layer_02/excess",
                    "maxWidth": 150,
                    "shownBy": null
                  },
                  {
                    "field": "layer_02/sum_insured",
                    "maxWidth": 150,
                    "shownBy": null
                  },
                  {
                    "field": "layer_02/ilf_xs_and_xm",
                    "maxWidth": 150,
                    "shownBy": null
                  },
                  {
                    "field": "layer_02/ilf_xs_and_xl",
                    "maxWidth": 150,
                    "shownBy": null
                  },
                  {
                    "field": "layer_02/ilf_xs_and_lmt",
                    "maxWidth": 150,
                    "shownBy": null
                  },
                  {
                    "field": "layer_02/ilf_xs",
                    "maxWidth": 150,
                    "shownBy": null
                  },
                  {
                    "field": "layer_02/pr_pct",
                    "maxWidth": 150,
                    "shownBy": null
                  },
                  {
                    "field": "layer_02/pr_net_premium",
                    "maxWidth": 150,
                    "shownBy": null
                  },
                  {
                    "field": "layer_03/expo_pct",
                    "maxWidth": 150,
                    "shownBy": null
                  },
                  {
                    "field": "layer_03/expo_premium",
                    "maxWidth": 150,
                    "shownBy": null
                  },
                  {
                    "field": "layer_03/excess",
                    "maxWidth": 150,
                    "shownBy": null
                  },
                  {
                    "field": "layer_03/sum_insured",
                    "maxWidth": 150,
                    "shownBy": null
                  },
                  {
                    "field": "layer_03/ilf_xs_and_xm",
                    "maxWidth": 150,
                    "shownBy": null
                  },
                  {
                    "field": "layer_03/ilf_xs_and_xl",
                    "maxWidth": 150,
                    "shownBy": null
                  },
                  {
                    "field": "layer_03/ilf_xs_and_lmt",
                    "maxWidth": 150,
                    "shownBy": null
                  },
                  {
                    "field": "layer_03/ilf_xs",
                    "maxWidth": 150,
                    "shownBy": null
                  },
                  {
                    "field": "layer_03/pr_pct",
                    "maxWidth": 150,
                    "shownBy": null
                  },
                  {
                    "field": "layer_03/pr_net_premium",
                    "maxWidth": 150,
                    "shownBy": null
                  },
                  {
                    "field": "layer_04/expo_pct",
                    "maxWidth": 150,
                    "shownBy": null
                  },
                  {
                    "field": "layer_04/expo_premium",
                    "maxWidth": 150,
                    "shownBy": null
                  },
                  {
                    "field": "layer_04/excess",
                    "maxWidth": 150,
                    "shownBy": null
                  },
                  {
                    "field": "layer_04/sum_insured",
                    "maxWidth": 150,
                    "shownBy": null
                  },
                  {
                    "field": "layer_04/ilf_xs_and_xm",
                    "maxWidth": 150,
                    "shownBy": null
                  },
                  {
                    "field": "layer_04/ilf_xs_and_xl",
                    "maxWidth": 150,
                    "shownBy": null
                  },
                  {
                    "field": "layer_04/ilf_xs_and_lmt",
                    "maxWidth": 150,
                    "shownBy": null
                  },
                  {
                    "field": "layer_04/ilf_xs",
                    "maxWidth": 150,
                    "shownBy": null
                  },
                  {
                    "field": "layer_04/pr_pct",
                    "maxWidth": 150,
                    "shownBy": null
                  },
                  {
                    "field": "layer_04/pr_net_premium",
                    "maxWidth": 150,
                    "shownBy": null
                  },
                  {
                    "field": "layer_05/expo_pct",
                    "maxWidth": 150,
                    "shownBy": null
                  },
                  {
                    "field": "layer_05/expo_premium",
                    "maxWidth": 150,
                    "shownBy": null
                  },
                  {
                    "field": "layer_05/excess",
                    "maxWidth": 150,
                    "shownBy": null
                  },
                  {
                    "field": "layer_05/sum_insured",
                    "maxWidth": 150,
                    "shownBy": null
                  },
                  {
                    "field": "layer_05/ilf_xs_and_xm",
                    "maxWidth": 150,
                    "shownBy": null
                  },
                  {
                    "field": "layer_05/ilf_xs_and_xl",
                    "maxWidth": 150,
                    "shownBy": null
                  },
                  {
                    "field": "layer_05/ilf_xs_and_lmt",
                    "maxWidth": 150,
                    "shownBy": null
                  },
                  {
                    "field": "layer_05/ilf_xs",
                    "maxWidth": 150,
                    "shownBy": null
                  },
                  {
                    "field": "layer_05/pr_pct",
                    "maxWidth": 150,
                    "shownBy": null
                  },
                  {
                    "field": "layer_05/pr_net_premium",
                    "maxWidth": 150,
                    "shownBy": null
                  }
                ]}
                  dynamic={true}
                  kb-interactive={true} />
              </HX.Pane>
            </HX.Pane>
          </HX.Section>
        </HX.With>
      </HX.Page>
      <HX.Page title="Limit Average Severity"
        viewScale={0.8}
        shownBy="model_state/show_steer_las_bdx">
        <HX.With context={{
          "path": "cds/steer/exposure_rating/limit_average_severity/layers",
          "type": "struct"
        }}>
          <HX.Section title="Limit Average Severity">
            <HX.Pane flow="down">
              <HX.Pane>
                <HX.Pane flow="right">
                  <HX.Table title="FGU"
                    data={[
                    "fgu/risk_profiles",
                    "fgu/total"
                  ]}
                    fields={[
                    {
                      "field": "lower",
                      "maxWidth": 150,
                      "shownBy": null
                    },
                    {
                      "field": "upper",
                      "maxWidth": 150,
                      "shownBy": null
                    },
                    {
                      "field": "losses",
                      "maxWidth": 150,
                      "shownBy": null
                    },
                    {
                      "field": "occurrences",
                      "maxWidth": 150,
                      "shownBy": null
                    },
                    {
                      "field": "average",
                      "maxWidth": 150,
                      "shownBy": null
                    },
                    {
                      "field": "las",
                      "maxWidth": 150,
                      "shownBy": null
                    },
                    {
                      "field": "ilf_empirical",
                      "maxWidth": 150,
                      "shownBy": null
                    }
                  ]} />
                  <HX.Notes field="/cds/steer/exposure_rating/risk_profile_bdx/message"
                    shownBy="/model_state/is_bdx_input_issue" />
                </HX.Pane>
                <HX.Pane>
                  <HX.Pane>
                    <HX.Section title="Layer 01"
                      shownBy="/model_state/show_layer_01">
                      <HX.Pane>
                        <HX.Pane>
                          <HX.With context={{
                            "index": 0,
                            "path": "/cds/layers",
                            "type": "list"
                          }}>
                            <HX.Collection fields={[
                              "excess",
                              null,
                              null,
                              null,
                              null,
                              null
                            ]}
                              horizontal={true} />
                            <HX.Collection fields={[
                              "limit",
                              null,
                              null,
                              null,
                              null,
                              null
                            ]}
                              horizontal={true} />
                          </HX.With>
                        </HX.Pane>
                        <HX.Pane>
                          <HX.Table data={[
                            "/cds/steer/exposure_rating/limit_average_severity/layers/layer_01/risk_profiles",
                            "/cds/steer/exposure_rating/limit_average_severity/layers/layer_01/total"
                          ]}
                            fields={[
                            {
                              "field": "current_year/lower",
                              "maxWidth": 150,
                              "shownBy": null
                            },
                            {
                              "field": "current_year/upper",
                              "maxWidth": 150,
                              "shownBy": null
                            },
                            {
                              "field": "current_year/ilf_user_input",
                              "maxWidth": 150,
                              "shownBy": null
                            },
                            {
                              "field": "current_year/ilf_selected",
                              "maxWidth": 150,
                              "shownBy": null
                            },
                            {
                              "field": "current_year/pct_of_claims_to_layer",
                              "maxWidth": 150,
                              "shownBy": null
                            },
                            {
                              "field": "current_year/premium",
                              "maxWidth": 150,
                              "shownBy": null
                            },
                            {
                              "field": "current_year/loss_to_layer",
                              "maxWidth": 150,
                              "shownBy": null
                            },
                            null,
                            {
                              "field": "chart/limit",
                              "maxWidth": 150,
                              "shownBy": null
                            },
                            {
                              "field": "chart/this_year",
                              "maxWidth": 150,
                              "shownBy": null
                            },
                            {
                              "field": "chart/ilf_selected",
                              "maxWidth": 150,
                              "shownBy": null
                            }
                          ]}
                            title="Layer 01"
                            kb-interactive={true}
                            syncColumnWidthsKey="field" />
                        </HX.Pane>
                        <HX.Pane>
                          <HX.With context={{
                            "path": "/cds/steer/exposure_rating/limit_average_severity/layers",
                            "type": "struct"
                          }}>
                            <HX.Collection fields={[
                              "layer_01/glr",
                              null,
                              null,
                              null,
                              null,
                              null
                            ]}
                              horizontal={true} />
                            <HX.Collection fields={[
                              "layer_01/expected_loss",
                              null,
                              null,
                              null,
                              null,
                              null
                            ]}
                              horizontal={true} />
                            <HX.Collection fields={[
                              "layer_01/pure_rate",
                              null,
                              null,
                              null,
                              null,
                              null
                            ]}
                              horizontal={true} />
                            <HX.Collection fields={[
                              "layer_01/rol",
                              null,
                              null,
                              null,
                              null,
                              null
                            ]}
                              horizontal={true} />
                            <HX.Collection fields={[
                              "/model_state/show_las_chart_layer_01",
                              null,
                              null,
                              null,
                              null,
                              null
                            ]}
                              horizontal={true} />
                            <HX.Pane flow="right"
                              shownBy="/model_state/show_las_chart_layer_01">
                              <HX.Pane ratio={1}>
                                <CustomComponent title="% of Claims to Layer"
                                  xAxisLabel="Limit"
                                  yAxisLabel="% of Claims to Layer"
                                  series={[
                                  {
                                    "points": [
                                      {
                                        "list": "/cds/steer/exposure_rating/limit_average_severity/layers/layer_01/risk_profiles",
                                        "x": "chart/limit",
                                        "y": "chart/this_year"
                                      }
                                    ],
                                    "seriesLabel": "Current Year"
                                  }
                                ]} />
                              </HX.Pane>
                              <HX.Pane ratio={1}>
                                <CustomComponent title="ILF"
                                  xAxisLabel="Limit"
                                  yAxisLabel="ILF"
                                  series={[
                                  {
                                    "points": [
                                      {
                                        "list": "/cds/steer/exposure_rating/limit_average_severity/layers/layer_01/risk_profiles",
                                        "x": "chart/limit",
                                        "y": "chart/ilf_selected"
                                      }
                                    ],
                                    "seriesLabel": "ILF Empirical"
                                  },
                                  {
                                    "points": [
                                      {
                                        "list": "/cds/steer/exposure_rating/limit_average_severity/layers/fgu/risk_profiles",
                                        "x": "upper",
                                        "y": "ilf_empirical"
                                      }
                                    ],
                                    "seriesLabel": "ILF Selected"
                                  }
                                ]} />
                              </HX.Pane>
                            </HX.Pane>
                          </HX.With>
                        </HX.Pane>
                      </HX.Pane>
                    </HX.Section>
                    <HX.Section title="Layer 02"
                      shownBy="/model_state/show_layer_02">
                      <HX.Pane>
                        <HX.Pane>
                          <HX.With context={{
                            "index": 1,
                            "path": "/cds/layers",
                            "type": "list"
                          }}>
                            <HX.Collection fields={[
                              "excess",
                              null,
                              null,
                              null,
                              null,
                              null
                            ]}
                              horizontal={true} />
                            <HX.Collection fields={[
                              "limit",
                              null,
                              null,
                              null,
                              null,
                              null
                            ]}
                              horizontal={true} />
                          </HX.With>
                        </HX.Pane>
                        <HX.Pane>
                          <HX.Table data={[
                            "/cds/steer/exposure_rating/limit_average_severity/layers/layer_02/risk_profiles",
                            "/cds/steer/exposure_rating/limit_average_severity/layers/layer_02/total"
                          ]}
                            fields={[
                            {
                              "field": "current_year/lower",
                              "maxWidth": 150,
                              "shownBy": null
                            },
                            {
                              "field": "current_year/upper",
                              "maxWidth": 150,
                              "shownBy": null
                            },
                            {
                              "field": "current_year/ilf_user_input",
                              "maxWidth": 150,
                              "shownBy": null
                            },
                            {
                              "field": "current_year/ilf_selected",
                              "maxWidth": 150,
                              "shownBy": null
                            },
                            {
                              "field": "current_year/pct_of_claims_to_layer",
                              "maxWidth": 150,
                              "shownBy": null
                            },
                            {
                              "field": "current_year/premium",
                              "maxWidth": 150,
                              "shownBy": null
                            },
                            {
                              "field": "current_year/loss_to_layer",
                              "maxWidth": 150,
                              "shownBy": null
                            },
                            null,
                            {
                              "field": "chart/limit",
                              "maxWidth": 150,
                              "shownBy": null
                            },
                            {
                              "field": "chart/this_year",
                              "maxWidth": 150,
                              "shownBy": null
                            },
                            {
                              "field": "chart/ilf_selected",
                              "maxWidth": 150,
                              "shownBy": null
                            }
                          ]}
                            title="Layer 02"
                            kb-interactive={true}
                            syncColumnWidthsKey="field" />
                        </HX.Pane>
                        <HX.Pane>
                          <HX.With context={{
                            "path": "/cds/steer/exposure_rating/limit_average_severity/layers",
                            "type": "struct"
                          }}>
                            <HX.Collection fields={[
                              "layer_02/glr",
                              null,
                              null,
                              null,
                              null,
                              null
                            ]}
                              horizontal={true} />
                            <HX.Collection fields={[
                              "layer_02/expected_loss",
                              null,
                              null,
                              null,
                              null,
                              null
                            ]}
                              horizontal={true} />
                            <HX.Collection fields={[
                              "layer_02/pure_rate",
                              null,
                              null,
                              null,
                              null,
                              null
                            ]}
                              horizontal={true} />
                            <HX.Collection fields={[
                              "layer_02/rol",
                              null,
                              null,
                              null,
                              null,
                              null
                            ]}
                              horizontal={true} />
                            <HX.Collection fields={[
                              "/model_state/show_las_chart_layer_02",
                              null,
                              null,
                              null,
                              null,
                              null
                            ]}
                              horizontal={true} />
                            <HX.Pane flow="right"
                              shownBy="/model_state/show_las_chart_layer_02">
                              <HX.Pane ratio={1}>
                                <CustomComponent title="% of Claims to Layer"
                                  xAxisLabel="Limit"
                                  yAxisLabel="% of Claims to Layer"
                                  series={[
                                  {
                                    "points": [
                                      {
                                        "list": "/cds/steer/exposure_rating/limit_average_severity/layers/layer_02/risk_profiles",
                                        "x": "chart/limit",
                                        "y": "chart/this_year"
                                      }
                                    ],
                                    "seriesLabel": "Current Year"
                                  }
                                ]} />
                              </HX.Pane>
                              <HX.Pane ratio={1}>
                                <CustomComponent title="ILF"
                                  xAxisLabel="Limit"
                                  yAxisLabel="ILF"
                                  series={[
                                  {
                                    "points": [
                                      {
                                        "list": "/cds/steer/exposure_rating/limit_average_severity/layers/layer_02/risk_profiles",
                                        "x": "chart/limit",
                                        "y": "chart/ilf_selected"
                                      }
                                    ],
                                    "seriesLabel": "ILF Empirical"
                                  },
                                  {
                                    "points": [
                                      {
                                        "list": "/cds/steer/exposure_rating/limit_average_severity/layers/fgu/risk_profiles",
                                        "x": "upper",
                                        "y": "ilf_empirical"
                                      }
                                    ],
                                    "seriesLabel": "ILF Selected"
                                  }
                                ]} />
                              </HX.Pane>
                            </HX.Pane>
                          </HX.With>
                        </HX.Pane>
                      </HX.Pane>
                    </HX.Section>
                    <HX.Section title="Layer 03"
                      shownBy="/model_state/show_layer_03">
                      <HX.Pane>
                        <HX.Pane>
                          <HX.With context={{
                            "index": 2,
                            "path": "/cds/layers",
                            "type": "list"
                          }}>
                            <HX.Collection fields={[
                              "excess",
                              null,
                              null,
                              null,
                              null,
                              null
                            ]}
                              horizontal={true} />
                            <HX.Collection fields={[
                              "limit",
                              null,
                              null,
                              null,
                              null,
                              null
                            ]}
                              horizontal={true} />
                          </HX.With>
                        </HX.Pane>
                        <HX.Pane>
                          <HX.Table data={[
                            "/cds/steer/exposure_rating/limit_average_severity/layers/layer_03/risk_profiles",
                            "/cds/steer/exposure_rating/limit_average_severity/layers/layer_03/total"
                          ]}
                            fields={[
                            {
                              "field": "current_year/lower",
                              "maxWidth": 150,
                              "shownBy": null
                            },
                            {
                              "field": "current_year/upper",
                              "maxWidth": 150,
                              "shownBy": null
                            },
                            {
                              "field": "current_year/ilf_user_input",
                              "maxWidth": 150,
                              "shownBy": null
                            },
                            {
                              "field": "current_year/ilf_selected",
                              "maxWidth": 150,
                              "shownBy": null
                            },
                            {
                              "field": "current_year/pct_of_claims_to_layer",
                              "maxWidth": 150,
                              "shownBy": null
                            },
                            {
                              "field": "current_year/premium",
                              "maxWidth": 150,
                              "shownBy": null
                            },
                            {
                              "field": "current_year/loss_to_layer",
                              "maxWidth": 150,
                              "shownBy": null
                            },
                            null,
                            {
                              "field": "chart/limit",
                              "maxWidth": 150,
                              "shownBy": null
                            },
                            {
                              "field": "chart/this_year",
                              "maxWidth": 150,
                              "shownBy": null
                            },
                            {
                              "field": "chart/ilf_selected",
                              "maxWidth": 150,
                              "shownBy": null
                            }
                          ]}
                            title="Layer 03"
                            kb-interactive={true}
                            syncColumnWidthsKey="field" />
                        </HX.Pane>
                        <HX.Pane>
                          <HX.With context={{
                            "path": "/cds/steer/exposure_rating/limit_average_severity/layers",
                            "type": "struct"
                          }}>
                            <HX.Collection fields={[
                              "layer_03/glr",
                              null,
                              null,
                              null,
                              null,
                              null
                            ]}
                              horizontal={true} />
                            <HX.Collection fields={[
                              "layer_03/expected_loss",
                              null,
                              null,
                              null,
                              null,
                              null
                            ]}
                              horizontal={true} />
                            <HX.Collection fields={[
                              "layer_03/pure_rate",
                              null,
                              null,
                              null,
                              null,
                              null
                            ]}
                              horizontal={true} />
                            <HX.Collection fields={[
                              "layer_03/rol",
                              null,
                              null,
                              null,
                              null,
                              null
                            ]}
                              horizontal={true} />
                            <HX.Collection fields={[
                              "/model_state/show_las_chart_layer_03",
                              null,
                              null,
                              null,
                              null,
                              null
                            ]}
                              horizontal={true} />
                            <HX.Pane flow="right"
                              shownBy="/model_state/show_las_chart_layer_03">
                              <HX.Pane ratio={1}>
                                <CustomComponent title="% of Claims to Layer"
                                  xAxisLabel="Limit"
                                  yAxisLabel="% of Claims to Layer"
                                  series={[
                                  {
                                    "points": [
                                      {
                                        "list": "/cds/steer/exposure_rating/limit_average_severity/layers/layer_03/risk_profiles",
                                        "x": "chart/limit",
                                        "y": "chart/this_year"
                                      }
                                    ],
                                    "seriesLabel": "Current Year"
                                  }
                                ]} />
                              </HX.Pane>
                              <HX.Pane ratio={1}>
                                <CustomComponent title="ILF"
                                  xAxisLabel="Limit"
                                  yAxisLabel="ILF"
                                  series={[
                                  {
                                    "points": [
                                      {
                                        "list": "/cds/steer/exposure_rating/limit_average_severity/layers/layer_03/risk_profiles",
                                        "x": "chart/limit",
                                        "y": "chart/ilf_selected"
                                      }
                                    ],
                                    "seriesLabel": "ILF Empirical"
                                  },
                                  {
                                    "points": [
                                      {
                                        "list": "/cds/steer/exposure_rating/limit_average_severity/layers/fgu/risk_profiles",
                                        "x": "upper",
                                        "y": "ilf_empirical"
                                      }
                                    ],
                                    "seriesLabel": "ILF Selected"
                                  }
                                ]} />
                              </HX.Pane>
                            </HX.Pane>
                          </HX.With>
                        </HX.Pane>
                      </HX.Pane>
                    </HX.Section>
                    <HX.Section title="Layer 04"
                      shownBy="/model_state/show_layer_04">
                      <HX.Pane>
                        <HX.Pane>
                          <HX.With context={{
                            "index": 3,
                            "path": "/cds/layers",
                            "type": "list"
                          }}>
                            <HX.Collection fields={[
                              "excess",
                              null,
                              null,
                              null,
                              null,
                              null
                            ]}
                              horizontal={true} />
                            <HX.Collection fields={[
                              "limit",
                              null,
                              null,
                              null,
                              null,
                              null
                            ]}
                              horizontal={true} />
                          </HX.With>
                        </HX.Pane>
                        <HX.Pane>
                          <HX.Table data={[
                            "/cds/steer/exposure_rating/limit_average_severity/layers/layer_04/risk_profiles",
                            "/cds/steer/exposure_rating/limit_average_severity/layers/layer_04/total"
                          ]}
                            fields={[
                            {
                              "field": "current_year/lower",
                              "maxWidth": 150,
                              "shownBy": null
                            },
                            {
                              "field": "current_year/upper",
                              "maxWidth": 150,
                              "shownBy": null
                            },
                            {
                              "field": "current_year/ilf_user_input",
                              "maxWidth": 150,
                              "shownBy": null
                            },
                            {
                              "field": "current_year/ilf_selected",
                              "maxWidth": 150,
                              "shownBy": null
                            },
                            {
                              "field": "current_year/pct_of_claims_to_layer",
                              "maxWidth": 150,
                              "shownBy": null
                            },
                            {
                              "field": "current_year/premium",
                              "maxWidth": 150,
                              "shownBy": null
                            },
                            {
                              "field": "current_year/loss_to_layer",
                              "maxWidth": 150,
                              "shownBy": null
                            },
                            null,
                            {
                              "field": "chart/limit",
                              "maxWidth": 150,
                              "shownBy": null
                            },
                            {
                              "field": "chart/this_year",
                              "maxWidth": 150,
                              "shownBy": null
                            },
                            {
                              "field": "chart/ilf_selected",
                              "maxWidth": 150,
                              "shownBy": null
                            }
                          ]}
                            title="Layer 04"
                            kb-interactive={true}
                            syncColumnWidthsKey="field" />
                        </HX.Pane>
                        <HX.Pane>
                          <HX.With context={{
                            "path": "/cds/steer/exposure_rating/limit_average_severity/layers",
                            "type": "struct"
                          }}>
                            <HX.Collection fields={[
                              "layer_04/glr",
                              null,
                              null,
                              null,
                              null,
                              null
                            ]}
                              horizontal={true} />
                            <HX.Collection fields={[
                              "layer_04/expected_loss",
                              null,
                              null,
                              null,
                              null,
                              null
                            ]}
                              horizontal={true} />
                            <HX.Collection fields={[
                              "layer_04/pure_rate",
                              null,
                              null,
                              null,
                              null,
                              null
                            ]}
                              horizontal={true} />
                            <HX.Collection fields={[
                              "layer_04/rol",
                              null,
                              null,
                              null,
                              null,
                              null
                            ]}
                              horizontal={true} />
                            <HX.Collection fields={[
                              "/model_state/show_las_chart_layer_04",
                              null,
                              null,
                              null,
                              null,
                              null
                            ]}
                              horizontal={true} />
                            <HX.Pane flow="right"
                              shownBy="/model_state/show_las_chart_layer_04">
                              <HX.Pane ratio={1}>
                                <CustomComponent title="% of Claims to Layer"
                                  xAxisLabel="Limit"
                                  yAxisLabel="% of Claims to Layer"
                                  series={[
                                  {
                                    "points": [
                                      {
                                        "list": "/cds/steer/exposure_rating/limit_average_severity/layers/layer_04/risk_profiles",
                                        "x": "chart/limit",
                                        "y": "chart/this_year"
                                      }
                                    ],
                                    "seriesLabel": "Current Year"
                                  }
                                ]} />
                              </HX.Pane>
                              <HX.Pane ratio={1}>
                                <CustomComponent title="ILF"
                                  xAxisLabel="Limit"
                                  yAxisLabel="ILF"
                                  series={[
                                  {
                                    "points": [
                                      {
                                        "list": "/cds/steer/exposure_rating/limit_average_severity/layers/layer_04/risk_profiles",
                                        "x": "chart/limit",
                                        "y": "chart/ilf_selected"
                                      }
                                    ],
                                    "seriesLabel": "ILF Empirical"
                                  },
                                  {
                                    "points": [
                                      {
                                        "list": "/cds/steer/exposure_rating/limit_average_severity/layers/fgu/risk_profiles",
                                        "x": "upper",
                                        "y": "ilf_empirical"
                                      }
                                    ],
                                    "seriesLabel": "ILF Selected"
                                  }
                                ]} />
                              </HX.Pane>
                            </HX.Pane>
                          </HX.With>
                        </HX.Pane>
                      </HX.Pane>
                    </HX.Section>
                    <HX.Section title="Layer 05"
                      shownBy="/model_state/show_layer_05">
                      <HX.Pane>
                        <HX.Pane>
                          <HX.With context={{
                            "index": 4,
                            "path": "/cds/layers",
                            "type": "list"
                          }}>
                            <HX.Collection fields={[
                              "excess",
                              null,
                              null,
                              null,
                              null,
                              null
                            ]}
                              horizontal={true} />
                            <HX.Collection fields={[
                              "limit",
                              null,
                              null,
                              null,
                              null,
                              null
                            ]}
                              horizontal={true} />
                          </HX.With>
                        </HX.Pane>
                        <HX.Pane>
                          <HX.Table data={[
                            "/cds/steer/exposure_rating/limit_average_severity/layers/layer_05/risk_profiles",
                            "/cds/steer/exposure_rating/limit_average_severity/layers/layer_05/total"
                          ]}
                            fields={[
                            {
                              "field": "current_year/lower",
                              "maxWidth": 150,
                              "shownBy": null
                            },
                            {
                              "field": "current_year/upper",
                              "maxWidth": 150,
                              "shownBy": null
                            },
                            {
                              "field": "current_year/ilf_user_input",
                              "maxWidth": 150,
                              "shownBy": null
                            },
                            {
                              "field": "current_year/ilf_selected",
                              "maxWidth": 150,
                              "shownBy": null
                            },
                            {
                              "field": "current_year/pct_of_claims_to_layer",
                              "maxWidth": 150,
                              "shownBy": null
                            },
                            {
                              "field": "current_year/premium",
                              "maxWidth": 150,
                              "shownBy": null
                            },
                            {
                              "field": "current_year/loss_to_layer",
                              "maxWidth": 150,
                              "shownBy": null
                            },
                            null,
                            {
                              "field": "chart/limit",
                              "maxWidth": 150,
                              "shownBy": null
                            },
                            {
                              "field": "chart/this_year",
                              "maxWidth": 150,
                              "shownBy": null
                            },
                            {
                              "field": "chart/ilf_selected",
                              "maxWidth": 150,
                              "shownBy": null
                            }
                          ]}
                            title="Layer 05"
                            kb-interactive={true}
                            syncColumnWidthsKey="field" />
                        </HX.Pane>
                        <HX.Pane>
                          <HX.With context={{
                            "path": "/cds/steer/exposure_rating/limit_average_severity/layers",
                            "type": "struct"
                          }}>
                            <HX.Collection fields={[
                              "layer_05/glr",
                              null,
                              null,
                              null,
                              null,
                              null
                            ]}
                              horizontal={true} />
                            <HX.Collection fields={[
                              "layer_05/expected_loss",
                              null,
                              null,
                              null,
                              null,
                              null
                            ]}
                              horizontal={true} />
                            <HX.Collection fields={[
                              "layer_05/pure_rate",
                              null,
                              null,
                              null,
                              null,
                              null
                            ]}
                              horizontal={true} />
                            <HX.Collection fields={[
                              "layer_05/rol",
                              null,
                              null,
                              null,
                              null,
                              null
                            ]}
                              horizontal={true} />
                            <HX.Collection fields={[
                              "/model_state/show_las_chart_layer_05",
                              null,
                              null,
                              null,
                              null,
                              null
                            ]}
                              horizontal={true} />
                            <HX.Pane flow="right"
                              shownBy="/model_state/show_las_chart_layer_05">
                              <HX.Pane ratio={1}>
                                <CustomComponent title="% of Claims to Layer"
                                  xAxisLabel="Limit"
                                  yAxisLabel="% of Claims to Layer"
                                  series={[
                                  {
                                    "points": [
                                      {
                                        "list": "/cds/steer/exposure_rating/limit_average_severity/layers/layer_05/risk_profiles",
                                        "x": "chart/limit",
                                        "y": "chart/this_year"
                                      }
                                    ],
                                    "seriesLabel": "Current Year"
                                  }
                                ]} />
                              </HX.Pane>
                              <HX.Pane ratio={1}>
                                <CustomComponent title="ILF"
                                  xAxisLabel="Limit"
                                  yAxisLabel="ILF"
                                  series={[
                                  {
                                    "points": [
                                      {
                                        "list": "/cds/steer/exposure_rating/limit_average_severity/layers/layer_05/risk_profiles",
                                        "x": "chart/limit",
                                        "y": "chart/ilf_selected"
                                      }
                                    ],
                                    "seriesLabel": "ILF Empirical"
                                  },
                                  {
                                    "points": [
                                      {
                                        "list": "/cds/steer/exposure_rating/limit_average_severity/layers/fgu/risk_profiles",
                                        "x": "upper",
                                        "y": "ilf_empirical"
                                      }
                                    ],
                                    "seriesLabel": "ILF Selected"
                                  }
                                ]} />
                              </HX.Pane>
                            </HX.Pane>
                          </HX.With>
                        </HX.Pane>
                      </HX.Pane>
                    </HX.Section>
                  </HX.Pane>
                </HX.Pane>
                <HX.Pane>
                  <HX.Table title="Summary"
                    with="/cds"
                    data={[
                    "layers"
                  ]}
                    fields={[
                    {
                      "field": "excess",
                      "maxWidth": 120,
                      "shownBy": null
                    },
                    {
                      "field": "limit",
                      "maxWidth": 120,
                      "shownBy": null
                    },
                    {
                      "field": "pricing_selection/limit_average_severity/pure_rate",
                      "maxWidth": 120,
                      "shownBy": null
                    }
                  ]}
                    kb-interactive={true}
                    syncColumnWidthsKey="field"
                    rowHeaderSettings={{
                    "width": 150
                  }} />
                </HX.Pane>
              </HX.Pane>
            </HX.Pane>
          </HX.Section>
        </HX.With>
      </HX.Page>
      <HX.Page title="Trial History"
        viewScale={0.8}
        shownBy="model_state/show_healthcare_cat">
        <HX.With context={{
          "path": "cds/healthcare_cat",
          "type": "struct"
        }}>
          <HX.Section title="Trial History">
            <HX.Pane flow="right">
              <HX.Pane flow="down" />
              <HX.Pane />
              <HX.Pane />
              <HX.Pane />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
            <HX.Pane flow="right">
              <HX.Pane>
                <HX.Table title="Trial History"
                  with="trial_history"
                  data={[
                  {
                    "datum": "trial",
                    "elementLabelBy": "display_yoa"
                  },
                  "total"
                ]}
                  fields={[
                  {
                    "field": "taken_to_trial",
                    "maxWidth": 150,
                    "shownBy": null
                  },
                  {
                    "field": "wins",
                    "maxWidth": 150,
                    "shownBy": null
                  },
                  {
                    "field": "losses",
                    "maxWidth": 150,
                    "shownBy": null
                  },
                  {
                    "field": "mistrials",
                    "maxWidth": 150,
                    "shownBy": null
                  },
                  {
                    "field": "win_pct",
                    "maxWidth": 150,
                    "shownBy": null
                  }
                ]}
                  kb-interactive={true} />
              </HX.Pane>
              <HX.Pane>
                <CustomComponent title="Historic Trend On Trials in Court"
                  data={[
                  {
                    "labelBy": "uw_year",
                    "list": "/cds/healthcare_cat/trial_history/trial"
                  }
                ]}
                  traces={[
                  {
                    "color": "#4085fd",
                    "field": "taken_to_trial",
                    "label": "Taken To Trial"
                  }
                ]}
                  series={[
                  {
                    "points": [
                      {
                        "list": "/cds/healthcare_cat/trial_history/trial",
                        "x": "uw_year",
                        "y": "win_pct"
                      }
                    ],
                    "seriesColor": "#e24a0e",
                    "seriesLabel": "Win %",
                    "seriesLineType": "solid",
                    "seriesMode": "lines"
                  }
                ]}
                  xAxisTickAngle={-45}
                  xAxisLabel="Taken To Trial"
                  yAxisLabel="Win %"
                  barMode="group"
                  gapBetweenBarsSize={0.3}
                  width={700}
                  height={500}
                  y2SeparateAxis={true} />
              </HX.Pane>
            </HX.Pane>
            <HX.Pane>
              <HX.Table title="Underwiting View on Average History Loss Ratio"
                with="trial_history"
                data={[
                "uw_view"
              ]}
                fields={[
                {
                  "field": "from_year",
                  "width": 150
                },
                {
                  "field": "to_year",
                  "width": 150
                },
                {
                  "field": "taken_to_trial",
                  "maxWidth": 150,
                  "shownBy": null
                },
                {
                  "field": "wins",
                  "maxWidth": 150,
                  "shownBy": null
                },
                {
                  "field": "losses",
                  "maxWidth": 150,
                  "shownBy": null
                },
                {
                  "field": "mistrials",
                  "maxWidth": 150,
                  "shownBy": null
                },
                {
                  "field": "win_pct",
                  "maxWidth": 150,
                  "shownBy": null
                }
              ]}
                kb-interactive={true} />
            </HX.Pane>
          </HX.Section>
        </HX.With>
      </HX.Page>
      <HX.Page title="Exposure Territory"
        viewScale={0.8}
        shownBy="model_state/show_healthcare_cat">
        <HX.With context={{
          "path": "cds/healthcare_cat/exposure_territory",
          "type": "struct"
        }}>
          <HX.Section title="Exposure Type">
            <HX.Pane flow="right">
              <HX.Pane flow="down">
                <HX.Collection fields={[
                  "type_of_business",
                  "specialty"
                ]}
                  syncColumnWidthsKey="measure" />
              </HX.Pane>
              <HX.Pane />
              <HX.Pane />
              <HX.Pane />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
          </HX.Section>
          <HX.Section title="Overall Exposure By Year">
            <HX.Pane>
              <HX.Table data={[
                {
                  "datum": "overall_exposure_per_year",
                  "elementLabelBy": "display_yoa"
                }
              ]}
                fields={[
                {
                  "field": "physicians",
                  "maxWidth": 150,
                  "shownBy": null
                },
                {
                  "field": "professional_associations",
                  "maxWidth": 150,
                  "shownBy": null
                },
                {
                  "field": "ambulatory_surgery_centres",
                  "maxWidth": 150,
                  "shownBy": null
                },
                {
                  "field": "hospitals",
                  "maxWidth": 150,
                  "shownBy": null
                },
                {
                  "field": "ltc_facilities",
                  "maxWidth": 150,
                  "shownBy": null
                },
                {
                  "field": "other_facilities",
                  "maxWidth": 150,
                  "shownBy": null
                },
                {
                  "field": "dentists",
                  "maxWidth": 150,
                  "shownBy": null
                },
                {
                  "field": "others",
                  "maxWidth": 150,
                  "shownBy": null
                },
                {
                  "field": "total_physicians_in_force",
                  "maxWidth": 150,
                  "shownBy": null
                }
              ]}
                kb-interactive={true} />
            </HX.Pane>
            <HX.Pane>
              <CustomComponent title="Exposure Mix per Year"
                data={[
                {
                  "labelBy": "uw_year",
                  "list": "/cds/healthcare_cat/exposure_territory/overall_exposure_per_year"
                }
              ]}
                traces={[
                {
                  "field": "physicians",
                  "label": "Physicians"
                },
                {
                  "field": "professional_associations",
                  "label": "Professional Associations"
                },
                {
                  "field": "ambulatory_surgery_centres",
                  "label": "Ambulatory Surgery Centres"
                },
                {
                  "field": "hospitals",
                  "label": "Hospitals"
                },
                {
                  "field": "ltc_facilities",
                  "label": "LTC Facilities"
                },
                {
                  "field": "other_facilities",
                  "label": "Other Facilities"
                },
                {
                  "field": "dentists",
                  "label": "Dentists"
                },
                {
                  "field": "others",
                  "label": "Others"
                }
              ]}
                xAxisTickAngle={-45}
                gapBetweenBarsSize={0.1}
                xAxisLabel="YOA"
                yAxisLabel="Number of Employees"
                barMode="stack"
                yAxisTickFormat="0"
                width={700}
                height={500} />
            </HX.Pane>
          </HX.Section>
          <HX.Section title="Exposure Split By State">
            <HX.Pane>
              <HX.Collection fields={[
                "choose_split_by"
              ]}
                syncColumnWidthsKey="measure" />
            </HX.Pane>
            <HX.Pane>
              <HX.Table title="Exposure Split By State"
                data={[
                {
                  "datum": "exposure_spit_by_state"
                }
              ]}
                fields={[
                {
                  "field": "venue",
                  "maxWidth": 150,
                  "shownBy": null
                },
                {
                  "field": "premium_written",
                  "maxWidth": 150,
                  "shownBy": null
                },
                {
                  "field": "total_pif_current_year",
                  "maxWidth": 150,
                  "shownBy": null
                },
                {
                  "field": "split",
                  "maxWidth": 150,
                  "shownBy": null
                }
              ]}
                kb-interactive={true} />
            </HX.Pane>
          </HX.Section>
        </HX.With>
      </HX.Page>
      <HX.Page title="Pricing Specifics"
        viewScale={0.8}
        shownBy="model_state/show_healthcare_cat">
        <HX.With context={{
          "path": "cds/healthcare_cat",
          "type": "struct"
        }}>
          <HX.Section title="Pricing Specifics">
            <HX.Pane>
              <HX.Table with="pricing"
                data={[
                "territory_adjustment",
                "trial_history_adjustment",
                "type_of_business_adjustment",
                "specialty_adjustment",
                "high_low_adjustment",
                "social_inflation_impact",
                "total_risk_adjustment"
              ]}
                fields={[
                {
                  "field": "value",
                  "width": 150
                },
                {
                  "field": "select",
                  "width": 150
                }
              ]}
                kb-interactive={true}
                rowHeaderSettings={{
                "width": 350
              }} />
            </HX.Pane>
          </HX.Section>
          <HX.Section title="Pricing Information">
            <HX.Pane>
              <HX.Table data={[
                {
                  "datum": "/cds/layers",
                  "width": 150
                }
              ]}
                fields={[
                "healthcare_cat/gross_portfolio_size",
                "epi_100",
                null,
                "excess",
                "limit",
                "healthcare_cat/detachment",
                null,
                "healthcare_cat/expected_cost_in_layer_total",
                "healthcare_cat/expected_cost_in_layer_beazley_share"
              ]}
                kb-interactive={true}
                transpose={true}
                rowHeaderSettings={{
                "width": 350
              }} />
            </HX.Pane>
          </HX.Section>
          <HX.Section title="Loss Distribution">
            <HX.Pane flow="right">
              <HX.Pane ratio={1}>
                <HX.Collection with="pricing"
                  fields={[
                  "mean_cat_ulr",
                  "decay_factor",
                  "loss_ratio_1_in_50"
                ]} />
              </HX.Pane>
              <HX.Pane ratio={1} />
              <HX.Pane ratio={1} />
              <HX.Pane ratio={1} />
              <HX.Pane ratio={1} />
            </HX.Pane>
            <HX.Pane flow="right">
              <HX.Pane>
                <HX.Table title="Loss distribution"
                  data={[
                  {
                    "datum": "pricing/loss_distribution_summary",
                    "elementLabelBy": "loss_percentile_display"
                  }
                ]}
                  fields={[
                  {
                    "field": "ulr",
                    "width": 150
                  }
                ]}
                  kb-interactive={true}
                  rowHeaderSettings={{
                  "width": 350
                }} />
              </HX.Pane>
              <HX.Pane>
                <CustomComponent title="ULR Cumulative Loss Distribution"
                  xAxisLabel="Probability of Loss"
                  yAxisLabel="Loss Ratio"
                  yAxis2Label=""
                  xAxisMin={0.9}
                  xAxisStep={0.1}
                  height={700}
                  width={600}
                  line_thickness={1}
                  legend_position="center"
                  series={[
                  {
                    "colour": "#CA3397",
                    "label": "Loss Ratio",
                    "line_type": "lines+marker",
                    "points": [
                      {
                        "list": "/healthcare_cat/pricing_calc/loss_distribution_calculation",
                        "x": "loss_percentile",
                        "y": "ulr"
                      }
                    ],
                    "yaxis": "y"
                  }
                ]} />
              </HX.Pane>
            </HX.Pane>
          </HX.Section>
        </HX.With>
      </HX.Page>
      <HX.Page title="Pricing Calculation"
        fullWidth={true}
        viewScale={0.8}
        shownBy="model_state/show_healthcare_cat">
        <HX.With context={{
          "path": "cds/healthcare_cat",
          "type": "struct"
        }}>
          <HX.Section title="Expected Cost Per Layer">
            <HX.Pane>
              <HX.Table data={[
                {
                  "datum": "/cds/layers",
                  "width": 150
                }
              ]}
                fields={[
                "healthcare_cat/expected_cost_in_layer_total",
                "healthcare_cat/expected_cost_in_layer_beazley_share"
              ]}
                kb-interactive={true}
                transpose={true}
                rowHeaderSettings={{
                "width": 350
              }} />
            </HX.Pane>
          </HX.Section>
          <HX.Section title="Pricing Calculation">
            <HX.Pane>
              <HX.Table title="Loss distribution"
                data={[
                "/healthcare_cat/pricing_calc/loss_distribution_calculation"
              ]}
                fields={[
                {
                  "field": "band_size",
                  "width": 150
                },
                {
                  "field": "loss_percentile",
                  "width": 150
                },
                {
                  "field": "ulr",
                  "width": 150
                },
                null,
                {
                  "field": "fgu_expected_cat_loss_01",
                  "width": 150
                },
                {
                  "field": "expected_loss_in_layer_01",
                  "width": 150
                },
                {
                  "field": "expected_loss_x_prob_of_loss_01",
                  "width": 150
                },
                null,
                {
                  "field": "fgu_expected_cat_loss_02",
                  "width": 150
                },
                {
                  "field": "expected_loss_in_layer_02",
                  "width": 150
                },
                {
                  "field": "expected_loss_x_prob_of_loss_02",
                  "width": 150
                },
                null,
                {
                  "field": "fgu_expected_cat_loss_03",
                  "width": 150
                },
                {
                  "field": "expected_loss_in_layer_03",
                  "width": 150
                },
                {
                  "field": "expected_loss_x_prob_of_loss_03",
                  "width": 150
                },
                null,
                {
                  "field": "fgu_expected_cat_loss_04",
                  "width": 150
                },
                {
                  "field": "expected_loss_in_layer_04",
                  "width": 150
                },
                {
                  "field": "expected_loss_x_prob_of_loss_04",
                  "width": 150
                },
                null,
                {
                  "field": "fgu_expected_cat_loss_05",
                  "width": 150
                },
                {
                  "field": "expected_loss_in_layer_05",
                  "width": 150
                },
                {
                  "field": "expected_loss_x_prob_of_loss_05",
                  "width": 150
                }
              ]}
                kb-interactive={true} />
            </HX.Pane>
          </HX.Section>
        </HX.With>
      </HX.Page>
      <HX.Page title="Pricing Selection"
        viewScale={0.8}
        shownBy="model_state/show_rater_priced">
        <HX.Section title="Pricing Selection">
          <HX.Pane>
            <HX.Pane flow="right"
              reflow={false}>
              <HX.Pane ratio={5}>
                <HX.Table title="Pricing assumptions"
                  with="cds"
                  data={[
                  {
                    "datum": "layers",
                    "width": 220
                  }
                ]}
                  fields={[
                  "status",
                  "currency",
                  "limit",
                  "excess",
                  "epi_100"
                ]}
                  kb-interactive={true}
                  rowHeaderSettings={{
                  "width": 170
                }}
                  transpose={true} />
              </HX.Pane>
              <HX.Pane ratio={2}>
                <HX.Table title="COB Assumptions"
                  with="cds/pricing_selection"
                  data={[
                  "pareto_parameters",
                  "odf_parameters"
                ]}
                  fields={[
                  {
                    "field": "default",
                    "maxWidth": 150
                  },
                  {
                    "field": "overwrite",
                    "maxWidth": 150
                  },
                  {
                    "field": "selected",
                    "maxWidth": 150
                  }
                ]}
                  kb-interactive={true}
                  rowHeaderSettings={{
                  "width": 170
                }} />
                <HX.Notes field="/model_state/pure_premium_error_message"
                  shownBy="/model_state/is_pure_premium_not_calculated" />
                <HX.Button task="advanced_features_task"
                  title="Calculate Advanced Features" />
              </HX.Pane>
            </HX.Pane>
            <HX.Pane>
              <HX.Table title="Final Selection"
                with="cds"
                data={[
                {
                  "datum": "layers",
                  "width": 220
                }
              ]}
                fields={[
                "pricing_selection/final_selection/total_weighting",
                "pricing_selection/final_selection/plr_method",
                "pricing_selection/final_selection/pure_rate",
                "pricing_selection/final_selection/pure_premium",
                "pricing_selection/final_selection/pure_rol"
              ]}
                kb-interactive={true}
                rowHeaderSettings={{
                "width": 170
              }}
                transpose={true} />
            </HX.Pane>
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Detailed (exc. Advanced Features)">
          <HX.Table title="Risk Profiles Bdx (Exposure)"
            with="cds"
            shownBy="/model_state/show_steer_risk_bdx"
            data={[
            {
              "datum": "layers",
              "width": 220
            }
          ]}
            fields={[
            "pricing_selection/risk_profile_bdx/cedant_loss_ratio",
            "pricing_selection/risk_profile_bdx/pure_rate",
            "pricing_selection/risk_profile_bdx/pure_premium",
            "pricing_selection/risk_profile_bdx/pure_rol",
            "pricing_selection/risk_profile_bdx/weighting"
          ]}
            kb-interactive={true}
            rowHeaderSettings={{
            "width": 170
          }}
            transpose={true} />
          <HX.Table title="Burning Cost (Experience)"
            with="cds"
            shownBy="/model_state/show_steer_experience_rating"
            data={[
            {
              "datum": "layers",
              "width": 220
            }
          ]}
            fields={[
            "pricing_selection/burning_cost/pure_rate",
            "pricing_selection/burning_cost/pure_premium",
            "pricing_selection/burning_cost/pure_rol",
            "pricing_selection/burning_cost/weighting"
          ]}
            kb-interactive={true}
            rowHeaderSettings={{
            "width": 170
          }}
            transpose={true} />
          <HX.Table title="LAS (Exposure)"
            with="cds"
            shownBy="/model_state/show_steer_las_bdx"
            data={[
            {
              "datum": "layers",
              "width": 220
            }
          ]}
            fields={[
            "pricing_selection/limit_average_severity/pure_rate",
            "pricing_selection/limit_average_severity/pure_premium",
            "pricing_selection/limit_average_severity/pure_rol",
            "pricing_selection/limit_average_severity/weighting"
          ]}
            kb-interactive={true}
            rowHeaderSettings={{
            "width": 170
          }}
            transpose={true} />
          <HX.Table title="Clash Rater *** Pending Implementation ***"
            with="cds"
            shownBy="/model_state/is_clash"
            data={[
            {
              "datum": "layers",
              "width": 220
            }
          ]}
            fields={[
            "pricing_selection/clash/pure_rate",
            "pricing_selection/clash/pure_premium",
            "pricing_selection/clash/pure_rol",
            "pricing_selection/clash/weighting"
          ]}
            kb-interactive={true}
            rowHeaderSettings={{
            "width": 170
          }}
            transpose={true} />
          <HX.Table title="Healthcare CAT Rater"
            with="cds"
            shownBy="/model_state/is_healthcare_cat"
            data={[
            {
              "datum": "layers",
              "width": 220
            }
          ]}
            fields={[
            "pricing_selection/healthcare_cat/pure_rate",
            "pricing_selection/healthcare_cat/pure_premium",
            "pricing_selection/healthcare_cat/pure_rol",
            "pricing_selection/healthcare_cat/weighting"
          ]}
            kb-interactive={true}
            rowHeaderSettings={{
            "width": 170
          }}
            transpose={true} />
          <HX.Table title="Other"
            with="cds"
            shownBy="/model_state/is_not_clash"
            data={[
            {
              "datum": "layers",
              "width": 220
            }
          ]}
            fields={[
            "pricing_selection/other_method/pure_rate",
            "pricing_selection/other_method/pure_premium",
            "pricing_selection/other_method/pure_rol",
            "pricing_selection/other_method/weighting"
          ]}
            kb-interactive={true}
            rowHeaderSettings={{
            "width": 170
          }}
            transpose={true} />
          <HX.Table title="Other (Clash Manual Input)"
            shownBy="/model_state/is_clash"
            with="cds"
            data={[
            {
              "datum": "layers",
              "width": 220
            }
          ]}
            fields={[
            "pricing_selection/other_method/pure_rate",
            "pricing_selection/other_method/pure_premium",
            "pricing_selection/other_method/pure_rol",
            "pricing_selection/other_method/weighting"
          ]}
            kb-interactive={true}
            rowHeaderSettings={{
            "width": 170
          }}
            transpose={true} />
          <HX.Notes field="/cds/other_method_rationale"
            title="Other Method Rationale" />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Advanced Features"
        fullWidth={true}
        viewScale={0.8}
        shownBy="model_state/show_rater_priced">
        <HX.Section title="Advanced Features">
          <HX.Pane>
            <HX.Pane flow="right"
              reflow={false}>
              <HX.Pane ratio={5}>
                <HX.Table title="Loss Cost Features - Loss Impact"
                  with="cds"
                  data={[
                  "layers"
                ]}
                  fields={[
                  {
                    "field": "limit",
                    "maxWidth": 150,
                    "shownBy": null
                  },
                  {
                    "field": "excess",
                    "maxWidth": 150,
                    "shownBy": null
                  },
                  {
                    "field": "expected_loss",
                    "maxWidth": 150,
                    "shownBy": null
                  },
                  {
                    "field": "expected_aad.read_only",
                    "maxWidth": 150,
                    "shownBy": null
                  },
                  {
                    "field": "loss_corridor_loss_cost.read_only",
                    "maxWidth": 150,
                    "shownBy": null
                  },
                  {
                    "field": "expected_losses_after_loss_sensitive_features",
                    "maxWidth": 150,
                    "shownBy": null
                  }
                ]}
                  kb-interactive={true} />
              </HX.Pane>
              <HX.Pane ratio={2}>
                <HX.Pane>
                  <HX.Table title="COB Assumptions"
                    with="cds/pricing_selection"
                    data={[
                    "pareto_parameters",
                    "odf_parameters"
                  ]}
                    fields={[
                    {
                      "field": "default",
                      "maxWidth": 150,
                      "shownBy": null
                    },
                    {
                      "field": "overwrite",
                      "maxWidth": 150,
                      "shownBy": null
                    },
                    {
                      "field": "selected",
                      "maxWidth": 150,
                      "shownBy": null
                    }
                  ]}
                    kb-interactive={true}
                    rowHeaderSettings={{
                    "width": 170
                  }} />
                </HX.Pane>
                <HX.Pane>
                  <HX.Notes field="/model_state/pure_premium_error_message"
                    shownBy="/model_state/is_pure_premium_not_calculated" />
                  <HX.Button task="advanced_features_task"
                    title="Calculate Advanced Features" />
                </HX.Pane>
              </HX.Pane>
            </HX.Pane>
            <HX.Pane>
              <HX.Table title="Remuneration Features - Premium Impact"
                with="cds"
                data={[
                "layers"
              ]}
                fields={[
                {
                  "field": "limit",
                  "maxWidth": 150,
                  "shownBy": null
                },
                {
                  "field": "excess",
                  "maxWidth": 150,
                  "shownBy": null
                },
                {
                  "field": "number_of_rips",
                  "maxWidth": 150,
                  "shownBy": null
                },
                {
                  "field": "brokerage_inc_swing",
                  "maxWidth": 150,
                  "shownBy": null
                },
                {
                  "field": "ceding_commission",
                  "maxWidth": 150,
                  "shownBy": null
                },
                {
                  "field": "bkg_gross_or_net",
                  "maxWidth": 150,
                  "shownBy": null
                },
                {
                  "field": "upfront_premium_gross_100",
                  "maxWidth": 150,
                  "shownBy": null
                },
                {
                  "field": "upfront_premium_net_100",
                  "maxWidth": 150,
                  "shownBy": null
                },
                null,
                {
                  "field": "expected_reinstatement_factor.read_only",
                  "maxWidth": 150,
                  "shownBy": null
                },
                {
                  "field": "expected_ncb_pct.read_only",
                  "maxWidth": 150,
                  "shownBy": null
                },
                {
                  "field": "profit_commission.read_only",
                  "maxWidth": 150,
                  "shownBy": null
                },
                {
                  "field": "swing_premium.read_only",
                  "maxWidth": 150,
                  "shownBy": null
                },
                null,
                {
                  "field": "expected_premium_paid_gross_100",
                  "maxWidth": 150,
                  "shownBy": null
                },
                {
                  "field": "expected_premium_paid_net_100",
                  "maxWidth": 150,
                  "shownBy": null
                },
                null,
                {
                  "field": "quoted_premium_100",
                  "maxWidth": 150,
                  "shownBy": null
                },
                {
                  "field": "quoted_premium_net_100",
                  "maxWidth": 150,
                  "shownBy": null
                }
              ]}
                kb-interactive={true} />
            </HX.Pane>
          </HX.Pane>
        </HX.Section>
      </HX.Page>
      <HX.Page title="Rating Summary"
        fullWidth={true}
        viewScale={0.8}
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
        <HX.Section title="Summary">
          <HX.Table title="Priced Quotes"
            data={[
            {
              "datum": "cds/layers",
              "width": 150
            },
            null,
            {
              "datum": "cds/programme_all",
              "width": 150
            },
            null,
            {
              "datum": "cds/programme_selected",
              "width": 150
            }
          ]}
            fields={[
            "status",
            "include_layer",
            "section_reference",
            "currency",
            "limit",
            "excess",
            "epi_100",
            "rate",
            {
              "field": "bpi_case_priced",
              "shownBy": "cds/standard_fields/is_case_priced"
            },
            null,
            {
              "field": "pure_rate",
              "shownBy": "cds/standard_fields/is_rater_priced"
            },
            {
              "field": "expected_loss",
              "shownBy": "cds/standard_fields/is_rater_priced"
            },
            {
              "field": "expected_losses_after_loss_sensitive_features",
              "shownBy": "cds/standard_fields/is_rater_priced"
            },
            {
              "field": "expected_loss_inc_nmp",
              "shownBy": "cds/standard_fields/is_rater_priced"
            },
            null,
            {
              "field": "upfront_premium_gross_100",
              "shownBy": "cds/standard_fields/is_rater_priced"
            },
            {
              "field": "expected_premium_paid_gross_100",
              "shownBy": "cds/standard_fields/is_rater_priced"
            },
            "quoted_premium_100",
            "benchmark_premium_100",
            "technical_premium_100",
            null,
            {
              "field": "upfront_premium_net_100",
              "shownBy": "cds/standard_fields/is_rater_priced"
            },
            {
              "field": "expected_premium_paid_net_100",
              "shownBy": "cds/standard_fields/is_rater_priced"
            },
            "quoted_premium_net_100",
            "benchmark_premium_net_100",
            "technical_premium_net_100",
            null,
            "written_line",
            "quoted_premium",
            null,
            "line_size",
            "bpi",
            "tpi",
            null,
            "pflr",
            "glr",
            "roc"
          ]}
            freezeLeft={0}
            transpose={true}
            kb-interactive={true} />
        </HX.Section>
        <HX.Section title="Layer View"
          shownBy="cds/standard_fields/is_rater_priced">
          <HX.Table data={[
            "cds/layers"
          ]}
            fields={[
            {
              "field": "status",
              "maxWidth": 150,
              "shownBy": null
            },
            {
              "field": "currency",
              "maxWidth": 150,
              "shownBy": null
            },
            {
              "field": "limit",
              "maxWidth": 150,
              "shownBy": null
            },
            {
              "field": "excess",
              "maxWidth": 150,
              "shownBy": null
            },
            {
              "field": "brokerage_inc_swing",
              "maxWidth": 150,
              "shownBy": null
            },
            {
              "field": "ceding_commission",
              "maxWidth": 150,
              "shownBy": null
            },
            {
              "field": "bkg_gross_or_net",
              "maxWidth": 150,
              "shownBy": null
            },
            {
              "field": "expected_aad.read_only",
              "maxWidth": 150,
              "shownBy": null
            },
            {
              "field": "ncb",
              "maxWidth": 150,
              "shownBy": null
            },
            {
              "field": "profit_commission_rate",
              "maxWidth": 150,
              "shownBy": null
            },
            {
              "field": "expense_allowance",
              "maxWidth": 150,
              "shownBy": null
            },
            {
              "field": "claim_frequency",
              "maxWidth": 150,
              "shownBy": null
            },
            {
              "field": "average_cost_per_claim",
              "maxWidth": 150,
              "shownBy": null
            },
            {
              "field": "expected_reinstatement_factor.read_only",
              "maxWidth": 150,
              "shownBy": null
            }
          ]}
            freezeLeft={4}
            kb-interactive={true} />
        </HX.Section>
        <HX.Section title="Reinstatements">
          <HX.Table data={[
            "cds/layers"
          ]}
            fields={[
            {
              "field": "no_reinstatement",
              "maxWidth": 150,
              "shownBy": null
            },
            {
              "field": "reinstatement_pct_1",
              "maxWidth": 150,
              "shownBy": null
            },
            {
              "field": "reinstatement_pct_2",
              "maxWidth": 150,
              "shownBy": null
            },
            {
              "field": "reinstatement_pct_3",
              "maxWidth": 150,
              "shownBy": null
            },
            {
              "field": "reinstatement_pct_4",
              "maxWidth": 150,
              "shownBy": null
            },
            {
              "field": "reinstatement_pct_5",
              "maxWidth": 150,
              "shownBy": null
            },
            {
              "field": "reinstatement_pct_6",
              "maxWidth": 150,
              "shownBy": null
            },
            {
              "field": "reinstatement_pct_7",
              "maxWidth": 150,
              "shownBy": null
            },
            {
              "field": "reinstatement_pct_8",
              "maxWidth": 150,
              "shownBy": null
            },
            {
              "field": "reinstatement_pct_9",
              "maxWidth": 150,
              "shownBy": null
            },
            {
              "field": "reinstatement_pct_10",
              "maxWidth": 150,
              "shownBy": null
            }
          ]}
            freezeLeft={0}
            kb-interactive={true} />
        </HX.Section>
        <HX.Section title="Technical Price Assumptions">
          <HX.Table data={[
            "cds/technical_price_assumptions"
          ]}
            fields={[
            {
              "field": "benchmark_loss_ratio",
              "maxWidth": 150,
              "shownBy": null
            },
            {
              "field": "claims_handling_expenses",
              "maxWidth": 150,
              "shownBy": null
            },
            {
              "field": "fixed_expenses",
              "maxWidth": 150,
              "shownBy": null
            },
            {
              "field": "variable_expenses",
              "maxWidth": 150,
              "shownBy": null
            },
            {
              "field": "investment_income",
              "maxWidth": 150,
              "shownBy": null
            },
            {
              "field": "cost_of_ri",
              "maxWidth": 150,
              "shownBy": null
            },
            {
              "field": "return_on_capital",
              "maxWidth": 150,
              "shownBy": null
            },
            {
              "field": "capital_cost",
              "maxWidth": 150,
              "shownBy": null
            },
            {
              "field": "non_modelled_perils_nmp",
              "maxWidth": 150,
              "shownBy": null
            }
          ]}
            freezeLeft={0}
            kb-interactive={true} />
        </HX.Section>
        <HX.Section title="Case Pricing Analysis Filepath">
          <HX.Notes field="cds/risk_information/case_pricing_analysis_location" />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Rate Change"
        fullWidth={false}
        viewScale={0.8}
        shownBy="model_state/show_rate_change_layer_no_ia_use">
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
                "field": "status.read_only"
              }
            ]}
              transpose={true} />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Pane ratio={1}>
              <HX.Button task="expiring_policy_fetch_task"
                title="Fetch Expiring Data"
                shownBy="cds/rate_change/has_rarc_not_run" />
            </HX.Pane>
            <HX.Pane ratio={1}>
              <HX.Button title="Calculate Rate Change"
                task="rarc_task"
                shownBy="cds/standard_fields/is_rater_priced" />
            </HX.Pane>
            <HX.Pane ratio={1}>
              <HX.Notes field="/model_state/pure_premium_error_message"
                shownBy="/model_state/is_pure_premium_not_calculated" />
            </HX.Pane>
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
              <HX.Table with="rate_change"
                data={[
                "currency",
                "premium/line_100pct/policy_term",
                "premium/beazley_line/policy_term",
                "premium/line_100pct/annualised",
                "premium/beazley_line/annualised",
                "limit",
                "excess",
                "brokerage",
                "rate"
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
                syncColumnWidthsKey="syncRateChange" />
              <HX.Table with="rate_change"
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
                syncColumnWidthsKey="syncRateChange"
                kb-interactive={true} />
              <HX.Collection fields={[
                "rate_change/rate_change_multiplier",
                null,
                null,
                null
              ]}
                horizontal={true} />
              <HX.Collection fields={[
                "rate_change/implied_renewable_rate",
                null,
                null,
                null
              ]}
                horizontal={true} />
              <HX.Collection fields={[
                "rate_change/implied_renewable_premium",
                null,
                null,
                null
              ]}
                horizontal={true} />
              <HX.Collection title="Final Rate Change"
                fields={[
                {
                  "field": "rate_change/rate_change/final",
                  "shownBy": "/cds/standard_fields/is_rater_priced"
                },
                {
                  "field": "rate_change/risk_adjusted_rate_change_case_priced",
                  "shownBy": "/cds/standard_fields/is_case_priced"
                },
                null,
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
              <HX.Table with="rate_change"
                data={[
                "currency",
                "premium/line_100pct/policy_term",
                "premium/beazley_line/policy_term",
                "premium/line_100pct/annualised",
                "premium/beazley_line/annualised",
                "limit",
                "excess",
                "brokerage",
                "rate"
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
                syncColumnWidthsKey="syncRateChange" />
              <HX.Table with="rate_change"
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
                syncColumnWidthsKey="syncRateChange"
                kb-interactive={true} />
              <HX.Collection fields={[
                "rate_change/rate_change_multiplier",
                null,
                null,
                null
              ]}
                horizontal={true} />
              <HX.Collection fields={[
                "rate_change/implied_renewable_rate",
                null,
                null,
                null
              ]}
                horizontal={true} />
              <HX.Collection fields={[
                "rate_change/implied_renewable_premium",
                null,
                null,
                null
              ]}
                horizontal={true} />
              <HX.Collection title="Final Rate Change"
                fields={[
                {
                  "field": "rate_change/rate_change/final",
                  "shownBy": "/cds/standard_fields/is_rater_priced"
                },
                {
                  "field": "rate_change/risk_adjusted_rate_change_case_priced",
                  "shownBy": "/cds/standard_fields/is_case_priced"
                },
                null,
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
              <HX.Table with="rate_change"
                data={[
                "currency",
                "premium/line_100pct/policy_term",
                "premium/beazley_line/policy_term",
                "premium/line_100pct/annualised",
                "premium/beazley_line/annualised",
                "limit",
                "excess",
                "brokerage",
                "rate"
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
                syncColumnWidthsKey="syncRateChange" />
              <HX.Table with="rate_change"
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
                syncColumnWidthsKey="syncRateChange"
                kb-interactive={true} />
              <HX.Collection fields={[
                "rate_change/rate_change_multiplier",
                null,
                null,
                null
              ]}
                horizontal={true} />
              <HX.Collection fields={[
                "rate_change/implied_renewable_rate",
                null,
                null,
                null
              ]}
                horizontal={true} />
              <HX.Collection fields={[
                "rate_change/implied_renewable_premium",
                null,
                null,
                null
              ]}
                horizontal={true} />
              <HX.Collection title="Final Rate Change"
                fields={[
                {
                  "field": "rate_change/rate_change/final",
                  "shownBy": "/cds/standard_fields/is_rater_priced"
                },
                {
                  "field": "rate_change/risk_adjusted_rate_change_case_priced",
                  "shownBy": "/cds/standard_fields/is_case_priced"
                },
                null,
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
              <HX.Table with="rate_change"
                data={[
                "currency",
                "premium/line_100pct/policy_term",
                "premium/beazley_line/policy_term",
                "premium/line_100pct/annualised",
                "premium/beazley_line/annualised",
                "limit",
                "excess",
                "brokerage",
                "rate"
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
                syncColumnWidthsKey="syncRateChange" />
              <HX.Table with="rate_change"
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
                syncColumnWidthsKey="syncRateChange"
                kb-interactive={true} />
              <HX.Collection fields={[
                "rate_change/rate_change_multiplier",
                null,
                null,
                null
              ]}
                horizontal={true} />
              <HX.Collection fields={[
                "rate_change/implied_renewable_rate",
                null,
                null,
                null
              ]}
                horizontal={true} />
              <HX.Collection fields={[
                "rate_change/implied_renewable_premium",
                null,
                null,
                null
              ]}
                horizontal={true} />
              <HX.Collection title="Final Rate Change"
                fields={[
                {
                  "field": "rate_change/rate_change/final",
                  "shownBy": "/cds/standard_fields/is_rater_priced"
                },
                {
                  "field": "rate_change/risk_adjusted_rate_change_case_priced",
                  "shownBy": "/cds/standard_fields/is_case_priced"
                },
                null,
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
              <HX.Table with="rate_change"
                data={[
                "currency",
                "premium/line_100pct/policy_term",
                "premium/beazley_line/policy_term",
                "premium/line_100pct/annualised",
                "premium/beazley_line/annualised",
                "limit",
                "excess",
                "brokerage",
                "rate"
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
                syncColumnWidthsKey="syncRateChange" />
              <HX.Table with="rate_change"
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
                syncColumnWidthsKey="syncRateChange"
                kb-interactive={true} />
              <HX.Collection fields={[
                "rate_change/rate_change_multiplier",
                null,
                null,
                null
              ]}
                horizontal={true} />
              <HX.Collection fields={[
                "rate_change/implied_renewable_rate",
                null,
                null,
                null
              ]}
                horizontal={true} />
              <HX.Collection fields={[
                "rate_change/implied_renewable_premium",
                null,
                null,
                null
              ]}
                horizontal={true} />
              <HX.Collection title="Final Rate Change"
                fields={[
                {
                  "field": "rate_change/rate_change/final",
                  "shownBy": "/cds/standard_fields/is_rater_priced"
                },
                {
                  "field": "rate_change/risk_adjusted_rate_change_case_priced",
                  "shownBy": "/cds/standard_fields/is_case_priced"
                },
                null,
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
        viewScale={0.8}
        shownBy="model_state/show_after_landing_page">
        <HX.Section title="Underwriter Rationale">
          <HX.Notes field="cds/standard_fields/uw_rationale" />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Standard KPIs"
        viewScale={0.8}
        shownBy="model_state/show_after_landing_page">
        <HX.Section title="Summary Layer 1">
          <HX.With context={{
            "index": 0,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "status.read_only",
              "section_reference.read_only",
              "brokerage.read_only",
              "written_line.read_only"
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              "quoted_premium_100",
              null,
              "technical_premium_100",
              "benchmark_premium_100",
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
                "field": "rate_change/rate_change/final",
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
        <HX.Section title="Summary Layer 2">
          <HX.With context={{
            "index": 1,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "status.read_only",
              "section_reference.read_only",
              "brokerage.read_only",
              "written_line.read_only"
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              "quoted_premium_100",
              null,
              "technical_premium_100",
              "benchmark_premium_100",
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
                "field": "rate_change/rate_change/final",
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
        <HX.Section title="Summary Layer 3">
          <HX.With context={{
            "index": 2,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "status.read_only",
              "section_reference.read_only",
              "brokerage.read_only",
              "written_line.read_only"
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              "quoted_premium_100",
              null,
              "technical_premium_100",
              "benchmark_premium_100",
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
                "field": "rate_change/rate_change/final",
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
        <HX.Section title="Summary Layer 4">
          <HX.With context={{
            "index": 3,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "status.read_only",
              "section_reference.read_only",
              "brokerage.read_only",
              "written_line.read_only"
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              "quoted_premium_100",
              null,
              "technical_premium_100",
              "benchmark_premium_100",
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
                "field": "rate_change/rate_change/final",
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
        <HX.Section title="Summary Layer 5">
          <HX.With context={{
            "index": 4,
            "path": "cds/layers",
            "type": "list"
          }}>
            <HX.Collection title="Risk Details"
              numCols={4}
              fields={[
              "status.read_only",
              "section_reference.read_only",
              "brokerage.read_only",
              "written_line.read_only"
            ]} />
            <HX.Collection title="Pricing"
              numCols={2}
              fields={[
              "quoted_premium_100",
              null,
              "technical_premium_100",
              "benchmark_premium_100",
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
                "field": "rate_change/rate_change/final",
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
      <HX.Page title="JSON View"
        shownBy="schema_view/show_view">
        <HX.Section>
          <CustomComponent title="Schema Viewer"
            stringifiedJsonPath="schema_view/stringified_json"
            shownBy="schema_view/show_view" />
        </HX.Section>
      </HX.Page>
      <HX.Page title="Timer"
        shownBy="model_profiling/show">
        <HX.Section title="Function Tree">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "selected_segment",
              "timer_threshold"
            ]}
              horizontal={true}
              with="model_profiling" />
            <HX.Pane ratio={1} />
          </HX.Pane>
          <HX.Notes field="function_tree"
            title="Function Call Tree"
            with="model_profiling" />
        </HX.Section>
        <HX.Section title="Timed Segments">
          <HX.Pane flow="right">
            <HX.Collection fields={[
              "selected_segment",
              "timer_threshold"
            ]}
              horizontal={true}
              with="model_profiling" />
            <HX.Pane ratio={1} />
          </HX.Pane>
          <HX.Table data={[
            "timed_segments"
          ]}
            fields={[
            "name",
            "time_taken",
            "start_time",
            "end_time"
          ]}
            filter="show"
            with="model_profiling"
            kb-interactive={true} />
        </HX.Section>
        <HX.Section title="Gantt View">
          <CustomComponent title="Profiling"
            listSegments="model_profiling/timed_segments"
            myListFields={[
            "name",
            "start_time",
            "time_taken",
            "end_time",
            "show"
          ]} />
        </HX.Section>
      </HX.Page>
    </HX.Root>
  );
}

export default {
  hx_calculation_legacy_initial_premium: hx_calculation_legacy_initial_premium_view,
};