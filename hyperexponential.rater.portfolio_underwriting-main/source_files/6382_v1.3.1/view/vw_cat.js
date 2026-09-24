import * as HX from "hx-model-components";
import { NUM_CURVES_IN_CAT } from "view/vw_constants";

function vw_cat(scale) {
  return (
    <HX.Page title="Cat" fullWidth={true} viewScale={scale} shownBy="model_state/show_cat">
      <HX.Section collapsible={false} title="CAT MODELLING">
        <HX.Pane>
          <HX.Collection fields={["cds/cat/currency", null, null, null, null, null, null]} horizontal />
          <HX.Collection fields={["cds/cat/modelling_as_at_date", null, null, null, null, null, null]} horizontal />
          <HX.Table
            title="Cat"
            with="cds/cat"
            kb-interactive
            data={[
              'curve_label',
              'model',
              'one_in_10000',
              'one_in_5000',
              'one_in_1000',
              'one_in_500',
              'one_in_250',
              'one_in_200',
              'one_in_100',
              'one_in_50',
              'one_in_30',
              'one_in_10',
              'one_in_5',
              'one_in_2',
              null,
              'aal',
              'standard_deviation',
              'cov',
              null,
              'selected_class',
              'gn_in_force_premium',
              'unadjusted_gn_cat_ulr',
              null,
              'roll_forward',
              'inflation_factor',
              'rate_change_factor',
              'selected_gn_cat_ulr',
            ]}
            fields={[
              'critical_prob',
              'return_period',
              ...Array.from({ length: NUM_CURVES_IN_CAT }, (_, i) => `curve_${i + 1}`),
              null,
              ...Array.from({ length: NUM_CURVES_IN_CAT }, (_, i) => `curve_${i + 1}_cnv`)]}
          />
        </HX.Pane>
        <HX.Notes field="cds/cat/note_1.read_only" />
        <HX.Notes field="cds/cat/note_2.read_only" />
      </HX.Section>
      <HX.Section title="Commentary" collapsible={false}>
        <HX.Notes field="cds/rationale/cat_notes" title="Please note any rationale for selection below, and any use of overrides:" />
      </HX.Section>
    </HX.Page >
  )
}

export { vw_cat };