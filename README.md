# Modbus Models

Public device Thing Models, product metadata and explicitly scoped evidence.
Models live in `<vendor>/<model>/`; optional scenes and images need their own
compatibility, source and redistribution review. Register maps belong only in TMs.
This repository contains no interpreter, simulator runtime or website.

Metadata schema 1 is provided by released `modpoll-wot==0.2.0a3`.
`schemas/schema-source.yaml` pins its source revision, artifact hashes and bundled
schema hash. The schema definition is not copied or independently maintained here.
Data release `modbus-models-v1` is the initial curated catalog. Consumers must
resolve its immutable tag to a full commit SHA and pin file hashes; never use a
floating branch. See schemas/migration.yaml for preserved TM/scenario bytes and
models deferred from the initial release. Vendor originals remain link-only.

## Check a contribution

Use Python 3.12 in a clean environment:

```sh
python -m pip install --require-hashes -r contrib/requirements.txt
python contrib/check.py
python contrib/tests/test-validation.py -v
```

The dependency lock is generated from `contrib/requirements.in` using the command
recorded in its header. Updating it requires checking the producer release and
schema hash, then rerunning the catalog and invalid-input tests.

Catalog validation checks metadata, TM structure/profile, stable IDs and local
reference containment. It does not verify permission claims, calibration or real
hardware. The evidence template deliberately starts at `not-tested`.

The default branch is `main`; all changes enter through a PR and the required
`catalog` check, including administrators. See [contribution guidance](contrib/guide.md).
