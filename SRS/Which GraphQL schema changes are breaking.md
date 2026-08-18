<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Safe (dump lists): add a type, field, or enum value; add a nullable field or optional argument with a default.

Breaking: remove or rename a field/type/enum still in use; change a field's type (String to Int, or nullability the wrong way); add a required (non-null, no default) argument.

Making an existing nullable **output** field non-null is often called fine; tightening an **input**/argument to non-null is breaking. Deprecate first; some teams run schema checks against real query traffic.

> [!warning] Unverified traps from the dump
> - Dump claim: output `!` added later is treated as safer than input `!` added later — verify before treating as gospel.
