<!--
reps: 0
priority: 0
-->
#Java/Annotations #Java/Language/Reflection #SRS

# How do you retrieve annotations at runtime?

> [!abstract] Short answer
> **Get an `AnnotatedElement` for a loaded type or member, then call `getAnnotation` / `isAnnotationPresent` (and `getAnnotationsByType` when the type is repeatable).** Those methods only see annotations the VM kept: `RetentionPolicy.RUNTIME`, stored as `RuntimeVisibleAnnotations`. `isAnnotationPresent(T.class)` is `getAnnotation(T.class) != null`.

## From a loaded `Class` to a member, then to the annotation

Runtime lookup is core reflection on the program **currently running in this VM** ([[What is reflection in Java]]). Obtain a `Class` ([[How can you get the Class object in Java]]), then a `Method`, `Field`, or `Constructor` — those reflected members, and `Class` itself, are `AnnotatedElement`s. Call the lookup on **that** element, not only on the class:

```java
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.METHOD)
@interface Route {
    String value();
}

class Api {
    @Route("/ping")
    void ping() {}
}

class Read {
    static String path() throws Exception {
        Method ping = Api.class.getDeclaredMethod("ping");
        if (!ping.isAnnotationPresent(Route.class)) {
            return null;
        }
        return ping.getAnnotation(Route.class).value();
    }
}
```

**Listing 1.** Marker check, then typed annotation, then element methods such as `value()`. Without `@Retention(RUNTIME)`, both calls miss `Route` ([[How do Java annotation retention policies work]], [[What happens if you omit Retention on a custom annotation]]).

Which member array you walk is a **reflection** choice, not a retention choice. `getDeclaredMethods()` / `getDeclaredFields()` return members **declared** on that class (all access levels, including synthetic/bridge methods) and **exclude inherited** members. `getMethods()` / `getFields()` return **public** members, including those inherited from superclasses and superinterfaces ([[What is the difference between getMethod and getDeclaredMethod]], [[What is the difference between getField and getDeclaredField]]).

```d2
direction: down
c: "Class (loaded type)" {
  width: 220
  height: 40
}
m: "getDeclaredMethod / getMethod\n(or Field, Constructor)" {
  width: 280
  height: 60
  style.fill: "#e3f2fd"
}
a: "isAnnotationPresent / getAnnotation\ngetAnnotationsByType" {
  width: 280
  height: 60
  style.fill: "#e8f5e9"
}
c -> m
m -> a
```

**Fig. 1.** Two hops: find the annotated construct, then read `RUNTIME` metadata. A processor that ran at compile time is a different consumer ([[How do annotation processors differ from runtime reflection]]).

`AnnotatedElement` methods differ by **which** annotations they return:

| Method | Inherited `@Inherited` on a **class**? | Looks through a `@Repeatable` container? |
| --- | --- | --- |
| `getAnnotation` / `isAnnotationPresent` / `getAnnotations` | Yes (`present`) | No |
| `getAnnotationsByType` (Java 8) | Yes (`associated`) | **Yes** |
| `getDeclaredAnnotation` / `getDeclaredAnnotations` | No (directly present only) | No |
| `getDeclaredAnnotationsByType` | No | **Yes** |

`@Inherited` is a meta-annotation on the **annotation interface**. If it is present and you query a **class** that has no annotation of that interface, the implementation walks superclasses up to `Object`. It has **no effect** on methods, fields, or constructors, and annotations on **implemented interfaces** are not inherited this way ([[What are meta-annotations in Java]]).

```java
@Inherited
@Retention(RetentionPolicy.RUNTIME)
@interface Audited {}

@Audited
class Base {}

class Child extends Base {}

// Child.class.getAnnotation(Audited.class) != null
// Child.class.getDeclaredAnnotation(Audited.class) == null
```

**Listing 2.** `getAnnotation` follows `@Inherited` on a class. `getDeclaredAnnotation` does not. Repeatable types: `getAnnotation(Tag.class)` sees a single `Tag` or the **container**, not the unwrapped list; use `getAnnotationsByType(Tag.class)` to look through the compiler-generated container.

These APIs return **declaration** annotations. Type-use annotations live on `AnnotatedType` (and related type-annotation attributes), not on `Class.getAnnotation`.

> [!warning] No `RUNTIME`, no reflection
> `SOURCE` is not in the class file. `CLASS` (the default if you omit `@Retention`) is in the file as a run-time-invisible attribute and is **not** returned by these methods, unless a VM-specific flag keeps those attributes. A framework scan that “never sees” your marker is usually this policy, not a wrong `getDeclaredMethod` name.

> [!warning] Declared members are not inherited members
> `Child.class.getDeclaredMethods()` does not include `Base.ping()`. Walking only declared methods and then calling `getAnnotation` looks like a retention bug; it is a member-lookup bug. For public inherited methods use `getMethods()` (or `getMethod`); for non-public superclass members, walk `getSuperclass()` and call `getDeclaredMethods()` on each class. `@Inherited` never copies a **method** annotation onto the subclass.

> [!tip] Interview answer
> **Get the `Class` or the `Method`/`Field`, then `isAnnotationPresent` / `getAnnotation` — those read `RUNTIME` declaration annotations only.** Repeatable types need `getAnnotationsByType` so the container is unwrapped. `getAnnotation` on a class follows `@Inherited`; `getDeclaredAnnotation` does not; `@Inherited` does not apply to methods. `getDeclaredMethods` skips inherited methods, which is a separate lookup rule from retention.
