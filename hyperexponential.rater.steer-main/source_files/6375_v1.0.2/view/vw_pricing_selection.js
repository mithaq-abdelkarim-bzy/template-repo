// # v0.5.1
import * as HX from "hx-model-components";
import { add_prefix_to_list } from "view/vw_utilities";

function convertToFieldObjects(originalList) {
  return originalList.map(item => {
    if (item === null) {
      return null;
    }
    return { field: item, maxWidth: 150 };
  });
}

const pricing_assumptions_fields = [
  "limit",
  "excess",
  "epi",
]

const final_selection_fields = [
  "total_weighting",
  "plr_method",
  "pure_rate",
  "pure_premium",
  "pure_rol",
]

const exposure_method_fields = [
  "cedant_loss_ratio",
  "pure_rate",
  "pure_premium",
  "pure_rol",
  "weighting"
]

const method_fields = [
  "pure_rate",
  "pure_premium",
  "pure_rol",
  "weighting"
]


const params_fields = [
  "default",
  "overwrite",
  "selected"
]

function vw_pricing_selection(scale) {
  return (
    <HX.Page title="Pricing Selection" viewScale={scale} shownBy="model_state/show_rater_priced" >

      <HX.Section title="Pricing Selection">
        <HX.Pane>
          <HX.Pane flow="right" reflow={false}>
            <HX.Pane ratio={5}>
              <HX.Table
                title="Pricing assumptions"
                with="cds"
                data={[
                  { datum: "layers", width: 220 }
                ]}
                fields={[
                  "status",
                  "currency",
                  "limit",
                  "excess",
                  "epi_100",
                ]}
                kb-interactive
                rowHeaderSettings={{ width: 170 }}
                transpose
              />
            </HX.Pane>
            <HX.Pane ratio={2}>

              <HX.Table
                title="COB Assumptions"
                with="cds/pricing_selection"
                data={[
                  "pareto_parameters",
                  "odf_parameters",
                ]}
                fields={[
                  ...convertToFieldObjects(params_fields)
                ]}
                kb-interactive
                rowHeaderSettings={{ width: 170 }}
              />
              <HX.Notes field="/model_state/pure_premium_error_message" shownBy="/model_state/is_pure_premium_not_calculated" />

              <HX.Button task="advanced_features_task" title="Calculate Advanced Features" />
            </HX.Pane>

          </HX.Pane>
          <HX.Pane>
            <HX.Table
              title="Final Selection"
              with="cds"
              data={[{ datum: "layers", width: 220 }]}
              fields={[
                ...add_prefix_to_list("pricing_selection/final_selection/", final_selection_fields)
              ]}
              kb-interactive
              rowHeaderSettings={{ width: 170 }}
              transpose
            />
          </HX.Pane>

        </HX.Pane>

      </HX.Section>

      <HX.Section title="Detailed (exc. Advanced Features)">
        {/* <HX.Table
          title="Risk Profiles Banded (Exposure)"
          with="cds"
          data={[{ datum: "layers", width: 220 }]}
          fields={[
            ...add_prefix_to_list("pricing_selection/risk_profile_banded/", exposure_method_fields)
          ]}
          kb-interactive
          rowHeaderSettings={{ width: 170 }}
          transpose
        /> */}

        <HX.Table
          title="Risk Profiles Bdx (Exposure)"
          with="cds"
          shownBy="/model_state/show_steer_risk_bdx"
          data={[{ datum: "layers", width: 220 }]}
          fields={[
            ...add_prefix_to_list("pricing_selection/risk_profile_bdx/", exposure_method_fields)
          ]}
          kb-interactive
          rowHeaderSettings={{ width: 170 }}
          transpose
        />

        <HX.Table
          title="Burning Cost (Experience)"
          with="cds"
          shownBy="/model_state/show_steer_experience_rating"
          data={[{ datum: "layers", width: 220 }]}
          fields={[
            ...add_prefix_to_list("pricing_selection/burning_cost/", method_fields)
          ]}
          kb-interactive

          rowHeaderSettings={{ width: 170 }}
          transpose
        />
        <HX.Table
          title="LAS (Exposure)"
          with="cds"
          shownBy="/model_state/show_steer_las_bdx"
          data={[{ datum: "layers", width: 220 }]}
          fields={[
            ...add_prefix_to_list("pricing_selection/limit_average_severity/", method_fields)
          ]}
          kb-interactive
          rowHeaderSettings={{ width: 170 }}
          transpose
        />

        <HX.Table
          title="Clash Rater *** Pending Implementation ***"
          with="cds"
          shownBy="/model_state/is_clash"
          data={[{ datum: "layers", width: 220 }]}
          fields={[
            ...add_prefix_to_list("pricing_selection/clash/", method_fields)
          ]}
          kb-interactive
          rowHeaderSettings={{ width: 170 }}
          transpose
        />

        <HX.Table
          title="Healthcare CAT Rater"
          with="cds"
          shownBy="/model_state/is_healthcare_cat"
          data={[{ datum: "layers", width: 220 }]}
          fields={[
            ...add_prefix_to_list("pricing_selection/healthcare_cat/", method_fields)
          ]}
          kb-interactive
          rowHeaderSettings={{ width: 170 }}
          transpose
        />
        <HX.Table
          title="Other"
          with="cds"
          shownBy="/model_state/is_not_clash"
          data={[{ datum: "layers", width: 220 }]}
          fields={[
            ...add_prefix_to_list("pricing_selection/other_method/", method_fields)
          ]}
          kb-interactive
          rowHeaderSettings={{ width: 170 }}
          transpose
        />

        <HX.Table
          title="Other (Clash Manual Input)"
          shownBy="/model_state/is_clash"
          with="cds"
          data={[{ datum: "layers", width: 220 }]}
          fields={[
            ...add_prefix_to_list("pricing_selection/other_method/", method_fields)
          ]}
          kb-interactive
          rowHeaderSettings={{ width: 170 }}
          transpose
        />

        <HX.Notes field="/cds/other_method_rationale" title="Other Method Rationale" />

      </HX.Section>


    </HX.Page>
  )
}

export { vw_pricing_selection };