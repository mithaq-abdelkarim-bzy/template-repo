import * as HX from "hx-model-components";
import ChoroplethMap from "components/choropleth";
import SimpleToggle from "components/toggle";

function vw_region_summary(scale) {
  return (
    <HX.Page title="Region Summary" fullWidth shownBy="cds/show_hide/page/show_sov">

      <HX.With context={{ type: "struct", path: "cds/exposure/aggregate" }}>

        <HX.Section title="Construction Summary">
          <HX.Pane flow="right">
            <HX.Pane>
              <HX.Collection fields={["show_chart"]} />
            </HX.Pane>
            <HX.Pane ratio={5} />
          </HX.Pane>
          <SimpleToggle boolNode={"show_counties"} falseLabel="States" trueLabel="States and Counties" shownBy="show_chart" />
          <HX.Pane flow="right" shownBy="show_chart">
            <HX.Pane  >
              <ChoroplethMap
                title="USA States"
                list="region_summary_state"
                text="label"
                locations="state"
                locationmode="USA-states"
                zs={["tiv", "beazley_share_gn_prem", "one_in_250_oep", "one_in_10_aep", "share_lim", "perc_share_limit", "beazley_share_lim"]}
                options={["TIV", "Beazley Share GN Prem", "1 in 250 OEP", "1 in 10 AEP", "Share Limit", "Share Limit %", "AFB Share Limit"]}
                percentFormat={[false, false, false, false, false, true, false]}
              />
            </HX.Pane>
            <HX.Pane shownBy="show_counties">
              <ChoroplethMap
                title="USA Counties"
                list="region_summary"
                text="county"
                locations="fips"
                locationmode="USA-counties"
                zs={["tiv", "beazley_share_gn_prem", "one_in_250_oep", "one_in_10_aep", "share_lim", "perc_share_limit", "beazley_share_lim"]}
                options={["TIV", "Beazley Share GN Prem", "1 in 250 OEP", "1 in 10 AEP", "Share Limit", "Share Limit %", "AFB Share Limit"]}
                percentFormat={[false, false, false, false, true, false]}
                ignoreLastRow
              />
            </HX.Pane>
          </HX.Pane>
          <HX.Table
            fields={["state", "county", "tiv", "beazley_share_gn_prem", "one_in_250_oep", "one_in_10_aep", "share_lim", "perc_share_limit", "beazley_share_lim"]}
            data={["region_summary", null, "region_summary_total"]}
            filter="show_row"
            dynamic={true}
            kb-interactive
            freezeLeft={2}
            maxListVisibleRows={20}
          />
        </HX.Section>

      </HX.With>

    </HX.Page>
  )
}

export { vw_region_summary };