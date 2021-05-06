import json
from pathlib import Path

from vpic.client import Vpic

api = Vpic()

# get model year vin guides for FCA US LLC (manufacturer of JEEP)

parts = []

for page in range(1, 10):
    results = api.get_parts("565", "2020-01-01", "2022-12-30", page)
    if len(results) == 0:
        break
    for r in results:
        if r["ManufacturerId"] == 994:
            parts.append(r)

for page in range(1, 10):
    results = api.get_parts("566", "2015-01-01", "2022-12-30", page)
    if len(results) == 0:
        break
    for r in results:
        if r["ManufacturerId"] == 994:
            parts.append(r)

with Path("jeep.json").open("w") as fp:
    json.dump(parts, fp)
