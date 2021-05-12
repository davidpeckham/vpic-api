from typing import List
from vpic.model import PlantCode
from vpic.typed_client import TypedClient


class TestManufacturers:
    def test_get_equipment_plant_codes(self, typed_client: TypedClient, responses):
        plant_codes: List[PlantCode] = typed_client.get_equipment_plant_codes(2016, 1)
        assert len(plant_codes) == 1089
        assert hasattr(plant_codes[0], 'dot_code')
