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
@app.get("/locations/{location_id}")
async def get_location(location_id: int):
    try:
        return data.loc[location_id].to_dict()
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