<!--
reps: 0
priority: 0
-->
#Java/Time #SRS

# How do you get the current date with the Java 8 Date Time API

> [!abstract] Short answer
> **`LocalDate.now()` — and inject a `java.time.Clock` when you need the "current" date to be deterministic.** `LocalDate` is an immutable ISO-8601 date without time or zone; `now()` asks the system clock in the default zone, while `now(clock)` and `now(zone)` make the source explicit and testable.

## What now() reads

`LocalDate` stores year, month, day — nothing else. The javadoc's own framing: it is "a description of the date, as used for birthdays"; it cannot name an instant on the timeline without zone or offset information. `now()` uses the system clock and default time zone; `now(ZoneId)` pins the zone; `now(Clock)` pins the whole time source.

```java
LocalDate today = LocalDate.now();
System.out.println("today = " + today);            // e.g. 2024-03-15

LocalDate fixed = LocalDate.now(Clock.fixed(
        LocalDate.of(2024, 3, 15)
                .atStartOfDay(ZoneId.systemDefault()).toInstant(),
        ZoneId.systemDefault()));
System.out.println("fixed = " + fixed);            // always 2024-03-15
```

**Listing 1.** The one-liner, and the testable variant. The fixed-`Clock` call prints `fixed = 2024-03-15` on every run (verified on JDK 21).

```d2
direction: right
src: "Time source\nClock.fixed(...) in tests" {
  width: 260
  height: 90
  style.fill: "#e3f2fd"
}
now: "LocalDate.now(clock)\nreads year/month/day" {
  width: 290
  height: 90
  style.fill: "#fff3e0"
}
zone: "No zone stored\nbirthday-style date" {
  width: 250
  height: 90
  style.fill: "#fff3e0"
}
out: "Immutable value\narithmetic returns copies" {
  width: 280
  height: 90
  style.fill: "#e8f5e9"
}
src -> now -> zone -> out
```

**Fig. 1.** The clock is a dependency you control; the date you get back is a plain immutable value.

## Variations worth knowing in the interview

The same `now()` family exists across the package: `LocalTime.now()` (time of day), `LocalDateTime.now()` (both, still zone-less — see [[How would you explain java.time.LocalDateTime]]), `ZonedDateTime.now()` (fully zone-aware — [[How would you explain java.time.ZonedDateTime]]), and `Instant.now()` (a timeline instant for machine time — [[How do you get the current time in milliseconds with the Java 8 Date Time API]]). Arithmetic never mutates: `today.plusWeeks(1)` returns a new `LocalDate`, covered in [[How do you add a week month year or decade with the Java 8 Date Time API]].

> [!warning] now() is not a constant — and the legacy Date does not come back
> Two traps. First, `LocalDate.now()` in a test depends on the wall clock: a "birthday check" that passes today fails the day after; production code should take a `Clock` (or a `LocalDate`) parameter, with `Clock.systemDefaultZone()` as the production wiring — this is the difference between a flaky and a deterministic test. Second, the answer is not `new Date()` — `java.util.Date` is a timestamp with a zone only in its `toString`, it is mutable, and mixing it with java.time forces conversions through `toInstant()`. Also note `LocalDate.now()` differs across servers by zone: two data centers "on the same day" can disagree around midnight unless the zone is pinned.

> [!tip] Interview answer
> **LocalDate.now() gives today's date in the default zone — an immutable ISO-8601 value with no time or zone attached. For tests, inject java.time.Clock and use Clock.fixed so "today" is deterministic; the same now() pattern exists for LocalTime, LocalDateTime, ZonedDateTime and Instant. Never reach back to java.util.Date for this.**

