# swot-wse-variability

This project analyzes temporal variability in lake water surface elevation (WSE)
using SWOT satellite data across the Mackenzie Delta.

## Overview

WSE values from May–September 2024 were processed to evaluate how lake levels vary over time.

## Methodology

### Data Processing
- Extracted WSE values from SWOT Level 2 lake shapefiles across 37 dates
- Intersected SWOT lakes with HydroLakes polygons
- Aggregated WSE values per lake using the Dissolve tool
- Compiled results into a multi-date dataset

### Statistical Analysis
- Calculated mean and standard deviation of WSE per lake (Excel)
- Computed coefficient of variation (COV = std / mean)
- Applied log transformation to reduce outlier influence

### Spatial Analysis
- Joined COV values back to HydroLakes in ArcGIS
- Visualized spatial variability across the Mackenzie Delta
- Performed Hot Spot Analysis (Getis-Ord Gi*) to identify clusters

## Tools Used

- Python (arcpy)
- ArcGIS Pro
- Excel

## Note

The coefficient of variation allows comparison of variability across lakes
with different WSE ranges, highlighting spatial patterns of hydrological stability and change.

- File paths must be updated before running scripts
- Data not included due to size and licensing
