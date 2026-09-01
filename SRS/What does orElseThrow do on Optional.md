<!--
reps: 0
priority: 0
-->
#Java/Language/Optional #Java/Exceptions/Unchecked #SRS

# What does `orElseThrow` do on `Optional`?

> [!abstract] Short answer
> **It returns the value if present; otherwise it throws.** `orElseThrow(supplier)` throws whatever the supplier produces. No-arg `orElseThrow()` (Java 10) throws `NoSuchElementException`. Prefer it over `get()`: same empty-case failure, but the name says the throw is deliberate. The supplier form can throw a domain type.

## Present value, or a chosen throwable

`Optional` is empty or holds a non-null value ([[What is Optional]], [[What are Optional.ofNullable and Optional.empty]], [[Why should a method that returns Optional never return null]]). `orElseThrow` is an accessor:

- If a value is present, it returns that value.
- If empty, no-arg `orElseThrow()` throws `NoSuchElementException` (`RuntimeException`, unchecked).
- `orElseThrow(Supplier)` throws the exception from `supplier.get()`. A method reference to a no-arg constructor is the documented style: `IllegalStateException::new`.

`Optional.get()` also throws `NoSuchElementException` on empty. The API’s preferred alternative is `orElseThrow()` ([[Why should you avoid calling get on an Optional]], [[What is Optional]]).

```d2
direction: down
o: "Optional" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
ok: "value present\nreturn it" {
  width: 260
  height: 60
  style.fill: "#e8f5e9"
}
nsee: "orElseThrow()\nNoSuchElementException" {
  width: 300
  height: 70
  style.fill: "#ffebee"
}
dom: "orElseThrow(supplier)\nsupplier's exception" {
  width: 300
  height: 70
  style.fill: "#fff8e1"
}
o -> ok
o -> nsee
o -> dom
```

**Fig. 1.** Empty `Optional` never returns `null` from `orElseThrow`; it throws.

```java
import java.io.IOException;
import java.util.Optional;

class Demo {
    static String must(Optional<String> o) {
        return o.orElseThrow();
    }

    static String domain(Optional<String> o) {
        return o.orElseThrow(IllegalStateException::new);
    }

    static String checked(Optional<String> o) throws IOException {
        return o.orElseThrow(IOException::new);
    }
}
```

**Listing 1.** `must` and `domain` need no `throws` (`NoSuchElementException` / `IllegalStateException` are unchecked). `checked` must declare `IOException` because that is what the supplier throws ([[Must you declare RuntimeException in a throws clause]], [[How would you explain the throws clause for checked exceptions]]). `Optional.of(null)` is a different failure (`NPE` at `of`, not `orElseThrow`) ([[What happens when you pass null to Optional.of]]).

If the `Optional` is empty and the supplier is `null` or returns `null`, `orElseThrow(Supplier)` throws `NullPointerException`.

> [!warning] No-arg `orElseThrow()` is Java 10
> Older dumps only show the supplier overload (Java 8). `get()` and no-arg `orElseThrow()` both throw `NoSuchElementException`; interviews still prefer `orElseThrow` as the readable “I accept a throw” form.

> [!warning] The supplier type is the `throws` of the call
> `orElseThrow(IOException::new)` is a checked throw. Treating `orElseThrow` as “always unchecked” is wrong. Empty-check with `isPresent` / `orElse` if you must not throw ([[What do isPresent and isEmpty do on Optional]]).

> [!tip] Interview answer
> **`orElseThrow` returns the value or throws: no-arg throws `NoSuchElementException`, the supplier form throws your exception.** Prefer it to `get()`. A checked type from the supplier still needs `catch` or `throws`.
