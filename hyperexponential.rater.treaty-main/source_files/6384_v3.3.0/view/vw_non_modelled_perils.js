import * as HX from "hx-model-components";
import { number_curves } from "view/vw_constants";

function vw_nmp_calcs(num_curves) {
  const objects = [];

  for (let n = 0; n < num_curves; n++) {
    const nmpField = [
      "limit.read_only_option",
      "excess.read_only_option",
      `nmp/non_modelled_perils_${n + 1}/gross_el`,
      `nmp/non_modelled_perils_${n + 1}/loss_on_line`,
      `nmp/non_modelled_perils_${n + 1}/gross_sd`,
      `nmp/non_modelled_perils_${n + 1}/include_curve`];

    objects.push(
      <HX.Section title={"Curve " + (n + 1)} shownBy={"cds/non_modelled_perils_visual/show_curve_" + (n + 1)} >
        <HX.With context={{ type: "list", path: "cds/non_modelled_perils", index: n }}>
          <HX.Pane flow="right">
            <HX.Table
              data={[{ datum: "curve_selections" },
              ]}
              fields={[
                "include_in_summary",
                "broker_pml",
                "peril",
                "description",
                { field: "curve", shownBy: "curve_selections/show_market_pml" },
                "rp",
                "loss",
                { field: "currency", shownBy: "/cds/show_intl_fields" }
              ]}
              transpose
              kb-interactive
            />
            <HX.Pane>
              <HX.Table
                data={[
                  "rp_labels",
                  { datum: "pml_broker", labelBy: "curve_selections/pml_broker_label" },
                  { datum: "pml_market", labelBy: "curve_selections/pml_market_label" },
                  "pml_final"
                ]}
                fields={["rp_10000", "rp_5000", "rp_1000", "rp_500", "rp_250", "rp_200", "rp_100", "rp_50", "rp_25", "rp_10", "rp_5", "rp_2"]}
                transpose
                kb-interactive
              />
            </HX.Pane>
          </HX.Pane>

        </HX.With>
        <HX.Pane>
          <HX.Table
            data={[{ datum: "cds/layers" }]}
            fields={nmpField}
            freezeLeft={0}
            kb-interactive
          />
        </HX.Pane>
      </HX.Section >
    );
  }

  return objects
}


function vw_non_modelled_perils(scale) {
  return (
    <HX.Page title="NMP" fullWidth={true} viewScale={scale} shownBy="cds/show_non_risk_xl">
      <HX.Section title="Summary">
        <HX.Pane flow="right" reflow={false}>
          <HX.Pane>
            <HX.Notes
              field="cds/non_modelled_perils_visual/information"
              title="NMP Information"
            />
            <HX.Notes
              field="cds/non_modelled_perils_visual/us_wf_information"
              title="US Wildfire RI Cost"
            />
          </HX.Pane>
          <HX.Pane>
          </HX.Pane>
        </HX.Pane>
        <HX.Pane flow="right" reflow={false}>
          <HX.Pane ratio={5}>
            <HX.Table
              data={[{ datum: "cds/layers" },
              ]}
              fields={[
                "limit.read_only_option",
                "excess.read_only_option",
                "nmp/non_modelled_perils_total/gross_el",
                "nmp/non_modelled_perils_total/gross_sd",
                "nmp/non_modelled_perils_total/gross_el_uw",
                "nmp/non_modelled_perils_total/gross_sd_uw",
                null,
                "nmp/non_modelled_perils_total/loss_on_line"
              ]}
              kb-interactive
            />
          </HX.Pane>
          <HX.Pane ratio={1}>
            <HX.Collection
              fields={["cds/non_modelled_perils_visual/curve_number"]}
            />
            <HX.Button task="nmp_calc_task" title="Run NMP Task" />
          </HX.Pane>
        </HX.Pane>
      </HX.Section>
      {vw_nmp_calcs(number_curves())}
    </HX.Page>
  )
}

export { vw_non_modelled_perils }