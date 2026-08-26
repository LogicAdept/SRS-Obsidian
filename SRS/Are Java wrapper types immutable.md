<!--
reps: 0
priority: 0
-->
#Java/Language/Wrappers #Java/Immutability #SRS

# Are Java wrapper types immutable?

> [!abstract] Short answer
> **Yes** for the eight boxing wrappers (`Boolean`, `Byte`, `Character`, `Short`, `Integer`, `Long`, `Float`, `Double`). Each holds one primitive in a `private final` field, the class is `final`, and there is no API that mutates that field after construction. Changing a “value” means assigning a different wrapper reference (often after unbox / compute / box).

## What “immutable wrapper” means

The JLS names the boxing wrappers explicitly: a boxing conversion may allocate a `Boolean`, `Byte`, `Character`, `Short`, `Integer`, `Long`, `Float`, or `Double`. In the JDK (Java SE 21 OpenJDK), those types are declared `public final`, store the payload in a `private final … value` field, and expose only readers such as `intValue()` / `booleanValue()` — never a setter for the wrapped primitive.

`Character` is called out the same way in the Oracle tutorial: once created, a `Character` object cannot be changed. The numeric wrappers follow the same design. This is the same shallow immutability story as [[Why is java.lang.String immutable and final]]: the object’s own state does not change; a variable of that type may still be reassigned.

```d2
direction: down
create: "Construct / box\nInteger.valueOf(10)" {
  width: 260
  height: 80
  style.fill: "#e3f2fd"
}
obj: "Integer instance\nprivate final int value = 10" {
  width: 280
  height: 90
  style.fill: "#e8f5e9"
}
read: "intValue() / unbox\nreads value only" {
  width: 260
  height: 80
  style.fill: "#fff3e0"
}
rebind: "ten = … / ten++\nvariable gets another reference" {
  width: 300
  height: 90
  style.fill: "#ffebee"
}

create -> obj
obj -> read
obj -> rebind: "object stays 10"
```

**Fig. 1.** Immutability is about the instance’s field, not about freezing the local variable that points at it.

## Why `ten++` still compiles

Postfix / prefix `++` on an `Integer` variable is legal because the language unboxes, increments a primitive, then boxes the result back into the variable (JLS §15.14.2 / §15.15.1: binary numeric promotion may unbox; the sum may be boxed before store). The original `Integer` object is not updated in place. See [[What happens when you increment an Integer with plus plus in Java]].

```java
Integer ten = Integer.valueOf(10);
Integer same = ten;
ten++;
// same.intValue() is still 10; ten refers to a boxed 11
```

**Listing 1.** Conceptual local-variable demo: `++` rebinds `ten`; `same` still sees the old immutable instance.

Oracle’s autoboxing tutorial shows the same idea for `%` and `+=` on `Integer`: those operators apply to `int`, so the compiler inserts `intValue()` (and boxing on assignment when the left-hand side is a wrapper).

```java
Integer n = Integer.valueOf(5);
n = Integer.valueOf(n.intValue() + 1); // what n++ amounts to
```

**Listing 2.** Conceptual expansion of increment-and-assign on a wrapper variable.

> [!warning] Reassignment is not mutation
> `Integer x = 1; x = 2;` looks like changing “the Integer,” but it only changes which object `x` names. Other references to the old instance still see the old value. Do not confuse this with mutable holders such as `AtomicInteger`, which are `Number` subtypes used for concurrent updates and are **not** the immutable boxing wrappers.

> [!warning] “New” boxed value may be cached
> Boxing of small `int` / `long` / etc. values can return a shared cached instance (JLS identity rule for many constants in `-128..127`). After `ten++`, `ten` holds a different **value**, but it is not always a freshly allocated object, and `==` between boxed values is unreliable outside the cache contract — prefer `equals` / `intValue()`.

> [!tip] Interview answer
> **Yes — `Integer`, `Boolean`, and the other boxing wrappers are immutable `final` classes with a `final` payload field and no mutating API.** Operations like `n++` unbox, compute on the primitive, and box a result into the variable; the previous wrapper object is unchanged. Variable reassignment is allowed; in-place mutation is not.
