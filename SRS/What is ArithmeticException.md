<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Unchecked #Java/Language/Primitives #SRS

# What is `ArithmeticException`?

> [!abstract] Short answer
> **An unchecked `RuntimeException` for an exceptional arithmetic condition.** The classic case is integer `/` or `%` by zero: `int z = 10 / 0` compiles, then throws at run time (often with message `/ by zero`). Floating-point `/ 0` does **not** throw. Ordinary `int`/`long` overflow wraps; it throws only if you use exact methods such as `Math.addExact`.

## Integer zero divisor, not overflow of `+`

`ArithmeticException` extends `RuntimeException`. You do not declare it in `throws`. The JVM may construct it with suppression disabled and a non-writable stack ([[Is RuntimeException a subclass of Exception]], [[Must you declare RuntimeException in a throws clause]], [[What are common kinds of unchecked exceptions in Java]]).

Integer `/` and `%` throw `ArithmeticException` when the divisor is `0`. Both operands are still evaluated first. `Integer.MIN_VALUE / -1` overflows and yields `Integer.MIN_VALUE` — **no** exception ([[Does floating-point division by zero throw ArithmeticException]]).

Floating-point `/` and `%` never throw a run-time exception for divide-by-zero: you get an infinity or NaN.

The built-in integer `+` / `*` wrap on overflow. `Math.addExact` (and `subtractExact`, `multiplyExact`, …) throw `ArithmeticException` when the result does not fit.

```d2
direction: down
intz: "10 / 0  (int)" {
  width: 260
  height: 50
  style.fill: "#ffebee"
}
ae: "ArithmeticException" {
  width: 260
  height: 50
  style.fill: "#ffebee"
}
fl: "10.0 / 0" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}
inf: "Infinity (no throw)" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}
wrap: "Integer.MAX_VALUE + 1" {
  width: 280
  height: 50
  style.fill: "#fff8e1"
}
silent: "wraps; no ArithmeticException" {
  width: 300
  height: 50
  style.fill: "#fff8e1"
}
intz -> ae
fl -> inf
wrap -> silent
```

**Fig. 1.** Zero divisor on `int`/`long` vs wrap vs IEEE floating-point.

```java
class Demo {
    static int divide() {
        return 10 / 0;
    }

    static int remainder() {
        return 10 % 0;
    }

    static int wrap() {
        return Integer.MAX_VALUE + 1;
    }

    static int exact() {
        return Math.addExact(Integer.MAX_VALUE, 1);
    }
}
```

**Listing 1.** `divide` and `remainder` throw `ArithmeticException` at run time. `wrap` returns `Integer.MIN_VALUE`. `exact` throws `ArithmeticException`. You may catch it like any unchecked exception ([[Can you catch an unchecked exception in Java]]). Neither `divide` nor `exact` needs `throws` ([[What happens if you neither catch nor declare a checked exception]]).

> [!warning] Overflow of `+` is not `ArithmeticException`
> `Integer.MAX_VALUE + 1` is silent wrap. Interview snippets that expect a throw on overflow are thinking of `Math.addExact`, not `+`.

> [!warning] `double` `/ 0` is not the integer example
> `10.0 / 0` is `Infinity`. Mixing `int` and `double` in the same question is the usual trap next to this type ([[Does floating-point division by zero throw ArithmeticException]]).

> [!tip] Interview answer
> **`ArithmeticException` is an unchecked `RuntimeException` for bad integer arithmetic — especially `/` or `%` by zero.** `10 / 0` compiles and then throws. Floating-point divide-by-zero does not throw, and `int` overflow of `+` wraps unless you call `addExact`.
