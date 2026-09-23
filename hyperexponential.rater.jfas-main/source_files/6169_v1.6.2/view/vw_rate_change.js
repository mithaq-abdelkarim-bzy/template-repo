import * as HX from "hx-model-components"; //Does this need to be imported in every subscript?
import Waterfall from "components/waterfall";

function vw_rate_change(scale) {
  return (
    <HX.Page title="Rate Change" fullWidth={true} viewScale={scale} shownBy="cds/show_page/show_rate_change" >
      <HX.With context={{ type: "list", path: "cds/layers", index: 0 }} >
        <HX.Section title="Technical Rate Change">
          <HX.Pane>
            <HX.Table shownBy="/cds/jb_masking"
              data={["jb_rc_tech"]}
              fields={[
                "prem_ly",
                "prem_exp_ly", "prem_exp_ty", "chg_exp", "prem_adj_exp",
                "prem_ded_ly", "prem_ded_ty", "chg_ded", "prem_adj_ded",
                "prem_lim_ly", "prem_lim_ty", "chg_lim", "prem_adj_lim",
                "prem_risk_ly", "prem_risk_ty", "chg_risk", "prem_adj_risk",
                "prem_tc_ly", "prem_tc_ty", "chg_tc", "prem_adj_tc",
                "prem_ty", "rarc"
              ]}
            />
            <HX.Table shownBy="/cds/fa_masking"
              data={["fa_rc_tech"]}
              fields={[
                "prem_ly",
                "prem_exp_ly", "prem_exp_ty", "chg_exp", "prem_adj_exp",
                "prem_ded_ly", "prem_ded_ty", "chg_ded", "prem_adj_ded",
                "prem_lim_ly", "prem_lim_ty", "chg_lim", "prem_adj_lim",
                "prem_risk_ly", "prem_risk_ty", "chg_risk", "prem_adj_risk",
                "prem_tc_ly", "prem_tc_ty", "chg_tc", "prem_adj_tc",
                "prem_ty", "rarc"
              ]}
            />
            <HX.Table shownBy="/cds/gs_masking"
              data={["gs_rc_tech"]}
              fields={[
                "prem_ly",
                "prem_exp_ly", "prem_exp_ty", "chg_exp", "prem_adj_exp",
                "prem_ded_ly", "prem_ded_ty", "chg_ded", "prem_adj_ded",
                "prem_lim_ly", "prem_lim_ty", "chg_lim", "prem_adj_lim",
                "prem_risk_ly", "prem_risk_ty", "chg_risk", "prem_adj_risk",
                "prem_tc_ly", "prem_tc_ty", "chg_tc", "prem_adj_tc",
                "prem_ty", "rarc"
              ]}
            />
            <HX.Table shownBy="/cds/cit_masking"
              data={["cit_rc_tech"]}
              fields={[
                "prem_ly",
                "prem_exp_ly", "prem_exp_ty", "chg_exp", "prem_adj_exp",
                "prem_ded_ly", "prem_ded_ty", "chg_ded", "prem_adj_ded",
                "prem_lim_ly", "prem_lim_ty", "chg_lim", "prem_adj_lim",
                "prem_risk_ly", "prem_risk_ty", "chg_risk", "prem_adj_risk",
                "prem_tc_ly", "prem_tc_ty", "chg_tc", "prem_adj_tc",
                "prem_ty", "rarc"
              ]}
            />
          </HX.Pane>
          <HX.Pane shownBy="/cds/jb_masking" flow="right">
            <Waterfall
              title="JB Premises Rate Change"
              // xAxisLabel="Risk component"
              yAxisLabel="GNWP (USD)"
              data={[
                { value: "exp_prem", label: "Expiring Premium" },
                { value: "exposure", label: "Exposure" },
                { value: "deduct", label: "Deductibles" },
                { value: "limit", label: "Limits" },
                { value: "risk", label: "Risk" },
                { value: "t_and_cs", label: "T&Cs" },
                { value: "risk_adj_prem", label: "Risk Adj Prem" },
                { value: "quote_prem", label: "Quote Prem" },
              ]}
              with="jb_1_rc_waterfall"
            />
            <Waterfall
              title="JB Travel Rate Change"
              // xAxisLabel="Risk component"
              yAxisLabel="GNWP (USD)"
              data={[
                { value: "exp_prem", label: "Expiring Premium" },
                { value: "exposure", label: "Exposure" },
                { value: "deduct", label: "Deductibles" },
                { value: "limit", label: "Limits" },
                { value: "risk", label: "Risk" },
                { value: "t_and_cs", label: "T&Cs" },
                { value: "risk_adj_prem", label: "Risk Adj Prem" },
                { value: "quote_prem", label: "Quote Prem" },
              ]}
              with="jb_2_rc_waterfall"
            />
            <Waterfall
              title="JB Additional Rate Change"
              // xAxisLabel="Risk component"
              yAxisLabel="GNWP (USD)"
              data={[
                { value: "exp_prem", label: "Expiring Premium" },
                { value: "exposure", label: "Exposure" },
                { value: "deduct", label: "Deductibles" },
                { value: "limit", label: "Limits" },
                { value: "risk", label: "Risk" },
                { value: "t_and_cs", label: "T&Cs" },
                { value: "risk_adj_prem", label: "Risk Adj Prem" },
                { value: "quote_prem", label: "Quote Prem" },
              ]}
              with="jb_3_rc_waterfall"
            />
          </HX.Pane>
          <HX.Pane shownBy="/cds/fa_masking" flow="right">
            <Waterfall
              title="FA Premises Rate Change"
              xAxisLabel="Risk component"
              yAxisLabel="GNWP (USD)"
              data={[
                { value: "exp_prem", label: "Expiring Premium" },
                { value: "exposure", label: "Exposure" },
                { value: "deduct", label: "Deductibles" },
                { value: "limit", label: "Limits" },
                { value: "risk", label: "Risk" },
                { value: "t_and_cs", label: "T&Cs" },
                { value: "risk_adj_prem", label: "Risk Adj Prem" },
                { value: "quote_prem", label: "Quote Prem" },
              ]}
              with="fa_1_rc_waterfall"
            />
            <Waterfall
              title="FA Travel Rate Change"
              xAxisLabel="Risk component"
              yAxisLabel="GNWP (USD)"
              data={[
                { value: "exp_prem", label: "Expiring Premium" },
                { value: "exposure", label: "Exposure" },
                { value: "deduct", label: "Deductibles" },
                { value: "limit", label: "Limits" },
                { value: "risk", label: "Risk" },
                { value: "t_and_cs", label: "T&Cs" },
                { value: "risk_adj_prem", label: "Risk Adj Prem" },
                { value: "quote_prem", label: "Quote Prem" },
              ]}
              with="fa_2_rc_waterfall"
            />
            <Waterfall
              title="FA Additional Rate Change"
              xAxisLabel="Risk component"
              yAxisLabel="GNWP (USD)"
              data={[
                { value: "exp_prem", label: "Expiring Premium" },
                { value: "exposure", label: "Exposure" },
                { value: "deduct", label: "Deductibles" },
                { value: "limit", label: "Limits" },
                { value: "risk", label: "Risk" },
                { value: "t_and_cs", label: "T&Cs" },
                { value: "risk_adj_prem", label: "Risk Adj Prem" },
                { value: "quote_prem", label: "Quote Prem" },
              ]}
              with="fa_3_rc_waterfall"
            />
          </HX.Pane>
          <HX.Pane shownBy="/cds/gs_masking" flow="right">
            <Waterfall
              title="GS Metals Rate Change"
              xAxisLabel="Risk component"
              yAxisLabel="GNWP (USD)"
              data={[
                { value: "exp_prem", label: "Expiring Premium" },
                { value: "exposure", label: "Exposure" },
                { value: "deduct", label: "Deductibles" },
                { value: "limit", label: "Limits" },
                { value: "risk", label: "Risk" },
                { value: "t_and_cs", label: "T&Cs" },
                { value: "risk_adj_prem", label: "Risk Adj Prem" },
                { value: "quote_prem", label: "Quote Prem" },
              ]}
              with="gs_1_rc_waterfall"
            />
            <Waterfall
              title="GS Cash Rate Change"
              xAxisLabel="Risk component"
              yAxisLabel="GNWP (USD)"
              data={[
                { value: "exp_prem", label: "Expiring Premium" },
                { value: "exposure", label: "Exposure" },
                { value: "deduct", label: "Deductibles" },
                { value: "limit", label: "Limits" },
                { value: "risk", label: "Risk" },
                { value: "t_and_cs", label: "T&Cs" },
                { value: "risk_adj_prem", label: "Risk Adj Prem" },
                { value: "quote_prem", label: "Quote Prem" },
              ]}
              with="gs_2_rc_waterfall"
            />
            <Waterfall
              title="GS Securities Rate Change"
              xAxisLabel="Risk component"
              yAxisLabel="GNWP (USD)"
              data={[
                { value: "exp_prem", label: "Expiring Premium" },
                { value: "exposure", label: "Exposure" },
                { value: "deduct", label: "Deductibles" },
                { value: "limit", label: "Limits" },
                { value: "risk", label: "Risk" },
                { value: "t_and_cs", label: "T&Cs" },
                { value: "risk_adj_prem", label: "Risk Adj Prem" },
                { value: "quote_prem", label: "Quote Prem" },
              ]}
              with="gs_3_rc_waterfall"
            />
            <Waterfall
              title="GS Additional Rate Change"
              xAxisLabel="Risk component"
              yAxisLabel="GNWP (USD)"
              data={[
                { value: "exp_prem", label: "Expiring Premium" },
                { value: "exposure", label: "Exposure" },
                { value: "deduct", label: "Deductibles" },
                { value: "limit", label: "Limits" },
                { value: "risk", label: "Risk" },
                { value: "t_and_cs", label: "T&Cs" },
                { value: "risk_adj_prem", label: "Risk Adj Prem" },
                { value: "quote_prem", label: "Quote Prem" },
              ]}
              with="gs_4_rc_waterfall"
            />
          </HX.Pane>
          <HX.Pane shownBy="/cds/cit_masking" flow="right">
            <Waterfall
              title="CIT Premises Rate Change"
              xAxisLabel="Risk component"
              yAxisLabel="GNWP (USD)"
              data={[
                { value: "exp_prem", label: "Expiring Premium" },
                { value: "exposure", label: "Exposure" },
                { value: "deduct", label: "Deductibles" },
                { value: "limit", label: "Limits" },
                { value: "risk", label: "Risk" },
                { value: "t_and_cs", label: "T&Cs" },
                { value: "risk_adj_prem", label: "Risk Adj Prem" },
                { value: "quote_prem", label: "Quote Prem" },
              ]}
              with="cit_1_rc_waterfall"
            />
            <Waterfall
              title="CIT Additional Rate Change"
              xAxisLabel="Risk component"
              yAxisLabel="GNWP (USD)"
              data={[
                { value: "exp_prem", label: "Expiring Premium" },
                { value: "exposure", label: "Exposure" },
                { value: "deduct", label: "Deductibles" },
                { value: "limit", label: "Limits" },
                { value: "risk", label: "Risk" },
                { value: "t_and_cs", label: "T&Cs" },
                { value: "risk_adj_prem", label: "Risk Adj Prem" },
                { value: "quote_prem", label: "Quote Prem" },
              ]}
              with="cit_2_rc_waterfall"
            />
          </HX.Pane>
          <HX.Pane>
            <HX.Table shownBy="/cds/jb_masking"
              title="Rate Change Calculations"
              data={["jb_1_rc_tech", "jb_2_rc_tech", "jb_3_rc_tech"]}
              fields={[
                "subcategory", "prem_ly",
                "prem_exp_ly", "prem_exp_ty", "chg_exp", "prem_adj_exp",
                "prem_ded_ly", "prem_ded_ty", "chg_ded", "prem_adj_ded",
                "prem_lim_ly", "prem_lim_ty", "chg_lim", "prem_adj_lim",
                "prem_risk_ly", "prem_risk_ty", "chg_risk", "prem_adj_risk",
                "prem_tc_ly", "prem_tc_ty", "chg_tc", "prem_adj_tc",
                "prem_ty", "rarc"
              ]}
            />
            <HX.Table shownBy="/cds/fa_masking"
              title="Rate Change Calculations"
              data={["fa_1_rc_tech", "fa_2_rc_tech", "fa_3_rc_tech"]}
              fields={[
                "subcategory", "prem_ly",
                "prem_exp_ly", "prem_exp_ty", "chg_exp", "prem_adj_exp",
                "prem_ded_ly", "prem_ded_ty", "chg_ded", "prem_adj_ded",
                "prem_lim_ly", "prem_lim_ty", "chg_lim", "prem_adj_lim",
                "prem_risk_ly", "prem_risk_ty", "chg_risk", "prem_adj_risk",
                "prem_tc_ly", "prem_tc_ty", "chg_tc", "prem_adj_tc",
                "prem_ty", "rarc"
              ]}
            />
            <HX.Table shownBy="/cds/gs_masking"
              title="Rate Change Calculations"
              data={["gs_1_rc_tech", "gs_2_rc_tech", "gs_3_rc_tech", "gs_4_rc_tech"]}
              fields={[
                "subcategory", "prem_ly",
                "prem_exp_ly", "prem_exp_ty", "chg_exp", "prem_adj_exp",
                "prem_ded_ly", "prem_ded_ty", "chg_ded", "prem_adj_ded",
                "prem_lim_ly", "prem_lim_ty", "chg_lim", "prem_adj_lim",
                "prem_risk_ly", "prem_risk_ty", "chg_risk", "prem_adj_risk",
                "prem_tc_ly", "prem_tc_ty", "chg_tc", "prem_adj_tc",
                "prem_ty", "rarc"
              ]}
            />
            <HX.Table shownBy="/cds/cit_masking"
              title="Rate Change Calculations"
              data={["cit_1_rc_tech", "cit_2_rc_tech", "cit_3_rc_tech"]}
              fields={[
                "subcategory", "prem_ly",
                "prem_exp_ly", "prem_exp_ty", "chg_exp", "prem_adj_exp",
                "prem_ded_ly", "prem_ded_ty", "chg_ded", "prem_adj_ded",
                "prem_lim_ly", "prem_lim_ty", "chg_lim", "prem_adj_lim",
                "prem_risk_ly", "prem_risk_ty", "chg_risk", "prem_adj_risk",
                "prem_tc_ly", "prem_tc_ty", "chg_tc", "prem_adj_tc",
                "prem_ty", "rarc"
              ]}
            />
          </HX.Pane>
        </HX.Section>
        <HX.Section title="Underwriter Adjusted Rate Change">
          <HX.Pane>
            <HX.Table shownBy="/cds/jb_masking"
              data={["jb_rc_uwadj"]}
              fields={[
                "prem_ly",
                "prem_exp_ly", "uwinput_exp", "prem_exp_ty", "chg_exp", "prem_adj_exp",
                "prem_ded_ly", "uwinput_ded", "prem_ded_ty", "chg_ded", "prem_adj_ded",
                "prem_lim_ly", "uwinput_lim", "prem_lim_ty", "chg_lim", "prem_adj_lim",
                "prem_risk_ly", "uwinput_risk", "prem_risk_ty", "chg_risk", "prem_adj_risk",
                "prem_tc_ly", "uwinput_tc", "prem_tc_ty", "chg_tc", "prem_adj_tc",
                "prem_ty", "rarc"
              ]}
            />
            <HX.Table shownBy="/cds/fa_masking"
              data={["fa_rc_uwadj"]}
              fields={[
                "prem_ly",
                "prem_exp_ly", "uwinput_exp", "prem_exp_ty", "chg_exp", "prem_adj_exp",
                "prem_ded_ly", "uwinput_ded", "prem_ded_ty", "chg_ded", "prem_adj_ded",
                "prem_lim_ly", "uwinput_lim", "prem_lim_ty", "chg_lim", "prem_adj_lim",
                "prem_risk_ly", "uwinput_risk", "prem_risk_ty", "chg_risk", "prem_adj_risk",
                "prem_tc_ly", "uwinput_tc", "prem_tc_ty", "chg_tc", "prem_adj_tc",
                "prem_ty", "rarc"
              ]}
            />
            <HX.Table shownBy="/cds/gs_masking"
              data={["gs_rc_uwadj"]}
              fields={[
                "prem_ly",
                "prem_exp_ly", "uwinput_exp", "prem_exp_ty", "chg_exp", "prem_adj_exp",
                "prem_ded_ly", "uwinput_ded", "prem_ded_ty", "chg_ded", "prem_adj_ded",
                "prem_lim_ly", "uwinput_lim", "prem_lim_ty", "chg_lim", "prem_adj_lim",
                "prem_risk_ly", "uwinput_risk", "prem_risk_ty", "chg_risk", "prem_adj_risk",
                "prem_tc_ly", "uwinput_tc", "prem_tc_ty", "chg_tc", "prem_adj_tc",
                "prem_ty", "rarc"
              ]}
            />
            <HX.Table shownBy="/cds/cit_masking"
              data={["cit_rc_uwadj"]}
              fields={[
                "prem_ly",
                "prem_exp_ly", "uwinput_exp", "prem_exp_ty", "chg_exp", "prem_adj_exp",
                "prem_ded_ly", "uwinput_ded", "prem_ded_ty", "chg_ded", "prem_adj_ded",
                "prem_lim_ly", "uwinput_lim", "prem_lim_ty", "chg_lim", "prem_adj_lim",
                "prem_risk_ly", "uwinput_risk", "prem_risk_ty", "chg_risk", "prem_adj_risk",
                "prem_tc_ly", "uwinput_tc", "prem_tc_ty", "chg_tc", "prem_adj_tc",
                "prem_ty", "rarc"
              ]}
            />
          </HX.Pane>
          <HX.Pane>
            <HX.Table shownBy="/cds/jb_masking"
              title="Rate Change Calculations"
              data={["jb_1_rc_uwadj", "jb_2_rc_uwadj", "jb_3_rc_uwadj"]}
              fields={[
                "subcategory", "prem_ly",
                "prem_exp_ly", "uwinput_exp", "prem_exp_ty", "chg_exp", "prem_adj_exp",
                "prem_ded_ly", "uwinput_ded", "prem_ded_ty", "chg_ded", "prem_adj_ded",
                "prem_lim_ly", "uwinput_lim", "prem_lim_ty", "chg_lim", "prem_adj_lim",
                "prem_risk_ly", "uwinput_risk", "prem_risk_ty", "chg_risk", "prem_adj_risk",
                "prem_tc_ly", "uwinput_tc", "prem_tc_ty", "chg_tc", "prem_adj_tc",
                "prem_ty", "rarc"
              ]}
            />
            <HX.Table shownBy="/cds/fa_masking"
              title="Rate Change Calculations"
              data={["fa_1_rc_uwadj", "fa_2_rc_uwadj", "fa_3_rc_uwadj"]}
              fields={[
                "subcategory", "prem_ly",
                "prem_exp_ly", "uwinput_exp", "prem_exp_ty", "chg_exp", "prem_adj_exp",
                "prem_ded_ly", "uwinput_ded", "prem_ded_ty", "chg_ded", "prem_adj_ded",
                "prem_lim_ly", "uwinput_lim", "prem_lim_ty", "chg_lim", "prem_adj_lim",
                "prem_risk_ly", "uwinput_risk", "prem_risk_ty", "chg_risk", "prem_adj_risk",
                "prem_tc_ly", "uwinput_tc", "prem_tc_ty", "chg_tc", "prem_adj_tc",
                "prem_ty", "rarc"
              ]}
            />
            <HX.Table shownBy="/cds/gs_masking"
              title="Rate Change Calculations"
              data={["gs_1_rc_uwadj", "gs_2_rc_uwadj", "gs_3_rc_uwadj", "gs_4_rc_uwadj"]}
              fields={[
                "subcategory", "prem_ly",
                "prem_exp_ly", "uwinput_exp", "prem_exp_ty", "chg_exp", "prem_adj_exp",
                "prem_ded_ly", "uwinput_ded", "prem_ded_ty", "chg_ded", "prem_adj_ded",
                "prem_lim_ly", "uwinput_lim", "prem_lim_ty", "chg_lim", "prem_adj_lim",
                "prem_risk_ly", "uwinput_risk", "prem_risk_ty", "chg_risk", "prem_adj_risk",
                "prem_tc_ly", "uwinput_tc", "prem_tc_ty", "chg_tc", "prem_adj_tc",
                "prem_ty", "rarc"
              ]}
            />
            <HX.Table shownBy="/cds/cit_masking"
              title="Rate Change Calculations"
              data={["cit_1_rc_uwadj", "cit_2_rc_uwadj", "cit_3_rc_uwadj"]}
              fields={[
                "subcategory", "prem_ly",
                "prem_exp_ly", "uwinput_exp", "prem_exp_ty", "chg_exp", "prem_adj_exp",
                "prem_ded_ly", "uwinput_ded", "prem_ded_ty", "chg_ded", "prem_adj_ded",
                "prem_lim_ly", "uwinput_lim", "prem_lim_ty", "chg_lim", "prem_adj_lim",
                "prem_risk_ly", "uwinput_risk", "prem_risk_ty", "chg_risk", "prem_adj_risk",
                "prem_tc_ly", "uwinput_tc", "prem_tc_ty", "chg_tc", "prem_adj_tc",
                "prem_ty", "rarc"
              ]}
            />
          </HX.Pane>
        </HX.Section>
      </HX.With>
    </HX.Page>
  )
}

export { vw_rate_change };