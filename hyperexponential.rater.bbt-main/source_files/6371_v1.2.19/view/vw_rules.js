//########### OUTSTANDING ########################
// this does not work...

import ImageComponent from "components/image";

import * as HX from "hx-model-components";


function vw_rules(scale) {
  return (
    <HX.Page title="Rules" /*fullWidth={true}*/>
      <HX.Section title="Image Example">
        <ImageComponent
          title="8-bit Rick Roll Gif"
          src="/workspace/editing/parameter_tables/test.jpg"
        />
      </HX.Section>
    </HX.Page>
  )
}

export { vw_rules };
