# Modbus Models

Public device Thing Models, product metadata and explicitly scoped evidence.
The repository is a data source; it contains no Modbus interpreter, simulator
runtime or website. Models live in `<vendor>/<model>/`. Scenarios and images are
optional and require their own source, compatibility and permission review.

This checkout is an initial candidate, not a released catalog. The metadata
schema is owned by modpoll-wot. Its schema-1 producer candidate has not yet been
published; schemas/producer-candidate.yaml records that dependency without
requiring an unavailable package in public installation or CI configuration.
After the producer release is verified, pin its exact wheel/schema hashes, add
public validation CI and issue an immutable data tag. Do not use a floating
branch as a consumer dependency.

See [contribution guidance](contrib/guide.md). Register maps belong only in TMs;
metadata and simulation inputs must not duplicate addresses or decoding rules.
