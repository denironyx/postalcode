# Postal Code Nigeria - Federal Capital Territory (FCT) Scraper

## Description

This project aims to scrape postal code data for the Federal Capital Territory (FCT) of Nigeria from the website "zipcode.com.ng". The scraped data includes postal codes, areas, streets, and districts within the FCT. Additionally, it provides an API endpoint built with FastAPI to serve the scraped and parsed data to clients. https://www.zipcode.com.ng/

## Features

- Scrapes postal code data for various districts within the FCT.
- Organizes scraped data into a structured DataFrame.
- Merges scraped data with additional district-specific information.
- Exports the final dataset to a CSV file for further analysis.
- Includes an API endpoint with FastAPI to serve the scraped and parsed data to clients.

## FastAPI Integration

To serve the scraped postal code data over an endpoint using FastAPI:

1. Set up a FastAPI application.
2. Define endpoints to serve the postal code data.
3. Implement logic to handle requests and serve the data.
4. Deploy the FastAPI application to make it accessible to clients.

## Usage

### Scraper Script

1. Run the Python script `fct_postal_codes_scraper.py`.
2. The script will scrape postal code data from the website and organize it into a DataFrame.
3. Additional district-specific information is fetched and merged with the DataFrame.
4. The final dataset is exported to a CSV file named `fct-postal-codes.csv`.

### FastAPI Endpoint

1. Set up a FastAPI application using the scraped postal code data.
2. Define endpoints to serve the postal code data to clients.
3. Implement logic to handle requests and serve the data.
4. Deploy the FastAPI application to a server or cloud platform.


Abuja (Capital)

Gwagwalada

`http://127.0.0.1:8000/locations/Abuja (Capital)/Asokoro`
