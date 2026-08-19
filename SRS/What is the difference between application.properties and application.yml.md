<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/Properties #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Both are supported. YAML is nicer for nested config and lists. Properties are flat.

Dump gotchas: YAML is whitespace-sensitive; historically YAML was not loaded via `@PropertySource`. If both formats exist in the same location, dumps say `.properties` wins.

> [!warning] Unverified traps from the dump
> - Do not assume `@PropertySource` loads YAML.
