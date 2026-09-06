<!--
reps: 0
priority: 0
-->
#Java/Lambdas #Java/Language/Modifiers/Final #Java/Versions/8 #SRS

# Which variables can lambda expressions access in Java?

> [!abstract] Short answer
> **Everything in the enclosing lexical scope that a nested block could see — with two extra rules.** The lambda’s own parameters; enclosing fields and methods through `this` / `Outer.this`; static members; and enclosing locals/parameters only when they are `final` or effectively final and definitely assigned. A lambda does **not** open a new scope: it cannot redeclare an enclosing local as a parameter. `this` is the enclosing instance, not the functional-interface object.

## Lexical scope, not a nested class scope

Declarations in a lambda body are interpreted as in the enclosing environment. The lambda does not inherit names from the functional interface’s supertypes and does not introduce a new level of scoping. That is why `(x) ->` is a compile-time error if `x` is already a local or parameter in the enclosing method, and why `this.x` is the enclosing class’s field, not a field of `Predicate` / `Consumer` ([[How would you explain lambda expressions in Java]], [[How would you explain nested classes in Java and when to use each kind]]).

What you can **read** (and, for fields, write):

| Name | Rule |
| --- | --- |
| Lambda parameters | Always; they are the SAM arguments |
| Enclosing instance fields / methods | Via `this` / `Enclosing.this` — no effectively-final check |
| Static members of enclosing types | By name or `ClassName.member` |
| Enclosing locals, method/constructor/lambda/exception parameters | Only if `final` or effectively final **and** definitely assigned |

The local/parameter row is **capture**. Details and the `++` / for-each vs `i++` cases live on [[Which variables can a Java lambda expression capture]] and [[How would you explain effectively final]]. A `final` reference still allows mutating the object ([[What does this code snippet print to the console 2]]).

```d2
direction: down
body: "lambda body" {
  width: 200
  height: 40
  style.fill: "#e3f2fd"
}
own: "its parameters" {
  width: 180
  height: 40
  style.fill: "#e8f5e9"
}
enc: "this / Outer.this\nfields, methods, statics" {
  width: 240
  height: 55
  style.fill: "#e8f5e9"
}
loc: "enclosing locals\nfinal or effectively final" {
  width: 260
  height: 55
  style.fill: "#fff3e0"
}
body -> own
body -> enc
body -> loc
```

**Fig. 1.** Access is three buckets. The third bucket is the capture rule. `this.x` in an inner class is that inner class’s field, not the lambda.

Tutorial shape: method parameter `x`, local `z`, lambda parameter `y`, inner-class field `this.x`, outer field `Outer.this.x`. Printing those yields the parameter, the lambda argument, the local, the inner field, and the outer field — five different variables, all accessible from one body.

```java
import java.util.function.Consumer;

class Demo {
    int outer = 0;

    class Inner {
        int inner = 1;

        void show(int x) {
            int z = 2;
            Consumer<Integer> c = (y) -> {
                System.out.println(x);
                System.out.println(y);
                System.out.println(z);
                System.out.println(this.inner);
                System.out.println(Demo.this.outer);
            };
            c.accept(x);
            // Consumer<Integer> shadow = (x) -> { }; // cannot redeclare x
            // z = 99; then the lambda above would not compile
        }
    }
}
```

**Listing 1.** Same access pattern as the language tutorial’s `LambdaScopeTest`: enclosing parameter, lambda parameter, effectively final local, `this` field, enclosing-class field.

> [!warning] `this` is not the `Consumer`
> `this.inner` is `Inner.this.inner`. There is no `this.accept` on the lambda object, and you cannot call the target functional interface’s `default` methods as `this.andThen(...)` — `this` is not the SAM instance. To refer to the function itself, or those defaults, use a method reference or an anonymous class. Replacing `y` with `x` in `(x) ->` fails because the lambda does not nest a scope that can hide the method parameter.

> [!warning] Accessing a local is capture
> Reading `z` in the body is enough to trigger the effectively-final check. Writing `z = 99` in the body, or `z = 99` after the lambda, both fail. Writing `this.inner = 3` inside the lambda is ordinary field assignment and is allowed.

> [!tip] Interview answer
> **A lambda sees its own parameters, the enclosing instance through `this`, statics, and enclosing locals that are `final` or effectively final.** It is lexically scoped: no new shadowing level, and `this` is the enclosing object. Locals are captured by variable, not by copying object state.
