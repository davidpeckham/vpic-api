from typing import List

import pytest
from vpic.models import Model
from vpic.typed_client import TypedClient


class TestModels:
    def test_get_models_for_makeid(self, typed_client: TypedClient, responses):
        models: List[Model] = typed_client.get_models_for_make(441)
        assert len(models) == 5

    def test_get_models_for_makeid_year(self, typed_client: TypedClient, responses):
        models: List[Model] = typed_client.get_models_for_make(441, model_year=2020)
        assert len(models) == 4

    def test_get_models_for_makeid_vehicletype(
        self, typed_client: TypedClient, responses
    ):
        models: List[Model] = typed_client.get_models_for_make(441, vehicle_type="Car")
        assert len(models) == 5

    def test_get_models_for_makeid_year_vehicletype(
        self, typed_client: TypedClient, responses
    ):
        models: List[Model] = typed_client.get_models_for_make(
            441, model_year=2021, vehicle_type="Car"
        )
        assert len(models) == 4

    def test_get_models_for_make(self, typed_client: TypedClient, responses):
        models: List[Model] = typed_client.get_models_for_make("TESLA")
        assert len(models) == 5

    def test_get_models_for_make_year(self, typed_client: TypedClient, responses):
        models: List[Model] = typed_client.get_models_for_make("TESLA", model_year=2020)
        assert len(models) == 4

    def test_get_models_for_make_vehicletype(
        self, typed_client: TypedClient, responses
    ):
        models: List[Model] = typed_client.get_models_for_make(
            "TESLA", vehicle_type="Car"
        )
        assert len(models) == 5

    def test_get_models_for_make_year_vehicletype(
        self, typed_client: TypedClient, responses
    ):
        models: List[Model] = typed_client.get_models_for_make(
            "TESLA", model_year=2020, vehicle_type="Car"
        )
        assert len(models) == 4

    @pytest.mark.xfail()
    def test_get_canadian_vehicle_specifications(
        self, typed_client: TypedClient, responses
    ):
        models: List[Model] = typed_client.get_canadian_vehicle_specifications(
            2011, make="Acura", model="", units=""
        )
        assert len(models) == 10
