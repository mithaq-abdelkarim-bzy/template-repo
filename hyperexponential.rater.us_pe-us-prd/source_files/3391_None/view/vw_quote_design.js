import * as HX from "hx-model-components";
import { get_quote_options, get_quotes } from "view/vw_constants";

function vw_quote_design(scale) {
  return (
    <HX.Page title="Quote Design" fullWidth={false} viewScale={scale}>
      <HX.With context={{ type: "struct", path: "cds/quote_design" }}>
        <HX.Section title="">
          <HX.Pane flow="right">
            <HX.Collection fields={["retro_date"]} />
          </HX.Pane>
          <HX.Pane flow="down">
            <HX.Table
              data={get_quotes()}
              fields={[
                {
                  field: "coverage_option",
                  labelBy: "coverage_options_label",
                },
                { field: "comment", labelBy: "comments_label" },
              ]}
            //kb-interactive
            //dynamic // filter and sort            
            />
            <HX.Collection fields={["overall_comments", {field: "is_e_cigarettes_check/value", shownBy: "is_e_cigarettes_check/show"}]} />
            <HX.Button title="Generate Email" task="generate_email" />
          </HX.Pane>
        </HX.Section>
      </HX.With>
    </HX.Page >
  );
}

export { vw_quote_design };
