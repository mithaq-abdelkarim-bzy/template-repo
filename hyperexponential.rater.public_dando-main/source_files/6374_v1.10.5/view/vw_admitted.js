import * as HX from "hx-model-components";

function vw_admitted(scale) {
  return (
    <HX.Page
      title="Admitted"
      fullWidth={true}
      viewScale={scale}
      shownBy="cds/admitted/is_admitted">
      <HX.Section title="Select Option">
        <HX.Collection syncColumnWidthsKey="sync_admitted"
          fields={[
            "cds/admitted/selected_option"
          ]} />
      </HX.Section>
      <HX.Section title="Company Info">
        <HX.Pane flow="right">
          <HX.Collection fields={[
            "company",
            "total_assets",
            "state",
            "limit",
            "inception_date",
            "excess",
            null,
            "deductible"
          ]} with="cds/admitted" numCols={2} />
          <HX.Collection fields={[null]} />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Admitted Modifiers" shownBy="cds/admitted/is_bici">
        <HX.Pane flow="right">
          <HX.Button task="set_admitted_to_min_task" title="Set to Inputs to Minimum" />
          <HX.Button task="set_admitted_to_midpoint_task" title="Set to Inputs to Midpoint" />
          <HX.Button task="set_admitted_to_max_task" title="Set to Inputs to Maximum" />
          <HX.Button task="reset_admitted_reasons_task" title="Reset Reasons" />
          {/* <HX.Collection
            fields={[null]}
          /> */}
        </HX.Pane>
        <HX.Pane>
          <HX.Table
            syncColumnWidthsKey="sync_admitted"
            data={[
              { datum: "step_1_bpm", infoBy: "step_1_bpm/message" },
              { datum: "step_2_im", infoBy: "step_2_im/message" },
              { datum: "step_3_mam", infoBy: "step_3_mam/message" },
              { datum: "step_4_pm", infoBy: "step_4_pm/message" },
              { datum: "step_5_qm", infoBy: "step_5_qm/message" },
              { datum: "step_6_cm", infoBy: "step_6_cm/message" },
              { datum: "step_7_fm", infoBy: "step_7_fm/message" },
              { datum: "step_8_em", infoBy: "step_8_em/message" },
              { datum: "step_9_om", infoBy: "step_9_om/message" },
              { datum: "step_10_lm", infoBy: "step_10_lm/message" },
              { datum: "step_11_chm", infoBy: "step_11_chm/message" },
              { datum: "step_12_sm", infoBy: "step_12_sm/message" },
              { datum: "step_13_edm", infoBy: "step_13_edm/message" },
              { datum: "step_14_spm", infoBy: "step_14_spm/message" },
              { datum: "step_15_rm", infoBy: "step_15_rm/message" },
              { datum: "step_16_pcm", infoBy: "step_16_pcm/message" },
              { datum: "step_17_icm", infoBy: "step_17_icm/message" },
              { datum: "step_18_llm", infoBy: "step_18_llm/message" }
            ]}
            with="cds/admitted/bici"
            fields={[
              { field: "selected", width: 100 },
              { field: "min", width: 100 },
              { field: "max", width: 100 },
              { field: "reason", minWidth: 700 }
            ]}
            rowHeaderSettings={{ width: 300 }}
            kb-interactive
          />
        </HX.Pane>
        <HX.Pane>
          <HX.Table
            shownBy="cds/admitted/bici/show_final_prem_factor"
            syncColumnWidthsKey="sync_admitted"
            data={[
              "cds/admitted/bici/step_18a_fcp"
            ]}
            fields={[
              { field: "selected", width: 100 },
              { field: "min", width: 100 },
              { field: "max", width: 100 }
            ]}
            rowHeaderSettings={{ width: 300 }}
            kb-interactive
          />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Premium Info" shownBy="cds/admitted/is_bici">
        <HX.Collection
          fields={[
            "final_premium", null,
            "rounding_message", null,
            "rounded_premium", null
          ]}
          with="cds/admitted/bici"
          numCols={2} />
      </HX.Section>
      <HX.Section title="Admitted Modifiers" shownBy="cds/admitted/is_baic">
        <HX.Pane flow="right">
          <HX.Button task="set_admitted_to_min_task" title="Set to Inputs to Minimum" />
          <HX.Button task="set_admitted_to_midpoint_task" title="Set to Inputs to Midpoint" />
          <HX.Button task="set_admitted_to_max_task" title="Set to Inputs to Maximum" />
          <HX.Button task="reset_admitted_reasons_task" title="Reset Reasons" />
          {/* <HX.Collection
            fields={[null]}
          /> */}
        </HX.Pane>
        <HX.Pane>
          <HX.Table
            syncColumnWidthsKey="sync_admitted"
            data={[
              { datum: "step_1_bpm", infoBy: "step_1_bpm/message" },
              { datum: "step_2_im", infoBy: "step_2_im/message" },
              { datum: "step_3_mam", infoBy: "step_3_mam/message" },
              { datum: "step_4_pm", infoBy: "step_4_pm/message" },
              { datum: "step_5_qm", infoBy: "step_5_qm/message" },
              { datum: "step_6_cm", infoBy: "step_6_cm/message" },
              { datum: "step_7_fm", infoBy: "step_7_fm/message" },
              { datum: "step_8_em", infoBy: "step_8_em/message" },
              { datum: "step_9_om", infoBy: "step_9_om/message" },
              { datum: "step_10_lm", infoBy: "step_10_lm/message" },
              { datum: "step_11_chm", infoBy: "step_11_chm/message" },
              { datum: "step_12_sm", infoBy: "step_12_sm/message" },
              { datum: "step_13_edm", infoBy: "step_13_edm/message" },
              { datum: "step_14_spm", infoBy: "step_14_spm/message" },
              { datum: "step_15_clrm", infoBy: "step_15_clrm/message" },
              { datum: "step_16_pcm", infoBy: "step_16_pcm/message" },
              { datum: "step_17_icm", infoBy: "step_17_icm/message" },
              { datum: "step_18_yo", infoBy: "step_18_yo/message" },
              { datum: "step_19_saf", infoBy: "step_19_saf/message" }
            ]}
            fields={[
              { field: "selected", width: 120 },
              { field: "min", width: 100 },
              { field: "max", width: 100 },
              { field: "reason", minWidth: 500 }
            ]}
            with="cds/admitted/baic"
            rowHeaderSettings={{ width: 300 }}
            shownBy="is_california_not"
            kb-interactive
          />
          <HX.Table
            syncColumnWidthsKey="sync_admitted"
            data={[
              { datum: "step_1_bpm", infoBy: "step_1_bpm/message" },
              { datum: "step_2_im", infoBy: "step_2_im/message" },
              { datum: "step_3_mam", infoBy: "step_3_mam/message" },
              { datum: "step_4_pm", infoBy: "step_4_pm/message" },
              { datum: "step_5_qm", infoBy: "step_5_qm/message" },
              { datum: "step_6_cm", infoBy: "step_6_cm/message" },
              { datum: "step_7_fm", infoBy: "step_7_fm/message" },
              { datum: "step_8_em", infoBy: "step_8_em/message" },
              { datum: "step_9_om", infoBy: "step_9_om/message" },
              { datum: "step_10_lm", infoBy: "step_10_lm/message" },
              { datum: "step_11_chm", infoBy: "step_11_chm/message" },
              { datum: "step_12_sm", infoBy: "step_12_sm/message" },
              { datum: "step_13_edm", infoBy: "step_13_edm/message" },
              { datum: "step_14_spm", infoBy: "step_14_spm/message" },
              { datum: "step_15_clrm", infoBy: "step_15_clrm/message" },
              { datum: "step_16_pcm", infoBy: "step_16_pcm/message" },
              { datum: "step_17_icm", infoBy: "step_17_icm/message" },
              { datum: "step_18_yo_ca", infoBy: "step_18_yo_ca/message" },
              { datum: "step_19_saf", infoBy: "step_19_saf/message" },
              { datum: "step_20a_fwic" },
              { datum: "step_20b_iglp" },
              { datum: "step_20c_rii" },
              { datum: "step_20d_str" },
              { datum: "step_20e_mcd" },
              { datum: "step_20f_lre" },
              { datum: "step_20_srf" }
            ]}
            fields={[
              { field: "selected", width: 120 },
              { field: "min", width: 100 },
              { field: "max", width: 100 },
              { field: "reason", minWidth: 500 }
            ]}
            with="cds/admitted/baic"
            rowHeaderSettings={{ width: 300 }}
            shownBy="is_california"
            kb-interactive
          />
        </HX.Pane>
        <HX.Pane>
          <HX.Table
            shownBy="cds/admitted/baic/show_final_prem_factor"
            syncColumnWidthsKey="sync_admitted"
            data={[
              "cds/admitted/baic/step_19a_fcp"
            ]}
            fields={[
              { field: "selected", width: 120 },
              { field: "min", width: 100 },
              { field: "max", width: 100 }
            ]}
            rowHeaderSettings={{ width: 300 }}
            kb-interactive
          />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Premium Info" shownBy="cds/admitted/is_baic">
        <HX.Collection
          fields={[
            "final_premium", null,
            "rounding_message", null,
            "rounded_premium", null
          ]}
          with="cds/admitted/baic"
          numCols={2} />
      </HX.Section>
    </HX.Page >
  )
}

export { vw_admitted };