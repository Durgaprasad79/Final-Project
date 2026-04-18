from ward_mapper import get_ward_mapper

# 1. Initialize the mapper (this loads the GeoJSON)
mapper = get_ward_mapper()

# 2. Test a point inside Vijayawada. 
# Based on your file, 16.491 N, 80.668 E is near Ward 74.
lat, lon = 16.491, 80.668
result = mapper.find_ward(lat, lon) 

# 3. Print the outcome
if result:
    print(f"Success! Coordinates ({lat}, {lon}) belong to: {result['ward_name']}")
else:
    print("No ward found. Check if the coordinates are within the GeoJSON boundaries.")