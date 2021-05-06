STANDARD_VARIABLE_NAMES = {
    "ID": "Id",
    "Make_ID": "MakeId",
    "Make_Name": "MakeName",
    "MakeID": "MakeId",
    "Mfr_CommonName": "ManufacturerCommonName",
    "Mfr_ID": "ManufacturerId",
    "Mfr_Name": "ManufacturerName",
    "MfrId": "ManufacturerId",
    "MfrName": "ManufacturerName",
    "Model_ID": "ModelId",
    "Model_Name": "ModelName",
    "ModelID": "ModelId",
}


def standardize_variable_names(object):
    """
    vPIC responses sometimes use different names for the same variable,
    so we'll standardize them before returning to the caller.

    """

    if isinstance(object, dict):
        return {
            STANDARD_VARIABLE_NAMES.get(key, key): standardize_variable_names(value)
            for key, value in object.items()
        }
    elif isinstance(object, list):
        return [standardize_variable_names(item) for item in object]
    else:
        return object
