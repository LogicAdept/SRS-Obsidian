<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/EnumMap #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps show the constructor that takes the key enum’s `Class`:

```java
enum STATE { NEW, RUNNING, WAITING, FINISHED }

EnumMap<STATE, String> stateMap = new EnumMap<STATE, String>(STATE.class);
stateMap.put(STATE.RUNNING, "Program is running");
```

After that, `put` / `get` / `size` / `containsKey` are ordinary `Map` operations.

> [!warning] Unverified traps from the dump
> - There is no no-arg `new EnumMap()` in the examples; the key type token is required.
> - IDE dumps: if the key is an enum, prefer this over `new HashMap<>()`.
