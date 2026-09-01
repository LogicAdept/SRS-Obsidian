<!--
reps: 0
priority: 0
-->
#Java/Language/Optional #SRS

# What does `Optional.ifPresent` do?

> [!abstract] Short answer
> **If a value is present, `ifPresent` runs the `Consumer` with that value; if empty, it does nothing.** The method is `void` — it is a side-effect hook, not a transform. To return a value, use `map` / `orElse` / `orElseThrow`. For an empty-side action, use `ifPresentOrElse` (Java 9).

## Run a consumer, or skip

`ifPresent` is a Java 8 instance method: `void ifPresent(Consumer<? super T> action)`. If a value is present, it performs the action with that value; otherwise it does nothing ([[What is Optional]], [[What do isPresent and isEmpty do on Optional]]).

That is the API’s replacement for `if (opt.isPresent()) { use(opt.get()); }` when the body is only a side effect (print, save, fire-and-forget). `get()` still throws `NoSuchElementException` if you get the branch wrong ([[Why should you avoid calling get on an Optional]]).

It does not unwrap into a return value. `map` produces another `Optional`; `orElse` / `orElseGet` / `orElseThrow` produce a `T` ([[How does Optional.map work]], [[What does orElseThrow do on Optional]]). `ifPresent` produces nothing you can assign.

`ifPresentOrElse(action, emptyAction)` (Java 9) is the two-branch form: the consumer if present, a `Runnable` if empty ([[What is Optional.ifPresentOrElse]]).

A `null` action throws `NullPointerException` **only when a value is present**. On an empty `Optional`, a `null` consumer is ignored — unlike `map` / `filter`, which require a non-null function even when empty.

```d2
direction: down
call: "optional.ifPresent(action)" {
  width: 300
  height: 50
  style.fill: "#e3f2fd"
}
present: "value present" {
  width: 240
  height: 45
  style.fill: "#e8f5e9"
}
empty: "empty" {
  width: 200
  height: 45
  style.fill: "#fff8e1"
}
run: "action.accept(value)" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}
npe: "action == null\nNullPointerException" {
  width: 280
  height: 70
  style.fill: "#ffebee"
}
skip: "do nothing" {
  width: 200
  height: 45
  style.fill: "#fff8e1"
}
call -> present
call -> empty
present -> run
present -> npe
empty -> skip
```

**Fig. 1.** Empty skips the consumer, even if the consumer is `null`. Present plus `null` action is `NullPointerException`.

```java
import java.util.Optional;

class Demo {
    static void printIfPresent(Optional<String> u) {
        u.ifPresent(System.out::println);
    }

    static void dumpStyle(Optional<String> u) {
        if (u.isPresent()) {
            System.out.println(u.get());
        }
    }

    static String label(Optional<String> u) {
        return u.orElse("missing");
    }
}
```

**Listing 1.** `printIfPresent` and `dumpStyle` both print a present value and skip empty. `label` cannot be written with `ifPresent` because `ifPresent` is `void`; `orElse` returns `String`. `Optional.empty().ifPresent(null)` does nothing; `Optional.of("x").ifPresent(null)` throws.

> [!warning] `ifPresent` cannot return a result
> A lambda in `ifPresent` is a `Consumer`: no useful return, assignment from `ifPresent(...)` does not compile. Compute with `map` / `flatMap` / `orElse` / `orElseGet`. Using `ifPresent` to fill an outer mutable variable is the “for side effects only” escape hatch, not the pipeline.

> [!warning] Null consumer is not always NPE
> Interviews assume every Optional combinator `requireNonNull`s the function first. `ifPresent` does not: empty + `null` action is a no-op. Present + `null` action is `NullPointerException`.

> [!tip] Interview answer
> **`ifPresent` runs a `Consumer` when a value is there and does nothing when empty.** It is `void`, so do not use it to compute a return value — that is `map` or `orElse`. For an empty branch, use `ifPresentOrElse` (Java 9) instead of `isPresent` then `get`.
