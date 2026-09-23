import * as HX from "hx-model-components";

function vw_rating_summary_mmp(scale) {
  return (
    <HX.Page title="Rating Summary MMP" fullWidth={true} shownBy="cds/risk_information/mmp_flag">
      {/* <HX.Section title="Rating Methodology">
        <HX.Pane flow="right">
          <HX.Collection fields={["cds/standard_fields/rating_methodology"]} />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>
      </HX.Section> */}
      <HX.Section title="Risk Summary">
        <HX.Pane flow="right">
          <HX.Table
            data={[{ datum: "cds", width: 400 }]}
            fields={[
              "standard_fields/insured_name.read_only",
              { field: "currencies/source_currency.read_only" },
              { field: "exposure/aggregate/exposure_currency.read_only", shownBy: "cds/risk_information/private_flag" },
              "exposure/aggregate/total_assets.read_only",
              "exposure/aggregate/row_ftes.read_only",
              null,
              "rating_factors/risk_information/country_of_domicile.read_only",
              "rating_factors/risk_information/main_operating_country.read_only",
            ]}
            transpose
            rowHeaderSettings={{ width: 200 }}
            kb-interactive
          />
          <HX.Pane>
            <HX.Notes field="cds/mmp/total/validation_note" title="Middle Market Private Notes" />

          </HX.Pane>
        </HX.Pane>

      </HX.Section>

      <HX.Section title="Middle Market" >
        <HX.Table
          title="Middle Market"
          data={["dno", "epl", "cll", //"crime", 
            // "ptl", 
            "total"]}
          fields={[
            { field: "coverage", width: 150 },
            { field: "expiring_appetite_comment.read_only", width: 150 },
            { field: "agg_aoc_limit", width: 150 },
            { field: "appetite_comment", width: 150 },
            { field: "limit", width: 150 },
            { field: "excess", width: 150 },
            { field: "deductible", width: 150 },
            null,
            { field: "quoted_premium_100", width: 150 },
            { field: "brokerage", width: 150 },
            { field: "written_line", width: 150 },
            { field: "technical_premium", width: 150 },
            { field: "benchmark_premium", width: 160 },
            null,
            { field: "status", width: 150 },
            { field: "section_reference", width: 150 },
            { field: "slip_leader", shownBy: "/cds/validation/slip_leader/valid", width: 150},
            { field: "slip_leader.notSupported", infoBy: "/cds/validation/slip_leader/info_text", shownBy: "/cds/validation/slip_leader/invalid", width: 150 },
            { field: "notes", width: 150 },
            null,
            { field: "tpi", width: 150 },
            { field: "bpi", width: 150 },
          ]}
          freezeLeft={0}
          with="cds/mmp"
          kb-interactive
        />
      </HX.Section>

      <HX.Section title="Options Calculators - Agg Limit" >
        <HX.Table
          title="D&O"
          data={["cds/mmp/dno/option_1", "cds/mmp/dno/option_2", "cds/mmp/dno/option_3", "cds/mmp/dno/option_4"]}
          fields={[
            { field: "aggregate_limit" },
            { field: "aggregate_excess" },
            { field: "aggregate_deductible" },
            { field: "technical_premium" }
          ]}
          transpose
          kb-interactive />

        <HX.Table
          title="EPL"
          data={["cds/mmp/epl/option_1", "cds/mmp/epl/option_2", "cds/mmp/epl/option_3", "cds/mmp/epl/option_4"]}
          fields={[
            { field: "aggregate_limit" },
            { field: "aggregate_excess" },
            { field: "aggregate_deductible" },
            { field: "technical_premium" }
          ]}
          transpose
          kb-interactive />

        <HX.Table
          title="CLL"
          data={["cds/mmp/cll/option_1", "cds/mmp/cll/option_2", "cds/mmp/cll/option_3", "cds/mmp/cll/option_4"]}
          fields={[
            { field: "aggregate_limit" },
            { field: "aggregate_excess" },
            { field: "aggregate_deductible" },
            { field: "technical_premium" }
          ]}
          transpose
          kb-interactive />

      </HX.Section>
    </HX.Page >

  )
}


export { vw_rating_summary_mmp };