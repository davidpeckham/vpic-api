import logging
from typing import Any, Dict, Optional
from urllib.parse import urljoin

from requests.adapters import HTTPAdapter

from .exceptions import handle_error_response
from .session import VpicAPISession

log: logging.Logger = logging.getLogger(__name__)


_STANDARD_VARIABLE_NAMES: Dict[str, str] = {
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
    "VehicleTypeName": "VehicleType",
}


class ClientBase(object):
    """A base class for vPIC clients

    Args:
        host: Hostname, including http(s)://, of the vPIC instance to query
        standardize_variables: vPIC uses different names for the same
            variable. Set this to True to standardize variables before
            returning the response.

    """

    def __init__(
        self,
        host: Optional[str] = "https://vpic.nhtsa.dot.gov/api/vehicles",
        standardize_variables: bool = True,
    ):
        if host:
            self.host: str = host
        self.standardize_variables: bool = standardize_variables
        self.session = VpicAPISession()
        self.session.mount(self.url, HTTPAdapter(pool_connections=2, max_retries=5))

    @property
    def url(self) -> str:
        return self.host

    def _request(self, endpoint: str, params: Dict[str, Any] = None):
        if not params:
            params = {"format": "json"}
        else:
            params["format"] = "json"

        api = urljoin(self.url, endpoint)
        resp = self.session.get(api, params=params)

        if resp.status_code >= 400:
            handle_error_response(resp)

        results = resp.json()["Results"]
        if self.standardize_variables:
            results = self._standardize_variable_names(results)

        return results

    def _request_post(self, endpoint: str, data, params=None):
        if not params:
            params = {"format": "json"}
        elif "format" not in params:
            params["format"] = "json"

        api = urljoin(self.url, endpoint)
        resp = self.session.post(url=api, data=data, params=params)

        if resp.status_code >= 400:
            handle_error_response(resp)

        results = resp.json()["Results"]
        if self.standardize_variables:
            results = self._standardize_variable_names(results)

        return results

    def _standardize_variable_names(self, object):
        """
        vPIC responses sometimes use different names for the same variable,
        so we'll standardize them before returning to the caller.

        """

        if isinstance(object, dict):
            return {
                _STANDARD_VARIABLE_NAMES.get(
                    key, key
                ): self._standardize_variable_names(value)
                for key, value in object.items()
            }
        elif isinstance(object, list):
            return [self._standardize_variable_names(item) for item in object]
        else:
            return object
