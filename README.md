1. Overview
This repository contains the exact implementation used to generate the results reported in the manuscript:
“A Lyne–Hollick Filter-Derived Threshold Framework for Event and Base Flow Separation in Subsurface Drainage Systems”
The framework provides a standardized, reproducible method for separating event flow and base flow in subsurface drainage systems, using discharge-based signals and seasonally adaptive thresholds.
This repository ensures:
•	Full reproducibility of reported results 
•	Transparent parameterization 
•	Long-term archival stability through versioning 
________________________________________
2. Version Information (CRITICAL FOR REPRODUCIBILITY)
Version used in manuscript results:
➡️ v1.0.0
Release type: Stable, archived version
Date of release: April 7th, 2026
This version is the exact codebase used to generate all results, figures, and metrics reported in the manuscript.
No modifications were made between analysis and publication.
________________________________________
3. Repository Contents
Core Files
•	Event Threshold App 
o	Computers seasonal thresholds using: 
	Lyne–Hollick recursive filter 
	BFI–alpha sensitivity and knee detection 
	Frequency-weighted flow statistics 
o	Supports: 
	Daily and hourly analysis 
	Seasonal delineation schemes A and B 
	Flashiness and amplification scaling 
________________________________________
•	Event Analysis Dashboard 
o	Performs full event and baseflow separation 
o	Identifies event periods using: 
	Threshold exceedance 
	Flow change criteria 
	Multi-step event termination logic 
o	Outputs: 
	Event time series 
	Baseflow time series 
	Flow-weighted concentration metrics 
	Visualization plots 
________________________________________
4. Installation
Requirements
Install dependencies:
pip install streamlit pandas numpy matplotlib seaborn scipy boto3
________________________________________
5. Input Data Format
The input CSV file must contain:
Column Name	Description
Date	Timestamp (required)
Flow	Drainage discharge
Concentration	Nutrient concentration (optional but recommended)
Optional columns:
•	Water table depth 
•	Water temperature 
⚠️ Important:
•	Missing concentration values must be replaced but unit place holders ‘1’
•	Do NOT replace missing values with arbitrary constants 
________________________________________
6. Running the Framework
Step 1: Compute Thresholds
streamlit run Event_threshold.py
This step:
•	Computes seasonal thresholds 
•	Applies Lyne–Hollick filtering 
•	Outputs threshold values used for event detection 
________________________________________
Step 2: Run Event Separation
streamlit run Event_separation_code.py
This step:
•	Applies thresholds to identify events 
•	Separates event flow and base flow 
•	Generates outputs and plots 
________________________________________
7. Methodological Reproducibility
The framework ensures reproducibility through:
7.1 Deterministic Workflow
•	No stochastic components 
•	Identical input → identical output 
7.2 Explicit Parameterization
Key parameters:
•	Seasonal thresholds (winter, spring, summer, fall) 
•	Flashiness factor 
•	Baseflow amplification factors 
•	Seasonal delineation scheme 
All parameters are:
•	User-defined 
•	Fully documented 
•	Stored during execution 
________________________________________
7.3 Event Identification Logic
Events are defined using:
1.	Threshold exceedance 
2.	Positive or sustained flow increase 
3.	Termination after two consecutive sub-threshold values 
Additional controls:
•	Compound event detection 
•	Event filtering based on magnitude 
•	Baseflow interpolation constraints 
________________________________________
8. Output Files
The framework generates:
File Name	Description
Daily_flow_event_data.txt	Event flow time series
Daily_flow_base_data.txt	Baseflow time series
Plots (PNG)	Discharge vs event separation
Event summaries	Event durations and timing
________________________________________
9. Reproducing Manuscript Results
To reproduce the results exactly:
1.	Use: 
o	Version v1.0.0 
o	Same dataset as referenced in manuscript 
2.	Apply: 
o	Same seasonal delineation scheme 
o	Same amplification and flashiness parameters 
3.	Run: 
o	Threshold app first 
o	Event separation dashboard second 
________________________________________
10. Notes on Limitations
•	Results depend on: 
o	Quality and continuity of discharge data 
o	Calibration of threshold scaling parameters 
•	Independent validation using: 
o	Precipitation 
o	Water table 
o	Soil moisture 
is recommended for future work.
________________________________________
11. Long-Term Reproducibility
To ensure reproducibility beyond publication:
•	This version is: 
o	Archived 
o	Immutable 
o	Fully executable 
•	Users are encouraged to: 
o	Cite version number in future work 
o	Avoid modifying core logic when reproducing results 
________________________________________
12. Citation
If you use this framework, please cite:
[Insert full paper citation here]
________________________________________
13. Contact
For questions or issues:
Emeka Aniekwensi
aniekwen@msu.edu; felixaniekwensi@gmail.com; efa2621@jagmail.southalabama.edu

