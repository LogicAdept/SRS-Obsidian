<!--
reps: 0
priority: 0
-->
#Java/Language/Assert #SRS

# Can the assert detail expression be a void method?

> [!abstract] Short answer
> **No. After the colon the compiler needs a value, not a `void` call.** `assert cond : someVoidMethod();` is a compile-time error (`'void' type not allowed here`). A method that returns a value is legal: if `methodOne()` returns `999` and the assert fails with assertions on, the thrown `AssertionError` has message `999`.

## A detail must denote a value

The two forms are `assert cond;` and `assert cond : detail;` ([[What are the two forms of the Java assert statement]]). In the second form, `detail` is evaluated only when assertions are enabled and `cond` is already `false` ([[When is the assert detail expression evaluated]]). Its value becomes the detail message of the thrown `AssertionError` after string conversion ([[What happens when a Java assert statement fails]]).

A method invocation is a legal `detail` when the method returns a value — `int`, `String`, or any other non-`void` type. A method declared `void` denotes nothing: it produces no value, so it cannot be `detail`. Parentheses around the condition (`assert (ok) : expr`) are ordinary grouping; they do not change the rule.

```d2
direction: down
stmt: "assert cond : expr" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
voidCall: "expr is a void method\ncompile-time error" {
  width: 300
  height: 70
  style.fill: "#ffebee"
}
value: "expr has a value\n(method call OK)" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
msg: "enabled and cond is false\nAssertionError(message)" {
  width: 300
  height: 70
  style.fill: "#fff8e1"
}
stmt -> voidCall
stmt -> value
value -> msg
```

**Fig. 1.** `detail` is a compile-time value check; only a non-`void` expression can become the `AssertionError` message.

```java
class Demo {
    static void log() { }

    static int methodOne() {
        return 999;
    }

    static void check(boolean ok) {
        // assert ok : log(); // does not compile — detail is void
        assert ok : methodOne();
    }
}
```

**Listing 1.** `methodOne()` is a legal detail because it returns `int`. Uncommenting `log()` fails compilation. With `-ea`, `check(false)` throws `AssertionError` whose message is `999`.

> [!warning] The detail call is not required logic
> Even a legal non-`void` method in `detail` runs only when assertions are enabled and the condition is already `false`. If assertions are off, or the condition is `true`, the method is not invoked. Do not put work the program must perform there ([[Why must Java assert expressions be free of side effects]]).

> [!warning] `Void` is not `void`
> A method declared to return `Void` (the class) is a reference-typed expression, so it compiles as `detail`. The forbidden case is the `void` keyword: a method that returns no value.

> [!tip] Interview answer
> **No — the colon form needs a value for the `AssertionError` message, so a `void` method call does not compile.** A method that returns something (`int`, `String`, `Object`) is fine. That call still runs only when assertions are on and the condition is already false, so do not put required work there.
