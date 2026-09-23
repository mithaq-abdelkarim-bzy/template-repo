import * as HX from "hx-model-components";

function vw_quote_summary(scale, shownBy = null) {
  return (
    <HX.Page title="Quote Summary" fullWidth shownBy={shownBy}>

      <HX.Section title="Quote Details">
        <HX.Pane flow="right">
          <HX.Collection
            title="Policy Details"
            with="cds/quote"
            fields={[
              "reinsured_name",
              "insured_name",
              "cover",
              "term"
            ]}
          />
          <HX.Collection
            title="Risk Details"
            with="cds/quote"
            fields={[
              "max_age_attained",
              "no_lives",
              "sum_insured_basis",
              "max_aol_sum_insured"
            ]}
          />
          <HX.Collection
            title=" "
            with="cds/quote"
            fields={[
              "free_cover_limit",
              "total_sum_insured",
              "event_limit"
            ]}
          />
          <HX.Collection
            title="Financial Details"
            with="cds/quote"
            fields={[
              "deposit_premium",
              "adjustable_rate",
              "commission"
            ]}
          />
        </HX.Pane>
      </HX.Section>

      <HX.Section title="Terms & Conditions">
        <HX.Pane flow="right">
          <HX.Table
            data={["cds/quote/exclusions"]}
            fields={[
              { field: "exclusion", width: 600 },
              { field: "is_excluded", width: 100 }
            ]}
            kb-interactive
          />
          <HX.Table
            data={["cds/quote/conditions"]}
            fields={[
              { field: "condition", width: 600 },
              { field: "is_included", width: 100 }
            ]}
            kb-interactive
          />
        </HX.Pane>
        <HX.Collection fields={["cds/quote/valid_until_date", null, null]} horizontal />
      </HX.Section>

      <HX.Section title="Notes & Summary Document">
        {/* <HX.Collection fields={["debug_str"]} /> */}
        <HX.Pane flow="right">
          <HX.Notes field="cds/quote/uw_notes" />
          <HX.Pane>
            <HX.Collection with="policy_doc" fields={["premium_check"]} shownBy="show_premium_check" />
            <HX.Button title="Generate Quote Summary" task="quote_to_excel_task" shownBy="policy_doc/show_generate_button" />
            <HX.File with="policy_doc" field="output_file" title="Click on the icon below to download the quote summary document" shownBy="show_download" />
          </HX.Pane>
        </HX.Pane>

      </HX.Section>

    </HX.Page >

  )
}

export { vw_quote_summary };