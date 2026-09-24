# Team:    
- Developer -           James Buckley
- Actuarial -           Yifei Zhao & Ashley Chalk
- Business Analyst -    Andreea Serban
- Migration -           Oana Stroe (Analyst), Vishrut Singh (Developer)
- Testing -             Priya Saidavaram (Manager), Ashwin Pawar
- Architect -           Mark Fleet
- Project Manager       Susan Middleton / Cezar Cervinschi

# When:   
- April 2026 - September 2026

# Plan:   
- Migrate the production Excel Event Cancellation & Non-Appearance rater to HX.
- Incorporate National Mourning enhancements available in the UAT Excel model.
- Modernise the experience-rating framework to align more closely with BBT methodology.
- Extend stochastic simulation to all applicable coverages.
- Remove layer-based Non-Appearance rating structure.
- Implement the standard HX rate-change framework.
- Correct material model defects identified during migration.
- Enable simultaneous Event Cancellation and Non-Appearance coverage quotation.

# Comments
- During development, underwriting requirements changed from mutually exclusive Event Cancellation (EC) and Non-Appearance (NA) coverages to supporting both coverages on a single policy.
  The existing schema was retained given the stage of development,  resulting in a structure that is slightly less intuitive than would be preferred.
- Reconciliation testing identified approximately 15-20 known behavioural differences between the legacy Excel model and HX implementation. 
  Where practical these were remediated in Excel to create a controlled reconciliation version. 
  A number of simulation-related differences could not be replicated in Excel due to limitations of the legacy model.
  Reconciliation therefore focused on expected-loss outputs before and after simulation from which we the got comfort in standard kpis of bpi and tpi. 
  Prior to simulation, the average variance across the 40-account testing sample was approximately USD 2 providing strong evidence that the underlying rating algorithms are consistent.
  Rate change did not compare well due to material defects in excel. We got comfort as we used a standard library, with sensible results on inspection.
- Known Differences are discussed on the separate documentation page

# Testing
- Basic Testing:        6 base test cases were specified by cuo at outset and reside in example data
- Algorithm Testing:    46 accounts were pushed through by our testing team, with KPIs compared to excel and any issues remediated
- UI Testing:           circa 20 stories & 200 story points by Testing team
- User Testing:         5+ Models built by UW 
- Migration Testing:    currently ongoing but will include a line by line on the resulting mapping and checking 15 cases back to the manual entered accounts

# Locations
- Excel Model PROD - \\bfl.local\UK\Groups\PAC_PCG\zBusiness Management\zPCG Pricing Models\Event Cancellation & Non Appearance\PROD\Event Cancellation & Non Appearance Rater.xlsb
- Excel Model UAT  - \\bfl.local\UK\Groups\PAC_PCG\zBusiness Management\zPCG Pricing Models\Event Cancellation & Non Appearance\UAT\Event Cancellation & Non Appearance Rater.xlsb 
- Dev Work         - \\bfl.local\UK\Groups\Finance\Actuarial\Pricing\01 - Property\JB\Contingency
- Testing Results  - https://beazley.sharepoint.com/sites/HXTestingTeam/Shared%20Documents/Rater%20Reconciliation/EC&NA/ECNA%20Algorithm%20Testing%20-Results%20-%2020260713.xlsx?web=1 (live)  
- Testing Results  - \\bfl.local\UK\Groups\Finance\Actuarial\Pricing\01 - Property\JB\Contingency\Testing\ECNA Algorithm Testing -Results - 20260713.xlsx (offline 11 Sept) 
- Testing Files    - \\bfl.local\UK\Groups\Finance\Actuarial\Pricing\01 - Property\JB\Contingency\Testing\
- Migration Mapping- https://beazley.sharepoint.com/sites/GlobalRating-ProductGovGroup/Shared%20Documents/Global%20Rating%20Engine/Requirements/Event%20Cancellation%20&%20Non%20Appearance/Migration/EC&NA%20migration%20file.xlsx?web=1 (live)
- Migration Mapping- \\bfl.local\UK\Groups\Finance\Actuarial\Pricing\01 - Property\JB\Contingency\EC&NA migration file.xlsx                 (offline 11 Sept) 
- Migration Script - \\bfl.local\UK\Groups\Finance\Actuarial\Pricing\01 - Property\JB\Contingency\EC & NA Migration Script - 11 Sept.txt    (offline 11 Sept) 
- PROD SQL Database- Server: [DBS-p9m-BeazleyIntelligenceDataSetsRO-PRD,12440]; Database: [NewContingencyRater]
