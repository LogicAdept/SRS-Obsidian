<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/Embedded #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Set `server.port` in config or `--server.port=9090` on the command line. Default dumps: 8080.

`server.port=0` binds a random free port — dumps use it in tests so parallel runs do not collide.

> [!warning] Unverified traps from the dump
> - `management.server.port` is a different port (Actuator), not `server.port`.
