import arcpy
arcpy.env.overwriteOutput = True
arcpy.env.workspace = r"C:\Users\viver\OneDrive\Desktop\crime_analysis\crime_analysis.gdb"
fc = "USA_States"
arcpy.management.AddField(fc, "Region", "TEXT")
fields = arcpy.ListFields(fc)
for field in fields:
    print(f"{field.name} - {field.type}")