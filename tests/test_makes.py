from . import expected_result


class TestMakes:
    def test_get_all_makes(self, vpic, responses, datadir):
        assert vpic.get_all_makes() == expected_result(
            datadir / "get-all-makes.json"
        )

    def test_get_makes_for_manufacturer(self, vpic, responses, datadir):
        assert vpic.get_makes_for_manufacturer(988) == expected_result(
            datadir / "get-makes-for-manufacturer.json"
        )

    def test_get_makes_for_manufacturer_by_name(self, vpic, responses, datadir):
        assert vpic.get_makes_for_manufacturer("Honda") == expected_result(
            datadir / "get-makes-for-manufacturer-name.json"
        )

    def test_get_makes_for_manufacturer_by_partial_name(
        self, vpic, responses, datadir
    ):
        assert vpic.get_makes_for_manufacturer("METRO") == expected_result(
            datadir / "get-makes-for-manufacturer-partial-name.json"
        )

    def test_get_makes_for_manufacturerid_and_modelyear(
        self, vpic, responses, datadir
    ):
        assert vpic.get_makes_for_manufacturer(988, 2021) == expected_result(
            datadir / "get-makes-for-manufacturerid-and-modelyear.json"
        )

    def test_get_makes_for_vehicle_type(self, vpic, responses, datadir):
        assert vpic.get_makes_for_vehicle_type("Car") == expected_result(
            datadir / "get-makes-for-vehicletype.json"
        )

    def test_get_vehicle_types_for_make_id(self, vpic, responses, datadir):
        assert vpic.get_vehicle_types_for_make(474) == expected_result(
            datadir / "get-vehicletypes-for-makeid.json"
        )

    def test_get_vehicle_types_for_make_name(self, vpic, responses, datadir):
        assert vpic.get_vehicle_types_for_make("kia") == expected_result(
            datadir / "get-vehicletypes-for-makename.json"
        )
