<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/Actuator #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

The `/loggers` endpoint shows loggers and lets you change the log level at runtime without restart. Dumps list it next to `/logfile` (read the log file contents).

> [!warning] Unverified traps from the dump
> - `/loggers` must be exposed (and usually secured) or the dump procedure does nothing over HTTP.
