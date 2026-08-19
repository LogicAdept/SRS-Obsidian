<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/MongoDB #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

MongoRepository is declarative, low-boilerplate CRUD and derived queries — for straightforward, predictable access.

MongoTemplate is programmatic: dynamic queries at runtime, complex aggregations, bulk operations, and options such as read preference and collation that are hard to express as a method name.

Dumps say real projects use both: repositories for simple cases, MongoTemplate injected for the rest. MongoRepository is described as a higher-level abstraction on top of MongoTemplate.
> [!warning] Unverified traps from the dump
> - You do not have to pick only one; mixing is the usual dump advice.
> - Aggregations and fully dynamic search forms are the Template side in these dumps.
