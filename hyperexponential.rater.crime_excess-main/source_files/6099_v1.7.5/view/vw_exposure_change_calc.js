import * as HX from "hx-model-components";

function vw_exposure_change_calculation() {
  return (
    <HX.Page title="Exposure Change Calculation">
      <HX.Section title="Exposure Change Calculation">
        <HX.Table
          kb-interactive
          title=""
          data={["cds/exposure_change/employee_count"]}
          fields={[

            "renewal", "expiry"

          ]}
        />
      </HX.Section>
    </HX.Page>
  );
}

export { vw_exposure_change_calculation };