# check_comsys_ups
Monitor Comsys UPS devices with OP5 Monitor.

Fetch metrics using the OpenXML (unauthenticated) endpoint from Comsys.

## Requirements

* python 2.7 or newer
* python-argparse, python-urllib3

## Installation

* Upload check_comsys_ups.py to /opt/plugins/custom on OP5-server. Set execution permissions.
* Import Comsys UPS.json in the OP5 Management Pack Configuration.
* Use the Host Wizard to add new host-objects.

## Notes

* Thresholds current only available for Load monitoring.
