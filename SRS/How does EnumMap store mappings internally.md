<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/EnumMap #Java/Language/Enum #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Interview dumps: `EnumMap` is an **array** indexed by the key’s `ordinal()`. There is no `hashCode` call and no collision handling.

A dump quotes `put` as:

```java
int index = ((Enum)key).ordinal();
Object oldValue = vals[index];
vals[index] = maskNull(value);
```

Common `get` / `put` are described as constant-time and typically faster than `HashMap` for enum keys.

> [!warning] Unverified traps from the dump
> - Dumps contrast this with `HashMap` buckets; they claim collision probability is zero because the index is the ordinal.
> - `maskNull` in the snippet is an implementation detail dumps mention for storing values, not a public API.
