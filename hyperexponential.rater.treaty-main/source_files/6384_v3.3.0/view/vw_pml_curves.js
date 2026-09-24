import * as HX from "hx-model-components";
import { pml_types, pml_titles } from "view/vw_constants";

const rp_loss_fields = [
  "rp_loss/rp_10000",
  "rp_loss/rp_5000",
  "rp_loss/rp_1000",
  "rp_loss/rp_500",
  "rp_loss/rp_250",
  "rp_loss/rp_200",
  "rp_loss/rp_100",
  "rp_loss/rp_50",
  "rp_loss/rp_25",
  "rp_loss/rp_10",
  "rp_loss/rp_5",
  "rp_loss/rp_2"]

const rp_loss_prev_fields = [
  "rp_loss_prev/rp_10000",
  "rp_loss_prev/rp_5000",
  "rp_loss_prev/rp_1000",
  "rp_loss_prev/rp_500",
  "rp_loss_prev/rp_250",
  "rp_loss_prev/rp_200",
  "rp_loss_prev/rp_100",
  "rp_loss_prev/rp_50",
  "rp_loss_prev/rp_25",
  "rp_loss_prev/rp_10",
  "rp_loss_prev/rp_5",
  "rp_loss_prev/rp_2"]

const rp_loss_change_fields = [
  "rp_loss_change/rp_10000",
  "rp_loss_change/rp_5000",
  "rp_loss_change/rp_1000",
  "rp_loss_change/rp_500",
  "rp_loss_change/rp_250",
  "rp_loss_change/rp_200",
  "rp_loss_change/rp_100",
  "rp_loss_change/rp_50",
  "rp_loss_change/rp_25",
  "rp_loss_change/rp_10",
  "rp_loss_change/rp_5",
  "rp_loss_change/rp_2"]


function vw_include(pml_types, pml_titles) {
  const objects = [];

  pml_types.forEach((pml_type, index) => {
    const pml_title = pml_titles[index];
    const pml_table = index + "_table";

    objects.push(
      <HX.Table
        title={pml_title}
        with={"cds/pml_curves"}
        data={[{ datum: pml_type, width: 200 }]}
        fields={[
          "include_in_peril_alloc",
          "peril",
          "curve_description",
          { field: "currency", shownBy: "/cds/show_intl_fields" }
        ]}
        transpose
        removeHorizontalScroll={true}
        rowHeaderSettings={{ width: 200 }}
        kb-interactive
      />
    );
  });

  return objects
}


function vw_curves_ty(pml_types, pml_titles) {
  const objects = [];

  pml_types.forEach((pml_type, index) => {
    const pml_title = pml_titles[index];
    const pml_table = index + "_table";

    objects.push(
      <HX.Table
        title="This Year"
        with={"cds/pml_curves"}
        data={[{ datum: pml_type, maxWidth: 200 }]}
        fields={rp_loss_fields}
        removeHorizontalScroll={true}
        transpose
        rowHeaderSettings={{ width: 200 }}
        kb-interactive
      />
    );
  });

  return objects
}


function vw_curves_change(pml_types, pml_titles) {
  const objects = [];

  pml_types.forEach((pml_type, index) => {
    const pml_title = pml_titles[index];
    const pml_table = index + "_table";

    objects.push(
      <HX.Table
        title="YOY Change"
        with={"cds/pml_curves"}
        data={[{ datum: pml_type, maxWidth: 200 }]}
        fields={rp_loss_change_fields}
        removeHorizontalScroll={true}
        transpose
        rowHeaderSettings={{ width: 200 }}
        kb-interactive
      />
    );
  });

  return objects
}


function vw_curves_ly(pml_types, pml_titles) {
  const objects = [];

  pml_types.forEach((pml_type, index) => {
    const pml_title = pml_titles[index];
    const pml_table = index + "_table";

    objects.push(
      <HX.Table
        title="Previous Year"
        with={"cds/pml_curves"}
        data={[{ datum: pml_type, maxWidth: 200 }]}
        fields={rp_loss_prev_fields}
        removeHorizontalScroll={true}
        transpose
        rowHeaderSettings={{ width: 200 }}
        kb-interactive
      />
    );
  });

  return objects
}


function vw_pml_curves(scale) {
  return (
    <HX.Page title="PML Curves" fullWidth={true} viewScale={scale} shownBy="cds/show_non_risk_xl">
      <HX.Section title="Peril PML Selection">
        <HX.Pane flow="right" reflow={false}>
          <HX.Pane ratio={1}>
            <HX.Collection
              numCols={1}
              fields={[
                { field: "cds/modelling_account_level/rms_eq_curve_selection", shownBy: "/cds/show_us_fields" },
                { field: "cds/modelling_account_level/rms_ws_curve_selection", shownBy: "/cds/show_us_fields" },
                { field: "cds/modelling_account_level/rms_scs_curve_selection", shownBy: "/cds/show_us_fields" },

                { field: "cds/modelling_account_level/rms_eu_ws_curve_selection", shownBy: "/cds/show_intl_fields" },
                { field: "cds/modelling_account_level/rms_jp_eq_curve_selection", shownBy: "/cds/show_intl_fields" },
                { field: "cds/modelling_account_level/rms_jp_ws_curve_selection", shownBy: "/cds/show_intl_fields" },
                { field: "cds/modelling_account_level/rms_can_eq_curve_selection", shownBy: "/cds/show_intl_fields" },
                { field: "cds/modelling_account_level/rms_caribbean_ws_curve_selection", shownBy: "/cds/show_intl_fields" },
              ]}
              stretch={true}
            />
          </HX.Pane>
          <HX.Pane ratio={3}>
            <HX.Notes
              field="cds/pml_curves/information"
              title="PML Selection Information"
            />
          </HX.Pane>
        </HX.Pane>
      </HX.Section>
      <HX.Section title="PML Comments">
        <HX.Notes
          field="cds/pml_curves/comments"
        />
      </HX.Section>
      <HX.Section title="PML Entry">
        <HX.Pane flow="right" reflow={false}>
          <HX.Table
            title={"                                                                                                                                                                                                    RMS Curves"}
            with={"cds/pml_curves"}
            data={[{ datum: "curve_aggregator", width: 200 }, { datum: "burn_curve", width: 200 }, null, { datum: "rms_curves", width: 200 }]}
            fields={[
              "include_in_peril_alloc",
              "peril",
              "curve_description",
              { field: "currency", shownBy: "/cds/show_intl_fields" }
            ]}
            transpose
            removeHorizontalScroll={true}
            rowHeaderSettings={{ width: 200 }}
            kb-interactive
          />
          {vw_include(pml_types, pml_titles)}
        </HX.Pane>
        <HX.Pane flow="right" reflow={false}>
          <HX.Table
            title="This Year"
            with={"cds/pml_curves"}
            data={[{ datum: "curve_aggregator", width: 200 }, { datum: "burn_curve", width: 200 }, null, { datum: "rms_curves", maxWidth: 200 }]}
            fields={rp_loss_fields}
            removeHorizontalScroll={true}
            transpose
            rowHeaderSettings={{ width: 200 }}
            kb-interactive
          />
          {vw_curves_ty(pml_types, pml_titles)}
        </HX.Pane>
        <HX.Pane flow="right" reflow={false}>
          <HX.Table
            title="YOY Change"
            with={"cds/pml_curves"}
            data={[{ datum: "curve_aggregator", width: 200 }, { datum: "burn_curve", width: 200 }, null, { datum: "rms_curves", maxWidth: 200 }]}
            fields={rp_loss_change_fields}
            removeHorizontalScroll={true}
            transpose
            rowHeaderSettings={{ width: 200 }}
            kb-interactive
          />
          {vw_curves_change(pml_types, pml_titles)}
        </HX.Pane>
        <HX.Pane flow="right" reflow={false}>
          <HX.Table
            title="Previous Year"
            with={"cds/pml_curves"}
            data={[{ datum: "curve_aggregator", width: 200 }, { datum: "burn_curve", width: 200 }, null, { datum: "rms_curves", maxWidth: 200 }]}
            fields={rp_loss_prev_fields}
            removeHorizontalScroll={true}
            transpose
            rowHeaderSettings={{ width: 200 }}
            kb-interactive
          />
          {vw_curves_ly(pml_types, pml_titles)}
        </HX.Pane>
      </HX.Section>
    </HX.Page >
  )
}

export { vw_pml_curves };