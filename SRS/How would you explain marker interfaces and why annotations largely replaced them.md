<!--
reps: 0
priority: 0
-->
#Java/OOP #Java/Annotations #SRS

# How would you explain marker interfaces and why annotations largely replaced them?

> [!abstract] Short answer
> A **marker interface** is a type with **no methods** whose only job is to **tag** implementing classes (`Serializable`, `Cloneable`, `RandomAccess`). The JVM or libraries test **`instanceof`**. **Annotations** took over most *new* tagging: they can sit on **members**, not only types, can carry **elements**, and do not invent a type in the hierarchy. Markers remain when you **need a type** (`void f(Serializable s)`, `Runnable & Serializable` lambdas).

## Presence as a type vs presence as metadata

`RandomAccess` is documented as a **marker interface**: `List` algorithms branch on `instanceof` to avoid quadratic `get` on a `LinkedList`. `Serializable` “has no methods or fields and serves only to identify the semantics of being serializable.” `Cloneable` tells `Object.clone()` the copy is allowed — and famously **does not declare `clone()`**, so implementing it does not give you a callable `clone` in the type system ([[Why is clone declared on Object rather than on Cloneable]]).

That pattern is a **type**: subtypes inherit it (`Serializable` subtypes are serializable), you can write it in signatures and casts, and JLS even calls `Serializable` a marker interface type for lambda intersections.

A **marker annotation** is an empty `@interface` ([[What is the difference between marker single-member and multi-member annotations]]). It is **not** a type of the instance. Nothing in the language runs it ([[Why do annotations have no direct effect on annotated code]]). A compiler, processor, or `isAnnotationPresent` must look.

Annotations **largely replaced** new markers because they are better *metadata*:

- **More sites** — methods, fields, parameters, packages, type uses; an interface only marks a **type**
- **Data, not only a bit** — elements and defaults; a marker interface cannot say `since = "2.0"`
- **Opt-in retention** — `SOURCE` / `CLASS` / `RUNTIME`; `implements` is always a runtime type
- **No accidental subtype contract** — `@Inherited` is explicit and class-only; `implements Serializable` infects every subclass

```java
class Order implements Serializable {}          // type: instanceof works

@Retention(RetentionPolicy.RUNTIME)
@interface Audited {}                           // metadata: not a type of Order

@Audited class Payment {}
boolean tagged = Payment.class.isAnnotationPresent(Audited.class);
```

**Listing 1.** Same “flag this class” intent; only the interface participates in the type system.

```d2
direction: right
mi: "empty interface\nimplements + instanceof" {
  width: 220
  height: 70
  style.fill: "#fff3e0"
}
ann: "empty @interface\n@Target + reflection" {
  width: 220
  height: 70
  style.fill: "#e8f5e9"
}
mi -> ann: "new tags"
```

**Fig. 1.** Libraries still use markers when the tag **must** be a type (`Serializable` — [[How does serialization and deserialization with Serializable work]]).

> [!warning] Do not “replace” Serializable with an annotation in your head
> Object serialization and `clone` still look for **interfaces**. An `@Serializable` you invent is invisible to `ObjectOutputStream`. Conversely, implementing `Cloneable` does not add a public `clone()` to the API. Use a marker interface when callers must mention the tag in a **signature**; use an annotation when they must not.

> [!tip] Interview answer
> A marker interface is an empty interface used as a run-time type tag, historically Serializable, Cloneable, and RandomAccess. Annotations replaced that pattern for most new metadata because they apply beyond types, can hold elements, and stay out of the implements clause. Keep a marker interface when you need instanceof or a parameter type; otherwise declare a marker annotation.
