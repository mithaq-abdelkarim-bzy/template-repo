
throw new Error(`This file is generated

Do not edit manually as all of the changes will be lost.
This is the static version of your View that will allow easier debugging.
`);

import * as HX from "hx-model-components";


function hx_calculation_legacy_initial_premium_view(props) {
  return (
    <HX.Root>
      <HX.Page>
        <HX.Section title="My fields v1.5.10">
          <HX.Pane>
            <HX.Collection fields={[
              "a",
              "b",
              "c",
              "j",
              "k"
            ]} />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
    </HX.Root>
  );
}

export default {
  hx_calculation_legacy_initial_premium: hx_calculation_legacy_initial_premium_view,
};