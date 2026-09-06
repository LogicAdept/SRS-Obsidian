<!--
reps: 0
priority: 0
-->
#Java/String #Java/Immutability #Java/Language/Modifiers/Final #SRS

# Why is java.lang.String immutable and final

> [!abstract] Short answer
> **Immutable:** a `String` has a constant value, so the JDK can intern and share one instance for equal literals without one alias changing another. Threads can read it without synchronizing on the object. The cached `hashCode` stays valid. **`final`:** no subclasses, so those methods cannot be overridden into a mutable or inconsistent fake-`String`. That is not “passwords are safe” — you still cannot wipe a `String`.

## Constant value, then no subclasses

The language type is an unchanging sequence of Unicode code points. The class note: because `String` objects are immutable they can be shared. Intern relies on that: the pool keeps unique instances for a sequence; if those characters could change, every alias would see the mutation ([[What is the Java string pool]], [[What does the String intern method do in Java]]).

Sharing without a monitor is the thread story: no `append` on a `String`. Hash maps: `equals` / `hashCode` are content-based; the JDK caches `hash` / `hashIsZero` on first `hashCode()` (not a public “at birth” contract). Immutability means that cache cannot go stale ([[How would you explain java.lang.String]]).

A `final` class has no subclasses; its methods are never overridden. `String` is `final`, so you cannot write a subclass that stores a mutable buffer behind `charAt` / `equals` while still typing as `String`. That protects intern, maps, and sharing. `final` does not mean the intern pool, and it does not encrypt secrets.

Security interviews often mix two facts. Callers can pass a path, URL, or SQL identifier as `String` and know another thread cannot change those characters. Passwords as `String` are still a problem because you **cannot overwrite** them — prefer `char[]` ([[Why is a char array preferred over String for passwords]]).

```d2
direction: down
imm: "Immutable value\nshare · intern · stable hash" {
  width: 280
  height: 50
}
fin: "final class\nno subclass override of charAt/equals" {
  width: 300
  height: 50
}
ok: "Safe to share the instance\nnot safe to use as a wipeable secret" {
  width: 320
  height: 50
}

imm -> ok
fin -> ok
```

**Fig. 1.** Immutability is the value. `final` closes the type so the value stays that way.

```java
public class StringWhyImmutable {
    static int keyHash(String key) {
        return key.hashCode(); // JDK may cache; key's chars cannot change
    }

    static void share(String path) {
        // other threads may read path; no API mutates it
        path.startsWith("/tmp");
    }
}
```

**Listing 1.** Sharing and hashing assume the characters never change. `class Evil extends String` does not compile.

```java
// Conceptual — illegal
// public class Evil extends String {}
```

**Listing 2.** Conceptual: `final` blocks subclassing. Do not compile this snippet.

> [!warning] Immutable ≠ secret, and hash is not “computed in the constructor”
> Interning needs immutability; it does not put `new String("x")` in the pool. `hashCode` is cached **when first computed**, including a real zero via `hashIsZero`. Do not cite PermGen as the reason `String` is `final`. Do not treat immutability as a substitute for wiping `char[]`.

> [!tip] Interview answer
> **`String` is immutable so interned and shared instances cannot change under you, hashes stay valid, and no per-call lock is required.** **It is `final` so nobody can subclass it and break that contract.** That enables the pool and maps; it does not make passwords safe.
