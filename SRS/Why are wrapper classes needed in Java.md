<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #Java/Language/Wrappers #SRS

# Why are wrapper classes needed in Java?

> [!abstract] Short answer
> Primitives are not objects. Wrappers exist so a number or `boolean`/`char` can be used **where an object is required** — especially **collections and generics** (`List<Integer>`, never `List<int>`) — and so the type can carry **class methods and constants** (`parseInt`, `MIN_VALUE`, `Character.isDigit`). Autoboxing (Java 5) inserts `valueOf` so you rarely wrap by hand. They are **not** a way for a method to mutate the caller’s primitive.

## Object APIs, utilities, absence

The platform’s number wrappers are the `Number` subclasses `Byte`, `Short`, `Integer`, `Long`, `Float`, `Double` (`Boolean` and `Character` are the other two language wrappers). You still write arithmetic on primitives. You wrap when you need an object ([[What are the wrapper types for Java primitives]], [[What is the difference between int and Integer in Java]]).

Official reasons to use a `Number` object rather than a primitive:

1. **A method or collection that expects an object** — `list.add(5)` boxes into `List<Integer>` ([[How does adding an int to an ArrayList of Integer autobox]]). Type arguments are reference types.
2. **Constants on the class** — `Integer.MIN_VALUE` / `MAX_VALUE`, `SIZE`, `BYTES`.
3. **Static conversions** — `parseInt`, `valueOf`, `toBinaryString`, radix conversions; instance `intValue` / `compareTo` / `equals`.

A fourth, type-system reason dumps always add: a wrapper **can be `null`** (unset / missing); an `int` cannot ([[Why cannot a Java primitive variable be null]], [[Why use wrapper types for JavaBean properties]]).

```d2
direction: down
prim: "int 5\nnot an object" {
  width: 200
  height: 50
}
wrap: "Integer.valueOf(5)\nobject for APIs" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
uses: "List / Map / null / parseInt" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}
prim -> wrap -> uses
```

**Fig. 1.** Wrappers exist to put a primitive payload into the object type system.

```java
List<Integer> numbers = new ArrayList<>();
numbers.add(5);              // autoboxing — List cannot hold int
Integer age = null;          // valid absence
// int age = null;           // does not compile

int parsed = Integer.parseInt("42");
int bits = Integer.SIZE;     // 32 — lives on the class, not on int
```

**Listing 1.** Conceptual: collections, null, and utilities — the three everyday needs.

Wrappers implement `Serializable` and sit in object graphs; that is a consequence of being classes, not a separate “serialization wrapper” feature. They are **value-based**: do **not** lock on an `Integer`. They are **immutable**: `void bump(Integer n) { n++; }` does not change the caller ([[Can wrapping a primitive let a Java method change the caller value]]).

Java is not “objects only.” Primitives stay for size and arithmetic; wrappers fill the holes where the type system demands a reference.

> [!warning] Wrapping is not pass-by-reference
> A dump that says “wrap it so the method can change the caller’s `int`” is describing a **mutable custom holder**, not `Integer`. Language wrappers have no setter; `++` rebinds a local.

> [!tip] Interview answer
> **Wrappers exist because primitives are not objects — you cannot put `int` in a `List` or a generic type, and you cannot call `parseInt` on a primitive type.** They also allow `null` for “no value.” Autoboxing builds the object for you. Use `int` for math; use `Integer` when the API or absence requires an object.
