from . import expected_result


class TestManufacturers:
    def test_get_wmis_for_manufacturerid(self, vpic, responses, datadir):
        actual = vpic.get_wmis_for_manufacturer(988)
        expected = expected_result(datadir / "get-wmis-for-manufacturerid.json")
        assert actual == expected

    def test_get_wmis_for_manufacturer_name(self, vpic, responses, datadir):
        actual = vpic.get_wmis_for_manufacturer("Honda")
        expected = expected_result(datadir / "get-wmis-for-manufacturer-name.json")
        assert actual == expected

    def test_get_wmis_for_manufacturer_partialname(self, vpic, responses, datadir):
        actual = vpic.get_wmis_for_manufacturer("TECHNOLOG")
        expected = expected_result(
            datadir / "get-wmis-for-manufacturer-partialname.json"
        )
        assert actual == expected

    def test_get_wmis_for_manufacturer_vehicletype(self, vpic, responses, datadir):
        actual = vpic.get_wmis_for_manufacturer(vehicle_type='mpv')
        expected = expected_result(
            datadir / "get-wmis-for-manufacturer-vehicletype.json"
        )
        assert actual == expected

    def test_get_all_manufacturers(self, vpic, responses, datadir):
        assert vpic.get_all_manufacturers(
            "Completed Vehicle Manufacturer", 1
        ) == expected_result(datadir / "get-all-manufacturers.json")

    def test_get_manufacturer_details(self, vpic, responses, datadir):
        assert vpic.get_manufacturer_details(988) == expected_result(
            datadir / "get-manufacturer-details.json"
        )

    def test_get_manufacturer_details_name(self, vpic, responses, datadir):
        assert vpic.get_manufacturer_details("Honda") == expected_result(
            datadir / "get-manufacturer-details-name.json"
        )

    def test_get_manufacturer_details_by_partial_name(self, vpic, responses, datadir):
        assert vpic.get_manufacturer_details("METRO") == expected_result(
            datadir / "get-manufacturer-details-partialname.json"
        )

    def test_get_equipment_plant_codes(self, vpic, responses, datadir):
        assert vpic.get_equipment_plant_codes(2016, 1) == expected_result(
            datadir / "get-equipment-plant-codes.json"
        )

    def test_get_parts_565(self, vpic, responses, datadir):
        assert vpic.get_parts("565", "2015-01-01", "2015-05-05", 1) == expected_result(
            datadir / "get-parts-565.json"
        )

    def test_get_parts_566(self, vpic, responses, datadir):
        assert vpic.get_parts("566", "2016-02-01", "2016-02-15", 1) == expected_result(
            datadir / "get-parts-566.json"
        )
