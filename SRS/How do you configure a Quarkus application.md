<!--
reps: 0
priority: 0
-->
#Java/Quarkus #SRS #New

> [!warning] Untrusted draft
> Drafted from general framework knowledge, not from an opened question dump. Not yet checked against official documentation. Do not treat this as a review answer.

Draft procedure: application.properties in src/main/resources (YAML possible via config-yaml extension); quarkus.* namespace belongs to the platform.
Injection: @ConfigProperty(name="...") on fields/constructor params, @ConfigMapping interfaces for groups, programmatic access via ConfigProvider or @Inject Config.
Sources by descending ordinal: system properties (400), environment variables (300), .env file (295), $PWD/config/application.properties (260), classpath application.properties (250), META-INF/microprofile-config.properties (100).
Profiles: prefix properties with %dev, %test, %prod; dev/test/prod activate automatically; custom profiles allowed; .env uses _DEV_ style prefixes.
SmallRye Config is the underlying implementation (MicroProfile Config).

> [!warning] Unverified traps from the draft
> - Facts above are plausible but unchecked; version numbers and exact API names must be confirmed against official docs before this card is used as a review answer.
> - Comparison cards must keep both sides tagged and avoid absolute always/never claims.
