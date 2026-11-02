# ADAM-5017UH

Eight read-only input registers, AI0_RAW through AI7_RAW, using FC4 at literal
PDU addresses 1–8. Values preserve raw uint16 words and are not calibrated
volts or milliamps. Verify rack, slot, firmware, range settings and wire format
for each installation. This is a mapping for one module, not the entire rack.

The TM bytes were preserved from public modsim commit `febe71632deac8f59b23f5e21302fb3b5d22c3d9`,
path `contrib/advantech/adam-5017uh/adam-5017uh.tm.json`, SHA-256
`9e1d6e38dbb4e2db2f30f8dfd3d9df90a349b2e9aeb60a168ae4d60ee709ead7`.
The original model README explicitly assigns the repository MIT license to the
model; its notice is retained in the root LICENSE. Vendor manuals remain vendor
copyright and are linked in device.yaml rather than redistributed.

No software or hardware evidence is inherited simply by moving this file.
Firmware is explicitly unknown. Device metadata is a draft until its schema
producer and this data repository have immutable releases.
