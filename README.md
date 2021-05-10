# vpic-api
Python client library for decoding VINs and querying the United States 
National Highway Traffic Safety Administration (NHTSA) [Vehicle Product 
Information Catalog Vehicle Listing (vPIC) API](https://vpic.nhtsa.dot.gov/api/).

Use this to gather information on vehicles and their specifications,
and to decode VINs to extract information for specific vehicles. vPIC
has information about these types of vehicles sold or imported in
the USA:

* Bus
* Incomplete Vehicle
* Low Speed Vehicle (LSV)
* Motorcycle
* Multipurpose Passenger Vehicle (MPV)
* Passenger Car
* Trailer
* Truck

vPIC has information about how manufacturers assign a VIN that
encodes a vehicle's characteristics. Vehicle manufacturers provide this
information to NHTSA under U.S. law 49 CFR Part 565.

The API available 24/7, is free to use, and does not require registration. NHTSA uses automatic traffic rate controls to maintain the performance of the API and their websites that use the API.

See https://vpic.nhtsa.dot.gov/api/home/index/faq for more on the API.

## Using vPIC

### Decode a Vehicle Identification Number (VIN)

Decode a 17-digit Vehicle Identification Number (VIN):

```python
from vpic import Client

c = Client()

result = c.decode_vin("1FA6P8TD5M5100001", 2021)
```

Here are a few of the 130+ attributes vPIC returns for the VIN:

```json
{
    "Doors": "2",
    "ErrorCode": "0",
    "ErrorText": "0 - VIN decoded clean. Check Digit (9th position) is correct",
    "Make": "FORD",
    "MakeId": "460",
    "Manufacturer": "FORD MOTOR COMPANY, USA",
    "ManufacturerId": "976",
    "Model": "Mustang",
    "ModelId": "1781",
    "ModelYear": "2021",
    "PlantCity": "FLATROCK",
    "PlantCountry": "UNITED STATES (USA)",
    "PlantState": "MICHIGAN",
    "Series": "I4 Coupe",
    "VIN": "1FA6P8TD5M5100001",
    "VehicleType": "PASSENGER CAR",
}
```

### Get the Models for a Make and Model Year

```python
result = c.get_models_for_make("TESLA", 2021)
```

vPIC returns a list of the models for this make and model year:

```json
[
    {
        "MakeId": 441,
        "Make": "TESLA",
        "ModelId": 1685,
        "Model": "Model S"
    },
    {
        "MakeId": 441,
        "Make": "TESLA",
        "ModelId": 10199,
        "Model": "Model X"
    },
    {
        "MakeId": 441,
        "Make": "TESLA",
        "ModelId": 17834,
        "Model": "Model 3"
    },
    {
        "MakeId": 441,
        "Make": "TESLA",
        "ModelId": 27027,
        "Model": "Model Y"
    }
]
```
