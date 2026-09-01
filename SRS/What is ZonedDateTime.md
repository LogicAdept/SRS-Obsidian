<!--
reps: 0
priority: 0
-->
#Java/Time/ZonedDateTime #Java/Versions/8 #SRS

# What is ZonedDateTime

> [!abstract] Short answer
> **`ZonedDateTime` is Java 8’s immutable ISO-8601 date-and-time *with a time-zone*** — e.g. `2007-12-03T10:15:30+01:00[Europe/Paris]`. It stores a `LocalDateTime`, a `ZoneId`, and the resolved `ZoneOffset`. That is how it maps the local timeline to an `Instant`. It is **not** `java.util.Calendar` (different type, immutable, value-based). Nanosecond precision. `plusDays` follows the **local** timeline; `plusHours` follows the **instant** timeline.

## Local fields plus zone rules

`java.time.ZonedDateTime` (`@since 1.8`) is `final`, immutable, thread-safe, and value-based. Design: primarily `LocalDateTime` + `ZoneId`. The offset is secondary but required so the value is an instant — especially in a DST overlap, when one local time has two valid offsets ([[What is LocalDateTime]], [[How would you explain java.time.ZonedDateTime]]).

The dump’s “Calendar analog” is a teaching shortcut: both carry civil fields and a zone. This class does **not** extend `Calendar`, is not mutable, and must not be compared with `==`. Offset from UTC comes from `ZoneId` rules, not a freely set field.

Converting local → instant has three cases: **normal** (one offset), **gap** (spring-forward: zero offsets; the local time is shifted forward by the gap, typically into “summer”), **overlap** (fall-back: two offsets; keep the previous offset if valid, else the earlier / typically “summer”). `withEarlierOffsetAtOverlap` / `withLaterOffsetAtOverlap` pick when both exist.

`plusDays` / `plusMonths` / `plusYears` add on the **local** timeline, then re-resolve the offset (gap/overlap rules). `plusHours` / `plusMinutes` / `plusSeconds` / `plusNanos` add on the **instant** timeline: one hour later is always one hour of elapsed time; the local clock may jump by a different amount. **Adding one day is not the same as adding 24 hours** ([[How would you explain java.time.LocalDateTime]], [[How do you get the current date with the Java 8 Date Time API]]).

```d2
ldt: "LocalDateTime\nlocal timeline" {
  shape: rectangle
}
zone: "ZoneId\nEurope/Paris rules" {
  shape: rectangle
}
zdt: "ZonedDateTime\nldt + zone + ZoneOffset" {
  shape: rectangle
}
inst: "Instant\nUTC timeline" {
  shape: rectangle
}
ldt -> zdt: "of / atZone"
zone -> zdt: "valid offsets"
zdt -> inst: "toInstant\nplusHours"
```

**Fig. 1.** Zone rules pick the offset. Days/months stay on the local line; hours stay on the instant line.

```java
ZonedDateTime paris = ZonedDateTime.parse("2007-12-03T10:15:30+01:00[Europe/Paris]");
paris.getZone();
paris.getOffset();
paris.toLocalDateTime();
paris.plusDays(1);
paris.plusHours(24);
ZonedDateTime.now();
```

**Listing 1.** ISO text with offset and zone id. `plusDays(1)` and `plusHours(24)` are different APIs (local vs instant) and can disagree across DST.

> [!warning] Zone is not a decoration, and 24 hours is not a day
>
> A DST **gap** has no local time; an **overlap** has two. `plusHours` always moves by that duration on the instant line — the wall clock can skip or repeat. `plusDays` keeps the civil time and re-resolves the offset. `OffsetDateTime` has an offset but not named zone rules. Do not use `==`. The offset cannot be set independently of the zone.

> [!tip] Interview answer
>
> **`ZonedDateTime` is immutable ISO date+time + `ZoneId` (and resolved offset), Java 8.** That is the `java.time` type for “when in Paris.” Not `Calendar`. Gaps/overlaps matter. `plusDays` = local timeline; `plusHours` = instant timeline (`1 day` ≠ `24 hours`). For a zoneless civil time use `LocalDateTime`; for a timeline tick use `Instant`.
