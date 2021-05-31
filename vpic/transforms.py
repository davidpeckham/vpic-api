import re
from typing import Dict, List, Any, Union

_STANDARD_VARIABLE_NAMES: Dict[str, str] = {
    "ID": "Id",
    "GCWR": "GCWRFrom",
    "GCWR_to": "GCWRTo",
    "GVWR": "GVWRFrom",
    "GVWR_to": "GVWRTo",
    "Make_ID": "MakeId",
    "MakeID": "MakeId",
    "Make_Name": "Make",
    "MakeName": "Make",
    "Mfr_CommonName": "ManufacturerCommonName",
    "Mfr_ID": "ManufacturerId",
    "Mfr_Name": "Manufacturer",
    "ManufacturerName": "Manufacturer",
    "MfrId": "ManufacturerId",
    "MfrName": "Manufacturer",
    "Model_ID": "ModelId",
    "Model_Name": "Model",
    "ModelName": "Model",
    "ModelID": "ModelId",
    "VehicleTypeName": "VehicleType",
}


def standardize(object: Union[Dict, List[Dict]]):
    """Standardize response variable names.

    vPIC responses sometimes use different names for the same variable,
    so we'll standardize them before returning to the caller.

    Args:
        object: a vPIC response object

    Returns:
        object, with standardized keys

    Example:
        >>> standardize({ 'Mfr_ID' : 232 })
        { 'ManufacturerId' : 232 }

    """
    if isinstance(object, dict):
        return {
            _STANDARD_VARIABLE_NAMES.get(key, key): standardize(value)
            for key, value in object.items()
        }
    elif isinstance(object, list):
        return [standardize(item) for item in object]
    else:
        return object


_VARIABLE_NAME_RE = re.compile(r"([A-Z]+)(?=([a-z_]|))")

_WORDS_TO_SEPARATE: Dict[str, str] = {
    "ncsa": "ncsa_",
    "evdrive": "ev_drive",
    "sae": "sae_",
    "dotcode": "dot_code",
    "gcwrfrom": "gcwr_from",
    "gvwrfrom": "gvwr_from",
    "gcwrto": "gcwr_to",
    "gvwrto": "gvwr_to",
}


def snake_case(object: Dict[str, Any]) -> Dict[str, Any]:
    """Convert response variable names (JSON keys) to snake case.

    TypedClient returns model objects with pythonic property names,
    so we need to transform variable names in vPIC responses to
    snake case.

    Args:
        object: a vPIC response object

    Returns:
        A new object with snake-cased variable names (keys)

    Example:
        >>> snake_case({ 'ManufacturerId' : 232 })
        { 'manufacturer_id' : 232 }

    """
    new_object: Dict[str, Any] = {}
    for key, value in object.items():
        new_key = _VARIABLE_NAME_RE.sub(r"_\1", key).lower()
        new_key = new_key.replace("__", "_")
        if new_key[0] == "_":
            new_key = new_key[1:]

        for compound_word, separated_word in _WORDS_TO_SEPARATE.items():
            if compound_word in new_key:
                new_key = new_key.replace(compound_word, separated_word)
                break

        if isinstance(value, list):
            value = [snake_case(v) for v in value]

        new_object[new_key] = value
    return new_object
