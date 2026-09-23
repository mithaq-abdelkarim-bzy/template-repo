import * as HX from "hx-model-components";

function vw_landing_page() {
  // return (
  //   // <HX.Page title="Landing Page" shownBy="model_state/show_landing_page" >
  //   <HX.Page title="Landing Page" shownBy="model_state/show_initialisation_page" >
  //     <HX.Section title="Start Renewal">
  //       <HX.Pane>
  //         <HX.Button task="initialise_model" title="Initialise Model" />
  //       </HX.Pane>
  //       <HX.Pane>
  //         <HX.Collection fields={[{ field: "model_state/landing_page_info" }]} />
  //       </HX.Pane>
  //       <HX.Pane flow="right">
  //         <HX.Pane>
  //           {/* <HX.Button task="roll_exposure_fields_task" title="Roll Forward Exposure Fields" /> */}
  //           <HX.Button task="start_renewal_task" title="Start Model" />
  //         </HX.Pane>
  //         <HX.Pane />
  //         <HX.Pane />
  //       </HX.Pane>
  //     </HX.Section>
  //   </HX.Page >
  // )
  return (
    // <HX.Page title="Landing Page" shownBy="model_state/show_landing_page" >
    <HX.Page title="Landing Page" shownBy="model_state/show_initialisation_page" >
      <HX.Section title="Initialise Model">



        <HX.Pane shownBy="model_state/show_landing_page">
          {/* <HX.Pane> */}
          <HX.Collection fields={[{ field: "model_state/landing_page_info" }]} />
        </HX.Pane>

        <HX.Pane flow="right" shownBy="model_state/show_initialise_model_button">
          <HX.Pane>
            <HX.Button task="initialise_model" title="Initialise Model" />
          </HX.Pane>
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>

        {/* <HX.Pane flow="right" shownBy="model_state/show_landing_page">
          <HX.Pane>
            <HX.Button task="start_renewal_task" title="Start Model" />
          </HX.Pane>
          <HX.Pane />
          <HX.Pane />
        </HX.Pane> */}

      </HX.Section>
    </HX.Page >
  )
}

export { vw_landing_page };