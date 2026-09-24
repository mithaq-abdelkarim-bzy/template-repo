import * as HX from "hx-model-components";
import { YEARS_TO_CONSIDER_IN_RATE_CHANGE } from "view/vw_constants";

const generatePastYearViewFields = () => {
  const years = Array.from({ length: YEARS_TO_CONSIDER_IN_RATE_CHANGE - 1 }, (_, i) => `year_${i + 1}`);
  return years.flatMap(year => [null, `${year}/yoa`, { field: `${year}/facility`, labelBy: `non_cds/rate_change/${year}/facility` }, `${year}/beazley_group_achieved`, `${year}/selected`]);
};

function vw_rate_change(scale) {
  return (
    <HX.Page title="Rate Change" fullWidth={true} viewScale={scale} shownBy="model_state/show_rate_change">
      <HX.Section title="Rate Change - Tabular" collapsible={false}>
        <HX.Table
          kb-interactive
          data={["cds/rate_change", null, "cds/rate_change_summary"]}
          fields={[
            'selected_lob',
            'dominant_risk_code',
            'bp_class',
            null,
            'year_0/yoa',
            { field: 'year_0/facility', labelBy: `non_cds/rate_change/year_0/facility` },
            'year_0/bp_rate_change',
            { field: 'year_0/bp_rarc_margin', infoBy: `cds/rate_change_summary/year_0/bp_rarc_margin_info` },
            'year_0/source',
            'year_0/selected',
            ...generatePastYearViewFields()
          ]}
          filter={'is_row_visible'}
        />
      </HX.Section>


      <HX.Section title="Rate Change - Expiring" defaultCollapsed={true} shownBy="/cds/standard_fields/is_renewal">
        <HX.Button
          task="map_expiring_rate_change_task"
          title="Map Expiring Rate Change to Renewing"
        />
        <HX.Table
          kb-interactive
          data={["cds/expiring/rate_change"]}
          fields={[
            'selected_lob',
            null,
            'year_0/yoa',
            'year_0/facility',
            'year_0/source',

            null,
            'year_1/yoa',
            'year_1/facility',
            null,
            'year_2/yoa',
            'year_2/facility',
            null,
            'year_3/yoa',
            'year_3/facility',
            null,
            'year_4/yoa',
            'year_4/facility',
            null,
            'year_5/yoa',
            'year_5/facility',
            null,
            'year_6/yoa',
            'year_6/facility',
            null,
            'year_7/yoa',
            'year_7/facility',
            null,
            'year_8/yoa',
            'year_8/facility',
            null,
            'year_9/yoa',
            'year_9/facility',
            null,
            'year_10/yoa',
            'year_10/facility',
            null,
            'year_11/yoa',
            'year_11/facility',
            null,
            'year_12/yoa',
            'year_12/facility',
            null,
            'year_13/yoa',
            'year_13/facility',
            null,
            'year_14/yoa',
            'year_14/facility',
            null,
            'year_15/yoa',
            'year_15/facility',
          ]}
        />

      </HX.Section>


      <HX.Section title="Commentary" collapsible={false}>
        <HX.Notes field="cds/rationale/rate_change_notes" title="Please note any rationale for selection below, and any use of overrides:" />
      </HX.Section>
      <HX.Section title="Rate Change - Selector" defaultCollapsed={true}>
        <HX.Pane flow="right">
          <HX.Selector with="cds"
            title="Renewing"
            data={["rate_change"]}
            dropdown="selected_lob">
            <HX.Table kb-interactive={true}
              data={[
                { "datum": "year_0" },
                { "datum": "year_1" },
                { "datum": "year_2" },
                { "datum": "year_3" },
                { "datum": "year_4" },
                { "datum": "year_5" },
                { "datum": "year_6" },
                { "datum": "year_7" },
                { "datum": "year_8" },
                { "datum": "year_9" },
                { "datum": "year_10" },
                { "datum": "year_11" },
                { "datum": "year_12" },
                { "datum": "year_13" },
                { "datum": "year_14" },
                { "datum": "year_15" }
              ]}

              fields={[
                { "field": "yoa", "maxWidth": 100 },
                { "field": "facility", "maxWidth": 150 },
                { "field": "beazley_group_achieved", "maxWidth": 150 },
                { "field": "bp_rate_change", "maxWidth": 150 },
                { "field": "bp_rarc_margin", "maxWidth": 150 },
                { "field": "source", "maxWidth": 150 },
                { "field": "selected", "maxWidth": 150 }
              ]}
              transpose={false} />
          </HX.Selector>

          <HX.Selector
            with="cds/expiring"
            title="Expiring"
            data={["rate_change"]}
            dropdown="selected_lob"
            shownBy="/cds/standard_fields/is_renewal">
            <HX.Table kb-interactive={true}
              data={[
                { "datum": "year_0" },
                { "datum": "year_1" },
                { "datum": "year_2" },
                { "datum": "year_3" },
                { "datum": "year_4" },
                { "datum": "year_5" },
                { "datum": "year_6" },
                { "datum": "year_7" },
                { "datum": "year_8" },
                { "datum": "year_9" },
                { "datum": "year_10" },
                { "datum": "year_11" },
                { "datum": "year_12" },
                { "datum": "year_13" },
                { "datum": "year_14" },
                { "datum": "year_15" }
              ]}

              fields={[
                { "field": "yoa", "maxWidth": 100 },
                { "field": "facility", "maxWidth": 150 },
                { "field": "source", "maxWidth": 150 },
              ]}
              transpose={false} />
          </HX.Selector>
        </HX.Pane>

      </HX.Section>





    </HX.Page >
  )
}

export { vw_rate_change };