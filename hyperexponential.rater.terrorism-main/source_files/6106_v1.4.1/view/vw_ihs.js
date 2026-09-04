import * as HX from "hx-model-components";


function vw_ihs() {
  return (
    <HX.Page title="IHS API">
      <HX.Section title="My fields">
        <HX.Pane>
          <HX.Table data={["countries"]} fields={["country"]} />
          <HX.Button title="Fetch IHS Data" task="task_fetch_ihs_data" />
          <HX.Notes field="ihs_data" />
        </HX.Pane>
      </HX.Section>
    </HX.Page>
  )
}

export { vw_ihs };
