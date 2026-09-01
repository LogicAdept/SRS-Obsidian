<!--
reps: 0
priority: 0
-->
#Java/Annotations #SRS

# Which program elements can be annotated in Java?

> [!abstract] Short answer
> **Declarations** (ten `ElementType` contexts) **and type uses** (`TYPE_USE`). Declarations: **module**, **package**, **type** (class/interface/enum/record/annotation type), **annotation type** (`ANNOTATION_TYPE`), **constructor**, **method**, **field** (including enum constants), **parameter**, **type parameter**, **local variable** (including `for` / `try-with-resources` / pattern variables), **record component**. `TYPE_USE` covers uses such as `new`, casts, `implements` arguments, and `throws` types. A **given** annotation only sits where its `@Target` allows.

## Declaration contexts vs type contexts

`@Target` lists `ElementType` constants. Those map onto **declaration contexts** (the program element being declared) plus **type contexts** (annotating a **type** that appears in a declaration or expression). Omit `@Target` and the type is allowed on **every declaration** and on **no** type use — [[How does the Target meta-annotation restrict annotation placement]].

Packages go on the `package` declaration in **`package-info.java`**, not on a random class in that package — [[How do you annotate a Java package]]. Annotation-interface declarations accept both `TYPE` and the narrower `ANNOTATION_TYPE`. Record headers: [[Where do annotations on Java record components apply]].

`TYPE` is “I am annotating the **declaration** of a class/interface/…”. `TYPE_USE` is “I am annotating **this occurrence of a type**.” They are not interchangeable — [[How does TYPE_USE differ from TYPE as an annotation target]].

```java
@Target(ElementType.TYPE_USE)
@interface NonNull {}

class Box<@NonNull T> implements @NonNull Supplier<@NonNull String> {
    @NonNull String f;
    @NonNull String m(@NonNull String p) throws @NonNull Exception {
        Object o = new @NonNull String();
        return (@NonNull String) o;
    }
}
```

**Listing 1.** `TYPE_USE` placements dumps usually want (`new`, cast, `throws`, type arguments). These need `@Target(TYPE_USE)`, not `@Target(TYPE)`.

```d2
direction: down
decl: "10 declaration contexts\nMODULE PACKAGE TYPE ANNOTATION_TYPE\nCONSTRUCTOR METHOD FIELD PARAMETER\nTYPE_PARAMETER LOCAL_VARIABLE RECORD_COMPONENT" {
  width: 420
  height: 90
  style.fill: "#e3f2fd"
}
use: "TYPE_USE — 17 type contexts\nnew, cast, implements, throws, …" {
  width: 420
  height: 70
  style.fill: "#e8f5e9"
}
```

**Fig. 1.** Language-wide map. Empty `@Target({})` annotates **nothing**: [[How does an empty Target array affect a custom annotation]].

> [!warning] `TYPE` is not `TYPE_USE`
> `@Target(ElementType.TYPE)` on `new @Foo Bar()` or a cast does **not** compile. `@Target(ElementType.PACKAGE)` on a class in that package does **not** annotate the package. Local-variable **declaration** annotations are also never stored in the class file; type-use annotations on that same syntax can be.

> [!tip] Interview answer
> You can annotate declarations — types, members, parameters, locals, packages, modules, type parameters, record components — and, since Java 8, type uses with TYPE_USE. Which sites a particular annotation accepts is @Target. TYPE means the type declaration; TYPE_USE means a use of a type in code, including new, casts, and throws.
