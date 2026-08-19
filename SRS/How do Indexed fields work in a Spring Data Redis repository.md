<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/Redis #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Redis does not natively query by field. @Indexed creates a Redis Set per field value that maps to entity ids, so findByUserId() works.

Example: for @Indexed String userId, Redis stores a Set at sessions:userId:user:1001 containing session ids for that user.

Trade-off: extra writes to maintain index sets. Indexes are not automatically cleaned when a key expires by TTL.
> [!warning] Unverified traps from the dump
> - TTL expiry of the hash does not reliably drop the secondary index sets in this dump.
> - @Indexed is write overhead, not a free index like a relational DB.
