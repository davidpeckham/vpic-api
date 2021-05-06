import json

import pytest
from requests import Response

from vpic.exceptions import (
    InvalidParameters,
    MethodNotFound,
    handle_error_response,
)


def _response(content, status_code):
    r = Response()
    r.status_code = status_code
    r._content = json.dumps(content).encode()
    return r


def test_invalid_parameter():
    r = _response(
        {
            "message": "The request is invalid.",
            "messageDetail": "The parameters dictionary contains a null entry \
                for parameter 'id' of non-nullable type 'System.Int32' for \
                    method 'System.Net.Http.HttpResponseMessage \
                        GetVehicleTypesForMakeId(Int32, System.String)' in \
                            'APIEF.Controllers.VehiclesController'. An optional \
                                parameter must be a reference type, a nullable type, \
                                    or be declared as an optional parameter.",
        },
        status_code=400,
    )

    with pytest.raises(InvalidParameters) as exc_info:
        handle_error_response(r)

    e = exc_info.value
    assert e.response == r


def test_missing_method():
    r = _response(
        {
            "message": "No HTTP resource was found that matches the \
                request URI 'https://app-prod-vpic-api.nhtsa-prod-ext.\
                    appserviceenvironment.net/api/vehicles/DecodeVinValues/\
                        ?modelyear=1891&format=json'.",
            "messageDetail": "No action was found on the controller \
                'Vehicles' that matches the request.",
        },
        status_code=404,
    )

    with pytest.raises(MethodNotFound) as exc_info:
        handle_error_response(r)

    e = exc_info.value
    assert e.response == r
