<!--
reps: 0
priority: 0
-->
#Java/Language/Optional #SRS

# How would you explain `orElse` / `orElseGet`?

> [!abstract] Short answer
> **`orElse(other)` returns the present value, otherwise `other`. `orElseGet(supplier)` returns the present value, otherwise `supplier.get()`.** Java evaluates the `orElse` argument before the method runs, so `orElse(load())` still calls `load()` on a present `Optional`. `orElseGet` calls the supplier only when empty. Use `orElse` for a cheap constant; use `orElseGet` when the fallback is work you must not do on the present path.

## Present `T`, or a substitute `T`

Both methods unwrap to `T` (Java 8). They do not stay in the box ([[What is Optional]], [[What are Optional.ofNullable and Optional.empty]]):

- `orElse(T other)` — if a value is present, return it; otherwise return `other`. `other` **may be `null`**.
- `orElseGet(Supplier<? extends T> supplier)` — if a value is present, return it; otherwise return `supplier.get()`. `NullPointerException` if the `Optional` is **empty** and `supplier` is `null`. A present value does not touch the supplier, so a `null` supplier on a present box does not throw.

The eagerness people quote is not extra work *inside* `orElse`. Method arguments are evaluated before the body runs. `opt.orElse(load())` always evaluates `load()`, then `orElse` only chooses which reference to return. `opt.orElseGet(Demo::load)` evaluates to a `Supplier`; `get()` runs only on the empty branch (`value != null ? value : supplier.get()`). A literal or an already-held variable in `orElse` is not a second computation.

`or(supplier)` (Java 9) is the same laziness but returns `Optional<T>`, so you can chain lookups and unwrap later ([[What does Optional.or do]]). `orElseThrow` unwraps or throws instead of substituting ([[What does orElseThrow do on Optional]], [[Why should you avoid calling get on an Optional]]).

```d2
direction: down
call: "unwrap to T" {
  width: 240
  height: 45
  style.fill: "#e3f2fd"
}
else: "orElse(other)\nother already evaluated" {
  width: 300
  height: 70
  style.fill: "#fff8e1"
}
get: "orElseGet(supplier)\nget() only if empty" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}
t: "T (may be null)" {
  width: 240
  height: 45
  style.fill: "#ffebee"
}
call -> else
call -> get
else -> t
get -> t
```

**Fig. 1.** Both yield `T`. The supplier is the delayed empty-path expression; the `orElse` argument is not.

```java
import java.util.Optional;
import java.util.concurrent.atomic.AtomicInteger;

class Demo {
    static final AtomicInteger loads = new AtomicInteger();

    static String load() {
        loads.incrementAndGet();
        return "fallback";
    }

    static String eager(Optional<String> o) {
        return o.orElse(load());
    }

    static String lazy(Optional<String> o) {
        return o.orElseGet(Demo::load);
    }

    static String cheap(Optional<String> o) {
        return o.orElse("unknown");
    }
}
```

**Listing 1.** `eager(Optional.of("x"))` still increments `loads`. `lazy(Optional.of("x"))` does not. `cheap` is the cheap-constant shape. `orElse(null)` compiles: empty then returns `null`. A supplier that returns `null` also unwraps to `null` — unlike `or`, there is no `requireNonNull` on that result.

> [!warning] `orElse(expensive())` is not a skipped default
> Presence does not skip the argument. `find(id).orElse(loadFromDb())` hits the database even when `find` returned a user. Put the call in `orElseGet(Demo::loadFromDb)` (or a lambda). `orElse("unknown")` is the form that needs no supplier.

> [!warning] Unwrapping can put `null` back
> `other` is documented as nullable. Empty `orElse(null)` and a supplier that returns `null` both yield `null`, so the next dereference is an NPE. That is allowed; it is no longer an `Optional`. Do not treat either method as “never null.”

> [!tip] Interview answer
> **`orElse` takes a ready `T`; that expression runs before the method, even if the Optional is present. `orElseGet` takes a `Supplier` and calls it only when empty.** Cheap constants go in `orElse`. Expensive or side-effecting fallbacks go in `orElseGet`. Both return `T`, not another `Optional`.
