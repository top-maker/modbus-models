# Contribute a model

Submit one executable Thing Model and identify the public source, permission to
redistribute your files, known mapping limits and firmware assumptions. Corrections
need only the relevant change and its source. A full device record, README,
image, scenario and hardware report are not mandatory submission paperwork;
maintainers can help curate the minimum record before data publication.

Use lowercase kebab-case vendor/model paths and keep stable IDs when correcting
mappings. Keep addresses, types, byte order and scaling only in the TM. Do not
include credentials, private endpoints, serial numbers or private customer data.
Vendor documents and photos need their own redistribution basis; an upstream
file being publicly accessible does not grant permission to mirror it.

Target `main` with a pull request. CI uses the exact released producer and schema
hash in schemas/schema-source.yaml. It validates TMs, metadata, references and
containment and rejects malformed-record regressions. A minimal TM-only PR may
remain pending while a maintainer adds the publication record; contributors are
not required to prepare the full metadata themselves.

Configuration checks, software interoperability and hardware communication are
separate evidence categories; report exact versions, coverage and limitations.
Never label an unexecuted check as passed. A merged model is not hardware certification.

L2 product records use schemas/evidence-schema.yaml. Keep model/scenario hashes,
actual CI run and test revision, exact tool versions, expected/actual checks,
covered/excluded properties and limitations. Catalog CI rejects hash drift and
passed records containing failed or mismatched checks; it does not execute or
certify hardware. No evidence is required merely to propose a new model.
