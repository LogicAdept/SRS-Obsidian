<!--
reps: 0
priority: 0
-->
#Java/Annotations #SRS

# How does the Target meta-annotation restrict annotation placement?

> [!abstract] Short answer
> `@Target` lists the `ElementType` contexts where instances of that annotation interface may appear. Use outside those contexts is a **compile-time error**. **Omit** `@Target` and the type is allowed on **every declaration** (not on type uses). `@Target({})` allows **no** standalone use.

## Declaration contexts vs type contexts

`@Target`’s `value` is an `ElementType[]`. Each constant names a **declaration** context, except `TYPE_USE`, which names **type** contexts (and, as a convenience, class/interface and type-parameter declarations).

| Constant | Where `@Foo` may appear | Since |
| --- | --- | --- |
| `TYPE` | Class, interface, enum, record, annotation interface | 1.5 |
| `FIELD` | Field, enum constant | 1.5 |
| `METHOD` | Method (including annotation elements) | 1.5 |
| `PARAMETER` | Formal / exception parameter | 1.5 |
| `CONSTRUCTOR` | Constructor | 1.5 |
| `LOCAL_VARIABLE` | Local variable (including resources / pattern variables) | 1.5 |
| `ANNOTATION_TYPE` | Annotation interface declaration only | 1.5 |
| `PACKAGE` | Package declaration (`package-info.java`) | 1.5 |
| `TYPE_PARAMETER` | Type parameter | 1.8 |
| `TYPE_USE` | A use of a type | 1.8 |
| `MODULE` | Module declaration | 9 |
| `RECORD_COMPONENT` | Record component | 16 |

Several constants may appear together. A **duplicate** constant in one `@Target` is a compile-time error: [[What happens if the same ElementType appears twice in Target]]. There is no `ElementType.USE` — type annotations use **`TYPE_USE`**.

```java
@Target({ElementType.FIELD, ElementType.METHOD})
public @interface Audited {}

class Job {
    @Audited String id;           // legal
    @Audited void run() {}        // legal
    @Audited Job() {}             // compile-time error — not CONSTRUCTOR
}
```

**Listing 1.** The compiler enforces the listed contexts only. Full placement map: [[Which program elements can be annotated in Java]]. Packages: [[How do you annotate a Java package]]. `TYPE` vs `TYPE_USE`: [[How does TYPE_USE differ from TYPE as an annotation target]].

## Omit, empty, or both declaration and type

- **No `@Target`** — applicable in **all declaration contexts**, **no** type contexts. (Older JavaDoc excluded type parameters; current language includes them as a declaration context.)
- **`@Target({})`** — applicable **nowhere** as a modifier; only as a nested member type. [[How does an empty Target array affect a custom annotation]]
- **Both a declaration constant and `TYPE_USE`** — at locations that are both a declaration and a type context (e.g. a field), the same `@Foo` applies to **the declaration and** the nearest type.

```d2
direction: right
meta: "@Target({FIELD, METHOD})" {
  width: 230
  height: 70
  style.fill: "#e3f2fd"
}
ok: "field / method" {
  width: 160
  height: 60
  style.fill: "#e8f5e9"
}
bad: "constructor / type use\ncompile-time error" {
  width: 220
  height: 70
  style.fill: "#ffebee"
}

meta -> ok
meta -> bad
```

**Fig. 1.** `@Target` is a closed allow-list. Anything not listed — including type uses when only declaration constants are given — is illegal.

> [!warning] `TYPE` does not mean “any type-related location”
> `TYPE` is **type declarations** (classes, interfaces, enums, records, `@interface`s). It does **not** cover type parameters (`TYPE_PARAMETER`), type uses (`TYPE_USE`), or packages (`PACKAGE`). `ANNOTATION_TYPE` is narrower than `TYPE`: only annotation interface declarations. Putting `@Foo` on a `package` line when `@Target` is `TYPE` is a compile-time error.

> [!tip] Interview answer
> @Target names the ElementType contexts where that annotation may be written; anywhere else is a compile-time error. If you omit @Target it may appear on any declaration but not as a type-use annotation; @Target({}) forbids standalone use. TYPE is declarations of types, TYPE_USE is uses of types, and repeating the same ElementType in one @Target is illegal.
