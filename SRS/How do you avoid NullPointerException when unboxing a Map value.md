<!--
reps: 0
priority: 0
-->
#Java/Language/Wrappers #Java/Collections #Java/Exceptions/Unchecked #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`Map.get` can return `null` for a missing key. Assigning that `Integer` to `int` unboxes and throws NPE.

Dumps list strategies:

- `int val = map.getOrDefault("key", 0);` (default must be compatible with `Integer`).
- `Integer wrapped = map.get(key); if (wrapped != null) { int val = wrapped; }`
- `int val = Objects.requireNonNullElse(map.get(key), 0);`
- `Optional.ofNullable(map.get(key)).orElse(0)`

Choice depends on whether `0` is a valid stored value that would be confused with “not present.”

> [!warning] Unverified traps from the dump
> - `getOrDefault` still unboxes if you assign to `int` and the stored value is `null` (a present null).
> - Do not treat missing key and stored `0` as the same unless that is the domain rule.
