"""Catalog acceptance rejects stale schema and unsafe or incomplete references."""

import hashlib
from importlib.metadata import version
from importlib.resources import files
import importlib.util
import json
from pathlib import Path
import shutil
from tempfile import TemporaryDirectory
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location(
    "catalog_check", ROOT / "contrib/check.py"
)
check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check)


class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.tmp = TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        for folder in ("advantech", "schemas", "contrib/templates"):
            shutil.copytree(ROOT / folder, self.root / folder)
        payload = (
            files("modpoll_wot").joinpath("schemas", "device-schema.yaml").read_bytes()
        )
        lock = {
            "package": "modpoll-wot",
            "version": version("modpoll-wot"),
            "schema-sha256": hashlib.sha256(payload).hexdigest(),
        }
        (self.root / "schemas/schema-source.yaml").write_text(yaml.safe_dump(lock))
        self.record = self.root / "advantech/adam-5017uh/device.yaml"
        self.tm = self.root / "advantech/adam-5017uh/adam-5017uh.tm.json"

    def test_valid_catalog_and_reserved_templates(self):
        self.assertEqual(check.validate_catalog(self.root), ["advantech/adam-5017uh", "advantech/adam-6024"])

    def test_missing_record_and_mismatched_identity(self):
        source = self.record.read_text()
        self.record.unlink()
        with self.assertRaises(FileNotFoundError):
            check.validate_catalog(self.root)
        self.record.write_text(source.replace("advantech/adam-5017uh", "another/model"))
        with self.assertRaisesRegex(ValueError, "stable model ID"):
            check.validate_catalog(self.root)

    def test_schema_hash_and_profile_regressions(self):
        lock = self.root / "schemas/schema-source.yaml"
        source = lock.read_text()
        lock.write_text(
            source.replace("schema-sha256:", "unexpected:")
            + '\nschema-sha256: "wrong"\n'
        )
        with self.assertRaisesRegex(ValueError, "schema content"):
            check.validate_catalog(self.root)
        lock.write_text(source)
        model = json.loads(self.tm.read_text())
        model["modpoll:version"] = "99"
        self.tm.write_text(json.dumps(model))
        with self.assertRaises(ValueError):
            check.validate_catalog(self.root)

    def test_symlink_escape_and_unreferenced_tm(self):
        payload = self.tm.read_bytes()
        outside = self.root / "outside.tm.json"
        outside.write_bytes(payload)
        self.tm.unlink()
        self.tm.symlink_to(outside)
        with self.assertRaisesRegex(ValueError, "leaves model directory"):
            check.validate_catalog(self.root)
        self.tm.unlink()
        self.tm.write_bytes(payload)
        self.tm.with_name("unexpected.tm.json").write_bytes(payload)
        with self.assertRaisesRegex(ValueError, "references disagree"):
            check.validate_catalog(self.root)

    def test_missing_producer_pin_and_symlinked_model_directory(self):
        pin = self.root / "schemas/schema-source.yaml"
        lock = pin.read_text()
        pin.unlink()
        with self.assertRaises(FileNotFoundError):
            check.verify_producer(self.root)
        pin.write_text(lock)
        outside = self.root.parent / (self.root.name + "-outside")
        self.addCleanup(shutil.rmtree, outside, True)
        shutil.move(self.root / "advantech/adam-5017uh", outside)
        (self.root / "advantech/adam-5017uh").symlink_to(
            outside, target_is_directory=True
        )
        with self.assertRaisesRegex(ValueError, "leaves catalog"):
            check.validate_catalog(self.root)

    def test_duplicate_metadata_key(self):
        self.record.write_text('model: "duplicate"\n' + self.record.read_text())
        with self.assertRaisesRegex(ValueError, "duplicate YAML key"):
            check.validate_catalog(self.root)


if __name__ == "__main__":
    unittest.main()
