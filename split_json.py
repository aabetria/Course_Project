import json
import os

# Configurable size limit per chunk (25 MB)
MAX_SIZE_MB = 25
MAX_SIZE_BYTES = MAX_SIZE_MB * 1024 * 1024

# Load your GeoJSON file
with open("large_file.geojson", "r", encoding="utf-8") as f:
    data = json.load(f)

features = data["features"]
chunk = []
os.makedirs("output_chunks", exist_ok=True)
file_count = 0

for feature in features:
    chunk.append(feature)
    temp_data = {
        "type": "FeatureCollection",
        "features": chunk
    }
    size = len(json.dumps(temp_data).encode("utf-8"))

    if size > MAX_SIZE_BYTES:
        chunk.pop()
        with open(f"output_chunks/chunk_{file_count}.geojson", "w", encoding="utf-8") as out:
            json.dump({
                "type": "FeatureCollection",
                "features": chunk
            }, out)
        file_count += 1
        chunk = [feature]

# Save remaining features
if chunk:
    with open(f"output_chunks/chunk_{file_count}.geojson", "w", encoding="utf-8") as out:
        json.dump({
            "type": "FeatureCollection",
            "features": chunk
        }, out)
