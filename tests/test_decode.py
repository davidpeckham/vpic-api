from . import expected_result


class TestDecode:
    def test_decode_vin(self, vpic, responses, datadir):
        assert vpic.decode_vin("1FTMW1T88MFA00001") == expected_result(
            datadir / "decode-vin.json"
        )

    def test_decode_vin_with_modelyear(self, vpic, responses, datadir):
        assert vpic.decode_vin("1FTMW1T88MFA00001", 2021) == expected_result(
            datadir / "decode-vin-with-modelyear.json"
        )

    def test_decode_vin_extended(self, vpic, responses, datadir):
        assert vpic.decode_vin(
            "1FTMW1T88MFA00001", 2021, extend=True
        ) == expected_result(datadir / "decode-vin-extended.json")

    def test_decode_vin_unflattened(self, vpic, responses, datadir):
        assert vpic.decode_vin(
            "1FTMW1T88MFA00001", 2021, flatten=False
        ) == expected_result(datadir / "decode-vin-unflattened.json")

    def test_decode_partial_vin(self, vpic, responses, datadir):
        assert vpic.decode_vin("5UXWX7C5*BA", 2011) == expected_result(
            datadir / "decode-partial-vin.json"
        )

    def test_decode_partial_vin_unflattened(self, vpic, responses, datadir):
        assert vpic.decode_vin(
            "1FA6P8C0!M!100001", 2021, flatten=False
        ) == expected_result(datadir / "decode-partial-vin-unflattened.json")

    def test_decode_vin_batch(self, vpic, responses, datadir):
        assert vpic.decode_vin_batch(
            ["5UXWX7C5*BA,2011", "5YJSA3DS*EF"]
        ) == expected_result(datadir / "decode-vin-batch.json")

    def test_decode_wmi(self, vpic, datadir, responses):
        actual = vpic.decode_wmi("1FT")
        expected = expected_result(datadir / "decode-wmi.json")
        assert actual == expected
