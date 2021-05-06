from . import expected_result


class TestParts:
    def test_get_parts_565(self, vpic, responses, datadir):
        assert vpic.get_parts("565", "2015-01-01", "2015-05-05", 1) == expected_result(
            datadir / "get-parts-565.json"
        )

    def test_get_parts_566(self, vpic, responses, datadir):
        assert vpic.get_parts("566", "2016-02-01", "2016-02-15", 1) == expected_result(
            datadir / "get-parts-566.json"
        )
