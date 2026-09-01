<!--
reps: 0
priority: 0
-->
#Java/Language/Optional/Usage #Java/Performance #SRS

# What is the performance cost of `Optional`?

> [!abstract] Short answer
> **Today `Optional` is a heap object: a value-based *identity* class with a reference field, so a present value is typically an extra allocation and an extra pointer hop.** That is acceptable as a method return. It is the wrong per-element or hot-loop structure. `empty()` / `ofNullable(null)` reuse a shared empty instance; the JIT may also elide a short-lived `Optional` that does not escape.

## A wrapper object, not a primitive

`Optional` is documented as a value-based class whose job is a **method return type**, not a field you store everywhere ([[What is Optional]], [[Why should you not use Optional as a field or method parameter]]). Until it is migrated to a true value class, it still has object identity, so the runtime represents a live instance like other identity objects: object header plus a pointer to the payload (or `null` inside the box for empty). Identity objects usually live on the heap, except when inlining and escape analysis can prove the wrapper does not escape.

Factories match that picture:

- `of(x)` / present `ofNullable(x)` do `new Optional<>(x)` — a new object unless the JIT scalarizes it away.
- `empty()` and `ofNullable(null)` return the shared empty instance — no per-call `new`.
- `map` / `filter` on an already-empty box return empty without allocating a second wrapper ([[How does Optional.map work]], [[What are Optional.ofNullable and Optional.empty]]).

Returning `Optional` from `find(id)` is the intended use: one wrapper per call, unpacked by the caller. Putting `Optional` in a field, an array, or a tight loop (`Optional.of(i)` millions of times) repeats header + indirection for every element. That is the cost Valhalla’s value-class work is designed to shrink for returns and locals (stack flattening of wrappers like `Optional`); it is not the default layout of `Optional` on current HotSpot without that migration.

`Optional<Integer>` pays **two** objects: the `Integer` box and the `Optional`. `OptionalInt` / `OptionalLong` / `OptionalDouble` still wrap a primitive in an object today, but they skip the `Integer`/`Long`/`Double` box ([[What are OptionalInt OptionalLong and OptionalDouble]]).

```d2
direction: down
of: "Optional.of(x)" {
  width: 240
  height: 50
  style.fill: "#ffebee"
}
heap: "new Optional + header\n+ pointer to x" {
  width: 280
  height: 70
  style.fill: "#ffebee"
}
emp: "empty() / ofNullable(null)" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
shared: "shared empty instance" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}
ret: "return from find(id)" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}
of -> heap
emp -> shared
ret -> of
```

**Fig. 1.** A present `Optional` is a new identity object in the unoptimized case. Empty is cheap. A single return is the documented use.

```java
import java.util.Optional;
import java.util.OptionalInt;

class User {
    final String id;

    User(String id) {
        this.id = id;
    }
}

class Demo {
    static Optional<User> find(String id) {
        return Optional.of(new User(id));
    }

    static int dumpLoop() {
        int s = 0;
        for (int i = 0; i < 10_000_000; i++) {
            s += Optional.of(i).map(x -> x + 1).get();
        }
        return s;
    }

    static int plusOne(int i) {
        return OptionalInt.of(i).orElseThrow() + 1;
    }
}
```

**Listing 1.** `find` is the cheap-enough return. `dumpLoop` boxes each `int` to `Integer`, allocates `Optional`, maps (another box), then `get()` — allocation plus the `get()` smell ([[Why should you avoid calling get on an Optional]]). `plusOne` still wraps, but it does not create an `Integer`. For a hot `int`, a bare `i + 1` is cheaper than either optional.

> [!warning] Not “always a GC bomb,” and not free
> Escape analysis can delete a wrapper that never escapes. `empty()` is not a `new`. Claiming “Optional is free” or “Optional is always catastrophic” are both wrong. Measure the hot path; do not sprinkle `Optional.of` inside an inner loop “for safety.”

> [!warning] `Optional.of(i)` in a loop is `Optional<Integer>`
> Autoboxing is a second allocation. Primitive optionals avoid that box, not the wrapper object itself. The dump loop’s `.get()` is a separate defect: empty would throw `NoSuchElementException`.

> [!tip] Interview answer
> **`Optional` is a small heap object around the value: extra allocation and indirection unless the JIT elides it or you hit the shared empty instance.** Use it as a return type, not as a per-element structure on a hot path. For primitives prefer `OptionalInt` and friends over `Optional<Integer>`, or skip the wrapper entirely in a tight loop.
