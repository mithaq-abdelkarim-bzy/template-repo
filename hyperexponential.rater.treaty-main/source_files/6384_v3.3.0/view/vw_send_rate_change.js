import * as HX from "hx-model-components";

function vw_send_rate_change(scale) {
  return (
    <HX.Page title="Send Rate Change" fullWidth={false} viewScale={scale} shownBy="model_state/show_after_landing_page">
      <HX.Section title="Send Rate Change Override">
        <HX.Pane>
          <HX.Notes
            field="cds/send_rate_change/message"
          />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Rate Change" shownBy="cds/send_rate_change/show_send_rate_change">
        <HX.Pane>
          <HX.Collection fields={[
            "synergy_upload/rate_change/email_recipients"
          ]} />
          <HX.Button task="synergy_send_rate_change_task"
            title="Send Rate Change" />
        </HX.Pane>
      </HX.Section>
    </HX.Page>
  )
}

export { vw_send_rate_change };