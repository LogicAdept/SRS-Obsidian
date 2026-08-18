<!--
reps: 0
priority: 0
-->
#Java/Language/Enum #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

No. `compareTo` is `final` on enumerations so callers cannot change the sort order, which is the declaration order of the constants.

> [!warning] Unverified traps from the dump
> - Use a `Comparator` if you need a different order; dumps do not spell that workaround.
