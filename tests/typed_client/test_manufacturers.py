from typing import List
from vpic.models import Document, ManufacturerDetail, PlantCode, WorldManufacturerIndex
from vpic.typed_client import TypedClient


class TestManufacturers:
    def test_get_wmis_for_manufacturerid(self, typed_client: TypedClient, responses):
        wmis: List[WorldManufacturerIndex] = typed_client.get_wmis_for_manufacturer(988)
        assert len(wmis) == 20

    def test_get_wmis_for_manufacturer_name(self, typed_client: TypedClient, responses):
        wmis: List[WorldManufacturerIndex] = typed_client.get_wmis_for_manufacturer(
            "Honda"
        )
        assert len(wmis) == 44

    def test_get_wmis_for_manufacturer_partialname(
        self, typed_client: TypedClient, responses
    ):
        wmis: List[WorldManufacturerIndex] = typed_client.get_wmis_for_manufacturer(
            "TECHNOLOG"
        )
        assert len(wmis) == 101

    def test_get_manufacturer_details(self, typed_client: TypedClient, responses):
        details: List[ManufacturerDetail] = typed_client.get_manufacturer_details(988)
        assert len(details) == 1
        honda = details[0]
        assert honda.manufacturer_id == 988
        assert (
            honda.manufacturer
            == "HONDA DEVELOPMENT & MANUFACTURING OF AMERICA, LLC"
        )
        assert honda.manufacturer_common_name == "Honda"
        assert honda.manufacturer_types is not None
        if honda.manufacturer_types is not None:
            assert honda.manufacturer_types[0].name == "Completed Vehicle Manufacturer"

    def test_get_manufacturer_details_name(self, typed_client: TypedClient, responses):
        details: List[ManufacturerDetail] = typed_client.get_manufacturer_details(
            "Honda"
        )

        assert details[0].manufacturer_id == 987
        assert details[0].manufacturer == "HONDA MOTOR CO., LTD"
        assert details[0].manufacturer_common_name == "Honda"

    def test_get_manufacturer_details_by_partial_name(
        self, typed_client: TypedClient, responses
    ):
        details: List[ManufacturerDetail] = typed_client.get_manufacturer_details(
            "METRO"
        )
        assert details[0].manufacturer_id == 3382
        assert details[0].manufacturer == "NICHIBEI METROPAGES, INC."
        assert details[0].manufacturer_common_name is None

    def test_get_equipment_plant_codes(self, typed_client: TypedClient, responses):
        plant_codes: List[PlantCode] = typed_client.get_equipment_plant_codes(2016, 1)
        assert len(plant_codes) == 1091
        assert hasattr(plant_codes[0], "dot_code")

    def test_get_parts_565(self, typed_client: TypedClient, responses):
        documents: List[Document] = typed_client.get_parts(
            "565", "2015-01-01", "2015-05-05", 1
        )
        assert len(documents) == 175

    def test_get_parts_566(self, typed_client: TypedClient, responses):
        documents: List[Document] = typed_client.get_parts(
            "566", "2016-02-01", "2016-02-15", 1
        )
        assert len(documents) == 15
