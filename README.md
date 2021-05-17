# vpic-api

A Python client library for decoding VINs and querying the United States 
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
information to NHTSA under U.S. 49 CFR Parts 551 – 574.

The API available 24/7, is free to use, and does not require registration. NHTSA uses automatic traffic rate controls to maintain the performance of the API and their websites that use the API.

See https://vpic.nhtsa.dot.gov/api/home/index/faq for more on the API.

## Using vpic.TypedClient

Use vpic.TypedClient to receive responses as Python objects.

### Decode a Vehicle Identification Number (VIN)

Decode a 17-digit Vehicle Identification Number (VIN):

```python
from vpic import TypedClient

c = TypedClient()

result = c.decode_vin("1FTMW1T88MFA00001")

Vehicle(
    abs="",
    ...
    body_cab_type="Crew/ Super Crew/ Crew Max",
    body_class="Pickup",
    brake_system_desc="",
    brake_system_type="Hydraulic",
    ...
    displacement_cc="3500.0",
    displacement_ci="213.58310433156",
    displacement_l="3.5",
    ...
    drive_type="4WD/4-Wheel Drive/4x4",
    ...
    engine_configuration="V-Shaped",
    engine_cycles="",
    engine_cylinders="6",
    engine_hp="375",
    engine_hp_to="",
    engine_kw="279.6375",
    engine_manufacturer="Ford",
    engine_model="GTDI",
    entertainment_system="",
    error_code="0",
    error_text="0 - VIN decoded clean. Check Digit (9th position) is correct",
    ...
    make_name="FORD",
    make_id="460",
    manufacturer_name="FORD MOTOR COMPANY, USA",
    manufacturer_id="976",
    model_name="F-150",
    model_id="1801",
    model_year="2021",
    motorcycle_chassis_type="Not Applicable",
    motorcycle_suspension_type="Not Applicable",
    ...
    plant_city="DEARBORN",
    plant_company_name="",
    plant_country="UNITED STATES (USA)",
    plant_state="MICHIGAN",
    ...
    series="F-Series",
    series2="",
    ...
    trim="SuperCrew-SSV",
    ...
    vin="1FTMW1T88MFA00001",
    ...
    vehicle_type="TRUCK ",
    ...
)
```

### Get the Models for a Make and Model Year

```python
get_models_for_make("TESLA", model_year=2020)

[
    Model(
        model_id=1685,
        model_name="Model S",
        make_id=441,
        make_name="TESLA",
        vehicle_type_id=None
    ),
    Model(
        model_id=10199,
        model_name="Model X",
        make_id=441,
        make_name="TESLA",
        vehicle_type_id=None
    ),
    Model(
        model_id=17834,
        model_name="Model 3",
        make_id=441,
        make_name="TESLA",
        vehicle_type_id=None
    ),
    Model(
        model_id=27027,
        model_name="Model Y",
        make_id=441,
        make_name="TESLA",
        vehicle_type_id=None
        )
]
```

## Using vpic.Client

Use vpic.Client if you need the JSON responses returned by the vPIC API.

This client automatically standardizes variable names where vPIC uses inconsistent naming. Turn this off if you need to see the unaltered JSON responses:

```python
from vpic import Client

c = Client(standardize_names=False)
```

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
    "MakeName": "FORD",
    "MakeId": "460",
    "ManufacturerName": "FORD MOTOR COMPANY, USA",
    "ManufacturerId": "976",
    "ModelName": "Mustang",
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
        "MakeName": "TESLA",
        "ModelId": 1685,
        "ModelName": "Model S"
    },
    {
        "MakeId": 441,
        "MakeName": "TESLA",
        "ModelId": 10199,
        "ModelName": "Model X"
    },
    {
        "MakeId": 441,
        "MakeName": "TESLA",
        "ModelId": 17834,
        "ModelName": "Model 3"
    },
    {
        "MakeId": 441,
        "MakeName": "TESLA",
        "ModelId": 27027,
        "ModelName": "Model Y"
    }
]
```
