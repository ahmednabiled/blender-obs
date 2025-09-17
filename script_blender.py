# blender_cursor_import.py
import bpy
import csv

# Path to the CSV recorded by OBS
csv_path = r"C:\Users\hhtg2\Desktop\ads_maker"

# Create empty
empty = bpy.data.objects.new("Cursor_Empty", None)
bpy.context.scene.collection.objects.link(empty)

# Ensure animation data exists
empty.animation_data_create()
empty.animation_data.action = bpy.data.actions.new(name="Cursor_Animation")

# Insert keyframes from CSV
with open(csv_path, newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        frame = int(row["frame"])
        x = float(row["x"])
        y = float(row["y"])
        
        empty.location = (x, y, 0)
        empty.keyframe_insert(data_path="location", frame=frame)
