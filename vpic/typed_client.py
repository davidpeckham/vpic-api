import logging
import re
from typing import Any, Dict, List, Union

from .client import Client
from .model import (
    Make,
    PlantCode,
    Vehicle,
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
        self._snake_re = re.compile(r"(?<!^)([A-Z])(?=[a-z])")

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

        return {
            self._snake_re.sub(r"_\1", key).lower(): value
            for key, value in object.items()
        }

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
