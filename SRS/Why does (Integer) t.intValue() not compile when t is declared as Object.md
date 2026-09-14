<!--
reps: 0
priority: 0
-->
#Career/Interview/Exercises #Java/Language/Wrappers/Autoboxing #SRS

# Why does `(Integer) t.intValue()` not compile when `t` is declared as `Object`?

> [!abstract] Short answer
> **It never reaches runtime: the line does not compile.** A cast applies to the whole unary expression that follows it, and a method invocation binds tighter than a cast, so `(Integer) t.intValue()` parses as `(Integer) (t.intValue())`. The variable `t` has static type `Object`, and `Object` declares no `intValue()` method, so the compiler reports `cannot find symbol: method intValue()`. Cast the reference first — `int k = (Integer) t / 10;` — and the program prints `10`.

## Parse order: cast vs method call

The cast operator wraps a **unary expression**, not a single identifier. A method invocation is a postfix (primary) expression, which is the base of the unary chain — so the entire call `t.intValue()` lands *inside* the cast. To call a method on the cast result you must parenthesize the cast itself: `((Integer) t).intValue()`.

```java
Object t = new Integer(101);            // legal: widening reference conversion
int k = (Integer) t.intValue() / 10;    // compile error: cannot find symbol: method intValue()
int j = ((Integer) t).intValue() / 10;  // legal: call on the cast result
int m = (Integer) t / 10;               // legal: cast first, then unboxing in the division
```

**Listing 1.** The original line fails in the compiler; the two corrected lines compile and both produce `10`.

```d2
direction: down
expr: "(Integer) t.intValue() / 10" {
  width: 300
  height: 50
  style.fill: "#e3f2fd"
}
parse: "cast operand is the whole\nunary expression t.intValue()" {
  width: 330
  height: 60
  style.fill: "#fff3e0"
}
fail: "Object has no intValue()\ncompile-time error" {
  width: 300
  height: 60
  style.fill: "#ffebee"
}
fixed: "(Integer) t / 10" {
  width: 250
  height: 50
  style.fill: "#e8f5e9"
}
check: "runtime check:\nt holds an Integer" {
  width: 290
  height: 55
  style.fill: "#e8f5e9"
}
unbox: "unbox Integer to int\nin binary numeric promotion" {
  width: 320
  height: 60
  style.fill: "#e8f5e9"
}
div: "101 / 10 -> 10" {
  width: 220
  height: 50
  style.fill: "#e8f5e9"
}

expr -> parse
parse -> fail
fixed -> check
check -> unbox
unbox -> div
```

**Fig. 1.** The broken line dies during compilation; the fixed line casts, checks the type, unboxes, and truncates.

## What the fixed line does at runtime

`Object t = new Integer(101);` is a plain upcast of the boxed value — nothing to fix there (modern code writes `Object t = 101;` and lets autoboxing do the wrapping [[When does autoboxing occur in Java]]). The fix `(Integer) t / 10` runs in three steps. First the downcast performs a **runtime check** and throws [[When can a ClassCastException be thrown in Java]] if `t` held some other type. Then the division applies binary numeric promotion, which **unboxes** the `Integer` operand with a compiler-inserted `intValue()` call [[What method does the compiler insert when unboxing an Integer]] [[What is unboxing]]. Finally integer division truncates toward zero, so `101 / 10` is `10`, and `System.out.println(k)` prints `10`.

> [!warning] A cast is not a member selector
> The cast does not bind to the next identifier only — it takes the entire unary expression that follows. The popular lie is that `(Integer) t.intValue()` means "cast `t`, then call `intValue`"; the compiler reads the opposite. And the corrected line is a **downcast**: if `t` actually held a `Long`, `(Integer) t` would throw `ClassCastException` at runtime rather than failing compilation.

> [!tip] Interview answer
> **The snippet does not compile.** `(Integer) t.intValue()` parses as `(Integer) (t.intValue())` because the method call binds tighter than the cast, and `Object` has no `intValue()` method — that is a `cannot find symbol` compile error. Cast first — `(Integer) t / 10` — which checks the type at runtime, unboxes the `Integer`, and divides: `101 / 10` prints `10`.
