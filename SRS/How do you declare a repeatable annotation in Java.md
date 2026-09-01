<!--
reps: 0
priority: 0
-->
#Java/Annotations #SRS

# How do you declare a repeatable annotation in Java?

> [!abstract] Short answer
> Declare the annotation as usual, then add **`@Repeatable(Container.class)`**. **`Container`** must be another `@interface` whose **`value()`** returns **`YourAnn[]`**, with any other elements defaulted. Retention of the container must be **at least as long** as the repeatable type, and the repeatable type must be **applicable everywhere the container is**. Multiple `@YourAnn` at one site are then legal; the compiler stores a **container** instance.

## Two types, one `@Repeatable`

`@Repeatable` is a meta-annotation whose `value` is the **containing** annotation interface. `@Repeatable` itself cannot be repeated — one container per type. A container can wrap **at most one** repeatable type. The repeatable type cannot name **itself** as container.

`Container` is well-formed only if:

- `value()` has type `A[]` (not `Object[]`, not `A`)
- every other container element has a **default**
- container retention ≥ repeatable retention (`RUNTIME` on `A` forces `RUNTIME` on `AC`)
- every `ElementType` on `AC` is allowed on `A` (with the usual `TYPE` / `ANNOTATION_TYPE` / `TYPE_USE` substitutions)
- if `A` is `@Documented` or `@Inherited`, `AC` must be too (the reverse is optional)

Repeat is allowed only where a container could be written. If `A` has no `@Target` but `AC` does, you may repeat `A` only on `AC`’s sites.

```java
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.METHOD)
@Repeatable(Schedules.class)
public @interface Schedule {
    String day();
}

@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.METHOD)
public @interface Schedules {
    Schedule[] value();
}

@Schedule(day = "Mon")
@Schedule(day = "Fri")
void backup() { }
```

**Listing 1.** Repeatable type + containing type. Use-site repeats become one `@Schedules` in the class file — [[How are repeating annotations stored for compatibility]].

```d2
direction: right
a: "@Schedule\n@Repeatable(Schedules.class)" {
  width: 220
  height: 70
  style.fill: "#e8f5e9"
}
c: "@interface Schedules\nSchedule[] value()" {
  width: 220
  height: 70
  style.fill: "#e3f2fd"
}
a -> c: "container"
```

**Fig. 1.** Two `@interface`s; only the first is written twice in source. Declare the types: [[How do you declare a custom annotation in Java]]. Meta-annotation: [[What are meta-annotations in Java]].

> [!warning] `@Repeatable` is not enough
> Pointing `@Repeatable` at a type that lacks `A[] value()` is a **compile error** on `A`, not a runtime surprise. Mismatched `@Retention` or a **wider** `@Target` on the container is the same. Reflection: `getAnnotation(Schedule.class)` is **null** when two are present — you need `getAnnotationsByType` (or read `Schedules`).

> [!tip] Interview answer
> Java 8 repeatable annotations are a pair: the annotation you repeat, marked @Repeatable, and a container whose value is an array of that type. The compiler wraps several instances into one container for older class-file readers. The container must be at least as visible (retention) and no more widely applicable than the repeatable type.
