import * as HX from 'hx-model-components';

function vw_anti_selection(scale) {
  return (
    <HX.Page title='Anti-selection' fullWidth={true} viewScale={scale} shownBy="model_state/show_anti_select">
      <HX.Section title='Anti-Selection Matrix'>

        <HX.Collection
          fields={["/cds/anti_selection/charge_required"]}
          syncColumnWidthsKey='table_1'
        />

        <HX.Table
          syncColumnWidthsKey='table_1'
          with='cds/anti_selection/matrix'
          kb-interactive
          data={[
            'baseline',
            'competing_portfolio',
            'delegation_scope',
            'quantity_quality',
            'cover_holder_alignment',
            'participation',
            'overall_selected',
          ]}
          fields={[
            'selection',
            'guideline_min',
            'guideline_max',
            'suggested',
            'final_selected',
            'comments'
          ]}
        />
      </HX.Section>
      <HX.Section title='Applied Anti-Selection Charge' shownBy="non_cds/risk_information/not_follow_main_syndicate">
        <HX.Table
          with='cds/anti_selection/applied_charge'
          kb-interactive
          data={['model_weighting', null, 'table']}
          fields={[
            'selected_lob',
            'own_performance',
            'lloyds_performance',
            'beazley_performance',
            'business_plan',
            'case_pricing',
            'pricing_2623_623',
            'anti_selection_charge'
          ]}
          filter={"is_row_visible"}
        // syncColumnWidthsKey='table_1'
        />
      </HX.Section>
      <HX.Section title='Anti-Selection Charge - Selection Details'>
        <HX.Notes field='cds/anti_selection/matrix/overall_selected/guidelines' />
        <HX.Notes field='cds/anti_selection/matrix/baseline/guidelines' />
        <HX.Notes field='cds/anti_selection/matrix/competing_portfolio/guidelines' />
        <HX.Notes field='cds/anti_selection/matrix/delegation_scope/guidelines' />
        <HX.Notes field='cds/anti_selection/matrix/quantity_quality/guidelines' />
        <HX.Notes field='cds/anti_selection/matrix/cover_holder_alignment/guidelines' />
        <HX.Notes field='cds/anti_selection/matrix/participation/guidelines' />
      </HX.Section>
    </HX.Page>
  )
}

export { vw_anti_selection };