import * as HX from 'hx-model-components';

function vw_uncertainty(scale) {
  return (
    <HX.Page title='Uncertainty' fullWidth={true} viewScale={scale} shownBy="model_state/show_uncertainty">
      <HX.Section title='Uncertainty Matrix'>

        <HX.Collection
          fields={["/cds/uncertainty/charge_required"]}
          syncColumnWidthsKey='table_1'
        />

        <HX.Table
          syncColumnWidthsKey='table_1'
          with='cds/uncertainty/matrix'
          kb-interactive
          data={[
            'quantity',
            'quality',
            'new_or_existing_facility',
            'perf_volatility',
            'reliance_on_ext_modelling',
            'add_subjectivity',
            null,
            'perf_discount',
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


      <HX.Section title='Applied Uncertainty Charge' shownBy="non_cds/risk_information/not_follow_main_syndicate">
        <HX.Table
          kb-interactive
          with='cds/uncertainty/applied_charge'
          data={['model_weighting', null, 'table']}
          fields={[
            'selected_lob',
            'own_performance',
            'lloyds_performance',
            'beazley_performance',
            'business_plan',
            'case_pricing',
            'pricing_2623_623',
            'load'
          ]}
          filter={"is_row_visible"}
        // syncColumnWidthsKey='table_1'
        />
      </HX.Section>
      <HX.Section title='Uncertainty Load - Selection Details/guidelines'>
        <HX.Notes field='cds/uncertainty/matrix/overall_selected/guidelines' />
        <HX.Notes field='cds/uncertainty/matrix/quantity/guidelines' />
        <HX.Notes field='cds/uncertainty/matrix/quality/guidelines' />
        <HX.Notes field='cds/uncertainty/matrix/new_or_existing_facility/guidelines' />
        <HX.Notes field='cds/uncertainty/matrix/perf_volatility/guidelines' />
        <HX.Notes field='cds/uncertainty/matrix/reliance_on_ext_modelling/guidelines' />
        <HX.Notes field='cds/uncertainty/matrix/add_subjectivity/guidelines' />
        <HX.Notes field='cds/uncertainty/matrix/perf_discount/guidelines' />
      </HX.Section>
    </HX.Page>
  )
}

export { vw_uncertainty };