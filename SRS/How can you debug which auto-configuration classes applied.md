<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/AutoConfiguration #Java/Spring/Boot/Actuator #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Run with `--debug` (or `debug=true`) to print the auto-configuration report: positive and negative matches with the condition that passed or failed.

Dumps also name `/actuator/conditions` for the same report at runtime.

> [!warning] Unverified traps from the dump
> - The conditions endpoint is Actuator: it must be on the classpath and exposed.
