<!--
reps: 0
priority: 0
-->
#Java/Language/Enum #Java/Collections/Map/EnumMap #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`EnumMap` is a `Map` for keys of one enum type. Internally it is an array indexed by `ordinal()`. Iteration follows declaration order. Faster and smaller than `HashMap` for enum keys.

```java
enum Day { MON, TUE, WED, THU, FRI, SAT, SUN }
EnumMap<Day, String> plans = new EnumMap<>(Day.class);
plans.put(Day.MON, "gym");
```

Companion dump on `EnumSet`: bit vector (`long` or `long[]`), factories `of` / `range` / `allOf` / `noneOf` / `complementOf`, not `new`. The vault already has an empty stub [[Why does Java provide EnumSet in addition to HashSet and TreeSet]].

> [!warning] Unverified traps from the dump
> - Null keys are typically forbidden on `EnumMap` (stated on other map-overview cards; confirm in fill).
