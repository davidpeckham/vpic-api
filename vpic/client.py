import logging
from typing import Any, Dict, List, Union

from .client_base import ClientBase

log = logging.getLogger(__name__)


class Client(ClientBase):
    """
    A client for the United States National Highway Traffic Safety
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

    See https://vpic.nhtsa.dot.gov/api/home/index/faq for more on the API.

    """

    host = "https://vpic.nhtsa.dot.gov/api/vehicles"

    def __init__(
        self,
        host="https://vpic.nhtsa.dot.gov/api/vehicles/",
        standardize_variables=True,
    ):
        """
        Instantiate a new API client.

        Parameters
        ----------
        host : str
            Hostname, including http(s)://, of the vPIC instance to query
        standardize_variables: bool
            vPIC uses different names for the same variable. Set this to True
            to standardize variables before returning the response.

        """
        super(Client, self).__init__(host, standardize_variables)

    def decode_vin(
        self, vin: str, model_year: int = None, extend=False, flatten=True
    ) -> Dict[str, Any]:
        """
        Decode the make, model, series, trim, and other vehicle information
        from VIN. Model year is required for pre-1980 vehicles, though vPIC
        recommends that you always pass it.

        If you don't have a complete 17-digit VIN, you can pass a partial
        VIN, using asterisk (*) for missing characters. The VIN check digit
        (the 9th character) isn't required for partial VINs. The shorter the
        partial VIN, the less vehicle information you'll receive in the
        response.

        See get_vehicle_variable_list for the variables returned here.

        Parameters
        ----------
        vin : str
            A 17-digit VIN or partial VIN. Use asterisk for missing
            characters
        model_year : int
            The vehicle's model year. Recommended, but not required.
        extend : bool
            If True, response will include variables for other NHTSA
            programs like NCSA. Defaults to False.
        flatten : bool
            True to receive vehicle variables in key-value pairs (this is the
            default and usually best choice). False to receive them as a list
            of variable objects that include the variable ID.

        """

        if vin is None:
            raise ValueError("vin is required")
        if not len(vin) in range(6, 17 + 1):
            raise ValueError(
                "vin must be at least 3 characters and at most 17 characters"
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
        """
        Decode the make, model, series, trim, and other vehicle information
        for a list of VINs:

        [
            "VIN, model_year",
            "VIN, model_year",
            "VIN, model_year",
            ...
        ]

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

        Parameters
        ----------
        vins : List[str]
            A list of 17-digit VINs or partial VINs and optional model year.
            Use asterisk for missing characters

        """

        if vins is None:
            raise ValueError("vins is required")

        if not len(vins) in range(1, 50 + 1):
            raise ValueError("pass at least one VIN, and at most 50 VINs")

        return self._request_post("DecodeVINValuesBatch", data={"DATA": ";".join(vins)})

    def decode_wmi(self, wmi: str) -> Dict[str, Any]:
        """
        This provides information on the World Manufacturer Identifier for a
        specific WMI code. WMIs may be put in as either 3 characters
        representing VIN position 1-3 or 6 characters representing VIN
        positions 1-3 & 12-14. Example "JTD", "1T9131".

        Parameters
        ----------
        wmi : str
            A 3-character or 6-character World Manufacturer Index code

        Example
        -------
        decode_wmi('1FT')

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
            "WMI": "1FT"
        }

        """

        if not len(wmi) in [3, 6]:
            raise ValueError("WMI must be 3 or 6 characters")

        result = self._request(f"DecodeWMI/{wmi}")[0]
        result["WMI"] = wmi
        return result

    def get_wmis_for_manufacturer(
        self, manufacturer: Union[str, int]
    ) -> List[Dict[str, Any]]:
        """
        Returns the WMIs for one or more manufacturers who are registered
        with vPIC.

        Parameters
        ----------
        manufacturer : Union[str, int]
            Pass the Manufacturer Id (int) or the complete manufacturer
            name (str) to return WMIs for a single manufacturer. Pass a
            partial name to return WMIs for all manufacturers with names
            that include the partial name.

        Example
        -------
        get_wmis_for_manufacturer('Honda')

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

        if manufacturer is None:
            raise ValueError("manufacturer is required")

        wmis = self._request(f"GetWMIsForManufacturer/{manufacturer}")

        for wmi in wmis:
            wmi["ManufacturerId"] = wmi["Id"]
            del wmi["Id"]
            wmi["ManufacturerName"] = wmi["Name"]
            del wmi["Name"]

        return wmis

    def get_all_makes(self) -> List[Dict[str, Any]]:
        """
        Returns all of the makes registered with vPIC.

        Example
        -------
        get_all_makes()

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
        """
        Returns a list of documents submitted by manufacturers to NHTSA
        to comply with these regulations:

        * 49 CFR Part 565 (Vehicle Identification Number Guidance)
        * 49 CFR Part 566 (Manufacturer Identification – Reporting Requirements)

        This provides a list of ORGs with letter date in the given range
        of the dates and with specified Type of ORG. Up to 1000 results
        will be returned at a time.

        Parameters
        ----------
        cfr_part : str
            '565' to return 49 CFR Part 565 submissions
            '566' to return 49 CFR Part 566 submissions
        from_date : str
            the beginning of the publication date range to search
        end_date : str
            the end of the publication date range to search
        page: int
            results are paginated; this is the number of the page to return

        Example
        -------
        get_parts('565', '2015-01-01', '2015-05-05', 1)

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
        """
        Return a list of vPIC manufacturers of the given manufacturer_type.

        This provides a list of all the Manufacturers available in vPIC Dataset.

        Parameters
        ----------
        manufacturer_type : str (optional)
            The manufacturer type, which is Incomplete Vehicles, Completed
            Vehicle Manufacturer, Incomplete Vehicle Manufacturer, Intermediate
            Manufacturer, Final-Stage Manufacturer, Alterer, Replica Vehicle
            Manufacturer. You can pass the full type name, or a substring of
            the type. See get_vehicle_variable_values_list("Manufacturer Type")
            for the list of manufacturer types.
        page: int
            results are paginated; this is the number of the page to return

        Example
        -------
        get_all_manufacturers("Completed Vehicle", 1)

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
        """
        Returns details for one or more manufacturers.

        Parameters
        ----------
        manufacturer : Union[str, int]
            Pass the Manufacturer Id (int) or the complete manufacturer
            name (str) to return detail for a single manufacturer. Pass a
            partial name to return manufacturers with names that include
            the partial name.

        Example
        -------
        get_manufacturer_details(988)

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
        """
        Returns makes produced by a manufacturer or manufacturers.

        Parameters
        ----------
        manufacturer : Union[str, int]
            Pass the Manufacturer Id (int) or the complete manufacturer
            name (str) to return detail for a single manufacturer. Pass a
            partial name to return manufacturers with names that include
            the partial name.
        model_year : int
            Optional. Pass a model year to return only those makes made by
            the manufacturer for that model year.

        Example
        -------
        get_makes_for_manufacturer(988)

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
        """
        Returns makes that produce a vehicle_type

        Parameters
        ----------
        vehicle_type : str
            A vPIC vehicle_type. For example, "Passenger Car", "Truck",
            or "Multipurpose Passenger Vehicle (MPV)". If you pass a
            partial vehicle_type, for example "Passenger", results will
            include makes for all matching vehicle types. Matching is not
            case sensitive.

        Example
        -------
        get_makes_for_vehicle_type('Car')

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
        """
        Returns vehicle types produced by a make or makes

        Parameters
        ----------
        make : Union[int,str]
            Pass the MakeId (int) or the complete make name (str) to return
            vehicle types for a single manufacturer. Pass a partial make name
            to return vehicle types for all makes that match the partial name.
            When you pass a make name, results will include the MakeId and
            MakeName because you may get vehicle_types for more than one make.

        Examples
        --------

        get_vehicle_types_for_make(499)

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

        get_vehicle_types_for_make('kia')

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
        """
        Returns a list of plants that manufacture certain vehicle equipment.
        Plants have a unique three-character U.S. Department of Transportation
        (DOT) code.

        vPIC API documentation says this API only accepts 2016 and later.

        Parameters
        ----------
        year : int
            must be 2016 or later
        equipment_type : int
            return plants that manufacture one of these equipment types:
              1 = Tires
              3 = Brake Hoses
              13 = Glazing
              16 = Retread
        report_type : str
            must be one of:
              New = plants whose code was assigned during the selected year
              Updated = plants whose data was modified during the selected year
              Closed = plants that are no longer active
              All = all active and closed plants, regardless of year

        Example
        -------
        get_equipment_plant_codes(2016, 1)

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
        """
        Return a list of models for a make or makes. Optionally filter by
        model year and vehicle type.

        Parameters
        ----------
        make : Union[int,str]
            Pass the MakeId (int) or the complete make name (str) to return
            vehicle types for a single manufacturer. Pass a partial make name
            to return vehicle types for all makes that match the partial name.
            When you pass a make name, results will include the MakeId and
            MakeName because you may get vehicle_types for more than one make.
        modelyear: int
            the model year
        vehicle_type : str
            one of the vPIC vehicle_types (for example, "Passenger Car",
            "Truck", or "Multipurpose Passenger Vehicle (MPV)")

        Returns
        -------
        [
            {
                "MakeId": 474,
                "MakeName": "HONDA",
                "Model_ID": 1864,
                "Model_Name": "Pilot",
                "VehicleTypeId": 7,
                "VehicleTypeName": "Multipurpose Passenger Vehicle (MPV)"
            },
            ...
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
        """
        Return a list of vehicle variables tracked by vPIC

        """

        return self._request("GetVehicleVariableList")

    def get_vehicle_variable_values_list(
        self, variable_name: str
    ) -> List[Dict[str, Any]]:
        """
        Return the values for a vehicle variable

        Parameters
        ----------
        variable_name : str
            the name of the vehicle variable

        """

        if variable_name is None:
            raise ValueError("variable_name is required")

        return self._request(f"GetVehicleVariableValuesList/{variable_name}")

    def get_canadian_vehicle_specifications(
        self, year: int, make: str, model: str = None, units: str = "Metric"
    ) -> List[Dict[str, Any]]:
        """
        Return the values for a vehicle variable

        Parameters
        ----------
        variable_name : str
            the name of the vehicle variable

        """

        params = {"Year": year, "Make": make, "Model": model, "units": units}

        return self._request("GetCanadianVehicleSpecifications", params=params)
