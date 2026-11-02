# ADAM-6024

Documentation-derived raw I/O mapping: six AI, two AO, two DI and two DO.
Candidate PDU starts are AI 0 (FC4), AO 10 (FC3), DI 0 (FC2), DO 16 (FC1).
Analog words are unscaled uint16; transport bounds do not establish legal output
ranges or calibrated engineering units. Confirm mapping and firmware before use.
Range configuration, calibration, watchdog and physical output behavior are excluded.

The TM and declarative scenario retain the project MIT license and original
bytes; see [migration provenance](../../schemas/migration.yaml). The scenario
uses synthetic AO-to-AI and DO-to-DI loopback, not physical device behavior.
Vendor manuals are linked in device.yaml and are not redistributed.
No hardware or software evidence is inherited by migration.

Use the fixed TM URL with modsim. Prepare the optional scenario locally from
this same data revision; only explicit --allow-scripts permits local Python.

The project TM and declarative simulation files are MIT-licensed. Vendor
reference materials remain link-only and are not covered by that permission.

The project TM and declarative simulation files are MIT-licensed. Vendor
reference materials remain link-only and are not covered by that permission.
