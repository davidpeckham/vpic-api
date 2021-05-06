from . import expected_result


class TestModels:
    def test_get_models_for_makeid(self, vpic, responses, datadir):
        assert vpic.get_models_for_make(441) == expected_result(
            datadir / "get-models-for-makeid.json"
        )

    def test_get_models_for_makeid_year(self, vpic, responses, datadir):
        assert vpic.get_models_for_make(441, model_year=2020) == expected_result(
            datadir / "get-models-for-makeid-year.json"
        )

    def test_get_models_for_makeid_vehicletype(self, vpic, responses, datadir):
        assert vpic.get_models_for_make(441, vehicle_type="Car") == expected_result(
            datadir / "get-models-for-makeid-vehicletype.json"
        )

    def test_get_models_for_makeid_year_vehicletype(self, vpic, responses, datadir):
        assert vpic.get_models_for_make(
            441, model_year=2021, vehicle_type="Car"
        ) == expected_result(datadir / "get-models-for-makeid-year-vehicletype.json")

    def test_get_models_for_make(self, vpic, responses, datadir):
        assert vpic.get_models_for_make("TESLA") == expected_result(
            datadir / "get-models-for-make.json"
        )

    def test_get_models_for_make_year(self, vpic, responses, datadir):
        assert vpic.get_models_for_make("TESLA", model_year=2020) == expected_result(
            datadir / "get-models-for-make-year.json"
        )

    def test_get_models_for_make_vehicletype(self, vpic, responses, datadir):
        assert vpic.get_models_for_make("TESLA", vehicle_type="Car") == expected_result(
            datadir / "get-models-for-make-vehicletype.json"
        )

    def test_get_models_for_make_year_vehicletype(self, vpic, responses, datadir):
        assert vpic.get_models_for_make(
            "TESLA", model_year=2020, vehicle_type="Car"
        ) == expected_result(datadir / "get-models-for-make-year-vehicletype.json")

    def test_get_canadian_vehicle_specifications(self, vpic, responses, datadir):
        assert vpic.get_canadian_vehicle_specifications(
            2011, make="Acura", model="", units=""
        ) == expected_result(datadir / "get-canadian-vehicle-specifications.json")
