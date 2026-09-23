// Configs for the various options tables

export const perils_covered_tables_configs = [
  {
    title: "Include Peril",
    fields: [
      { field: 'coverages/aop/include_peril/value', shownBy: "show_aop_option" },
      { field: 'coverages/wildfire/include_peril/value', shownBy: "wildfire_enabled" },
      { field: 'coverages/wildfire/include_peril/value.read_only_same_label', shownBy: "wildfire_disabled" },
      { field: 'coverages/ws/include_peril/value', shownBy: "show_ws_option" },
      { field: 'coverages/eb/include_peril/value', shownBy: "show_eb_option" },
      { field: 'coverages/fl/include_peril/value', shownBy: "show_fl_option" },
      { field: 'coverages/eq/include_peril/value', shownBy: "show_eq_option" },
      { field: 'coverages/paf/include_peril/value', shownBy: "show_paf_option" }
    ],
    showLockedTableBy: "/cds/lock_layer",
    isLockedTableEnabled: false,
    specialReadOnlyFields: {
      'coverages/aop/include_peril/value': ".read_only_same_label",
      'coverages/wildfire/include_peril/value': ".read_only_same_label",
      'coverages/ws/include_peril/value': ".read_only_same_label",
      'coverages/eb/include_peril/value': ".read_only_same_label",
      'coverages/fl/include_peril/value': ".read_only_same_label",
      'coverages/eq/include_peril/value': ".read_only_same_label",
      'coverages/paf/include_peril/value': ".read_only_same_label",
    }
  },
  {
    title: "Limits",
    fields: [
      { field: "coverage_a_building_limit", shownBy: "pricing_limits_table/show_coverage_a_building_limit" },
      { field: "coverage_b_other_structures_limit", shownBy: "pricing_limits_table/show_coverage_b_other_structures_limit" },
      { field: "coverage_c_personal_property_limit", shownBy: "pricing_limits_table/show_coverage_c_personal_property_limit" },
      { field: "coverage_d_loss_of_use_limit", shownBy: "pricing_limits_table/show_coverage_d_loss_of_use_limit" },
      { field: "coverage_e_additional_living_expense_limit", shownBy: "pricing_limits_table/show_coverage_e_additional_living_expense_limit" },
      { field: "coverage_l_liability_limit", shownBy: "pricing_limits_table/show_coverage_l_liability_limit" },
      { field: "coverage_m_med_pay_limit", shownBy: "/cds/validation/coverage_m_med_pay_limit/valid" },
      { field: "coverage_m_med_pay_limit.notSupported", shownBy: "/cds/validation/coverage_m_med_pay_limit/invalid", infoBy: "/cds/validation/coverage_m_med_pay_limit/info_text" },
    ],
    showLockedTableBy: "/cds/lock_layer",
    isLockedTableEnabled: true
  },
  {
    title: "Sub-Limits",
    fields: [
      "sublimits/animal_included",
      { field: "sublimits/animal", shownBy: "/cds/validation/animal/valid" },
      { field: "sublimits/animal.notSupported", shownBy: "/cds/validation/animal/invalid", infoBy: "/cds/validation/animal/info_text" },
      "sublimits/diving_board_and_pool_included",
      { field: "sublimits/diving_board_and_pool", shownBy: "/cds/validation/diving_board_and_pool/valid" },
      { field: "sublimits/diving_board_and_pool.notSupported", shownBy: "/cds/validation/diving_board_and_pool/invalid", infoBy: "/cds/validation/diving_board_and_pool/info_text" },
      "sublimits/trampoline_included",
      { field: "sublimits/trampoline", shownBy: "/cds/validation/trampoline/valid" },
      { field: "sublimits/trampoline.notSupported", shownBy: "/cds/validation/trampoline/invalid", infoBy: "/cds/validation/trampoline/info_text" },
      "sublimits/swimming_pool_included",
      { field: "sublimits/swimming_pool", shownBy: "/cds/validation/swimming_pool/valid" },
      { field: "sublimits/swimming_pool.notSupported", shownBy: "/cds/validation/swimming_pool/invalid", infoBy: "/cds/validation/swimming_pool/info_text" },
      "sublimits/premises_only"
    ],
    showLockedTableBy: "/cds/lock_layer",
    isLockedTableEnabled: false
  }
]

export const pricing_table_config = [
  {
    title: "AOP", fields: [
      { field: 'coverages/aop/tiv/value' },
      { field: 'coverages/aop/base_rate' },
      { field: 'coverages/aop/modifiers_impact/factor' },
      { field: 'coverages/aop/adjusted_base_rate' },
      { field: 'coverages/aop/minimum_rate' },
      { field: 'coverages/aop/final_modified_rate' },
      { field: "coverages/aop/deductible", shownBy: "/cds/validation/aop_deductible/valid" },
      { field: "coverages/aop/deductible.notSupported", shownBy: "/cds/validation/aop_deductible/invalid", infoBy: "/cds/validation/aop_deductible/info_text" },
      'coverages/aop/minimum_deductible',
      'coverages/aop/final_deductible',
      "coverages/aop/water_damage_deductible",
      'coverages/aop/deductible_impact',
      "coverages/aop/water_damage_sublimit",
      'coverages/aop/model_premium',
      { field: 'coverages/aop/model_premium_water_damage' },
      { field: 'coverages/aop/model_premium_hail' },
      { field: 'coverages/aop/model_premium_fire' },
      { field: 'coverages/aop/model_premium_other' },
      'coverages/aop/model_rate',
      { field: 'coverages/aop/model_rate_water_damage' },
      { field: 'coverages/aop/model_rate_hail' },
      { field: 'coverages/aop/model_rate_fire' },
      { field: 'coverages/aop/model_rate_other' },
    ],
    shownBy: "show_aop_options",
    showLockedTableBy: "/cds/lock_layer",
    collection_field: "show_full_pricing_tables_aop",
    isLockedTableEnabled: true,
    outputFields: ['coverages/aop/tiv/value', 'coverages/aop/base_rate', 'coverages/aop/modifiers_impact/factor', 'coverages/aop/adjusted_base_rate', 'coverages/aop/minimum_rate', 'coverages/aop/final_modified_rate',
      'coverages/aop/minimum_deductible', 'coverages/aop/final_deductible', 'coverages/aop/deductible_impact', 'coverages/aop/model_premium', 'coverages/aop/model_premium_water_damage', 'coverages/aop/model_premium_hail',
      'coverages/aop/model_premium_fire', 'coverages/aop/model_premium_other', 'coverages/aop/model_rate', 'coverages/aop/model_rate_water_damage', 'coverages/aop/model_rate_hail', 'coverages/aop/model_rate_fire', 'coverages/aop/model_rate_other']
  },
  {
    title: "Wildfire", fields: [
      { field: 'coverages/wildfire/tiv/value' },
      { field: 'coverages/wildfire/base_rate' },
      { field: 'coverages/wildfire/modifiers_impact/factor' },
      { field: 'coverages/wildfire/adjusted_base_rate' },
      { field: 'coverages/wildfire/minimum_rate' },
      { field: 'coverages/wildfire/final_modified_rate' },
      { field: "coverages/wildfire/deductible_type", shownBy: "/cds/validation/wildfire_deductible_type/valid" },
      { field: "coverages/wildfire/deductible_type.notSupported", shownBy: "/cds/validation/wildfire_deductible_type/invalid", infoBy: "/cds/validation/wildfire_deductible_type/info_text" },
      { field: "coverages/wildfire/deductible", shownBy: "/cds/validation/wildfire_deductible/valid" },
      { field: "coverages/wildfire/deductible.notSupported", shownBy: "/cds/validation/wildfire_deductible/invalid", infoBy: "/cds/validation/wildfire_deductible/info_text" },
      'coverages/wildfire/minimum_deductible',
      'coverages/wildfire/final_deductible',
      'coverages/wildfire/deductible_impact',
      'coverages/wildfire/model_premium',
      'coverages/wildfire/model_rate',
      'coverages/wildfire/wildfire_score'
    ],
    shownBy: "show_wildfire_options",
    showLockedTableBy: "/cds/lock_layer",
    collection_field: "show_full_pricing_tables_wildfire",
    isLockedTableEnabled: true,
    outputFields: ['coverages/wildfire/tiv/value', 'coverages/wildfire/base_rate', 'coverages/wildfire/modifiers_impact/factor', 'coverages/wildfire/adjusted_base_rate', 'coverages/wildfire/minimum_rate',
      'coverages/wildfire/final_modified_rate', 'coverages/wildfire/minimum_deductible', 'coverages/wildfire/final_deductible', 'coverages/wildfire/deductible_impact', 'coverages/wildfire/model_premium',
      'coverages/wildfire/model_rate']
  },
  {
    title: "WS", key: "ws", fields: [
      { field: 'coverages/ws/tiv/value' },
      { field: 'coverages/ws/base_rate' },
      { field: 'coverages/ws/modifiers_impact/factor' },
      { field: 'coverages/ws/adjusted_base_rate' },
      { field: 'coverages/ws/minimum_rate' },
      { field: 'coverages/ws/final_modified_rate' },

      // ✅ Hide if excess wind hail selected
      { field: 'coverages/ws/deductible_type/value', shownBy: "/cds/excess_wind_hail_not_selected" },

      // ✅ Hide if excess wind hail selected
      { field: "coverages/ws/deductible", shownBy: "/cds/excess_wind_hail_not_selected", infoBy: "/cds/validation/ws_deductible/info_text" },

      // ✅ Hide if excess wind hail selected
      { field: 'coverages/ws/deductible_all_perils', shownBy: "/cds/excess_wind_hail_not_selected" },

      // ✅ Hide if excess wind hail NOT selected
      { field: 'coverages/ws/xs_building_coverage', shownBy: "/cds/excess_wind_hail_selected" },
      { field: 'coverages/ws/xs_contents_coverage', shownBy: "/cds/excess_wind_hail_selected" },

      // ✅ Hide if excess wind hail selected
      { field: 'coverages/ws/minimum_deductible', shownBy: "/cds/excess_wind_hail_not_selected" },
      { field: 'coverages/ws/final_deductible', shownBy: "/cds/excess_wind_hail_not_selected" },
      { field: 'coverages/ws/deductible_impact', shownBy: "/cds/excess_wind_hail_not_selected" },
      'coverages/ws/model_premium',
      'coverages/ws/model_rate',
    ]
    ,
    shownBy: "show_ws_options",
    showLockedTableBy: "/cds/lock_layer",
    collection_field: "show_full_pricing_tables_ws",
    isLockedTableEnabled: true,
    outputFields: ['coverages/ws/tiv/value', 'coverages/ws/base_rate', 'coverages/ws/modifiers_impact/factor', 'coverages/ws/adjusted_base_rate', 'coverages/ws/minimum_rate', 'coverages/ws/final_modified_rate',
      'coverages/ws/minimum_deductible', 'coverages/ws/final_deductible', 'coverages/ws/deductible_impact', 'coverages/ws/model_premium', 'coverages/ws/model_rate',]
  },
  {
    title: "Liability", key: "liability", fields: [
      { field: 'coverages/liability/tiv/value' },
      { field: 'coverages/liability/base_rate' },
      { field: 'coverages/liability/modifiers_impact/factor' },
      'coverages/liability/model_premium',
      'coverages/liability/model_rate',
    ],
    // shownBy: "show_liability_options",
    // tableCollectionShownBy: "show_liability_collection_and_table",
    tableCollectionToggleField: "rating_factors/high_profile_client",
    // collection_field: "show_full_pricing_tables_liability",

  },
  {
    title: "Equipment Breakdown", key: "eb", fields: [
      'coverages/eb/tiv/value',
      { field: 'coverages/eb/base_rate' },
      { field: 'coverages/eb/modifiers_impact/factor' },
      'coverages/eb/deductible',
      'coverages/eb/deductible_impact',
      'coverages/eb/model_premium',
      'coverages/eb/model_rate',
    ],
    shownBy: "show_eb_options",
    showLockedTableBy: "/cds/lock_layer",
    collection_field: "show_full_pricing_tables_eb",
    notes_field: "notes/equipment_breakdown_note",
    isLockedTableEnabled: true,
    outputFields: ['coverages/eb/base_rate', 'coverages/eb/modifiers_impact/factor', 'coverages/eb/deductible_impact', 'coverages/eb/model_premium', 'coverages/eb/model_rate']
  },
  {
    title: "Excess FL", key: "fl", fields: [
      { field: 'coverages/fl/tiv/value' },
      { field: 'coverages/fl/base_rate' },
      { field: 'coverages/fl/modifiers_impact/factor' },
      { field: 'coverages/fl/adjusted_base_rate' },
      { field: 'coverages/fl/minimum_rate' },
      { field: 'coverages/fl/final_modified_rate' },
      'coverages/fl/xs_building_coverage',
      'coverages/fl/xs_contents_coverage',
      'coverages/fl/model_premium',
      'coverages/fl/model_rate',
    ],
    shownBy: "show_fl_options",
    collection_field: "show_full_pricing_tables_fl"
  },
  {
    title: "EQ", key: "eq", fields: [
      { field: 'coverages/eq/tiv/value' },
      { field: 'coverages/eq/base_rate' },
      { field: 'coverages/eq/modifiers_impact/factor' },
      { field: 'coverages/eq/adjusted_base_rate' },
      { field: 'coverages/eq/minimum_rate' },
      { field: 'coverages/eq/final_modified_rate' },
      'coverages/eq/deductible',
      'coverages/eq/deductible_impact',
      'coverages/eq/model_premium',
      'coverages/eq/model_rate',
    ],
    shownBy: "show_eq_options",
    showLockedTableBy: "/cds/lock_layer",
    collection_field: "show_full_pricing_tables_eq",
    isLockedTableEnabled: true,
    outputFields: ['coverages/eq/tiv/value', 'coverages/eq/base_rate', 'coverages/eq/modifiers_impact/factor', 'coverages/eq/adjusted_base_rate', 'coverages/eq/minimum_rate', 'coverages/eq/final_modified_rate',
      'coverages/eq/deductible_impact', 'coverages/eq/model_premium', 'coverages/eq/model_rate']
  },
];

export const paf_deductibles_configs = [
  {
    title: "PAF Options",
    fields: [
      'coverages/paf/deductible',
      'coverages/paf/deductible_impact',
      'coverages/paf/model_premium',
      'coverages/paf/model_rate',
    ],
    shownBy: "show_paf_options",
    showLockedTableBy: "/cds/lock_layer",
    isLockedTableEnabled: true,
    outputFields: ['coverages/paf/deductible_impact', 'coverages/paf/model_premium', 'coverages/paf/model_rate']
  },
];

export const kpi_splits_tables_configs = [
  {
    title: "Coverage Split By % TIV",
    fields: [
      "kpis/tiv_split/cov_a_perc",
      "kpis/tiv_split/cov_b_perc",
      "kpis/tiv_split/cov_c_perc",
      "kpis/tiv_split/others_perc",
    ],
  },
  {
    title: "Peril Split By % EL",
    collection_field: { "field": "kpis_show_aop_break_down", "shownBy": "show_aop_options" },
    fields: [
      { "field": "kpis/pflr_split/aop_perc", "shownBy": "show_aop_options" },
      { "field": "kpis/pflr_split/water_damage_perc", "shownBy": "/cds/kpis_show_aop_break_down" },
      { "field": "kpis/pflr_split/hail_perc", "shownBy": "/cds/kpis_show_aop_break_down" },
      { "field": "kpis/pflr_split/fire_perc", "shownBy": "/cds/kpis_show_aop_break_down" },
      { "field": "kpis/pflr_split/other_perc", "shownBy": "/cds/kpis_show_aop_break_down" },
      "kpis/pflr_split/liability_perc",
      // { "field": "kpis/pflr_split/liability_perc", "shownBy": "show_liability_options" },
      { "field": "kpis/pflr_split/ws_perc", "shownBy": "show_ws_options" },
      { "field": "kpis/pflr_split/eq_perc", "shownBy": "show_eq_options" },
      { "field": "kpis/pflr_split/fl_perc", "shownBy": "show_fl_options" },
      { "field": "kpis/pflr_split/eb_perc", "shownBy": "show_eb_options" },
      { "field": "kpis/pflr_split/paf_perc", "shownBy": "show_paf_options" },
    ],
  }
]

export const hvh_kpi_premiums_tables_configs = [
  {
    title: "HVH",
    fields: [
      { "field": "kpis/hvh/technical_premium/rate", "shownBy": "kpis_show_rates" },
      { "field": "kpis/hvh/technical_premium/premium", "shownBy": "kpis_show_premiums" },
      { "field": "kpis/hvh/commercial_premium_pre_uw_adj/rate", "shownBy": "kpis_show_rates" },
      { "field": "kpis/hvh/commercial_premium_pre_uw_adj/premium", "shownBy": "kpis_show_premiums" },

      { "field": "kpis/hvh/commercial_premium_pre_uw_adj/premium_splits/ho", "shownBy": "/cds/show_premium_splits" },
      { "field": "kpis/hvh/commercial_premium_pre_uw_adj/premium_splits/eq", "shownBy": "/cds/show_premium_splits" },
      { "field": "kpis/hvh/commercial_premium_pre_uw_adj/premium_splits/excess_flood", "shownBy": "/cds/show_premium_splits" },
      { "field": "kpis/hvh/commercial_premium_pre_uw_adj/premium_splits/equipment_breakdown", "shownBy": "/cds/show_premium_splits" },

      { "field": "kpis/hvh/commercial_premium_pre_uw_adj/rate_splits/ho", "shownBy": "/cds/show_rate_splits" },
      { "field": "kpis/hvh/commercial_premium_pre_uw_adj/rate_splits/eq", "shownBy": "/cds/show_rate_splits" },
      { "field": "kpis/hvh/commercial_premium_pre_uw_adj/rate_splits/excess_flood", "shownBy": "/cds/show_rate_splits" },
      { "field": "kpis/hvh/commercial_premium_pre_uw_adj/rate_splits/equipment_breakdown", "shownBy": "/cds/show_rate_splits" },

      { "field": "kpis/hvh/commercial_premium/rate", "shownBy": "kpis_show_rates" },
      { "field": "kpis/hvh/commercial_premium/premium", "shownBy": "kpis_show_premiums" },

      { "field": "kpis/hvh/commercial_premium/premium_splits/ho", "shownBy": "/cds/show_premium_splits" },
      { "field": "kpis/hvh/commercial_premium/premium_splits/eq", "shownBy": "/cds/show_premium_splits" },
      { "field": "kpis/hvh/commercial_premium/premium_splits/excess_flood", "shownBy": "/cds/show_premium_splits" },
      { "field": "kpis/hvh/commercial_premium/premium_splits/equipment_breakdown", "shownBy": "/cds/show_premium_splits" },

      { "field": "kpis/hvh/commercial_premium/rate_splits/ho", "shownBy": "/cds/show_rate_splits" },
      { "field": "kpis/hvh/commercial_premium/rate_splits/eq", "shownBy": "/cds/show_rate_splits" },
      { "field": "kpis/hvh/commercial_premium/rate_splits/excess_flood", "shownBy": "/cds/show_rate_splits" },
      { "field": "kpis/hvh/commercial_premium/rate_splits/equipment_breakdown", "shownBy": "/cds/show_rate_splits" },

      "kpis/hvh/modifiers/uw_adjustment",
    ],
    showLockedTableBy: "/cds/lock_layer",
    isLockedTableEnabled: true,
    outputFields: ["kpis/hvh/technical_premium/rate", "kpis/hvh/technical_premium/premium", "kpis/hvh/commercial_premium_pre_uw_adj/rate", "kpis/hvh/commercial_premium_pre_uw_adj/premium",
      "kpis/hvh/commercial_premium_pre_uw_adj/premium_splits/ho", "kpis/hvh/commercial_premium_pre_uw_adj/premium_splits/eq", "kpis/hvh/commercial_premium_pre_uw_adj/premium_splits/excess_flood",
      "kpis/hvh/commercial_premium_pre_uw_adj/premium_splits/equipment_breakdown", "kpis/hvh/commercial_premium_pre_uw_adj/rate_splits/ho", "kpis/hvh/commercial_premium_pre_uw_adj/rate_splits/eq",
      "kpis/hvh/commercial_premium_pre_uw_adj/rate_splits/excess_flood", "kpis/hvh/commercial_premium_pre_uw_adj/rate_splits/equipment_breakdown", "kpis/hvh/commercial_premium/premium_splits/ho",
      "kpis/hvh/commercial_premium/premium_splits/eq", "kpis/hvh/commercial_premium/premium_splits/excess_flood", "kpis/hvh/commercial_premium/premium_splits/equipment_breakdown",
      "kpis/hvh/commercial_premium/rate_splits/ho", "kpis/hvh/commercial_premium/rate_splits/eq", "kpis/hvh/commercial_premium/rate_splits/excess_flood",
      "kpis/hvh/commercial_premium/rate_splits/equipment_breakdown", "kpis/hvh/modifiers/uw_adjustment"],
  }
]

export const paf_kpi_premiums_tables_configs = [
  {
    title: "PAF",
    fields: [
      { "field": "kpis/paf/technical_premium/rate", "shownBy": "kpis_show_rates" },
      { "field": "kpis/paf/technical_premium/premium", "shownBy": "kpis_show_premiums" },
      { "field": "kpis/paf/commercial_premium_pre_uw_adj/rate", "shownBy": "kpis_show_rates" },
      { "field": "kpis/paf/commercial_premium_pre_uw_adj/premium", "shownBy": "kpis_show_premiums" },
      { "field": "kpis/paf/commercial_premium/rate", "shownBy": "kpis_show_rates" },
      { "field": "kpis/paf/commercial_premium/premium", "shownBy": "kpis_show_premiums" },
      "kpis/paf/modifiers/uw_adjustment",
    ],
    shownBy: "show_paf_options",
    showLockedTableBy: "/cds/lock_layer",
    isLockedTableEnabled: true,
    outputFields: ["kpis/paf/technical_premium/rate", "kpis/paf/technical_premium/premium", "kpis/paf/commercial_premium_pre_uw_adj/rate", "kpis/paf/commercial_premium_pre_uw_adj/premium",
      "kpis/paf/commercial_premium/rate", "kpis/paf/commercial_premium/premium", "kpis/paf/modifiers/uw_adjustment"]
  }
]

export const total_kpi_premiums_tables_configs = [
  {
    title: "Total",
    fields: [
      { field: "status", shownBy: "/cds/validation/status/valid" },
      { field: "status.notSupported", shownBy: "/cds/validation/status/invalid", infoBy: "/cds/validation/status/info_text" },
      { "field": "kpis/total/technical_premium/rate", "shownBy": "kpis_show_rates" },
      { "field": "kpis/total/technical_premium/premium", "shownBy": "kpis_show_premiums" },
      { "field": "kpis/total/commercial_premium_pre_uw_adj/rate", "shownBy": "kpis_show_rates" },
      { "field": "kpis/total/commercial_premium_pre_uw_adj/premium", "shownBy": "kpis_show_premiums" },
      { "field": "kpis/total/commercial_premium/rate", "shownBy": "kpis_show_rates" },
      { "field": "kpis/total/commercial_premium/premium", "shownBy": "kpis_show_premiums" },
      "kpis/total/tpi_pre_uw_adj",
      "kpis/total/tpi",
      "kpis/total/pflr_pre_uw_adj",
      "kpis/total/pflr",
    ],
  },
]
