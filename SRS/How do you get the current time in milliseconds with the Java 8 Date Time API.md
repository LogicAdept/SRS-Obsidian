<!--
reps: 0
priority: 0
-->
#Java/Time #SRS

# How do you get the current time in milliseconds with the Java 8 Date Time API

> [!abstract] Short answer
> **`Instant.now().toEpochMilli()` is the java.time answer; it equals `System.currentTimeMillis()` — both count milliseconds since 1970-01-01T00:00Z.** The difference is architecture: `Instant` is a real type you can pass, store, and convert, while the static method is a bare long; for tests, wrap either in an injected `Clock`.

## Three sources, one timeline

All three are the same epoch-milli count read at slightly different nanoseconds of the run:

```java
System.out.println("System.currentTimeMillis = " + System.currentTimeMillis());
System.out.println("Instant.now().toEpochMilli = " + Instant.now().toEpochMilli());
System.out.println("new Date().getTime() = " + new java.util.Date().getTime());
```

**Listing 1.** One run on JDK 21:

```java
System.currentTimeMillis = 1788981348036
Instant.now().toEpochMilli = 1788981348049
new Date().getTime() = 1788981348050
```

**Listing 2.** The three values differ only because each call happens a few microseconds later — the scale is the same: milliseconds since the 1970 epoch, in UTC.

```d2
direction: right
sys: "System.currentTimeMillis()\nbare long, cheapest" {
  width: 300
  height: 90
  style.fill: "#e3f2fd"
}
ins: "Instant.now().toEpochMilli()\nsame value as a real type" {
  width: 320
  height: 90
  style.fill: "#fff3e0"
}
clk: "clock.millis()\nvia injected Clock" {
  width: 260
  height: 90
  style.fill: "#e8f5e9"
}
conv: "Conversions\nInstant.ofEpochMilli(m)\nDate.toInstant()" {
  width: 300
  height: 90
  style.fill: "#fff3e0"
}
sys <-> ins
ins <-> clk
ins <-> conv
```

**Fig. 1.** One timeline, several doors; conversions between them are lossless at millisecond precision.

The java.time idiom reverses direction for tests: inject `Clock`, call `clock.instant().toEpochMilli()` (or `clock.millis()`), and hand `Clock.fixed(...)` to the code under test.

## What Instant is — and is not

`Instant` is a point on the UTC timeline (seconds + nanos); it has no calendar fields and no zone. From it, everything else is a conversion: `LocalDateTime.ofInstant(instant, zone)` for civil time (see [[How would you explain java.time.LocalDateTime]]), `instant.atZone(zone)` for a full `ZonedDateTime` (see [[How would you explain java.time.ZonedDateTime]]). `Instant` also carries nanosecond precision — `toEpochMilli()` truncates to millis, which is fine for timestamps and quietly lossy for measuring tiny intervals.

> [!warning] Epoch millis are not a local time, and Instant.now() is not a clock substitution
> Traps around this one-liner. First: the same millisecond value prints as different wall-clock times in Moscow and New York — epoch millis are zone-less; any "current time in milliseconds per user's zone" question is really "convert an Instant to a zone", not "read a different number". Second, precision caveats: `System.currentTimeMillis()` is wall-clock and can step back when NTP adjusts it — duration measurement belongs to `System.nanoTime()`, or better `Instant` sources explicitly documented as monotonic (a plain `Instant.now()` is not guaranteed monotonic either). Third, the legacy hop `new Date().getTime()` works but drags a mutable type into the code for zero benefit; if the API boundary forces a `Date`, convert once (`date.toInstant()`), then stay in java.time.

> [!tip] Interview answer
> **Instant.now().toEpochMilli() — and it is the same number as System.currentTimeMillis(): millis since 1970 UTC. Instant is the java.time type for that count, so it converts cleanly to LocalDateTime or ZonedDateTime through a ZoneId, and to legacy Date via toInstant. For tests, take a Clock parameter and use Clock.fixed. Measure durations with nanoTime, not the wall clock.**

