<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/Properties #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: Boot silently ignores unknown keys. The property class keeps its default. That is a common works-in-dev / wrong-in-prod config bug.

Mitigations dumps name: `@Validated` with `@NotNull` / `@NotBlank`; configuration processor so the IDE warns; fail-on-unknown if enabled; tests that bind from YAML and assert values.

> [!warning] Unverified traps from the dump
> - Relaxed binding is not a spellchecker — `mail-hst` does not bind to `mailHost`.
