//########### OUTSTANDING ########################
// Needs a shownby criteria 




import * as HX from "hx-model-components";

function vw_ihs(scale) {
  return (
    <HX.Page title="IHS Information" fullWidth={true} shownBy="cds/show_hide/page/show_ihs">


      <HX.Section title="IHS Dataframe" >
        <HX.Collection
          fields={[
            "last_run_status"
            , "last_run_date"
            , "last_run_value"
            , "calc_run_value"
            , "check_run_consistent"
          ]}
          with="cds/ihs"
          horizontal
        />

        <HX.Button title="Load IHS Data" task="task_api_ihs_data" />


        <HX.Pane flow="right">
          <HX.Table
            title="IHS Outlook"
            data={["cds/ihs/ihs_outlook"]}
            fields={[
              { field: 'country', maxWidth: 100 }
              , { field: 'risk_name', maxWidth: 250 }
              , { field: 'outlook', maxWidth: 120 }
              , { field: 'outlook_description', maxWidth: 500 }
              , { field: 'last_updated_date', maxWidth: 200 }
              , { field: 'last_updated_value', maxWidth: 200 }
            ]}
            maxListVisibleRows={15}
            kb-interactive
            dynamic
          />

          <HX.Table
            title="IHS Historic Values"
            data={["cds/ihs/ihs_detail"]}
            fields={[
              { field: 'country', maxWidth: 100 }
              , { field: 'risk_name', maxWidth: 250 }
              , { field: 'historic_updated_date', maxWidth: 200 }
              , { field: 'historic_updated_value', maxWidth: 200 }
            ]}
            maxListVisibleRows={15}
            kb-interactive
            dynamic
          />
        </HX.Pane>
      </HX.Section>


    </HX.Page>
  )
}

export { vw_ihs };
