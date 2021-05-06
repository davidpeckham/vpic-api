import json

from vpic.utils import standardize_variable_names


def expected_result(response_path):
    with response_path.open() as fp:
        content = json.load(fp)
    # TODO Update JSON response files to reflect the actual expected
    # result and then remove this call to standardize_variable_names
    return standardize_variable_names(content["expected_result"])
