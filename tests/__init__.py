import json


def expected_result(response_path):
    with response_path.open(encoding="utf-8") as fp:
        content = json.load(fp)
    return content["expected_result"]
