import * as HX from "hx-model-components";
import { peril_references, peril_titles } from "view/vw_constants";

function vw_peril_allocation_calcs(peril_references, peril_titles) {
  const objects = [];
  const peril_allocation_fields = [
    "peril_allocation/rms_aal"
    , "peril_allocation/air_aal"
    , "peril_allocation/rms_el_approx"
    , "peril_allocation/air_el_approx"
    , "peril_allocation/ivor_aal"]


  peril_references.forEach((peril_ref, index) => {
    const peril_title = peril_titles[index];
    const peril_allocation_fields_mod = peril_allocation_fields.map(field_ref => field_ref + "/" + peril_ref)
    objects.push(
      <HX.Table
        title={peril_title}
        data={["cds/layers"]}
        fields={peril_allocation_fields_mod}
        freezeLeft={0}
        rowHeaderSettings={{ width: 250 }}
        kb-interactive
      />
    );
  });

  return objects
}

function vw_peril_allocation(scale) {
  return (
    <HX.Page title="Peril Allocation" fullWidth={true} viewScale={scale} shownBy="cds/show_non_risk_xl">
      <HX.Section title="Final Proportions">
        <HX.Table
          data={["cds/layers"]}
          fields={[
            "peril_allocation/final_proportions/el_eq",
            "peril_allocation/final_proportions/el_ws",
            "peril_allocation/final_proportions/el_scs",
            "peril_allocation/final_proportions/el_wf",
            "peril_allocation/final_proportions/el_winter",
            "peril_allocation/final_proportions/el_fl",
            "peril_allocation/final_proportions/el_other"
          ]}
          freezeLeft={0}
          rowHeaderSettings={{ width: 250 }}
          kb-interactive
        />
      </HX.Section>
      <HX.Section title="Methodology">
        <HX.Pane flow="right" reflow={false}>
          <HX.Pane >
            <HX.Collection
              numCols={2}
              fields={[
                "cds/peril_allocation_account_level/allocation_methodology",
                "cds/peril_allocation_account_level/include_ivor",
                "cds/peril_allocation_account_level/skip_peril_allocation"
              ]}
            />
          </HX.Pane>
          <HX.Pane>
            <HX.Button task="peril_allocation_task" title="Run Peril Allocation" />
          </HX.Pane>
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Peril Allocation Inputs">
        {vw_peril_allocation_calcs(peril_references, peril_titles)}
      </HX.Section>
    </HX.Page >
  )
}

export { vw_peril_allocation };