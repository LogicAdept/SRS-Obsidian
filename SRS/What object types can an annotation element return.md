<!--
reps: 0
priority: 0
-->
#Java/Annotations #SRS

# What object types can an annotation element return?

> [!abstract] Short answer
> Not `Object`. An annotation **element** (the method in an `@interface`) may return only: a **primitive**, **`String`**, **`Class`** (or `Class<…>` / `Class<? extends …>`), an **enum** type, an **annotation** type, or a **one-dimensional array** of those. No wrappers, no `List`, no `String[][]`, no `throws`, no parameters.

## The closed list

Each method in the `@interface` body **is** an element of that annotation type ([[What is a Java annotation]]). The return type must be one of:

1. A primitive (`int`, `boolean`, … — **not** `Integer`)
2. `String`
3. `Class` or a parameterized `Class` (`Class<?>`, `Class<? extends Number>`)
4. An enum class
5. Another annotation interface (nested annotations)
6. An array whose **component** type is one of 1–5 — **one** dimension only

Anything else is a compile-time error. `Object`, `Integer`, `Number`, arbitrary classes, and nested arrays (`String[][]`) are out. The element must not clash with `Object` / `Annotation` methods (`equals`, `hashCode`, `toString`, `annotationType`). An annotation type **T** must not declare an element of type **T** (directly or through another annotation).

Elements have **no** formal parameters, **no** type parameters, **no** `throws`. Optional `default` is an element default (commensurate value: constant, class literal, enum constant, nested annotation, or `{ … }`), not an interface `default` method.

```java
enum Complexity { LOW, HIGH }

public @interface ComplexAnnotation {
    Class<?> value();           // Class (wildcard OK)
    int[] types();              // 1-D array of primitive
    Complexity complexity();    // enum
    Copyright notice() default @Copyright("n/a"); // nested annotation
}

@interface Copyright { String value(); }
```

**Listing 1.** Legal element types — `value` still follows [[How does the value element shorthand work]].

```java
@interface Illegal {
    Object complexity();  // error — not on the list
    Integer count();      // error — wrappers are not primitives
    String[][] grid();    // error — nested array
}
```

**Listing 2.** Typical interview failures.

```d2
direction: down
ok: "primitive | String | Class | enum | annotation" {
  width: 360
  height: 50
  style.fill: "#e8f5e9"
}
arr: "T[] of those only" {
  width: 360
  height: 50
  style.fill: "#e3f2fd"
}
no: "Object, Integer, List, T[][]" {
  width: 360
  height: 50
  style.fill: "#ffebee"
}
ok -> arr: "one dimension"
```

**Fig. 1.** Closed set; arrays do not nest. Marker vs members: [[What is the difference between marker single-member and multi-member annotations]].

> [!warning] `Class` is the only class type
> `Class<Foo>` is allowed; **`Foo` itself is not**. Nested `@interface` types are allowed as element types; that is not a loophole for random classes. Declare `int`, not `Integer`.

> [!tip] Interview answer
> Annotation elements are methods with a tiny return-type list: primitives, String, Class, enums, other annotations, and one-dimensional arrays of those. Object and wrapper types do not compile. No parameters or throws; a default clause is an element default, not a default method.
