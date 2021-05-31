import logging
from typing import List, Optional, Union

import desert
import marshmallow

from .client import Client
from .models import (
    Document,
    Make,
    Manufacturer,
    ManufacturerDetail,
    Model,
    PlantCode,
    Value,
    Variable,
    Vehicle,
    VehicleType,
    WorldManufacturerIndex,
)
from .transforms import snake_case

log = logging.getLogger(__name__)


class TypedClient:
    """A client library for the U.S. NHTSA vPIC API

    ``TypedClient`` returns model objects instead of JSON responses. If you
    need the original vPIC JSON responses, use ``vpic.Client``.

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

    NHTSA occasionally adds, removes, or renames variables in vPIC API
    responses. This class uses Marshmallow to deserialize the response.
    When a variable is missing or renamed, methods in this class raise
    ``marshmallow.exceptions.ValidationError``. If you instantiate this class
    with unknown='RAISE', methods will also raise
    ``marshmallow.exceptions.ValidationError`` when the vPIC response
    includes a new variable that isn't defined in the model (models.py).

    See https://vpic.nhtsa.dot.gov/api for more on the API.

    Attributes:
        host: Hostname, including http(s)://, of the vPIC instance to query.
        unknowns: exclude new API response variables ('EXCLUDE'), or raise an
            exception ('RAISE') instead

    """

    def __init__(
        self,
        host: Optional[str] = "https://vpic.nhtsa.dot.gov/api/vehicles/",
        unknown: Optional[str] = "EXCLUDE",
    ):
        if unknown == "EXCLUDE":
            self._meta = {"unknown": marshmallow.EXCLUDE}
        elif unknown == "RAISE":
            self._meta = {"unknown": marshmallow.RAISE}
        else:
            raise ValueError("unknown must be 'EXCLUDE' or 'RAISE'")
        self._client = Client(host, standardize_variables=True)

    def decode_vin(
        self, vin: str, model_year: Optional[int] = None, extend: Optional[bool] = False
    ) -> Vehicle:
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

        Returns:
            A ``Vehicle`` with the information decoded from ``vin``.

        Raises:
            ValueError: if ``vin`` is missing or isn't 6 to 17 characters long.
            ValueError: if ``model_year`` is earlier than 1981.

        Example:
            >>> decode_vin('1FTMW1T88MFA00001')
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
                error_text="0 - VIN decoded clean. Check Digit (9th position) is co...",
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
        schema = desert.schema(Vehicle, meta=self._meta)
        return schema.load(snake_case(self._client.decode_vin(vin, model_year, extend)))

    def decode_vin_batch(self, vins: List[str]) -> List[Vehicle]:
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

        Returns:
            A list of ``Vehicle``s with the information decoded from ``vins``.

        Raises:
            ValueError: if ``vin`` is missing or isn't 6 to 17 characters long.
            ValueError: if ``model_year`` is earlier than 1981.

        Example:
            >>> decode_vin_batch(["5UXWX7C5*BA,2011", "5YJSA3DS*EF"])
            [Vehicle(...), Vehicle(...)]

        """
        vehicles = self._client.decode_vin_batch(vins)
        schema = desert.schema(Vehicle, meta=self._meta)
        return [schema.load(snake_case(v)) for v in vehicles]

    def decode_wmi(self, wmi: str) -> WorldManufacturerIndex:
        """Decode a WMI to get manufacturer information

        Provides information on the World Manufacturer Identifier for a
        specific WMI code.

        Args:
            wmi: A 3-character or 6-character World Manufacturer Index code.
                 Large volume manufacturers usually have a  3 character WMI
                 representing positions 1 to 3 ("JTD") of a VIN. Smaller
                 manufacturers have a 6 character WMI representing positions
                 1 to 3 and 12 to 14 of a VIN.

        Returns:
            A ``WorldManufacturerIndex`` with information about the manufacturer.

        Raises:
            ValueError: if ``wmi`` is missing or isn't 3 or 6 characters long.

        Example:
            >>> decode_wmi('1FT')
            WorldManufacturerIndex(
                common_name="Ford",
                created_on="2015-03-23",
                date_available_to_public="2015-01-01",
                make="FORD",
                manufacturer="FORD MOTOR COMPANY, USA",
                parent_company_name="",
                updated_on=None,
                url="http://www.ford.com/",
                vehicle_type="Truck ",
            )

        """
        schema = desert.schema(WorldManufacturerIndex, meta=self._meta)
        return schema.load(snake_case(self._client.decode_wmi(wmi)))

    def get_wmis_for_manufacturer(
        self,
        manufacturer: Union[str, int],
        vehicle_type: Optional[Union[str, int]] = None,
    ) -> List[WorldManufacturerIndex]:
        """Returns the WMIs for one or all manufacturers

        Args:
            manufacturer: Pass the Manufacturer Id (int) or the complete
                manufacturer name (str) to return WMIs for a single manufacturer.
                Pass a partial name to return WMIs for all manufacturers with
                names that include the partial name.
            vehicle_type: Pass the vehicle_type Id (int) or complete vehicle_type
                name to return WMIs for that vehicle_type. Pass a partial name to
                return WMIs for vehicle_types matching that name.

        Returns:
            A list of ``WorldManufacturerIndex`` with information about the
            manufacturers.

        Raises:
            ValueError: if ``manufacturer`` is missing

        Examples:
            >>> get_wmis_for_manufacturer('Honda')
            [
                WorldManufacturerIndex(
                    created_on='2015-03-26',
                    date_available_to_public='2015-01-01',
                    manufacturer='HONDA MOTOR CO., LTD',
                    updated_on='2015-06-04',
                    vehicle_type='Passenger Car',
                    wmi='JHM', common_name='',
                    country=None,
                    make='',
                    manufacturer_id=987,
                    parent_company_name='',
                    url=''
                ),
                ...
            ]

        """
        wmis = self._client.get_wmis_for_manufacturer(manufacturer, vehicle_type)
        schema = desert.schema(WorldManufacturerIndex, meta=self._meta)
        return [schema.load(snake_case(wmi)) for wmi in wmis]

    def get_all_makes(self) -> List[Make]:
        """Returns all of the makes registered with vPIC.

        Returns:
            A list of all of the ``Make``s registered with vPIC.

        Examples:
            >>> get_all_makes()
            [
                Make(make_id=440, make='ASTON MARTIN'),
                Make(make_id=441, make='TESLA'),
                Make(make_id=442, make='JAGUAR'),
                Make(make_id=443, make='MASERATI'),
                Make(make_id=444, make='LAND ROVER'),
                Make(make_id=445, make='ROLLS ROYCE'),
                Make(make_id=446, make='BUELL (EBR)'),
                Make(make_id=447, make='JIALING'),
                Make(make_id=448, make='TOYOTA'),
                Make(make_id=449, make='MERCEDES-BENZ'),
                ...
            ]

        """
        makes = self._client.get_all_makes()
        schema = desert.schema(Make, meta=self._meta)
        return [schema.load(snake_case(make)) for make in makes]

    def get_parts(
        self, cfr_part: str, from_date: str, to_date: str, page: int = 1
    ) -> List[Document]:
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
            to_date: the end of the date range to search
            page: results are paginated; this is page number to return

        Returns:
            A list of ``Document``s registered with vPIC.

        Raises:
            ValueError: if ``cvr_part`` is missing

        Examples:
            >>> get_parts('565', '2015-01-01', '2015-05-05', 1)
            [
                Document(
                    cover_letter_url='',
                    letter_date='1/1/2015',
                    manufacturer_id=959,
                    manufacturer='MASERATI NORTH AMERICA, INC.',
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
            # snake_case doesn't handle lowerUPPER
            doc["CoverLetterUrl"] = doc["CoverLetterURL"]
            del doc["CoverLetterURL"]
        schema = desert.schema(Document, meta=self._meta)
        return [schema.load(snake_case(doc)) for doc in documents]

    def get_all_manufacturers(
        self, manufacturer_type: Optional[str] = None, page: int = 1
    ) -> List[Manufacturer]:
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

        Returns:
            A list of the ``Manufacturers``s registered with vPIC.

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
        raise NotImplementedError

    def get_manufacturer_details(
        self, manufacturer: Union[str, int]
    ) -> List[ManufacturerDetail]:
        """Returns details for one or more manufacturers.

        Args:
            manufacturer: Pass the Manufacturer Id (int) or the complete
                manufacturer name (str) to return detail for a single
                manufacturer. Pass a partial name to return manufacturers
                with names that include the partial name.

        Returns:
            A list of ``ManufacturerDetail``s for the manufacturer(s)

        Examples:
            >>> get_manufacturer_details(988)
            [
                ManufacturerDetail(
                    manufacturer_id=988,
                    manufacturer="HONDA DEVELOPMENT & MANUFACTURING OF AMER...",
                    manufacturer_common_name="Honda",
                    address="1919 Torrance Blvd.",
                    address2=None,
                    city="Torrance",
                    contact_email="...@ahm.honda.com",
                    contact_fax=None,
                    contact_phone="...",
                    country="UNITED STATES (USA)",
                    dbas="Marysville Auto Plant and East Liberty Auto Plant; ...",
                    equipment_items=[],
                    last_updated="/Date(1618422117803-0400)/",
                    manufacturer_types=[
                        ManufacturerType(
                            name="Completed Vehicle Manufacturer")
                        ],
                    other_manufacturer_details=None,
                    postal_code="90501",
                    primary_product=None,
                    principal_first_name="...",
                    principal_last_name=None,
                    principal_position="President & CEO",
                    state_province="CALIFORNIA",
                    submitted_name="...",
                    submitted_on="/Date(1618286400000-0400)/",
                    submitted_position="Sr. Specialist, II",
                    vehicle_types=[
                        VehicleType(
                            vehicle_type="Passenger Car",
                            vehicle_type_id=None,
                            make_id=None,
                            make=None,
                            gvwr_from="Class 1A: 3,000 lb or less (1,360 kg or less)",
                            gvwr_to="Class 1D: 5,001 - 6,000 lb (2,268 - 2,722 kg)",
                            is_primary=True
                        ),
                        VehicleType(
                            vehicle_type="Truck ",
                            vehicle_type_id=None,
                            make_id=None,
                            make=None,
                            gvwr_from="Class 2E: 6,001 - 7,000 lb (2,722 - 3,175 kg)",
                            gvwr_to="Class 2E: 6,001 - 7,000 lb (2,722 - 3,175 kg)",
                            is_primary=False
                        ),
                        VehicleType(
                            vehicle_type="Multipurpose Passenger Vehicle (MPV)",
                            vehicle_type_id=None,
                            make_id=None,
                            make=None,
                            gvwr_from="Class 1B: 3,001 - 4,000 lb (1,360 - 1,814 kg)",
                            gvwr_to="Class 2E: 6,001 - 7,000 lb (2,722 - 3,175 kg)",
                            is_primary=False
                        )
                    ]
                )
            ]

        """
        results = self._client.get_manufacturer_details(manufacturer)
        for r in results:
            r["dbas"] = r["DBAs"]
            del r["DBAs"]

            # r["ManufacturerTypes"] = [
            #     ManufacturerType(name=mt["Name"]) for mt in r["ManufacturerTypes"]
            # ]
            # r["VehicleTypes"] = [
            #     VehicleType(
            #         vehicle_type=vt["Name"],
            #         is_primary=vt["IsPrimary"],
            #         gvwr_from=vt["GVWRFrom"],
            #         gvwr_to=vt["GVWRTo"],
            #     )
            #     for vt in r["VehicleTypes"]
            # ]

            # r["ManufacturerTypes"] = [snake_case(mt) for mt in r["ManufacturerTypes"]]
            # r["VehicleTypes"] = [snake_case(vt) for vt in r["VehicleTypes"]]

        schema = desert.schema(ManufacturerDetail, meta=self._meta)
        snake_cased = [snake_case(r) for r in results]
        return [schema.load(sc) for sc in snake_cased]

    def get_makes_for_manufacturer(
        self, manufacturer: Union[str, int], model_year: Optional[int] = None
    ) -> List[Make]:
        """Returns makes produced by a manufacturer or manufacturers.

        Args:
            manufacturer: Pass the Manufacturer Id (int) or the complete
                manufacturer name (str) to return detail for a single manufacturer.
                Pass a partial name to return manufacturers with names that include
                the partial name.
            model_year: Pass a model year to return only those makes made by
                the manufacturer for that model year.

        Returns:
            A list of ``Makes``s produced by the manufacturer(s)

        Raises:
            ValueError: if ``manufacturer`` is missing

        Examples:
            >>> get_makes_for_manufacturer(988)
            [
                Make(
                    make_id:474
                    make:'HONDA'
                    manufacturer_id:None
                    manufacturer:'HONDA DEVELOPMENT & MANUFACTURING OF AMERICA...'
                ),
                Make(
                    make_id=475,
                    make='ACURA',
                    manufacturer_id=None,
                    manufacturer='HONDA DEVELOPMENT & MANUFACTURING OF AMERICA...'
                )
                ...
            ]

        """
        makes = self._client.get_makes_for_manufacturer(manufacturer, model_year)
        schema = desert.schema(Make, meta=self._meta)
        return [schema.load(snake_case(m)) for m in makes]

    def get_makes_for_vehicle_type(self, vehicle_type: str) -> List[Make]:
        """Returns makes that produce a vehicle_type

        Args:
            vehicle_type: A vPIC vehicle_type. For example, "Passenger Car",
                "Truck", or "Multipurpose Passenger Vehicle (MPV)". If you pass
                a partial vehicle_type, for example "Passenger", results will
                include makes for all matching vehicle types. Matching is not
                case sensitive.

        Returns:
            A list of ``Makes``s that produce the ``vehicle_type``

        Raises:
            ValueError: if ``vehicle_type`` is missing

        Examples:
            >>> get_makes_for_vehicle_type('Car')
            [
                Make(
                    make_id=440,
                    make='ASTON MARTIN',
                    manufacturer_id=None,
                    manufacturer=None,
                    vehicle_type_id=2,
                    vehicle_type='Passenger Car'
                )
                ...
            ]

        """
        makes = self._client.get_makes_for_vehicle_type(vehicle_type)
        schema = desert.schema(Make, meta=self._meta)
        return [schema.load(snake_case(m)) for m in makes]

    def get_vehicle_types_for_make(self, make: Union[str, int]) -> List[VehicleType]:
        """Returns vehicle types produced by a make or make

        Args:
            make: Pass the MakeId (int) or the complete make name (str) to return
                vehicle types for a single manufacturer. Pass a partial make name
                to return vehicle types for all makes that match the partial name.
                When you pass a make name, results will include the MakeId and
                MakeName because you may get vehicle_types for more than one make.

        Returns:
            A list of ``VehicleType``s produced by the ``make``(s)

        Raises:
            ValueError: if ``make`` is missing

        Examples:
            >>> get_vehicle_types_for_make(474)
            [
                VehicleType(
                    vehicle_type_id=1,
                    vehicle_type='Motorcycle',
                    make_id=None,
                    make=None
                ),
                VehicleType(
                    vehicle_type_id=2,
                    vehicle_type='Passenger Car',
                    make_id=None,
                    make=None
                ),
                VehicleType(
                    vehicle_type_id=3,
                    vehicle_type='Truck ',
                    make_id=None,
                    make=None
                ),
                VehicleType(
                    vehicle_type_id=7,
                    vehicle_type='Multipurpose Passenger Vehicle (MPV)',
                    make_id=None,
                    make=None
                ),
                VehicleType(
                    vehicle_type_id=9,
                    vehicle_type='Low Speed Vehicle (LSV)',
                    make_id=None,
                    make=None
                )
            ]

        """
        schema = desert.schema(VehicleType, meta=self._meta)
        results = self._client.get_vehicle_types_for_make(make)
        snake_cased = [snake_case(r) for r in results]
        return [schema.load(sc) for sc in snake_cased]

    def get_equipment_plant_codes(
        self, year: int, equipment_type: int, report_type: str = "All"
    ) -> List[PlantCode]:
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

        Returns:
            A list of ``PlantCode``s that manufacture the equipment_type

        Raises:
            ValueError: if ``year`` is earlier than 2016

        Example:
            >>> get_equipment_plant_codes(2016, 1)
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
        schema = desert.schema(PlantCode, meta=self._meta)
        return [schema.load(snake_case(pc)) for pc in plant_codes]

    def get_models_for_make(
        self,
        make: Union[int, str],
        model_year: Optional[int] = None,
        vehicle_type: Optional[str] = None,
    ) -> List[Model]:
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

        Returns:
            A list of ``Model``s

        Raises:
            ValueError: if ``year`` is earlier than 2016

        Examples:
            >>> get_models_for_make("TESLA", model_year=2020)
            [
                Model(
                    model_id=1685,
                    model='Model S',
                    make_id=441,
                    make='TESLA',
                    vehicle_type_id=None
                ),
                Model(
                    model_id=10199,
                    model='Model X',
                    make_id=441,
                    make='TESLA',
                    vehicle_type_id=None
                ),
                Model(
                    model_id=17834,
                    model='Model 3',
                    make_id=441,
                    make='TESLA',
                    vehicle_type_id=None
                ),
                Model(
                    model_id=27027,
                    model='Model Y',
                    make_id=441,
                    make='TESLA',
                    vehicle_type_id=None
                    )
            ]

        VehicleTypeId and VehicleType are only returned
        when you specify vehicle_type.

        """
        models = self._client.get_models_for_make(make, model_year, vehicle_type)
        schema = desert.schema(Model, meta=self._meta)
        return [schema.load(snake_case(m)) for m in models]

    def get_vehicle_variable_list(self) -> List[Variable]:
        """Return a list of vehicle variables tracked by vPIC

        Returns:
            A list of ``Variable``s

        Examples:
            >>> get_vehicle_variable_list()
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
        schema = desert.schema(Variable, meta=self._meta)
        return [schema.load(snake_case(v)) for v in variables]

    def get_vehicle_variable_values_list(self, variable_name: str) -> List[Value]:
        """Return the values for a vehicle variable

        Args:
            variable_name: the name of the vehicle variable

        Returns:
            A list of ``Values``s

        Raises:
            ValueError: if ``variable_name`` is missing

        Examples:
            >>> get_vehicle_variable_values_list("Vehicle Type")
            [
                Value(element_name="Vehicle Type", id=1, name="Motorcycle"),
                Value(element_name="Vehicle Type", id=2, name="Passenger Car"),
                Value(element_name="Vehicle Type", id=3, name="Truck "),
                Value(element_name="Vehicle Type", id=5, name="Bus"),
                Value(element_name="Vehicle Type", id=6, name="Trailer"),
                Value(element_name="Vehicle Type", id=7, name="Multipurpose P..."),
                Value(element_name="Vehicle Type", id=9, name="Low Speed Vehi..."),
                Value(element_name="Vehicle Type", id=10, name="Incomplete Ve..."),
                Value(element_name="Vehicle Type", id=13, name="Off Road Vehicle")
            ]

        """
        values = self._client.get_vehicle_variable_values_list(variable_name)
        schema = desert.schema(Value, meta=self._meta)
        return [schema.load(snake_case(v)) for v in values]
