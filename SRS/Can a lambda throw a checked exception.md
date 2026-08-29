<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Checked #Java/Lambdas #SRS

# Can a lambda throw a checked exception?

> [!abstract] Short answer
> **Yes, but only through the target function type.** A lambda *expression* throws nothing when it is evaluated. The *body* may throw a checked exception `E` only if `E` is a subclass of some type named in the `throws` clause of that target function type. Catch-or-specify is against `Consumer.accept`, `Callable.call`, and so on — not against an enclosing `try` around the lambda literal.

## The body is checked; the expression is not

Evaluating `() -> { ... }` produces a functional-interface instance. The body is not run then, so the expression itself can throw no exception classes. Later, when the functional method is invoked, the body runs, and compile-time checking has already required that every checked type the body can throw is covered by that method's `throws`.

```d2
direction: down
expr: "lambda expression\nevaluates; throws nothing" {
  width: 300
  height: 70
  style.fill: "#e3f2fd"
}
body: "lambda body\ncan throw checked E" {
  width: 300
  height: 70
  style.fill: "#fff3e0"
}
ft: "target function type throws\n(from the SAM method)" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}
ok: "E is a subclass of some\ntype in that throws → compiles" {
  width: 300
  height: 80
  style.fill: "#f3e5f5"
}
body -> ft
ft -> ok
expr -> body: "body runs later"
```

**Fig. 1.** Exception checking uses the targeted function type, not the site that materializes the lambda. See [[What is functional interface]] and [[What happens if you neither catch nor declare a checked exception]].

Most `java.util.function` types declare **no** checked exceptions: `Consumer.accept(T)`, `Function.apply(T)`, and therefore `Iterable.forEach(Consumer)` (it just calls `action.accept(t)`). A body that can throw `IOException` is a compile-time error there unless you catch `IOException` **inside** the body.

```java
import java.io.IOException;
import java.util.List;

class Demo {
    static void load(String name) throws IOException {}

    static void printAll(List<String> names) {
        names.forEach(n -> {
            try {
                load(n);
            } catch (IOException e) {
                throw new IllegalStateException(e);
            }
        });
    }
}
```

**Listing 1.** `forEach` targets `Consumer`. Catch inside the lambda, or wrap in an unchecked type. `names.forEach(n -> load(n));` does not compile. See [[Which functional interface does Iterable forEach use]] and [[Does wrapping a checked exception in RuntimeException require a throws clause]].

## Target types that declare checked `throws`

`Callable.call()` is `V call() throws Exception`. A `Callable` lambda may throw `IOException` and other `Exception` subclasses. `Runnable.run()` declares no checked exceptions; the same body is illegal there. The platform API states the contrast: `Runnable` cannot throw a checked exception.

```java
import java.io.IOException;
import java.util.concurrent.Callable;

class Demo {
    static Callable<Integer> failing() {
        return () -> {
            throw new IOException("fail");
        };
    }

    static Runnable illegal() {
        return () -> {
            throw new IOException("fail"); // compile-time error
        };
    }
}
```

**Listing 2.** `Callable` allows the checked throw; `Runnable` does not.

A custom `@FunctionalInterface` whose single abstract method declares `throws IOException` (or `throws Exception`) is the same rule: the lambda body may throw that type or a subclass.

Unchecked types (`IllegalArgumentException`, `RuntimeException`, `Error`) never need to appear on the function type. They may be thrown from a `forEach` lambda with no `throws` anywhere.

> [!warning] An enclosing `try` does not license the body
> `try { list.forEach(p -> load(p)); } catch (IOException e) {}` still fails to compile. That `catch` would handle exceptions `forEach` itself throws. The lambda body is checked against `Consumer`, which names no checked type. Catch **inside** the lambda, change the target type, or wrap.

> [!warning] Wrapping is not a language exemption
> Catching `IOException` and throwing `RuntimeException` (or `UncheckedIOException`) is ordinary catch-or-specify *inside* the body. The compiler then sees only an unchecked throw. It is not a special Stream loophole, and it is not required — a `Callable` or a functional method that declares `throws Exception` can propagate the checked type instead.

> [!tip] Interview answer
> **A lambda expression throws nothing when it is created; the body is checked against the target functional method's `throws`. If that method declares no checked exceptions — `Consumer`, `Function`, `Runnable`, `Iterable.forEach` — the body cannot throw `IOException` unless you catch it inside or wrap it in an unchecked exception. Target `Callable` or a functional interface whose method declares `throws Exception`, and checked types are allowed.**
