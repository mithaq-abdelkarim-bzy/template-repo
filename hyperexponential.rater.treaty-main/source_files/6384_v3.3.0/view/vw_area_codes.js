import * as HX from "hx-model-components";


// northern_europe
const northern_europe_values = ['eat', 'ebe', 'ech', 'edk', 'emz', 'efi', 'efr', 'ege', 'eic', 'eie', 'enl', 'eno', 'egf', 'ese', 'euk', 'euf'];
const northern_europe_fields = [];
for (const val of northern_europe_values) {
  northern_europe_fields.push(`area_codes_select/${val}`);
  northern_europe_fields.push(`area_codes_perc/${val}`);
  northern_europe_fields.push(null);
}
northern_europe_fields.pop();

// southern_europe
const southern_europe_values = ['ees', 'egr', 'eit', 'ept', 'etu'];
const southern_europe_fields = [];
for (const val of southern_europe_values) {
  southern_europe_fields.push(`area_codes_select/${val}`);
  southern_europe_fields.push(`area_codes_perc/${val}`);
  southern_europe_fields.push(null);
}
southern_europe_fields.pop();

// cee
const cee_values = ['ebg', 'cef', 'ecx', 'ecz', 'ehu', 'epl', 'ero', 'eru', 'esb', 'esc', 'esr'];
const cee_fields = [];
for (const val of cee_values) {
  cee_fields.push(`area_codes_select/${val}`);
  cee_fields.push(`area_codes_perc/${val}`);
  cee_fields.push(null);
}
cee_fields.pop();

// us
const us_values = ['usa01', 'usa02', 'usa03', 'usa04', 'usa05', 'usa06', 'usa07', 'usa08', 'usa09', 'usa10', 'usa11', 'usa12', 'usa13', 'usa14', 'usa15', 'usa16', 'usa20', 'usa21', 'usa22'];
const us_fields = [];
for (const val of us_values) {
  us_fields.push(`area_codes_select/${val}`);
  us_fields.push(`area_codes_perc/${val}`);
  us_fields.push(null);
}
us_fields.pop();

// lat_am
const lat_am_values = ['sar', 'sbz', 'sbv', 'sbr', 'scl', 'sco', 'scr', 'sec', 'sel', 'sgt', 'sgy', 'shn', 'smx', 'snq', 'spa', 'spy', 'spe', 'suy', 'sve', 'ofg'];
const lat_am_fields = [];
for (const val of lat_am_values) {
  lat_am_fields.push(`area_codes_select/${val}`);
  lat_am_fields.push(`area_codes_perc/${val}`);
  lat_am_fields.push(null);
}
lat_am_fields.pop();

// aus
const aus_values = ['oa1', 'oa2', 'oa3', 'oa4', 'oa5', 'oa6', 'ota', 'onz', 'ofj'];
const aus_fields = [];
for (const val of aus_values) {
  aus_fields.push(`area_codes_select/${val}`);
  aus_fields.push(`area_codes_perc/${val}`);
  aus_fields.push(null);
}
aus_fields.pop();

// caribbean
const caribbean_values = ['bag', 'bah', 'ban', 'bbb', 'bbh', 'bbm', 'bcb', 'bcm', 'bcu', 'bdo', 'bdr', 'bgn', 'bgs', 'bgu', 'bht', 'bjm', 'bkn', 'bmq', 'bms', 'bon', 'bpr', 'bsl', 'bsv', 'bv1', 'bvs', 'bx7'];
const caribbean_fields = [];
for (const val of caribbean_values) {
  caribbean_fields.push(`area_codes_select/${val}`);
  caribbean_fields.push(`area_codes_perc/${val}`);
  caribbean_fields.push(null);
}
caribbean_fields.pop();

// canada
const canada_values = ['cbc', 'cqu', 'con', 'cpr', 'cat', 'bpm'];
const canada_fields = [];
for (const val of canada_values) {
  canada_fields.push(`area_codes_select/${val}`);
  canada_fields.push(`area_codes_perc/${val}`);
  canada_fields.push(null);
}
canada_fields.pop();

// far_east
const far_east_values = ['fct', 'fcq', 'fkr', 'fhk', 'fia', 'oph', 'fsp', 'fsk', 'fta', 'fjq', 'fjw', 'mbd', 'fcy', 'ogm', 'fmy', 'mma', 'fby', 'fnp', 'mpk', 'opg', 'fth', 'fvn'];
const far_east_fields = [];
for (const val of far_east_values) {
  far_east_fields.push(`area_codes_select/${val}`);
  far_east_fields.push(`area_codes_perc/${val}`);
  far_east_fields.push(null);
}
far_east_fields.pop();

// amei
const amei_values = ['mis', 'min', 'asa', 'mae', 'mba', 'aal', 'amo', 'aeg', 'ali', 'amu', 'mjo', 'mom', 'mqa', 'ayt', 'agi'];
const amei_fields = [];
for (const val of amei_values) {
  amei_fields.push(`area_codes_select/${val}`);
  amei_fields.push(`area_codes_perc/${val}`);
  amei_fields.push(null);
}
amei_fields.pop();


function vw_area_codes(scale) {
  return (
    <HX.Page title="Area Codes" fullWidth={true} viewScale={scale} shownBy="model_state/show_after_landing_page">
      <HX.Section title="Summary">
        <HX.Pane>
          <HX.Collection
            numCols={4}
            fields={[
              "cds/send_rate_change/confirm_area_codes",
              null,
              null,
              null
            ]} />
          <HX.Table
            title="Total"
            data={[{ datum: "cds/layers" }]}
            fields={[
              "area_codes_summary/europe",
              "area_codes_summary/us_aus",
              "area_codes_summary/can_car",
              "area_codes_summary/far_east_amei",
              null,
              "area_codes_summary/total"
            ]}
            kb-interactive
          />
        </HX.Pane>
      </HX.Section>

      <HX.Section title="Northern Europe, Southern Europe and CEE" shownBy="cds/show_intl_fields">
        <HX.Table
          title="EU EX WS Selector"
          data={[{ datum: "cds", maxWidth: 200, labelBy: "cds/blank_label" }, null, { datum: "cds/layers", maxWidth: 200 }]}
          fields={["area_code_x_eu_ws"]}
          kb-interactive
          transpose
          syncColumnWidthsKey="europe"
        />
        <HX.Pane>
          <HX.Table
            title="Northern Europe"
            data={[{ datum: "cds", maxWidth: 200, labelBy: "cds/area_code_label" }, null, { datum: "cds/layers", maxWidth: 200 }]}
            fields={northern_europe_fields}
            kb-interactive
            transpose
            syncColumnWidthsKey="europe"
          />
          <HX.Table
            title="Southern Europe"
            data={[{ datum: "cds", maxWidth: 200, labelBy: "cds/area_code_label" }, null, { datum: "cds/layers", maxWidth: 200 }]}
            fields={southern_europe_fields}
            kb-interactive
            transpose
            syncColumnWidthsKey="europe"
          />
          <HX.Table
            title="CEE"
            data={[{ datum: "cds", maxWidth: 200, labelBy: "cds/area_code_label" }, null, { datum: "cds/layers", maxWidth: 200 }]}
            fields={cee_fields}
            kb-interactive
            transpose
            syncColumnWidthsKey="europe"
          />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="US, Latin America and Australia">
        <HX.Pane>
          <HX.Table
            title="US"
            data={[{ datum: "cds", maxWidth: 200, labelBy: "cds/area_code_label" }, null, { datum: "cds/layers", maxWidth: 200 }]}
            fields={us_fields}
            kb-interactive
            transpose
            syncColumnWidthsKey="us"
          />
          <HX.Table
            title="Latin America"
            data={[{ datum: "cds", maxWidth: 200, labelBy: "cds/area_code_label" }, null, { datum: "cds/layers", maxWidth: 200 }]}
            fields={lat_am_fields}
            kb-interactive
            transpose
            syncColumnWidthsKey="us"
          />
          <HX.Table
            title="Australia"
            data={[{ datum: "cds", maxWidth: 200, labelBy: "cds/area_code_label" }, null, { datum: "cds/layers", maxWidth: 200 }]}
            fields={aus_fields}
            kb-interactive
            transpose
            syncColumnWidthsKey="us"
          />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Caribbean and Canada" shownBy="cds/show_intl_fields">
        <HX.Pane>
          <HX.Table
            title="Caribbean"
            data={[{ datum: "cds", maxWidth: 200, labelBy: "cds/area_code_label" }, null, { datum: "cds/layers", maxWidth: 200 }]}
            fields={caribbean_fields}
            kb-interactive
            transpose
            syncColumnWidthsKey="carr"
          />
          <HX.Table
            title="Canada"
            data={[{ datum: "cds", maxWidth: 200, labelBy: "cds/area_code_label" }, null, { datum: "cds/layers", maxWidth: 200 }]}
            fields={canada_fields}
            kb-interactive
            transpose
            syncColumnWidthsKey="carr"
          />
        </HX.Pane>
      </HX.Section>
      <HX.Section title="Far East and AMEI" shownBy="cds/show_intl_fields">
        <HX.Pane>
          <HX.Table
            title="Far East"
            data={[{ datum: "cds", maxWidth: 200, labelBy: "cds/area_code_label" }, null, { datum: "cds/layers", maxWidth: 200 }]}
            fields={far_east_fields}
            kb-interactive
            transpose
            syncColumnWidthsKey="far_east"
          />
          <HX.Table
            title="AMEI"
            data={[{ datum: "cds", maxWidth: 200, labelBy: "cds/area_code_label" }, null, { datum: "cds/layers", maxWidth: 200 }]}
            fields={amei_fields}
            kb-interactive
            transpose
            syncColumnWidthsKey="far_east"
          />
        </HX.Pane>
      </HX.Section>
    </HX.Page>
  )
}

export { vw_area_codes };