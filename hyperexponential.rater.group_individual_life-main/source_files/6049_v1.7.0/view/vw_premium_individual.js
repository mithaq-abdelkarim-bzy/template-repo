import * as HX from "hx-model-components";


function vw_premium_individual(scale) {
  return (
    <HX.Page title="Premium" shownBy="cds/is_individual">
      <HX.Section title="Life Details">
        <HX.Pane>
          <HX.With context={{ type: "list", path: "cds/exposure/granular/life", index: 0 }}>
            <HX.Collection
              fields={[
                "age_next_bday",
                "age_attained",
                "sum_insured",
                "coverage",
                "nationality",
                "location",
                "smoker_status",
                "term"
              ]}
              numCols={2}
            />
          </HX.With>
          <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
            {/* <HX.Collection fields={[{ field: "brokerage", labelBy: "brokerage_label" }, "brokerage_ri"]} horizontal /> */}
            <HX.Collection fields={["rga_load_mult", "rga_load_add"]} horizontal />
          </HX.With>
        </HX.Pane>
      </HX.Section>

      <HX.Section title="Premium Results">
        <HX.Pane>
          <HX.With context={{ type: "list", path: "cds/exposure/granular/life", index: 0 }}>
            <HX.Collection title="Beazley to pay RGA" fields={["rga_rate", "rga_premium"]} horizontal />
            <HX.Collection title="RI Brokerage" fields={["brokerage_ri_amount", "gross_rga_premium"]} horizontal />
            <HX.Collection title="Beazley to charge" fields={["bzl_rate", "bzl_premium"]} horizontal />
          </HX.With>
          <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
            <HX.Collection title="Actual quote" fields={["quoted_rate", "quoted_premium_ind"]} horizontal />
          </HX.With>
        </HX.Pane>
      </HX.Section>

      <HX.Section title="Rating Summary">
        <HX.Pane>
          <HX.With context={{ type: "list", path: "cds/layers", index: 0 }}>
            <HX.Collection fields={[{ field: "expected_loss_cost", labelBy: "el_label" }, "quoted_premium_net"]} horizontal />
            <HX.Collection fields={["benchmark_premium", "bpi"]} horizontal />
            <HX.Collection fields={["technical_premium", "tpi"]} horizontal />
          </HX.With>
        </HX.Pane>
      </HX.Section>

    </HX.Page >
  )
}

export { vw_premium_individual };
