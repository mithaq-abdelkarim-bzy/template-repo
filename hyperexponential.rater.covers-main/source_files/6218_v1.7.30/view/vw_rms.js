//########### OUTSTANDING ########################
// Needs a shownby criteria 



import * as HX from "hx-model-components";


function vw_rms(scale) {
  return (
    <HX.Page title="RMS" shownBy="cds/show_hide/page/show_rms">

      <HX.Section title="RMS Results">

        <HX.Pane>
          <HX.Collection fields={["rms/edm_reference_requested", null, null]} with="cds" horizontal />

          <HX.Pane flow="right">
            <HX.Button task="edm_fetch_task" title="Search Database" />
            <HX.Notes field="cds/rms/fetch_edm_data_reference_lookup_task_status" />
            <HX.Collection fields={[null]} />
          </HX.Pane>

          <HX.Collection fields={["rms/edm_reference_selected", null, null]} with="cds" horizontal />
          <HX.Collection fields={["rms/use_override", null, null]} with="cds" horizontal />
        </HX.Pane>


        <HX.Pane>
          <HX.Collection fields={[null]} />
        </HX.Pane>


        <HX.Table
          title="Summary Information"
          data={["cds/rms/edm_summary/all_peril_calc_at_acc_fx"
            , "cds/rms/edm_summary/all_peril_override_at_acc_fx"
            , "cds/rms/edm_summary/all_peril_selected_at_acc_fx"
          ]}
          fields={[
            "fx"
            , "aal_raw"
            , "aal"
            , "std_dev"
            , "prem"
            , "coeff_var"
            , "gross_lr_pre_adj"
            , "gross_lr"
          ]}
          kb-interactive
          transpose
          syncColumnWidthsKey="rms"
        />


        <HX.Table
          title="EP Curve"
          data={[{ datum: "edm_epcurve", elementLabelBy: "return_period_label" }]}
          fields={[
            "all_peril_calc_at_acc_fx"
            , "all_peril_override_at_acc_fx"
            , "all_peril_selected_at_acc_fx"
          ]}
          with="cds/rms"
          kb-interactive
          dynamic
          syncColumnWidthsKey="rms"
        />



      </HX.Section>
    </HX.Page>
  )
}

export { vw_rms };
