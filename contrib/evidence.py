"""Validate scoped product evidence; schemas do not certify execution or hardware."""

import hashlib
import json
from pathlib import Path

from jsonschema import Draft202012Validator
import yaml


def load_yaml(payload):
    class UniqueLoader(yaml.SafeLoader):
        def construct_mapping(self, node, deep=False):
            result = {}
            for key, value in node.value:
                name = self.construct_object(key, deep=deep)
                if not isinstance(name, str) or name in result:
                    raise ValueError("Evidence YAML requires unique string keys")
                result[name] = self.construct_object(value, deep=deep)
            return result
    if any(isinstance(event, yaml.AliasEvent) or getattr(event, "anchor", None) for event in yaml.parse(payload)):
        raise ValueError("Evidence aliases/anchors are unsupported")
    return yaml.load(payload, Loader=UniqueLoader)


def validate_evidence(document, schema, read, property_names):
    error = next(Draft202012Validator(schema, format_checker=Draft202012Validator.FORMAT_CHECKER).iter_errors(document), None)
    if error:
        raise ValueError(f"Invalid evidence: {error.message}")
    for field in ("model", "scenario"):
        reference = document[field]
        if hashlib.sha256(read(reference["path"])).hexdigest() != reference["sha256"]:
            raise ValueError(f"Evidence {field} hash differs from input")
    if not set(document["covered"]).issubset(property_names):
        raise ValueError("Evidence covers unknown properties")
    if document["status"] == "passed" and any(c["status"] != "passed" or c["expected"] != c["actual"] or c["actual"] is None for c in document["checks"]):
        raise ValueError("Passed evidence contains an unpassed check")
    scene = json.loads(read(document["scenario"]["path"]))
    if not set(document["covered"]).issubset(scene.get("initial", {})):
        raise ValueError("Evidence scenario lacks covered initial values")
