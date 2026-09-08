<!--
reps: 0
priority: 0
-->
#Java/Language #SRS

# What does strong typing mean in Java?

> [!abstract] Short answer
> Java is **strongly typed**: a type **limits the values** a variable may hold and an expression may produce, **limits the operations** on those values, and **fixes what those operations mean**. It is separately **statically typed**: those types are known at **compile time**. Together that is “strong static typing” — many mistakes are compile-time errors. Static vs this cue: [[How would you explain static typing in Java]].

## Strong is the limits; static is when they are known

**Static:** every variable and every expression has a compile-time type ([[How would you explain kinds of variables in Java such as local and instance]]).

**Strong:** that type is not a comment. An `int` variable cannot hold a `boolean`. `&&` is not defined on `int`. `+` on two `int`s is numeric addition; `+` with a `String` is concatenation. Those meanings are chosen from the types, not from the bits at run time.

The language has two kinds of type: **primitive** (`boolean` and the numeric types) and **reference** (classes, interfaces, arrays), plus the nameless **null type** ([[How would you explain Java primitive data types]], [[How would you explain reference types in the Java type system]]). There is **no** conversion between `boolean` and the numeric types, so `boolean b = 0` does not compile ([[Why cannot you assign 0 or TRUE to a Java boolean]]). Assignment, invocation, and casting are conversion contexts: some conversions are implicit (widening `int` to `long`, boxing, String conversion in `+`); others need a cast; some pairs are simply illegal.

```d2
direction: down
t: "type of the variable / expression" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
v: "which values are legal" {
  width: 240
  height: 45
  style.fill: "#e8f5e9"
}
op: "which operators apply\nand what they mean" {
  width: 260
  height: 55
  style.fill: "#fff3e0"
}
t -> v
t -> op
```

**Fig. 1.** Strong typing is a restriction on values and operations, not a synonym for “no subclasses.”

```java
class Demo {
    static void go() {
        int n = 1;
        boolean ok = true;
        String s = "n=" + n;     // + means concatenation because of String
        // boolean b = 0;        // illegal: no int → boolean conversion
        // int m = n && 1;       // illegal: && is not an integer operator
        Object o = s;            // legal: String is a subtype of Object
        String t = (String) o;   // legal: run-time check
    }
}
```

**Listing 1.** Types pick both legality and meaning. `+` with `String` is not integer add. A subtype assignment is still strongly typed.

Strong typing does **not** mean “the run-time never sees a type error.” A cast can throw `ClassCastException`. An `Object[]` alias of a `String[]` can throw `ArrayStoreException` on store. Unchecked generic operations can pollute a heap `List`. Those are still typed operations that failed a **run-time** check. `var` only infers a compile-time type; it does not loosen the limits ([[What does keyword word var]]). `instanceof` is the explicit type test ([[What is the instanceof operator for in Java]]).

> [!warning] Strong is not the same as static, and not “no polymorphism”
> Static = the compiler **knows** the type. Strong = the type **constrains** values and operators. `Shape x = new Circle()` is both: `x` is a `Shape` at compile time, and you may only call `Shape` members on it, while the object’s class may still be `Circle`. Do not answer “strong typing” with only “types are checked at compile time” — that sentence is **static** typing.

> [!warning] Java is not C, and not a dynamic language
> In C, `0` is usable as false and types are weaker about mixing integers and pointers. In Java that is a compile-time error. `Object` plus a cast is not dynamic typing: the variable still has a type, and the cast is checked. Generics are strong at compile time and **erased** at run time — that is a hole in reification, not a hole in “variables have types.”

> [!tip] Interview answer
> **Strong typing means the type of a variable or expression limits which values are legal and which operations apply — `boolean` is not an `int`, and `&&` is not an integer operator.** Java is also statically typed: those types are known before the program runs. Subtype assignment and casts still exist; they do not make the language dynamically typed.
