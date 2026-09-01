<!--
reps: 0
priority: 0
-->
#Java/Annotations #SRS

# How does TYPE_USE differ from TYPE as an annotation target?

> [!abstract] Short answer
> **`TYPE` is a declaration; `TYPE_USE` is a type in source.** `@Target(ElementType.TYPE)` allows `@Foo` on a **class, interface, enum, record, or `@interface` declaration**. `@Target(ElementType.TYPE_USE)` (Java 8) allows `@Foo` on a **use of a type** — `new`, casts, `implements` / `throws`, type arguments, nested array levels, and so on. The same source position can be both; **`@Target` decides** whether `@Foo` attaches to the declaration, the type, or both.

## Declaration context vs type context

`TYPE` is one of the **declaration** contexts. It does **not** cover packages, type-parameter **declarations**, or any expression that merely **mentions** a type.

`TYPE_USE` covers the **17 type contexts** (plus, as a convenience, class/interface declarations and type-parameter declarations so checkers can write `@NonNull class C {}`). There is no `ElementType.USE`. `TYPE_PARAMETER` is a **different** Java 8 constant: the `<T>` in `class Box<T>`, not a use of `T`. Full map: [[How does the Target meta-annotation restrict annotation placement]], [[Which program elements can be annotated in Java]].

```java
@Target(ElementType.TYPE)
@interface OnType {}

@Target(ElementType.TYPE_USE)
@interface OnUse {}

@OnType                       // legal — type declaration
class Box<@OnUse T> {         // TYPE_USE on a type-parameter declaration
    @OnUse Box<@OnUse String> make(@OnUse String s) {
        return new @OnUse Box<@OnUse String>();
    }
}

@OnType String notADecl;      // compile-time error — field, not a type declaration
```

**Listing 1.** Conceptual — `TYPE` does not license `@OnType` on a field type. `TYPE_USE` licenses annotations in `new`, type arguments, and on `<T>`.

```java
@Target(ElementType.TYPE_USE)
@interface A {}
@Target(ElementType.TYPE_USE)
@interface B {}
@Target(ElementType.TYPE_USE)
@interface C {}

@C int @A [] @B [] f;
```

**Listing 2.** Nested array annotations require `TYPE_USE`. `@A` applies to `int[][]`, `@B` to `int[]`, `@C` to `int`. `@Target(TYPE)` cannot express this.

At `@Foo int f;`:

- `FIELD` only → declaration annotation on `f`
- `TYPE_USE` only → type annotation on `int`
- **both** → both at once

`TYPE_USE` alone on a `void` method or a `var` variable is a compile-time error (no closest type). A type annotation cannot sit on a **package name** (`java` in `java.lang.String`). Receiver parameters are type contexts only.

```d2
direction: right
decl: "TYPE\nclass / interface\nenum / record / @interface" {
  width: 240
  height: 90
  style.fill: "#fff3e0"
}
use: "TYPE_USE\nnew, cast, throws,\ntype args, arrays, …" {
  width: 250
  height: 90
  style.fill: "#e3f2fd"
}

decl -> use: "same token may\nbe both"
```

**Fig. 1.** `TYPE` names the entity; `TYPE_USE` names a type appearing in a declaration or expression.

Runtime: `getAnnotation` on `Class` / `Method` returns **declaration** annotations. Type-use annotations are on `AnnotatedType` (`getAnnotatedReturnType()`, …): [[How do you retrieve annotations at runtime]]. Local-variable **declaration** annotations are not stored in the class file; **type** annotations on that variable’s type can be.

> [!warning] `TYPE` will not compile on `new`, casts, or `throws`
> Those positions are type contexts. You need `TYPE_USE` (often with a checker such as nullness). `TYPE_PARAMETER` is not a substitute: it marks the declaration of a type variable, not `List<@Foo String>`. Combining `TYPE` and `TYPE_USE` is legal and makes `@Foo class C {}` both a declaration annotation and a type annotation.

> [!tip] Interview answer
> TYPE is for annotating the declaration of a class, interface, enum, record, or annotation type. TYPE_USE, added in Java 8, is for annotating a type wherever it appears — constructors, casts, type arguments, nested arrays, implements and throws. The compiler uses @Target to decide whether a modifier-looking annotation applies to the declaration, the nearest type, or both; TYPE_PARAMETER is a third constant for <T> declarations.
