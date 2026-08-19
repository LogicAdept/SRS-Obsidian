<!--
reps: 0
priority: 0
-->
#Java/Spring/Cloud/Config #Java/Spring/Boot/Properties #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: `bootstrap.properties` (or `bootstrap.yml`) sets up the **bootstrap context**, especially to reach Spring Cloud Config **before** the main application context starts. `application.properties` / `application.yml` hold application-specific configuration.

Config client connection details (server URI, fail-fast, application name) historically lived in bootstrap so they are available early enough to load remote property sources.

> [!warning] Unverified traps from the dump
> - Newer Spring Cloud / Boot prefer `spring.config.import=configserver:` in `application.properties` and have deprecated the bootstrap context — interview answers should mention both eras.
> - Putting Config Server URL only in `application.properties` on old stacks is too late if the bootstrap context already started without it.
