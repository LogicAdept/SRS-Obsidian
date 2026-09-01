<!--
reps: 0
priority: 0
-->
#Java/Lambdas #Java/Versions/8 #SRS

# What is lambda what and specifics using lambda

> [!abstract] Short answer
> **A Java 8 lambda is a poly expression `parameters -> body` that evaluates to a functional-interface instance — the body does not run at `->`.** It runs later, each time the SAM is invoked. Params match the abstract method (types may be inferred). One parameter may drop parentheses; zero params use `()`. Expression body or `{` block `}` with `return` if a value is required. Not a shortened anonymous class: `this` is the enclosing instance.

## Arrow, target type, deferred body

A lambda is like a method: formals plus a body (expression or block) in terms of those parameters. It may appear only in an assignment, invocation, or cast context — somewhere a **target type** exists. That target must be a functional interface. Evaluating the lambda **creates** (or reuses) an object that implements that interface; it does **not** run the body. The body runs when the function method is invoked ([[How would you explain lambda expressions in Java]], [[What is functional interface]], [[How would you explain to what variable are there access lambda]]).

`->` has very low precedence. Left: parameter list. Right: body. The dump `(x, y) -> x + y` assigned to `Operationable` then `calculate(10, 20)` is `30`.

Parameters are either all **explicit** (`(int x, int y)`) or all **inferred** (`(x, y)`). Mixing `(x, int y)` is illegal. Inferred types come from the target FI. Zero parameters: `()`. One inferred parameter: parentheses optional (`n -> n * n`). You cannot declare type parameters on a lambda.

An expression body can be void (a statement expression) or a value. A block body is `{` statements `}`; a value-compatible block must `return` a value on every path (or throw / loop forever). Defaults on the FI do not count toward the SAM — “only one method without implementation” is the dump’s loose wording for **one abstract method**.

Captured locals must be `final` or effectively final. Unlike an anonymous class, names / `this` / `super` mean the **enclosing** context.

```d2
direction: down
syn: "(params) -> body" {
  width: 220
  height: 45
  style.fill: "#fff8e1"
}
fi: "target: functional interface" {
  width: 260
  height: 45
  style.fill: "#e8f5e9"
}
later: "SAM invoke runs the body" {
  width: 260
  height: 45
  style.fill: "#e3f2fd"
}

syn -> fi: "assignment / arg / cast"
fi -> later: "deferred"
```

**Fig. 1.** Parse once, run later, as many times as you call the SAM. The lambda is never invoked with `operation(10, 20)` — only `operation.calculate(...)`.

```java
interface Operationable {
    int calculate(int x, int y);
}

interface Printable {
    void print(String s);
}

class Demo {
    static int sum(int[] numbers, java.util.function.IntPredicate condition) {
        int result = 0;
        for (int i : numbers) {
            if (condition.test(i)) result += i;
        }
        return result;
    }

    static void use() {
        Operationable op = (x, y) -> x + y;
        op.calculate(10, 20); // 30
        Operationable div = (x, y) -> {
            if (y == 0) return 0;
            return x / y;
        };
        Printable p = s -> System.out.println(s);
        p.print("Hello, world");
        sum(new int[] {0, 1, 0, 3}, n -> n != 0);
        // (x, int y) -> x + y  // illegal: mixed inferred/declared
    }
}
```

**Listing 1.** Dump arithmetic and `print` / block / method-arg shapes. `IntPredicate` is the JDK SAM for `int -> boolean`; a homemade `Condition` is the same idea.

> [!warning] Not an anonymous class with different braces
> `this` in a lambda is the outer object. A second abstract method on the target type does not compile, but extra `default` methods do. `(x, int y) ->` is illegal. A value block without `return` is illegal.

> [!warning] The body is not a method you call by name
> `Operationable operation = (x, y) -> x + y` stores an object. Execution happens at `calculate`. The implementation may skip allocating a fresh object every time the lambda expression is evaluated. Serializing that object is extra, not the default.

> [!tip] Interview answer
> **Lambda = `(params) -> body` that implements one abstract method.** Types inferred or all written; `()` if none; parens optional for one inferred param; `{ return ...; }` for a block that yields a value. Body runs when the SAM is called, not at `->`. `this` is enclosing. Locals captured must be effectively final.
