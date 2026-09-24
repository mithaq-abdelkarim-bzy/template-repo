# Known Differences vs Excel:
1	IHS factors were reversed in old model
2	New National Mourning Approach
3	Simulation logic - old was partial run (now all cvg); old was 50% wgt (now 100%); old didn’t scale
4	Old National Mourning Approach treated a 1 day event as nil days … 19/12-19/12 = 0; 19/12-20/12=1 … these are now 1 and 2 respectively
5	Experience Rating has been fundamentally rewritten but should yield similar results, noting any specific comments
6	Experience Rating loss conversion to USD was upside down a GBP claim got smaller when translated to USD
7	Priced loss ratio (PFLR) was shown gross of brokerage in old model, latest has it net of commission
8	event end date was not always filled in and assumed to be 10 days later - this has now been added
9	New National Mourning Approach in UAT Excel used same mortality table for trump and charlie
10	New National Mourning Approach in UAT Excel didn’t cap for expiry date
11	NMP load - excel hardcoded 3.8%, hx uses tp param - 2% for 24 & 25, 0% for 26
12	Experience Rating could generate a weight to the method (vs exposure) when no years were selected and hence no loss costs
13	Experience Rating no IELR entered for 2025 so excel defaults to NIL
14	TP Parameters - Excel has slightly different fixed expenses vs tp parameters library
15	Excel uses different Fx rates to/from usd vs Hx - relevant for non-US TPs
16	Aggregate Deductible Formula gives a 2.8% discount when the deductible is nil … the 100% dependence on simulation removes it and then drive a variance
17	With Non App look ups (Attach + Lim)/TIV not interpolating, table is finely graded, so only small impact. Hx interpolates
18  Simulation - curve used on Adverse Weather was incorrect
19  Simulation - aggregate got depleted in R too quickly - as looped through coverages there was double counting of the early coverages
20  Rate Change - model compared actual expiring PREMIUM to expected LOSSES after adjusting for exposure and called it exposure change