import * as HX from "hx-model-components";
import LineBar from "components/combined_bar_line";
// import Bar from "components/bar";

function vw_beazley_projections(scale) {


  const generateSelectedLobSection = (index) => {
    return (
      <HX.Section title={`Selected LoB - ${index}`} defaultCollapsed={true} >
        <HX.With context={{ type: "struct", path: `cds/projections_beazley` }}>

          <HX.Collection
            title={"Visual Settings"}
            fields={[`lookup_lob_${index}`, 'show_all_yrs', null, null]}
            horizontal
          />  {/* notice we use ` not ' for js to recognise as JS template literal */}

          <HX.Pane flow="right">

            <HX.Table
              title={"LOB Settings"}
              data={[{ datum: "summary_table", maxWidth: 200 }]}
              fields={['selected_lob', 'risk_code',
                'bp_class', 'tracker_class', 'projection_type', 'ielr_approach', 'composition']}
              filter={`lob_visible_${index}`}
              kb-interactive
              transpose
            />

            <HX.Table
              title={"Summary IELRs"}
              data={[{ datum: "summary_table", maxWidth: 200 }]}
              fields={['model_ielr_nominal', 'model_ielr_onlevel', 'model_ielr_ol_allyr',
                null, 'lloyds_ielr', 'ielr_source', null, 'model_ielr', 'selected_ielr']}
              filter={`lob_visible_${index}`}
              kb-interactive
              transpose
            />

            <HX.Table
              title="Model Default Loss Ratios"
              data={[{ datum: "summary_table", maxWidth: 200 }]}
              fields={[
                'model_gn_ulr', 'model_base_aqn', 'model_acc_aqn',
                'model_adj_gn_ulr', null, 'bp_cat_load', 'model_final_gn_ulr']}
              filter={`lob_visible_${index}`}
              kb-interactive
              transpose
            />

            <HX.Table
              title="Selected Loss Ratios"
              data={[{ datum: "summary_table", maxWidth: 200 }]}
              fields={[
                'selected_gn_ulr', 'selected_base_aqn', 'selected_acc_aqn',
                'selected_adj_gn_ulr', null, 'bp_cat_load', 'selected_final_gn_ulr']}
              filter={`lob_visible_${index}`}
              kb-interactive
              transpose
            />

          </HX.Pane>

          <HX.Table
            title="Analysis Detail"
            data={[
              { datum: "detail_table", elementLabelBy: "yoa" }
              , null
              , { datum: `selected_lob_totals_${index}`, elementLabelBy: "yoa" }]}
            fields={generateCommonFields(index)}
            maxListVisibleRows={8}
            filter={`lob_visible_${index}`}
            kb-interactive
            transpose={false}
            freezeLeft={0}

          />


          <HX.Pane flow="right">
            <HX.Pane>
              <HX.With context={{ type: "struct", path: `selected_lob_totals_${index}` }}>
                <LineBar
                  title={`Selected Lob - ${index}`}
                  titleBy={"lookup_lob"}
                  // select data to pass in prop below
                  data={[{ list: "chart_data", labelBy: "yoa", }]}
                  // select data to render as bars in prop below
                  traces={[
                    { field: "incurred_loss_ratio", label: "Total GN ILR %", color: "#DC199B" },
                    { field: "ultimate_selected_ulr", label: "Total GN ULR %", color: "#4B0050" },
                    { field: "on_levelled_selected_ulr", label: "On-levelled Total GN ULR %", color: "#C8C3CD" }
                  ]}
                  // select data to render as lines in prop below
                  series={[{
                    seriesLabel: "Pricing Basis %",
                    seriesColor: "#4FADC7",
                    seriesLineType: 'dash',
                    seriesMode: 'lines',
                    // edit below specifically
                    points: [{ list: "chart_data", x: "yoa", y: "pricing_basis", },],
                  },]}
                  xAxisTickAngle={-45}
                  xAxisLabel="Year of Account"
                  yAxisLabel="Total GNLR (%)"
                  barMode="group"
                  gapBetweenBarsSize={0.3}
                  width={800}
                  height={500}
                  y2SeparateAxis={false}
                />
              </HX.With>
            </HX.Pane>




            <HX.With context={{ type: "list", path: `summary_table`, indexBy: `/cds/projections_beazley/selected_lob_totals_${index}/row` }}>
              <HX.Notes
                field={'actuarial_notes'}
                title="Please note any rationale for selection below, and any use of overrides:"
              />
            </HX.With>

          </HX.Pane>



        </HX.With>
      </HX.Section >
    )
  }

  const generateCommonFields = (index) => [
    // 'yoa',
    'latest_gpi',
    'latest_gnpi',
    'acquisition_ratio',
    'latest_paid',
    'latest_incurred',
    'incurred_loss_ratio',

    'dev_patterns_gnpi',
    'dev_patterns_paid',
    'dev_patterns_incurred',

    'inflation_model',
    'rate_change_model',
    'rate_change_selected',

    'ultimate_gnpi',
    'ultimate_gnpi_ol_model',
    'ultimate_gnpi_ol_selected',

    'ultimate_cl_paid',
    'ultimate_cl_paid_ulr',
    'ultimate_cl_incurred',
    'ultimate_cl_incurred_ulr',

    'ultimate_ielr_model',
    'ultimate_ielr_model_ulr',
    'ultimate_ielr_selected',
    'ultimate_ielr_selected_ulr',

    'ultimate_bf_model_paid',
    'ultimate_bf_model_incurred',
    'ultimate_bf_selected_paid',
    'ultimate_bf_selected_incurred',

    'weighting_ielr',
    'method_paid',
    'method_incurred',


    'ultimate_model',
    'ultimate_model_ulr',
    'ultimate_selected',
    'ultimate_selected_ulr',

    'on_levelled_model_ulr',
    'on_levelled_selected_ulr',

    'weighting_model',
    'weighting_selected',

    null,
    'weighting_1_exposure_onlevel',
    'weighting_2_decay_ratio',
    'weighting_3_developed',
    'weighting_onlevel',
    null,
    'weighting_1_exposure_nominal',
    'weighting_nominal',
    null,
    'inflation_model_index',
    'rate_change_model_index',
    'rate_change_selected_index',
    'loss_ratio_model_index',
    'loss_ratio_selected_index'

  ]

  return (
    <HX.Page title="Beazley Projections"
      fullWidth={true}
      viewScale={0.8}
      shownBy="model_state/show_beazley_proj">
      <HX.Section title="Beazley Projection Summary">
        {/* JB: TODO check this NOTES FIELD*/}
        <HX.Notes field={"cds/projections_own_experience/error_msg"} shownBy="non_cds/own_experience/is_error_msg_shown" />

        <HX.Table
          title="Beazley Projection Summary"
          data={["cds/projections_beazley/summary_table"]}
          fields={[
            'risk_code',
            'selected_lob',
            'bp_class',
            'tracker_class',
            'composition',
            'model_acc_aqn',
            'projection_type',
            'cat_lr_source',
            'ielr_source',
            'ielr_approach',
            'selected_final_gn_ulr',
            'bp_cat',
            'bp_cat_load',
            'selected_ielr',
            'model_final_gn_ulr',
            'model_ielr',
            'checked',
            'comments'
          ]}
          maxListVisibleRows={10}
          filter={'is_row_visible'}
          kb-interactive
          freezeLeft={1}
        />
        {/* <HX.Table
          title="Own Experience Correlation Working"
          data={["cds/own_experience/correlation_working"]}
          fields={generateCorrelationFields()}
          kb-interactive
        /> */}
      </HX.Section>
      {generateSelectedLobSection(1)}
      {generateSelectedLobSection(2)}
      {generateSelectedLobSection(3)}

    </HX.Page>
  )
}

export { vw_beazley_projections };