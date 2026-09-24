import * as HX from 'hx-model-components';
import { NUM_SECTION_REFERENCES } from "./vw_constants"

function generate_sec_ref_rows(num_refs = NUM_SECTION_REFERENCES) {
  return Array.from({ length: num_refs }, (_, i) => {
    const idx = String(i + 1).padStart(2, "0");
    return {
      field: `ref_${idx}`,
      shownBy: `/non_cds/rating_summary/section_ref_allocation/show_refs/ref_${idx}`
    };
  });
}


function vw_section_ref_allocation(scale) {
  return (
    <HX.Page title='Section Reference Allocation' fullWidth={true} viewScale={scale} shownBy="model_state/show_risk_information" >
      <HX.Section title='Section Reference Allocation'>

        <HX.Collection fields={["/cds/rating_summary/section_ref_allocation/num_ref"]} syncColumnWidthsKey='table_1' />

        <HX.Pane flow="down">
          <HX.Table
            syncColumnWidthsKey='table_1'
            with='/cds/rating_summary/section_ref_allocation'
            kb-interactive
            data={[
              { datum: "section_ref" },
              { datum: "total_trifocus" },
              { datum: "premium_by_lob", elementLabelBy: "label" },//, maxWidth: 200 }
              // { datum: "total_total_pcts" },
              // { datum: "total_check" },
            ]}
            fields={["total"]}
            transpose
            filter={"is_row_visible"}
          />
          <HX.Table
            syncColumnWidthsKey='table_1'
            with='/cds/rating_summary/section_ref_allocation'
            kb-interactive
            data={[
              { datum: "section_ref" }, //, maxWidth: 200 },
              { datum: "trifocus" }, //, maxWidth: 200 },
              { datum: "table_pcts", elementLabelBy: "label" },//, maxWidth: 200 }
              // { datum: "total_pcts_by_ref" },
              // { datum: "check" },
            ]}
            fields={[...generate_sec_ref_rows()]}
            transpose
            filter={"is_row_visible"}
          />
          <HX.Table
            syncColumnWidthsKey='table_1'
            with='/cds/rating_summary/section_ref_allocation'
            kb-interactive
            data={[
              { datum: "total_section_ref" },
              { datum: "total_trifocus" },
              { datum: "total_pcts_by_lob", elementLabelBy: "label" },//, maxWidth: 200 }
              // { datum: "total_total_pcts" },
              // { datum: "total_check" },
            ]}
            fields={["total", "check"]}
            transpose
            filter={"is_row_visible"}
          />
        </HX.Pane>

        <HX.Table
          title="Amounts Allocated to Section Reference"
          with='/cds/rating_summary/section_ref_allocation'
          kb-interactive
          data={[{ datum: "metrics_by_ref", elementLabelBy: "section_ref" }, null, "metrics_summary"]}
          fields={[
            "trifocus"
            , "status"

            , null
            , 'quoted_premium_gn_bst'
            , "written_line"
            , "quoted_premium_gg_bst"

            , null
            , "market_deductions"
            , "mga_fee"
            , "facility_brokerage"
            , "leaders_fee"
            , "service_fee"
            , "other"
            , "selected_effective_deductions"

            , null
            , "technical_premium_gn_bst"
            , "benchmark_premium_gn_bst"
            , "technical_premium_gg_bst"
            , "benchmark_premium_gg_bst"
            , "tpi"
            , "bpi"
            , "pflr"
            , "roc"
            , "rarc"

            , null
            , "technical_premium_gn_bst_pre"
            , "benchmark_premium_gn_bst_pre"
            , "technical_premium_gg_bst_pre"
            , "benchmark_premium_gg_bst_pre"
            , "tpi_pre_uw_adj"
            , "bpi_pre_uw_adj"
            , "pflr_pre_uw_adj"
            , "roc_pre_uw_adj"
            , "uw_adj_impact"

          ]}
        // transpose
        />

      </HX.Section>
    </HX.Page>
  )
}

export { vw_section_ref_allocation };