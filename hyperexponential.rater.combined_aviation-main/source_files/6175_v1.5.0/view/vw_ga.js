import * as HX from "hx-model-components";


function vw_ga(shownBy) {
  const check = "_check"
  const check_l = "_check_label"
  const show = "/cds/exposure/granular/show_check_cols";
  const label = "/cds/exposure/granular/ga_check_col_labels/";
  const aircrafts_fields_default = [
    "include",
    "aircraft_class",
    "number_of_engines",
    "operator",
    "aircraft_master_series",
    "no_of_aircraft",
    "registration",
    "value",
    "hull_ccy",
    "attachment_date",
    "expiry_date",
    "time_in_service",
    "build_location",
    "build_year",
    "operator_country",
    "operator_region",
    "use",
    "per_occ_deductible_pct",
    "per_occ_deductible",
    "pax_net_worth",
    "total_seats",
    "crew_seats",
    "seat_occupancy",
    "fatality",
    "per_pax_liab_limit",
    "combined_single_limit",
    "liability_ccy",
    "tpl_limit_exposed",
    "achieved_hull_rate",
    null,
    "hull_benchmark_rate",
    "pax_liab_benchmark_per_seat",
    "tpl_benchmark",
    "total_hull_benchmark",
    "total_liab_benchmark",
    null,
    "renewing_aircraft",
    "bm_allocated_hull_premium",
    "bm_allocated_liab_premium"
  ]
  const aircrafts_fields_validation = [
    "include",
    "aircraft_class",
    { field: `aircraft_class${check}`, labelBy: `${label}aircraft_class${check_l}` },
    "number_of_engines",
    "operator",
    "aircraft_master_series",
    "no_of_aircraft",
    { field: `no_of_aircraft${check}`, labelBy: `${label}no_of_aircraft${check_l}` },
    "registration",
    "value",
    { field: `value${check}`, labelBy: `${label}value${check_l}` },
    "hull_ccy",
    "attachment_date",
    { field: `attachment_date${check}`, labelBy: `${label}attachment_date${check_l}` },
    "expiry_date",
    { field: `expiry_date${check}`, labelBy: `${label}expiry_date${check_l}` },
    "time_in_service",
    { field: `time_in_service${check}`, labelBy: `${label}time_in_service${check_l}` },
    "build_location",
    "build_year",
    { field: `build_year${check}`, labelBy: `${label}build_year${check_l}` },
    "operator_country",
    { field: `operator_country${check}`, labelBy: `${label}operator_country${check_l}` },
    "operator_region",
    "use",
    { field: `use${check}`, labelBy: `${label}use${check_l}` },
    "per_occ_deductible_pct",
    { field: `per_occ_deductible_pct${check}`, labelBy: `${label}per_occ_deductible_pct${check_l}` },
    "per_occ_deductible",
    { field: `per_occ_deductible${check}`, labelBy: `${label}per_occ_deductible${check_l}` },
    "pax_net_worth",
    "total_seats",
    { field: `total_seats${check}`, labelBy: `${label}total_seats${check_l}` },
    "crew_seats",
    { field: `crew_seats${check}`, labelBy: `${label}crew_seats${check_l}` },
    "seat_occupancy",
    "fatality",
    "per_pax_liab_limit",
    { field: `per_pax_liab_limit${check}`, labelBy: `${label}per_pax_liab_limit${check_l}` },
    "combined_single_limit",
    { field: `combined_single_limit${check}`, labelBy: `${label}combined_single_limit${check_l}` },
    "liability_ccy",
    "tpl_limit_exposed",
    { field: `tpl_limit_exposed${check}`, labelBy: `${label}tpl_limit_exposed${check_l}` },
    "achieved_hull_rate",
    null,
    "hull_benchmark_rate",
    "pax_liab_benchmark_per_seat",
    "tpl_benchmark",
    "total_hull_benchmark",
    "total_liab_benchmark",
    null,
    "renewing_aircraft",
    "bm_allocated_hull_premium",
    "bm_allocated_liab_premium"
  ]
  return (
    <HX.Page title="Aircraft Details" shownBy={shownBy} fullWidth viewScale={0.8} >
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
                fields={["operator"]}
                kb-interactive
              />
              <HX.Collection fields={["fleet_size", "show_ga_pricing"]} horizontal />
            </HX.Pane>
            {/* <HX.Button task="get_sql_inputs_task" title="Refresh Database" /> */}
            <HX.Pane />
          </HX.Pane>
        </HX.Section>

        <HX.Section title="Default Values and Totals">
          <HX.Table
            data={["aircrafts_default"]}
            fields={aircrafts_fields_default}
            dynamic
            kb-interactive
            freezeLeft={0}
          />
        </HX.Section>

        <HX.Section title="Aircraft Details">
          <HX.Pane>
            <HX.Pane flow="right">
              <HX.Pane>
                <HX.Button task="fill_with_defaults_task" title="Autopopulate Default Values" shownBy="/sql_db/are_regs_selected" />
                <HX.Button task="fetch_by_operator_task" title="Autopopulate from Cirium by Above Selected Operator" shownBy="/sql_db/are_regs_selected" />
                <HX.Button task="fetch_by_registration_task" title="Autopopulate from Cirium by Registration" shownBy="/sql_db/are_regs_selected" />
                <HX.Button task="fill_pax_limit_implied" title="Autopopulate PAX Liability Limit If Time in Service is 0%" shownBy="/sql_db/are_regs_selected" />
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
              data={["aircrafts"]}
              fields={aircrafts_fields_default}
              dynamic
              kb-interactive
              maxListVisibleRows={20}
              freezeLeft={1}
            />
            {/* Show validation table */}
            <HX.Table
              title="Only rows with invalid entries are shown. Click on 'Validate Data' again to return to the full table."
              shownBy="show_validation_table"
              data={["aircrafts"]}
              fields={aircrafts_fields_validation}
              dynamic
              kb-interactive
              maxListVisibleRows={20}
              freezeLeft={1}
              filter="has_error"
            />
          </HX.Pane>
          {/* <HX.Notes field="/debug_str" /> */}
        </HX.Section>

      </HX.With>
    </HX.Page >
  )
}

export { vw_ga };
