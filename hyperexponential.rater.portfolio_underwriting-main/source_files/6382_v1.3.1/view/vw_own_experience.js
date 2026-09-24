import * as HX from "hx-model-components";
import LineBar from "components/combined_bar_line";
// import Bar from "components/bar";

function vw_own_experience(scale) {


  const generateAttrLargeCatTotalNestedFields = (prefix, path = '', is_shown_conditional = false) => {
    if (is_shown_conditional) {
      return [
        generate_shown_by_obj(`${prefix}_attr`, path),
        generate_shown_by_obj(`${prefix}_large`, path),
        generate_shown_by_obj(`${prefix}_cat`, path),
        `${prefix}_total`
        // generate_shown_by_obj(`${prefix}_total`, path)  - JB commented out as we always want totals to show
      ]
    }
    else {
      return [`${prefix}_attr`, `${prefix}_large`, `${prefix}_cat`, `${prefix}_total`];
    }
  }


  const generate_shown_by_obj = (field, path) => {
    return { "field": field, "shownBy": path }

  }



  const generateSelectedLobFields = (index, not_compact) => [
    // in various places below we use the spread operator to assign additional items to the array depending on whether not_compact is true or false
    //     THE TEST      [WHEN TRUE           ] : [WHEN FALSE])
    // ...(not_compact ? [ /* extra fields */ ] : [          ])

    'latest_gpi',
    'latest_gnpi',
    'acquisition_costs',


    ...(not_compact ? [...generateAttrLargeCatTotalNestedFields('latest_incurred_open_claims', `/cds/projections_own_experience/selected_lob_totals_${index}/show_alc`, true),] : []),
    ...(not_compact ? [...generateAttrLargeCatTotalNestedFields('latest_incurred_closed_claims', `/cds/projections_own_experience/selected_lob_totals_${index}/show_alc`, true),] : []),
    ...generateAttrLargeCatTotalNestedFields('latest_incurred_total_claims', `/cds/projections_own_experience/selected_lob_totals_${index}/show_alc`, true),
    ...(not_compact ? [...generateAttrLargeCatTotalNestedFields('last_year_position', `/cds/projections_own_experience/selected_lob_totals_${index}/show_alc`, true),] : []),
    ...generateAttrLargeCatTotalNestedFields('movement', `/cds/projections_own_experience/selected_lob_totals_${index}/show_alc`, true),
    ...generateAttrLargeCatTotalNestedFields('gn_ilr', `/cds/projections_own_experience/selected_lob_totals_${index}/show_alc`, true),

    null,

    { field: 'applied_rate_change.read_only_option', shownBy: "/non_cds/risk_information/is_underwriter" },
    { field: 'applied_inflation.read_only_option', shownBy: "/non_cds/risk_information/is_underwriter" },
    { field: "applied_rate_change", shownBy: "/non_cds/risk_information/is_actuarial" },
    { field: "applied_inflation", shownBy: "/non_cds/risk_information/is_actuarial" },

    ...(not_compact ? [
      'applied_rate_change_cumulative',
      'applied_inflation_cumulative',
      'onlevel_factor_cumulative',
    ] : []),

    null,

    ...(not_compact ? [
      { field: 'development_pattern_premium_lloyds_unadjusted', shownBy: "/cds/risk_information/show_refs" },
      { field: 'development_pattern_paid_lloyds_unadjusted', shownBy: "/cds/risk_information/show_refs" },
      { field: 'development_pattern_incurred_lloyds_unadjusted', shownBy: "/cds/risk_information/show_refs" },
      'development_pattern_premium_lloyds',
      'development_pattern_incurred_lloyds',
      { field: 'development_pattern_premium_override.read_only_option', shownBy: "/non_cds/risk_information/is_underwriter" },
      { field: 'development_pattern_incurred_override.read_only_option', shownBy: "/non_cds/risk_information/is_underwriter" },
      { field: "development_pattern_premium_override", shownBy: "/non_cds/risk_information/is_actuarial" },
      { field: "development_pattern_incurred_override", shownBy: "/non_cds/risk_information/is_actuarial" },
    ] : []),

    'development_pattern_premium_selected',
    'development_pattern_incurred_selected',

    null,

    ...(not_compact ? ['ultimate_premium_selected_gnpi_cl',] : []),
    'ultimate_premium_selected_gnpi_override',
    'ultimate_premium_selected_gnpi_selected',
    'ultimate_premium_selected_gnpi_selected_ol',

    ...(not_compact ? [
      ...generateAttrLargeCatTotalNestedFields('ultimate_incurred_cl', `/cds/projections_own_experience/selected_lob_totals_${index}/show_alc`, true),
      'ultimate_incurred_cl_ielr',
      ...generateAttrLargeCatTotalNestedFields('ultimate_incurred_ielr', `/cds/projections_own_experience/selected_lob_totals_${index}/show_alc`, true),
      ...generateAttrLargeCatTotalNestedFields('ultimate_incurred_bf', `/cds/projections_own_experience/selected_lob_totals_${index}/show_alc`, true),
      ...generateAttrLargeCatTotalNestedFields('ielr_weighting_cl', `/cds/projections_own_experience/selected_lob_totals_${index}/show_alc`, true),
      'method_incurred',
      ...generateAttrLargeCatTotalNestedFields('additional_ibnr'),
      ...generateAttrLargeCatTotalNestedFields('ultimate_incurred_selected', `/cds/projections_own_experience/selected_lob_totals_${index}/show_alc`, true),
      { field: 'ultimate_incurred_selected_total_x_cat', shownBy: `/cds/projections_own_experience/selected_lob_totals_${index}/show_alc` },
    ] : []),


    ...generateAttrLargeCatTotalNestedFields('ultimate_ulr_selected', `/cds/projections_own_experience/selected_lob_totals_${index}/show_alc`, true),
    { field: 'ultimate_ulr_selected_total_x_cat', shownBy: `/cds/projections_own_experience/selected_lob_totals_${index}/show_alc` },
    null,
    ...generateAttrLargeCatTotalNestedFields('ultimate_ulr_on_levelled', `/cds/projections_own_experience/selected_lob_totals_${index}/show_alc`, true),
    { field: 'ultimate_ulr_on_levelled_total_x_cat', shownBy: `/cds/projections_own_experience/selected_lob_totals_${index}/show_alc` },
    null,
    'modelled_weighting',
    ...generateAttrLargeCatTotalNestedFields('ielr_weighting_sel', `/cds/projections_own_experience/selected_lob_totals_${index}/show_alc`, true),


    ...(not_compact ? [
      null,
      'exposure_weighting_onlevel_1',
      'decay_ratio_weighting_2',
      'developed_weighting_3',
      'overall_weighting_onlevel',
      null,
      'exposure_weighting_nominal_1',
      'overall_weighting_nominal',

      { field: null, shownBy: "/cds/risk_information/show_refs" },
      { field: 'adjustments_actual', shownBy: "/cds/risk_information/show_refs" },
      { field: 'adjustments_lower', shownBy: "/cds/risk_information/show_refs" },
      { field: 'adjustments_upper', shownBy: "/cds/risk_information/show_refs" },
      { field: 'adjustments_prem_lloyds_lower', shownBy: "/cds/risk_information/show_refs" },
      { field: 'adjustments_prem_lloyds_upper', shownBy: "/cds/risk_information/show_refs" },
      { field: 'adjustments_prem_lloyds_actual', shownBy: "/cds/risk_information/show_refs" },
      { field: 'adjustments_incurred_lloyds_lower', shownBy: "/cds/risk_information/show_refs" },
      { field: 'adjustments_incurred_lloyds_upper', shownBy: "/cds/risk_information/show_refs" },
      { field: 'adjustments_incurred_lloyds_actual', shownBy: "/cds/risk_information/show_refs" },
    ] : []),
  ]









  const generateSelectedLob = (index) => {
    return (
      <HX.Section title={`Selected LoB - ${index}`} defaultCollapsed={true} >
        <HX.With context={{ type: "struct", path: `cds/projections_own_experience` }}>

          <HX.Collection
            title={"Visual Settings"}
            fields={[`selected_lob_${index}`, 'show_all_yrs', 'show_detail', null]}
            horizontal
          />  {/* notice we use ` not ' for js to recognise as JS template literal */}

          <HX.Pane flow="right" >

            <HX.Table
              title={"LOB Settings"}
              data={[{ datum: "summary_table", maxWidth: 200 }]}
              fields={[
                'selected_lob', 'claim_source', 'claim_basis', 'claim_to_develop_to_ultimate', 'cat_basis',
                { field: "ielr_approach", shownBy: "/non_cds/risk_information/is_actuarial" },
                { field: "ielr_approach.read_only_option", shownBy: "/non_cds/risk_information/is_underwriter" },]}
              filter={`lob_visible_${index}`}
              kb-interactive
              transpose
            />

            <HX.Table
              title={"Selected IELRs"}
              data={[{ datum: "summary_table", maxWidth: 100 }]}
              fields={[
                { field: "ielr_attr", shownBy: `/cds/projections_own_experience/selected_lob_totals_${index}/show_alc` },
                { field: "ielr_large", shownBy: `/cds/projections_own_experience/selected_lob_totals_${index}/show_alc` },
                { field: "ielr_cat", shownBy: `/cds/projections_own_experience/selected_lob_totals_${index}/show_alc` },
                'ielr_total', 'ielr_total_excl_cat', 'lloyds_selected_ielr']}
              filter={`lob_visible_${index}`}
              kb-interactive
              transpose
            />

            <HX.With context={{ type: "struct", path: `selected_lob_totals_${index}` }}>
              <HX.Table
                with={"ielr_approaches"}
                title={"Model Default - IELR Approach Analysis"}
                data={[
                  { datum: "nominal", maxWidth: 100 },
                  { datum: "ol_all_yr", maxWidth: 100 },
                  { datum: "ol_cl_yr", maxWidth: 100 }
                ]}
                fields={['ielr_attr', 'ielr_large', 'ielr_cat', 'ielr_total', 'ielr_total_excl_cat']}
                kb-interactive
                transpose
                shownBy="/non_cds/risk_information/is_actuarial"
              />
            </HX.With>

          </HX.Pane>

          {/* compact view */}
          <HX.Table
            title="Analysis Detail"
            data={[
              { datum: "detail_table", elementLabelBy: "yoa" }
              , null
              , { datum: `selected_lob_totals_${index}`, elementLabelBy: "yoa" }]}
            fields={generateSelectedLobFields(index, false)}        // observe this value change true/false
            // maxListVisibleRows={8}
            freezeLeft={0}
            filter={`lob_visible_${index}`}
            kb-interactive
            transpose={false}
            shownBy="/cds/projections_own_experience/show_compact"
          />

          {/* detail view */}
          <HX.Table
            title="Analysis Detail"
            data={[
              { datum: "detail_table", elementLabelBy: "yoa" }
              , null
              , { datum: `selected_lob_totals_${index}`, elementLabelBy: "yoa" }]}
            fields={generateSelectedLobFields(index, true)}        // observe this value change true/false
            // maxListVisibleRows={8}
            freezeLeft={0}
            filter={`lob_visible_${index}`}
            kb-interactive
            transpose={false}
            shownBy="/cds/projections_own_experience/show_detail"
          />


          <HX.Pane flow="right">


            <HX.Pane flow="right">
              <HX.With context={{ type: "struct", path: `selected_lob_totals_${index}` }}>
                <LineBar
                  title={`Selected Lob - ${index}`}
                  titleBy={"selected_lob"}
                  // select data to pass in prop below
                  data={[{ list: "chart_data", labelBy: "yoa", }]}
                  // select data to render as bars in prop below
                  traces={[
                    { field: "gn_ilr_total", label: "Total GN ILR %", color: "#DC199B" },
                    { field: "ultimate_ulr_selected_total", label: "Total GN ULR %", color: "#4B0050" },
                    { field: "ultimate_ulr_on_levelled_total", label: "On-levelled Total GN ULR %", color: "#C8C3CD" }
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


            <HX.Pane flow="right">
              <HX.Table
                title="Model Default Loss Ratios"
                data={[{ datum: "summary_table", maxWidth: 150 }]}
                fields={[
                  'model_default_attr', 'model_default_large', 'model_default_cat_exp',
                  'model_default_cat_bp', 'model_default_cat_rms', 'model_default_cat_basis', 'model_default_cat',
                  null, 'model_default_total', 'model_default_total_excl_cat']}
                filter={`lob_visible_${index}`}
                kb-interactive
                transpose
              />

              <HX.Table
                title="Selected Loss Ratios"
                data={[{ datum: "summary_table", maxWidth: 150 }]}
                fields={[
                  'selected_attr', 'selected_large',
                  'selected_cat_exp', 'selected_cat_bp', 'selected_cat_rms', 'selected_cat_basis', 'selected_cat',
                  null, 'selected_total', 'selected_total_excl_cat']}
                filter={`lob_visible_${index}`}
                kb-interactive
                transpose
              />

              <HX.With context={{ type: "list", path: `summary_table`, indexBy: `/cds/projections_own_experience/selected_lob_totals_${index}/row` }}>
                <HX.Notes
                  field={'actuarial_notes'}
                  title="Please note any rationale for selection below, and any use of overrides:"
                />
              </HX.With>
            </HX.Pane>
          </HX.Pane>



        </HX.With>
      </HX.Section >
    )
  }



  return (
    <HX.Page title="Own Experience" fullWidth={true} viewScale={0.8} shownBy="model_state/show_own_experience">
      <HX.Section title="Own Experience Summary">
        <HX.Notes field={"cds/projections_own_experience/error_msg"} shownBy="non_cds/own_experience/is_error_msg_shown" />
        <HX.Table
          title="Own Experience Summary"
          data={["cds/projections_own_experience/summary_table"]}
          fields={[
            'selected_lob',
            'claim_source',
            'claim_basis',
            'claim_to_develop_to_ultimate',
            'cat_basis',
            { field: "ielr_approach", shownBy: "/non_cds/risk_information/is_actuarial" },
            { field: "ielr_approach.read_only_option", shownBy: "/non_cds/risk_information/is_underwriter" },
            null,
            'selected_attr',
            'selected_large',
            'selected_cat',
            'selected_total',
            'selected_total_excl_cat',
            null,
            'model_default_attr',
            'model_default_large',
            'model_default_cat',
            'model_default_total',
            'model_default_total_excl_cat',
            null,

            "ovd_dev",
            "ovd_index",
            "ovd_premium",
            "ovd_ielr_weights",
            "ovd_ielr",
            "ovd_ibnr",
            "ovd_ultimate_method",
            "ovd_ultimate",
            "ovd_ulr_weights",
            "ovd_ulr",

            // YZ request 13 Mar 26 to show for all users
            // { field: "ovd_dev", shownBy: "/non_cds/risk_information/is_actuarial" },
            // { field: "ovd_index", shownBy: "/non_cds/risk_information/is_actuarial" },
            // { field: "ovd_premium", shownBy: "/non_cds/risk_information/is_actuarial" },
            // { field: "ovd_ielr_weights", shownBy: "/non_cds/risk_information/is_actuarial" },
            // { field: "ovd_ielr", shownBy: "/non_cds/risk_information/is_actuarial" },
            // { field: "ovd_ibnr", shownBy: "/non_cds/risk_information/is_actuarial" },
            // { field: "ovd_ultimate_method", shownBy: "/non_cds/risk_information/is_actuarial" },
            // { field: "ovd_ultimate", shownBy: "/non_cds/risk_information/is_actuarial" },
            // { field: "ovd_ulr_weights", shownBy: "/non_cds/risk_information/is_actuarial" },
            // { field: "ovd_ulr", shownBy: "/non_cds/risk_information/is_actuarial" },

          ]}
          filter={'is_row_visible'}
          kb-interactive

        />
        {/* <HX.Table
          title="Own Experience Correlation Working"
          data={["cds/own_experience/correlation_working"]}
          fields={generateCorrelationFields()}
          kb-interactive
        /> */}
      </HX.Section>
      {generateSelectedLob(1)}
      {generateSelectedLob(2)}
      {generateSelectedLob(3)}
      {generateSelectedLob(4)}
      {generateSelectedLob(5)}

    </HX.Page>
  )
}

export { vw_own_experience };