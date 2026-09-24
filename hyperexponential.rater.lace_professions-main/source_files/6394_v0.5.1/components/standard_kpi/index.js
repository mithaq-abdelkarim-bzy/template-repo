import * as HX from "hx-model-components";
import { getNodeValue, renderWithShownBy } from "../common/utilities";

const CURRENCY_FIELDS = new Set([
    "quoted_premium_100",
    "technical_premium_100",
    "benchmark_premium_100",
]);

const PERCENT_FIELDS = new Set([
    "brokerage",
    "written_line",
    "tpi",
    "bpi",
    "tpi_pre_uw_adj",
    "bpi_pre_uw_adj",
    "pflr",
    "pflr_pre_uw_adj",
    "uw_adj_impact",
    "rate_change/risk_adjusted_rate_change",
    "rate_change/risk_adjusted_rate_change_case_priced",
]);

const FIELD_LABELS = {
    status: "Status",
    section_reference: "Section Reference",
    brokerage: "Brokerage",
    written_line: "Written Line",
    quoted_premium_100: "Quoted Premium",
    technical_premium_100: "Technical Premium",
    benchmark_premium_100: "Benchmark Premium",
    tpi: "TPI",
    bpi: "BPI",
    tpi_pre_uw_adj: "TPI (Pre-UW Adj)",
    bpi_pre_uw_adj: "BPI (Pre-UW Adj)",
    pflr: "Priced-for Loss Ratio",
    pflr_pre_uw_adj: "Priced-for Loss Ratio (Pre-UW Adj.)",
    uw_adj_impact: "Impact of Underwriting Adjustments",
    "rate_change/risk_adjusted_rate_change": "Risk Adjusted Rate Change",
    "rate_change/risk_adjusted_rate_change_case_priced": "Risk Adjusted Rate Change",
};

const listNodes = {
    include: { type: "static", path: "include" },
    status: { type: "static", path: "status" },
    section_reference: { type: "static", path: "section_reference" },
    brokerage: { type: "static", path: "brokerage" },
    written_line: { type: "static", path: "written_line" },
    premium_label: { type: "static", path: "premium_label" },
    quoted_premium_100: { type: "static", path: "quoted_premium_100" },
    technical_premium_100: { type: "static", path: "technical_premium_100" },
    benchmark_premium_100: { type: "static", path: "benchmark_premium_100" },
    tpi_quoted_100: { type: "static", path: "tpi_quoted_100" },
    tpi_bound_100: { type: "static", path: "tpi_bound_100" },
    tpi_quoted_100_incl_adj: { type: "static", path: "tpi_quoted_100_incl_adj" },
    tpi_bound_100_incl_adj: { type: "static", path: "tpi_bound_100_incl_adj" },
    bpi_quoted_100: { type: "static", path: "bpi_quoted_100" },
    bpi_bound_100: { type: "static", path: "bpi_bound_100" },
    bpi_quoted_100_incl_adj: { type: "static", path: "bpi_quoted_100_incl_adj" },
    bpi_bound_100_incl_adj: { type: "static", path: "bpi_bound_100_incl_adj" },
    pflr: { type: "static", path: "pflr" },
    pflr_pre_uw_adj: { type: "static", path: "pflr_pre_uw_adj" },
    uw_adj_impact: { type: "static", path: "uw_adj_impact" },
    risk_adjusted_rate_change: { type: "static", path: "rate_change/risk_adjusted_rate_change" },
    risk_adjusted_rate_change_case_priced: { type: "static", path: "rate_change/risk_adjusted_rate_change_case_priced" },
};

const formatNumber = (value, decimals) => {
    if (value === null || value === undefined || value === "") return "";
    if (typeof value !== "number") return value;
    return value.toLocaleString(undefined, {
        minimumFractionDigits: decimals,
        maximumFractionDigits: decimals,
    });
};

const formatValue = (field, value) => {
    if (value === null || value === undefined || value === "") return "";
    if (PERCENT_FIELDS.has(field) && typeof value === "number") {
        return `${formatNumber(value * 100, 1)}%`;
    }
    if (CURRENCY_FIELDS.has(field) && typeof value === "number") {
        return formatNumber(value, 0);
    }
    return value;
};

const isBoundLayer = (nodes) => ["Bound", "Post Bind Complete"].includes(getNodeValue(nodes.status));

const pricingNodeKey = (nodes, field) => {
    const premiumType = isBoundLayer(nodes) ? "bound" : "quoted";

    if (field === "tpi") return `tpi_${premiumType}_100_incl_adj`;
    if (field === "bpi") return `bpi_${premiumType}_100_incl_adj`;
    if (field === "tpi_pre_uw_adj") return `tpi_${premiumType}_100`;
    if (field === "bpi_pre_uw_adj") return `bpi_${premiumType}_100`;

    return field;
};

const fieldValue = (nodes, field) => {
    const fieldKey = field.includes("/") ? field.split("/").pop() : field;
    const nodeKey = fieldKey === "risk_adjusted_rate_change" || fieldKey === "risk_adjusted_rate_change_case_priced"
        ? fieldKey
        : pricingNodeKey(nodes, field);
    return getNodeValue(nodes[nodeKey]);
};

const labelFor = (nodes, field) => {
    if (field === "quoted_premium_100") {
        return getNodeValue(nodes.premium_label) || FIELD_LABELS[field];
    }
    if (["tpi", "bpi", "tpi_pre_uw_adj", "bpi_pre_uw_adj"].includes(field)) {
        const prefix = isBoundLayer(nodes) ? "Bound" : "Quoted";
        return `${prefix} ${FIELD_LABELS[field]}`;
    }
    return FIELD_LABELS[field] || field;
};

const KpiField = ({ nodes, field }) => (
    <div style={{ padding: "6px 8px" }}>
        <div style={{ fontSize: "11px", color: "#5f6670", marginBottom: "2px" }}>
            {labelFor(nodes, field)}
        </div>
        <div style={{ fontSize: "13px", fontWeight: 600 }}>
            {formatValue(field, fieldValue(nodes, field))}
        </div>
    </div>
);

const KpiGroup = ({ title, children }) => (
    <div style={{ marginTop: "10px" }}>
        <div style={{ fontSize: "13px", fontWeight: 700, marginBottom: "4px" }}>{title}</div>
        <div
            style={{
                display: "grid",
                gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))",
                border: "1px solid #d7dce2",
                borderRadius: "4px",
                overflow: "hidden",
            }}
        >
            {children}
        </div>
    </div>
);

const LayerCard = ({ nodes, title, collapsed, onToggle, showRaterPriced, showCasePriced, showRenewal }) => (
    <div
        style={{
            border: "1px solid #c9d0d8",
            borderRadius: "6px",
            marginBottom: "14px",
            backgroundColor: "#fff",
            overflow: "hidden",
        }}
    >
        <button
            type="button"
            onClick={onToggle}
            style={{
                alignItems: "center",
                backgroundColor: "#f6f8fa",
                border: "0",
                borderBottom: collapsed ? "0" : "1px solid #d7dce2",
                cursor: "pointer",
                display: "flex",
                font: "inherit",
                justifyContent: "space-between",
                padding: "12px",
                textAlign: "left",
                width: "100%",
            }}
        >
            <span style={{ fontSize: "16px", fontWeight: 700 }}>{title}</span>
            <span style={{ fontSize: "13px", fontWeight: 700 }}>{collapsed ? "Expand" : "Collapse"}</span>
        </button>
        {collapsed ? null : (
            <div style={{ padding: "12px" }}>
                <KpiGroup title="Risk Details">
                    <KpiField nodes={nodes} field="status" />
                    <KpiField nodes={nodes} field="section_reference" />
                    <KpiField nodes={nodes} field="brokerage" />
                    <KpiField nodes={nodes} field="written_line" />
                </KpiGroup>
                <KpiGroup title="Pricing">
                    <KpiField nodes={nodes} field="quoted_premium_100" />
                    <KpiField nodes={nodes} field="technical_premium_100" />
                    <KpiField nodes={nodes} field="benchmark_premium_100" />
                    <KpiField nodes={nodes} field="tpi" />
                    <KpiField nodes={nodes} field="bpi" />
                    {showRaterPriced ? <KpiField nodes={nodes} field="tpi_pre_uw_adj" /> : null}
                    {showRaterPriced ? <KpiField nodes={nodes} field="bpi_pre_uw_adj" /> : null}
                </KpiGroup>
                {showRaterPriced ? (
                    <KpiGroup title="Expected Loss Ratio">
                        <KpiField nodes={nodes} field="pflr" />
                        <KpiField nodes={nodes} field="pflr_pre_uw_adj" />
                        <KpiField nodes={nodes} field="uw_adj_impact" />
                    </KpiGroup>
                ) : null}
                {showCasePriced ? (
                    <KpiGroup title="Expected Loss Ratio">
                        <KpiField nodes={nodes} field="pflr" />
                    </KpiGroup>
                ) : null}
                {showRenewal ? (
                    <KpiGroup title="Rate Change">
                        {showRaterPriced ? <KpiField nodes={nodes} field="rate_change/risk_adjusted_rate_change" /> : null}
                        {showCasePriced ? <KpiField nodes={nodes} field="rate_change/risk_adjusted_rate_change_case_priced" /> : null}
                    </KpiGroup>
                ) : null}
            </div>
        )}
    </div>
);

const StandardKpi = HX.buildCustomComponent({
    apiVersion: "1.0.0",
    propTypes: {
        layersPath: HX.PropTypes.path,
        additionalLayersPath: HX.PropTypes.path,
        shownBy: HX.PropTypes.path.optional,
    },
    mapper: (props) => ({
        nodes: {
            shownBy: props.shownBy
                ? { type: "static", path: props.shownBy }
                : { type: "const", value: true },
            isRaterPriced: { type: "static", path: "cds/standard_fields/is_rater_priced" },
            isCasePriced: { type: "static", path: "cds/standard_fields/is_case_priced" },
            isRenewal: { type: "static", path: "cds/standard_fields/is_renewal" },
            layers: {
                type: "list",
                path: props.layersPath,
                nodes: listNodes,
                offset: 0,
                limit: 100,
            },
            additionalLayers: {
                type: "list",
                path: props.additionalLayersPath,
                nodes: listNodes,
                offset: 0,
                limit: 100,
            },
        },
        state: { collapsedLayers: {} },
    }),
    render: (props, data) => {
        const showRaterPriced = Boolean(getNodeValue(data.nodes.isRaterPriced));
        const showCasePriced = Boolean(getNodeValue(data.nodes.isCasePriced));
        const showRenewal = Boolean(getNodeValue(data.nodes.isRenewal));
        const collapsedLayers = data.state.collapsedLayers || {};
        const toggleLayer = (key) => {
            data.setState({
                ...data.state,
                collapsedLayers: {
                    ...collapsedLayers,
                    [key]: !collapsedLayers[key],
                },
            });
        };

        const renderList = (list, titlePrefix, keyPrefix) =>
            (list.elements || [])
                .filter((element) => element && getNodeValue(element.nodes.include))
                .map((element, index) => {
                    const key = `${keyPrefix}-${element.listIndex}`;
                    return (
                        <LayerCard
                            key={key}
                            nodes={element.nodes}
                            title={`${titlePrefix} ${index + 1}`}
                            collapsed={Boolean(collapsedLayers[key])}
                            onToggle={() => toggleLayer(key)}
                            showRaterPriced={showRaterPriced}
                            showCasePriced={showCasePriced}
                            showRenewal={showRenewal}
                        />
                    );
                });

        return renderWithShownBy(
            data.nodes.shownBy,
            <div style={{ padding: "8px 0" }}>
                {renderList(data.nodes.layers, "Summary Layer", "layer")}
                {renderList(data.nodes.additionalLayers, "Summary Additional Layer", "additional-layer")}
            </div>,
        );
    },
});

export default StandardKpi;
