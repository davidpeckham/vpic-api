from typing import List
from vpic.model import PlantCode, WorldManufacturerIndex
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

    def test_get_equipment_plant_codes(self, typed_client: TypedClient, responses):
        plant_codes: List[PlantCode] = typed_client.get_equipment_plant_codes(2016, 1)
        assert len(plant_codes) == 1089
        assert hasattr(plant_codes[0], "dot_code")
