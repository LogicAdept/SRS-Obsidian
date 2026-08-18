<!--
reps: 0
priority: 0
-->
#Java/Language/Wrappers #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps say wrapper classes convert primitives to objects (and back) because many Java APIs require objects.

Claimed reasons:

- Collections and generics store objects, not primitives (`List<Integer>`, not `List<int>`).
- Nullability: a wrapper field can be `null`; a primitive cannot.
- JavaBeans: properties are often wrappers so an unset value can be `null`.
- Utility methods on the class (`parseInt`, `toBinaryString`, `compareTo`, `Character.isDigit`).
- Serialization, synchronization, cloning, and `java.util` APIs that deal with objects.

```java
List<Integer> numbers = new ArrayList<>();
numbers.add(5);  // autoboxing
Integer age = null;  // valid; int age = null; does not compile
```

> [!warning] Unverified traps from the dump
> - One dump also claims wrapping a primitive lets a method change the caller’s value — that conflicts with immutable wrappers.
> - Need for wrappers is about the type system and APIs, not about making Java “fully OOP.”
