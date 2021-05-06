from enum import unique
import json
from pathlib import Path

names = []

def get_variable_names(object):
    if isinstance(object, dict):
        for key, value in object.items():
            names.append(key)
            get_variable_names(value)
    elif isinstance(object, list):
        for item in object:
            get_variable_names(item)


response_files = list(Path("tests").glob("**/*.json"))
for rf in response_files:
    with rf.open() as fp:
        resp = json.load(fp)
        get_variable_names(resp)

unique_names = list(set(names))
unique_names.sort()

with Path("variables.txt").open("w", newline="\n") as fp:
    for name in unique_names:
        fp.write(f"{name}\n")
