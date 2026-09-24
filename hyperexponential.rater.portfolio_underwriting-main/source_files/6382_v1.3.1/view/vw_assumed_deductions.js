import * as HX from "hx-model-components";
import { YEARS_TO_CONSIDER_IN_ASSUMED_DEDUCTIONS } from './vw_constants'

const getYearsHeaders = (start = 0, prefix = '') => {
  return Array.from({ length: YEARS_TO_CONSIDER_IN_ASSUMED_DEDUCTIONS }, (_, i) => ({
    field: `year_${start + i}`,
    labelBy: `/non_cds/assumed_deductions/${prefix}year_${start + i}`
  }));
};

function vw_assumed_deductions(scale) {
  return (
    <HX.Page title="Deductions" fullWidth={true} viewScale={scale} shownBy="model_state/show_deductions">
      <HX.Section collapsible={false} shownBy="cds/risk_information/prem_data_available" title=" ">
        <HX.Collection fields={[
          "cds/assumed_deductions/model_type", null, null, null, null, null, null, null,
          "cds/assumed_deductions/data_driven_deductions/year_start",
          "cds/assumed_deductions/data_driven_deductions/year_end"]}
          horizontal={true} />
      </HX.Section>
      <HX.Section title="Gross Premium" shownBy="cds/risk_information/prem_data_available" defaultCollapsed={true}>
        <HX.Table
          kb-interactive
          title="Gross Premium Derived From Data"
          with="cds/assumed_deductions/data_driven_deductions/gross_premium"
          data={['deductions_derived_from_data', null, "summary"]}
          fields={[
            "selected_lob",
            ...getYearsHeaders().reverse()
          ]}
          syncColumnWidthsKey="table_1"
        />
      </HX.Section>
      <HX.Section title="Net Premium" shownBy="cds/risk_information/prem_data_available" defaultCollapsed={true}>
        <HX.Table
          kb-interactive
          title="Net Premium Derived From Data"
          with="cds/assumed_deductions/data_driven_deductions/net_premium"
          data={['deductions_derived_from_data', null, "summary"]}
          fields={[
            "selected_lob",
            ...getYearsHeaders().reverse()
          ]}
          syncColumnWidthsKey="table_1"
        />
      </HX.Section>
      <HX.Section title="Market Deductions" shownBy="cds/risk_information/prem_data_available" defaultCollapsed={true}>
        <HX.Table
          kb-interactive
          title="Implied Market Deductions Derived From Data"
          with="cds/assumed_deductions/data_driven_deductions/market_deductions"
          data={['deductions_derived_from_data', null, "summary"]}
          fields={[
            "selected_lob",
            ...getYearsHeaders().reverse()
          ]}
          syncColumnWidthsKey="table_1"
        />
      </HX.Section>
      <HX.Section title="Data Driven Deductions" shownBy="cds/risk_information/prem_data_available" collapsible={false}>
        <HX.Table
          title="Data Driven Deductions"
          data={['cds/assumed_deductions/data_driven_deductions/deductions/amount', 'cds/assumed_deductions/data_driven_deductions/deductions/basis', null, 'cds/assumed_deductions/data_driven_deductions/deductions/table']}
          fields={['selected_lob', 'market_deductions', 'mga_fee', 'facility_brokerage', 'leaders_fee', 'service_fee', 'other', 'selected_effective_deductions']}
          syncColumnWidthsKey="bp_summary_by_lob"
          filter={'is_row_visible'}
          kb-interactive
        />
      </HX.Section>
      <HX.Section title="Manually Entered Deductions" shownBy="non_cds/assumed_deductions/is_manual" collapsible={false}>
        <HX.Table
          title=" "
          data={['cds/assumed_deductions/deductions_manually_entered/amount', 'cds/assumed_deductions/deductions_manually_entered/basis']}
          fields={["selected_lob", "market_deductions", 'mga_fee', 'facility_brokerage', 'leaders_fee', 'service_fee', 'other']}
          syncColumnWidthsKey="bp_summary_by_lob"
          kb-interactive
        />
        <HX.Table
          title="Manually entered Deductions"
          data={['cds/assumed_deductions/deductions_manually_entered/table']}
          fields={['selected_lob', 'market_deductions', 'mga_fee', 'facility_brokerage', 'leaders_fee', 'service_fee', 'other', 'selected_effective_deductions']}
          syncColumnWidthsKey="bp_summary_by_lob"
          maxListVisibleRows={15}
          filter={'is_row_visible'}
          kb-interactive
        />
      </HX.Section>
    </HX.Page >
  )
}

export { vw_assumed_deductions };