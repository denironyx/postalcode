from fastapi import FastAPI, HTTPException
from typing import List
import pandas as pd

# Load the data into a pandas DataFrame
data = pd.read_csv("api/data/final_df.csv")

# Initialize FastAPI app
app = FastAPI()

def clean_data(data: pd.DataFrame) -> List[dict]:
    # Replace NaN values with None for better JSON serialization
    cleaned_data = data.where(pd.notna(data), None)
    # Convert DataFrame to list of dictionaries
    records = cleaned_data.to_dict(orient="records")
    # Convert float values to string to avoid JSON serialization issues
    records_str = [{k: str(v) if isinstance(v, float) else v for k, v in record.items()} for record in records]
    return records_str

# Hello, World! endpoint
@app.get("/")
async def hello_world():
    return {"message": "Nigeria Postal Code - power by zipcode.ng cc Dennis Irorere"}

# Endpoint to get all locations
@app.get("/locations/", response_model=List[dict])
async def get_locations():
    """
    Retrieve all locations.
    """
    return clean_data(data)

# Endpoint to get locations by district
@app.get("/locations/{district}", response_model=List[dict])
async def get_district_location(district: str):
    """
    Retrieve locations by district.
    """
    try:
        # Filter the data by District and Area
        district_data = data[(data['District'] == district)]
        area_data = data[(data['Area'] == district)]
        
        if not district_data.empty:
            return clean_data(district_data)
        elif not area_data.empty:
            return clean_data(area_data)
        else:
            raise HTTPException(status_code=404, detail="Location not found")
    except KeyError:
        raise HTTPException(status_code=404, detail="Location not found")
    
# Endpoint to get locations by district
@app.get("/locations/{postalcode}", response_model=List[dict])
async def get_postalcode_location(postalcode: str):
    """
    Retrieve locations by postal code.
    """
    try:
        # Filter the data by District and Area
        district_data = data[(data['Postal Code'] == postalcode)]
        
        if not district_data.empty:
            return clean_data(district_data)
        else:
            raise HTTPException(status_code=404, detail="Location not found")
    except KeyError:
        raise HTTPException(status_code=404, detail="Location not found")

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