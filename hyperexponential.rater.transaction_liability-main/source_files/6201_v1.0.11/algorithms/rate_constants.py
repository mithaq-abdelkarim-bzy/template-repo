import pandas as pd
import algorithms.rate_utilities as utils

# If changing the max_layers below, you must also update in vw_constants to the same number
max_layers = 10

#Loss ratios
priced_to_lr = 0.5
benchmark_lr = 0.7

# Policyholder options
lst_policyholder = ["Buyer", "Seller"]

# Severity coverages
sev_cov = ["due_diligence", "disclosure", "general_warranties", "tax_warranties"]
sev_cov_label = ["Due Diligence", "Disclosure", "General Warranties", "Tax Warranties/Deed"]
sev_cov_incl_term = [False, False, True, True]
sev_cov_df = pd.DataFrame(list(zip(sev_cov, sev_cov_label, sev_cov_incl_term)), columns =['cov', 'label', 'incl_term_mod'])
sev_cov_dict = utils.df_to_dict(sev_cov_df, 'cov', ['label', 'incl_term_mod'])

# Severity adjustment limits
sev_adj_min = -0.5
sev_adj_max = 0.5

# Rating constants

max_discount = 0.5
total_limit_amt = 10e6
pml_factor = 1
base_rate = 0.018975	

# MBBEFD constants
sev_gen_param_weight = 0.25
sev_gen_param_mu =  0.0746710838261301

sev_base_rate = 0.018975

div_threshold = 0.1

# fundamental top up coverages 
eu_base_rate = .003
all_other_base_rate = .005