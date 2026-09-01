<!--
reps: 0
priority: 0
-->
#Java/Language/Records #Java/Generics #SRS

# Can a Java record be generic?

> [!abstract] Short answer
> **Yes.** After the record name you may declare type parameters in angle brackets, exactly as for a generic class. Those variables are in scope in the header, so component types, generated accessors, and the canonical constructor can all mention them. Bounds (`T extends Number`) are allowed. Generic records shipped with the standardized feature in Java 16.

## Type parameters follow the name

```d2
direction: down
header: "record Pair<A, B>(A first, B second)" {
  width: 340
  height: 70
  style.fill: "#e3f2fd"
}
params: "type parameters A, B\nin scope in the header and body" {
  width: 300
  height: 70
  style.fill: "#fff3e0"
}
members: "private final A first\npublic A first()\ncanonical Pair(A, B)" {
  width: 280
  height: 90
  style.fill: "#e8f5e9"
}
header -> params: "optional TypeParameters"
params -> members: "same variables"
```

**Fig. 1.** A generic record is a generic class: type parameters sit after the name and flow into components and derived members.

`RecordDeclaration` is `record` *Name* `[TypeParameters]` *Header* *Body*. A class is generic when that section declares type variables. JLS §6.3 gives a record’s type parameters an extra region of scope: the **header**, not only the body — that is why `T` may appear as a component type. JEP 395 states a record class can be top level or nested, **and can be generic**.

Type bounds use the same `extends` clause as other generic classes:

```java
record Pair<A, B>(A first, B second) {}

record Result<T>(T value, String message) {}

record NumberPair<T extends Number>(T x, T y) {}

record ListNode<T>(T value, ListNode<T> next) {}

Pair<String, Integer> p = new Pair<String, Integer>("hello", 42);
String s = p.first();
Integer n = p.second();
ListNode<String> node = new ListNode<String>("x", null);
```

**Listing 1.** Unbounded parameters, an upper bound, and a self-referential node. Accessors return the component types; construction uses a parameterized type. Type arguments are reference types or wildcards — `Pair<int, int>` does not compile.

A generic record is still a concise data carrier — a common stand-in for a typed pair or wrapper — not a special tuple type in the language. See [[What is the difference between a Java record and a regular class]] and [[What methods does the compiler generate for a Java record]].

The canonical constructor’s derived signature has **no constructor type parameters** of its own; an explicit canonical constructor **must not be generic**. An accessor **must not be generic** either. The class type parameters already supply `A` and `B` to those members.

## Erasure and static scope are unchanged

A generic record declaration still defines one runtime class. `Pair<String, Integer>` and `Pair<Integer, String>` share that class after type erasure, the same mapping as `Vector<String>` vs `Vector<Integer>`. Parameterized types with concrete arguments are not reifiable, so `instanceof Pair<String, Integer>` is a compile-time error; `instanceof Pair<?, ?>` is allowed. Details: [[How does type erasure work for Java generics]]. Bounds: [[What is the purpose of type bounds in Java generics]].

```java
Pair<String, Integer> a = new Pair<String, Integer>("a", 1);
Pair<Integer, String> b = new Pair<Integer, String>(1, "b");
boolean sameClass = a.getClass() == b.getClass(); // true
// boolean bad = a instanceof Pair<String, Integer>; // not reifiable
boolean ok = a instanceof Pair<?, ?>;
```

**Listing 2.** One erased `Pair` class at run time; only a reifiable `instanceof` compiles.

A static method or a nested record cannot mention the outer type parameters. Nested records are implicitly `static`, so they are not inner classes of the enclosing record. Give the static method or nested record **its own** type parameters. Related: [[Can a Java record declare static members and instance methods]] and [[How do you declare a static generic method in Java]].

```java
record Pair<A, B>(A first, B second) {
    // static Pair<A, B> of(A a, B b) { ... } // A, B not in a static context

    static <X, Y> Pair<X, Y> of(X x, Y y) {
        return new Pair<X, Y>(x, y);
    }
}

record Box<T>(T value) {
    // record Wrap(T inner) {} // nested record is static; T is not in scope
    record Wrap<U>(U inner) {}
}
```

**Listing 3.** Class type parameters are instance-scoped. Static factories and nested records redeclare type variables if they need them.

> [!warning] Erasure is not waived for records
> A generic record does not keep its type arguments at run time. Do not branch on `Pair<String, Integer>` with `instanceof` or cast through a raw `Pair` and expect the compiler to restore `A` and `B`. Two parameterizations are still one `Class` object.

> [!warning] Nested records cannot capture the outer type parameter
> `record Outer<T>(T v) { record Inner(T x) {} }` does not compile: the nested record is implicitly static, and a type parameter of `Outer` must not appear in a static nested type. Declare `record Inner<U>(U x)` or keep the component on the outer record.

> [!tip] Interview answer
> **Yes — a record can declare type parameters after its name, and the header can use them, so `record Pair<A, B>(A first, B second)` is a normal generic class with generated accessors.** Bounds work the same way as on other classes. Erasure still applies, and static members or nested records need their own type parameters because they do not see `A` and `B`.
