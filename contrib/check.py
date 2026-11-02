"""Validate the catalog using the exact released interpreter and metadata schema."""

import hashlib
from importlib.metadata import version
from importlib.resources import files
import json
from pathlib import Path
import sys

import yaml
from evidence import load_yaml, validate_evidence
from modpoll_wot import loads_model, validate_standard
from modpoll_wot.metadata import load_device_record

ROOT = Path(__file__).resolve().parents[1]
RESERVED = {"contrib", "schemas"}


def contained(path, directory):
    resolved = path.resolve(strict=True)
    if not resolved.is_relative_to(directory.resolve()) or not resolved.is_file():
        raise ValueError(f"Reference leaves model directory: {path}")
    return resolved


def verify_producer(root):
    lock = yaml.safe_load((root / "schemas/schema-source.yaml").read_text())
    if lock["package"] != "modpoll-wot" or version("modpoll-wot") != lock["version"]:
        raise ValueError("Installed producer differs from the exact schema lock")
    payload = (
        files("modpoll_wot").joinpath("schemas", "device-schema.yaml").read_bytes()
    )
    if hashlib.sha256(payload).hexdigest() != lock["schema-sha256"]:
        raise ValueError("Installed schema content differs from the schema lock")


def validate_catalog(root):
    root = Path(root).resolve()
    verify_producer(root)
    entries = []
    seen = set()
    for directory in sorted(root.glob("*/*")):
        if directory.parts[-2] in RESERVED or directory.parts[-2].startswith("."):
            continue
        if not directory.is_dir():
            continue
        if not directory.resolve().is_relative_to(root):
            raise ValueError(f"Model directory leaves catalog: {directory}")
        record = load_device_record(contained(directory / "device.yaml", directory))
        expected = directory.relative_to(root).as_posix()
        if record["id"] != expected or record["id"] in seen:
            raise ValueError(f"Duplicate or mismatched stable model ID: {record['id']}")
        seen.add(record["id"])
        paths = {item["path"] for item in record["models"]}
        if paths != {p.name for p in directory.glob("*.tm.json")}:
            raise ValueError(f"TM files and metadata references disagree: {expected}")
        for name in sorted(paths):
            path = contained(directory / name, directory)
            payload = path.read_bytes()
            validate_standard(json.loads(payload), kind="tm")
            loads_model(
                payload,
                source=str(path),
                kind="tm",
                host="127.0.0.1",
                port=5020,
                unit_id=1,
            )
        evidence_schema = load_yaml((root / "schemas/evidence-schema.yaml").read_bytes())
        for evidence in sorted((directory / "evidence").glob("*.yaml")):
            document = load_yaml(contained(evidence, directory).read_bytes())
            def read_reference(value):
                return contained(evidence.parent / value, directory).read_bytes()
            model = json.loads(read_reference(document["model"]["path"]))
            validate_evidence(document, evidence_schema, read_reference, set(model["properties"]))
        entries.append(record["id"])
    if not entries:
        raise ValueError("No publishable model records found")
    load_device_record(root / "contrib/templates/device.yaml")
    evidence = yaml.safe_load(
        (root / "contrib/templates/evidence/l1-check.yaml").read_text()
    )
    required = {
        "level",
        "status",
        "model",
        "profile",
        "tools",
        "checks",
        "executed-at",
        "executor",
        "run-url",
        "limitations",
    }
    if not required.issubset(evidence) or evidence["status"] != "not-tested":
        raise ValueError(
            "Evidence template must retain required fields and untested status"
        )
    return entries


if __name__ == "__main__":
    try:
        result = validate_catalog(ROOT)
    except (ValueError, OSError, KeyError, TypeError, yaml.YAMLError) as error:
        print(f"Catalog validation failed: {error}", file=sys.stderr)
        raise SystemExit(1)
    print(f"Validated {len(result)} model record(s); no hardware or calibration claim")
