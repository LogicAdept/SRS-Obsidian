<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/MongoDB #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

MongoTemplate is the central helper for Spring Data MongoDB. It offers create, update, delete, and query operations and maps domain objects to documents.

It implements MongoOperations. Methods are named after the driver Collection API (find, findAndModify, insert, remove, save, update). You pass domain objects instead of raw Document, and you get fluent Query, Criteria, and Update APIs.

Dumps call it thread-safe and reusable, and the right tool for large or complex queries.
> [!warning] Unverified traps from the dump
> - Prefer the MongoOperations interface when injecting the template, according to the same dumps.
> - Repositories still sit on a mongoTemplate bean named mongoTemplate by default.
