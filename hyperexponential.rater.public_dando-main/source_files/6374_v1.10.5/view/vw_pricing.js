import * as HX from "hx-model-components";
import Slider from "components/slider";
import ExpandableEditableText from "components/text_box_expandable";
import ModalNotesEditor from "components/modal_notes_editor";
import DivConfig from "components/divs";


function vw_pricing(scale) {
  return (
    <HX.Page title="Pricing" fullWidth={true} viewScale={scale} shownBy="model_state/show_after_landing_page">

      <HX.Section title="Modifiers" shownBy="/cds/review_type/rater_priced">
        <HX.Pane flow='right'>
          <HX.Pane ratio={2}>
            {/* <DivConfig mindWidth="900px"> */}
            <HX.Table
              syncColumnWidthsKey="sync_modifiers"
              data={[
                {
                  datum: "management_corp_gov",
                  labelBy: "/non_cds/modifier_labels/management_corp_gov"
                },
                {
                  datum: "business_financial_model_factors",
                  labelBy: "/non_cds/modifier_labels/business_financial_model_factors"
                },
                {
                  datum: "significant_event_factors",
                  labelBy: "/non_cds/modifier_labels/significant_event_factors"
                },
                {
                  datum: "stock_market_factors",
                  labelBy: "/non_cds/modifier_labels/stock_market_factors"
                },
                {
                  datum: "regulatory",
                  labelBy: "/non_cds/modifier_labels/regulatory"
                },
                // "management_corp_gov",
                // "business_financial_model_factors",
                // "significant_event_factors",
                // "stock_market_factors",
                // "regulatory",
                null,
                "freq_adj_factor",
                null,
                {
                  datum: "obj_freq_adj_factor",
                  infoBy: "obj_freq_adj_factor/info",
                },
                null,
                "total_freq_adj_factor"]}
              fields={[
                { field: "value", width: 100 },
                { field: "min", width: 100 },
                { field: "max", width: 100 },
                { field: "comment_plain_text", width: 200 },
                //{ field: "comment", width: 200 },
                // { field: "show_comment", maxWidth: 120 },
              ]}
              rowHeaderSettings={{ width: 350 }}
              with="cds/modifiers"
              kb-interactive
            />
            {/* </DivConfig> */}
          </HX.Pane>
          <HX.Pane flow='down'>
            <ModalNotesEditor
              notesPath="cds/modifiers/management_corp_gov/comment"
              plainTextPath="cds/modifiers/management_corp_gov/comment_plain_text"
              label="Management and Corporate Governance Comment"
              width="400px"
              marginTop="55px"
              marginBottom="4px"
              autosave={true}
            />
            <ModalNotesEditor
              notesPath="cds/modifiers/business_financial_model_factors/comment"
              plainTextPath="cds/modifiers/business_financial_model_factors/comment_plain_text"
              label="Business / Financial Model Factors Comment"
              width="400px"
              marginTop="4px"
              marginBottom="4px"
              autosave={true}
            />
            <ModalNotesEditor
              notesPath="cds/modifiers/significant_event_factors/comment"
              plainTextPath="cds/modifiers/significant_event_factors/comment_plain_text"
              label="Significant Event Factors Comment"
              width="400px"
              marginTop="4px"
              marginBottom="4px"
              autosave={true}
            />
            <ModalNotesEditor
              notesPath="cds/modifiers/stock_market_factors/comment"
              plainTextPath="cds/modifiers/stock_market_factors/comment_plain_text"
              label="Stock Market Factors Comment"
              width="400px"
              marginTop="4px"
              marginBottom="4px"
              autosave={true}
            />
            <ModalNotesEditor
              notesPath="cds/modifiers/regulatory/comment"
              plainTextPath="cds/modifiers/regulatory/comment_plain_text"
              label="Regulatory Comment"
              width="400px"
              marginTop="4px"
              marginBottom="4px"
              autosave={true}
            />
          </HX.Pane>
        </HX.Pane>
        <HX.Pane>
          <HX.Collection
            syncColumnWidthsKey="sync_modifiers"
            fields={[
              "sca_model_freq",
              "sca_freq_override",
              "sca_used_freq",
            ]} with="cds/frequency" />
        </HX.Pane>
        <HX.Pane flow='right'>
          <HX.Pane ratio={2}>
            <HX.Table
              syncColumnWidthsKey="sync_modifiers"
              data={[{ datum: "derivative", labelBy: "/non_cds/modifier_labels/derivative" },
              { datum: "ma", infoBy: "ma/info" }]}
              fields={[
                { field: "value", width: 100 },
                { field: "min", width: 100 },
                { field: "max", width: 100 },
                { field: "comment_plain_text", width: 120 },
              ]}
              with="cds/modifiers"
              kb-interactive
            />
          </HX.Pane>
          <HX.Pane>
            <ModalNotesEditor
              notesPath="cds/modifiers/derivative/comment"
              plainTextPath="cds/modifiers/derivative/comment_plain_text"
              label="Derivative Comment"
              width="400px"
              marginTop="55px"
              marginBottom="4px"
              autosave={true}
            />
            <ModalNotesEditor
              notesPath="cds/modifiers/ma/comment"
              plainTextPath="cds/modifiers/ma/comment_plain_text"
              label="M&A Comment"
              width="400px"
              marginTop="4px"
              marginBottom="4px"
              autosave={true}
            />
          </HX.Pane>
        </HX.Pane>
        <HX.Pane>
          <HX.Collection
            syncColumnWidthsKey="sync_modifiers"
            fields={[
              "d_used_freq",
              "ma_used_freq",
              "total_freq",
            ]} with="cds/frequency" />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Coverage">
        <HX.Pane>
          <HX.Table
            syncColumnWidthsKey="sync_layers"
            data={[{ datum: "cds/layers", minWidth: 175, maxWidth: 250 }]}
            fields={[
              "status"
            ]}
            rowHeaderSettings={{ width: 250 }}
            transpose
            // shownBy="cds/is_abc"
            kb-interactive
          />
        </HX.Pane>
        <HX.Pane>
          <HX.Table
            syncColumnWidthsKey="sync_layers"
            data={[{ datum: "cds/layers", minWidth: 175, maxWidth: 250 }]}
            fields={[
              // Layering
              "coverages/abc/limit",
              "coverages/abc/excess",
              "coverages/abc/deductible",
              "coverages/abc/ma_retention",
              null,
              // Premium info
              "coverages/abc/premium",
              // { field: "runoff_adjustment", shownBy: "cds/is_runoff", infoBy: "cds/runoff_adjustment_info" },
              // { field: "runoff_original_premium", shownBy: "cds/is_runoff" },
              "coverages/abc/written_line",
              "coverages/abc/quoted_market_share",
              "coverages/abc/brokerage",
              null,
              // Rating outputs
              { field: "coverages/abc/benchmark_premium", shownBy: "/cds/review_type/rater_priced" },
              { field: "coverages/abc/elr", shownBy: "/cds/review_type/rater_priced" },
              { field: "coverages/abc/bpi", shownBy: "/cds/review_type/rater_priced" },
              { field: "coverages/abc/technical_premium", shownBy: "/cds/review_type/rater_priced" },
              { field: "coverages/abc/tpi", shownBy: "/cds/review_type/rater_priced" },
              { field: "coverages/abc/roc", shownBy: "/cds/review_type/rater_priced" },

              // these are for when the rater is case priced or private priced
              { field: "coverages/abc/private_priced/benchmark_premium", shownBy: "/cds/review_type/private_priced" },
              { field: "coverages/abc/private_priced/bpi", shownBy: "/cds/review_type/private_priced" },
              { field: "coverages/abc/private_priced/technical_premium", shownBy: "/cds/review_type/private_priced" },
              { field: "coverages/abc/private_priced/tpi", shownBy: "/cds/review_type/private_priced" },
              null,
              // Percentiles
              { field: "coverages/abc/at_cost_75", shownBy: "/cds/review_type/rater_priced" },
              { field: "coverages/abc/incl_dimissals_75", shownBy: "/cds/review_type/rater_priced" },
              { field: null, shownBy: "/cds/review_type/rater_priced" },
              // Tags
              "coverages/abc/selected"
            ]}
            title="Options"
            rowHeaderSettings={{ width: 250 }}
            transpose
            shownBy="cds/is_abc"
            kb-interactive
          />
          <HX.Table
            syncColumnWidthsKey="sync_layers"
            data={[{ datum: "cds/layers", minWidth: 175, maxWidth: 250 }]}
            fields={[
              // Layering
              "coverages/side_a/limit",
              "coverages/side_a/excess",
              "coverages/side_a/tower",
              "coverages/side_a/total_excess",
              "coverages/side_a/deductible",
              "coverages/side_a/director_limit",
              null,
              // Premium info
              "coverages/side_a/premium",
              // { field: "runoff_adjustment", shownBy: "cds/is_runoff", infoBy: "cds/runoff_adjustment_info" },
              // { field: "runoff_original_premium", shownBy: "cds/is_runoff" },
              "coverages/side_a/written_line",
              "coverages/side_a/quoted_market_share",
              "coverages/side_a/brokerage",
              "coverages/side_a/non_rescindable_coverage",
              null,
              // Rating outputs
              { field: "coverages/side_a/benchmark_premium", shownBy: "/cds/review_type/rater_priced" },
              { field: "coverages/side_a/elr", shownBy: "/cds/review_type/rater_priced" },
              { field: "coverages/side_a/bpi", shownBy: "/cds/review_type/rater_priced" },
              { field: "coverages/side_a/technical_premium", shownBy: "/cds/review_type/rater_priced" },
              { field: "coverages/side_a/tpi", shownBy: "/cds/review_type/rater_priced" },
              { field: "coverages/side_a/roc", shownBy: "/cds/review_type/rater_priced" },


              // these are for when the rater is case priced or private priced
              { field: "coverages/side_a/private_priced/benchmark_premium", shownBy: "/cds/review_type/private_priced" },
              { field: "coverages/side_a/private_priced/bpi", shownBy: "/cds/review_type/private_priced" },
              { field: "coverages/side_a/private_priced/technical_premium", shownBy: "/cds/review_type/private_priced" },
              { field: "coverages/side_a/private_priced/tpi", shownBy: "/cds/review_type/private_priced" },
              null,
              // Percentiles
              { field: "coverages/side_a/at_cost_75", shownBy: "/cds/review_type/rater_priced" },
              { field: "coverages/side_a/incl_dimissals_75", shownBy: "/cds/review_type/rater_priced" },
              { field: null, shownBy: "/cds/review_type/rater_priced" },
              // Tags
              "coverages/side_a/selected"
            ]}
            title="Options"
            rowHeaderSettings={{ width: 250 }}
            transpose
            shownBy="cds/is_side_a"
            kb-interactive
          />
          <HX.Pane flow="right">
            <HX.Button task="generate_tags_cuap" title="Save Tags" />
            <HX.Collection fields={[null]} />
            <HX.Collection fields={[null]} />
            <HX.Collection fields={[null]} />
          </HX.Pane>
          <HX.Pane flow="right">
            <HX.Collection fields={["cds/policy_tag_error"]} shownBy="cds/is_policy_tag_error" horizontal />
            <HX.Collection fields={[null]} />
            <HX.Collection fields={[null]} />
            <HX.Collection fields={[null]} />
          </HX.Pane>
          <HX.Collection
            syncColumnWidthsKey="sync_layers"
            fields={["cds/entity_investigation"]}
          //shownBy="cds/is_abc"
          />
          <HX.Table
            syncColumnWidthsKey="sync_layers"
            data={[{ datum: "cds/layers" }]}
            fields={["ei_limit", "ei_price"]}
            transpose
            shownBy="cds/entity_investigation"
            kb-interactive
          />
          <HX.Collection
            syncColumnWidthsKey="sync_layers"
            fields={["cds/bridge_countries"]}
          />
          <HX.Table
            data={[{ datum: "cds/bridge_country" }]}
            fields={[
              { field: "country", width: 200 },
              { field: "premium", width: 200 }
            ]}
            shownBy="cds/bridge_countries"
            kb-interactive
          />
          <HX.Collection
            syncColumnWidthsKey="sync_layers"
            fields={["cds/bridge_premium", "cds/bridge_comment"]}
            shownBy="cds/bridge_countries"
          />
        </HX.Pane>
      </HX.Section>
    </HX.Page >
  )
}

export { vw_pricing };