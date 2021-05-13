from typing import List
from vpic.model import Make
from vpic.typed_client import TypedClient


class TestMakes:
    def test_get_all_makes(self, typed_client: TypedClient, responses):
        makes: List[Make] = typed_client.get_all_makes()
        assert len(makes) == 9583
        assert makes[0].make_name == "ASTON MARTIN"
        assert makes[0].make_id == 440
        assert makes[1].make_name == "TESLA"
        assert makes[1].make_id == 441

    def test_get_makes_for_manufacturer(self, typed_client: TypedClient, responses):
        makes: List[Make] = typed_client.get_makes_for_manufacturer(988)
        assert len(makes) == 2

    def test_get_makes_for_manufacturer_by_name(
        self, typed_client: TypedClient, responses
    ):
        makes: List[Make] = typed_client.get_makes_for_manufacturer("Honda")
        assert len(makes) == 15

    def test_get_makes_for_manufacturer_by_partial_name(
        self, typed_client: TypedClient, responses
    ):
        makes: List[Make] = typed_client.get_makes_for_manufacturer("METRO")
        assert len(makes) == 4

    def test_get_makes_for_manufacturerid_and_modelyear(
        self, typed_client: TypedClient, responses
    ):
        makes: List[Make] = typed_client.get_makes_for_manufacturer(988, 2021)
        assert len(makes) == 2
