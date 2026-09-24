/* eslint-disable */
import * as HX from "hx-model-components";

function HXModel() {
  return (
    // Your model code goes here
    <HX.Root>
      <HX.Page>
        <HX.Section title="My fields v1.5.10">
          <HX.Pane>
            <HX.Collection fields={["a", "b", "c", "j", "k"]} />
          </HX.Pane>
        </HX.Section>
      </HX.Page>
    </HX.Root>
  );
}

export default HXModel;
