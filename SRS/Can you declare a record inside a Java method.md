<!--
reps: 0
priority: 0
-->
#Java/Language/Records #SRS

# Can you declare a record inside a Java method?

> [!abstract] Short answer
> **Yes.** A **local record class** may be declared in a method (or constructor or initializer) body, like a local class. It is implicitly `static`: it does not capture the enclosing instance or the enclosing method’s local variables. Pass anything it needs as components. Standardized with records in Java 16 (present in the JDK 15 second preview).

## Local records are nested records in a block

```d2
direction: down
method: "findTopMerchants(...) { ... }" {
  width: 300
  height: 60
  style.fill: "#e3f2fd"
}
local: "record MerchantSales(Merchant m, double sales)" {
  width: 340
  height: 60
  style.fill: "#e8f5e9"
}
rules: "implicitly static — not an inner class\nno enclosing instance\nno enclosing-method locals" {
  width: 320
  height: 90
  style.fill: "#fff3e0"
}
method -> local: "local declaration"
local -> rules
```

**Fig. 1.** A local record lives in the method body but does not close over that method’s state.

JLS §8.10: a record declaration may be top level, a member, or a **local** record class (§14.3). JLS §14.3: a local class may be a record class; every local record class is implicitly `static`, therefore **not** an inner class. You still must not write the `static` modifier on a local declaration — that is a compile-time error for any local class or interface, even when the type is implicitly static. `public` / `protected` / `private` are also illegal on a local record.

JEP 395’s reason: intermediate values in a method (especially streams) want a named, immutable holder **next to** the code that uses it, without a hidden enclosing-instance field that would add silent state. Ordinary local classes are **never** static and *do* capture the enclosing method. See [[What is the difference between a Java record and a regular class]] and [[Can a Java record declare static members and instance methods]].

```java
List<Merchant> findTopMerchants(List<Merchant> merchants, int month) {
    record MerchantSales(Merchant merchant, double sales) {}

    return merchants.stream()
        .map(merchant -> new MerchantSales(merchant, computeSales(merchant, month)))
        .sorted((m1, m2) -> Double.compare(m2.sales(), m1.sales()))
        .map(MerchantSales::merchant)
        .toList();
}
```

**Listing 1.** Local record as a named pipeline holder (same shape as JEP 395 / the Java SE tutorial). `month` is used in the enclosing method, then passed into `computeSales` — not read from inside `MerchantSales`.

The same pattern is `record Ranked(User user, int score) {}` before a `sorted` / `limit` / `map` chain.

Local records were introduced in the records **second preview** (JDK 15) and finalized in **JDK 16** with the rest of the feature. [[In which Java version were records standardized]]

## Implicitly static: what you cannot capture

Methods of the local record cannot mention locals, parameters, or catch variables of the enclosing method. Because the record is not an inner class, it also has no enclosing instance — no extra hidden field, and no `Outer.this`. Put captured data in the header.

```java
void printScaled(int factor) {
    // record Scaled(int x) {
    //     int apply() { return x * factor; } // factor is an enclosing-method variable
    // }

    record Scaled(int x, int factor) {
        int apply() { return x * factor; } // component, not a capture
    }

    System.out.println(new Scaled(10, factor).apply());
}
```

**Listing 2.** Pass enclosing data as a component. Do not expect local-class capture.

You cannot write `static record Ranked(...) {}` or `private record Ranked(...) {}` inside the method. The local record is already static, and JLS §14.3 forbids `static` and the access modifiers `public` / `protected` / `private` on any local type. Local enums follow the same implicit-static story — contrast [[Can you declare a Java enum inside a method]].

> [!warning] Implicitly static means no hidden enclosing-instance field
> A local class can silently capture `this` and effectively final locals. A local record does not. That is deliberate: extra captured state would break the “header is the whole instance state” model. If the compiler complains that a name is not in scope inside the local record, add a component (or compute the value in the enclosing method and pass it in).

> [!warning] Do not write `static` on the local declaration
> Nested *member* records may say `static` redundantly. A **local** record must not: JLS §14.3 forbids the `static` modifier on local class and interface declarations, even though the local record is implicitly `static`.

> [!tip] Interview answer
> **Yes — you can declare a record inside a method; it is a local record class, used a lot as a tiny named holder in streams.** It is implicitly static, so it does not capture the enclosing instance or method locals; pass those as components. The feature is part of standardized records in Java 16.
