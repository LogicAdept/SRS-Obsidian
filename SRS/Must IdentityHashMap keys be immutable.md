<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/IdentityHashMap #Java/HashCodeEquals #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: **no.** `HashMap` keys should be immutable because `equals` / `hashCode` must stay stable. `IdentityHashMap` does **not** call those methods, so that immutability rule **does not apply**.

> [!warning] Unverified traps from the dump
> - “Need not be immutable” is not “mutating the key is a good idea”; the dump’s CreditCard sample only shows `HashMap` lookup breaking.
> - Identity still follows the **reference**. Replacing the key object is a different `==`.
