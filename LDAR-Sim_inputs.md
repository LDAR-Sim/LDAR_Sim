# LDAR-Sim Documentation for Input Parameters and Data

Github Repository: IM3S
Version: 1.X
Branch: Master
Document Custodian: Thomas Fox
Email: thomas@highwoodemissions.com

# Read This First
Please note the following before reading, using, or modifying this document:
 
 - The purpose of this document is to catalogue the input parameters, files, data, and arguments required to run the LDAR-Sim model.
 - The document you are now reading will *always* be associated with a specific version or branch of LDAR-Sim. Multiple versions of this document therefore exist, as multiple versions and subversions of LDAR-Sim exist.
 - **If you are submitting a pull request to the public LDAR-Sim repo**, please update this documentation alongside modification to code. Your pull request will not be approved without updating this document with relevant changes to inputs and their implications.
 - Within each category, please maintain alphabetic ordering on contents.
 - For more information on LDAR-Sim, including code, instructions, and additional resources, please visit the Github page by [clicking this link](https://github.com/tarcadius/LDAR_Sim).
 - If you find any errors or inaccuracies in this documentation, please contact the document custodian (email included above).

# Introduction

To reduce fugitive methane emissions from the oil and gas (O&amp;G) industry, companies implement leak detection and repair (LDAR) programs across their asset base. Traditionally, regulators have specified the use of close-range methods such as the U.S. Environmental Protection Agency&#39;s (EPA) Method 21 or Optical Gas Imaging (OGI) cameras for component-level surveys in LDAR programs. These methods remain widely approved by regulators and are effective, however, they are also time consuming and labor intensive. New methane detection and measurement technologies that incorporate satellites, aircraft, drones, fixed sensors, and vehicle-based systems have emerged that promise to deliver faster and more cost-effective LDAR. Prior to applying these technologies and their work practices in LDAR programs, producers must demonstrate equivalence to the regulator – that the proposed alternative will achieve at least the same emissions reductions as incumbent regulatory methods. To support this process, the Leak Detection and Repair Simulator (LDAR-Sim) was developed at the University of Calgary to evaluate the emissions reduction potential of alternative LDAR programs.

LDAR-Sim is a computer model that simulates an asset base of oil and gas facilities, the emissions they produce, and the work crews that use different technologies and methods to find and repair leaks. LDAR-Sim replicates the complex reality of LDAR in a virtual world and allows users to test how changes to facilities or the applications of different technologies and methods might affect emissions reductions and LDAR program costs.

To support wider use of LDAR-Sim, the University of Calgary and Highwood Emissions Management have partnered to expand the model&#39;s capabilities and stakeholder accessibility through the IM3S Project. This document details the model&#39;s input data definitions, requirements, and formats. For each input parameter, the data type, defaults, and a detailed description are provided, as well as additional information about data acquisition and limitations. The parameter list comprises general inputs such as weather, leak counts and rates, and facility coordinates, as well as those specific to individual close-range and screening methods like cost-per-day and follow-up thresholds. All inputs, whether empirical distributions or Boolean logic, are customizable. Recommended defaults are described.

By detailing the model inputs, this report creates the technical foundation for adding new functionality and enabling wider use of the model. This document will be revised continuously as modules, inputs, and functionality are added to or removed from LDAR-Sim.

# General Inputs

## consider\_operator

**Data type:** Boolean

**Default input:** False

**Description:** A binary True/False to activate the operator module (also called the &#39;natural repair rate&#39;). The operator is intended to represent natural leak detection and repair processes that occur at a facility that are independent of a formal LDAR program. If set to False, only the LDAR programs can find and repair leaks. If True, an operator visits each facility at a regular interval (typically, every Monday) and periodically finds leaks and tags them for repair (they then enter repair queue in the same manner as for any leak detected by LDAR). The operator probability of detection is a function of several variables, is calculated automatically, and is explained in Fox et al. (2020).

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** Ultimately, leak production rate (LPR) and natural repair rate (NRR) processes remain poorly understood but can greatly impact modeling results. No clear set of rules or guidance exists for how to navigate LPR and NRR. We recommend that the operator module be used with care and that a range of results be simulated under different assumptions to understand the impact of any assumptions surrounding LPR and NRR. For a nuanced discussion of this topic, see Fox et al. (2020).

### max\_det\_op

**Data type:** Numeric

**Default input:** 0

**Description:** A numerical scalar ranging from 0 to 1 that increases the relative probability that operators will detect large leaks. Although it makes intuitive sense that an operator would be more likely to hear/smell/see a large leak and would be more likely to care about it for safety and economic reasons, there exists no empirical data to guide the operator detection curve.

**Notes on acquisition:** As of January 2021 (time of writing), no data exists to help parameterize how likely operators are to find large vs. small leaks. Ultimately controlled release testing should be performed to understand typical probability of detection ranges for the human senses (AVO).

**Notes of caution:** This is currently a made-up technique that is not grounded in empirical data. Another problem is that it simply adds to the probability of high leaks being detected, but does not lower the probability for small leaks.

### operator\_strength

**Data type:** Numeric

**Default input:** 1

**Description:** A numerical scalar that adjusts the probability of detection of the operator. At zero, the probability of detection becomes zero, while at 1, it is maximized. Values above 1 are probably unnecessary and are not advisable in most circumstances. The purpose of this parameter is to linearly and easily adjust the impact of the operator to test a range of operator strengths (e.g., test from 0 to 1 at increments of 0.1).

## consider\_venting

**Data type:** Boolean

**Default input:** N/A

**Description:** A binary True/False to activate the presence of vented emissions. We do not recommend a default, as the importance of vented emissions varies by LDAR program. With only close-range methods (e.g., OGI), the presence of vented emissions should not matter, as technicians operating close-range instruments should be able to perform the classification. For screening technologies, which cannot distinguish vented from fugitive emissions, including vented emissions will result in a more realistic depiction of program performance, especially if only fugitive emissions are being targeted.

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** Screening technology performance will typically suffer if only fugitive emissions are being targeted due to the confounding presence of design (e.g., vented) emissions. Results from simulations of screening technologies that do not consider venting are therefore optimistic and unlikely to be representative of true reductions. When vented emissions are considered, it will change what facilities are selected for follow-up by screening technologies.

## count\_file

**Data type:** Character string that specifies the name of the csv count file.

**Default input:**&quot;leak\_counts.csv&quot;

**Description:** The count\_file specifies the number of leaks expected to be found at a facility. It is a distribution of leak counts that is sampled once for each facility during initialization. At the bare minimum, the csv contains a single column with the heading name _counts_. Each cell contains an integer representing the number of leaks found during a single LDAR survey. For many applications, this single column may be sufficient. Additional columns can be included if &#39;intelligent&#39; sampling of leak counts is to be used. These fields must have matching fields in the infrastructure\_file. Examples include facility type, production type, company, and so on. Beyond column A (_counts_), any column headings can be used, and all data contents are treated as character strings (category labels).

**Notes on acquisition:** It is important that count data are collected using the same instrument that is used to collect leak rate data (i.e., both collected using M21 or both collected using OGI). Ideally, count and leak data would be collected at the same time and for the same sites (see leak\_file below).

**Notes of caution:** The count distribution should include a zero for each leak-free facility that was visited during the collection of empirical data. For &#39;supplemental&#39; columns (columns B and onward), the number of leaks required for the distribution should increase exponentially for each new column, because count sampling will become increasingly specific. Categories must also be sufficiently exhaustive to be representative. For example, in the table below, each time a natural gas facility with type 361 is sampled, only a single option exists, so the leak count sampled for the new facility will be 1. If the facility type is 311, then the number of leaks sampled could be 6 or 8. If a facility is input to the infrastructure\_file that is subtype 341 and gas, or subtype 401, an error will be returned, as a matching input distribution cannot be generated.

## infrastructure\_file

**Data type:** Character string that specifies the name of the csv file that contains all of the required data on the facilities that comprise the LDAR program.

**Default input:**&quot;facility\_list\_template.csv&quot;

**Description:** At a bare minimum, the csv must contain the following columns: &#39;facility\_ID&#39;, &#39;lat&#39;, &#39;lon&#39; (see Table 2 for an example). For each mobile measurement company used as part of the LDAR program, the number of annual surveys (survey frequency) must be indicated and the inspection time for each method indicated (in minutes). The number of fixed sensors used at each site must also be indicated. Subsections 1.7.X describe individual columns in greater detail.

**Notes on acquisition:** See subsections.

**Notes of caution:** Although facility-specific inputs provide flexibility, in most cases the appropriate data will not be available, and the same survey time or survey frequency may be used for all facilities. Similarly, in most cases the orange text in Table 2 will not be required, and should only be used if the available input distributions are comprehensive (see count\_file section for futher context). In general, LDAR-Sim does not hard-code methods, facility types, production types, and so on. These are provided by the user as categorical variables and can be anything. However, categorical variables must be consistent among different input files or errors will occur.

### facility\_ID

**Data type:** Character string

**Default input:** N/A

**Description:** A character string indicating the unique facility code.

**Notes on acquisition:** Should be available from the facility operator.

**Notes of caution:** Must be a unique identifier.

###

### lat

**Data type:** Numeric

**Default input:** N/A

**Description:** A numeric scalar indicating facility latitude in decimal degrees.

**Notes on acquisition:** May need to be estimated from legal land description in Canada.

**Notes of caution:** Should range between -90 (South Pole) and 90 (North Pole). Will be negative for facilities south of the equator. Fewer decimal places can be used to anonymize location.

### lon

**Data type:** Numeric

**Default input:** N/A

**Description:** A numeric scalar indicating facility longitude in decimal degrees.

**Notes on acquisition:** May need to be estimated from legal land description in Canada.

**Notes of caution:** Should be between -180 and 180 (both correspond to the 180th meridian). Will be negative for facilities west of the Prime Meridian and positive for facilities east of it. Fewer decimal places can be used to anonymize location.

### \*\*\*\_RS

**Data type:** Integer

**Default input:** N/A

**Description:** For each method, an integer indicating the number of required surveys at each facility per calendar year. The three asterisks indicate the interchangeable method name (e.g., OGI\_RS, truck\_RS).

**Notes on acquisition:** Survey frequencies can be based on regulatory requirements, company policies, or can be fabricated by the modeler to explore different scenarios.

**Notes of caution:** Note that just because a number of surveys is prescribed, it does not mean that this number of surveys will necessarily be performed. For example, if labour limitations exist (i.e., not enough crews are available to inspect the number of facilities in the program) or inf environmental conditions are unsuitable (i.e., a particular facility is in a cloudy location that cannot be accessed by satellite), the performed number of surveys may be less than the prescribed number. This variable is not required for continuous measurement methods.

### \*\*\*\_time

**Data type:** Integer

**Default input:** N/A

**Description:** For each mobile method, the number of minutes required to complete a survey at each facility. Three asterisks indicate the interchangeable method name (e.g., OGI\_time).

**Notes on acquisition:** In most cases, an estimate will be made as data will not exist for the specific combination of facility and unique method. However, as new methods and programs and implemented, data will become available to better refine modeling estimates and develop more intelligent programs.

**Notes of caution:** This variable is an empirical estimate of how much time is required for a given mobile method to complete a survey at a given facility. This includes anything that happens onsite (e.g., calibrations, interfacing with the operator, etc.) but _does not include_ driving time between facilities or any other account of time spent offsite. This variable is simply the amount of time that passes from the start of a facility survey to the end. If a facility takes longer than there is time left in a day, then the agent/crew returns the following day to continue work, and so on and so forth, until the facility is completed. This variable is not required for continuous measurement methods.

### fixed\_sensors

**Data type:** Integer

**Default input:** N/A

**Description:** An integer indicating the number of fixed sensors installed at each facility.

**Notes on acquisition:** Can be based on regulatory requirements, company policies, or can be fabricated by the modeler to explore different scenarios.

**Notes of caution:** None

### additional categories

**Data type:** Character String

**Default input:** N/A

**Description:** Any column heading (in Table 2, examples in orange) that helps to refine the numerical sampling process (i.e., &#39;intelligent&#39; sampling). Common examples include facility type, production type, facility age, etc.

**Notes on acquisition:** Specific to the category chosen and up to the user to define.

**Notes of caution:** Categories used here must correspond with any categories used elsewhere in the model. In particular, when sampling from the count\_file and the leak\_file, LDAR-Sim will match the additional categories specified in all files to refine the sampling process and generate emissions information that is representative of the facility for which sampling is being performed. Note that the number of leak counts and leak rates required for the custom empirical distribution should increase exponentially for each new additional category used, because sampling will become increasingly specific. Categories must also be sufficiently exhaustive to be representative. See the count\_file section for an example of why additional categories must be included deliberately and with prudence.

## leak\_file

**Data type:** Character string that specifies the name of the csv file containing empirical leak data.

**Default input:**&quot;leaks\_rates.csv&quot;

**Description:** The leak\_file specifies the leak rates and relevant characteristics of empirical leaks, forming the basis of the leak-rate distribution that is sampled once for each new leak that is generated. At the bare minimum, the csv contains a single column with the heading name _gpersec_. Each cell contains a numeric value representing the emission rate of a real, previously detected, and quantified leak, in grams per second. For many applications, this single column may be sufficient. Additional columns can be included if &#39;intelligent&#39; sampling of leak counts is to be used. These fields must have matching fields in the infrastructure\_file. Examples include facility type, production type, company, and so on. Beyond column A (_counts_), any column headings can be used, and all data contents are treated as character strings (category labels). See Table 3 for an example.

**Notes on acquisition:** It is important that leak rate data are collected using the same instrument that is used to collect leak count data (i.e., both collected using M21 or both collected using OGI). Ideally, count and leak data would be collected at the same time and for the same sites.

**Notes of caution:** For non-mandatory columns (columns B and onward), the number of leaks required for the distribution should increase exponentially for each new column, because leak rate sampling will become increasingly specific. Categories must also be sufficiently exhaustive to be representative. See count\_file for an example.

### leak_rate_dist

**Data type:** List

**Default input:** ['lognorm',-2.776, 1.462, "kilogram", "hour"]

**Description:** An list describing the empirical leak function from which leak emission rates are drawn.

**Notes on acquisition:** 

**Notes of caution:** None

## LPR

**Data type:** Numeric

**Default input:** 0.0065

**Description:** Anumeric scalar that denotes the leak production rate (LPR).New leaks are generated using a site-level empirical LPR that is independent of the number of leaks already present on site. LPR is the probability that a new leak will arise, each day, for each site. The LPR is an empirical representation of all conditions that lead to the occurrence of leaks, including facility age, management practices, predictive maintenance, and random chance. Currently, a single LPR is used for all facility types, production types, facility ages, and so on. In the future, as more LDAR data becomes available, LPRs could be calculated that are specific to each of these or other variables, or distributions of LPRs could be generated. For an extended discussion on LPR, see Fox et al. (2020).

**Notes on acquisition:** While the &quot;true&quot; LPR is elusive, it can be estimated by dividing the number of leaks found during an LDAR survey at a facility by the number of days that have passed since the previous LDAR survey at the same facility. If this is done for a large number of survey intervals at a large number of facilities, one should eventually converge on a representative estimate. When LDAR-Sim is used, operator-specific LPR values should be estimated if sufficient data exist to do so.

**Notes of caution:** Available techniques for estimating LPR make a number of problematic assumptions. Ultimately, we have relatively poor data on LPR and the relationship between LPR and NRR. Modeling results are extremely sensitive to LPR. Given that LPR is elusive, we strongly recommend that a broad range of LPR values is evaluated in LDAR-Sim before any decisions are made. For more information, refer to discussions in the main text and supplementary information of Fox et al. (2020).

## make\_maps

**Data type:** Boolean

**Default input:** True

**Description:** Abinary True/False to control whether output maps are generated for each simulation. These maps can be used to understand where/when different technologies are effective and where/when deployment blackout periods occur. During runs with a very large number of simulations, setting make\_maps to False will reduce run time.

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** N/A

## make\_plots

**Data type:** Boolean

**Default input:** True

**Description:** Abinary True/False to control whether output plots are generated for each individual run of a simulation. Automatically generating plots provide a broad range of insights into individual simulation runs that can be extremely useful for interpretation. When dozens, 100s, or 1000s or simulation runs are being performed in succession (i.e., for sensitivity analysis or when comparing multiple different programs), plots from individual runs may not be needed and this variable can be turned to False (in these cases, the target information is in the aggregate results, so individual runs can be ignored). Turning this variable to False will reduce the run time of each simulation by a few seconds, which can be significant if the required number of simulations is high.

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** N/A

## max_leak_rate

**Data type:** Integer

**Default input:** 100

**Description:** The maximum possible leak rate that can be sampled from a distribution.

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** Using None will require almost all of your computer&#39;s total processor utilization across all cores. If background tasks require CPU (e.g., OneDrive, internet browser) your computer may crash.

## n\_processes

**Data type:** Integer or None

**Default input:** None

**Description:** The number of parallel processes to use. None = all available processes, 1 = one virtual core, and so on. We recommend using None to greatly reduce simulation run time.

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** Using None will require almost all of your computer&#39;s total processor utilization across all cores. If background tasks require CPU (e.g., OneDrive, internet browser) your computer may crash.

## n\_simulations

**Data type:** Integer

**Default input:** 3 (much more to constrain uncertainty)

**Description:** The number of simulations to perform for an identical set of inputs.

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** Using more simulations leads to better-constrained results but requires greater run time. For high-consequence scenarios that are meant to inform decision-making, we recommend using 10+ simulations for each scenario modeled.A minimum of two simulations is required to compare a set of different LDAR programs.

## NRD

**Data type:** Integer

**Default input:** 150

**Description:** The kill date of each leak in number of days.

**Notes on acquisition:** Estimate from empirical data or use previously published value. 

**Notes of caution:** This value is highly uncertain and likely depends on context.

## print\_from\_simulations

**Data type:** Boolean

**Default input:** False

**Description:** A binary True/False to indicate whether to print informational messages from within the simulations. These messages can have value when debugging or troubleshooting.

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** N/A

## program\_list

**Data type:** List of character strings

**Default input:** [&#39;P\_ref&#39;, &#39;P\_alt1&#39;, &#39;P\_alt2&#39;]

**Description:** Alist of all the programs to be simulated. Each entry in the list is the name of a single program, and each program is separated by a comma. If only one program is used, the model will still run, but the batch reporting module will not be triggered, and no comparisons will be made. There is no limit to the number of programs that can be specified, but each program must be defined in a unique text file in the input directory. If a reference program is used (e.g., regulatory OGI), it must be placed in position 1 of the list.

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** It is recommended that for each program in the list, the same number of simulations, the same number of timesteps, and the same start\_year be used. It is critically important to double check that other variables are only different between when programs when intended. For example, in almost all cases LPR should be the same for all programs, unless the modelers is specifically evaluating the impact of using different LPR values. We do not recommend using more than 5-6 different programs simultaneously because the batch plots become quite crowded. When making new program files, a method library is available in the inputs template folder to help define the methods to be used. Always ensure that the program name is specified in three places: (i) as the text file name, (ii) as the dictionary name on line 1 of the text file, and (iii) as the program\_name in the text file, directly below the section that specifies which method dictionaries are to be used.

## program\_name

**Data type:** Character string

**Default input:**&#39;P\_ref&#39; (for the reference program)

**Description:** The name of the program. Typical naming convention is &#39;P\_ref&#39; for the reference program, &#39;P\_alt1&#39; for the first alternative program, &#39;P\_cont&#39; for a continuous measurement program, &#39;SA\_MGL&#39; for a sensitivity analysis on a mobile ground lab program, and so on. Any name can be used, so long as it is consistently used elsewhere (see Notes of caution below).

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** Should be the same as specified elsewhere in the program text file (see program\_list).

## repair\_cost

**Data type:** Integer

**Default input:** N/A

**Description:** The average cost of leak repair. This value is added to the total program cost each time a leak is repaired, whether as a result of an LDAR program or due to routine maintenance by the operator.

**Notes on acquisition:** The duty holder should have data on cost of repairs.

**Notes of caution:** Cost of repair is highly variable and not well characterized by a single value. For example, a percentage of leaks will have near-zero repair costs if it is just a matter of tightening a valve. Other repairs, especially if specialized equipment is involved, could be extremely expensive – especially if a shutdown is required and production decline, leading to indirect costs. Those with good data and an intimate understanding of LDAR-Sim may opt to reprogram the model to accept a distribution of repair costs associated with different kinds of repairs – this could greatly improve LDAR cost estimates.

## repair\_delay

**Data type:** Integer

**Default input:** 14

**Description:** Specifies the amount of time that passes between the tagging of a leak and the point at which it is repaired (i.e., it stops emitting and is removed from the tag pool). This value is specific to a program, not a method, because once a leak is tagged, it is the responsibility of the duty holder to resolve it.

**Notes on acquisition:** Little public data exists to inform this value, though repair delays are often dictated by regulatory requirements. In reality, the repair delay is likely a bimodal distribution, which some leaks repaired immediately by inspectors while others may take weeks or months if parts must be ordered or if a facility shutdown is required.

**Notes of caution:** Do not confuse with method-specific reporting delays. Reporting delays define the time between surveys and transfer of information to the next responsible party. For example, an OGI company may have a reporting delay of 2 days and the duty holder might have a repair delay of 14 days. In this case, the amount a leak would continue to emit for 16 days following detection.

## sensitivity

**Data type:** Dictionary

**Default input:** {&#39;perform&#39;: True, &#39;program&#39;: &#39;OGI&#39;, &#39;order&#39;: &#39;1&#39;, &#39;write\_results\_postsim&#39;: False}

**Description:** Adictionary of inputs that triggers and parameterizes a sensitivity analysis (SA). The first entry is a Boolean True/False that indicates whether a SA should be performed. The second entry indicates the method. The order indicates the position of the entry in &#39;program\_list&#39; (it should be &#39;1&#39; for the reference program). Finally, write\_results\_postsim exports the SA results to a csv file.

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** Sensitivity analyses should be run separately from the main simulation. When an SA is run, all input parameters are rewritten, so many of the inputs in the program files are inconsequential. As currently written, the sensitivity analysis is method-specific and is not generalizable across program types. The SA should be rebuilt to be generalizable to any program.

## site\_samples

**Data type:** List

**Default input:** [False, 0]

**Description:** Alist of inputs to sample from infrastructure\_file, if desired. This functionality would generally be used to run a series of rapid simulations when a large number of sites are included in the program. The first element in the list is a Boolean True/False to trigger whether or not to take samples. The second element indicates the number of samples to acquire.

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** This functionality could be used to &#39;increase&#39; the number of sites in a program, as sampling occurs with replacement. For example, if a program only had 5 sites, sampling of 100 sites would create the illusion of more sites in the program. However, the sites will only represent 5 locations, so if simulations include geographical considerations (e.g. road networks), this may not be advisable as travel times might not be meaningful.

## spin\_up

**Data type:** Integer

**Default input:** 0

**Description:** Number of days to ignore at the start of the simulation when generating automated plots. Data outputs are unaffected – only plots are truncated by the number of spin-up days. This can be useful for data visualization when there is a significant step change between baseline emissions and a new, much lower equilibrium emissions level following implementation of an LDAR program

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** Indicating a spin\_up value only affects plotting and does not affect the underlying data outputs. If you want to compare emissions of two programs using output datasets and want to exclude the influence of the initial step change in emissions, a spin up must be added manually.

## start\_year

**Data type:** Integer

**Default input:** 2003

**Description:** The year at which the simulation will begin.

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** The NetCDF file must encompass the start year plus the number of timesteps. For example, if the start date is 2015 and 1460 timesteps are used, the NetCDF file must extend from at least 2015 to 2019.

## subtype\_distributions

**Data type:** List

**Default input:** [False, 'subtype_distributions.csv']

**Description:** 

**Notes on acquisition:** 

**Notes of caution:** If True, will overwrite global leak distribution.

## subtype\_times

**Data type:** List

**Default input:** [False, &#39;subtype\_times.csv&#39;]

**Description:** Imports a lookup table that allows the modeler to set the survey time per facility according to facility type. This functionality can be used when survey times are not known for each individual site, but can be approximately estimated by facility subtype. Each row represents a facility type and each column represents a method. Times are the number of minutes that pass between arrival at a facility and completion of the inspection at that facility (exclusive of time between workdays and travel time if a site is too large to finish in any given day).

**Notes on acquisition:** Ideally, empirical data for similar facilities are used to inform the lookup table and that each value represents a representative average based on a reasonable number of surveys

**Notes of caution:** Facility types must match those used in infrastructure\_file. When used, subtype\_times overwrites any facility-specific times present in infrastructure\_file.

## t\_offsite\_file

**Data type:** Character string

**Default input:**&quot;time\_offsite\_ground.csv&quot;

**Description:** Character string that specifies the csv file containing a distribution of times spent offsite presented in a single column. The column heading must be &quot;mins\_offsite\_per\_site&quot; and each cell contains an integer representing an empirical estimate of the amount of time (in minutes) spent offsite between two facilities or between a home base (i.e., town where hotel is) and a facility.

**Notes on acquisition:** Each value should represent not only driving time, but all time spent not conducting surveys (driving, breaks, meals, break downs, trains, etc.) This data should be scraped from historical GPS data associated with LDAR survey crews, ideally for the facilities under evaluation.

**Notes of caution:** These data may be difficult to acquire and may lack representativeness. An alternative is to use geospatial road data and route planning with LDAR-Sim.

## timesteps

**Data type:** Integer

**Default input:** N/A

**Description:** The number of daily timesteps to use for each simulation run of the program.

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** We recommend running the simulation for several years due to the stochastic nature of LDAR systems and the periods of time over which leaks arise and are repaired. Using 1000 timesteps is a good place to start. Keep in mind that if a spin\_up is used, the number of timesteps must be greater. Also note that the simulation will run until start\_date + timesteps, so keep in mind that the end date cannot extend beyond the available ERA5 weather data, if used.

## use_empirical_rates
**Data type:** Boolean or string

**Default input:** False

**Description:** 

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** 


## UTC\_offset
**Data type:** Integer

**Default input:** N/A

**Description:** The timezone of the study region, which is used to query the correct weather data.

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** N/A

## vent\_file

**Data type:** Character string that specifies the name of the csv file containing empirical facility-scale emissions data used to bootstrap design emissions.

**Default input:**&quot;site\_rates.csv&quot;

**Description:** The vent\_file specifies the facility-scale emission rates that are resampled alongside leak rate data to generate distributions of design (vented + incomplete combustion) emissions at each site. The csv contains a single column with the heading name _gpersec_. Each cell contains a numeric value representing the emission rate of a real, previously detected, and quantified facility-scale emission rate in grams per second.

**Notes on acquisition:** Established methods should be used, when possible, and data should be representative of the region and facilities of study. Recommended approaches for facility-scale estimates include the tracer-release method, OTM33A, and aerial mass balance, among others.

**Notes of caution:** N/A

## verification\_cost

**Data type:** Integer

**Default input:** N/A

**Description:** The average cost of repair verification. This value is added to the total program cost each time a repair is verified. Some regulations require verification of successful repair within a certain number of days following repair. If the operator is already onsite and can easily verify the repair with readily available instruments (e.g., FID), the cost of verification could be negligible. If the operator has to drive long distances or engage an independent service provider to verify repairs, costs could be high.

**Notes on acquisition:** The duty holder should have data on cost of verification.

**Notes of caution:** Cost of verification is likely to be facility specific. Modelers with good data and an intimate understanding of LDAR-Sim may opt to reprogram the model to accept a distribution of site-level verification cost estimates.

## weather\_file

**Data type:** Character string that specifies the name of the environmental analysis NetCDF4 data file.

**Default input:**&quot;ERA5\_AB\_1x1\_hourly\_2015\_2019.nc&quot;

**Description:** Specifies the name of the ERA5 NetCDF4 file that contains all weather data to be used in the analysis. Generally, at a minimum, OGI requires wind, temperature, and precipitation data. LDAR-Sim reads in temperature data in degrees Celsius at 2 meters above ground, wind in meters per second at 10 meters above ground, and total precipitation in millimeters accumulated per hour. Other weather variables are freely available for download.

**Notes on acquisition:** Raw data are available from the European Centre for Medium-Range Weather Forecasts. Pre-processed and ready to use weather data have been prepared and are available for download on AWS for Alberta, Colorado, and New Mexico. LDAR-Sim will access these files directly if the file names are specified correctly in the program file. Currently available files are:

- Alberta: &quot;ERA5\_AB\_1x1\_hourly\_2015\_2019.nc&quot;
- Colorado: &quot;ERA5\_CO\_1x1\_hourly\_2015\_2019.nc&quot;
- New Mexico: &quot;ERA5\_NM\_1x1\_hourly\_2015\_2019.nc&quot;

Each of these files provides hourly weather (wind, temp, precip) data spanning the years specified at a spatial resolution of 1 degree latitude and 1 degree longitude. If custom configurations are needed for different regions, spatial resolutions, temporal resolutions, dates, or weather variables (e.g., clouds, snow cover, etc.), they must be downloaded manually from the ERA5 database. The &#39;ERA5\_downloader&#39; python file in the model code folder provides code and guidance for accessing custom weather data.

**Notes of caution:**

Weather file sizes can become quite large, especially when spatial and temporal resolution increase (maximum resolutions of 1.25 degrees and 1 hour, respectively). Modelers must decide how to navigate these tradeoffs, and understand the implications of the resolutions chosen.

If using different weather files for different programs (e.g., when comparing different regions), weather data must be downloaded manually and saved to the inputs folder before beginning simulations, as the automatic downloader built into LDAR-Sim will only download one file at a time.

## weather_is_hourly

**Data type:** 

**Default input:** False

**Description:** 

**Notes on acquisition:** 

**Notes of caution:** 

## wd

**Data type:** Character string

**Default input:**&quot;../inputs\_template/&quot;

**Description:** A character string that specifies the name of your working directory (the folder that contains all of your inputs). This working directory should be contained within the same parent folder as the &quot;../model\_code/&quot; folder, contains the python files for running the LDAR-Sim program. Typically, the parent folder is named LDAR\_Sim and contains the model\_code and inputs\_template folders.

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** You do not need to specify the entire path to the working directory. As LDAR-Sim will be running from the model\_code folder, it will search within the same parent directory for inputs\_template.

## write\_data

**Data type:** Boolean

**Default input:** True

**Description:** A binary True/False to activate the export of simulation data to csv files. Generally recommended that this remains set to True unless it is desired to reduce time/storage requirements during sensitivity analyses.

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** Must be True to make automated maps and plots.

# Close-range (OGI) Inputs

## consider_daylight

**Data type:** Boolean

**Default input:** False

**Description:** A binary True/False to indicate whether crews should only work during daylight hours. If False, crews work the number of hours specified by the &#39;max\_workday&#39; input variable used for each method. If True, crews work the shorter of either &#39;max\_workday&#39; or the number of daylight hours calculated using the PyEphem package in python using latitude, longitude of each site, for each day of the year. PyEphem accepts two arguments: obs.horizon and obs.pressure.

**Notes on acquisition:** Acquisition is automated using required lat and lon coordinates for each facility (see infrastructure\_file input) at each timestep.

**Notes of caution:** In most cases, True and False will yield similar results. Use of daylight constraints should be considered for companies that do not wish to deploy crews in the dark for safety reasons, especially for locations at high latitudes during winter months (e.g., Northern Alberta). However, this functionality should not be used to determine whether sunlight is available for passive remote sensing methods or other technologies that require sunlight operate, as the sun has already set when civil twilight occurs (see obs.horizon). Solar flux will vary will topography and cloud cover (use ERA5 data).

###

### obs.horizon

**Data type:** Character string

**Default input:**&quot;-6&quot;

**Description:** Defines the length of the day by the number of degrees below the horizon the sun must be to delineate day from night. Options include civil twilight (-6), nautical (-12), and astronomical (-18).

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** See notes of caution for &#39;consider\_daylight&#39;.

### obs.pressure

**Data type:** Integer

**Default input:** 0

**Description:** Sets the pressure (mBar), enabling PyEphem&#39;s mechanism for computing atmospheric refraction near the horizon. Setting pressure to zero ignores refraction, which we recommend.

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** To our knowledge, accounting for refraction has not been tested in LDAR-Sim. We recommend ignoring refraction unless there is a compelling reason to do otherwise.

## consider\_weather

**Data type:** Boolean

**Default input:** True

**Description:**  A binary True/False to indicate whether weather the method is affected by weather. If true surveys/screening occurs regardless of weather for scheduled visits.

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** Locations with more extreme weather will be more effected if this is disabled.

## is\_follow\_up

**Data type:** Boolean

**Default input:** False

**Description:**  A binary True/False to indicate whether the method is used to survey sites previously flagged by screening technologies. If marked turned off this method will not visit sites on regular intervals.

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** No data acquisition required.

## is\_screening

**Data type:** Boolean

**Default input:** False

**Description:**  A binary True/False to indicate whether the method is used to flag sites / equipment groups or to survey and tage leaks. If set true, a Follow-up method is required to tag leaks detected with this method.

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** No data acquisition required.

## cost\_per\_day

**Data type:** Integer

**Default input:** N/A

**Description:** The daily cost charged by the service provider (per crew). It is charged each time a crew is deployed, regardless of how many sites they survey that day.

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** Currency is not important but must be consistent across all inputs.

## max_precip

**Data type:** Numeric

**Default input:** 100

**Description:** The maximum precipitation accumulation allowed (mm) over one hour.

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** N/A

## max_wind

**Data type:** Numeric

**Default input:** 100

**Description:** The maximum average hourly wind speed (m/s at 10m) at which crews will work.

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** N/A

## max_workday

**Data type:** Integer

**Default input:** 10

**Description:** The maximum number of hours a crew can work in day (include travel time).

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** Can be overwritten if consider\_daylight is True and days are short.

## measurement_scale

**Data type:** String

**Default input:** "component"

**Description:** A character string describing the measurements scale. Possible inputs are "component", "equipment", and "site".

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** N/A

## MDL

**Data type:** List

**Default input:** [0.01275, 2.78e-6]

**Description:** Alist of parameters [_x__0_, σ] that define the minimum detection limit of OGI. The two parameters define a sigmoidal Gaussian cumulative probability function as described in Ravikumar et al. (2018), where _x__0_ is the emission rate (in grams per second) at which 50% of leaks are detected (i.e., median detection limit), and σ is one standard deviation of _x__0_. In Ravikumar et al., the median detection limit can be estimated with the equation:

,

where Q = the emission rate in grams of methane per hour and d is the distance of the OGI camera operator from the source. In Zimmerle et al. (2020), the mean detection distance was 2.7 m, which would result in a median detection limit of 4.59 g/h using the Ravikumar equation (0.001275 g/s as an LDAR-Sim input). However, detection limits were found to be an order of magnitude higher in the Zimmerle study. As such, LDAR-Sim assumes a median detection limit of 0.01275 g/s. For reasons listed below, we note that this is likely a conservative estimate. Also, this approach assumes a constant distance of 3 meters from camera to source. We also adopt the 3-meter sigma from Ravikumar et al. of 0.01 g/h, which translates to 2.78e-6 g/s.

**Notes on acquisition:** We recommend extensive controlled release testing under a range of representative release rates and conditions to establish detection limits. Given the amount of work required to collect this information, we recommend using historical estimates.

**Notes of caution:** Detection probabilities for OGI cameras have been shown to vary with operator experience, wind speed, scene background, and other variables. Estimates from Ravikumar et al. (2018) are experimentally derived but are likely low because (i) the OGI inspector knew where to look, (ii) measurements were performed over only 1 week of good conditions, (iii) OGI cameras were tripod mounted, and (iv) videos were analyzed by experts after data collection. Estimates from Zimmerle et al. (2020) are an order of magnitude higher, and likely closer to reality. However, this estimate applies only to experienced inspectors with over 700 site inspections under their belts, so the true median detection across all inspectors may be lower. Furthermore, the Zimmerle study for experienced inspectors could still represent an underestimate as (i) weather conditions were relatively good, (ii) OGI inspectors were participating in a formal study and were likely very focused, and (iii) many of the leaks were odorized. These results would therefore not include laziness, neglect, or missing of leaks from difficult to access areas. See Section 3.8 for more information on detection limits, including the use of single values or probability surfaces.

## min_interval

**Data type:** Integer

**Default input:** N/A

**Description:** The minimum number of days that must pass between surveys at a facility.

**Notes on acquisition:** Often established by the regulator.

**Notes of caution:** As the number of required surveys becomes more evenly spaced through the year, emissions get lower. As surveys become more clustered, emission rise (because leaks go longer without repair). In general, the minimum interval should attempt to evenly space surveys through the year, but should still be representative of what crews are likely to do. The minimum interval can approximate the number of days in a year divided by the survey frequency (so for two surveys, an interval of ~180 day should evenly space the surveys. However, keep in mind that the crews may take several days or weeks to complete surveys, so if not enough time remains in the year, facilities may be missed and end up out of compliance.

## min_temp

**Data type:** Numeric

**Default input:** -100

**Description:** The minimum average hourly temperature (°C) at which crews will work.

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** Note that units are in degrees Celsius, not Fahrenheit.

## n_crews

**Data type:** Integer

**Default input:** 1

**Description:** The number of distinct, independent crews that will be deployed using the same method.

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** Unless explicitly evaluating labour constraints, ensure that sufficient crews are available to perform LDAR according to the requirements set out in the infrastructure\_file. For example, if 2000 facilities require LDAR, and each takes an saverage of 300 minutes, ~10,000 work hours are required, or 3-4 crews working full time.

## name

**Data type:** Character string

**Default input:**&quot;OGI&quot;

**Description:** A character string denoting the name of the method.

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** Must match the company and crew python files that match the method. For example, if the method file is named OGI\_company, the name must be &quot;OGI&quot;.

## reporting\_delay

**Data type:** Integer

**Default input:** 0

**Description:** The number of days that pass between the end of a survey (when leaks are tagged) and when the duty holder is informed. The reporting delay is then followed by repair\_delay.

**Notes on acquisition:** Get this information from the service provider.

**Notes of caution:** Many service providers have automated systems for reporting leaks as soon as they are found and tagged. However, some companies still provide paper or pdf reports days or even weeks later. It is important to understand the expectations between the duty holder and the service provider.

# Screening Inputs

## name

See Section 2.1.

## n\_crews

See Section 2.2.

## [various weather]

As deemed relevant for the method under evaluation. See Sections 2.3, 2.4, and 2.5 for examples.

## min\_interval

See Section 2.6.

## max\_workday

See Section 2.7.

## cost\_per\_day

See Section 2.8.

## reporting\_delay

**Data type:** Integer

**Description:** The number of days that pass between the flagging of sites by screening methods and when a close-range company (e.g., OGI) is informed that follow-up is required. Follow-up crews will not inspect a site and tag leaks until the reporting delay has passed.

**Notes on acquisition:** Get this information from the service provider.

**Notes of caution:** Note that both close-range and screening methods have reporting delays, and that they work slightly differently. Screening methods report flagged sites to follow-up crews, while close-range methods report tagged leaks to the operator for repair. Also see warning in Section 2.9.

## MDL

**Data type:** Numeric

**Default input:** N/A

**Description:** Minimum detection limit of the screening method in grams per second.

**Notes on acquisition:** We recommend extensive controlled release testing under a range of representative release rates, distances, and conditions to establish detection limits. Given the amount of work required to collect this information, we recommend using historical estimates.

**Notes of caution:** A single value for MDL is used for screening technologies while a parameter list is used for OGI that defines a sigmoidal probability of detection curve (see Section 2.10). These are examples and with more experimental data, probability of detection surfaces can be generated that can estimate detection probabilities as a function of numerous relevant variables (e.g., distance, wind speed, etc.)

## follow\_up\_thresh

**Data type:** List

**Default input:** [1.0, &quot;proportion&quot;] or [0, &quot;absolute&quot;]

**Description:** Alist of two parameters that define the follow-up threshold. Measured site-level emissions must be above the follow-up threshold before a site becomes a candidate for flagging. The character string in the second position of the list must read &quot;proportion&quot; or &quot;absolute&quot;. If absolute, the numeric value in the first position indicates the follow-up threshold in grams per second. If &quot;proportion&quot;, the numeric value in the first position is passed to a function that calculates emission rate that corresponds to a desired proportion of total emissions for a given leak size distribution. The function estimates the MDL needed to find the top X percent of sources for a given leak size distribution. For example, given a proportion of 0.01 and a leak-size distribution, this function will return an estimate of the follow-up threshold that will ensure that all leaks in the top 1% of leak sizes are found.

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** Follow-up thresholds are explored in detail in Fox et al., 2021. Choosing follow-up rules is complex and work practices should be developed following extensive analysis of different scenarios. It is important to understand how follow-up thresholds and follow-up ratios interact, especially if both are to be used in the same program. Note that follow-up thresholds are similar to minimum detection limits but that the former is checked against to the measured emission rate (which is a function of quantification error) while the latter is checked against the true emission rate.

## follow\_up\_ratio

**Data type:** Numeric

**Default input:** 1.0

**Description:** Asingle value that defines the proportion of candidate flags to receive follow-up. For example, if the follow-up ratio is 0.5, the top 50% of candidate flags (ranked by measured emission rate) will receive follow-up. Candidate flags have already been checked against the minimum detection limit and the follow-up threshold. See Section 3.9 for more information.

**Notes on acquisition:** No data acquisition required.

**Notes of caution:** The follow-up ratio ranks sites based on their measured emission rate, which may differ from the true emission rate if quantification error is used. The effect of follow\_up\_ratio will depend on the temporal interval over which sites accumulate in the candidate flags pool. Currently, LDAR-Sim is only configured to do this on a daily basis. For example, all candidate flags detected by all crews will be considered at the end of the day, and flags will be assigned according to the follow-up ratio. In the future, new functionality will enable variable time periods over which candidate flags can be accumulated and compared.

## t\_lost\_per\_site

**Data type:** Integer

**Default input:** N/A

**Description:** A single value that estimates the travel time between facilities for aerial methods. Each time a site survey is complete, the day is advanced by this number of minutes before the subsequent site survey begins.

**Notes on acquisition:** Travel time between facilities

**Notes of caution:** This input is only used for methods that travel between sites in the air (e.g., aircraft). Ground-based methods use t\_offsite\_file or road networks.

## QE

**Data type:** Numeric

**Default input:** 0

**Description:** The standard deviation of a normal distribution with a mean of zero from which a quantification error multiplier is drawn each time an emission rate is estimated. For example, for a value of 2.2, ~35% of measured emission rates will fall within a factor of two of the true emission rate. For a value of 7.5, ~82% of measurements will fall within an order of magnitude of the true emission rate. When QE = 0, the measured emission rate equals the true emission rate. As QE increases, so does the average absolute difference between measured and true emission rates. See Fox et al 2021 for more information and Ravikumar et al. (2019) for empirical quantification error estimates.

**Notes on acquisition:** We recommend extensive controlled release testing under a range of representative release rates, distances, and conditions to establish quantification error. Given the amount of work required to collect this information, we recommend using historical estimates.

**Notes of caution:** As facility-scale quantification error remains poorly constrained for LDAR screening methods, and likely depends on work practice, dispersion modeling, and environment, screening programs should be evaluated using a range of possible quantification errors. We recommend understanding exactly how quantification error works before making use of this functionality. Alternatively, we suggest using literature values of 2.2 and 7.5.

## consider\_daylight

See Section 2.11.

# Fixed Sensor Inputs

## name

See Section 2.1.

## [various\_weather]

As deemed relevant for the method under evaluation. See Sections 2.3, 2.4, and 2.5 for examples.

## up\_front\_cost

**Data type:** Integer

**Default input:** N/A

**Description:** The initial up-front cost of each fixed system. This cost is only charged once.

**Notes on acquisition:** Consult service provider.

**Notes of caution:** Does not account of maintenance activities or the cost of replacing devices after at the end of their lifetime.

## cost\_per\_day

**Data type:** Integer

**Default input:** N/A

**Description:** A daily subscription cost, per device installed.

**Notes on acquisition:** Consult service provider.

**Notes of caution:** Subscriptions are sometimes based on months or annual fees. Ensure that these are converted to a daily estimates.

## MDL

See Sections 2.10 and 3.8.

## follow\_up\_thresh

See Section 3.9.

## follow\_up\_ratio

See Section 3.10. For fixed systems, the follow-up ratio is slightly different in that it considers all candidate flags from all fixed systems, each day. Given that measurements are continuous, the follow-up ratio should be much smaller than it would be for a screening method, as facilities are flagged each day, rather than (for example) three times per year.

## time\_to\_detection

**Data type:** Integer

**Default input:** N/A

**Description:** The number of days between leak onset and detection by the fixed system.

**Notes on acquisition:** We recommend extensive controlled release testing under a range of representative release rates, distances, and conditions to establish time to detection.

**Notes of caution:** Does not include reporting\_delay. In reality, this should be a function of distance and emission rate, so this functionality should be added.

## reporting\_delay

See Section 3.7.

## QE

See Section 3.12.

## consider\_daylight

See Section 2.11.

# Mobile methods Inputs

## route\_planning

**Data type:** Boolean

**Default input:** N/A

**Description:** A binary True/False to activate the route planning. Route planning allows LDAR crews to choose the nearest facility and home bases to visit based on the shortest travelling cost. The travelling cost is travel time that is calculated using the Haversine distance metric and maximum speed limit of travelling. The maximum speed limit is sampeld from speed list. It also allows LDAR crew to depart from the home base (town or city, or airport) at the start of each day and return to the home base at the end of each day.This will be improved in the future, especially for OGI, drone, and trucks.  

**Notes on acquisition:** It requires user to also define input for home_bases_files, speed_list and, LDAR_crew_init_location. 

**Notes of caution:** Only mobile methods can use this functionality.


## home\_bases\_files

**Data type:** Character string that specifies the name of the csv file that contains all of the required data on the home bases that used for LDAR scheduling.

**Default input:** N/A

**Description:** At a bare minimum, the csv must contain the following columns: 'name', 'lat', 'lon', where 'name' indicates the name of home bases (e.g., Calgary), and 'lat' and 'lon' are coordinates of each home base. The home bases for aircraft method should be airports, and the home bases for rest mobile methods should be towns and cities. 

**Notes on acquisition:** It is only required if route_planning is activated.   

**Notes of caution:** Only mobile methods can use this functionality.

## speed\_list

**Data type:** list

**Default input:** [60.0,70.0,80.0,90.0] for OGI and truck methods, [200.0,210.0,220.0,230.0] for aircraft method. 

**Description:** A list of speed limits that define the maximum travelling speed of technologies. A random speed is sampled from this list when calculating the travel time between two facilities or between the facility and home base. Can also be a list with a single value.

**Notes on acquisition:** It is only required if route_planning is activated.   

**Notes of caution:** Only mobile methods can use this functionality.

## LDAR\_crew\_init\_location

**Data type:** list

**Default input:** N/A

**Description:** A list of coordinates [longitude, latitude] that define the initial location of the LDAR crew. It is only required if route_planning or geography is activated.      

**Notes on acquisition:** It is only required if route_planning is activated. 

**Notes of caution:** Only mobile methods can use this functionality.

## deployment\_years

**Data type:** list

**Default input:** N/A

**Description:** A list of years used for scheduling. Methods can only be deployed during these years. For example, [2017,2018] indictates methods can only be deployed in 2017 and 2018. If not defined, LDARSim aussmes methods can be depolyed every year. 

**Notes on acquisition:** N/A

**Notes of caution:** Only mobile methods can use this functionality.

## deployment\_months

**Data type:** list

**Default input:** N/A

**Description:** A list of months used for scheduling. Methods can only be deployed during these months. For example, [8,9] indictates methods can only be deployed in August and Septamber.If not defined, LDARSim aussmes methods can be depolyed every month. 

**Notes on acquisition:** N/A


**Notes of caution:** Only mobile methods can use this functionality.


# Data sources, modelling confidence and model sensitivity

There are a broad range of inputs used in LDAR-Sim that must be derived from various sources. Each of these parameters should be carefully considered and understood before using LDAR-Sim to inform decision making. Like other models, the quality of simulation results will depend on the quality and representativeness of the inputs used.

The sensitivity of modeling results to inputs will vary on a case-by-case basis. In general, it is best to assume that all parameters in LDAR-Sim are important before modeling begins. It is strongly recommended to perform sensitivity analyses each time LDAR-Sim is used in order to understand the impact that uncertainty in inputs might have on results. Each LDAR program is unique in many ways. Therefore, there is no universal set of rules or guidelines to indicate _a priori_ which parameters will have the greatest impact on results.

In the same way, the confidence in the accuracy of input data can only be determined by the user who provides the data. For example, if provided an empirical leak-size distribution consisting of only 5 measurements, LDAR-Sim will run and generate results without generating warnings. It is the responsibility of the user to have sufficient experience to understand how LDAR-Sim processes different types of data so that they can confidently provide high quality inputs.

In terms of data source, inputs can come from oil and gas companies, technology providers, or solution providers. Some parameters and inputs can also be sourced from peer reviewed literature or can be used simply as experimental levers to explore different scenarios within LDAR-Sim. The lists below provide a general overview of what stakeholders will _generally_ be responsible for different parameters and inputs. Excepts will always exist, and may vary according to the purpose of modeling, the jurisdiction, and the scope of the modeling exercise. In general, we strongly suggest deriving method performance metrics from single-blind controlled release testing experiments.

Duty Holder / Operator (historical LDAR data)

- count\_file\*
- leak\_file\*
- LPR\*
- vent\_file\*

Duty Holder / Operator (organizational data)

- infrastructure\_file (Id, lat, lng, OGI\_RS, OG\_time)
- repair\_cost\*
- repair\_delay\*
- t\_offsite\_file
- verification\_cost

Technology / Solution Provider / Operator (if self-performing LDAR)

- OGI – n\_crews, min\_temp\*, max\_wind\*, max\_precip\*, min\_interval, max\_workday, cost\_per\_day\*, reporting\_delay, MDL\* , consider\_daylight
- Screening Methods – n\_crews, [various weather and operational envelopes]\*, min\_interval, max\_workday, cost\_per\_day\*, reporting\_delay, MDL\*, consider\_daylight, follow\_up\_thresh, follow\_up\_ratio, t\_lost\_per\_site, QE\*
- Fixed sensor – same as screening methods &amp; up\_front\_cost , time to detection

Modeling Expert

- weather\_file
- max\_det\_op
- perator\_strength
- consider\_venting

\* In absence of this data, published data can be used.

# References

Fox, Thomas A., Mozhou Gao, Thomas E. Barchyn, Yorwearth L. Jamin, and Chris H. Hugenholtz. 2021. &quot;An Agent-Based Model for Estimating Emissions Reduction Equivalence among Leak Detection and Repair Programs.&quot; _Journal of Cleaner Production_, 125237. https://doi.org/10.1016/j.jclepro.2020.125237.

Ravikumar, Arvind P., Sindhu Sreedhara, Jingfan Wang, Jacob Englander, Daniel Roda-Stuart, Clay Bell, Daniel Zimmerle, David Lyon, Isabel Mogstad, and Ben Ratner. 2019. &quot;Single-Blind Inter-Comparison of Methane Detection Technologies–Results from the Stanford/EDF Mobile Monitoring Challenge.&quot; _Elem Sci Anth_ 7 (1).

Ravikumar, Arvind P., Jingfan Wang, Mike McGuire, Clay S. Bell, Daniel Zimmerle, and Adam R. Brandt. 2018. &quot;Good versus Good Enough? Empirical Tests of Methane Leak Detection Sensitivity of a Commercial Infrared Camera.&quot; _Environmental Science &amp; Technology_.

Zimmerle, Daniel, Timothy Vaughn, Clay Bell, Kristine Bennett, Parik Deshmukh, and Eben Thoma. 2020. &quot;Detection Limits of Optical Gas Imaging for Natural Gas Leak Detection in Realistic Controlled Conditions.&quot; _Environmental Science &amp; Technology_ 54 (18): 11506–14.

#####

