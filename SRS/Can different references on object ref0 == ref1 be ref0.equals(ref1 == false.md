<!--
reps: 0
priority: 0
-->
#Java/HashCodeEquals/Contract #SRS

# Can two references with `ref0 == ref1` have `ref0.equals(ref1) == false`?

> [!abstract] Short answer
> **Not if `equals` is correct.** `ref0 == ref1` (and non-null) means both names are the **same** object, so the call is `x.equals(x)`. The contract is **reflexive**: that must be `true`. `Object.equals` is reference equality, so `==` already implies `true`. Only a **broken** override can return `false`.

## Same reference is `x.equals(x)`

Java SE 21 `Object.equals`: for any non-null `x`, `x.equals(x)` should return `true`. `Object`’s own method returns `true` if and only if `x == y`. Put those together:

```text
ref0 == ref1, both non-null
    → same instance
    → ref0.equals(ref1)  is  x.equals(x)
    → MUST be true under the contract
    → IS true for Object.equals (it is ==)

ref0 == ref1 == null
    → cannot call ref0.equals(...)  — NullPointerException
    → not a false result; the call does not complete
```

**Listing 1.** Reflexivity plus `Object`’s identity implementation. [[What is the Object equals contract]] covers the other `equals` laws. The opposite cue — distinct references that still `equals` — is [[Can different objects ref0 != ref1 be ref0.equals(ref1 == true]].

```d2
direction: down
same: "ref0 == ref1\nnon-null" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
ok: "Contract-obeying equals\nx.equals(x) → true" {
  width: 280
  height: 80
  style.fill: "#e8f5e9"
}
bad: "Override that returns false\nfor this — contract broken" {
  width: 300
  height: 80
  style.fill: "#ffebee"
}

same -> ok
same -> bad
```

**Fig. 1.** Two names, one object: legal `equals` cannot answer `false`. A lying override can, and then collections misbehave.

```java
Object a = new Object();
Object b = a;
a == b;      // true
a.equals(b); // true — Object.equals is (this == obj)

final class Broken {
    @Override
    public boolean equals(Object o) {
        return false; // violates reflexive
    }
}

Broken x = new Broken();
x == x;      // true
x.equals(x); // false — illegal under the contract
```

**Listing 2.** Conceptual: identity `equals` stays aligned with `==`. A constant-`false` override is what people mean by “it can be false,” and it is a bug. Hash tables that assume reflexivity will treat that object as missing from a set that already contains it. [[How would you explain pitfalls when implementing equals and hashCode]]

The usual first line of a value `equals` — `if (this == o) return true;` — is the cheap way to keep reflexivity even when later field checks are messy. It is not optional if those checks could otherwise fail for `this`.

> [!warning] `null` is not a `false` from `equals`
> `ref0 == ref1` can be true for two nulls. Then `ref0.equals(ref1)` throws. That is not “`equals` returned false.” [[How would you explain someObj.equals(null)]] is the non-null receiver vs `null` argument (`false`, no NPE).

> [!tip] Interview answer
> **No — not for a legal `equals`.** If `ref0 == ref1` and both are non-null, you are asking `x.equals(x)`, and reflexivity requires `true`. `Object.equals` is `==`, so it already agrees. You only see `false` from a broken override, which will break `HashMap` / `HashSet`.
