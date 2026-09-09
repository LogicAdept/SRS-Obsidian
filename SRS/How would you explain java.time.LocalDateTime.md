<!--
reps: 0
priority: 0
-->
#Java/Time/LocalDateTime #SRS

# How would you explain java.time.LocalDateTime

> [!abstract] Short answer
> **`LocalDateTime` is an immutable date-plus-time-of-day with NO time zone — "March 15, 2024, 10:30" on a wall clock somewhere, without saying where.** It stores year-month-day and hour-minute-second-nanos; any mapping to a real instant needs a `ZoneId` supplied by you.

## What it stores and what it refuses to

The javadoc calls it "a description of the local date-time... not tied to any specific locality or time-line". Components are readable directly (`getYear()`, `getHour()`), arithmetic returns new copies, and the type sits between `LocalDate` (no time) and `ZonedDateTime` (adds zone rules).

```java
LocalDateTime dt = LocalDateTime.of(2024, 3, 15, 10, 30);
LocalDateTime later = dt.plusDays(1);
System.out.println("dt             = " + dt);
System.out.println("dt.plusDays(1) = " + later);
System.out.println("same object?   = " + (dt == later));
```

**Listing 1.** Verified on JDK 21:

```java
dt             = 2024-03-15T10:30
dt.plusDays(1) = 2024-03-16T10:30
same object?   = false
```

**Listing 2.** `plusDays` built a new object — the original is untouched; ISO-8601 `T` separates date and time in `toString`.

```d2
direction: right
ld: "LocalDate\n2024-03-15" {
  width: 230
  height: 80
  style.fill: "#e3f2fd"
}
ldt: "LocalDateTime\n2024-03-15T10:30" {
  width: 260
  height: 80
  style.fill: "#fff3e0"
}
zdt: "ZonedDateTime\n2024-03-15T10:30+03:00[Europe/Moscow]" {
  width: 380
  height: 90
  style.fill: "#e8f5e9"
}
ins: "Instant\none point on the UTC line" {
  width: 300
  height: 80
  style.fill: "#fff3e0"
}
ld -> ldt: "atTime(10, 30)"
ldt -> zdt: "atZone(zone)"
zdt -> ins: "toInstant()"
```

**Fig. 1.** `LocalDateTime` in the chain of types: date → date+time → zone-aware → instant. The zone is what turns the picture into a real moment.

## Where it is the right type

`LocalDateTime` matches domain concepts that are civil, not physical: a store opening hours ("09:00 local"), an appointment, a scheduled report per office. Databases map it to SQL `TIMESTAMP`/`TIMESTAMP WITHOUT TIME ZONE`; JSON APIs carry it with an ISO string. Conversions are explicit: `atZone(zone)` produces a `ZonedDateTime`, `toLocalDate()`/`toLocalTime()` split it, `ofInstant(instant, zone)` builds it from a machine instant — the millisecond view is in [[How do you get the current time in milliseconds with the Java 8 Date Time API]].

> [!warning] Two LocalDateTime values can be the same moment — or not
> The trap that costs production incidents: 10:30 in Moscow and 10:30 in New York are six different moments while both print `10:30` — comparing, sorting, or storing `LocalDateTime` across zones silently conflates them. Rules of thumb: persistence and wire formats that mean "a real moment" need `Instant`/`ZonedDateTime` (or `TIMESTAMP WITH TIME ZONE`), not `LocalDateTime`; and never use `LocalDateTime` for arithmetic that crosses a DST boundary — on the US spring-forward night, `local.plusHours(2)` naively walks through a wall-clock hour that does not exist, while `ZonedDateTime.plusHours(2)` lands where the rules say. That divergence is demonstrated in [[How would you explain java.time.ZonedDateTime]]. Also do not confuse it with the legacy `java.util.Date` — `Date` is a zone-less instant (it secretly uses the JVM default zone only when printing), not a civil date-time.

> [!tip] Interview answer
> **LocalDateTime is an immutable ISO date and time of day with no zone — 2024-03-15T10:30 as printed. It is the type for civil, wall-clock meaning: openings, appointments, TIMESTAMP WITHOUT TIME ZONE columns. It cannot name a real instant until you attach a ZoneId via atZone, and cross-zone comparisons or DST-night arithmetic belong to ZonedDateTime or Instant, not here.**

