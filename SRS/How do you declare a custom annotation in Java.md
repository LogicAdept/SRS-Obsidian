<!--
reps: 0
priority: 0
-->
#Java/Annotations #SRS

# How do you declare a custom annotation in Java?

> [!abstract] Short answer
> Write an **annotation interface**: `@interface Name { … }`. Each **element** is a no-arg method with a legal return type and an optional `default`. You almost always add **meta-annotations** — at least `@Target` and `@Retention`. The type implicitly extends `Annotation`; you **cannot** write `extends`, type parameters, or a local `@interface`.

## `@interface` is the declaration

`@` plus `interface` is a distinct kind of interface, not a class and not a normal `interface` you implement by hand. Use it at top level or as a **member** type. It is never generic, never `sealed` / `non-sealed`, and never local (no canonical name). It does not take `extends`; a type that `extends` an annotation type is a **plain** interface — [[Can you extend an annotation type in Java]].

Body members that look like methods **are** the elements ([[What object types can an annotation element return]]): primitive, `String`, `Class`, enum, nested annotation, or a 1-D array of those. No parameters, no `throws`, no `default`/`static`/`private` methods. `default <value>` is an **element default**, not an interface default method. Nested enums used as element types are fine.

Put **meta-annotations** on the `@interface` itself ([[What are meta-annotations in Java]]):

- `@Target` — where instances may appear; omit it and **every declaration** is legal, **no** type uses. [[How does the Target meta-annotation restrict annotation placement]]
- `@Retention` — how far instances survive; omit it and you get **CLASS**, invisible to `getAnnotation`. [[What happens if you omit Retention on a custom annotation]]
- Optionally `@Documented`, `@Inherited`, `@Repeatable`

```java
@Documented
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.TYPE)
public @interface ClassPreamble {
    String author();
    String date();
    int currentRevision() default 1;
    String[] reviewers();
}

@ClassPreamble(author = "Ada", date = "2024-01-01", reviewers = {"Alan"})
public class Generation3List {}
```

**Listing 1.** Declare the type, then apply it. `value()` is still the only element that may drop its name at the use site.

```d2
direction: down
meta: "@Target + @Retention\n(and friends)" {
  width: 260
  height: 55
  style.fill: "#e3f2fd"
}
iface: "@interface Name { elements }" {
  width: 260
  height: 55
  style.fill: "#e8f5e9"
}
use: "@Name(...) on a program element" {
  width: 260
  height: 55
}
meta -> iface -> use
```

**Fig. 1.** Meta-annotations configure the type; they are not required by syntax but are required for a usable custom annotation.

> [!warning] Syntax compiles; retention often does not do what you meant
> A bare `@interface Flag {}` is legal and is a marker, but frameworks using reflection will **not** see `@Flag` unless you set `@Retention(RUNTIME)`. `@Target({})` compiles and then **forbids every placement**. Do not declare `Integer x();` or `void f() throws Exception;` — those are not legal elements.

> [!tip] Interview answer
> A custom annotation is an @interface: methods in the body are elements with a tiny set of return types and optional defaults. Add Target and Retention; the compiler will not extend Annotation for you in source, and you cannot write extends or generics. Without RUNTIME retention, getAnnotation returns null even though the annotation compiled.
