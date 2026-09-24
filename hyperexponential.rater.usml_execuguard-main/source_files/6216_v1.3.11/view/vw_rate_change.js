import * as HX from "hx-model-components";

function vw_rate_change(scale) {
  return (
    <HX.Page title="Rate Change" shownBy="cds/rate_change/show_hide_rc" viewScale={scale} fullWidth={true}>
      <HX.Section title="Fetch Expiring Policy">
        <HX.Pane flow="right" >
          <HX.Collection fields={["cds/rate_change/expiring_policy_option_id", null]} horizontal />
        </HX.Pane>
        <HX.Pane flow="right" >
          {/* <HX.Button task="expiring_policy_fetch_task" title="Fetch Expiring Data" shownBy="cds/rate_change/has_rarc_not_run" /> */}
          <HX.Button title="Calculate Rate Change" task="rarc_task" />
          <HX.Pane />
        </HX.Pane>
        <HX.Pane>
          <HX.Notes with="cds/rate_change" field="rarc_run_again_message" shownBy="rarc_message_show" />
        </HX.Pane>
      </HX.Section>

      <HX.Section>
        <HX.With context={{ type: "struct", path: "cds/rate_change" }}>
          <HX.Pane>
            <HX.Table
              rowHeaderSettings={{ width: 320 }}
              data={["premium_annualized_beazley_share"]}
              fields={[
                { field: "epl/renewal", width: 100, shownBy: "coverage_indicator/epl" }, { field: "epl/expiring", width: 100, shownBy: "coverage_indicator/epl" },
                { field: "fid/renewal", width: 100, shownBy: "coverage_indicator/fid" }, { field: "fid/expiring", width: 100, shownBy: "coverage_indicator/fid" },
                { field: "pcl/renewal", width: 100, shownBy: "coverage_indicator/pcl" }, { field: "pcl/expiring", width: 100, shownBy: "coverage_indicator/pcl" },
                null,
                { field: "execuguard/renewal", width: 100 }, { field: "execuguard/expiring", width: 100 }
              ]}
            />
          </HX.Pane>
        </HX.With>

        <HX.With context={{ type: "struct", path: "cds/rate_change" }}>
          <HX.Pane>
            <HX.Table
              rowHeaderSettings={{ width: 320 }}
              data={[
                "exposure_change",
                "risk_characteristics_change",
                "deductible_change",
                "limit_change",
                "terms_conditions_change",
                "brokerage_change",
                null,
                "rate_change"
              ]}
              fields={[
                { field: "epl/model", width: 100, shownBy: "coverage_indicator/epl" }, { field: "epl/selected", width: 100, shownBy: "coverage_indicator/epl" },
                { field: "fid/model", width: 100, shownBy: "coverage_indicator/fid" }, { field: "fid/selected", width: 100, shownBy: "coverage_indicator/fid" },
                { field: "pcl/model", width: 100, shownBy: "coverage_indicator/pcl" }, { field: "pcl/selected", width: 100, shownBy: "coverage_indicator/pcl" },
                null,
                { field: "execuguard/model", width: 100 }, { field: "execuguard/selected", width: 100 }
              ]}
            // with="rate_change"
            />
          </HX.Pane>
        </HX.With>
      </HX.Section>

      <HX.Section title="Coverage RC Details">
        <HX.With context={{ type: "struct", path: "cds/rate_change" }}>
          <HX.Pane flow="right">
            <HX.Table shownBy="coverage_indicator/epl"
              data={["fte", "limit", "ded"]}
              fields={[
                { field: "epl/expiry", width: 130 },
                { field: "epl/renewal", width: 130 },
                { field: "epl/rate_change", width: 130 }
              ]}
            />
            <HX.Table shownBy="coverage_indicator/fid"
              data={["assets", "participants", "limit", "ded"]}
              fields={[
                { field: "fid/expiry", width: 130 },
                { field: "fid/renewal", width: 130 },
                { field: "fid/rate_change", width: 130 },
              ]}
            />
            <HX.Table shownBy="execugard_package"
              data={["assets", "limit", "ded"]}
              fields={[
                { field: "pcl/expiry", width: 130 },
                { field: "pcl/renewal", width: 130 },
                { field: "pcl/rate_change", width: 130 }
              ]}
            />
            <HX.Table shownBy="not_execugard_package"
              data={["assets", "fte", "limit", "ded"]}
              fields={[
                { field: "pcl/expiry", width: 130 },
                { field: "pcl/renewal", width: 130 },
                { field: "pcl/rate_change", width: 130 }
              ]}
            />
          </HX.Pane>
          <HX.Collection title="Final Rate Change" fields={["uw_selected_rarc", null, null, null]} horizontal />
        </HX.With>
      </HX.Section>

    </HX.Page >
  )
}
export { vw_rate_change };