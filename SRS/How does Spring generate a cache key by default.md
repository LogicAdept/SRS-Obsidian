<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Cache #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`SimpleKeyGenerator`: no args → `SimpleKey.EMPTY`; one arg → the argument itself; several args → `new SimpleKey(...)` with `equals`/`hashCode`. Override with `key` SpEL on the annotation or a `keyGenerator` bean. Dumps say you cannot set both `key` and `keyGenerator` on the same annotation.

> [!warning] Unverified traps from the dump
> - Mutable argument objects as keys break if `equals`/`hashCode` change after the put.
> - One-arg keys that are arrays or poorly implemented value types collide.

