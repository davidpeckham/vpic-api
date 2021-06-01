# vPIC API Client Library

![PyPI](https://img.shields.io/pypi/v/vpic-api)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/vpic-api)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/vpic-api)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/vpic-api)
[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/tterb/atomic-design-ui/blob/master/LICENSEs)
[![Tests](https://github.com/davidpeckham/vpic-api/actions/workflows/main.yml/badge.svg)](https://github.com/davidpeckham/vpic-api/actions/workflows/main.yml)

A Python client library for decoding VINs and querying the United States 
National Highway Traffic Safety Administration (NHTSA) [Vehicle Product 
Information Catalog Vehicle Listing (vPIC) API](https://vpic.nhtsa.dot.gov/api/).

## NHTSA vPIC API

The Vehicle Production Information Catalog (vPIC) API is hosted by the U.S. National Highway Transportation Safety Administration (NHTSA). vPIC data is provided by manufacturers who make vehicles for sale in the United States. The vPIC API is available 24/7, is free to use, and does not require registration. See https://vpic.nhtsa.dot.gov/api/home/index/faq for more on the vPIC API.

## Features

- Decode Vehicle Identification Numbers (VIN)
- Discover manufacturers, makes, and models
- Supports cars, MPVs, trucks, motorcycles, buses, trailers, low speed vehicles and incomplete vehicles manufactured in the U.S.A, or imported for sale in the U.S.A.
- Find manufacturer model year VIN guides
- Use vpic.TypedClient to get results as Python objects
- Use vpic.Client to get results as JSON
- Comprehensive support for the vPIC API

## Author

- [@davepeckham](https://www.github.com/davepeckham)

## Installation

Install vpic-api with Poetry

```bash 
  poetry --dev add vpic-api
```

## vpic.TypedClient Examples

vpic.TypedClient returns results as Python objects.

### Decode a VIN

Get the characteristics of a vehicle by it's 17-digit Vehicle Identification Number (VIN):

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
    make="FORD",
    make_id="460",
    manufacturer="FORD MOTOR COMPANY, USA",
    manufacturer_id="976",
    model="F-150",
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
        model="Model S",
        make_id=441,
        make="TESLA",
        vehicle_type_id=None
    ),
    Model(
        model_id=10199,
        model="Model X",
        make_id=441,
        make="TESLA",
        vehicle_type_id=None
    ),
    Model(
        model_id=17834,
        model="Model 3",
        make_id=441,
        make="TESLA",
        vehicle_type_id=None
    ),
    Model(
        model_id=27027,
        model="Model Y",
        make_id=441,
        make="TESLA",
        vehicle_type_id=None
        )
]
```

## vpic.Client Examples

vpic.Client returns JSON results from the vPIC API.

This client automatically standardizes variable names where vPIC uses inconsistent naming. Disable this to see the unaltered JSON responses:

```python
from vpic import Client

c = Client(standardize_names=False)
```

### Decode a VIN

Get the characteristics of a vehicle by it's 17-digit Vehicle Identification Number (VIN):

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
