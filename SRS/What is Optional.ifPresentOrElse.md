<!--
reps: 0
priority: 0
-->
#Java/Language/Optional #Java/Versions/9 #SRS

# What is `Optional.ifPresentOrElse`?

> [!abstract] Short answer
> **`ifPresentOrElse(consumer, runnable)` (Java 9) runs the `Consumer` when a value is present and the `Runnable` when empty.** Both branches are side effects: the method is `void`. Java 8 writes the same thing as `if (opt.isPresent()) { ... } else { ... }`.

## Two actions, still no return value

`void ifPresentOrElse(Consumer<? super T> action, Runnable emptyAction)` : if a value is present, perform `action` with that value; otherwise perform `emptyAction` ([[What is Optional]], [[What does Optional.ifPresent do]], [[What do isPresent and isEmpty do on Optional]]).

That is `ifPresent` plus an empty branch. It does not unwrap and does not produce a result you can `return` or assign. For a value, use `map` / `or` / `orElse` / `orElseThrow` ([[How does Optional.map work]], [[What does Optional.or do]], [[Why should you avoid calling get on an Optional]]).

`NullPointerException` is thrown only for the branch that actually runs: present + `null` consumer, or empty + `null` runnable. The unused argument may be `null` without throwing.

On Java 8 there is no `ifPresentOrElse`. The equivalent is `isPresent()` then `get()` in the `if`, and an `else` for empty — the empty path is obvious, but the present path still uses `get()`.

```d2
direction: down
call: "ifPresentOrElse(action, emptyAction)" {
  width: 340
  height: 50
  style.fill: "#e3f2fd"
}
present: "value present" {
  width: 220
  height: 45
  style.fill: "#e8f5e9"
}
empty: "empty" {
  width: 180
  height: 45
  style.fill: "#fff8e1"
}
run: "action.accept(value)" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}
npeA: "action == null\nNullPointerException" {
  width: 260
  height: 70
  style.fill: "#ffebee"
}
runE: "emptyAction.run()" {
  width: 240
  height: 50
  style.fill: "#fff8e1"
}
npeE: "emptyAction == null\nNullPointerException" {
  width: 280
  height: 70
  style.fill: "#ffebee"
}
call -> present
call -> empty
present -> run
present -> npeA
empty -> runE
empty -> npeE
```

**Fig. 1.** Exactly one branch runs. NPE applies to that branch’s callback, not to the unused one.

```java
import java.util.Optional;

class User {
    private final String name;

    User(String name) {
        this.name = name;
    }

    String getName() {
        return name;
    }
}

class Demo {
    static Optional<User> find(String id) {
        return "1".equals(id) ? Optional.of(new User("Ada")) : Optional.empty();
    }

    static void announce(String id) {
        find(id).ifPresentOrElse(
            user -> System.out.println("Found " + user.getName()),
            () -> System.out.println("No user found")
        );
    }

    static void java8Style(Optional<User> u) {
        if (u.isPresent()) {
            System.out.println("Found " + u.get().getName());
        } else {
            System.out.println("No user found");
        }
    }
}
```

**Listing 1.** `announce` is the Java 9 two-branch side effect. `java8Style` is the same control flow with `isPresent` / `get`. Neither method can return a `String`; that would be `map` / `orElse`.

> [!warning] Still `void` — not a functional `if` expression
> You cannot `return` from the lambdas into the enclosing method in a way that makes `ifPresentOrElse` yield a value. Filling an outer mutable variable from both lambdas works but is the side-effect escape hatch. Prefer `orElse` / `orElseGet` / `or` when the result is data.

> [!warning] Java 9+, and NPE is branch-specific
> Java 8 has only `ifPresent` (no empty runnable) or a manual `if`. Empty + `null` `emptyAction` throws; empty + `null` consumer does not. Present is the reverse. That differs from combinators that `requireNonNull` both arguments up front.

> [!tip] Interview answer
> **`ifPresentOrElse` (Java 9) runs a consumer if the value is there and a runnable if empty.** It is `void`, so it is if/else for side effects, not for computing a return value. On Java 8 you write `if (isPresent())` / `else`; a `null` callback throws only on the branch that runs.
