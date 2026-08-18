<!--
reps: 0
priority: 0
-->
#Java/Language/Enum #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Use an enum when variants are structurally the same singletons (same fields). Use a sealed type when variants carry different data.

| | Enum | Sealed class |
| --- | --- | --- |
| Per-instance data | Same fields for all constants | Each subtype can have different fields |
| Extensibility | Closed at compile time | Closed via `permits` |
| Exhaustive switch | Yes | Yes (Java 21) |
| Polymorphic behaviour | Abstract / constant-specific methods | Subtype methods |

```java
enum Status { PENDING, ACTIVE, CLOSED }

sealed interface Event permits OrderPlaced, OrderShipped, OrderCancelled {}
record OrderPlaced(String orderId, Instant at) implements Event {}
```

> [!warning] Unverified traps from the dump
> - There is no `#Java/Language` child leaf yet for sealed types.
