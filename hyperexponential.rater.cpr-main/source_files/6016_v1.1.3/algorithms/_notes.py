##############################################################################################################################
################                             Notes                                                            ################ 
##############################################################################################################################

### 1) This table needs to be updated annually it is used in the rate change calculation, algorithm wont fall over if it is not updated but it will use slightly out of date ihs factors on the expiring policy
        # Table: tbl_ihs_static_data;
        # Excel File to assist: \\bfl.local\UK\Groups\Finance\Actuarial\Pricing\01 - Property\JB\cpr\ihs table.xlsx 
### 2) Day 2: consider if political exposure adjustments to simulation woudl be better happening before sinulation ref: Exposure Details line 1013
### 3) DAY 2: check 0.01 in implied_pod_capped - relected 0.01 per model but AAA pod is 0.0000001 {implied_pod_capped          = min(1,    max(0.01,   implied_pod))}  ref: rate_rating_summary line 271 - better code shown at relevant lines albeit commented out
### 4) DAY 2: Currently political side of model changes little if at all by term, discussed with AC and suggestion was to be investigated day 2
### 5) DAY 2: Consider rate change and country details table on political risk - when v2 library goes live we would ideally separate exposure change on on existing country from newly added country (which probably belongs in a different bucket) 

##############################################################################################################################



