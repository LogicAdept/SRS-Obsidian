<!--
reps: 0
priority: 0
-->
#Java/Language/Optional #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Use `flatMap` when the mapper itself returns `Optional`. `map` would yield `Optional<Optional<…>>`; `flatMap` flattens to one layer.

```java
Optional<Address> wrong = find(id).map(User::getAddress);     // Optional<Optional<Address>>
Optional<Address> ok    = find(id).flatMap(User::getAddress);

String zip = find(id)
    .flatMap(User::getAddress)
    .map(Address::getZip)
    .orElse("unknown");
```

Same `map` / `flatMap` idea as `Stream`.

> [!warning] Unverified traps from the dump
> - If `getAddress()` already returns `Optional`, `map` is the nested-wrapper bug interviewers want.
