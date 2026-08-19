<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Cache #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Put SpEL in `key`. Examples: `key = "#isbn"`, `key = "#author.name + #genre"`, `key = "#id"`. Dumps also show `#p0` / `#a0`, `#root.method.name`, `#root.args[0]`. `#result` is for `unless`, not for `key` on the way in.

> [!warning] Unverified traps from the dump
> - Dynamic cache *name* via `value = 

