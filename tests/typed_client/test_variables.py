from typing import List
from vpic.models import Variable, Value
from vpic.typed_client import TypedClient


class TestVariables:
    def test_get_vehicle_variable_list(self, typed_client: TypedClient, responses):
        variables: List[Variable] = typed_client.get_vehicle_variable_list()
        assert len(variables) == 138
        assert hasattr(variables[0], "data_type")
        assert hasattr(variables[0], "description")
        assert hasattr(variables[0], "group_name")
        assert hasattr(variables[0], "id")
        assert hasattr(variables[0], "name")
        assert variables[0].id == 1

    def test_get_vehicle_variable_values_list(
        self, typed_client: TypedClient, responses
    ):
        values: List[Value] = typed_client.get_vehicle_variable_values_list(
            "Vehicle Type"
        )
        assert len(values) == 9
        assert values[0].id == 1
        assert values[0].name == "Motorcycle"
