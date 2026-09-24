// # v0.5.1
import * as HX from "hx-model-components";

function vw_steer_exposure_rating_curve_descriptions(scale) {
  return (
    <HX.Page title="Curve Descriptions" viewScale={scale} shownBy="model_state/show_steer_risk_bdx">
      <HX.Section title="All Curves">
        <HX.Pane>
          <HX.Table
            // title=""
            with="steer/exposure_rating/curve_descriptions"
            data={[
              // { datum: "all_curves", width: 250 }
              data = "all_curves"
            ]}
            fields={[
              "description",
              "parametric",
              "curve_description",
              "source"

            ]}

            kb-interactive
            dynamic // filter and sort
          // transpose
          />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Commercial Auto State Groupings">
        <HX.Pane>
          <HX.Table
            // title=""
            with="steer/exposure_rating/curve_descriptions"
            data={[
              // { datum: "all_curves", width: 250 }
              data = "commercial_auto_state"
            ]}
            fields={[
              "group_1",
              "group_2",
              "group_3",
              "group_4",
              "group_5",
              "group_6",
              "group_7",
              "group_8",
            ]}

            kb-interactive
            dynamic // filter and sort
          // transpose
          />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Cyber Groupings">
        <HX.Pane>
          <HX.Table
            // title=""
            with="steer/exposure_rating/curve_descriptions"
            data={[
              // { datum: "all_curves", width: 250 }
              data = "cyber"
            ]}
            fields={[
              "low",
              "high",

            ]}

            kb-interactive
            dynamic // filter and sort
          // transpose
          />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Healthcare Groupings">
        <HX.Pane>
          <HX.Table
            // title=""
            with="steer/exposure_rating/curve_descriptions"
            data={[
              // { datum: "all_curves", width: 250 }
              data = "healthcare"
            ]}
            fields={[
              "low",
              "medium",
              "medium_high",
              "high",
              "very_high"

            ]}

            kb-interactive
            dynamic // filter and sort
          // transpose
          />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Private D&O Groupings">
        <HX.Pane>
          <HX.Table
            // title=""
            with="steer/exposure_rating/curve_descriptions"
            data={[
              // { datum: "all_curves", width: 250 }
              data = "private_d_o"
            ]}
            fields={[
              "low",
              "medium",
              "high",
              "very_high"

            ]}

            kb-interactive
            dynamic // filter and sort
          // transpose
          />
        </HX.Pane>
      </HX.Section>
    </HX.Page>
  )
}

export { vw_steer_exposure_rating_curve_descriptions };