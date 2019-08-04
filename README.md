## Django - Google Maps Geocoding Demonstration

How this works:

 - You upload an excel file (`.csv`) which contains an `address` column
 - It is assumed that the excel file contains multiple rows of addresses
 - Address in each row is extracted and a Geocoding lookup is made through Google Maps Geocoding API
 - The `latitude` and `longtitude` is pulled from the API response
 - The `lat` and `long` from above is written against the same row in the address
 - The new excel file along with `address`, `lat` and `long` is availabe for download

*Note: **NO** address will be saved in the database*