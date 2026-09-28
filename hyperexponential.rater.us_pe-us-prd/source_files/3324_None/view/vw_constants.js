function get_quotes() {
  const options = [];
  for (let i = 1; i < 11; i++) {
    options.push(`quotes/quote_${i}`);
  }

  return options;
}

function get_quote_options() {
  const options = [];
  for (let i = 1; i < 11; i++) {
    options.push(`coverage_option_${i}`);
    options.push(`comment_${i}`);
  }

  return options;
}


export {
  get_quote_options,
  get_quotes,
};
