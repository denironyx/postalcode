from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
from pathlib import Path

# print(Path.cwd('/data'))
# print(Path.home())
path_lib = f"{Path.cwd()}\data"
# Load the data into a pandas DataFrame
data = pd.read_csv('final_df.csv')

# Define Pydantic model
class Location(BaseModel):
    District: str
    Area: str
    Street: str
    Postal_Code: float
    Address: str
    Latitude: float
    Longitude: float

# Initialize FastAPI app
app = FastAPI()

# Endpoint to get all locations
# Endpoint to get all locations
@app.get("/locations/")
async def get_locations():
    # Replace NaN values with None for better JSON serialization
    cleaned_data = data.where(pd.notna(data), None)
    # Convert DataFrame to list of dictionaries
    records = cleaned_data.to_dict(orient="records")
    # Convert float values to string to avoid JSON serialization issues
    records_str = [{k: str(v) if isinstance(v, float) else v for k, v in record.items()} for record in records]
    return records_str
# Endpoint to get a single location by index

@app.get("/locations/{district}")
async def get_district_location(district: str):
    try:
        # Filter the data by District and Area
        location_data = data[(data['District'] == district)]
        
        location_data2 = data[(data['Area'] == district)]
        # Check if any location matches the given District and Area
        if not location_data.empty:
            # Replace NaN values with None for better JSON serialization
            cleaned_data = location_data.where(pd.notna(location_data), None)
            # Convert DataFrame to list of dictionaries
            records = cleaned_data.to_dict(orient="records")
            # Convert float values to string to avoid JSON serialization issues
            records_str = [{k: str(v) if isinstance(v, float) else v for k, v in record.items()} for record in records]
            return records_str
        elif not location_data2.empty:
            # Replace NaN values with None for better JSON serialization
            cleaned_data = location_data2.where(pd.notna(location_data2), None)
            # Convert DataFrame to list of dictionaries
            records = cleaned_data.to_dict(orient="records")
            # Convert float values to string to avoid JSON serialization issues
            records_str = [{k: str(v) if isinstance(v, float) else v for k, v in record.items()} for record in records]
            return records_str
            
        else:
            raise HTTPException(status_code=404, detail="Location not found")
    except KeyError:
        raise HTTPException(status_code=404, detail="Location not found")

# @app.get("/locations/{area}")
# async def get_area_location(area: str):
#     try:
#         # Filter the data by District and Area
#         location_data = data[(data['Area'] == area)]
#         # Check if any location matches the given District and Area
#         if not location_data.empty:
#             # Replace NaN values with None for better JSON serialization
#             cleaned_data = location_data.where(pd.notna(location_data), None)
#             # Convert DataFrame to list of dictionaries
#             records = cleaned_data.to_dict(orient="records")
#             # Convert float values to string to avoid JSON serialization issues
#             records_str = [{k: str(v) if isinstance(v, float) else v for k, v in record.items()} for record in records]
#             return records_str
#         else:
#             raise HTTPException(status_code=404, detail="Location not found")
#     except KeyError:
#         raise HTTPException(status_code=404, detail="Location not found")


@app.get("/locations/{district}/{area}")
async def get_district_area_locations(district: str, area: str):
    try:
        # Filter the data by District and Area
        location_data = data[(data['District'] == district) & (data['Area'] == area)]
        # Check if any location matches the given District and Area
        if not location_data.empty:
            # Replace NaN values with None for better JSON serialization
            cleaned_data = location_data.where(pd.notna(location_data), None)
            # Convert DataFrame to list of dictionaries
            records = cleaned_data.to_dict(orient="records")
            # Convert float values to string to avoid JSON serialization issues
            records_str = [{k: str(v) if isinstance(v, float) else v for k, v in record.items()} for record in records]
            return records_str
        else:
            raise HTTPException(status_code=404, detail="Location not found")
    except KeyError:
        raise HTTPException(status_code=404, detail="Location not found")
# Endpoint to update a location
@app.put("/locations/{location_id}")
async def update_location(location_id: int, location: Location):
    try:
        data.loc[location_id] = location.dict()
        return {"message": "Location updated successfully"}
    except KeyError:
        raise HTTPException(status_code=404, detail="Location not found")

# Endpoint to delete a location
@app.delete("/locations/{location_id}")
async def delete_location(location_id: int):
    try:
        data.drop(location_id, inplace=True)
        return {"message": "Location deleted successfully"}
    except KeyError:
        raise HTTPException(status_code=404, detail="Location not found")

# Endpoint to create a new location
@app.post("/locations/")
async def create_location(location: Location):
    data = data.append(location.dict(), ignore_index=True)
    return {"message": "Location created successfully"}