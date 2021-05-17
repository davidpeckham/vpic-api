# vpic-api

A client library for the U.S. NHTSA vPIC API

vPIC is the United States National Highway Traffic Safety Administration (NHTSA)
[Vehicle Product Information Catalog (vPIC) Vehicle Listing API](https://vpic.nhtsa.dot.gov/api). 
The API available 24/7, is free to use, and doesn't require registration.

Use the vpic-api client library to decode Vehicle Identification Numbers (VINS),
and get information about manufacturers, plants, makes, and models.

## Vehicles

vPIC has information about these types of vehicles sold in the USA:

* Bus
* Incomplete Vehicle
* Low Speed Vehicle (LSV)
* Motorcycle
* Multipurpose Passenger Vehicle (MPV)
* Passenger Car
* Trailer
* Truck

Note that NHTSA uses automatic rate limiting. They request that you save batch
processing for evenings and weekends (Eastern Time).

For more on the NHTSA vPIC, visit [their home page](https://vpic.nhtsa.dot.gov/about.html).

## Features

* Decode a 17-digit Vehicle Identification Numer (VIN)
* Decode a partial VIN when you don't have the complete VIN
* Get information about vehicle manufacturers, plants, makes, and models
* Supports 1981 and later model years

## Alternatives

In May 2021, NHTSA released a standalone database for Microsoft SQL Server 2012.
This database as all of the information you need to decode VINs. You can download
it from the [vPIC API home page](https://vpic.nhtsa.dot.gov/api/).