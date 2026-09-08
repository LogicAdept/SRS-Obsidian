<!--
reps: 0
priority: 0
-->
#Java/Language #SRS

# What does keyword word var?

> [!abstract] Short answer
> `var` is **local-variable type inference** from **Java 10**: the compiler takes the type from a **standalone** initializer. `int i = 0` and `var i = 0` both give `i` type `int`. It is a **reserved type name**, not a keyword — existing `var` fields, methods, and packages stay legal; a class named `var` does not. Fields, method parameters, and return types still need a written type. Lambda parameters may use `var` from **Java 11**, and then **every** parameter of that lambda must.

## Where inference is allowed

```d2
direction: down
ok: "locals with initializer\nenhanced / basic for\ntry-with-resources" {
  width: 300
  height: 80
  style.fill: "#e8f5e9"
}
j11: "Java 11: all params of an\nimplicitly typed lambda" {
  width: 300
  height: 70
  style.fill: "#e3f2fd"
}
no: "fields, method params, return type\nnull / lambda / method-ref init\nno initializer, diamond-to-Object trap" {
  width: 340
  height: 90
  style.fill: "#ffebee"
}
ok -> j11
ok -> no: "not these"
```

**Fig. 1.** LVTI is for locals (and, from 11, uniformly `var` on an implicitly typed lambda). It is not a new dynamic type.

Legal places: a local with an initializer, the index of a traditional `for`, the element of an enhanced `for` ([[How would you explain the enhanced for each loop in Java]]), a try-with-resources resource. The initializer is typed **as if it were not in an assignment context**, so a lambda or method reference as the initializer is a compile error — there is no target type. `var g = null` is illegal because the type would be the null type.

`var list = new ArrayList<String>()` infers `ArrayList<String>`. Diamond is **allowed**: `var list = new ArrayList<>()` infers `ArrayList<Object>` because there is no target type to fill `<>`. That is the opposite of “diamond is forbidden with `var`.” Put the type argument on `new`, or write the left-hand type and keep diamond.

From Java 11 you may write `(var a, var b) -> a + b` on an implicitly typed lambda. Mixing `var` with a bare inferred name (`(var x, y)`) or with a manifest type (`(var x, int y)`) is illegal. Capture rules do not change ([[Which variables can a Java lambda expression capture]]).

```java
import java.util.ArrayList;
import java.util.function.BiFunction;

class Demo {
    int locals() {
        var i = 0;                              // int
        var list = new ArrayList<String>();     // ArrayList<String>
        var objects = new ArrayList<>();        // ArrayList<Object> — diamond has no target
        for (var s : list) {                    // String
            i += s.length();
        }
        BiFunction<Integer, Integer, Integer> add = (var a, var b) -> a + b;
        return i + objects.size() + add.apply(1, 2);
    }

    // var field = 1;                 // illegal: not a local
    // var f() { return 0; }          // illegal: return type
    // void m(var x) {}               // illegal: method parameter
    // var e;                         // illegal: no initializer
    // var f = { 6 };                 // illegal: array initializer
    // var d[] = new int[4];          // illegal: brackets on the name
    // var b = 2, c = 3.0;            // illegal: multiple declarators
    // var g = (g = 7);               // illegal: self-reference
    // var n = null;                  // illegal: null type
    // var lam = () -> "hello";       // illegal: lambda needs a target type
}
```

**Listing 1.** `var i = 0` matches `int i = 0`. Diamond without a type argument infers `Object`. Commented lines are compile errors.

If the compiler cannot produce a type, the declaration does not compile (javac often reports that it cannot infer the type of the local). Locals still have **no default**; inference does not skip definite assignment ([[Why must a local primitive variable be initialized before use in Java]], [[How would you explain kinds of variables in Java such as local and instance]]). Some inferred types are not denotable as a written name (intersection types, anonymous classes); `var` is the only way to name those locals.

> [!warning] `var` is not a keyword and not `Object`
> Code that used `var` as a **variable or method** name still compiles. A type named `var` does not. The local still has a **concrete** compile-time type; you cannot assign a `String` to a `var i = 0` later. `var` on a field or a method signature is not LVTI.

> [!warning] Diamond plus `var` infers `ArrayList<Object>`
> `var list = new ArrayList<>()` is legal and usually **wrong** for a `String` list. The dump claim that generics cannot use `<>` with `var` is the wrong diagnosis. Write `new ArrayList<String>()` on the right, or `List<String> list = new ArrayList<>()` on the left. `var` also rejects `null`, lambdas, method references, `{ … }` array initializers, `var x[]`, multiple names in one declaration, and an initializer that mentions the variable being declared.

> [!tip] Interview answer
> **From Java 10, `var` infers a local’s type from its initializer — `var i = 0` is `int i = 0`. It is a reserved type name, not a keyword, and it does not apply to fields or method signatures.** Java 11 lets you write `var` on every parameter of an implicitly typed lambda. Diamond still works; without a type argument you get `ArrayList<Object>`, and `null` or a lambda initializer does not compile.
