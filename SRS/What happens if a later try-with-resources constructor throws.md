<!--
reps: 0
priority: 0
-->
#Java/Exceptions/TryCatch/TryWithResources #SRS

# What happens if a later try-with-resources constructor throws?

> [!abstract] Short answer
> **Earlier resources still close; later ones are never created; the try body does not run.** Initialization is left to right. If a later initializer throws, every resource that already initialized to a non-null value is closed in reverse order, and that initializer exception is the primary throw. Failures from those `close()` calls are `addSuppressed` on it, not replacements.

## Init left-to-right; close what you already opened

Resources in `try (A a = …; B b = …)` initialize in source order. If `B`’s expression throws, `A` was already created, so `A` is still closed (if it is non-null). `B` is never assigned. The `try` block is skipped ([[What is try-with-resources]], [[How does the compiler translate try-with-resources]]).

Several resources compile as nested try-with-resources. The outer generated `finally` still closes `A` when the inner initializer fails. That is the case hand-written `try`/`finally` often got wrong: people closed `A` only after a successful `B` ([[What is the difference between try-with-resources and try-finally when both throw]]).

If closing an already-opened resource also throws, that close exception is suppressed on the **initializer** exception. The statement still completes abruptly because of the original `V` ([[What is a suppressed exception in try-with-resources]], [[What happens if close throws after a try-with-resources body succeeds]]). A resource whose initializer yielded `null` is not closed ([[What happens if a try-with-resources resource is null]]).

```d2
direction: down
a: "new A() succeeds" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
b: "new B() throws V" {
  width: 280
  height: 50
  style.fill: "#ffebee"
}
close: "close A (reverse order)" {
  width: 280
  height: 50
  style.fill: "#fff8e1"
}
skip: "try body never runs" {
  width: 280
  height: 50
  style.fill: "#eceff1"
}
a -> b
b -> close
b -> skip
```

**Fig. 1.** Failed later initializer: reverse-close earlier resources, propagate `V`.

```java
class Demo {
    static class R implements AutoCloseable {
        final String name;
        final boolean closeBoom;

        R(String name, boolean failInit, boolean closeBoom) {
            this.name = name;
            this.closeBoom = closeBoom;
            if (failInit) {
                throw new IllegalStateException("init " + name);
            }
        }

        @Override
        public void close() {
            if (closeBoom) {
                throw new RuntimeException("close " + name);
            }
        }
    }

    static void laterInitFails() {
        try (R a = new R("a", false, true); R b = new R("b", true, false)) {
            throw new AssertionError("unreachable");
        }
    }
}
```

**Listing 1.** `b`’s constructor throws `IllegalStateException`. `a.close()` then throws `RuntimeException`. The thrown object is the init failure; `close a` is suppressed on it. The body does not run.

> [!warning] Do not assume “constructor failed ⇒ nothing to close”
> Only **later** resources are uncreated. Everything to the left that initialized non-null is still closed. Forgetting that is the classic leak in nested manual `try`.

> [!warning] Close failures do not replace the initializer exception
> If `close` on `A` throws, you still see `B`’s constructor exception as the primary. Look at `getSuppressed()` for the close failure.

> [!tip] Interview answer
> **If a later try-with-resources initializer throws, earlier resources close in reverse order, the body is skipped, and that initializer exception propagates.** Close failures on those earlier resources are suppressed on it, not swapped in as the primary.
