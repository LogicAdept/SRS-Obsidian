<!--
reps: 0
priority: 0
-->
#Java/HashCodeEquals #Java/Language/Object #Java/OOP #SRS

# How are `hashCode` and `equals` implemented in `java.lang.Object`?

> [!abstract] Short answer
> `Object.equals` is **reference equality**: for non-null `x` and `y` it is `true` if and only if `x == y`. Each object is its own equivalence class. `Object.hashCode` is **`native`**: as far as reasonably practical it returns distinct `int`s for distinct objects. `System.identityHashCode(x)` returns that same default hash even if `x`’s class overrode `hashCode`; for `null` it returns `0`. It is **not** specified to be the object’s memory address.

## What `Object` actually does

OpenJDK 21 `java.lang.Object`:

```java
@IntrinsicCandidate
public native int hashCode();

public boolean equals(Object obj) {
    return (this == obj);
}
```

**Listing 1.** Default implementations. `equals` is ordinary Java (`this == obj`). `hashCode` is implemented by the JVM (HotSpot may intrinsic the call). Distinct instances are never equal under this method, even when every field matches. [[How would you explain the Object equals method contract]] is the five-clause contract this pair already satisfies.

The class javadoc only promises distinct ints **as far as is reasonably practical** — not uniqueness, not an address. That matches identity `equals`: each instance is unequal to the others, so distinct hashes are the quality goal.

```text
new Object().equals(new Object())     → false   (different ==)
x.equals(x)                           → true
x.hashCode() == x.hashCode()          → true this run
x.hashCode() == y.hashCode()          → maybe, even if x != y
identityHashCode(x) vs x.hashCode()   → same until you override
```

**Listing 2.** Observable defaults. Collisions of identity hashes remain legal. [[What is a hash collision]] still applies. [[How would you explain the hashCode method contract in Java]] is the three-clause rule.

```d2
direction: down
obj: "java.lang.Object" {
  width: 240
  height: 60
  style.fill: "#e3f2fd"
}
eq: "equals(Object)\nthis == obj" {
  width: 240
  height: 80
  style.fill: "#e8f5e9"
}
hc: "hashCode()\nnative identity int" {
  width: 260
  height: 80
  style.fill: "#fff3e0"
}

obj -> eq
obj -> hc
```

**Fig. 1.** Both defaults are identity. Value types replace **both** together.

`Object.toString` prints `ClassName@` plus the unsigned hex of **that object’s** `hashCode()`, so the default string is identity-based. After you override `hashCode`, default `toString` shows the new hash unless you override `toString` too.

These two `Object` methods already obey “equal objects, equal hashes”: the only equal pair is the same reference, which shares one hash. [[Where do default equals and hashCode implementations come from in Java]] is why every class starts here.

> [!warning] “`hashCode` returns the address”
> That interview line is not the Java SE 21 spec. The method must return the **same** `int` for the same object throughout a run (while identity is unchanged). A live heap address would move under GC and break that. Treat the default as a **stable identity hash**, not a pointer you can convert back to an object.

> [!warning] `identityHashCode` is not `hashCode` after an override
> Once a class overrides `hashCode`, `x.hashCode()` and `System.identityHashCode(x)` can disagree. Identity-based maps (`IdentityHashMap`) use identity hashes and `==`, not your value `equals`/`hashCode`. [[What is the difference between HashMap and IdentityHashMap]] is that split.

> [!tip] Interview answer
> **`Object.equals` is `this == obj`. `Object.hashCode` is native identity hashing — distinct when practical, same as `identityHashCode`, not defined as the memory address.** Classes that want value equality override **both**. Leave them alone when identity is the right notion.
