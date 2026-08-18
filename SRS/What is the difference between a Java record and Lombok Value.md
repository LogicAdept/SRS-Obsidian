<!--
reps: 0
priority: 0
-->
#Java/Language/Records #Java/Library/Lombok #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

| Aspect | Java record | Lombok `@Value` / `@Data` |
| --- | --- | --- |
| Accessor style | `x()` | `getX()` (JavaBean) |
| Immutability | Enforced by compiler | `@Value` enforces, `@Data` does not |
| Inheritance | Cannot extend or be extended | Normal class inheritance |
| Extra instance fields | No | Yes |
| Build tool | JDK feature | Lombok + annotation processor |
| Customisation | Compact constructor | `@Builder`, `@NonNull`, etc. |

```java
@Value public class Point { int x; int y; }
point.getX();

record Point(int x, int y) {}
point.x();
```

Dumps: prefer records for new code on Java 16+; use Lombok when you need `getX()` for older bean-oriented tools, `@Builder`, or mutable builders. Records do not “replace Lombok” wholesale.

> [!warning] Unverified traps from the dump
> - `@Data` is not the same as a record: dumps say it does not enforce immutability.
> - A dump red flag: “Record is just syntactic sugar for Lombok.”
