<!--
reps: 0
priority: 0
-->
#Java/Quarkus #SRS #New

> [!warning] Untrusted draft
> Drafted from general framework knowledge, not from an opened question dump. Not yet checked against official documentation. Do not treat this as a review answer.

Draft: quarkus.* properties are split into build-time-fixed and runtime-overridable. Build-time properties are consumed during augmentation, baked into the artifact, and become read-only at runtime; changing them requires a rebuild (or re-augmentation).
Runtime properties (e.g. database URL, credentials, HTTP port) can change per environment without rebuild.
Docs mark build-time-fixed properties with a lock icon in the configuration reference.
Build records available config into the binary so startup fails fast on missing required values; system properties, env vars, .env and build-system sources are excluded from that recording.
Trap: launching with a different profile than the build profile is supported but can yield unexpected results; default runtime profile equals the build profile.

> [!warning] Unverified traps from the draft
> - Facts above are plausible but unchecked; version numbers and exact API names must be confirmed against official docs before this card is used as a review answer.
> - Comparison cards must keep both sides tagged and avoid absolute always/never claims.
