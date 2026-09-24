import * as HX from "hx-model-components";
import CollapsibleSchemaViewer from "components/schema_view";

function SchemaViewPage() {
  return (
    <HX.Page title="JSON View" shownBy="model_state/show_json_view">
      <HX.Section>
        <CollapsibleSchemaViewer
          title="Schema Viewer"
          stringifiedJsonPath="schema_view/stringified_json"
          shownBy="schema_view/show_view"
        />
      </HX.Section>
    </HX.Page>
  )
}

export default SchemaViewPage;