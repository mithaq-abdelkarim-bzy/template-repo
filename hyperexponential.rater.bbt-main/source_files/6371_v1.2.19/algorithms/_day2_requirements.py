##############################################################################################################################
################    BELOW ARE KNOWN DEFECTS WITH THE ALGORITHM THAT HAVE BEEN CARRIED FORWARD or Needed Day 2 ################ 
##############################################################################################################################

###  1 No exposure inflation used in model
###  2 No weightings used on large/cat experience calc.
###	 3 No weightings used on attritional in first analysis stage (this arguably is deliberate, but when I have seen before weightings were applied at both first and last stage).
###  4 Prior Year Attritional bridge – at one stage we apply last times development factors to this times data – the development is out of step.
###  5 Prior Year Attritional bridge – we use this times Total Deductions to determine a GN Previous (could be deliberate arguably)
###  6 Triangle pushes incomplete year of development into trailing diagonal not first origin period - PLAN TO BE FIXED DAY 1
###  7 No PY total figure possibly to rating summary.
###  8 Exposure Weight only allows adjustment if reducing.
###	 9 Policy length scalant doesn’t seem appropriate – should be handled by premium in exposure weights.
###	10 Inconsistency - Large and cat don’t use policy length scalant but attritional does
###	11 I have fixed rating summary e98 to have the min(0.9 wrapper that exists on shock loss – cant see why we wouldn’t have here also
###	12 Inconsistency in application of profit commission in technical premium calculation – treated as multiplicative not additive in places
###	13 Technical calcs – also consider calculating plan premium…
###	14 Arguably the PC should be calculated explicitly before and after UW adj
### 15 Block Claims were shown in the Claims Summary for large claims - FIXED DAY 1
### 16 multitude of different fx approaches in play across (i) bi premiums & claims vs (ii) claims movementsvs (iii) rms, also we removed the pims update from uat for claims and went back to prod version - build consistency
### 18 PC - Parameters - allow some weight to client data
### 19 PC - Parameters - client std_dev (0 weighte currently) is calculated for att/large/cat it isnt exposure adjusted and on large/cat it isnt developed...
### 20 PC - Automation - given implementing scenario calculation - it maybe useful to allow to promote a scenario to main calculation
### 21 PC - ???- dont understand old model calc pc tab ax31 is trying achieve - can replicate just dont make sense to me
### 22 PC - APPROACH - THRESHOLD - check always net lr 
### 23 PC - APPROACH - DEFICIT - seen approach used, however could consider a long term approach - allowing for a deficit means that a client makes a loss one year 
###                    and they get rewarded for it the following year by a lower est pc and hence higher Tech Adeq - assumes no changes in loss picks e.g. cat - 
### 24 PC - APPROACH - DEFICIT - i maybe mis remembering this but are deficits client dependent - i.e. it would be unusual to express at 100 percent - do they have this info
### 25 PC - APPROACH - SLIDING SCALE - excel description says net loss ratio but calculation based on gross
### 25 PC - APPROACH - SLIDING SCALE - differences between prod version and uat version for scenario - have tracked prod version 
### 26 PC - APPROACH - SLIDING SCALE - assumes no pc is payable in 'mid' section
### 27 PC - APPROACH - SLIDING SCALE - assumes UW profit = PC
### 28 PC - APPROACH - SLIDING SCALE -based on total_deductions - which includes brokerage (paid to aon/willis etc) - i dont know but suspect that would not be contemplated in a PC (brokerage is a negotiation between us and the wholesaler not the agent - they may not even know what it is)
### 29 PC - Parameters - fitting is done on afb amounts not 100% - this is minor as it gets forced to reconcile to 100 percent at the end
### 30 BI - clm - mvmt query - does fx conversion immediately - inconsistent from claims amounts 
### 31 PC - test if pc parameters are consistent - this could be enhanced to allow for other influences e.g. premium, deductions, expected loss, scenario settings
### 32 RMS - consider logic herein - we get AAL & Associated Premium and then apply it to all Premium - i.e. assume that all premium has that cat loss ratio 
### 33 RS - rows 395-408 we removed the mechanism to use triangles trailing diagonal for the sugegsted values in analysing loss data - due to a concern around the fx treatment - note we still it for bucketing att/large/cat
### 34 (post-live 12-12-24) request from UW to be able to search on UW names - MF said can load history into tags/pas_references - future would need to be scripted to async - suggest write few lines to do it and summon from each of key async tasks
