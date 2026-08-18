<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/LinkedHashMap #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: **yes, like `HashMap`.** One **null key** and **multiple null values**. A Map-overview dump repeats: this implementation **allows nulls like `HashMap`**.

> [!warning] Unverified traps from the dump
> - “Allows nulls like HashMap” is not the `TreeMap` story; those lists still forbid a null key under natural order.
> - The dump does not name `NullPointerException`; it only states the allowed nulls.
