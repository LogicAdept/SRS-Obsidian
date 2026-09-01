<!--
reps: 0
priority: 0
-->
#Java/Language/Object #SRS

# How would you explain key methods declared on `java.lang.Object`?

> [!abstract] Short answer
> **`Object` declares the methods every class instance and array already has.** Interview “key” set: **`equals` / `hashCode` / `toString`** (overridable identity and display), **`getClass`** (`final` runtime class), **`clone`** (protected shallow copy), **`wait` / `notify` / `notifyAll`** (`final` monitor wait set), and **`finalize`** (deprecated cleanup). Defaults are **identity** (`==` for `equals`, distinct-ish `hashCode`, `ClassName@hex`).

## What is actually on `Object`

`Object` is the root type, so these members are inherited unless a subclass hides or overrides them ([[How would you explain java.lang.Object as the root of the class hierarchy]]). Visibility splits the list: **`public`** instance methods you call on any reference; **`protected clone` and `finalize`**; **`final`** on `getClass`, `wait`, `notify`, and `notifyAll` (you cannot override those).

```d2
direction: right
id: "Identity\nequals · hashCode\ntoString · getClass" {
  width: 240
  height: 80
  style.fill: "#e3f2fd"
}
copy: "Copy\nclone" {
  width: 140
  height: 80
  style.fill: "#fff3e0"
}
thr: "Monitor\nwait · notify\nnotifyAll" {
  width: 180
  height: 80
  style.fill: "#e8f5e9"
}
leg: "Legacy\nfinalize" {
  width: 140
  height: 80
  style.fill: "#ffebee"
}
```

**Fig. 1.** Four clusters. Only the identity group plus `clone` / `finalize` are overridable.

## Identity and display

**`equals(Object)`** — `Object`’s implementation is **reference equality**: `true` iff `this == obj`. It is reflexive, symmetric, transitive, consistent, and `x.equals(null)` is `false`. Subclasses that want **value** equality override it and **must** override **`hashCode`** so equal objects have equal hash codes ([[How would you explain default equals and hashCode inherited from Object]], [[Why should equals and hashCode be overridden together]]).

**`hashCode()`** — contract: same object, unmodified, same `int` during one run; equal objects → equal codes; unequal objects **need not** differ (collisions are allowed). `Object` returns distinct integers for distinct objects **as far as reasonably practical** — not a guaranteed memory address.

**`toString()`** — `Object` returns `getClass().getName() + '@' + Integer.toHexString(hashCode())`. Override for a readable value; the default is an identity-ish debug string, not “the contents.”

**`getClass()`** — **`public final`**. Returns the `Class` object for the **runtime** class (the one locked by `static synchronized` methods of that class). Arrays and class instances both have one. You cannot override it to lie.

```java
Object a = new Object();
Object b = new Object();
boolean eq = a.equals(b);           // false — not the same instance
boolean id = a == b;                // false
String s = a.toString();            // java.lang.Object@…
Class<?> c = a.getClass();          // class java.lang.Object
int h = a.hashCode();
```

**Listing 1.** Conceptual: defaults compare and print **identity**, not fields. `a.equals(a)` is `true`.

## Copy, threads, cleanup

**`clone()`** — **`protected`**, throws `CloneNotSupportedException` if the runtime class is not `Cloneable`. `Object.clone` is a **shallow** field-for-field copy ([[How would you explain the Object clone method and its issues]], [[What is the difference between shallow and deep copying in Java]]). Convention: override as `public` and call `super.clone()`.

**`wait` / `notify` / `notifyAll`** — **`public final`**. They operate on **this object’s monitor**. The caller **must own** that monitor or the call throws `IllegalMonitorStateException`. `wait` places the thread in the wait set and **releases that monitor** (only); `notify` wakes one waiter, `notifyAll` all of them. `wait` without a timeout waits until notified, interrupted, or a **spurious wakeup** — loop on the condition ([[How would you explain the Object wait method and waiting on monitors]]). Three overloads: no-arg, `wait(millis)` (`0` means no timeout, like no-arg `wait`), `wait(millis, nanos)` with nanos in `0–999999`. There is also a public **`Object()`** constructor.

**`finalize()`** — **`protected`**, `@Deprecated(since = "9", forRemoval = true)`. `Object`’s method does nothing. The collector **might** call it later, once, on some thread that holds no user-visible locks; an exception from `finalize` is ignored. Prefer `AutoCloseable` / `Cleaner`. Do not treat it as a destructor ([[How would you explain the finalize method in Java and why it is discouraged]]).

> [!warning] Default `equals` is `==`
> Putting a class with only the inherited `equals` / `hashCode` into a `HashMap` keys by **identity**. Two “equal-looking” instances miss each other. If you override `equals`, override `hashCode` in the same class; skipping `hashCode` breaks the map contract even when `equals` looks right.

> [!warning] `wait` is not `Thread.sleep`
> `o.wait()` without `synchronized (o)` (or an equivalent monitor acquisition) throws **`IllegalMonitorStateException`**. Sleeping does not release `o`’s monitor and does not wait for `o.notify()`.

> [!tip] Interview answer
> **Name the clusters: identity (`equals`, `hashCode`, `toString`, `getClass`), copy (`clone`), monitor (`wait`/`notify`/`notifyAll`), and deprecated `finalize`.** Say that `Object.equals` is `==`, `getClass` and the wait/notify family are `final`, and `clone`/`finalize` are `protected`. If they use your type as a map key, you override `equals` and `hashCode` together; you do not use `finalize` for resource cleanup.
