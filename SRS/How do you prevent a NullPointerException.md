<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Unchecked #SRS

# How do you prevent a `NullPointerException`?

> [!abstract] Short answer
> **Never use `null` where an object is required.** Fail fast on illegal arguments with `Objects.requireNonNull`, keep “maybe absent” in `Optional` or an explicit check, invoke instance members only on a proven non-null receiver, and do not unbox a wrapper until it is non-null. Treat NPE as a programming error to fix, not as something every method should catch.

## NPE means a `null` was used as an object

`NullPointerException` is an unchecked `RuntimeException` thrown when code uses `null` as if it were an object: calling an instance method, reading or writing a field, using array length or an array slot, or throwing `null` ([[What is NullPointerException]]). Prevention is making those uses impossible, not wrapping every call in `catch` ([[Can you catch an unchecked exception in Java]]).

```d2
direction: down
use: "method / field / array / unbox / throw" {
  width: 320
  height: 50
  style.fill: "#e3f2fd"
}
npe: "null receiver or null wrapper\nNullPointerException" {
  width: 300
  height: 70
  style.fill: "#ffebee"
}
ok: "requireNonNull, Optional,\nnon-null equals receiver, no raw unbox" {
  width: 360
  height: 70
  style.fill: "#e8f5e9"
}
use -> npe
use -> ok
```

**Fig. 1.** The JVM throws NPE at the use of `null`. Guards belong before that use.

**Fail fast at the boundary.** `Objects.requireNonNull(arg)` (optionally with a message) returns the argument if it is non-null and throws NPE otherwise. That documents a required parameter and fails in the callee, not later on a field access ([[What does Objects.requireNonNull do]], [[Should you throw NullPointerException or IllegalArgumentException for a null argument]]).

**Represent absence.** A method that might not have a result can return `Optional` (`ofNullable` / `empty`) instead of `null`, and must not return a null `Optional` ([[What is Optional]], [[What are Optional.ofNullable and Optional.empty]], [[Why should a method that returns Optional never return null]]).

**Keep a non-null receiver.** `"expected".equals(s)` and `Objects.equals(s, "expected")` do not call an instance method on `s` when `s` is `null`. `s.equals("expected")` does ([[How would you explain someObj.equals(null)]], [[What is wrong with null and how do you avoid it]]).

**Do not unbox a `null` wrapper.** `int n = map.get(key)` throws if `get` returned `null`. Check the wrapper, use `getOrDefault` only when a stored `null` cannot occur, or coalesce with `Objects.requireNonNullElse` ([[How do you avoid NullPointerException when unboxing a Map value]], [[What is unboxing]]).

```java
import java.util.Map;
import java.util.Objects;
import java.util.Optional;

class Demo {
    static void greet(String name) {
        Objects.requireNonNull(name, "name");
        System.out.println(name.length());
    }

    static Optional<String> find(String id) {
        return Optional.empty();
    }

    static boolean isFoo(String s) {
        return "foo".equals(s);
    }

    static int count(Map<String, Integer> counts) {
        return Objects.requireNonNullElse(counts.get("n"), 0);
    }
}
```

**Listing 1.** Boundary check, empty `Optional`, non-null `equals` receiver, and a coalesced map value. None of these catch NPE.

> [!warning] `Optional.get()` is not a null-check
> Calling `get()` on an empty `Optional` throws `NoSuchElementException`, not NPE. You have swapped one crash for another. Use `orElse`, `orElseThrow`, or `ifPresent` ([[Why should you avoid calling get on an Optional]]).

> [!warning] Catching NPE does not prevent it
> A method-level `catch (NullPointerException e)` hides the defect and still crashes if you rethrow. Fix the null use. Unboxing a null `Integer` (including a missing map value, and a ternary that unboxes both arms) still throws NPE even when you “checked” something else ([[What happens when a ternary operator unboxes a null Integer in Java]]).

> [!tip] Interview answer
> **Prevent NPE by not using null as an object: `requireNonNull` at APIs, `Optional` or explicit checks for absence, a non-null receiver for `equals`, and no unboxing of a null wrapper.** Do not catch NPE in every method. `Optional.get()` on empty is a different exception, not a fix.
