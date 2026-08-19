<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/MongoDB #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Reuse a single MongoClient / connection pool via Spring auto-configuration; do not create a client per request.

Define indexes explicitly (@Indexed or migration scripts) rather than relying on auto-index-creation in production.

Use DTOs or projections to avoid over-fetching large documents.

Enable retryable writes/reads; set connectTimeoutMS and socketTimeoutMS; use write concern majority for critical writes.

Monitor with the Spring Boot Actuator MongoDB health indicator plus Atlas or Ops Manager metrics.

Example URI dump: mongodb+srv://.../db?retryWrites=true&w=majority with management.health.mongo.enabled=true.
> [!warning] Unverified traps from the dump
> - Auto-creating indexes at startup is a mapping convenience and a production smell in the same dumps.
> - A single shared client is required for pooling; new MongoClient per request is the anti-pattern.
