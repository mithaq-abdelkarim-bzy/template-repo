import Plot from "react-plotly.js";
import * as HX from "hx-model-components";
import {
  commonPropTypes,
  getCommonNodes,
  renderWithShownBy,
  getNodeValue,
  wrapWith,
} from "../common/utilities";


function formatPercent(value, { decimals = 1, multiply = true } = {}) {
  // Handle null/undefined/""
  if (value === null || value === undefined || value === "") return "";

  // If it's already a string that ends with %, return as-is
  if (typeof value === "string" && value.trim().endsWith("%")) return value;

  const num = Number(value);
  if (Number.isNaN(num)) {
    // Non-numeric content gets returned unmodified
    return String(value);
  }

  // Many data sources store proportions (e.g., 0.123),
  // set multiply=true to turn 0.123 into 12.3%
  const scaled = multiply ? num * 100 : num;

  // Use Intl for locale-friendly formatting; you can tweak minimumFractionDigits/maximumFractionDigits
  const formatted = new Intl.NumberFormat(undefined, {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  }).format(scaled);

  return `${formatted}%`;
}

function formatFieldName(fieldName) {
  return fieldName
    .split('_') // Split the string into an array by the underscore
    .map(word => word.charAt(0).toUpperCase() + word.slice(1)) // Capitalize the first letter of each word
    .join(' '); // Join the words back with a space
}

function buildTableDataFromJSON(label, jsonString) {
  // Parse the JSON string into a JavaScript object
  const tableData = JSON.parse(jsonString);
  const colKeys = Object.keys(tableData);
  const headers = ["Index", ...colKeys.map((_, i) => String(i + 1))];   // First header is for the row index column, then numeric column headings 1..N

  // Determine the maximum number of entries across all years for proper row alignment
  // const maxRows = Math.max(...Object.values(yearsData).map(values => values.length));
  const maxRows = Math.max(0, ...Object.values(tableData).map(values => Array.isArray(values) ? values.length : 0));


  // Create the data table with row alignment, filling missing values with 'N/A'
  const rows = Array.from({ length: maxRows }, (_, rowIndex) => {
    const rowNumber = rowIndex + 1; // 1-based row index
    const interior = colKeys.map(colKey => {
      const raw = (tableData[colKey] && tableData[colKey][rowIndex] !== undefined)
        ? tableData[colKey][rowIndex]
        : "";
      return formatPercent(raw, { decimals: 1, multiply: true });
    });
    return [rowNumber, ...interior];
  });

  // Transpose the rows into columns to match Plotly's expected format
  const cells = headers.map((_, colIndex) => rows.map(row => row[colIndex]));

  return { headers, cells };
}

function getFieldValues(parentList) {
  if (!Array.isArray(parentList)) return "{}";

  const result = {};

  parentList.forEach((bigList, index) => {
    // If multiple row names are blank, it only sets to one key in the dictionary
    // Work around is to set it to random assortment of letters with index, and 
    // then check for those letter above and replace with empty string if so
    const key = bigList?.nodes?.parentListName?.value || `asfhlas ${index}`;
    result[key] = [
      ...new Set(
        (bigList?.nodes?.childList?.elements || []).map(
          element => element?.nodes?.field?.value
        ).filter(value => value !== undefined) // Exclude undefined values
      ),
    ];
  });

  return JSON.stringify(result, null, 2); // Convert dictionary to a JSON string with pretty formatting
}




const Matrix = HX.buildCustomComponent({
  apiVersion: "1.0.0",
  propTypes: {
    with: HX.PropTypes.path.optional,
    title: HX.PropTypes.string.optional,
    parentList: HX.PropTypes.path.required,
    parentListName: HX.PropTypes.path.required,
    childList: HX.PropTypes.path.required,
    field: HX.PropTypes.path.required,
  },
  mapper: (props) => ({
    nodes: {
      parentList: {
        type: "list",
        path: wrapWith(props.parentList, props.with),
        nodes: {
          parentListName: { type: "static", path: wrapWith(props.parentListName, props.with) },
          childList: {
            type: "list",
            path: wrapWith(props.childList, props.with),
            nodes: {
              field: { type: "static", path: wrapWith(props.field, props.with) },
            }
          }
        }
      }

    },
  }),

  render: (props, data, tools) => {

    const jsonData = getFieldValues(data.nodes.parentList.elements)
    const jsonStringDefault = '{"years": {"": [""]}}';
    // Need default value or else undefined hxd value crashes the cuic and it wont refresh
    const jsonString = (jsonData && jsonData !== '{}' && Object.keys(JSON.parse(jsonData)).length > 0)
      ? jsonData
      : jsonStringDefault;
    const label = data.nodes?.parentList?.nodes?.childList?.nodes?.field?.metadata?.view?.label || formatFieldName(props.field)
    const { headers, cells } = buildTableDataFromJSON(label, jsonString);


    const columnCount = headers.length;
    const perCellPx = 80;
    const extraPaddingPx = 50;
    const minPlotWidth = 600;                     // ensure it never collapses too small
    const totalWidth = Math.max(minPlotWidth, columnCount * perCellPx + extraPaddingPx);


    // tools.log(data.nodes?.parentList?.elements[0]?.childList?.elements[0]?.field || "")
    // const initialData = buildTableDataFromJSON(jsonString);
    // const [headers, setHeaders] = useState(initialData.headers);
    // const [cells, setCells] = useState(initialData.cells);

    return (
      <div>
        {/* <div style={{ marginBottom: '10px' }}>
          <button onClick={addRow} style={{ marginRight: '5px' }}>Add Row</button>
          <button onClick={addColumn}>Add Column</button>
        </div> */}
        {/* Table Plot */}

        <div style={{ overflowX: 'auto', overflowY: 'hidden', maxWidth: '100%' }}>
          <div style={{ width: `${totalWidth}px` }}>

            <Plot
              data={[
                {
                  type: 'table',
                  header: {
                    values: headers,
                    align: "center",
                    line: { width: 1, color: '#326B9F' },
                    fill: { color: "white" },
                    font: { family: "Acid Grotesk", size: 18, color: "#0F124C" }, // Increased font size for header
                    height: 40, // Increase header height for more spacing
                  },
                  cells: {
                    values: cells,
                    align: "center",
                    line: { color: "#326B9F", width: 0.5 },
                    fill: { color: ['white', '#F1F9FB'] },
                    font: { family: "Acid Grotesk", size: 16, color: ["0F124C", "black"] }, // Increased font size for cells
                    height: 35, // Increase the cell height
                    padding: 5, // Add padding to the cells for extra space
                    // Set max width to 250px for each cell
                    width: perCellPx, // keep in sync with totalWidth calc
                  }
                }
              ]}
              layout={{
                title: {
                  text: props.title || '',     // <<< use the passed string
                  font: { family: 'Acid Grotesk', size: 16, color: 'black' },
                  x: 0,
                  xanchor: 'left',
                },
                margin: { l: 40, r: 40, t: props.title ? 60 : 30, b: 20 }, // extra top margin if title exists

                autosize: false,   // control width explicitly for horizontal scroll
                width: totalWidth, // critical to make content overflow horizontally
                datarevision: Date.now()
              }}
              style={{ width: `${totalWidth}px`, height: "100%" }}
              useResizeHandler={true}
              config={{ responsive: true }}
              key={JSON.stringify(headers)}





            />

          </div>
        </div>
      </div >
    );
  }
});

export default Matrix;
