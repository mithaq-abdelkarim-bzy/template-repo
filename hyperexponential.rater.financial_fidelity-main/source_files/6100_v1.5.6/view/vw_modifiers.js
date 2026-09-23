/* eslint-disable */
import * as HX from "hx-model-components";

function vw_modifiers() {
  return (
    <HX.Page title="Schedule Rating" shownBy="modifier_flag">
      <HX.Section title="Schedule Rating Modifiers">
        <HX.Table
          data={["audit_procedures", "internal_controls", "management_and_personnel", "classification_peculiarities", null, { datum: "total_modifiers", infoBy: "modifier_label" }]}
          fields={["minimum", "maximum", "selected", "comment"]}
        />
      </HX.Section>
    </HX.Page>
  )
}

export { vw_modifiers };
