# snmp_ms
A wrapper for **easysnmp** with manager and session which manager is used for polling and session is extended to support different vendors.

## Session (snmps)
* The input paramter is almost as same as easysnmp.
* baseClient is the base snmp worker to get data, for now it would only get cpu, storage, interface bandwidth and vendor cpu.
* For now, only ciscoClient is extended from baseClient to support getting vendor cpu.
* Some idea is coming from _nelsnmp_.

## Manaegr (snmpm)
* An simple polling mechanism working in thread.
* Maintain a snmp agent list to be monitored.

## test
* Test script to use snmps and snmpm.