import logging
from typing import Any, Dict, List, Optional, Union

from .client_base import ClientBase

log = logging.getLogger(__name__)


class Client(ClientBase):
    """A client library for the U.S. NHTSA vPIC API

    ``Client`` returns JSON responses from the vPIC API. vPIC responses
    don't always use the same name for a variable, so by default this
    library standardizes variable names. You can disable this by creating
    a client like this:

        ``c = Client(standardize_names=False)``

    If you prefer to receive model objects instead of JSON responses,
    use ``vpic.Client`` instead.

    A client library for the United States National Highway Traffic Safety
    Administration (NHTSA) Vehicle Product Information Catalog (vPIC) Vehicle
    Listing API.

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

    vPIC has all of the information about how manufacturers assign a VIN that
    encodes the vehicles characteristics. Vehicle manufacturers provide this
    information to NHTSA under U.S. law 49 CFR Part 565.

    The API available 24/7, is free to use, and does not require registration.
    NHTSA uses automatic traffic rate controls to maintain the performance of
    the API and their websites that use the API.

    See https://vpic.nhtsa.dot.gov/api for more on the API.

    Attributes:
        host: Hostname, including http(s)://, of the vPIC instance to query.
        standardize_variables: vPIC uses different names for the same
            variable, so this client standarizes those names by default.
            Set this to False to receive the raw vPIC response.

    """

    def __init__(
        self,
        host: Optional[str] = "https://vpic.nhtsa.dot.gov/api/vehicles/",
        standardize_variables: bool = True,
    ):
        super(Client, self).__init__(host, standardize_variables)

    def decode_vin(
        self, vin: str, model_year: int = None, extend=False, flatten=True
    ) -> Dict[str, Any]:
        """Decode a 17-digit Vehicle Identification Number (VIN) or partial VIN.

        Decode the make, model, series, trim, and other vehicle information
        from VIN. Model year is required for pre-1980 vehicles, though vPIC
        recommends that you always pass it.

        If you don't have a complete 17-digit VIN, you can pass a partial
        VIN, using asterisk (*) for missing characters. The VIN check digit
        (the 9th character) isn't required for partial VINs. The shorter the
        partial VIN, the less vehicle information you'll receive in the
        response.

        See get_vehicle_variable_list for the variables returned here.

        Args:
            vin: A 17-digit VIN or partial VIN. Use asterisk for missing
                characters.
            model_year: The vehicle's model year. Recommended, but not required.
            extend: If True, response will include variables for other NHTSA
                programs like NCSA. Defaults to False.
            flatten: True to receive vehicle variables in key-value pairs (this is
                the default and usually best choice). False to receive them as a
                list of variable objects that include the variable ID.

        Raises:
            ValueError: if ``vin`` is missing or isn't 6 to 17 characters long.
            ValueError: if ``model_year`` is earlier than 1981.

        """
        if vin is None:
            raise ValueError("vin is required")
        if not len(vin) in range(6, 17 + 1):
            raise ValueError(
                "vin must be at least 6 characters and at most 17 characters"
            )
        if model_year and model_year < 1981:
            raise ValueError("model year must be 1981 or later")

        endpoint = "DecodeVin"
        if flatten:
            endpoint = "DecodeVinValues"
        if extend:
            endpoint = f"{endpoint}Extended"

        if model_year is not None:
            params = {"modelyear": model_year}
        else:
            params = {}

        results = self._request(f"{endpoint}/{vin}", params)
        return results[0] if flatten else results

    def decode_vin_batch(self, vins: List[str]) -> List[Dict[str, Any]]:
        """Decode a batch of 17-digit VINs or partial VINs.

        Model year is required for pre-1980 vehicles, though vPIC recommends
        that you always pass it.

        If you don't have a complete 17-digit VIN, you can pass a partial
        VIN, using asterisk (*) for missing characters. The VIN check digit
        (the 9th character) isn't required for partial VINs. The shorter the
        partial VIN, the less vehicle information you'll receive in the
        response.

        Vehicle variables will be returned in key-value pairs, the same
        format returned by decode_vin(.., flatten=True).

        See get_vehicle_variable_list for the variables returned here.

        Args:
            vins: A list of 17-digit VIN or partial VINs and optional model year.
                Use asterisk for missing characters. For example: ["VIN, model_year",
                "VIN, model_year", ...]

        Raises:
            ValueError: if ``vin`` is missing or isn't 6 to 17 characters long.
            ValueError: if ``model_year`` is earlier than 1981.

        """
        if vins is None:
            raise ValueError("vins is required")

        if not len(vins) in range(1, 50 + 1):
            raise ValueError("pass at least one VIN, and at most 50 VINs")

        return self._request_post("DecodeVINValuesBatch", data={"DATA": ";".join(vins)})

    def decode_wmi(self, wmi: str) -> Dict[str, Any]:
        """Decode a WMI to get manufacturer information

        Provides information on the World Manufacturer Identifier for a
        specific WMI code.

        Args:
            wmi: A 3-character or 6-character World Manufacturer Index code.
                 Large volume manufacturers usually have a  3 character WMI
                 representing positions 1 to 3 ("JTD") of a VIN. Smaller
                 manufacturers have a 6 character WMI representing positions
                 1 to 3 and 12 to 14 of a VIN.

        Raises:
            ValueError: if ``wmi`` is missing or isn't 3 or 6 characters long.

        Example:
            >>> decode_wmi('1FT')
            {
                "CommonName": "Ford",
                "CreatedOn": "2015-03-23",
                "DateAvailableToPublic": "2015-01-01",
                "MakeName": "FORD",
                "ManufacturerName": "FORD MOTOR COMPANY, USA",
                "ParentCompanyName": "",
                "URL": "http://www.ford.com/",
                "UpdatedOn": null,
                "VehicleType": "Truck ",
            }

        """
        if not len(wmi) in [3, 6]:
            raise ValueError("WMI must be 3 or 6 characters")

        result = self._request(f"DecodeWMI/{wmi}")[0]
        # result["WMI"] = wmi
        return result

    def get_wmis_for_manufacturer(
        self,
        manufacturer: Optional[Union[str, int]] = None,
        vehicle_type: Optional[Union[str, int]] = None,
    ) -> List[Dict[str, Any]]:
        """Returns the WMIs for one or all manufacturers

        You must pass one or both of provide manufacturer or vehicle_type.

        Args:
            manufacturer: Pass the Manufacturer Id (int) or the complete
                manufacturer name (str) to return WMIs for a single manufacturer.
                Pass a partial name to return WMIs for all manufacturers with
                names that include the partial name.
            vehicle_type: Pass the vehicle_type Id (int) or complete vehicle_type
                name to return WMIs for that vehicle_type. Pass a partial name to
                return WMIs for vehicle_types matching that name.

        Raises:
            ValueError: if ``manufacturer`` and ``vehicle_type`` are missing

        Examples:
            >>> get_wmis_for_manufacturer('Honda')
            [
                {
                    "Country": null,
                    "CreatedOn": "2015-03-26",
                    "DateAvailableToPublic": "2015-01-01",
                    "Id": 987,
                    "Name": "HONDA MOTOR CO., LTD",
                    "UpdatedOn": "2015-06-04",
                    "VehicleType": "Passenger Car",
                    "WMI": "JHM"
                },
                ...
            ]

        """
        if manufacturer is None and vehicle_type is None:
            raise ValueError("manufacturer or vehicle_type is required")

        if manufacturer is None:
            endpoint = "GetWMIsForManufacturer"
        else:
            endpoint = f"GetWMIsForManufacturer/{manufacturer}"

        params = {}
        if vehicle_type:
            params["vehicleType"] = vehicle_type

        wmis = self._request(endpoint, params)

        # for wmi in wmis:
        #     wmi["ManufacturerId"] = wmi["Id"]
        #     del wmi["Id"]
        #     wmi["Manufacturer"] = wmi["Name"]
        #     del wmi["Name"]

        return wmis

    def get_all_makes(self) -> List[Dict[str, Any]]:
        """Returns all of the makes registered with vPIC.

        Examples:
            >>> get_all_makes()
            [
                {
                    "MakeId": 440,
                    "MakeName": "ASTON MARTIN"
                },
                {
                    "MakeId": 441,
                    "MakeName": "TESLA"
                },
                {
                    "MakeId": 442,
                    "MakeName": "JAGUAR"
                },
                ...
            ]

        """
        return self._request("GetAllMakes")

    def get_parts(
        self, cfr_part: str, from_date: str, to_date: str, page: int = 1
    ) -> List[Dict[str, Any]]:
        """Returns a list of vehicle documentation submitted by manufacturers.

        Manufacturers provide vehicle information to NHTSA to comply with these
        regulations:

        * 49 CFR Part 565 (Vehicle Identification Number Guidance)
        * 49 CFR Part 566 (Manufacturer Identification – Reporting Requirements)

        This provides a list of documents submitted in a date range. Up to 1,000
        results will be returned at a time.

        Args:
            cfr_part: '565' to return 49 CFR Part 565 submissions;
                '566' to return 49 CFR Part 566 submissions
            from_date: the beginning of the date range to search
            end_date: the end of the date range to search
            page: results are paginated; this is page number to return

        Raises:
            ValueError: if ``cvr_part`` is missing

        Examples:
            >>> get_parts('565', '2015-01-01', '2015-05-05', 1)
            [
                {
                    "CoverLetterURL": "",
                    "LetterDate": "5/5/2015",
                    "ManufacturerId": 8012,
                    "ManufacturerName": "PORSCHE CARS NORTH AMERICA, INC.",
                    "ModelYearFrom": null,
                    "ModelYearTo": null,
                    "Name": "ORG10658",
                    "Type": null,
                    "URL": "http://vpic.nhtsa.dot.gov/mid/home/displayfile/[guid here]"
                },
                ...
            ]

        """
        if cfr_part is None:
            raise ValueError("cfr_part is required")

        params = {
            "type": cfr_part,
            "fromDate": from_date,
            "toDate": to_date,
            "page": page,
        }
        return self._request("GetParts", params)

    def get_all_manufacturers(
        self, manufacturer_type: str = None, page: int = 1
    ) -> List[Dict[str, Any]]:
        """Return a list of vPIC manufacturers of the given manufacturer_type.

        This provides a list of all the Manufacturers available in vPIC Dataset.

        See ``get_vehicle_variable_values_list("Manufacturer Type")`` for the list
        of manufacturer types.

        Args:
            manufacturer_type: The manufacturer type, which is Incomplete Vehicles,
                Completed Vehicle Manufacturer, Incomplete Vehicle Manufacturer,
                Intermediate Manufacturer, Final-Stage Manufacturer, Alterer,
                Replica Vehicle Manufacturer. You can pass the full type name, or a
                substring of the type.
            page: results are paginated; this is the page number to return

        Examples:
            >>> get_all_manufacturers("Completed Vehicle", 1)
            [
                {
                "Country": "UNITED STATES (USA)",
                "Mfr_CommonName": "Tesla",
                "Mfr_ID": 955,
                "Mfr_Name": "TESLA, INC.",
                "VehicleTypes": [
                    {
                        "IsPrimary": true,
                        "Name": "Passenger Car"
                    },
                    {
                        "IsPrimary": false,
                        "Name": "Multipurpose Passenger Vehicle (MPV)"
                    }
                },
                ...
            ]

        """
        params = {"ManufacturerType": manufacturer_type, "page": page}
        return self._request("GetAllManufacturers", params)

    def get_manufacturer_details(
        self, manufacturer: Union[str, int]
    ) -> List[Dict[str, Any]]:
        """Returns details for one or more manufacturers.

        Args:
            manufacturer: Pass the Manufacturer Id (int) or the complete
                manufacturer name (str) to return detail for a single
                manufacturer. Pass a partial name to return manufacturers
                with names that include the partial name.

        Examples:
            >>> get_manufacturer_details(988)
            [
                {
                    "Address": "1919 Torrance Blvd.",
                    "Address2": null,
                    "City": "Torrance",
                    "ContactEmail": "jeff_chang@ahm.honda.com",
                    "ContactFax": null,
                    "ContactPhone": "(310)783-3401",
                    "Country": "UNITED STATES (USA)",
                    "DBAs": "...",
                    "EquipmentItems": [],
                    "LastUpdated": "/Date(1618422117803-0400)/",
                    "ManufacturerTypes": [
                        {
                            "Name": "Completed Vehicle Manufacturer"
                        }
                    ],
                    "Mfr_CommonName": "Honda",
                    "Mfr_ID": 988,
                    "Mfr_Name": "HONDA DEVELOPMENT & MANUFACTURING OF AMERICA, LLC",
                    "OtherManufacturerDetails": null,
                    "PostalCode": "90501",
                    "PrimaryProduct": null,
                    "PrincipalFirstName": "Shinji Aoyama",
                    "PrincipalLastName": null,
                    "PrincipalPosition": "President & CEO",
                    "StateProvince": "CALIFORNIA",
                    "SubmittedName": "Wilson Tran",
                    "SubmittedOn": "/Date(1618286400000-0400)/",
                    "SubmittedPosition": "Sr. Specialist, II",
                    "VehicleTypes": [
                        {
                            "GVWRFrom": "Class 1A: 3,000 lb or less (1,360 kg or less)",
                            "GVWRTo": "Class 1D: 5,001 - 6,000 lb (2,268 - 2,722 kg)",
                            "IsPrimary": true,
                            "Name": "Passenger Car"
                        },
                        {
                            "GVWRFrom": "Class 2E: 6,001 - 7,000 lb (2,722 - 3,175 kg)",
                            "GVWRTo": "Class 2E: 6,001 - 7,000 lb (2,722 - 3,175 kg)",
                            "IsPrimary": false,
                            "Name": "Truck "
                        },
                        {
                            "GVWRFrom": "Class 1B: 3,001 - 4,000 lb (1,360 - 1,814 kg)",
                            "GVWRTo": "Class 2E: 6,001 - 7,000 lb (2,722 - 3,175 kg)",
                            "IsPrimary": false,
                            "Name": "Multipurpose Passenger Vehicle (MPV)"
                        }
                    ]
                }
                ...
            ]

        """
        if manufacturer is None:
            raise ValueError("manufacturer is required")

        return self._request(f"GetManufacturerDetails/{manufacturer}")

    def get_makes_for_manufacturer(
        self, manufacturer: Union[str, int], model_year: int = None
    ) -> List[Dict[str, Any]]:
        """Returns makes produced by a manufacturer or manufacturers.

        Args:
            manufacturer: Pass the Manufacturer Id (int) or the complete
                manufacturer name (str) to return detail for a single manufacturer.
                Pass a partial name to return manufacturers with names that include
                the partial name.
            model_year: Pass a model year to return only those makes made by
                the manufacturer for that model year.

        Raises:
            ValueError: if ``manufacturer`` is missing

        Examples:
            >>> get_makes_for_manufacturer(988)
            [
                {
                    "MakeId": 474,
                    "MakeName": "HONDA",
                    "Mfr_Name": "HONDA DEVELOPMENT & MANUFACTURING OF AMERICA, LLC"
                },
                {
                    "MakeId": 475,
                    "MakeName": "ACURA",
                    "Mfr_Name": "HONDA DEVELOPMENT & MANUFACTURING OF AMERICA, LLC"
                }
                ...
            ]

        """
        if manufacturer is None:
            raise ValueError("manufacturer is required")

        if model_year:
            results = self._request(
                f"GetMakesForManufacturerAndYear/{manufacturer}", {"year": model_year}
            )
        else:
            results = self._request(f"GetMakeForManufacturer/{manufacturer}")

        return results

    def get_makes_for_vehicle_type(self, vehicle_type: str) -> List[Dict[str, Any]]:
        """Returns makes that produce a vehicle_type

        Args:
            vehicle_type: A vPIC vehicle_type. For example, "Passenger Car",
                "Truck", or "Multipurpose Passenger Vehicle (MPV)". If you pass
                a partial vehicle_type, for example "Passenger", results will
                include makes for all matching vehicle types. Matching is not
                case sensitive.

        Raises:
            ValueError: if ``vehicle_type`` is missing

        Examples:
            >>> get_makes_for_vehicle_type('Car')
            [
                {
                    "MakeId": 440,
                    "MakeName": "ASTON MARTIN",
                    "VehicleTypeId": 2,
                    "VehicleTypeName": "Passenger Car"
                },
                {
                    "MakeId": 441,
                    "MakeName": "TESLA",
                    "VehicleTypeId": 2,
                    "VehicleTypeName": "Passenger Car"
                },
                ...
            ]

        """
        if vehicle_type is None:
            raise ValueError("vehicle_type is required")

        return self._request(f"GetMakesForVehicleType/{vehicle_type}")

    def get_vehicle_types_for_make(self, make: Union[str, int]) -> List[Dict[str, Any]]:
        """Returns vehicle types produced by a make or make

        Args:
            make: Pass the MakeId (int) or the complete make name (str) to return
                vehicle types for a single manufacturer. Pass a partial make name
                to return vehicle types for all makes that match the partial name.
                When you pass a make name, results will include the MakeId and
                MakeName because you may get vehicle_types for more than one make.

        Raises:
            ValueError: if ``make`` is missing

        Examples:
            >>> get_vehicle_types_for_make(474)
            [
                {
                    "VehicleTypeId": 1,
                    "VehicleTypeName": "Motorcycle"
                },
                {
                    "VehicleTypeId": 2,
                    "VehicleTypeName": "Passenger Car"
                },
                {
                    "VehicleTypeId": 3,
                    "VehicleTypeName": "Truck "
                },
                {
                    "VehicleTypeId": 7,
                    "VehicleTypeName": "Multipurpose Passenger Vehicle (MPV)"
                },
                {
                    "VehicleTypeId": 9,
                    "VehicleTypeName": "Low Speed Vehicle (LSV)"
                }
            ]

            >>> get_vehicle_types_for_make('kia')
            [
                {
                    "MakeId": 499,
                    "MakeName": "KIA",
                    "VehicleTypeId": 2,
                    "VehicleTypeName": "Passenger Car"
                },
                {
                    "MakeId": 499,
                    "MakeName": "KIA",
                    "VehicleTypeId": 7,
                    "VehicleTypeName": "Multipurpose Passenger Vehicle (MPV)"
                },
                {
                    "MakeId": 5848,
                    "MakeName": "MGS GRAND SPORT (MARDIKIAN)",
                    "VehicleTypeId": 2,
                    "VehicleTypeName": "Passenger Car"
                }
            ]

        """
        if make is None:
            raise ValueError("make is required")

        if isinstance(make, int):
            return self._request(f"GetVehicleTypesForMakeId/{make}")
        else:
            return self._request(f"GetVehicleTypesForMake/{make}")

    def get_equipment_plant_codes(
        self, year: int, equipment_type: int, report_type: str = "All"
    ) -> List[Dict[str, Any]]:
        """Returns a list of plants that manufacture certain vehicle equipment.

        Plants have a unique three-character U.S. Department of Transportation
        (DOT) code. vPIC API documentation says this API only accepts 2016 and
        later.

        Args:
            year: must be 2016 or later
            equipment_type: return plants that manufacture one of these equipment
                types: 1 = Tires; 3 = Brake Hoses; 13 = Glazing; 16 = Retread
            report_type: must be one of
                New = plants whose code was assigned during the selected year
                Updated = plants whose data was modified during the selected year
                Closed = plants that are no longer active
                All = all active and closed plants, regardless of year

        Raises:
            ValueError: if ``year`` is earlier than 2016

        Example:
            >>> get_equipment_plant_codes(2016, 1)
            [
                {
                    "Address": "2950 INTERNATIONAL BLVD.",
                    "City": "CLARKSVILLE",
                    "Country": "USA",
                    "DOTCode": "00T",
                    "Name": "HANKOOK TIRE MANUFACTURING TENNESSEE, LP",
                    "OldDotCode": "",
                    "PostalCode": "37040",
                    "StateProvince": "TENNESSEE",
                    "Status": "Active"
                },
                ...
            ]

        """
        if year < 2016:
            raise ValueError("Year must be 2016 or later")

        params = {
            "year": year,
            "equipmentType": equipment_type,
            "reportType": report_type,
        }
        return self._request("GetEquipmentPlantCodes", params)

    def get_models_for_make(
        self, make: Union[int, str], model_year: int = None, vehicle_type: str = None
    ) -> List[Dict[str, Any]]:
        """Return a list of models for a make or makes.

        Optionally filter the results by model year and vehicle type.

        Args:
            make: Pass the MakeId (int) or the complete make name (str) to return
                vehicle types for a single manufacturer. Pass a partial make name
                to return vehicle types for all makes that match the partial name.
                When you pass a make name, results will include the MakeId and
                MakeName because you may get vehicle_types for more than one make.
            model_year: pass this to return models made in this model year
            vehicle_type: one of the vPIC vehicle_types (for example, "Passenger Car",
                "Truck", or "Multipurpose Passenger Vehicle (MPV)")

        Raises:
            ValueError: if ``year`` is earlier than 2016

        Examples:
            >>> get_models_for_make("TESLA", model_year=2020)
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

        VehicleTypeId and VehicleTypeName are only returned
        when you specify vehicle_type.

        """
        if make is None:
            raise ValueError("make is required")

        if model_year or vehicle_type:
            my = f"/modelyear/{model_year}" if model_year else ""
            vt = f"/vehicletype/{vehicle_type}" if vehicle_type else ""
            if isinstance(make, int):
                endpoint = f"GetModelsForMakeIdYear/makeId/{make}{my}{vt}"
            else:
                endpoint = f"GetModelsForMakeYear/make/{make}{my}{vt}"
        else:
            if isinstance(make, int):
                endpoint = f"GetModelsForMakeId/{make}"
            else:
                endpoint = f"GetModelsForMake/{make}"

        return self._request(endpoint)

    def get_vehicle_variable_list(self) -> List[Dict[str, Any]]:
        """Return a list of vehicle variables tracked by vPIC

        Examples:
            >>> get_vehicle_variable_list()
            [
                {
                    "DataType": "string",
                    "Description": "<p>Any other battery information that does...",
                    "Id": 1,
                    "Name": "Other Battery Info"
                },
                {
                    "DataType": "lookup",
                    "Description": "<p>Battery type field stores the battery ...",
                    "Id": 2,
                    "Name": "Battery Type"
                },
                {
                    "DataType": "lookup",
                    "Description": "<p>Bed type is the type of bed (the open b...",
                    "Id": 3,
                    "Name": "Bed Type"
                },
                {
                    "DataType": "lookup",
                    "Description": "<p>Cab type applies to both pickup truck ...",
                    "Id": 4,
                    "Name": "Cab Type"
                },
                {
                    "DataType": "lookup",
                    "Description": "<p>Body Class presents the Body Type, bas...",
                    "Id": 5,
                    "Name": "Body Class"
                },
                ...
            ]

        """
        return self._request("GetVehicleVariableList")

    def get_vehicle_variable_values_list(
        self, variable_name: str
    ) -> List[Dict[str, Any]]:
        """Return the values for a vehicle variable

        Args:
            variable_name: the name of the vehicle variable

        Raises:
            ValueError: if ``variable_name`` is missing

        Examples:
            >>> get_vehicle_variable_values_list("Vehicle Type")
            [
                {
                    "ElementName": "Vehicle Type",
                    "Id": 1,
                    "Name": "Motorcycle"
                },
                {
                    "ElementName": "Vehicle Type",
                    "Id": 2,
                    "Name": "Passenger Car"
                },
                {
                    "ElementName": "Vehicle Type",
                    "Id": 3,
                    "Name": "Truck "
                },
                {
                    "ElementName": "Vehicle Type",
                    "Id": 5,
                    "Name": "Bus"
                },
                {
                    "ElementName": "Vehicle Type",
                    "Id": 6,
                    "Name": "Trailer"
                },
                {
                    "ElementName": "Vehicle Type",
                    "Id": 7,
                    "Name": "Multipurpose Passenger Vehicle (MPV)"
                },
                {
                    "ElementName": "Vehicle Type",
                    "Id": 9,
                    "Name": "Low Speed Vehicle (LSV)"
                },
                {
                    "ElementName": "Vehicle Type",
                    "Id": 10,
                    "Name": "Incomplete Vehicle"
                },
                {
                    "ElementName": "Vehicle Type",
                    "Id": 13,
                    "Name": "Off Road Vehicle"
                }
            ]

        """
        if variable_name is None:
            raise ValueError("variable_name is required")

        return self._request(f"GetVehicleVariableValuesList/{variable_name}")

    def get_canadian_vehicle_specifications(
        self, year: int, make: str, model: str = None, units: str = "Metric"
    ) -> List[Dict[str, Any]]:
        """Get original vehicle dimensions from the Canadian Vehicle Specification.

        The Canadian Vehicle Specifications (CVS) consists of a database of
        original vehicle dimensions, used primarily in collision investigation
        and reconstruction, combined with a search engine. The database is
        compiled annually by the Collision Investigation and Research Division
        of Transport Canada.

        See [Canadian Vehicle Specifications](http://www.carsp.ca/research/resources
        /safety-sources/canadian-vehicle-specifications/).

        Args:
            year: 1971 or later
            make: a make name like "Honda", "Toyota", ...
            model: a model name like "Pilot", "Focus", ...
            units: "Metric" or "US"

        """
        params = {"Year": year, "Make": make, "Model": model, "units": units}
        return self._request("GetCanadianVehicleSpecifications", params=params)
