<!--
reps: 0
priority: 0
-->
#Java/Time #SRS

# How do you get the second Saturday of the current month with the Java 8 Date Time API

> [!abstract] Short answer
> **`LocalDate.now().with(TemporalAdjusters.dayOfWeekInMonth(2, DayOfWeek.SATURDAY))` — the ordinal adjuster does it in one step.** The two-step idiom (first day of month, `nextOrSame(SATURDAY)` to find the first, then `next(SATURDAY)` to reach the second) gives the same answer; `dayOfWeekInMonth` is the declarative form and the one to name in an interview.

## One-step ordinal adjuster vs the chain

`dayOfWeekInMonth(ordinal, dayOfWeek)` returns the ordinal-th occurrence of that weekday inside the date's month. Ordinal 1 is the first occurrence; the count restarts every month.

```java
LocalDate today = LocalDate.of(2024, 3, 15); // March 2024: 1st=Fri, 2nd=Sat
LocalDate first = today.withDayOfMonth(1);

LocalDate chained = first.with(TemporalAdjusters.nextOrSame(DayOfWeek.SATURDAY))
                         .with(TemporalAdjusters.next(DayOfWeek.SATURDAY));
LocalDate ordinal = today.with(TemporalAdjusters.dayOfWeekInMonth(2, DayOfWeek.SATURDAY));

System.out.println("chain  = " + chained);
System.out.println("ordinal= " + ordinal);
```

**Listing 1.** Verified on JDK 21:

```java
chain  = 2024-03-09
ordinal= 2024-03-09
```

**Listing 2.** Both paths agree: the second Saturday of March 2024 is the 9th.

```d2
direction: right
a: "First Saturday\nfirst.with(nextOrSame(SAT))" {
  width: 300
  height: 90
  style.fill: "#e3f2fd"
}
b: "Second Saturday\n.next(SAT)" {
  width: 230
  height: 80
  style.fill: "#e3f2fd"
}
c: "dayOfWeekInMonth(2, SATURDAY)\none declarative step" {
  width: 330
  height: 90
  style.fill: "#e8f5e9"
}
a -> b
b -> c: "same result"
```

**Fig. 1.** The manual chain encodes the definition ("first occurrence, then one more"); the ordinal adjuster states the goal directly.

The javadoc wording for `dayOfWeekInMonth`: a new date "with the ordinal day-of-week based on the month" — ordinal 2, weekday Saturday. Negative ordinals count from the end (`-1` is the last Saturday of the month), which the chain approach handles awkwardly.

> [!warning] The chain silently breaks for ordinal 1 and the last week
> Two things to check before shipping either version. First, the chain `nextOrSame` → `next` hard-codes "second": adapting it to "third" means another `next` hop, and "first" means stopping early — the ordinal form just changes the number, so the chain is where copy-paste bugs live. Second, "second Saturday of the current month" is ambiguous if "current" is computed late: `LocalDate.now()` in one process can be the last day of the month and in another the first of the next — pin the month first (`withDayOfMonth(1)`) or inject a `Clock` so the month cannot drift between the two computation steps (the testability pattern from [[How do you get the current date with the Java 8 Date Time API]]). Related adjusters and arithmetic: [[How do you get the next Tuesday with the Java 8 Date Time API]], [[How do you add a week month year or decade with the Java 8 Date Time API]].

> [!tip] Interview answer
> **LocalDate.now().with(TemporalAdjusters.dayOfWeekInMonth(2, DayOfWeek.SATURDAY)) — the ordinal adjuster picks the second Saturday of the month in one step. The interview alternative is the chain: jump to the first of the month, nextOrSame(SATURDAY) for the first, next(SATURDAY) for the second — same result, more moving parts. Both return new immutable dates.**

