import arcpy
import os
import csv


# Input path HydroLakes
hydrolakes_shapefile = r"path\to\HydroLAKES.shp"

# Where SWOT folders are stored
base_folder = r"path\to\swot folders"

# Subfolder names (SWOT folders containing shapefiles for different passes)
swot_folders = [
    "SWOT 468",
    "SWOT 431",
    "SWOT 496",
    "SWOT 403",
    "SWOT 218"
]

# Create list of shapefiles
swot_shapefiles = []

# Loop through each SWOT folder to collect all shapefiles
for swot_folder in swot_folders:
    swot_folder_path = os.path.join(base_folder, swot_folder)
    for root, dirs, files in os.walk(swot_folder_path):
        for file in files:
            if file.endswith(".shp"):  # Check if the file is a shapefile
                swot_shapefiles.append(os.path.join(root, file))

# Output path
output_dir = r"path\to\output"
results = {}

# Loop through each SWOT shapefile (each represents a different date)
for i, swot_shapefile in enumerate(swot_shapefiles):

    # Use shapefile name for the column header
    folder_name = os.path.basename(os.path.dirname(swot_shapefile))
    date = folder_name

    print(f"\n--- Processing {swot_shapefile} for {date} ---")

    # 1: Get lakes that intersect with HydroLakes
    intersected_lakes = os.path.join(output_dir, f"intersected_{date}.shp")
    arcpy.analysis.Intersect([swot_shapefile, hydrolakes_shapefile], intersected_lakes)

    # 2: Use Dissolve to aggregate the results
    dissolved_lakes = os.path.join(output_dir, f"dissolved_{date}.shp")
    arcpy.management.Dissolve(intersected_lakes, dissolved_lakes, ["Hylak_id"], statistics_fields=[["wse", "MEAN"]])

    # 3: Get data (Mean WSE, Hylak_id) from dissolved shapefile
    with arcpy.da.SearchCursor(dissolved_lakes, ['Hylak_id', 'MEAN_wse']) as cursor:
        for row in cursor:
            hylak_id = row[0]
            mean_wse = row[1]

            # Track the data for each Hylak_id
            if hylak_id not in results:
                results[hylak_id] = {
                    'Hylak_id': hylak_id
                }

            # Add the mean WSE for the current date
            results[hylak_id][date] = mean_wse

            print(f"Added data for Hylak_id {hylak_id} - mean WSE: {mean_wse} (Date: {date})")

# Results to a CSV file
output_csv = os.path.join(output_dir, "wse_results_variability.csv")
with open(output_csv, 'w', newline='') as csvfile:

    # Write the fieldnames (columns)
    fieldnames = ['Hylak_id'] + [os.path.basename(os.path.dirname(shapefile)) for shapefile in swot_shapefiles]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for hylak_id, data in results.items():
        writer.writerow(data)

print(f"Results have been saved to {output_csv}")
