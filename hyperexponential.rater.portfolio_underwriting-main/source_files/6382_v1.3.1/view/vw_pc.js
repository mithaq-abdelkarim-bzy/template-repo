import * as HX from 'hx-model-components';
import { MAX_NUM_LOB } from 'view/vw_constants';
import Matrix from "components/matrixWorking";

const generateForSlidingScaleFields = () => {
  return Array.from({ length: MAX_NUM_LOB }, (_, idx) => {
    const i = idx + 1;
    const shownByPath = `non_cds/pc/pc_structure/for_sliding_scale/is_selected_lob_${i}_shown`;
    return [
      { field: `selected_lob_${i}/gn_ulr_less_than`, width: 200, shownBy: shownByPath },
      { field: `selected_lob_${i}/pc`, width: 100, shownBy: shownByPath },
    ];
  }).flat();
}

const generateDataForCorrelationMatrix = (parent) => {
  return Array.from({ length: MAX_NUM_LOB }, (_, idx) => ({
    datum: `cds/pc/correlation_matrix/${parent}/selected_lob_${idx + 1}`,
    elementLabelBy: 'selected_lob'
  }));
};

const generateFieldsForCorrelationMatrix = () => {
  return Array.from({ length: MAX_NUM_LOB }, (_, idx) => ({
    field: `selected_lob_${idx + 1}`,
    width: 200,
    shownBy: `non_cds/pc/correlation_matrix/is_selected_lob_${idx + 1}_shown`,
    labelBy: `non_cds/pc/correlation_matrix/selected_lob_${idx + 1}_label`
  }));
};


function vw_pc(scale) {
  return (
    <HX.Page title='PC' fullWidth={true} viewScale={scale} shownBy="model_state/show_pc">
      <HX.Section title='PC Control' collapsible={false}>
        <HX.Pane flow='right'>
          <HX.Pane>
            <HX.Button title="Calculate Profit commission" task="calculate_profit_commission_task" />
          </HX.Pane>
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>
        <HX.Collection
          with='cds/pc/pc_control'
          numCols={6}
          fields={[
            "is_pc_interlocking",
            "allow_for_correlation",
            "show_details",
            null,
            null,
            null,

            "dcf_opt",
            { field: "dcf_amount", shownBy: "/non_cds/pc/pc_control/is_amount" },
            { field: "dcf_amount_basis", shownBy: "/non_cds/pc/pc_control/is_amount" },
            { field: null, shownBy: "/non_cds/pc/pc_control/is_amount" },
            { field: null, shownBy: "/non_cds/pc/pc_control/is_amount" },
            { field: null, shownBy: "/non_cds/pc/pc_control/is_amount" },

            { field: null, shownBy: "/non_cds/pc/pc_control/is_none" },
            { field: null, shownBy: "/non_cds/pc/pc_control/is_none" },
            { field: null, shownBy: "/non_cds/pc/pc_control/is_none" },
            { field: null, shownBy: "/non_cds/pc/pc_control/is_none" },
            { field: null, shownBy: "/non_cds/pc/pc_control/is_none" },

            { field: "dcf_exper_num_yrs", shownBy: "/non_cds/pc/pc_control/is_experience" },
            { field: "dcf_exper_exc_yrs", shownBy: "/non_cds/pc/pc_control/is_experience" },
            { field: "dcf_exper_basis", shownBy: "/non_cds/pc/pc_control/is_experience" },
            { field: null, shownBy: "/non_cds/pc/pc_control/is_experience" },
            { field: null, shownBy: "/non_cds/pc/pc_control/is_experience" },

            "ul_binders_pc",
            { field: "ul_pc_as_expense", shownBy: "/non_cds/pc/pc_control/is_pc_on_binders" },
            { field: "ul_pc_as_expense_pct", shownBy: "/non_cds/pc/pc_control/is_pc_on_binders" },
            { field: null, shownBy: "/non_cds/pc/pc_control/is_pc_on_binders" },
            { field: null, shownBy: "/non_cds/pc/pc_control/is_pc_on_binders" },
            { field: null, shownBy: "/non_cds/pc/pc_control/is_pc_on_binders" },
            "no_of_simulations"

          ]} />
      </HX.Section>

      <HX.Section title='PC Structure'>
        <HX.Table
          // rowHeaderSettings={{ width: 200 }}
          syncColumnWidthsKey='table_1'
          transpose
          kb-interactive
          filter={"is_row_visible"}
          data={[{ datum: 'cds/pc/pc_structure/table', maxWidth: 300 }]}
          fields={[
            'selected_lob',
            'pc_type',
            'uw_expense',
            'expense_basis',
            'std_pc_percent'
          ]} />



        <HX.Selector
          with="cds/pc/pc_structure"
          title="Select the Line of Business to build a sliding scale for"
          data={["table_sliding_scale"]}
          dropdown="selected_lob"
        >
          <HX.Table
            // rowHeaderSettings={{ width: 200 }}
            syncColumnWidthsKey='table_1'
            kb-interactive
            // filter={"is_row_visible"}
            data={[{ datum: 'scale' }]}
            fields={['gn_ulr_less_than', 'pc']}
          />
        </HX.Selector>




        <HX.Table
          // rowHeaderSettings={{ width: 200 }}
          shownBy='non_cds/pc/pc_structure/show_for_sliding_scale'
          title='For Sliding Scale'
          kb-interactive
          data={['cds/pc/pc_structure/for_sliding_scale']}
          fields={generateForSlidingScaleFields()} />
      </HX.Section>

      <HX.Section title='Correlation Matrix' shownBy='cds/pc/pc_control/allow_for_correlation' defaultCollapsed={true}>
        <Matrix
          title="Calculated Correlation Matrix"
          parentList="cds/pc/cm_calc"
          parentListName="NotUsed"
          childList="cm_col"
          field="coeff"
        />
        {/* <Matrix
          parentList="cds/pc/cm_ovd"
          parentListName="NotUsed"
          childList="cm_col"
          field="coeff"
        /> */}
        <HX.Selector
          with="cds/pc"
          title="Select the Line of Business to add correlation for"
          data={["cm_ovd"]}
          dropdown="selected_lob"
        >
          <HX.Table
            kb-interactive
            data={[{ datum: 'cm_col', maxWidth: 150 }]}
            fields={['coeff']}
            transpose
          />
        </HX.Selector>

        <HX.Selector
          with="cds/pc"
          title="Select the Line of Business to check correlation for"
          data={["cm_sel"]}
          dropdown="selected_lob"
        >
          <HX.Table
            kb-interactive
            data={[{ datum: 'cm_col', maxWidth: 150 }]}
            fields={['coeff']}
            transpose
          />
        </HX.Selector>

        <Matrix
          parentList="cds/pc/cm_sel"
          title="Selected Correlation Matrix"
          parentListName="xxx"
          childList="cm_col"
          field="coeff"
        />

      </HX.Section>

      <HX.Section title='PC Calculations' shownBy='cds/pc/pc_control/show_details' defaultCollapsed={true}>
        <HX.Table
          syncColumnWidthsKey='table_1'
          shownBy='cds/pc/pc_control/show_details'
          transpose
          kb-interactive
          filter={"is_row_visible"}
          data={[{ datum: 'cds/pc/pc_calculations/details', maxWidth: 300 }, null, { datum: 'cds/pc/pc_calculations/summary', maxWidth: 300 }]}
          fields={[
            'selected_lob',
            null,
            'gwp_5623',
            'deductions',
            'nwp_5623',
            null,
            'bm_class_auto',
            'bm_class_override',
            'bm_class_applied',
            'cov_basis_attr',
            'cov_basis_large',
            'cov_basis_cat',
            'attr_gg_ulr',
            'large_gg_ulr',
            'cat_gg_ulr',
            'total_gg_ulr',
            null,
            'attr_cov',
            'large_cov',
            'cat_cov',
            null,
            'attr_el',
            'large_el',
            'cat_non_weather_el',
            'cat_weather_el',
            null,
            'attr_sd',
            'large_sd',
            'cat_non_weather_sd',
            'cat_weather_sd',
          ]} />
      </HX.Section>
      <HX.Section title='Profit Commission on Contract'>
        <HX.Table
          syncColumnWidthsKey='table_1'
          transpose
          kb-interactive
          filter={"is_row_visible"}
          data={[{ datum: 'cds/pc/profit_commission/details', maxWidth: 300 }, null, { datum: 'cds/pc/profit_commission/summary', maxWidth: 300 }]}
          fields={[
            "selected_lob",
            { field: 'gwp_5623', shownBy: 'cds/pc/pc_control/show_details' },
            { field: 'deductions', shownBy: 'cds/pc/pc_control/show_details' },
            { field: 'nwp_5623', shownBy: 'cds/pc/pc_control/show_details' },
            null,
            { field: 'total_losses', shownBy: 'cds/pc/pc_control/show_details' },
            { field: 'uw_expense', shownBy: 'cds/pc/pc_control/show_details' },
            { field: 'dcf', shownBy: 'cds/pc/pc_control/show_details' },
            { field: 'expected_pl', shownBy: 'cds/pc/pc_control/show_details' },
            { field: 'pc_on_binders', shownBy: 'cds/pc/pc_control/show_details' },
            { field: 'pc_on_contract', shownBy: 'cds/pc/pc_control/show_details' },
            { field: 'nwp_after_pc', shownBy: 'cds/pc/pc_control/show_details' },
            null,
            'total_gn_ulr_pre',
            'total_gn_ulr_post',
            'pc_impact'
          ]} />
      </HX.Section>
    </HX.Page>
  )
}

export { vw_pc };