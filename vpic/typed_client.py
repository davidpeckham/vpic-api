import logging
import re
from typing import Any, Dict, List, Union

from .client import Client
from .model import (
    Document,
    Make,
    Manufacturer,
    ManufacturerDetail,
    ManufacturerType,
    Model,
    PlantCode,
    Vehicle,
    VehicleType,
    WorldManufacturerIndex,
    Variable,
    Value,
)

log = logging.getLogger(__name__)


class TypedClient:
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

    def __init__(self, host="https://vpic.nhtsa.dot.gov/api/vehicles/"):
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
        self._client = Client(host, standardize_variables=True)
        self._snake_re = re.compile(r"([A-Z]+)(?=([a-z_]|))")

    # def _snake_case(self, object: Union[Dict, List, str]) -> Union[Dict, List, str]:
    #     """
    #     Convert variable names (JSON keys) to snake case

    #     """

    #     if isinstance(object, dict):
    #         return {self._snake_case(key): value for key, value in object.items()}
    #     elif isinstance(object, list):
    #         return [self._snake_case(item) for item in object]
    #     else:
    #         return self._snake_re.sub(r"_\1", object).lower()

    def _snake_case(self, object: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert variable names (JSON keys) to snake case

        """

        # TODO simplify this
        new_object: Dict[str, Any] = {}
        for key, value in object.items():
            new_key = self._snake_re.sub(r"_\1", key).lower()
            new_key = new_key.replace("__", "_")
            if new_key[0] == '_':
                new_key = new_key[1:]
            new_key = new_key.replace("ncsa", "ncsa_")
            new_key = new_key.replace("evdrive", "ev_drive")
            new_key = new_key.replace("sae", "sae_")
            new_key = new_key.replace("dotcode", "dot_code")
            new_object[new_key] = value
        return new_object

        # return {
        #     self._snake_re.sub(r"_\1", key).lower(): value
        #     for key, value in object.items()
        # }

    def decode_vin(self, vin: str, model_year: int = None, extend=False) -> Vehicle:
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

        Example
        -------
        decode_vin('1FTMW1T88MFA00001')

        Vehicle(
            abs="",
            ...
            body_cab_type="Crew/ Super Crew/ Crew Max",
            body_class="Pickup",
            brake_system_desc="",
            brake_system_type="Hydraulic",
            ...
            displacementcc="3500.0",
            displacementci="213.58310433156",
            displacementl="3.5",
            ...
            drive_type="4WD/4-Wheel Drive/4x4",
            ...
            engine_configuration="V-Shaped",
            engine_cycles="",
            engine_cylinders="6",
            enginehp="375",
            enginehp_to="",
            enginekw="279.6375",
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

        """

        return Vehicle(
            **self._snake_case(self._client.decode_vin(vin, model_year, extend))
        )

    def decode_vin_batch(self, vins: List[str]) -> List[Vehicle]:
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

        Example
        -------
        decode_vin_batch(["5UXWX7C5*BA,2011", "5YJSA3DS*EF"])

        [
            Vehicle(...),
            Vehicle(...),
        ]

        """
        return [
            Vehicle(**self._snake_case(v)) for v in self._client.decode_vin_batch(vins)
        ]

    def decode_wmi(self, wmi: str) -> WorldManufacturerIndex:
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

        WorldManufacturerIndex(
            common_name="Ford",
            created_on="2015-03-23",
            date_available_to_public="2015-01-01",
            make="FORD",
            manufacturer_name="FORD MOTOR COMPANY, USA",
            parent_company_name="",
            updated_on=None,
            url="http://www.ford.com/",
            vehicle_type="Truck ",
        )

        """

        return WorldManufacturerIndex(**self._snake_case(self._client.decode_wmi(wmi)))

    def get_wmis_for_manufacturer(
        self, manufacturer: Union[str, int]
    ) -> List[WorldManufacturerIndex]:
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
            WorldManufacturerIndex(
                created_on='2015-03-26',
                date_available_to_public='2015-01-01',
                manufacturer_name='HONDA MOTOR CO., LTD',
                updated_on='2015-06-04',
                vehicle_type='Passenger Car',
                wmi='JHM', common_name='',
                country=None,
                make_name='',
                manufacturer_id=987,
                parent_company_name='',
                url=''),
            ...
        ]

        """

        wmis = self._client.get_wmis_for_manufacturer(manufacturer)
        return [WorldManufacturerIndex(**self._snake_case(wmi)) for wmi in wmis]

    def get_all_makes(self) -> List[Make]:
        """
        Returns all of the makes registered with vPIC.

        Example
        -------
        get_all_makes()

        [
            Make(make_id=440, make_name='ASTON MARTIN'),
            Make(make_id=441, make_name='TESLA'),
            Make(make_id=442, make_name='JAGUAR'),
            Make(make_id=443, make_name='MASERATI'),
            Make(make_id=444, make_name='LAND ROVER'),
            Make(make_id=445, make_name='ROLLS ROYCE'),
            Make(make_id=446, make_name='BUELL (EBR)'),
            Make(make_id=447, make_name='JIALING'),
            Make(make_id=448, make_name='TOYOTA'),
            Make(make_id=449, make_name='MERCEDES-BENZ'),
            ...
        ]

        """

        return [Make(**self._snake_case(m)) for m in self._client.get_all_makes()]

    def get_parts(
        self, cfr_part: str, from_date: str, to_date: str, page: int = 1
    ) -> List[Document]:
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
            Document(
                cover_letter_url='',
                letter_date='1/1/2015',
                manufacturer_id=959,
                manufacturer_name='MASERATI NORTH AMERICA, INC.',
                name='ORG13044',
                url='...',
                type=None,
                model_year_from=None,
                model_year_to=None
            ),
            ...
        ]

        """

        documents = self._client.get_parts(cfr_part, from_date, to_date, page)
        for doc in documents:
            # _snake_case can't handle lowerUPPER
            doc["CoverLetterUrl"] = doc["CoverLetterURL"]
            del doc["CoverLetterURL"]
        return [Document(**self._snake_case(doc)) for doc in documents]

    def get_all_manufacturers(
        self, manufacturer_type: str = None, page: int = 1
    ) -> List[Manufacturer]:
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
        raise NotImplementedError

    def get_manufacturer_details(
        self, manufacturer: Union[str, int]
    ) -> List[ManufacturerDetail]:
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
            ManufacturerDetail(
                manufacturer_id=988,
                manufacturer_name='HONDA DEVELOPMENT & MANUFACTURING OF AMERICA, LLC',
                manufacturer_common_name='Honda',
                address='1919 Torrance Blvd.',
                address2=None,
                city='Torrance',
                contact_email='someone@ahm.honda.com',
                contact_fax=None,
                contact_phone='(310)555-1212',
                country='UNITED STATES (USA)',
                dbas='Marysville Auto Plant and East Liberty Auto Plant; Alabama A...',
                equipment_items=[],
                last_updated='/Date(1618422117803-0400)/',
                manufacturer_types=[{'Name': 'Completed Vehicle Manufacturer'}],
                other_manufacturer_details=None,
                postal_code='90501',
                primary_product=None,
                principal_first_name='Shinji Aoyama',
                principal_last_name=None,
                principal_position='President & CEO',
                state_province='CALIFORNIA',
                submitted_name=None,
                submitted_on='/Date(1618286400000-0400)/',
                submitted_position=None,
                vehicle_types=[
                    {'GVWRFrom': 'Class 1A: 3,
                        000 lb or less (1,
                        360 kg or less)', 'GVWRTo': 'Class 1D: 5,
                        001 - 6,
                        000 lb (2,
                        268 - 2,
                        722 kg)', 'IsPrimary': True, 'Name': 'Passenger Car'
                    },
                    {'GVWRFrom': 'Class 2E: 6,
                        001 - 7,
                        000 lb (2,
                        722 - 3,
                        175 kg)', 'GVWRTo': 'Class 2E: 6,
                        001 - 7,
                        000 lb (2,
                        722 - 3,
                        175 kg)', 'IsPrimary': False, 'Name': 'Truck '
                    },
                    {'GVWRFrom': 'Class 1B: 3,
                        001 - 4,
                        000 lb (1,
                        360 - 1,
                        814 kg)', 'GVWRTo': 'Class 2E: 6,
                        001 - 7,
                        000 lb (2,
                        722 - 3,
                        175 kg)', 'IsPrimary': False, 'Name': 'Multipurpose Passen...'
                    }
                ]
            )
        ]

        """

        results = self._client.get_manufacturer_details(manufacturer)
        for r in results:
            r["dbas"] = r["DBAs"]
            del r["DBAs"]
            r["ManufacturerTypes"] = [
                ManufacturerType(name=mt["Name"]) for mt in r["ManufacturerTypes"]
            ]
            r["VehicleTypes"] = [
                VehicleType(
                    vehicle_type=vt["Name"],
                    is_primary=vt["IsPrimary"],
                    gvwr_from=vt["GVWRFrom"],
                    gvwr_to=vt["GVWRTo"],
                )
                for vt in r["VehicleTypes"]
            ]

        return [ManufacturerDetail(**self._snake_case(m)) for m in results]

    def get_makes_for_manufacturer(
        self, manufacturer: Union[str, int], model_year: int = None
    ) -> List[Make]:
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
            Make(
                make_id:474
                make_name:'HONDA'
                manufacturer_id:None
                manufacturer_name:'HONDA DEVELOPMENT & MANUFACTURING OF AMERICA, LLC'
            ),
            Make(
                make_id=475,
                make_name='ACURA',
                manufacturer_id=None,
                manufacturer_name='HONDA DEVELOPMENT & MANUFACTURING OF AMERICA, LLC'
            )
            ...
        ]

        """

        makes = self._client.get_makes_for_manufacturer(manufacturer, model_year)
        return [Make(**self._snake_case(m)) for m in makes]

    def get_makes_for_vehicle_type(self, vehicle_type: str) -> List[Make]:
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
            Make(
                make_id=440,
                make_name='ASTON MARTIN',
                manufacturer_id=None,
                manufacturer_name=None,
                vehicle_type_id=2,
                vehicle_type='Passenger Car'
            )
            ...
        ]

        """

        makes = self._client.get_makes_for_vehicle_type(vehicle_type)
        return [Make(**self._snake_case(m)) for m in makes]

    def get_vehicle_types_for_make(self, make: Union[str, int]) -> List[VehicleType]:
        """
        Returns vehicle types produced by a make or make

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

        get_vehicle_types_for_make(474)

        [
            VehicleType(
                vehicle_type_id=1,
                vehicle_type='Motorcycle',
                make_id=None,
                make_name=None
            ),
            VehicleType(
                vehicle_type_id=2,
                vehicle_type='Passenger Car',
                make_id=None,
                make_name=None
            ),
            VehicleType(
                vehicle_type_id=3,
                vehicle_type='Truck ',
                make_id=None,
                make_name=None
            ),
            VehicleType(
                vehicle_type_id=7,
                vehicle_type='Multipurpose Passenger Vehicle (MPV)',
                make_id=None,
                make_name=None
            ),
            VehicleType(
                vehicle_type_id=9,
                vehicle_type='Low Speed Vehicle (LSV)',
                make_id=None,
                make_name=None
            )
        ]

        """

        types = self._client.get_vehicle_types_for_make(make)
        return [VehicleType(**self._snake_case(vt)) for vt in types]

    def get_equipment_plant_codes(
        self, year: int, equipment_type: int, report_type: str = "All"
    ) -> List[PlantCode]:
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
            PlantCode(address='2950 INTERNATIONAL BLVD.', city='CLARKSVILLE', ...),
            PlantCode(address='1850 BARTON FERRY ROAD', city='WEST POINT', cou...),
            PlantCode(address='No. 52 Street 536, Bau Tran Hamlet, Nhuan Duc C...),
            PlantCode(address='NO. 23, HAILAR EAST ROAD', city='HUHHOT', count...),
            PlantCode(address='NO. 9 EAST BEISAN ROAD', city='SHENYANG', count...),
            PlantCode(address='HONGSHANZUI ECONOMIC DEV. ZONE', city='PINGQUAN...),
            PlantCode(address='QIANLIU VILLAGE XIADIAN TOWN', city='CHANGYI CI...),
            PlantCode(address='DOWANG TOWN', city='GUANGRAO COUNTY', country='...),
            PlantCode(address='NO.1 HUIXIN ROAD', city='GAOTANG', country='CHI...),
            PlantCode(address='NO.668 LAMEI ROAD,JIESHI TOWN,BANAN DISTRICT', ...),
        ]

        """

        plant_codes = self._client.get_equipment_plant_codes(
            year, equipment_type, report_type
        )
        return [PlantCode(**self._snake_case(pc)) for pc in plant_codes]

    def get_models_for_make(
        self, make: Union[int, str], model_year: int = None, vehicle_type: str = None
    ) -> List[Model]:
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

        Example
        -------
        get_models_for_make("TESLA", model_year=2020)

        [
            Model(
                model_id=1685,
                model_name='Model S',
                make_id=441,
                make_name='TESLA',
                vehicle_type_id=None
            ),
            Model(
                model_id=10199,
                model_name='Model X',
                make_id=441,
                make_name='TESLA',
                vehicle_type_id=None
            ),
            Model(
                model_id=17834,
                model_name='Model 3',
                make_id=441,
                make_name='TESLA',
                vehicle_type_id=None
            ),
            Model(
                model_id=27027,
                model_name='Model Y',
                make_id=441,
                make_name='TESLA',
                vehicle_type_id=None
                )
        ]

        VehicleTypeId and VehicleType are only returned
        when you specify vehicle_type.

        """

        models = self._client.get_models_for_make(make, model_year, vehicle_type)
        return [Model(**self._snake_case(m)) for m in models]

    def get_vehicle_variable_list(self) -> List[Variable]:
        """
        Return a list of vehicle variables tracked by vPIC

        Example
        -------
        get_vehicle_variable_list()

        [
            Variable(id=1, name='Other Battery Info', data_type='string', descr...),
            Variable(id=2, name='Battery Type', data_type='lookup', description...),
            Variable(id=3, name='Bed Type', data_type='lookup', description='<p...),
            Variable(id=4, name='Cab Type', data_type='lookup', description='<p...),
            Variable(id=5, name='Body Class', data_type='lookup', description='...),
            Variable(id=9, name='Engine Number of Cylinders', data_type='int', ...),
        ]

        """

        variables = self._client.get_vehicle_variable_list()
        return [Variable(**self._snake_case(v)) for v in variables]

    def get_vehicle_variable_values_list(self, variable_name: str) -> List[Value]:
        """
        Return the values for a vehicle variable

        Parameters
        ----------
        variable_name : str
            the name of the vehicle variable

        Example
        -------
        get_vehicle_variable_values_list("Vehicle Type")

        [
            VariableValue(element_name="Vehicle Type", id=1, name="Motorcycle"),
            VariableValue(element_name="Vehicle Type", id=2, name="Passenger Car"),
            VariableValue(element_name="Vehicle Type", id=3, name="Truck "),
            VariableValue(element_name="Vehicle Type", id=5, name="Bus"),
            VariableValue(element_name="Vehicle Type", id=6, name="Trailer"),
            VariableValue(element_name="Vehicle Type", id=7, name="Multipurpose P..."),
            VariableValue(element_name="Vehicle Type", id=9, name="Low Speed Vehi..."),
            VariableValue(element_name="Vehicle Type", id=10, name="Incomplete Ve..."),
            VariableValue(element_name="Vehicle Type", id=13, name="Off Road Vehicle")
        ]

        """

        values = self._client.get_vehicle_variable_values_list(variable_name)
        return [Value(**self._snake_case(v)) for v in values]

    def get_canadian_vehicle_specifications(
        self, year: int, make: str, model: str = None, units: str = "Metric"
    ) -> List[Model]:
        """
        Return the values for a vehicle variable

        Parameters
        ----------
        variable_name : str
            the name of the vehicle variable

        """

        raise NotImplementedError
