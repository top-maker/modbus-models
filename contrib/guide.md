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

The templates are drafts pending an immutable schema producer release. A future
contribution CI must validate TMs, metadata, references and file containment before
merge. Configuration checks, software interoperability and hardware communication
are separate evidence categories; report exact versions, coverage and limitations.
Never label an unexecuted check as passed. A merged model is not hardware certification.
