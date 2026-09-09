<!--
reps: 0
priority: 0
-->
#Java/Time #SRS

# How do you get the next Tuesday with the Java 8 Date Time API

> [!abstract] Short answer
> **`date.with(TemporalAdjusters.next(DayOfWeek.TUESDAY))` — the adjuster jumps to the first Tuesday strictly after the date.** If the date itself is a Tuesday, `next` skips forward a week; `nextOrSame` keeps the same day. Adjusters work through `with(...)`, which returns a new immutable date.

## next vs nextOrSame

`TemporalAdjusters` is a factory of date-policy objects: `with(TemporalAdjuster)` applies one. The `next` contract: the first occurrence of the requested day-of-week **after** the date. `nextOrSame` returns the date unchanged when it already matches.

```java
LocalDate friday = LocalDate.of(2024, 3, 15);   // a Friday
LocalDate tuesday = LocalDate.of(2024, 3, 12);  // a Tuesday

System.out.println("next TUE from Fri = " + friday.with(TemporalAdjusters.next(DayOfWeek.TUESDAY)));
System.out.println("next TUE from TUE = " + tuesday.with(TemporalAdjusters.next(DayOfWeek.TUESDAY)));
```

**Listing 1.** Verified on JDK 21:

```java
next TUE from Fri = 2024-03-19
next TUE from TUE = 2024-03-19
```

**Listing 2.** From Friday the 15th the next Tuesday is the 19th; from a Tuesday itself, `next` still lands on the 19th — a week later. `nextOrSame` would have returned the 12th unchanged.

```d2
direction: right
d: "date.with(\nTemporalAdjusters.next(TUESDAY))" {
  width: 330
  height: 90
  style.fill: "#e3f2fd"
}
q1: "Already Tuesday?" {
  width: 220
  height: 70
  style.fill: "#fff3e0"
}
n: "next: +7 days\nnextOrSame: same date" {
  width: 280
  height: 80
  style.fill: "#fff3e0"
}
q2: "Otherwise:\nfirst Tuesday after" {
  width: 270
  height: 80
  style.fill: "#e8f5e9"
}
d -> q1
q1 -> n: "yes"
q1 -> q2: "no"
```

**Fig. 1.** The only branch in the contract is "what if the date already is a Tuesday".

## Where adjusters fit

`next` and `nextOrSame` are two of a family: `firstDayOfMonth()`, `lastDayOfMonth()`, `firstInMonth(DayOfWeek)`, and the ordinal ones like `dayOfWeekInMonth(2, DayOfWeek.SATURDAY)` — see [[How do you get the second Saturday of the current month with the Java 8 Date Time API]]. For weekday cycling beyond "next", `date.plusWeeks(1)` from [[How do you add a week month year or decade with the Java 8 Date Time API]] composes with adjusters: "next Tuesday plus two weeks" is `.with(next(TUESDAY)).plusWeeks(2)`. Custom rules implement `TemporalAdjuster` (`adjustInto`) rather than hand-rolling day arithmetic with conditionals.

> [!warning] The adjuster is not a query on "this week"
> Traps people fall into. First: `TemporalAdjusters.next(...)` is a **stateless policy applied by `with`** — calling it alone does nothing; the return value is the answer and the source date is untouched. Second, the Tuesday-from-Tuesday case is a real behavioral fork: a schedule builder that means "same day or later" but writes `next` silently moves same-day events a week out; `nextOrSame` is usually the business meaning. Third, adjusters do not know about zones or calendars beyond ISO: on a `ZonedDateTime` they shift the date part and keep the time and zone, which can interact surprisingly with DST boundaries — the arithmetic rules are in [[How would you explain java.time.ZonedDateTime]] and the plain-date model in [[How would you explain java.time.LocalDateTime]].

> [!tip] Interview answer
> **with(TemporalAdjusters.next(DayOfWeek.TUESDAY)) — a TemporalAdjuster applied through with(), returning a new immutable date. The contract: first Tuesday strictly after the date, and if the date already is a Tuesday, next moves a week ahead while nextOrSame stays. Same family covers firstDayOfMonth, dayOfWeekInMonth and friends, and custom rules just implement TemporalAdjuster.**

