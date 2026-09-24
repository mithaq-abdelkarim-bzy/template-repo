# From: James Buckley 
# Sent: Tuesday, April 14, 2026 11:09 AM
# To: Joe Delaney <Joe.Delaney@beazley.com>; Yifei Zhao <Yifei.Zhao@beazley.com>; Asa Euridge <Asa.Euridge@beazley.com>
# Subject: FW: notes for meeting 14-april

# Working Directory
# •	General: \\bfl.local\UK\Groups\Finance\Actuarial\Pricing\12 - Market Facilities\08 HX 
# •	Personal:\\bfl.local\UK\Groups\Finance\Actuarial\Pricing\01 - Property\JB\PU 
# •	Testing: https://beazley-my.sharepoint.com/personal/yifei_zhao_beazley_com/Documents/Microsoft%20Teams%20Chat%20Files/PU%202026%20Case%20List.xlsx?web=1


# Background
# •	24 & 25               - Excel Model - built in 2024 & continued to evolve through 2025 – Dimitri, Rita, Shathu
# •	24Q4                   - Hx Model - build started - Anshul, then James F & Mark B
# •	25Q4                   - JB got brought in with certain challenges presenting around speed / responsiveness, complexity and existing developers leaving
# •	Nov24                 - JB proposed updating schema & vectorising –late October/Early November 25 began working on that (with help from SA/YZ) 
# •	Nov24                 - JB proposed updating methods in November 2025 which led to significant changes in excel and hx – predominantly the Nominal/On-level approach
# •	Feb24                  - initial testing alongside defect resolution and adding things such as validation/ display / cds mapping
# •	Mar24                 - wider testing – pushing through all 1.1s and adding more to display, case pricing approach, renewal, export to excel
# •	Given the targeted approach JB has only had hands-on on parts of the model


# Current Model State:
# •	Excel Model ended on v30.6/v30.7 but most 2026-1-1 cases were priced on v28 to v30.0
# •	Hx Model
# o	Main Live version is v1.0.0 currently
# o	In Prod Environment there are 2 additional branches (1) considering day 2 task for section reference allocation; (2) defect resolution of Premium/Limit JD raised
# •	Speed:
# o	Model algorithm typically runs in around 2 seconds with caching – Not as fast as some hx models, but much faster than excel, noting can’t turn off calculations here
# o	Been seeing variability from 1.6 to 2.6 seconds which we have asked hx to investigate which they relate to the timer itself, although I am doubtful
# •	There is an understanding that some of the very complex cases may not be explicitly be priced in the tool, instead just recorded there with the case pricing approach
# •	Given the many flavours of the model it was acknowledged there would probably be some unseen defects – with the risk mitigated by loading 53 live accounts (60% or more of the book) and testing those repeatedly
# Flavours include:
# o	Approach:        (i) Standard mode with caching; (ii) Standard mode without caching; (iii) large mode; (iv) bbt; (v) Case pricing; 
# o	Data:                   (i) None; (ii) Policy level only; (iii) Claims level
# o	Analysis:           (i) Nominal/Onlevel; (ii) Total/AttLrgCat; (iii) Open/Open+Closed; (iv) Cat Basis
# o	PC:                        (i) standard pc, (ii) sliding pc; (iii) correlation/interdependency; (iv) monoline; (v) bbt
# o	Manual vs data: (i) risk composition; (ii) deductions
# o	Overrides:        on many fields
# •	View: 
# o	Restricted to only being able to see 3 lobs at once on the key analysis pages for speed & design constraints
# o	Recognised the approach became locked when finalized.
# o	Mitigated by using Export to excel to drop all data out and making it required to be run to be finalised

# Testing: 
# •	Actuary-led:         Given predominantly actuary led model it was decided to focus on the actuary testing
# •	Not typical test:    Agreed too complex to test / migrate the data in the common Beazley way
# •	Environment:         Testing was undertaken in the Prod-Test area to allow us to work with live data agreed with MF
# •	PreTest:             9 typical accounts + 2 bbt accounts have been loaded successfully into the rater by JB before putting out for initial testing (6 of the 9 typical presented some defect to resolve)
# •	Initial Testing:     AE/PB/YZ/SB/MW – each pushed 2-5 accounts through and fed back concerns for resolution.
# •	Wider Testing:       53 accounts were loaded relating to 1.1.26 and forward primarily and issues resolved
# •	BBT accounts & case pricing whilst they worked there was little to validate to

# UW Interaction:
# •	User Guides written and uploaded by AM/AE/YZ
# •	UW Demo in March by AE/YZ with session uploaded

# Migration:
# •	Once we reached a stable version of the model the 53 test models were updated to this version and rechecked
# •	MF then migrated the data from Prod-Test to Prod-Live in late March

# Excel Model – sometime variances to Hx – these are defect in some excel versions since v28:
# •	Lloyds Parameters – had some noise in some versions
# •	2026 Technical Parameters and Formulas
# •	Nominal/On-level Basis
# •	Open Claim only dev and BBT
# •	Beazley Projections – rarely used but interpolation issue

# Day 2 items include:
# •	Correlation – not cleanest but had to move on
# •	Code Review of other sections
# •	Section Ref Allocation
# •	Export to Excel – display Lloyds/Beazley Analysis
# •	There is a list maintained in the General directory above

# Parameters:
# •	Suggest Annual:
# o	Inflation x2 – Base, Excess
# o	Beazley data – could do more frequent – PB has also suggested making it a live connection (day 2?)
# o	Business Plan
# o	BBT parameters
# o	Lloyds x 3 – risk codes, risk code description, risk code data
# o	Lookups - Firm Name; broker details; trifocus
# •	Suggest Periodic as things change/rate reviews lead to changes:
# o	Anti-selection x6
# o	Uncertainty x 5
# o	Lookups: Currency codes; Facility Type
# •	As & When: 
# o	Underwriters
# •	Other:
# o	Rate constants has some key assumptions such as decay ratio; bench lr; switch ielr-bf-cl; default #years … lobs etc

# Libraries:
# •	Annual:              tp_parameters, fx_rates
# •	Periodic:            cds; hx api; model profiler; rate change (but not used)
