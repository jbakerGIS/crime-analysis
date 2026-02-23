# 🗺️ State-Level Violent Crime and Political Majority Analysis (2012–2024)
## 📌 Project Overview

This project explores state-level patterns in violent crime and examines whether long-term political majority alignment (Democratic, Republican, or Tie) shows any meaningful spatial or statistical relationship with crime rates in the United States.

Using a combination of Python, ArcGIS Pro, and spatial statistics, the project integrates election results from four presidential cycles (2012–2024) with violent crime data to produce maps, summary statistics, and exploratory visualizations suitable for policy-focused GIS analysis.

## 🎯 Research Questions

How are violent crime rates spatially distributed across U.S. states?

Do long-term political majorities correlate with higher or lower crime rates?

Are there statistically significant spatial clusters of violent crime?

Do regional patterns explain crime variation better than political alignment?

## 🧾 Data Sources
### Crime Data

Violent crime incidents by state (2024)

Normalized to incidents per 100,000 residents

Source: FBI UCR Program via Council of State Governments Justice Center

### Election Data

Presidential election results: 2012, 2016, 2020, 2024

Scraped from the UCSB American Presidency Project

Aggregated to determine long-term state political majority

## 🧠 Methods
### 1️⃣ Election Data Collection (Python Web Scraping)

Script: 
- scripts/voting_results_web_scrape.py
  
Notebook:
- notebooks/web_scrape_test.ipynb

Scraped election result tables using requests and BeautifulSoup

Dynamically parsed rows based on detected data types (vote counts, percentages, EVs)

Handled inconsistent table structures across election years

Output saved to /data/raw/ as yearly CSV files

Key outcome: Clean, structured election datasets for four presidential cycles

### 2️⃣ Political Majority Determination

Script: 
- scripts/election_results_analysis.py

Notebook:
- notebooks/spreadsheet_analysis_test.ipynb

Compared Democratic vs Republican vote totals for each state and year

Assigned a party winner per state per election

Aggregated results across all four elections

Assigned each state a Majority_Party:

- Democratic
- Republican
- Tie

📄 Final output:
/data/final/state_majority_party.csv

### 3️⃣ GIS Data Integration (ArcGIS Pro)

Notebook: notebooks/gis_analysis.ipynb

Steps performed using arcpy:

- Added a Region field (Northeast, Midwest, South, West)

- Joined:

  - Political majority CSV → state polygons

  - Crime data CSV → joined state feature class

- Created finalized analysis feature class:

  - USA_States_Crime_Join

### 4️⃣ Exploratory & Statistical Analysis
Summary Statistics

Mean and median violent crime rates calculated by:

- Political majority

- Region

Charts

Bar charts: mean crime by party & region

Used matplotlib and seaborn for exportable figures

### 5️⃣ Spatial Analysis
Global Spatial Autocorrelation

Moran’s I used to test whether violent crime rates are spatially clustered

Results documented in:

- Spatial Autocorrelation Report.pdf

Hot Spot Analysis (Getis-Ord Gi*)

Identified statistically significant clusters

Limited hot spots emerged, highlighting the dominance of outlier states rather than broad regional clustering

## 🗺️ Key Maps & Figures
Political Majority by State (2012–2024)

Violent Incidents per 100k Residents (2024)

Percent Change in Violent Crime (2019–2024)

Hot Spot Analysis

Mean Violent Crime by Political Majority

Mean Violent Crime by Region

## 📊 Results Summary

Violent crime rates vary widely across states, with a small number of high-value outliers

Political majority categories show substantial overlap in crime distributions

Regional grouping explains more variance than political alignment

Spatial clustering exists, but is limited and highly influenced by outlier states

## ⚠️ Limitations

State-level aggregation masks urban vs rural variation

Crime reporting practices differ by jurisdiction

Political majority based solely on presidential elections

Correlation does not imply causation

## 🔮 Future Work

Incorporate socioeconomic variables (income, education, unemployment)

Perform county-level analysis

Expand temporal analysis beyond 2019–2024

Test regression-based spatial models

## 🛠️ Tools & Technologies

Python: pandas, numpy, BeautifulSoup, matplotlib, seaborn

GIS: ArcGIS Pro, arcpy

Spatial Statistics: Moran’s I, Getis-Ord Gi*

Version Control: Git & GitHub

## 📁 Repository Structure
crime-analysis/
│
├── data/
│   ├── raw/
│   ├── intermediate/
│   └── final/
│
├── notebooks/
│   ├── gis_analysis.ipynb
│   ├── spreadsheet_analysis_test.ipynb
│   └── web_scrape_test.ipynb
│
├── scripts/
│   ├── voting_results_web_scrape.py
│   └── election_results_analysis.py
│
├── figures/
├── maps/
└── README.md

## 🧑‍💻 Author
Justin Baker
GIS Analyst | Spatial Data & Visualization
GitHub: https://github.com/jbakerGIS
