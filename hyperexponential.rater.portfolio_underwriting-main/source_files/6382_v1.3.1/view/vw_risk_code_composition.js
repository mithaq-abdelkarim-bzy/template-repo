import * as HX from "hx-model-components";
import { YEARS_TO_CONSIDER_IN_RISK_CODE_COMPOSITION } from './vw_constants'

const getYearsHeaders = (start = 0, prefix = '') => {
  return Array.from({ length: YEARS_TO_CONSIDER_IN_RISK_CODE_COMPOSITION }, (_, i) => ({
    field: `year_${start + i}`,
    labelBy: `non_cds/risk_code_composition/${prefix}year_${start + i}`
  }));
};

function vw_risk_code_composition(scale) {
  return (
    <HX.Page title="Risk Code Composition" fullWidth={true} viewScale={scale} shownBy="model_state/show_risk_code_comp">
      <HX.Section title="Risk Code Composition" collapsible={false}>
        <HX.Pane shownBy="non_cds/global_fields/mismatched_lob_table_length" flow="right">
          <HX.Collection fields={["non_cds/global_fields/mismatched_lob_error_msg.warning"]} />
          <HX.Button task="sync_lob_lists_task" title="Sync LOB Lists" />
        </HX.Pane>
        <HX.Pane>
          <HX.Collection fields={[
            "cds/risk_code_composition/model_type", null, null, null, null, null, null, null, null,
            "cds/risk_code_composition/data_driven_composition/year_start",
            "cds/risk_code_composition/data_driven_composition/year_end",
            null, "cds/risk_code_composition/data_driven_composition/premium_basis", null, null]}
            syncColumnWidthsKey="input_1"
            shownBy="cds/risk_information/prem_data_available"
            horizontal={true} />
        </HX.Pane>
        <HX.Pane>
          <HX.Pane>
            <HX.Table
              title="Premium summary by Risk Code and YOA from Policy Level Data"
              data={["cds/risk_code_composition/data_driven_composition/premiums_table", null, "cds/risk_code_composition/data_driven_composition/summary"]}
              fields={[
                "risk_code",
                ...getYearsHeaders().reverse(),
                null,
                "selected_premium",
                "exist_in_lloyds_data_bool",
                "composition"
              ]}
              syncColumnWidthsKey="input_1"
              shownBy="cds/risk_information/prem_data_available"
              maxListVisibleRows={20}
              kb-interactive
              dynamic
            />
          </HX.Pane>
        </HX.Pane>
        <HX.Pane>
          <HX.Pane>
            <HX.Collection fields={["cds/risk_code_composition/data_driven_composition/composition_selection/modelled", null, null, null, null, null, null]}
              shownBy="cds/risk_information/prem_data_available"
              horizontal />
            <HX.Table title="Risk Code Composition Derived from Data"
              data={["cds/risk_code_composition/data_driven_composition/composition_selection/table"]}
              fields={[
                "cs_risk_code",
                "cs_composition",
                "exists_in_data_bool",
                "model",
                "composition_reweighted",
                "cs_facility_line_of_business",
                "selected_lob",
                "selected_bp_class",
                "tracker_class",
                "risk_code_description",
              ]}
              syncColumnWidthsKey="table_1"
              shownBy="cds/risk_information/prem_data_available"
              maxListVisibleRows={20}
              kb-interactive
              dynamic
              filter={"is_row_visible"}
            />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Pane>
              <HX.Button
                task="copy_composition_selection_table"
                title="Copy Risk Code Composition"
                shownBy="non_cds/risk_code_composition/is_manual_and_prem_data_available_true"
              />
              <HX.Button
                task="clear_manual_risk_code_composition_table"
                title="Clear Table"
                shownBy="non_cds/risk_code_composition/is_manual"
              />
            </HX.Pane>
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
          <HX.Pane>
            <HX.Collection fields={["cds/risk_code_composition/composition_manual/modelled", null, null, null, null, null]}
              horizontal
              shownBy="non_cds/risk_code_composition/is_manual"
            />
            <HX.Table title="Risk Code Composition Manually Entered"
              data={["cds/risk_code_composition/composition_manual/table"]}
              fields={[
                "cs_risk_code",
                "cs_composition",
                "exists_in_data_bool",
                "model",
                "composition_reweighted",
                "cs_facility_line_of_business",
                "selected_lob",
                "selected_bp_class",
                "tracker_class",
                "risk_code_description",
              ]}
              syncColumnWidthsKey="table_1"
              maxListVisibleRows={20}
              kb-interactive
              dynamic
              shownBy="non_cds/risk_code_composition/is_manual"
            />
          </HX.Pane>
        </HX.Pane>
      </HX.Section>
    </HX.Page >
  )
}

export { vw_risk_code_composition };