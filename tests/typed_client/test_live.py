from typing import List

from vpic.models import Make, VehicleType, Value
from vpic.typed_client import TypedClient


class TestLive:
    def test_get_makes_for_vehicle_type(self, typed_client: TypedClient):
        makes: List[Make] = typed_client.get_makes_for_vehicle_type("Truck ")
        pass

    def test_get_vehicle_variable_values_list(self, typed_client: TypedClient):
        values: List[Value] = typed_client.get_vehicle_variable_values_list(
            "Vehicle Type"
        )
        pass
