<!--
reps: 0
priority: 0
-->
#Java/Time #SRS

# How do you add a week month year or decade with the Java 8 Date Time API

> [!abstract] Short answer
> **Use the typed `plus` methods — `plusWeeks(1)`, `plusMonths(1)`, `plusYears(1)` — and `plus(1, ChronoUnit.DECADES)` for a decade.** Each returns a new immutable object; nothing mutates. Months and years clamp intelligently at month ends (January 31 plus one month is February 29 in a leap year, not March 2).

## The plus family

`LocalDate`, `LocalDateTime`, `ZonedDateTime` all expose the same plus/minus API. For a decade there is no `plusDecades` method — you go through the generic form `plus(long, TemporalUnit)` with `ChronoUnit.DECADES`.

```java
LocalDate today = LocalDate.of(2024, 3, 15);
System.out.println("plusWeeks(1)     = " + today.plusWeeks(1));
System.out.println("plusMonths(1)    = " + today.plusMonths(1));
System.out.println("plusYears(1)     = " + today.plusYears(1));
System.out.println("plus(1, DECADES) = " + today.plus(1, ChronoUnit.DECADES));
```

**Listing 1.** Run on JDK 21:

```java
plusWeeks(1)     = 2024-03-22
plusMonths(1)    = 2024-04-15
plusYears(1)     = 2025-03-15
plus(1, DECADES) = 2034-03-15
```

**Listing 2.** Weeks add 7 days; months add a calendar month (same day-of-month); years add a calendar year; a decade is ten years via the generic `TemporalUnit` form.

```d2
direction: right
in: "LocalDate\n(immutable)" {
  width: 220
  height: 80
  style.fill: "#e3f2fd"
}
plus: "plusWeeks / plusMonths /\nplusYears / plus(n, ChronoUnit)" {
  width: 340
  height: 90
  style.fill: "#fff3e0"
}
out: "New copy\noriginal untouched" {
  width: 240
  height: 80
  style.fill: "#e8f5e9"
}
in -> plus -> out
```

**Fig. 1.** Every plus/minus is a factory: same type out, source value unchanged — chainable like `today.plusMonths(1).plusDays(3)`.

## The month-end clamp is the detail they probe

Calendar-month arithmetic keeps the day-of-month when it exists and clamps when it does not:

```java
LocalDate jan31 = LocalDate.of(2024, Month.JANUARY, 31);
System.out.println("Jan31 +1 month = " + jan31.plusMonths(1));
```

**Listing 3.** Verified on JDK 21:

```java
Jan31 +1 month = 2024-02-29
```

**Listing 4.** 2024 is a leap year, so January 31 plus one month lands on February 29 — the API adds a calendar month, not 30 or 31 days.

> [!warning] plusMonths is not plusDays(30), and the result is a throwaway unless you keep it
> Two traps. First, confusing calendar arithmetic with duration arithmetic: `plusMonths(1)` can move the date by 28, 29, 30, or 31 actual days — if a business rule means "add 30 days", write `plusDays(30)`, not `plusMonths(1)`. Second, the classic immutability bug: `date.plusMonths(1);` alone changes nothing — the returned copy must be assigned. For repeated date math in a loop, that silent no-op is a real production bug, not an interview riddle. Mixed-unit spans go through `Period` (`plus(Period.of(1, 2, 3))` for 1 year, 2 months, 3 days). The same copy semantics hold for time fields — see [[How would you explain java.time.LocalDateTime]] — and around zone arithmetic the story changes: [[How would you explain java.time.ZonedDateTime]].

> [!tip] Interview answer
> **plusWeeks, plusMonths, plusYears, and plus with a ChronoUnit for anything else — plus(1, ChronoUnit.DECADES) for a decade. Everything returns a new immutable date, so you must assign the result. Months are calendar months with a month-end clamp: Jan 31 plus one month is Feb 29 in a leap year, not an exception and not March 2. If the rule is duration-based, use plusDays instead.**

