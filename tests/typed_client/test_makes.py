from typing import List
from vpic.model import Make
from vpic.typed_client import TypedClient


class TestMakes:
    def test_get_all_makes(self, typed_client: TypedClient, responses):
        makes: List[Make] = typed_client.get_all_makes()
        assert len(makes) == 9583
        assert makes[0].make_name == 'ASTON MARTIN'
        assert makes[0].make_id == 440
        assert makes[1].make_name == 'TESLA'
        assert makes[1].make_id == 441
