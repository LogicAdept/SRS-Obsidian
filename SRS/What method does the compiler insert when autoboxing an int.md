<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #Java/Language/Wrappers/Autoboxing #SRS

# What method does the compiler insert when autoboxing an `int`?

> [!abstract] Short answer
> **`Integer.valueOf(int)`.** An assignment such as `Integer y = num` or `list.add(5)` is compiled as a static call to that factory, not as `new Integer`. That is why autoboxed values in **-128..127** can be `==` identical, and why `new Integer` is a different identity path. Unboxing is the reverse: `intValue()` ([[What method does the compiler insert when unboxing an Integer]]).

## Boxing is a factory call

Boxing conversion turns an `int` expression into an `Integer` whose `intValue()` equals that `int`. The compiler implements that conversion with `Integer.valueOf`. The same pattern holds for the other primitives (`Boolean.valueOf`, `Long.valueOf`, …) ([[When does autoboxing occur in Java]], [[What is the difference between Integer.valueOf and new Integer]]).

```d2
direction: down
src: "int num / list.add(5)" {
  width: 220
  height: 50
}
call: "Integer.valueOf(int)" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
out: "Integer reference" {
  width: 200
  height: 50
}
src -> call -> out
```

**Fig. 1.** Autoboxing of `int` is `invokestatic Integer.valueOf`.

```java
int num = 42;
Integer y = num;                 // Integer.valueOf(num)

List<Integer> list = new ArrayList<>();
list.add(5);                     // list.add(Integer.valueOf(5))

Integer a = 100;
Integer b = 100;
boolean cached = (a == b);       // true: valueOf cache
Integer c = 200;
Integer d = 200;
boolean maybe = (c == d);        // not required; often false
```

**Listing 1.** Conceptual: what the compiler writes, and why `==` follows `valueOf`.

`valueOf` is specified to cache **-128..127** and may cache more if the runtime raised the high end ([[How can you extend the Integer autobox cache maximum]]). Language boxing of those **constant** `int`s must yield `==` identical references; `new Integer(100)` never does.

The constructors exist but are deprecated. Writing `new Integer(num)` yourself is not autoboxing and bypasses the factory.

> [!warning] Do not answer `new Integer`
> Older snippets show `Integer y = new Integer(num)`. That compiles (with deprecation) and always allocates. Autoboxing has used `valueOf` since it was introduced (Java 5). Mixing `new` with boxed literals is how interview `==` traps are built.

> [!tip] Interview answer
> **Autoboxing an `int` inserts `Integer.valueOf(int)`.** That factory can return a cached object, which is why two boxed `100`s may be `==` and two boxed `200`s may not. Unboxing inserts `intValue()`. Never describe boxing as `new Integer`.
