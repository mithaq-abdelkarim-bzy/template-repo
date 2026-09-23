import * as HX from "hx-model-components";
import { venue_us, venue_international } from "view/vw_constants";

function vw_venue_factors(scale) {
  return (
    <HX.Page title="Venue Factors" fullWidth={true} viewScale={scale}>

      {/* For single venue selection */}

      <HX.Section title="Venue Factors">
        <HX.Pane flow="right">
          <HX.Button task="venue_factors_select_all" title="Select All Venues" />
          {/* <HX.Button task="venue_factors_calculate_selected" title="Calculate Selected Venues" />
          <HX.Button task="venue_factors_override_flag" title="Update Override Flag" /> */}
          <HX.Button task="venue_calculation_with_override" title="Calculate Selected Venues" />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Collection fields={["cds/exposure/aggregate/total_venue_factor"]} />
        </HX.Pane>

        <HX.Pane flow="right">
          <HX.Button task="venue_factors_clear_all" title="Clear All Venues" />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Collection fields={["cds/exposure/aggregate/total_venue_international_factor"]} shownBy="/cds/international_masking" />
          <HX.Collection fields={["cds/exposure/aggregate/total_venue_us_factor"]} shownBy="/cds/us_masking" />
          <HX.Collection fields={["cds/exposure/aggregate/total_percentage_selected"]} />
        </HX.Pane>

        <HX.Pane>
          <HX.Table shownBy="/cds/us_masking"
            syncColumnWidthsKey="mySyncedTables1"
            data={venue_us()}
            // fields={["override_flag", "percentage_output_copy", "percentage_async_copy", "factor", "percentage", "selection"]}
            fields={[{ field: "factor", maxWidth: 300 },
            { field: "percentage", maxWidth: 300 },
            // { field: "percentage.mandatory", maxWidth: 300, shownBy:"percentage_complete" }, // IR: note that     shownBy: { field: "percentage_complete" }    does not work either :(
            { field: "selection", maxWidth: 300 }]}
            title="US Venue Factors"
            with="cds/exposure/granular"
            kb-interactive
          />
        </HX.Pane>

        <HX.Pane flow="right">
          <HX.Collection fields={["cds/exposure/granular/include_international_venues"]} shownBy="/cds/us_masking" />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>

        <HX.Pane >
          <HX.Table shownBy="/cds/international_masking"
            syncColumnWidthsKey="mySyncedTables1"
            data={venue_international()}
            fields={[{ field: "factor", maxWidth: 300 },
            { field: "percentage", maxWidth: 300 },
            // { field: "percentage.mandatory", maxWidth: 300, shownBy: "percentage_complete" },
            { field: "selection", maxWidth: 300 }]}
            title="International Venue Factors"
            with="cds/exposure/granular"
            kb-interactive
          />
        </HX.Pane>

        <HX.Pane flow="right">
          <HX.Collection fields={["cds/exposure/granular/include_us_venues"]} shownBy="/cds/international_masking" />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
        </HX.Pane>

        {/* Now add in the options if they include international or us with the initial selection */}
        <HX.Pane >

          <HX.Pane flow="right">
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Collection fields={["cds/exposure/aggregate/total_venue_international_factor"]} shownBy="/cds/us_and_international_masking" />

          </HX.Pane>

          <HX.Table shownBy="/cds/us_and_international_masking"
            syncColumnWidthsKey="mySyncedTables1"
            data={venue_international()}
            // fields={["override_flag", "percentage_output_copy", "percentage_async_copy", "factor", "percentage", "selection"]}
            fields={[{ field: "factor", maxWidth: 300 },
            { field: "percentage", maxWidth: 300 },
            { field: "selection", maxWidth: 300 }]}
            title="International Venue Factors"
            with="cds/exposure/granular"
            kb-interactive
          />
        </HX.Pane>

        <HX.Pane flow="right">
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Pane />
          <HX.Collection fields={["cds/exposure/aggregate/total_venue_us_factor"]} shownBy="/cds/international_and_us_masking" />

        </HX.Pane>
        <HX.Pane>
          <HX.Table shownBy="/cds/international_and_us_masking"
            syncColumnWidthsKey="mySyncedTables1"
            data={venue_us()}
            fields={[{ field: "factor", maxWidth: 300 },
            { field: "percentage", maxWidth: 300 },
            { field: "selection", maxWidth: 300 }]}
            title="US Venue Factors"
            with="cds/exposure/granular"
          />
        </HX.Pane>

      </HX.Section>

      {/* <HX.Pane flow="right">
        <HX.Pane />
        <HX.Pane />
        <HX.Pane />
        <HX.Collection fields={["cds/exposure/granular/total_venue_us_factor"]} shownBy="cds/exposure/granular/include_us_venues" />
      </HX.Pane>
      <HX.Pane>
        <HX.Table shownBy="/cds/us_and_international_masking"
          syncColumnWidthsKey="mySyncedTables1"
          data={venue_us()}
          fields={["factor", "percentage", "selection"]}
          title="US Venue Factors"
          with="cds/exposure/granular"
        />
      </HX.Pane> */}



    </HX.Page>
  )
}

export { vw_venue_factors };