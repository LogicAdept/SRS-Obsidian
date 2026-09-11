<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Databases/SQL/DataTypes #SRS

# What is the difference between timestamp and timestamptz in PostgreSQL?

> [!abstract] Short answer
> Neither stores a time zone. `timestamp` (without time zone) stores the literal wall-clock fields you typed; `timestamptz` (with time zone) stores the instant — internally always UTC — and converts to the session's TimeZone on input and output. For anything that crosses time zones or DST boundaries, timestamptz is the correct type; both are 8 bytes with microsecond precision.

## The conversion behavior

On input to timestamptz, a literal with an offset is converted to UTC; without one, the session's TimeZone is assumed. On output the UTC instant renders in the session's time zone. timestamp just stores and returns the fields verbatim — the same value means different instants in different sessions.

```sql
SET timezone = 'Europe/Moscow';
SELECT '2026-06-01 12:00:00'::timestamptz;          -- 2026-06-01 12:00:00+03
SELECT '2026-06-01 12:00:00+00'::timestamptz;       -- 2026-06-01 15:00:00+03
SELECT '2026-06-01 12:00:00'::timestamp;            -- 2026-06-01 12:00:00 (no zone)
```

**Listing 1.** Same literal, three outcomes: timestamptz normalizes to an instant and renders per session; timestamp keeps the fields.

```d2
lit: "Input literal" {width: 200; height: 60}
tz: "timestamptz\ninstant, stored as UTC\nrendered per TimeZone" {width: 320; height: 90}
ts: "timestamp\nwall-clock fields only\nzone-agnostic" {width: 300; height: 90}
lit -> tz
lit -> ts
```

**Fig. 1.** One input, two contracts: an instant versus a set of clock fields.

## Practical consequences

- DST safety: arithmetic and comparisons on timestamptz follow real instants; timestamp arithmetic is naive wall-clock math that breaks across DST shifts.
- Scheduling "09:00 local" per user is a timestamp-shaped business rule; storing the event instant is timestamptz. Mixing them is the classic bug.
- Range types and exclusion constraints over time use timestamptz naturally ([[What is an exclusion constraint in PostgreSQL]]).
- Both range from 4713 BC to 294276 AD with 1 microsecond resolution; `now()` returns timestamptz (transaction start time).

> [!warning] timestamptz does not store your time zone
> The zone is not persisted — only the instant. If you must remember "this happened at 09:00 Moscow time", the zone itself is extra data: store timestamptz for the instant plus a zone column for the business rule. Believing the column remembers the original zone produces off-by-hours bugs for other sessions ([[What are IMMUTABLE STABLE and VOLATILE functions in PostgreSQL]] matters here too: functions like date_trunc on timestamptz depend on the session zone).

> [!tip] Interview answer
> Both are 8-byte microsecond values and neither stores a zone. timestamp keeps literal wall-clock fields; timestamptz converts input to UTC, stores the instant, and renders it per the session TimeZone. Any cross-zone or DST-sensitive system uses timestamptz, and keeps a separate zone column when the local time itself is business data.
