import * as HX from "hx-model-components";


function vw_airlines(shownBy) {
  const check = "_check"
  const check_l = "_check_label"
  const show = "/cds/exposure/granular/show_check_cols";
  const label = "/cds/exposure/granular/airlines_check_col_labels/";
  const airlines_fields_default = [
    { field: "include", width: 120 },
    { field: "no_of_aircraft", width: 120 },
    "operator",
    "aircraft_master_series",
    "registration",
    "aircraft_status",
    "coverage",
    "attachment_date",
    "expiry_date",
    "time_in_service",
    "build_year",
    "usage",
    "primary_usage",
    "market_class",
    "russian_built",
    "operator_country",
    "operator_region",
    "total_seats",
    "previous12_months_hours",
    "operating_mtow_lb",
    "value",
    "hull_limit",
    "hull_excess",
    "hull_ccy",
    "liability_limit",
    "liability_excess",
    "liability_ccy"
  ]
  const airlines_fields_validation = [
    { field: "include", width: 120 },
    { field: "no_of_aircraft", width: 120 },
    { field: `no_of_aircraft${check}`, labelBy: `${label}no_of_aircraft${check_l}` },
    "operator",
    "aircraft_master_series",
    "registration",
    "aircraft_status",
    "coverage",
    "attachment_date",
    { field: `attachment_date${check}`, labelBy: `${label}attachment_date${check_l}` },
    "expiry_date",
    { field: `expiry_date${check}`, labelBy: `${label}expiry_date${check_l}` },
    "time_in_service",
    { field: `time_in_service${check}`, labelBy: `${label}time_in_service${check_l}` },
    "build_year",
    { field: `build_year${check}`, labelBy: `${label}build_year${check_l}` },
    "usage",
    "primary_usage",
    "market_class",
    "russian_built",
    "operator_country",
    "operator_region",
    "total_seats",
    { field: `total_seats${check}`, labelBy: `${label}total_seats${check_l}` },
    "previous12_months_hours",
    { field: `previous12_months_hours${check}`, labelBy: `${label}previous12_months_hours${check_l}` },
    "operating_mtow_lb",
    { field: `operating_mtow_lb${check}`, labelBy: `${label}operating_mtow_lb${check_l}` },
    "value",
    { field: `value${check}`, labelBy: `${label}value${check_l}` },
    "hull_limit",
    { field: `hull_limit${check}`, labelBy: `${label}hull_limit${check_l}` },
    "hull_excess",
    { field: `hull_excess${check}`, labelBy: `${label}hull_excess${check_l}` },
    "hull_ccy",
    "liability_limit",
    { field: `liability_limit${check}`, labelBy: `${label}liability_limit${check_l}` },
    "liability_excess",
    { field: `liability_excess${check}`, labelBy: `${label}liability_excess${check_l}` },
    "liability_ccy"
  ]
  return (
    <HX.Page title="Airlines Details" shownBy={shownBy} fullWidth viewScale={0.8} >
      <HX.With context={{ type: "struct", path: "cds/exposure/granular" }}>

        <HX.Section title="Operator Details">
          <HX.Pane flow="right">
            <HX.Pane>
              <HX.Pane flow="right" >
                <HX.Collection fields={["operator_search"]} />
                <HX.Button title="Search for Operator" task="search_for_operator_task" />
                <HX.Notes field="operators_msg" shownBy="are_operators_fetched" />
              </HX.Pane>
              <HX.Table
                data={["operators"]}
                fields={["operator", "operator_class"]}
                kb-interactive
              />
              <HX.Collection fields={["fleet_size", "selected_operator_class"]} horizontal />
            </HX.Pane>
            <HX.Pane>
              <HX.Table
                data={["status_split"]}
                fields={["in_service", "storage", "other"]}
                kb-interactive
                transpose
              />
              {/* <HX.Button task="get_sql_inputs_task" title="Refresh Database" /> */}
              <HX.Collection fields={["status_split_msg"]} shownBy="show_status_split_msg" />
              <HX.Collection fields={["show_al_pricing"]} />
            </HX.Pane>
          </HX.Pane>
        </HX.Section>

        <HX.Section title="Default Values">
          <HX.Table
            data={["airlines_default"]}
            fields={airlines_fields_default}
            dynamic
            kb-interactive
            freezeLeft={0}
          />
        </HX.Section>

        <HX.Section title="Airlines Details">
          {/* <HX.Notes field="/debug_str" /> */}
          <HX.Pane>

            <HX.Pane flow="right">
              <HX.Pane>
                <HX.Button task="fill_with_defaults_task" title="Autopopulate Default Values" shownBy="/sql_db/are_regs_selected" />
                <HX.Button task="fetch_by_operator_task" title="Autopopulate from Cirium by Above Selected Operator" shownBy="/sql_db/are_regs_selected" />
                <HX.Button task="fetch_by_registration_task" title="Autopopulate from Cirium by Registration" shownBy="/sql_db/are_regs_selected" />
                <HX.Button task="clear_table_task" title="Clear Below" shownBy="/sql_db/are_regs_selected" />
              </HX.Pane>
              <HX.Pane>
                <HX.Table
                  data={[{ datum: "hull_premium", infoBy: "hull_premium/difference_msg" }]}
                  fields={[
                    { field: "from_slip", width: 150 },
                    { field: "from_rate", width: 150, shownBy: "hull_premium/are_premiums_equal" },
                    { field: "from_rate.red", width: 150, shownBy: "hull_premium/are_premiums_different" }
                  ]}
                  kb-interactive
                  shownBy="/sql_db/are_regs_selected"
                />
                <HX.Collection fields={["show_check_cols", "data_check"]} shownBy="/sql_db/are_regs_selected" horizontal />
                {/* <HX.Collection fields={["has_duplicate_regs_msg"]} shownBy="has_duplicate_regs" /> */}
                <HX.Notes field="has_duplicate_regs_msg" shownBy="has_duplicate_regs" />
                <HX.Notes field="has_missing_regs_msg" shownBy="has_missing_regs" />
              </HX.Pane>
            </HX.Pane>

            <HX.Pane flow="right">
              <HX.Notes field="/sql_db/duplicate_regs_msg" shownBy="/sql_db/has_duplicate_regs" />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
            <HX.Table
              shownBy="/sql_db/has_duplicate_regs"
              data={["/sql_db/duplicate_regs"]}
              fields={[
                { field: "is_selected", width: 100 },
                { field: "registration", width: 200 },
                { field: "aircraft_family", width: 300 },
                { field: "operator", width: 300 },
                { field: "serial_number", width: 200 },
              ]}
              dynamic
              kb-interactive
            />
            <HX.Pane flow="right">
              <HX.Button task="get_selected_regs_task" title="Keep selected" shownBy="/sql_db/is_at_least_one_reg_selected" />
              <HX.Notes field="/sql_db/duplicate_regs_selected_msg" shownBy="/sql_db/are_duplicate_regs_selected" />
              <HX.Pane />
              <HX.Pane />
            </HX.Pane>
            {/* Show full table */}
            <HX.Table
              shownBy="show_full_table"
              data={["airlines"]}
              fields={[
                ...airlines_fields_default,
                { field: "pll_award", width: 135 },
                { field: "tpl_limit_exposed", width: 120 },
                { field: "achieved_hull_rate", width: 120 },
              ]}
              dynamic
              kb-interactive
              maxListVisibleRows={20}
              freezeLeft={1}
            />
            {/* Show validation table */}
            <HX.Table
              title="Only rows with invalid entries are shown. Click on 'Validate Data' again to return to the full table."
              shownBy="show_validation_table"
              data={["airlines"]}
              fields={[
                ...airlines_fields_validation,
                { field: "pll_award", width: 135 },
                { field: `pll_award${check}`, labelBy: `${label}pll_award${check_l}` },
                { field: "tpl_limit_exposed", width: 120 },
                { field: "achieved_hull_rate", width: 120 },
              ]}
              dynamic
              kb-interactive
              maxListVisibleRows={20}
              freezeLeft={1}
              filter="has_error"
            />
          </HX.Pane>
        </HX.Section>

      </HX.With>
    </HX.Page >
  )
}

export { vw_airlines };
