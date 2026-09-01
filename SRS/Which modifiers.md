<!--
reps: 0
priority: 0
-->
#Java/Language/Modifiers #SRS

# Which modifiers?

> [!abstract] Short answer
> Java splits **access** (`public`, `protected`, package access with **no** keyword, `private`) from **other modifiers** that depend on the declaration: classes also take `abstract`, `static`, `final`, `sealed`, `non-sealed`; fields take `static`, `final`, `transient`, `volatile`; methods take `abstract`, `static`, `final`, `synchronized`, `native`. `default` is an **interface-method** modifier, not an access level. `strictfp` is **obsolete** and has no effect. Access: [[How do Java access modifiers work]]. `static` / `final` / `abstract`: [[What does the static keyword mean in Java]], [[What does the final keyword mean in Java]], [[How would you explain the abstract keyword in Java]].

## Access vs everything else

Exactly one access story per declaration: `public`, `protected`, `private`, or **omitted** (package access). There is no modifier named `default` for access. On interface members, omitting the keyword means **`public`**: [[How would you explain default modifiers for fields and methods inside interfaces]].

An overriding instance method may **widen** access, not narrow it.

## By declaration

| On | Other modifiers (besides access) |
| --- | --- |
| Class / interface | `abstract`, `static` (nested), `final`, `sealed`, `non-sealed`; `strictfp` allowed but inert |
| Field | `static`, `final`, `transient`, `volatile` |
| Method | `abstract`, `static`, `final`, `synchronized`, `native`; `strictfp` inert; interfaces also `default` |
| Constructor | **access only** — not `abstract`, `static`, `final`, `native`, `synchronized` |

**`abstract`** — incomplete class, or instance method with no body. [[Where and why is used modifier abstract]]

**`static`** — class-level field, method, or nested type.

**`final`** — no subclass, no override/hide, or no reassignment.

**`sealed` / `non-sealed`** — the class’s direct subclasses are listed (`permits`); a subclass of a sealed type must be `final`, `sealed`, or `non-sealed`.

**`transient`** — skip the field in default serialization. [[How would you explain the transient field modifier in Java]]

**`volatile`** — reads and writes of **that variable** are visible across threads with defined ordering. It does not make compound updates atomic, and a volatile **reference** does not make the object’s fields volatile.

**`synchronized`** (method) — acquire the monitor of `this`, or of the `Class` object for a `static` method, then run the body. The same idea exists as a `synchronized (expr) { }` **statement**, which is not a modifier.

**`native`** — method body is a semicolon; the implementation is platform code (typically C), not Java.

**`default`** (interface method) — instance method on an interface **with a body**.

**`strictfp`** — do not use in new code; presence or absence does not change compile-time or run-time behavior.

```d2
direction: down
all: "modifiers" {
  width: 140
  height: 32
  style.fill: "#fff8e1"
}
acc: "access\npublic protected\n(package) private" {
  width: 180
  height: 56
  style.fill: "#e3f2fd"
}
rest: "by target\nclass / field / method" {
  width: 200
  height: 48
  style.fill: "#e8f5e9"
}
all -> acc
all -> rest
```

**Fig. 1.** Interview split: four access levels, then the modifiers legal on that kind of declaration.

> [!warning] `default` is not package-private
> Package access is the **absence** of `public`, `protected`, and `private`. `default` marks a concrete interface method. Calling package access “the default modifier” is the usual mix-up.

> [!warning] `volatile` is not “the object is thread-safe”
> It covers that field’s reads and writes. `volatile int n` does not make `n++` atomic. `volatile Foo f` publishes the reference, not `f`’s internals. `strictfp` never meant “more precision than IEEE”; historically it **restricted** FP to the standard, and now it does nothing.

> [!tip] Interview answer
> Name the four access levels first — and that package access has no keyword. Then list what else can appear: `static`, `final`, `abstract` on types and methods; `transient` and `volatile` on fields; `synchronized` and `native` on methods; `default` on interface methods; `sealed` / `non-sealed` on classes. Skip `strictfp` for new code. Constructors take only access modifiers.
