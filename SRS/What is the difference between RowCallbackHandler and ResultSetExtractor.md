<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/DataAccess #Java/JDBC #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Climb: `RowCallbackHandler` is for processing each `ResultSet` row one at a time. `ResultSetExtractor` is for processing the entire `ResultSet` at once.

Exam notes add: `ResultSetExtractor` returns a single assembled object and you loop `rs.next()` yourself; `RowCallbackHandler.processRow` returns void and is useful when you stream or side-effect per row without storing a list.

> [!warning] Unverified traps from the dump
> - `RowMapper` is the third callback: one object per row, collected into a list by `query`. Do not collapse all three into one interface.

