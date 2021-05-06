from . import expected_result


class TestVariables:
    def test_get_vehicle_variable_list(self, vpic, responses, datadir):
        assert vpic.get_vehicle_variable_list() == expected_result(
            datadir / "get-vehicle-variable-list.json"
        )

    def test_get_vehicle_variable_values_list(self, vpic, responses, datadir):
        assert vpic.get_vehicle_variable_values_list("Vehicle Type") == expected_result(
            datadir / "get-vehicle-variable-values-list.json"
        )
