<!--
reps: 0
priority: 0
-->
#Java/String #SRS

# What does the String intern method do in Java

> [!abstract] Short answer
> **`intern()` returns the canonical interned `String` for this sequence.** `String` keeps a private pool, initially empty. If the pool already has an `equals` match, that pooled instance is returned. Otherwise **this** object is added and `intern()` returns **this** — it does not allocate a second copy. Literals and string-valued constant expressions are interned already. For live interned `s` and `t`, `s.intern() == t.intern()` iff `s.equals(t)`.

## Lookup by `equals`, then maybe install `this`

The pool is the intern table, not the class-file `constant_pool` ([[What is the Java string pool]]). Matching is `String.equals` (same characters), not `==`.

Call `s.intern()`:

1. If some interned instance `p` satisfies `s.equals(p)`, return `p` (even if `s != p`).
2. Else put `s` in the pool and return `s`.

So `new String("Hello").intern() == "Hello"` is true: the literal was interned at class creation; intern on the copy finds it ([[How do string literals enter the Java string pool]]). A unique runtime string’s first `intern()` is identity-preserving for that object until it is no longer reachable. HotSpot’s table does not pin the object with a strong ref ([[How long do strings live in the Java string pool]]).

`intern()` is `native` in the JDK. Do not intern secrets or unbounded unique user text ([[How would you explain security implications of string interning and the string pool]]).

```d2
direction: down
call: "s.intern()" {
  width: 200
  height: 40
}
hit: "pool has t with s.equals(t)?" {
  width: 280
  height: 45
}
ret: "return pooled t" {
  width: 200
  height: 40
}
add: "add s to pool\nreturn s" {
  width: 200
  height: 45
}

call -> hit
hit -> ret: "yes"
hit -> add: "no"
```

**Fig. 1.** Canonical instance: reuse or install `this`. No third object is created on a miss.

```java
public class InternDemo {
    static void demo() {
        String lit = "Hello";
        String copy = new String("Hello");
        String pooled = copy.intern();
        boolean foundLiteral = lit == pooled;   // true
        boolean copyNotPooled = copy != pooled; // true — copy was not installed

        String built = "prefix-" + new String("unique-runtime");
        boolean firstInstall = built.intern() == built; // true if that sequence was not pooled yet
    }
}
```

**Listing 1.** Hit: intern returns the literal. Miss: intern returns the receiver. `new String("Hello")` itself stays a distinct object.

> [!warning] Intern is not `new String` and not a copy factory
> A miss adds **the instance you called it on**, not a fresh interned clone. A hit returns someone else’s object — your `new String(...)` remains eligible for GC. `==` after intern is identity of interned content, not a substitute for `equals` on non-interned strings. Filling the pool with unique keys is a heap cost, not a `HashMap`.

> [!tip] Interview answer
> **`intern()` returns the unique pooled `String` with the same characters.** If none exists, the receiver is placed in `String`’s private pool and returned. Literals are interned already, so `new String("x").intern() == "x"`. It is lookup-or-install, not “make a copy in PermGen.”
