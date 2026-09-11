<!--
reps: 0
priority: 0
-->
#Java/Versions/8 #Java/Time #SRS

# What is the java.time API and why did it replace Date and Calendar

> [!abstract] Short answer
> **`java.time` (JSR-310, Java 8) is the immutable, thread-safe date-time API built from the Joda-Time design: `LocalDate`/`LocalTime`/`LocalDateTime` for civil time, `Instant` for a machine timeline point, `ZonedDateTime`/`OffsetDateTime` when a zone or offset matters, `Period`/`Duration` for amounts, and `DateTimeFormatter` for parsing.** It replaced `Date` and `Calendar` because they were mutable, badly typed (0-based months, year-minus-1900), zone-confused, and thread-hostile (`SimpleDateFormat`).

## The model

Every type is immutable, so instances are shareable across threads and `plus*`/`with*` return copies. The split is deliberate: **civil vs timeline**. `LocalDateTime` is a wall-clock reading with no zone — it cannot identify an instant until you attach one (`atZone`) ([[What is LocalDateTime]]). `Instant` is seconds/nanos since the epoch — the right type for timestamps and persistence. `ZonedDateTime` attaches a full IANA zone (rules, DST), `OffsetDateTime` a fixed UTC offset — different tools: DST-safe scheduling wants `ZonedDateTime`, wire formats want `OffsetDateTime` ([[What is ZonedDateTime]]). Amounts split too: `Period` is calendar-based (days/months), `Duration` is time-based (seconds/nanos).

`DateTimeFormatter` is immutable and thread-safe — the direct fix for `SimpleDateFormat`'s shared-instance corruption. The legacy types remain for interop: `Date.from(instant)` / `date.toInstant()` convert, but mixing them invites the old bugs back ([[What was new in Java 8 outside the language]]).

```d2
direction: down
civil: "Civil (wall clock)\nLocalDate / LocalTime / LocalDateTime" {
  width: 360
  height: 65
  style.fill: "#e3f2fd"
}
zone: "attach zone or offset" {
  width: 250
  height: 50
  style.fill: "#fff8e1"
}
tz: "ZonedDateTime (DST rules)\nOffsetDateTime (fixed offset)" {
  width: 340
  height: 65
  style.fill: "#e8f5e9"
}
inst: "Instant — one point on the UTC timeline" {
  width: 360
  height: 55
  style.fill: "#f3e5f5"
}
amt: "Amounts: Period (calendar) / Duration (time)\nFormat: DateTimeFormatter (immutable)" {
  width: 420
  height: 65
  style.fill: "#fff3e0"
}
civil -> zone
zone -> tz
tz -> inst: "toInstant()"
```

**Fig. 1.** Civil types are zoneless readings; zones turn them into instants. `Instant` is the timeline identity the legacy API faked with `Date`.

```java
import java.time.LocalDate;
import java.time.Month;
import java.util.Calendar;
import java.util.Date;

public class V10_JavaTime {
    public static void main(String[] args) {
        Date legacyDecember = new Date(2020 - 1900, 11, 25); // year minus 1900, month 0-based!
        Calendar cal = Calendar.getInstance();
        cal.set(2020, Calendar.DECEMBER, 25);
        LocalDate modern = LocalDate.of(2020, Month.DECEMBER, 25);

        System.out.println("new Date(2020-1900, 11, 25): " + legacyDecember);
        System.out.println("calendar.get(MONTH): " + cal.get(Calendar.MONTH));
        System.out.println("LocalDate.of(2020, DECEMBER, 25): " + modern);

        LocalDate copy = modern.plusDays(7);
        System.out.println("plusDays returns copy: " + copy + " original still " + modern);
    }
}
```

**Listing 1.** Verified on JDK 21 (V10_JavaTime in empirics): `new Date(2020-1900, 11, 25): Fri Dec 25 00:00:00 UTC 2020`, `calendar.get(MONTH): 11`, `LocalDate.of(2020, DECEMBER, 25): 2020-12-25`, `plusDays returns copy: 2021-01-01 original still 2020-12-25` — the 0-based-month trap and copy semantics in one run (out/V10_JavaTime.txt).

> [!warning] The legacy traps java.time exists to kill
> `new Date(y, m, d)` needs **year minus 1900** and **0-based month** — `11` is December; `Calendar.MONTH` returns `11` for December, which people read as November. `Date` is mutable and not thread-safe; `SimpleDateFormat` corrupts shared parse state under concurrency. `java.sql.Date`/`Timestamp` subclass `java.util.Date` and print misleading values. And `LocalDateTime` is **not** a timestamp: storing it "to be safe" loses the instant — persist `Instant` or `OffsetDateTime` when the moment matters ([[What is LocalDateTime]]).

> [!tip] Interview answer
> **java.time is the JSR-310, Joda-derived API: immutable, thread-safe, properly split — LocalDate/LocalDateTime for civil time, Instant for the timeline, ZonedDateTime for DST, Period vs Duration, immutable formatters.** It replaced Date/Calendar because they were mutable, 0-based-month legacy with a non-thread-safe formatter. I convert at the edges with toInstant/from and keep the rest in java.time.
