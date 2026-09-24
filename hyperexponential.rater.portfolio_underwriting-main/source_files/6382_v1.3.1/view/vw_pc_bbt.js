import * as HX from 'hx-model-components';
import { MAX_NUM_LOB } from 'view/vw_constants';


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


function vw_pc_bbt(scale) {
  return (
    <HX.Page title='PC' fullWidth={true} viewScale={scale} shownBy="non_cds/pc/show_pc_bbt">
      <HX.Section title='PC Control'>
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
          numCols={5}
          fields={[
            "dcf_opt_bbt",
            { field: "amount/amount", shownBy: "/non_cds/pc/pc_control/is_amount" },
            { field: "amount/basis", shownBy: "/non_cds/pc/pc_control/is_amount" },
            null,
            null,
            { field: null, shownBy: "/non_cds/pc/pc_control/is_none" },
            { field: null, shownBy: "/non_cds/pc/pc_control/is_none" }
          ]} />
        <HX.Collection
          with='cds/pc/pc_control'
          numCols={5}
          fields={["show_details", "no_of_simulations", null, null, null]} />
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
            'pc_type',
            'uw_expense',
            'expense_basis',
            'std_pc_percent'
          ]} />



        <HX.With context={{ "index": 0, "path": "cds/pc/pc_structure/table_sliding_scale", "type": "list" }}>

          <HX.Table
            // shownBy='non_cds/pc/pc_structure/show_for_sliding_scale'
            syncColumnWidthsKey='table_1'
            kb-interactive
            title='For Sliding Scale'
            data={[{ datum: 'scale' }]}
            fields={[{ "field": 'gn_ulr_less_than', "maxWidth": 300 }, { "field": 'pc', "maxWidth": 300 }]}
          />

        </HX.With>



      </HX.Section>

      <HX.Section title='PC Calculations' shownBy='cds/pc/pc_control/show_details'>
        <HX.Table
          syncColumnWidthsKey='table_1'
          shownBy='cds/pc/pc_control/show_details'
          transpose
          kb-interactive
          filter={"is_row_visible"}
          data={[{ datum: 'cds/pc/pc_calculations/details', maxWidth: 300 }]}
          fields={[
            'gwp_5623',
            'deductions',
            'nwp_5623',
            null,
            'bm_class_auto',
            'bm_class_override',
            'bm_class_applied',
            'cov_basis_attr_bbt',
            'cov_basis_large_bbt',
            'cov_basis_cat_bbt',
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
          filter={"is_row_visible"}
          data={[{ datum: 'cds/pc/profit_commission/details', maxWidth: 300 }]}
          fields={[
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

export { vw_pc_bbt };