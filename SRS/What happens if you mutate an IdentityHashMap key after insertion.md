<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/IdentityHashMap #Java/HashCodeEquals #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump sample: put the same `CreditCard` instance into `HashMap` and `IdentityHashMap`, then **mutate** `expiryDate` (a field used by `equals`/`hashCode`). After that, `HashMap.get` / `containsKey` are **false** (hashCode changed). `IdentityHashMap.get` / `containsKey` stay **true** (still the same reference).

> [!warning] Unverified traps from the dump
> - The dump never calls `equals` on the IdentityHashMap path in the printed log.
> - This is not a license to use mutable value-keys in `HashMap`.
