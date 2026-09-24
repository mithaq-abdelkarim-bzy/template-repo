from algorithms.rate_constants import get_base_params
from algorithms.rate_simulation import run_simulation
from algorithms.rate_simulation_inputs import (
    get_ded_params,
    get_model_params,
    get_quotes_params,
    get_quotes_params_addl,
    validate_simulation_inputs,
)


RARC_SIMULATION_COUNT = 5000
_has_validated_transient_inputs = False


def reset_rarc_simulation_validation_state():
    """Reset one-time transient validation state before a new RARC run."""
    global _has_validated_transient_inputs
    _has_validated_transient_inputs = False


def _validate_transient_inputs_once(hxd, progress):
    """Validate the first transient HXD used by RARC simulation repricing."""
    global _has_validated_transient_inputs
    if not _has_validated_transient_inputs:
        validate_simulation_inputs(hxd, progress)
        _has_validated_transient_inputs = True


def validate_transient_simulation_inputs(hxd, progress):
    """Compatibility wrapper for transient simulation input validation."""
    validate_simulation_inputs(hxd, progress)


def _populate_layer_simulation_outputs(layers, model_outputs):
    counter = 0
    for layer in layers:
        if layer.include:
            if counter >= len(model_outputs):
                break

            layer.sim_output_uw_adj.exposure_premium = model_outputs["BookRate"].iloc[counter]
            layer.sim_output_uw_adj.average_freq = model_outputs["FreqPer1000"].iloc[counter]
            layer.sim_output_uw_adj.average_defense_cost_freq = model_outputs["DefFreqFGUPer1000"].iloc[counter]
            layer.sim_output_uw_adj.layer_exhaust_prob = model_outputs["ExhaustionProb"].iloc[counter]
            layer.exposure_rate = model_outputs["BookRate"].iloc[counter]
            counter += 1


def recalculate_exposure_rates_for_rate_change(hxd, progress):
    """Run a lightweight simulation and update transient layer exposure rates for RARC repricing."""
    _validate_transient_inputs_once(hxd, progress)

    expected_exposure = hxd.cds.exposure.granular.exposure_expected_current_year or 0
    profession = "lpl" if hxd.cds.profession == "Lawyers" else "aec"

    bp = get_base_params(profession)
    df_quote_params = get_quotes_params(hxd)
    df_quote_params_addl = get_quotes_params_addl(hxd)
    df_ded_params = get_ded_params(hxd)
    df_model_params_final, _ = get_model_params(hxd, profession, expected_exposure, False)

    df_modeloutputs, df_addmodeloutputs = run_simulation(
        ded_params=df_ded_params,
        model_params=df_model_params_final,
        quotes_params=df_quote_params,
        add_quotes_params=df_quote_params_addl,
        revenue=expected_exposure,
        r_scalar_input_odf=bp.odf,
        num_sims=RARC_SIMULATION_COUNT,
    )

    _populate_layer_simulation_outputs(hxd.cds.layers, df_modeloutputs)
    _populate_layer_simulation_outputs(hxd.cds.layers_addl, df_addmodeloutputs)
