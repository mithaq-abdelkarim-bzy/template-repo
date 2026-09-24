import * as HX from "hx-model-components";

function vw_tpi_calculations(scale) {
  return (
    <HX.Page title="TPI Calculations" fullWidth={true} viewScale={scale} shownBy="/cds/review_type/rater_priced">
      <HX.Section title="Select Option" shownBy="model_state/show_after_landing_page">
        <HX.Pane flow="right">
          <HX.Collection fields={[
            "cds/tpi_calculations/selected_option"
          ]} />
          <HX.Pane /><HX.Pane />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="SCA Frequency">
        <HX.Table
          syncColumnWidthsKey="sync_calcs1"
          title="Risk Information"
          data={[
            "sca_base_frequency",
            "market_cap_factor",
            "ipo_factor"
          ]}
          fields={[
            { field: "value", width: 150 },
            { field: "book_average", width: 150 },
            { field: "comment", width: 600 }
          ]}
          rowHeaderSettings={{ width: 400 }}
          with="cds/tpi_calculations"
        />
        <HX.Pane>
          <HX.Table
            syncColumnWidthsKey="sync_calcs1"
            title="CapIQ"
            data={[
              "minimum_trading_volume_factor",
              "volatility_of_trading_factor",
              "execs_under_age_50_factor",
              "years_in_business_factor",
              null,
              { datum: "capiq_total_factor", infoBy: "capiq_total_factor/info" },
              null,
              "freq_sca_after_capiq"
            ]}
            fields={[
              { field: "value" },
              { field: "book_average" }//,
              //{ field: "comment" }
            ]}
            with="cds/tpi_calculations"
          />
        </HX.Pane>
        <HX.Table
          syncColumnWidthsKey="sync_calcs1"
          title="Modifiers & Overrides"
          data={[
            "freq_sca_after_overrides",
            "freq_sca_after_modifiers"
          ]}
          fields={[
            { field: "value" },
            { field: "book_average" },
            { field: "comment" }
          ]}
          with="cds/tpi_calculations"
        />
      </HX.Section>
      <HX.Section title="SCA Severity">
        <HX.Table
          syncColumnWidthsKey="sync_calcs2"
          //title=""
          data={[
            "ground_up_sca_dismissal",
            "sca_loss_to_layer"
          ]}
          fields={[
            { field: "value", width: 150 },
            { field: "comment", width: 750 }
          ]}
          rowHeaderSettings={{ width: 400 }}
          with="cds/tpi_calculations"
        />
      </HX.Section>
      <HX.Section title="Technical Premium">
        <HX.Table
          syncColumnWidthsKey="sync_calcs2"
          title="Dismissal Rate"
          data={[
            "sca_dismissal_rate"
          ]}
          fields={[
            { field: "value" },
            { field: "comment" }
          ]}
          with="cds/tpi_calculations"
        />
        <HX.Table
          shownBy="is_abc"
          syncColumnWidthsKey="sync_calcs2"
          title="Loss Cost"
          data={[
            { datum: "sca_loss_cost", infoBy: "sca_loss_cost/info" },
            "non_sca_loss_cost",
            "cat_load",
            null,
            { datum: "abc_loss_cost", infoBy: "abc_loss_cost/info" }
          ]}
          fields={[
            { field: "value" },
            { field: "comment" }
          ]}
          with="cds/tpi_calculations"
        />
        {/* <HX.Table
          shownBy="is_side_a"
          syncColumnWidthsKey="sync_calcs1"
          title="Loss Cost"
          data={[
            "sca_loss_cost",
            "non_sca_loss_cost",
            "cat_load",
            null,
            "dic_adjustment",
            "bankruptcy_load",
            null,
            { datum: "side_a_loss_cost", infoBy: "side_a_loss_cost/info" }
          ]}
          fields={[
            { field: "value" },
            { field: "book_average" },
            { field: "comment" }
          ]}
          with="cds/tpi_calculations"
        /> */}
        <HX.Table
          shownBy="is_side_a"
          syncColumnWidthsKey="sync_calcs2"
          title="Loss Cost"
          data={[
            { datum: "sca_loss_cost", infoBy: "sca_loss_cost/info" },
            "non_sca_loss_cost",
            "cat_load"
          ]}
          fields={[
            { field: "value" }
          ]}
          with="cds/tpi_calculations"
        />
        <HX.Table
          shownBy="is_side_a"
          syncColumnWidthsKey="sync_calcs1"
          title="Side A Factors"
          data={[
            "dic_adjustment",
            "bankruptcy_load"
          ]}
          fields={[
            { field: "value" },
            { field: "book_average" }
          ]}
          with="cds/tpi_calculations"
        />
        <HX.Table
          shownBy="is_side_a"
          syncColumnWidthsKey="sync_calcs2"
          title="Total Loss Cost"
          data={[
            { datum: "side_a_loss_cost", infoBy: "side_a_loss_cost/info" }
          ]}
          fields={[
            { field: "value" },
            { field: "comment" }
          ]}
          with="cds/tpi_calculations"
        />
        <HX.Pane>
          <HX.Table
            syncColumnWidthsKey="sync_calcs2"
            title="TPI"
            data={[
              "net_premium",
              { datum: "profit", infoBy: "profit/info" },
              { datum: "roc", infoBy: "roc/info" },
              { datum: "technical_premium", infoBy: "technical_premium/info" },
              { datum: "tpi", infoBy: "tpi/info" }
            ]}
            fields={[
              { field: "value" }
              //{ field: "comment" }
            ]}
            with="cds/tpi_calculations"
          />
          <HX.Pane flow="right">
            <HX.Notes
              //title="Plan Metrics"
              field="cds/tpi_calculations/net_premium/comment"
            //stretch
            />
            <HX.Pane />
          </HX.Pane>
        </HX.Pane>
      </HX.Section>
    </HX.Page >
  )
}

export { vw_tpi_calculations };