import * as HX from "hx-model-components";
import { wrapWith, getNodeValue, renderWithShownBy } from "../common/utilities";

const NULL_DATA_LITERAL = "__CUIC_TABLE_NULL_DATA__";
const NULL_FIELD_LITERAL = "__CUIC_TABLE_NULL_FIELD__";
const NULL_FILTER_LITERAL = "__CUIC_TABLE_NULL_FILTER__";

const TableNoEmptyRow = HX.buildCustomComponent({
    apiVersion: "1.0.0",
    propTypes: {
        data: HX.PropTypes.arrayOfType(
            HX.PropTypes.oneOfType([
                HX.PropTypes.path,
                HX.PropTypes.objectOfType({
                    datum: HX.PropTypes.path.optional,
                    labelBy: HX.PropTypes.path.optional,
                    infoBy: HX.PropTypes.path.optional,
                    labelAlign: HX.PropTypes.string.optional,
                    width: HX.PropTypes.number.optional,
                    minWidth: HX.PropTypes.number.optional,
                    maxWidth: HX.PropTypes.number.optional,
                }),
                HX.PropTypes.oneOfLiteral([null, NULL_DATA_LITERAL]),
            ]),
        ),
        fields: HX.PropTypes.arrayOfType(
            HX.PropTypes.oneOfType([
                HX.PropTypes.field,
                HX.PropTypes.objectOfType({
                    field: HX.PropTypes.field.optional,
                    shownBy: HX.PropTypes.path.optional,
                    labelBy: HX.PropTypes.path.optional,
                    infoBy: HX.PropTypes.path.optional,
                    labelAlign: HX.PropTypes.string.optional,
                    width: HX.PropTypes.number.optional,
                    minWidth: HX.PropTypes.number.optional,
                    maxWidth: HX.PropTypes.number.optional,
                }),
                HX.PropTypes.oneOfLiteral([null, NULL_FIELD_LITERAL]),
            ]),
        ),
        with: HX.PropTypes.path.optional,
        shownBy: HX.PropTypes.path.optional,
        title: HX.PropTypes.string.optional,
        filter: HX.PropTypes.oneOfType([
            HX.PropTypes.path,
            HX.PropTypes.oneOfLiteral([null, NULL_FILTER_LITERAL]),
            HX.PropTypes.arrayOfType(
                HX.PropTypes.oneOfType([
                    HX.PropTypes.path,
                    HX.PropTypes.oneOfLiteral([null, NULL_FILTER_LITERAL]),
                ]),
            ),
        ]).optional,
        transpose: HX.PropTypes.boolean.optional,
        dynamic: HX.PropTypes.boolean.optional,
        "kb-interactive": HX.PropTypes.boolean.optional,
        maxListVisibleRows: HX.PropTypes.number.optional,
        minListVisibleRows: HX.PropTypes.number.optional,
        freezeLeft: HX.PropTypes.number.optional,
        freezeRight: HX.PropTypes.number.optional,
        syncColumnWidthsKey: HX.PropTypes.string.optional,
        rowHeaderSettings: HX.PropTypes.objectOfType({
            width: HX.PropTypes.number.optional,
            minWidth: HX.PropTypes.number.optional,
            maxWidth: HX.PropTypes.number.optional,
        }).optional,
    },
    mapper: (props) => {
        const fieldConfigs = normaliseFields(props.fields ?? []);
        const rowConfigs = normaliseRows(props, fieldConfigs);

        const columnNodes = fieldConfigs.map((field) => ({
            label: field.labelByPath
                ? { type: "static", path: wrapWith(field.labelByPath, props.with) }
                : { type: "const", value: undefined },
            shown: field.shownByPath
                ? { type: "static", path: wrapWith(field.shownByPath, props.with) }
                : { type: "const", value: true },
            info: field.infoByPath
                ? { type: "static", path: wrapWith(field.infoByPath, props.with) }
                : { type: "const", value: undefined },
        }));

        const rowNodes = rowConfigs.map((row) => buildRowNode(row));

        return {
            nodes: {
                shownBy: props.shownBy
                    ? { type: "static", path: props.shownBy }
                    : { type: "const", value: true },
                columns: columnNodes,
                rows: rowNodes,
            },
        };
    },
    render: (props, data, tools) => {
        const fieldConfigs = normaliseFields(props.fields ?? []);
        const rowConfigs = normaliseRows(props, fieldConfigs);

        if (props.transpose && tools) {
            tools.log(
                "table_no_empty_row currently renders in row orientation; transpose is ignored.",
            );
        }

        const columns = fieldConfigs.map((field, index) => {
            const columnNode = data.nodes.columns?.[index];
            const shown = columnNode ? Boolean(getNodeValue(columnNode.shown)) : true;
            const labelFromNode = columnNode ? getNodeValue(columnNode.label) : undefined;
            const info = columnNode ? getNodeValue(columnNode.info) : undefined;

            const fallbackLabel = field.fieldPath
                ? field.fieldPath.split("/").pop()?.replace(/_/g, " ")
                : "";

            return {
                key: field.key,
                shown,
                label: labelFromNode ?? fallbackLabel ?? "",
                info,
                width: field.width,
                minWidth: field.minWidth,
                maxWidth: field.maxWidth,
                labelAlign: field.labelAlign,
            };
        });

        const rowsData = data.nodes.rows ?? [];
        const renderedRows = [];

        rowsData.forEach((rowNode, rowIndex) => {
            const rowConfig = rowConfigs[rowIndex];
            if (!rowConfig || rowConfig.kind !== "row") {
                return;
            }

            const listNode = rowNode?.list;
            const structureNode = rowNode?.structure;

            if (listNode && !listNode.pathError && listNode.nodeId) {
                const elements = listNode.elements?.filter(Boolean) ?? [];
                elements.forEach((element, elementIndex) => {
                    if (!element) {
                        return;
                    }

                    if (rowConfig.listFilterPath) {
                        const filterNode = element.nodes?.__filter;
                        if (filterNode && !isTruthy(getNodeValue(filterNode))) {
                            return;
                        }
                    }

                    const cells = {};
                    fieldConfigs.forEach((field) => {
                        const fieldNode = element.nodes?.[field.key];
                        const value = fieldNode ? getNodeValue(fieldNode) : undefined;
                        cells[field.key] = { value, node: fieldNode };
                    });

                    if (rowHasOnlyZeroes(cells, columns)) {
                        return;
                    }

                    const label = deriveListRowLabel(
                        element,
                        rowNode,
                        rowConfig,
                        elementIndex,
                    );

                    renderedRows.push({
                        key: `${rowIndex}-${element.listIndex}`,
                        label,
                        labelAlign: rowConfig.headerAlign,
                        labelWidth: rowConfig.headerWidth,
                        labelMinWidth: rowConfig.headerMinWidth,
                        labelMaxWidth: rowConfig.headerMaxWidth,
                        cells,
                    });
                });
                return;
            }

            if (!structureNode) {
                return;
            }

            if (rowConfig.structureFilterPath) {
                const filterNode = structureNode.__filter;
                if (filterNode && !isTruthy(getNodeValue(filterNode))) {
                    return;
                }
            }

            const cells = {};
            fieldConfigs.forEach((field) => {
                const fieldNode = structureNode[field.key];
                const value = fieldNode ? getNodeValue(fieldNode) : undefined;
                cells[field.key] = { value, node: fieldNode };
            });

            if (rowHasOnlyZeroes(cells, columns)) {
                return;
            }

            const label = deriveStructureRowLabel(rowNode, rowConfig, rowIndex);

            renderedRows.push({
                key: `${rowIndex}`,
                label,
                labelAlign: rowConfig.headerAlign,
                labelWidth: rowConfig.headerWidth,
                labelMinWidth: rowConfig.headerMinWidth,
                labelMaxWidth: rowConfig.headerMaxWidth,
                cells,
            });
        });

        const displayedColumns = columns.filter((column) => column.shown);
        const headerBaseStyle = createSizeStyle(props.rowHeaderSettings);

        const table = (
            <div className="table-no-empty-row">
                {props.title ? (
                    <h3 className="table-no-empty-row__title">{props.title}</h3>
                ) : null}
                <table className="table-no-empty-row__table">
                    <thead>
                        <tr>
                            <th
                                className="table-no-empty-row__header table-no-empty-row__header--row-label"
                                style={headerBaseStyle}
                            />
                            {displayedColumns.map((column) => (
                                <th
                                    key={column.key}
                                    className="table-no-empty-row__header"
                                    style={createColumnStyle(column)}
                                >
                                    {column.label}
                                </th>
                            ))}
                        </tr>
                    </thead>
                    <tbody>
                        {renderedRows.length === 0 ? (
                            <tr>
                                <td
                                    className="table-no-empty-row__cell table-no-empty-row__cell--empty"
                                    colSpan={displayedColumns.length + 1}
                                >
                                    No rows to display
                                </td>
                            </tr>
                        ) : (
                            renderedRows.map((row) => {
                                const rowHeaderStyle = {
                                    ...headerBaseStyle,
                                    ...overrideRowHeaderStyle(row),
                                };

                                return (
                                    <tr key={row.key}>
                                        <th
                                            className="table-no-empty-row__row-label"
                                            style={rowHeaderStyle}
                                        >
                                            {row.label}
                                        </th>
                                        {displayedColumns.map((column) => {
                                            const cell = row.cells[column.key];
                                            return (
                                                <td
                                                    key={column.key}
                                                    className="table-no-empty-row__cell"
                                                    style={createColumnStyle(column)}
                                                >
                                                    {formatValue(cell?.value)}
                                                </td>
                                            );
                                        })}
                                    </tr>
                                );
                            })
                        )}
                    </tbody>
                </table>
            </div>
        );

        return renderWithShownBy(data.nodes.shownBy, table);
    },
});

function normaliseFields(fields) {
    return fields.map((entry, index) => {
        if (entry === null || entry === undefined) {
            return {
                key: `field_${index}`,
                fieldPath: null,
                shownByPath: null,
                labelByPath: null,
                infoByPath: null,
                labelAlign: null,
                width: null,
                minWidth: null,
                maxWidth: null,
            };
        }

        if (typeof entry === "string") {
            return {
                key: `field_${index}`,
                fieldPath: entry,
                shownByPath: null,
                labelByPath: null,
                infoByPath: null,
                labelAlign: null,
                width: null,
                minWidth: null,
                maxWidth: null,
            };
        }

        return {
            key: `field_${index}`,
            fieldPath: entry.field ?? null,
            shownByPath: entry.shownBy ?? null,
            labelByPath: entry.labelBy ?? null,
            infoByPath: entry.infoBy ?? null,
            labelAlign: entry.labelAlign ?? null,
            width: entry.width ?? null,
            minWidth: entry.minWidth ?? null,
            maxWidth: entry.maxWidth ?? null,
        };
    });
}

function normaliseRows(props, fieldConfigs) {
    const dataEntries = props.data ?? [];
    const filters = normaliseFilter(props.filter, dataEntries.length);

    return dataEntries.map((entry, index) => {
        if (entry === null || entry === undefined || entry === NULL_DATA_LITERAL) {
            return { kind: "separator" };
        }

        if (typeof entry === "string") {
            return buildRowConfig(
                { datum: entry },
                filters[index] ?? null,
                props.with,
                fieldConfigs,
                index,
            );
        }

        if (typeof entry === "object" && entry.datum) {
            return buildRowConfig(
                entry,
                filters[index] ?? null,
                props.with,
                fieldConfigs,
                index,
            );
        }

        return { kind: "separator" };
    });
}

function normaliseFilter(filterProp, count) {
    if (filterProp === undefined || filterProp === null || filterProp === NULL_FILTER_LITERAL) {
        return new Array(count).fill(null);
    }

    if (Array.isArray(filterProp)) {
        return Array.from({ length: count }, (_, idx) => {
            const value = filterProp[idx];
            if (value === undefined || value === null || value === NULL_FILTER_LITERAL) {
                return null;
            }
            return value;
        });
    }

    return new Array(count).fill(filterProp);
}

function buildRowConfig(entry, filterPath, withProp, fieldConfigs, index) {
    const datumPath = entry.datum;
    if (!datumPath) {
        return { kind: "separator" };
    }

    const resolvedDatumPath = wrapWith(datumPath, withProp);

    const listFieldPaths = {};
    const structureFieldPaths = {};

    fieldConfigs.forEach((field) => {
        if (!field.fieldPath) {
            return;
        }

        listFieldPaths[field.key] = field.fieldPath;

        const structurePath = field.fieldPath.startsWith("/")
            ? field.fieldPath
            : `${resolvedDatumPath}/${field.fieldPath}`;

        structureFieldPaths[field.key] = structurePath;
    });

    const structureFilterPath = filterPath
        ? filterPath.startsWith("/")
            ? filterPath
            : `${resolvedDatumPath}/${filterPath}`
        : null;

    return {
        kind: "row",
        datumPath: resolvedDatumPath,
        listPath: resolvedDatumPath,
        listFieldPaths,
        structureFieldPaths,
        listLabelPath: entry.labelBy ?? null,
        structureLabelPath: entry.labelBy
            ? entry.labelBy.startsWith("/")
                ? entry.labelBy
                : `${resolvedDatumPath}/${entry.labelBy}`
            : null,
        listFilterPath: filterPath ?? null,
        structureFilterPath,
        headerAlign: entry.labelAlign ?? null,
        headerWidth: entry.width ?? null,
        headerMinWidth: entry.minWidth ?? null,
        headerMaxWidth: entry.maxWidth ?? null,
        originalIndex: index,
    };
}

function buildRowNode(rowConfig) {
    if (!rowConfig || rowConfig.kind !== "row") {
        return { type: "const", value: { kind: rowConfig?.kind ?? "separator" } };
    }

    const node = {};

    if (rowConfig.datumPath) {
        node.datumMetadata = { type: "static", path: rowConfig.datumPath };
    }

    if (rowConfig.listPath) {
        const listNodes = {};
        Object.entries(rowConfig.listFieldPaths ?? {}).forEach(([key, path]) => {
            if (path) {
                listNodes[key] = { type: "static", path };
            }
        });

        if (rowConfig.listLabelPath) {
            listNodes.__label = { type: "static", path: rowConfig.listLabelPath };
        }

        if (rowConfig.listFilterPath) {
            listNodes.__filter = { type: "static", path: rowConfig.listFilterPath };
        }

        if (Object.keys(listNodes).length > 0) {
            node.list = {
                type: "list",
                path: rowConfig.listPath,
                nodes: listNodes,
            };
        }
    }

    const structureNodes = {};
    Object.entries(rowConfig.structureFieldPaths ?? {}).forEach(([key, path]) => {
        if (path) {
            structureNodes[key] = { type: "static", path };
        }
    });

    if (rowConfig.structureLabelPath) {
        structureNodes.__label = { type: "static", path: rowConfig.structureLabelPath };
    }

    if (rowConfig.structureFilterPath) {
        structureNodes.__filter = { type: "static", path: rowConfig.structureFilterPath };
    }

    if (Object.keys(structureNodes).length > 0) {
        node.structure = structureNodes;
    }

    return node;
}

function rowHasOnlyZeroes(cells, columns) {
    const relevantColumns = columns.filter((column) => column.shown);
    if (relevantColumns.length === 0) {
        return false;
    }

    let hasComparableValue = false;

    const allZero = relevantColumns.every((column) => {
        const value = cells[column.key]?.value;

        if (value === undefined || value === null || value === "") {
            return true;
        }

        if (typeof value === "number") {
            if (!Number.isFinite(value)) {
                return false;
            }
            hasComparableValue = true;
            return value === 0;
        }

        if (typeof value === "boolean") {
            hasComparableValue = true;
            return value === false;
        }

        if (typeof value === "string") {
            const numericValue = Number(value);
            if (!Number.isNaN(numericValue)) {
                hasComparableValue = true;
                return numericValue === 0;
            }
        }

        return false;
    });

    return hasComparableValue && allZero;
}

function formatValue(value) {
    if (value === undefined || value === null) {
        return "";
    }

    if (typeof value === "number") {
        return Number.isFinite(value) ? value.toLocaleString() : value;
    }

    if (typeof value === "boolean") {
        return value ? "True" : "False";
    }

    return value;
}

function deriveListRowLabel(element, rowNode, rowConfig, fallbackIndex) {
    const explicitLabel = element.nodes?.__label
        ? getNodeValue(element.nodes.__label)
        : undefined;

    if (explicitLabel !== undefined && explicitLabel !== null && explicitLabel !== "") {
        return explicitLabel;
    }

    const metadataLabel = rowNode?.datumMetadata?.metadata?.view?.label;
    if (metadataLabel) {
        return `${metadataLabel} ${fallbackIndex + 1}`;
    }

    if (rowConfig.datumPath) {
        const segments = rowConfig.datumPath.split("/").filter(Boolean);
        const base = segments[segments.length - 1];
        if (base) {
            return `${base} ${fallbackIndex + 1}`;
        }
    }

    return `Row ${fallbackIndex + 1}`;
}

function deriveStructureRowLabel(rowNode, rowConfig, fallbackIndex) {
    const explicitLabel = rowNode.structure?.__label
        ? getNodeValue(rowNode.structure.__label)
        : undefined;

    if (explicitLabel !== undefined && explicitLabel !== null && explicitLabel !== "") {
        return explicitLabel;
    }

    const metadataLabel = rowNode?.datumMetadata?.metadata?.view?.label;
    if (metadataLabel) {
        return metadataLabel;
    }

    if (rowConfig.datumPath) {
        const segments = rowConfig.datumPath.split("/").filter(Boolean);
        const base = segments[segments.length - 1];
        if (base) {
            return base;
        }
    }

    return `Row ${fallbackIndex + 1}`;
}

function createSizeStyle(settings) {
    if (!settings) {
        return {};
    }

    const style = {};
    if (settings.width !== undefined && settings.width !== null) {
        style.width = `${settings.width}px`;
    }
    if (settings.minWidth !== undefined && settings.minWidth !== null) {
        style.minWidth = `${settings.minWidth}px`;
    }
    if (settings.maxWidth !== undefined && settings.maxWidth !== null) {
        style.maxWidth = `${settings.maxWidth}px`;
    }
    if (settings.labelAlign) {
        style.textAlign = settings.labelAlign;
    }
    return style;
}

function createColumnStyle(column) {
    const style = createSizeStyle(column);
    if (column.labelAlign) {
        style.textAlign = column.labelAlign;
    }
    return style;
}

function overrideRowHeaderStyle(row) {
    const style = {};
    if (row.labelWidth !== undefined && row.labelWidth !== null) {
        style.width = `${row.labelWidth}px`;
    }
    if (row.labelMinWidth !== undefined && row.labelMinWidth !== null) {
        style.minWidth = `${row.labelMinWidth}px`;
    }
    if (row.labelMaxWidth !== undefined && row.labelMaxWidth !== null) {
        style.maxWidth = `${row.labelMaxWidth}px`;
    }
    if (row.labelAlign) {
        style.textAlign = row.labelAlign;
    }
    return style;
}

function isTruthy(value) {
    if (typeof value === "boolean") {
        return value;
    }
    if (typeof value === "number") {
        return value !== 0;
    }
    return Boolean(value);
}

export default TableNoEmptyRow;
