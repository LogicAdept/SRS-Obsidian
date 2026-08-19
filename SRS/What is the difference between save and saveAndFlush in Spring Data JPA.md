<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/JPA #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

In Spring Data JPA, both save() and saveAndFlush() persist an entity. The difference is when changes are written to the database.

save() may delay the write until the transaction commits. saveAndFlush() writes immediately (flush the persistence context). Both return the saved entity. Dumps recommend save() for batch inserts or updates, and saveAndFlush() when you need the row visible in the database right away. Immediate flush is described as slightly slower.
> [!warning] Unverified traps from the dump
> - Flush is not the same as commit; a later rollback can still undo a flushed change.
> - save() still inserts or updates depending on whether the entity already has an id.
