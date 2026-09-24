// # v0.5.1
// Utility function for views

// function createLayersList(n) {
//   const layers = [];
//   for (let i = 1; i <= n; i++) {
//     layers.push(`layer_${i}`); // Use backticks for template literals
//   }
//   layers.push(`fgu`)
//   return layers;
// }
function createLayersList(n) {
  const layers = [];
  for (let i = 1; i <= n; i++) {
    layers.push(`layer_${i.toString().padStart(2, '0')}`); // Use backticks for template literals
  }
  layers.push(`fgu`)
  return layers;
}

function createLayersListNoFgu(n) {
  const layers = [];
  for (let i = 1; i <= n; i++) {
    layers.push(`layer_${i.toString().padStart(2, '0')}`); // Use backticks for template literals
  }

  return layers;
}

function createLayersListSelector(n) {
  const layers = [];
  for (let i = 1; i <= n; i++) {
    layers.push(`layer_${i.toString().padStart(2, '0')}`); // Use backticks for template literals
  }
  // layers.push(`fgu`)
  return layers;
}

// Define the list of layers to loop through ["layer_1",..."layer_n"]
function createLayersList_las(n) {
  const layers = [];
  for (let i = 1; i <= n; i++) {
    // layers.push(`layer_${i}`); // Use backticks for template literals
    layers.push(`layer_${i.toString().padStart(2, '0')}`); // Use backticks for template literals
  }
  // layers.push(`fgu`)
  return layers;
}

// Create table Field with maxWidth and optional showBy list
function convertToFieldObjects(originalList, maxWidth = 150, shownByList = []) {
  return originalList.map((item, index) => {
    if (item === null) return null;

    const shownBy = shownByList[index] ?? null;
    return { field: item, maxWidth: maxWidth, shownBy: shownBy };
  });
}

function convertToDataObjects(originalList, options = {}) {
  const { maxWidth, shownByList = [], elementLabelBy } = options;

  return originalList.map((item, index) => {
    if (item === null) return null;

    const result = { datum: item };

    if (maxWidth !== undefined) {
      result.maxWidth = maxWidth;
    }

    if (shownByList.length > 0) {
      result.shownBy = shownByList[index] ?? null;
    }

    if (elementLabelBy !== undefined) {
      result.elementLabelBy = elementLabelBy;
    }

    return result;
  });
}

// Function to render all layers, using layer list and function as argument
function renderAllLayers(layersList, layerFunction) {
  const objects = [];
  layersList.forEach(layer => {
    objects.push(layerFunction(layer));
  });
  return objects;
}



// Function to create the node name with a number suffix and saving them to the objects list
function node_name_list_with_suffix(node_name, separator, max_number, suffix = "") {
  const objects = [];
  for (let n = 1; n <= max_number; n++) {

    // objects.push(`${node_name}${separator}${suffix}${n}`);

    const formattedNumber = n.toString().padStart(2, '0'); // Format as 01, 02, ..., 100, 101,
    objects.push(`${node_name}${separator}${suffix}${formattedNumber}`);
  }
  return objects
}

// Function to create the node name with a number suffix and saving them to the objects list. Result = layer_1/quoted_premium
function node_names_with_prefix(prefix, separator, max_number, level_separator, node_names) {
  const objects = [];
  for (let n = 1; n <= max_number; n++) {
    node_names.forEach(field => {

      // objects.push(`${prefix}${separator}${n}${level_separator}${field}`);
      const formattedNumber = n.toString().padStart(2, '0'); // Format as 01, 02, ..., 100, 101,
      objects.push(`${prefix}${separator}${formattedNumber}${level_separator}${field}`);
    });
  }
  return objects
}

// Function to create the node name with a number suffix and saving them to the objects list. Result = layer_1/quoted_premium
function add_prefix_to_list(prefix, nodes_list) {
  const objects = [];
  nodes_list.forEach(node_name => {
    objects.push(`${prefix}${node_name}`);
  });
  return objects
}

// export { createLayersList, createLayersList_las, convertToFieldObjects, renderAllLayers, node_name_list_with_suffix, node_names_with_prefix, convertToFieldObjectsPlusShowBy };
export { createLayersList, createLayersListNoFgu, createLayersListSelector, createLayersList_las, convertToDataObjects, convertToFieldObjects, renderAllLayers, node_name_list_with_suffix, node_names_with_prefix, add_prefix_to_list };
