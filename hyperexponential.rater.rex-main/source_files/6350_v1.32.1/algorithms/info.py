


cyber_msg = f"""## Cyber Coverage

Please *Run Rater* to calculate the model premium. 
Coverages are defined as follows:
- Affirmative: Cyber losses (typically resulting from computer system-related events) and/or Data Restoration costs (costs to restore or recreate data/programs from backups or previous generations).
- Ensuing Loss (Malicious): Physical damage that results from an unathorized, malicious or criminal cyber act or series of unathorized, malicious or criminal acts.

**Note**
Ensuing Loss (Malicious) coverage will not impact technical rate adequacy metrics.
Sublimit is ground-up, above deductibles. If no sublimit is entered, the model will default to the policy limit.

"""


machinery_breakdown_msg = f"""## Machinery Breakdown Coverage

This Machinery Breakdown section allows the user to input the estimated proportion of Contents and BI TIV that is subject to Machinery Breakdown cover. 

Machinery Breakdown coverage is designed for heavy industrial risks, including sectors such as mining, oil and gas, utilities and other large-scale manufacturing. It is different to Equipment Breakdown, which, by contrast, is generally associated with “softer” occupancies. The machinery covered under Machinery Breakdown policies tends to be industrial-grade equipment and these higher hazard occupancies would typically be excluded under a standard Equipment Breakdown policy. 

Once the SOV table has been populated, use the **Load Industries** button to populate the Machinery Breakdown table. 

If the Machinery Breakdown coverage has an associated sublimit, please enter the ground up value below the table. 

Below are the default Machinery Breakdown proportions by industry: 

- Food: 2%
- Heavy Industry: 24%
- Light Industry: 2%
- Mining: 10%
- Utilites: 36%
"""


equipment_breakdown_msg = """## Equipment Breakdown Coverage

Equipment Breakdown is an ancillary coverage underwritten by **Travellers**.

Each occupancy is allocated an occupancy code A, B, C or D which determines the maximum insurable value for that location:

- **Group A** covers a broad range of standard commercial, residential, and public occupancies. Maximum SLTIV $100m.
- **Group B** is for moderate hazard commercial manufacturing and contracting risks. Maximum SLTIV $50m.
- **Group C** includes higher hazard industrial, food, entertainment, and healthcare occupancies. Maximum SLTIV $30m.
- **Group D** is reserved for high hazard industrial risks or specialist manufacturing and **requires referral**. 
Refer to the Occupancy Guide in the Schedule page for the code assigned to each particular occupancy. 

### What is the difference between Equipment Breakdown and Machinery Breakdown?

**Equipment Breakdown** coverage is typically associated with “softer” occupancies, such as educational institutions, office buildings, government facilities, hotels, and similar environments. In these settings, the insured equipment generally includes mechanical and electrical systems such as HVAC units, lifts, small transformers, water pumps, electrical panels, and IT infrastructure.

**Machinery Breakdown**, by contrast, is designed for heavy industrial risks, including sectors such as mining, oil and gas, utilities, and large-scale manufacturing. The machinery covered under these policies tends to be industrial-grade equipment, such as turbines, compressors, mills, and boilers. Travelers exclude these higher hazard occupancies from the standard Equipment Breakdown policy.


"""


remodelling_info_msg = """## Remodelling Check

**Purpose**

If users manually update the **NAICS Industry / Occupancy** selections in the Rex schedule, this check determines whether the newly selected **NAICS occupancy** results in a different **ATC occupancy**.
- **If the ATC occupancy changes:** The file may need to be sent back to Exposure Management for remodelling.
- **If the ATC occupancy remains the same:** There is no need to send it back, as Exposure Management uses ATC groupings for their modelling.
The generated file is an email listing all occupancy changes that imply a new ATC occupancy.

**Steps**

1.	Download and open the email file.
2.	Review the contents to confirm accuracy.
3.	To send, **forward** the email for inclusion in the Exposure Management workflow.


"""

deductible_info_msg = """**Please note REX's deductible logic described below:**
- *Minimum Per Occurrence Deductibles* apply to both International and US regions.
- The US and International *Location Deductibles* can be used to override the *Minimum Per Occurrence Deductible* in the specified region"""