// Reusable function to generate option tables for different coverages
import * as HX from "hx-model-components";
import SimpleToggle from "components/toggle";

/**
 * Generates option tables for a given set of coverages.
 * Each coverage defines a section with a table and an optional collection field.
 *
 * @param {Array} coverages - Array of coverage objects, each containing:
 *   - title: Section title
 *   - fields: Fields to be displayed in the table
 *   - shownBy: Conditional visibility of the section
 *   - tableCollectionShownBy: (Optional) Path to a boolean field used as shownBy for Collection/Table
 *   - tableCollectionToggleField: (Optional) Field used in a Collection to toggle tableCollectionShownBy
 *   - collection_field: (Optional) Field to be used as a collection
 *   - notes_field: (Optional) Field to be used for notes
 *   - isLockedTableEnabled: (Optional) Field to represent whether we should show a second table with the locked options based on Status=="Bound"
 *   - outputFields: (Optional) Field for each table which represents the list of nodes that are outputs - used to calculate when to add ".read_only"
 *   - showLockedTableBy (Optional) Field to boolean which represents whether we have any locked layers
 * @returns {JSX.Element[]} - Array of JSX elements representing option tables
 */
export function generate_tables(coverages) {
  const toReadOnlyField = (value, specialReadOnlyFields) => {
    if (typeof value !== "string") return value;

    // Some fields that we're validating might have this suffix, in which case we need to remove it to add ".read_only" 
    if (value.endsWith(".notSupported")) {
      return value.replace(/\.notSupported$/, ".read_only");
    }

    if (specialReadOnlyFields && Object.hasOwn(specialReadOnlyFields, value)) {
      return value + specialReadOnlyFields[value];
    }

    return value + ".read_only";
  };

  const isOutputField = (fieldName, outputFields) => {
    return outputFields?.includes(fieldName);
  };

  const transformFieldForReadOnly = (field, collectionField, outputFields, specialReadOnlyFields) => {
    // if it's a string, we convert it directly
    if (typeof field === "string") {
      return isOutputField(field, outputFields)
        ? field
        : toReadOnlyField(field, specialReadOnlyFields);
    }

    // if it's an object, we spread the object then convert only the field
    const { field: fieldName, ...rest } = field;

    return {
      ...rest,
      field: isOutputField(fieldName, outputFields)
        ? fieldName
        : toReadOnlyField(fieldName, specialReadOnlyFields),
      ...(collectionField
        ? { shownBy: rest.shownBy ?? collectionField }
        : {})
    };
  };

  return coverages.map(({ title, fields, shownBy, tableCollectionShownBy, tableCollectionToggleField, collection_field, notes_field, isLockedTableEnabled, outputFields, showLockedTableBy, specialReadOnlyFields }) => (
    // Provides context for the section, specifying that we are working within 'cds' struct
    <HX.With context={{ type: 'struct', path: 'cds' }}>
      {/* Section wrapper for the table */}
      <HX.Section title={title} shownBy={shownBy}>
        {tableCollectionShownBy && tableCollectionToggleField && (
          <HX.Pane flow="right">
            <HX.Collection
              fields={[tableCollectionToggleField]} // This collection acts as a toggle for tableCollectionShownBy
              shownBy={shownBy}
            />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
        )}
        {/* If a collection field is defined, render a Collection component */}
        {collection_field && (
          <HX.Pane flow="right">
            <HX.Collection
              fields={[collection_field]}
              shownBy={tableCollectionShownBy || shownBy}
            />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
        )}

        {/* If it's the HVH table, add the Toggle custom component */}
        {title === "HVH" && (
          <HX.Pane flow="right">
            <SimpleToggle boolNode="show_commercial_premium_breakdown" label="Commercial Premium Breakdown" />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>

        )}
        {/* Main table displaying layers and fields */}
        <HX.Pane flow="right">
          <HX.Table
            data={[{ datum: "layers", width: 250, elementLabelBy: 'layer_label' }]}
            fields={fields.map(field =>
              // If the field is a string, return it as is
              typeof field === 'string'
                ? field
                : {
                  // Spread the original field properties
                  ...field,
                  // If a collection field exists, apply its 'shownBy' property to the field
                  ...(collection_field ? { shownBy: field.shownBy || collection_field } : {})
                }
            )}
            syncColumnWidthsKey="options_table_column_widths"
            filter={isLockedTableEnabled ? "unlock_layers" : "show_layer"} // If we're not showing a locked table for the section, only show the full left table
            shownBy={tableCollectionShownBy || shownBy}
            freezeLeft={0}
            transpose
            kb-interactive
          />
          {isLockedTableEnabled && (
            <HX.Table
              data={[{ datum: "layers", width: 250, elementLabelBy: 'layer_label' }]}
              fields={fields.map((field) =>
                transformFieldForReadOnly(field, collection_field, outputFields, specialReadOnlyFields)
              )}
              syncColumnWidthsKey="options_table_column_widths"
              filter="lock_layers"
              shownBy={showLockedTableBy}  // if the boolean is true, it means that we have locked layers and should show the locked table
              freezeLeft={0}
              transpose
              kb-interactive
            />
          )}
        </HX.Pane>
        {notes_field && (
          <HX.Pane flow="right">
            <HX.Notes field={notes_field} />
            <HX.Pane />
            <HX.Pane />
            <HX.Pane />
          </HX.Pane>
        )}
      </HX.Section>
    </HX.With >
  ));
}
