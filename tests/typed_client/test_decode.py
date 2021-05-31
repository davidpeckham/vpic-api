from vpic.models import Vehicle, WorldManufacturerIndex
from vpic.typed_client import TypedClient


class TestDecode:
    def test_decode_vin(self, typed_client: TypedClient, responses):
        vehicle: Vehicle = typed_client.decode_vin("1FTMW1T88MFA00001")
        assert vehicle.make == "FORD"
        assert vehicle.model == "F-150"
        assert vehicle.trim == "SuperCrew-SSV"
        assert vehicle.vehicle_type == "TRUCK "

    def test_decode_vin_with_model_year(self, typed_client: TypedClient, responses):
        vehicle = typed_client.decode_vin("1FTMW1T88MFA00001", 2021)
        assert vehicle.make == "FORD"
        assert vehicle.model == "F-150"
        assert vehicle.trim == "SuperCrew-SSV"
        assert vehicle.vehicle_type == "TRUCK "

    def test_decode_vin_extended(self, typed_client: TypedClient, responses):
        vehicle = typed_client.decode_vin("1FTMW1T88MFA00001", 2021, extend=True)
        assert vehicle.make == "FORD"
        assert vehicle.model == "F-150"
        assert vehicle.trim == "SuperCrew-SSV"
        assert vehicle.vehicle_type == "TRUCK "

    def test_decode_partial_vin(self, typed_client: TypedClient, responses):
        vehicle = typed_client.decode_vin("5UXWX7C5*BA", 2011)
        assert vehicle.make == "BMW"
        assert vehicle.model == "X3"
        assert vehicle.trim == "xDrive35i"
        assert vehicle.vehicle_type == "MULTIPURPOSE PASSENGER VEHICLE (MPV)"

    def test_decode_vin_batch(self, typed_client: TypedClient, responses):
        vehicles = typed_client.decode_vin_batch(["5UXWX7C5*BA,2011", "5YJSA3DS*EF"])

        bmw = vehicles[0]
        assert bmw.model_year == "2011"
        assert bmw.make == "BMW"
        assert bmw.model == "X3"
        assert bmw.trim == "xDrive35i"
        assert bmw.vehicle_type == "MULTIPURPOSE PASSENGER VEHICLE (MPV)"

        tesla = vehicles[1]
        assert tesla.model_year == "2014"
        assert tesla.make == "TESLA"
        assert tesla.model == "Model S"
        assert tesla.trim == "w/DC Fast Charge"
        assert tesla.vehicle_type == "PASSENGER CAR"

    def test_decode_wmi(self, typed_client: TypedClient, responses):
        wmi: WorldManufacturerIndex = typed_client.decode_wmi("1FT")
        assert wmi.common_name == "Ford"
        assert wmi.created_on == "2015-03-23"
        assert wmi.date_available_to_public == "2015-01-01"
        assert wmi.make == "FORD"
        assert wmi.manufacturer == "FORD MOTOR COMPANY, USA"
        assert wmi.parent_company_name == ""
        assert wmi.updated_on is None
        assert wmi.url == "http://www.ford.com/"
        assert wmi.vehicle_type == "Truck "
