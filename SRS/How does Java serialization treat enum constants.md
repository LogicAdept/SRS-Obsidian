<!--
reps: 0
priority: 0
-->
#Java/Language/Enum #Java/Serialization #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: enums are `Serializable` because `java.lang.Enum` implements `Serializable`. You do not write `implements Serializable` on the enum.

Serialization writes the constant’s `name()`, not the full object graph / extra field state in the usual way. Deserialization looks the constant up (dumps: by name / `valueOf`) so the singleton identity is kept.

Default `serialVersionUID` for enum types is claimed to be `0L`. Extra instance fields on the enum are described as not part of that name-based form.

> [!warning] Unverified traps from the dump
> - Verify whether extra fields survive serialize/deserialize; dumps emphasise name-only.
