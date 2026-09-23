import * as HX from "hx-model-components";
import ChoroplethMap from "components/choropleth";

const capitalize = (str) => {
  if (typeof str !== 'string') return '';
  return str.charAt(0).toUpperCase() + str.slice(1);
};

function ChoroplethPage(List, Text) {
  return (
    <HX.Page title={"SI Map by " + capitalize(Text)} fullWidth shownBy="cds/exposure/granular/show_exposure_map">
      <HX.Section title={"Exposure by " + capitalize(Text)}>
        <HX.With context={{ type: "struct", path: "cds/exposure/granular" }}>
          <HX.Pane>
            <ChoroplethMap
              title={"Total Sum Insured by " + capitalize(Text)}
              list={List}
              text={Text}
              locations="country_iso3"
              z="total_sum_insured"
            />
          </HX.Pane>
        </HX.With>
      </HX.Section>
    </HX.Page >
  );
}

export default ChoroplethPage;
