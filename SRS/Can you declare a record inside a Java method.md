<!--
reps: 0
priority: 0
-->
#Java/Language/Records #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Yes. Local records (Java 16+) can be declared inside a method, like local classes. Dumps use them as named pipeline holders.

```java
List<String> topEmails(List<User> users) {
    record Ranked(User user, int score) {}

    return users.stream()
        .map(u -> new Ranked(u, computeScore(u)))
        .sorted(Comparator.comparingInt(Ranked::score).reversed())
        .limit(10)
        .map(r -> r.user().email())
        .toList();
}
```

Local records are implicitly `static` (they do not capture enclosing-instance state).

> [!warning] Unverified traps from the dump
> - Implicitly static means no hidden enclosing-instance field on the local record.
> - Dump places local records in Java 16+, same as standard records.
