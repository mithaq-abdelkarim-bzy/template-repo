import * as HX from "hx-model-components";

function underwriter_appetite() {
    return (
        <HX.Page title="Underwriter Appetite" fullWidth={true}>
            <HX.Section title="CAT Limit Framework Information">
                <HX.Notes field="info/cat_limit_framwork_msg" />
            </HX.Section>
            <HX.Selector data={["layers"]} dropdown="layer_label">
                <HX.Section title="Critical CAT Zone Summary">
                    <HX.Pane flow="right">
                        <HX.Table title="WS CAT Zone Summary"
                            data={["perils/named_windstorm/crit_cat_zone_total_summary"]}
                            fields={[
                                "cat_zone",
                                "exposed_limit_threshold",
                                "within_threshold"
                            ]}
                        />

                        <HX.Table title="EQ CAT Zone Summary"
                            data={["perils/quake/crit_cat_zone_total_summary"]}
                            fields={[
                                "cat_zone",
                                "exposed_limit_threshold",
                                "within_threshold"
                            ]}
                        />
                    </HX.Pane>
                </HX.Section>


                <HX.Section title="Critical CAT Zone Detail">
                    <HX.Pane flow="right">
                        <HX.Table title="WS CAT Zone Detail"
                            data={["perils/named_windstorm/crit_cat_zone_summary"]}
                            fields={[
                                "cat_zone",
                                "tiv",
                                "exposed_limit",
                                "exposed_limit_threshold",
                                "within_threshold",
                                "flood_zone_av_exposed_limit"
                            ]}
                        />

                        <HX.Table title="EQ CAT Zone Detail"
                            data={["perils/quake/crit_cat_zone_summary"]}
                            fields={[
                                "cat_zone",
                                "tiv",
                                "exposed_limit",
                                "exposed_limit_threshold",
                                "within_threshold"
                            ]}
                        />
                    </HX.Pane>
                </HX.Section>
                <HX.Section title="Gate Detail" defaultCollapsed={true}>
                    <HX.Pane flow="right">
                        <HX.Table title="WS Gate Detail"
                            data={["perils/named_windstorm/gate_appetite_summary"]}
                            fields={[
                                "gate",
                                "tiv",
                                "exposed_limit",
                                "flood_zone_av_exposed_limit"
                            ]}
                        />

                        <HX.Table title="EQ Gate Detail"
                            data={["perils/quake/gate_appetite_summary"]}
                            fields={[
                                "gate",
                                "tiv",
                                "exposed_limit"
                            ]}
                        />
                    </HX.Pane>
                </HX.Section>
            </HX.Selector>
        </HX.Page >
    )
}

export { underwriter_appetite };