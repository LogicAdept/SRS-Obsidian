<!--
reps: 0
priority: 0
-->
#Java/Versions/25 #SRS

# What are flexible constructor bodies

> [!abstract] Short answer
> **JEP 513 (final in Java 25; previewed as 447/482/492 across 22–24) allows statements in a constructor before the explicit `this(...)`/`super(...)` call. The preamble cannot touch `this` — no instance methods, no superclass state — but can validate arguments, compute, and initialize the class's own fields, eliminating the static-helper-validation idiom.**

## Why the old restriction existed and what changed

The JVM has always allowed byte-level flexibility; the language restricted it so the superclass constructor ran on a "clean" object, making fields like `Object`'s hash and monitor safe to touch. The problem: argument validation before delegation required awkward static helper methods, and defensive copies before `super()` could observe them were impossible — a real hole when the superclass constructor calls overridable methods that read state. With flexible bodies, the preamble validates and pre-initializes own fields (statements may write own instance fields, may not read them), then delegates. Records benefit directly: canonical-constructor normalization can happen in natural order ([[What are compact source files and instance main methods]] is the other 25 beginner-syntax piece).

```java
public class V46_FlexibleCtors {
    static final class Account {
        private final long id;

        Account(long id) {
            this(check(id), true);             // pre-25: only static calls fit before this()
            System.out.println("body: id=" + id);
        }

        Account(long id, boolean unused) { this.id = id; }

        static long check(long id) {
            if (id <= 0) throw new IllegalArgumentException("id must be positive");
            return id;
        }
    }

    public static void main(String[] args) {
        new Account(42L);
        try { new Account(-1L); }
        catch (IllegalArgumentException e) {
            System.out.println("rejected: " + e.getMessage());
        }
        // JEP 513 (final in 25; previews 447/482/492): the check can live directly
        // in the constructor body BEFORE this(...) / super(...) - no static helper.
    }
}
```

**Listing 1.** Verified on JDK 21 (V46_FlexibleCtors in empirics): `body: id=42`, `rejected: id must be positive` (out/V46_FlexibleCtors.txt) — the pre-25 shape compiles everywhere; the 25 form puts `check(id)` inline in the preamble.

```d2
direction: right
pre: "preamble\nvalidate args, init own fields" { style.fill: "#e8f5e9"; width: 260; height: 80 }
call: "explicit this(...) / super(...)" { style.fill: "#e3f2fd"; width: 270; height: 70 }
post: "rest of body\nfull this access" { style.fill: "#fff3e0"; width: 220; height: 70 }
pre -> call -> post: ""
```

**Fig. 1.** A 25 constructor in three phases: the preamble runs first, delegation happens in the middle, the remainder executes after the superclass is up.

> [!warning] The preamble is not a free zone
> Statements before delegation may not read `this`, call instance methods, or reference superclass state — the compiler rejects them. The often-quoted justification remains: if the preamble could leak a half-built `this`, a superclass constructor calling a virtual method would observe uninitialized fields. Flexible bodies relax the least necessary amount ([[What is a helpful NullPointerException]] is unrelated but also a "constructor crash" interview trap).

> [!tip] Interview answer
> **Flexible constructor bodies, final in 25 after three preview rounds from 22, let the constructor validate arguments and initialize its own fields before calling super or this. The preamble still cannot touch the instance otherwise — that is what keeps superclass constructors safe. It kills the static-validator idiom and closes the defensive-copy-before-super hole.**
