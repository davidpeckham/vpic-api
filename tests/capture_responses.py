import json
from pathlib import Path

from requests.adapters import HTTPAdapter
from vpic.session import VpicAPISession
from vpic.transforms import standardize


"""
Capture API responses for unit tests

Supports GET requests, but does not yet support POST requests
like decode_vin_batch.

"""

session = VpicAPISession()
session.mount(
    "https://vpic.nhtsa.dot.gov/api/vehicles",
    HTTPAdapter(pool_connections=2, max_retries=5),
)

response_files = list(Path("tests").glob("**/*.json"))
for rf in response_files:
    with rf.open(encoding="utf-8") as fp:
        data = json.load(fp)
        url = data["url"]
        limit = data.get("limit", None)
        post_data = data.get("post_data", None)

        if post_data is None:
            resp = session.get(url)
        else:
            resp = session.post(url=url, data=post_data)

        print(f"{fp.name} {url} {resp.status_code}")

        if resp.status_code < 400:
            raw_response = resp.json()
            results = raw_response["Results"]
            if limit == 1:
                transformed_response = standardize(results[0])
            else:
                transformed_response = standardize(results)
        else:
            raw_response = None
            transformed_response = None

    if raw_response is None:
        continue

    with rf.open(encoding="utf-8", mode="w") as fp:
        data["content"] = raw_response
        data["expected_result"] = transformed_response
        json.dump(data, fp, indent=4)
