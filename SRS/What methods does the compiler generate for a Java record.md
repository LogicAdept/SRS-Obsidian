<!--
reps: 0
priority: 0
-->
#Java/Language/Records #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

The identifiers in the record header are components. Dumps say the compiler generates five kinds of members:

- A `private final` field per component.
- A public accessor named after the component (`name()`, not `getName()`).
- A canonical constructor that takes all components in header order and assigns them.
- `equals()` and `hashCode()` over all components.
- `toString()` in the form `User[name=John, age=25]`.

```java
public record User(String name, int age) {}

User user = new User("John", 25);
user.name();
user.age();
user.equals(other);
user.hashCode();
user.toString();  // User[name=John, age=25]
```

Conceptual `equals` from dumps: identity check, then `instanceof`, then `Objects.equals` on reference components and `==` on primitives.

Conceptual `hashCode`: dumps disagree whether the compiler uses `Objects.hash(...)` or an inlined `31 * h + next` chain.

> [!warning] Unverified traps from the dump
> - There is no generated setter. Records are described as immutable by construction.
> - You can override `equals` / `hashCode` / `toString`; dumps say overriding only `equals` still breaks the HashMap contract.
> - hashCode is claimed not to be cached, because you cannot add an extra instance field to store it.
