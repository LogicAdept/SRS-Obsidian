<!--
reps: 0
priority: 0
-->
#Java/Time/ZonedDateTime #SRS

# How would you explain java.time.ZonedDateTime

> [!abstract] Short answer
> **`ZonedDateTime` is a date-time with a full time-zone attached (`2024-03-10T04:30-04:00[America/New_York]`): the civil local fields, the zone rules, and the resolved offset from UTC.** It is the type that answers "what wall clock reads there right now" and the one whose arithmetic respects DST — it lands where the zone rules say, even when the local time jumps an hour.

## Three views in one value

A `ZonedDateTime` carries the local date-time, the `ZoneId` (rules), and the resolved `ZoneOffset`. The offset is computed from the rules at that instant — which is why the same `LocalDateTime` can have two different offsets across a DST change.

```java
ZoneId ny = ZoneId.of("America/New_York");
ZonedDateTime before = ZonedDateTime.of(2024, 3, 10, 1, 30, 0, 0, ny);
System.out.println("zdt +2h = " + before.plusHours(2));
System.out.println("ldt +2h = " + before.toLocalDateTime().plusHours(2));
```

**Listing 1.** The US spring-forward night of 2024: 02:00 does not exist — clocks jump from 01:59:59 to 03:00. Run on JDK 21:

```java
zdt +2h = 2024-03-10T04:30-04:00[America/New_York]
ldt +2h = 2024-03-10T03:30
```

**Listing 2.** Zone-aware arithmetic added two real hours and the offset changed from `-05:00` to `-04:00`, so the wall clock reads 04:30 — three local hours later. The zone-less arithmetic walked straight through the missing hour and claims 03:30.

```d2
direction: down
a: "2024-03-10 01:30-05:00\nNew York (EST)" {
  width: 300
  height: 90
  style.fill: "#e3f2fd"
}
gap: "02:00 does not exist\n(spring forward)" {
  width: 280
  height: 80
  style.fill: "#ffebee"
}
b: "plusHours(2) on ZonedDateTime\n04:30-04:00 — offset re-resolved" {
  width: 350
  height: 90
  style.fill: "#e8f5e9"
}
c: "plusHours(2) on LocalDateTime\n03:30 — walked through the gap" {
  width: 350
  height: 90
  style.fill: "#ffebee"
}
a -> gap
a -> b
a -> c
```

**Fig. 1.** Same input, same operation name, two different answers: the zone is what re-resolves the offset after the gap.

## Where it belongs in a stack

Use `ZonedDateTime` at the edges where humans and zones meet: displaying a UTC instant to a user (`instant.atZone(userZone)`), scheduling in local time, converting between offices. Persistence usually prefers the pair `Instant` (moments — [[How do you get the current time in milliseconds with the Java 8 Date Time API]]) and `LocalDateTime` (civil fields — [[How would you explain java.time.LocalDateTime]]); `ZonedDateTime` is the view that joins them through `ZoneId`. Conversions are explicit both ways: `toInstant()` freezes it to a timeline point; `toLocalDateTime()` drops the zone.

> [!warning] The gap rules are subtle in BOTH directions — and offsets are not zones
> First, adding to a nonexistent local time is not an exception: `plusHours` re-resolves per rules, while `with` of an invalid local time shifts by the gap length; the same input can resolve differently for spring-forward versus fall-back (where one local hour happens twice and the offset decides). Rely on the demonstrated behavior — real hour arithmetic through `ZonedDateTime` — rather than assuming either answer. Second, a common lie: "ZonedDateTime equals LocalDateTime plus an offset string". An offset (`+03:00`) is a number; a zone (`Europe/Moscow`) is a rule set that can change (DST, law changes) — storing only the offset makes future instants unresolvable. Third, comparing: `isBefore`/`isAfter` compare the instant, `compareTo` too, so two `ZonedDateTime`s in different zones compare correctly even when their local clocks disagree.

> [!tip] Interview answer
> **ZonedDateTime is local date-time plus a real ZoneId and the offset resolved from its rules — it is how you present or schedule across zones. Its arithmetic is rule-aware: across a DST boundary plusHours(2) lands where the rules say and the offset changes, while LocalDateTime walks straight through a nonexistent hour. Convert with atZone and toInstant; store moments as Instant, and remember a zone is a rule set, not just an offset.**

