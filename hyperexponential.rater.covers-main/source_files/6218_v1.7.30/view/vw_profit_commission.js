//########### OUTSTANDING ########################
// Needs a shownby criteria on loss distributions related to selected sceanrio


import * as HX from "hx-model-components";

function vw_profit_commission(scale) {
  return (
    <HX.Page title="Profit Commission" fullWidth={true} viewScale={0.8} shownBy="cds/show_hide/page/show_profit_commission">

      <HX.Section title="Profit Commission Base Case Analysis">
        <HX.Pane flow="right">

          <HX.Pane flow="down">
            <HX.Button task="simulate_pc_task" title="Calculate Profit Commission" />
            <HX.Notes field="cds/profit_commission/simulate_pc_task_status" />
            <HX.Notes field="cds/profit_commission/consistent_pc_latest_param" />

            <HX.With context={{ type: "list", path: "cds/profit_commission/scenarios", index: 0 }}>
              <HX.Collection
                //JB ideally this would be a table
                fields={["result_exp_loss_att"
                  , "result_exp_loss_large"
                  , "result_exp_loss_cat_other"
                  , "result_exp_loss_cat_natural"
                  , "result_exp_loss_total"
                  , null
                  , "result_exp_pc_payable"
                  , "result_exp_pc_payable_override"
                  , "result_exp_pc_payable_selected"
                  , null
                  , "result_exp_frequency_loss"
                ]}
                title="Base Case Analysis"
              />
            </HX.With>
          </HX.Pane>

          <HX.Pane flow="down">            <HX.Collection fields={[null]} />          </HX.Pane>
          <HX.Pane flow="down">            <HX.Collection fields={[null]} />          </HX.Pane>

        </HX.Pane>
      </HX.Section>


      <HX.Section title="Simulation Parameters" defaultCollapsed={true}>
        <HX.Pane flow="right">

          <HX.Table
            title="Simulation Parameters"
            data={[
              null
              , { datum: "param_attritional" }
              , { datum: "param_large" }
              , { datum: "param_cat_natural" }
              , { datum: "param_cat_other" }
            ]}
            fields={[
              { field: "expected_loss", maxWidth: 140 }
              , { field: "cov_benchmark", maxWidth: 140 }
              , { field: "cov_actual", maxWidth: 140 }
              , { field: "cov_selected", maxWidth: 140 }
              , { field: "stdev_benchmark", maxWidth: 140 }
              , { field: "stdev_actual", maxWidth: 140 }
              , { field: "stdev_selected", maxWidth: 140 }
              , { field: "distribution", maxWidth: 300 }
              , { field: "param_1", maxWidth: 140 }
              , { field: "param_2", maxWidth: 140 }
              , { field: "client_weight", maxWidth: 140 }

            ]}
            with="cds/profit_commission"
          />

        </HX.Pane>
      </HX.Section>


      <HX.Section title="Profit Commission - Scenario Analysis" defaultCollapsed={true}>
        <HX.Pane flow="down">

          <HX.Table
            title="Simulation Scenario Inputs"
            data={[{ datum: "scenarios", elementLabelBy: "label", maxWidth: 140 }]}
            fields={[
              null
              , { field: "include" }
              , { field: "additionalfeaturesindicator" }
              , null

              , { field: "share" }
              , { field: "expenses" }
              , { field: "basis" }
              , { field: "deficit" }
              , null

              , { field: "threshold_lr_cutoff1" }
              , { field: "threshold_bonus_share1" }
              , { field: "threshold_lr_cutoff2" }
              , { field: "threshold_bonus_share2" }
              , { field: "threshold_lr_cutoff3" }
              , { field: "threshold_bonus_share3" }
              , { field: "threshold_bonus_share4" }
              , null

              , { field: "slidingscale_bonus_lr" }
              , { field: "slidingscale_bonus_scale" }
              , { field: "slidingscale_bonus_maxtotalpc" }
              , { field: "slidingscale_clawback_lr" }
              , { field: "slidingscale_clawback_scale" }
              , { field: "slidingscale_clawback_mintotalpc" }
              , null

              , { field: "complete" }

            ]}
            with="cds/profit_commission"
            transpose
            kb-interactive
            syncColumnWidthsKey="pc_scenarios"
          />

          <HX.Table
            title="Simulation Scenario Outputs"
            data={[{ datum: "scenarios", elementLabelBy: "label", maxWidth: 140 }]}
            fields={[
              null
              , { field: "result_exp_loss_att" }
              , { field: "result_exp_loss_large" }
              , { field: "result_exp_loss_cat_other" }
              , { field: "result_exp_loss_cat_natural" }
              , { field: "result_exp_loss_total" }
              , null

              , { field: "result_exp_pc_payable" }
              , { field: "result_exp_pc_payable_override" }
              , { field: "result_exp_pc_payable_selected" }
              , null

              , { field: "result_exp_frequency_loss" }

            ]}
            with="cds/profit_commission"
            transpose
            kb-interactive
            syncColumnWidthsKey="pc_scenarios"
          />
        </HX.Pane>
      </HX.Section>


      <HX.Section title="Profit Commission - Loss Distributions" defaultCollapsed={true}>
        <HX.Pane flow="down">
          <HX.Table
            title="Simulation Scenario Inputs"
            data={[{ datum: "distributions", elementLabelBy: "bucket" }]}
            fields={[
              null
              , { field: "ulr", maxWidth: 140 }
              , null
              , { field: "scenario", maxWidth: 140 }
              , null
              , { field: "uw_profit", maxWidth: 140 }
              , { field: "pc_payable", maxWidth: 140 }
              , { field: "pdf_att", maxWidth: 140 }
              , { field: "pdf_large", maxWidth: 140 }
              , { field: "pdf_cat_other", maxWidth: 140 }
              , { field: "pdf_cat_natural", maxWidth: 140 }
              , { field: "pdf_total", maxWidth: 140 }
            ]}
            with="cds/profit_commission"
            kb-interactive
          />
        </HX.Pane>
      </HX.Section>


    </HX.Page >
  )
}

export { vw_profit_commission };
