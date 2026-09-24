// v0.3.0
// If changing the max_layers below, you must also update in rate_constants to the same number
function max_layers() {
  return 6
}

function exposure_detail_years() {
  return Array.from({ length: 21 }, (_, i) => {
    const yearIndex = 20 - i;
    const entry = {
      datum: `exposure_details/year_${yearIndex}`, // starts at year_19 down to year_0
      labelAlign: "center",
      labelBy: `exposure_details_year_labels/year_${yearIndex}`,
    };

    if (yearIndex === 0) {
      entry.infoBy = "/cds/hover_info/latest_policy_year";
    }

    if (yearIndex == 20) {
      entry.infoBy = "/cds/hover_info/calculated_policy_year";
    }

    return entry;
  });
}

// function claims_summary_years_15() {
//   return Array.from({ length: 15 }, (_, i) => ({
//     datum: `claims_summary/year_${14 - i}`, // starts at year_14 down to year_0
//     labelAlign: "center",
//     labelBy: `claims_summary/year_${14 - i}/policy_year`
//   }));
// }

function claims_summary_years_15() {
  return Array.from({ length: 16 }, (_, i) => ({
    datum: `claims_summary/year_${15 - i}`, // starts at year_15 down to year_0
    labelAlign: "center",
    labelBy: `claims_summary/year_${15 - i}/policy_year`
  }));
}

function claims_summary_years_20() {
  return Array.from({ length: 21 }, (_, i) => ({
    datum: `claims_summary/year_${20 - i}`, // starts at year_15 down to year_0
    labelAlign: "center",
    labelBy: `claims_summary/year_${20 - i}/policy_year`
  }));
}

export { max_layers, exposure_detail_years, claims_summary_years_15, claims_summary_years_20 };
