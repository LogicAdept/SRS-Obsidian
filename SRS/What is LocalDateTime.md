<!--
reps: 0
priority: 0
-->
#Java/Versions/8 #Java/Time/LocalDateTime #SRS

# What is LocalDateTime

> [!abstract] Short answer
> **`LocalDateTime` is Java 8’s immutable ISO-8601 date-and-time with nanosecond precision and no time-zone.** Think wall-clock date plus time (`2007-12-03T10:15:30`), not an instant on the timeline. Split with `toLocalDate()` / `toLocalTime()`. `plusHours` / `plusMinutes` return **copies**. `now()` reads the clock but the value still stores no zone.

## Date and time, not a zone

`java.time.LocalDateTime` (`@since 1.8`) is a `final`, immutable, thread-safe, value-based class. It is a date-time without a time-zone in the ISO-8601 calendar (proleptic Gregorian). Example: `2007-12-03T10:15:30`. Time goes to nanoseconds. It does **not** store a zone or offset, so it cannot represent an instant unless you add one (`atZone`, `atOffset`) ([[How would you explain java.time.LocalDateTime]], [[What is ZonedDateTime]], [[How would you explain java.time.ZonedDateTime]]).

The dump’s “`LocaleDate`” is `LocalDate`. `toLocalDate()` / `toLocalTime()` are the two halves. Use it like a birthday-plus-wall-clock, not like `Instant`.

`now()` / `now(ZoneId)` query a clock (default or given zone) and then **drop** the zone from the stored value. `plusMinutes` / `plusHours` / `plusNanos` return a new object; `this` is unchanged. `isAfter` / `isBefore` / `equals` compare the civil date-time (`==` is the wrong tool — value-based).

Dump methods: `plusMinutes`, `plusHours`, `isAfter` exist. **`toSecondOfDay` is not on `LocalDateTime`.**

```d2
direction: down
ldt: "LocalDateTime\nISO date + time, no zone" {
  width: 280
  height: 55
  style.fill: "#e8f5e9"
}
ld: "LocalDate" {
  width: 160
  height: 40
  style.fill: "#fff8e1"
}
lt: "LocalTime" {
  width: 160
  height: 40
  style.fill: "#fff8e1"
}
zdt: "ZonedDateTime / OffsetDateTime" {
  width: 280
  height: 45
  style.fill: "#e3f2fd"
}

ldt -> ld: "toLocalDate"
ldt -> lt: "toLocalTime"
ldt -> zdt: "atZone / atOffset"
```

**Fig. 1.** Same civil fields, no zone. Attach a `ZoneId` only when you need an instant.

```java
import java.time.LocalDateTime;
import java.time.ZoneId;

class Demo {
    static void civil() {
        LocalDateTime t = LocalDateTime.of(2007, 12, 3, 10, 15, 30);
        t.plusHours(1).plusMinutes(5);
        t.isAfter(LocalDateTime.now());
        t.toLocalDate();
        t.toLocalTime();
        t.atZone(ZoneId.of("Europe/Paris"));
        // t.toSecondOfDay(); // not a LocalDateTime method
    }
}
```

**Listing 1.** `of` / `plus*` copies / `isAfter` / split / `atZone`. `now()` uses a clock; the result is still zoneless. `LocalDateTime::now` is a `Supplier` ([[How would you explain for what needed functional interface SupplierT BooleanSupplier DoubleSupplier IntSupplie]]).

> [!warning] No zone means no instant
> Two `LocalDateTime`s that look equal can be different UTC instants in different regions. DST gaps/overlaps appear only after `atZone`. `plusHours` does not apply zone rules — it just adds civil hours. Do not use `==`.

> [!warning] `toSecondOfDay` is the dump mixing types
> That method is not on this class. Mutating APIs do not exist: every `plus*` / `minus*` / `with*` returns a copy. Historical dates are ISO/proleptic Gregorian, which is the wrong calendar for many pre-modern timelines.

> [!tip] Interview answer
> **`LocalDateTime` is immutable ISO date+time, nanoseconds, no time-zone, Java 8 (`java.time`).** Combine `LocalDate` and `LocalTime`. Not an instant — use `ZonedDateTime` / `Instant` for that. `now()` reads a clock; `plusHours` returns a copy.
