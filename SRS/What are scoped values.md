<!--
reps: 0
priority: 0
-->
#Java/Versions/25 #SRS

# What are scoped values

> [!abstract] Short answer
> **Scoped values (JEP 506, final in Java 25; incubated in 20, previewed 21–24) are the immutable, bounded-lifetime replacement for ThreadLocal context sharing: `ScopedValue.where(KEY, value).run(runnable)` binds KEY to value only for the dynamic extent of run, and child tasks created inside inherit the binding — designed for millions of virtual threads.**

## The model and the ThreadLocal contrast

A binding lives exactly as long as the `run`/`call` executes: after it returns, `isBound()` is false and `orElse` supplies a default. Values are effectively immutable (you can create a nested rebinding with `where` inside the extent), there is no `set` to forget to remove, and no unbounded lifetime leaking through pooled thread reuse. Inheritance is structural: code spawned via structured concurrency inside the extent sees the binding without copying maps per thread — where `InheritableThreadLocal` copies on thread creation and ThreadLocal in a virtual-thread-per-request server multiplies lookups and memory ([[How would you explain Virtual Threads]], [[How would you explain Structured Concurrency]]).

```java
import java.lang.ScopedValue;

public class V51_ScopedValues {
    static final ScopedValue<String> USER = ScopedValue.newInstance(); // preview 21 (446), final 25 (506)

    public static void main(String[] args) {
        System.out.println("before: bound=" + USER.isBound());
        ScopedValue.where(USER, "ada").run(() -> {
            System.out.println("inside: " + USER.get() + " bound=" + USER.isBound());
        });
        System.out.println("after: bound=" + USER.isBound() + " get-orElse=" + USER.orElse("nobody"));
    }
}
```

**Listing 1.** Verified on JDK 21 with `--enable-preview` (V51_ScopedValues in empirics): `before: bound=false`, `inside: ada bound=true`, `after: bound=false get-orElse=nobody` (out/V51_ScopedValues.txt) — the binding exists exactly for the extent of `run`.

```d2
direction: right
outer: "outside run\nUSER unbound" { style.fill: "#ffebee"; width: 180; height: 80 }
run: "ScopedValue.where(USER, ada).run(...)\nUSER bound to ada" { style.fill: "#e8f5e9"; width: 380; height: 80 }
child: "child tasks spawned here\ninherit the binding" { style.fill: "#e3f2fd"; width: 300; height: 80 }
outer -> run -> child: ""
```

**Fig. 1.** Binding lifetime follows the dynamic extent: bound inside `run` and its children, unbound before and after.

> [!warning] ScopedValue is not a drop-in ThreadLocal
> There is no `set()`: to change a value you nest a rebinding, so code that mutates context mid-execution needs restructuring, not renaming. Sharing outside a structured scope is not supported — unstructured `Thread.start()` inside the extent does not get the binding guarantee. And on pre-25 JDKs this is preview/incubator only ([[What was new in Java 20]] has the incubator origins).

> [!tip] Interview answer
> **Scoped values, final in 25 after incubator in 20 and previews from 21, share immutable context with a bounded lifetime: where(KEY, value).run gives the binding only inside that extent, children inherit it structurally. Versus ThreadLocal: no set to forget, no leaks across pooled threads, no per-thread copying — built for virtual-thread-per-request servers.**
