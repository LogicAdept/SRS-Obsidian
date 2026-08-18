<!--
reps: 0
priority: 0
-->
#Java/Language/Records #Java/Immutability #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: every record component field is `private final`. You cannot reassign the field after construction.

```java
public record User(String name, int age) {}
User user = new User("John", 25);
// user.name = "Jane";  // compile error
user = new User("Jane", 25);  // rebind the variable
```

`final` on the header is redundant: `record Point(final int x, final int y)` is the same as without `final`.

Shallow immutability: if a component type is mutable (`List`, array, `Date`), the object it refers to can still be mutated.

```java
record Scores(List<Integer> values) {}
Scores s = new Scores(new ArrayList<>(List.of(1, 2, 3)));
s.values().add(99);  // legal — mutates the list
```

Dump fix: defensive copy in the compact constructor, e.g. `values = List.copyOf(values)` or `Collections.unmodifiableList`.

> [!warning] Unverified traps from the dump
> - `final` freezes the reference, not the contents of a `List` or array.
> - A mutable component also makes a record a risky `HashMap` key if that state later changes.
