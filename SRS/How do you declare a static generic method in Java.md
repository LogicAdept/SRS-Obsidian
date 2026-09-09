<!--
reps: 0
priority: 0
-->
#Java/Generics #SRS

# How do you declare a static generic method in Java

> [!abstract] Short answer
> Declare the type parameters in angle brackets between the modifiers and the return type — `static <T> T pick(T a, T b)` — and the compiler infers `T` from the arguments and target type at each call. Static members cannot use the class's own type parameters, so a static method that needs a variable type must declare its own.

The parameter list `<T extends B>` is identical in shape to a generic class header (see [[What is the purpose of type bounds in Java generics]]), but it belongs to the method: each call supplies — implicitly or explicitly — its own argument, and different calls of one method can use unrelated types.

## Anatomy of a generic method

Modifiers come first, then the type parameter section, then the return type, name, and parameters. The type parameter scopes over the return type and the whole parameter list, so `<T> List<T> singleton(T value)` connects argument and result. An instance method may also reference the class's type parameters alongside its own:

```d2
direction: right
mods: "static\n(modifiers)" {
  width: 180
  height: 80
  style.fill: "#e3f2fd"
}
tparam: "<T extends Comparable<T>>\n(type parameter section)" {
  width: 320
  height: 90
  style.fill: "#fff3e0"
}
ret: "List<T>\n(return type may use T)" {
  width: 250
  height: 90
  style.fill: "#e8f5e9"
}
params: "(T value, ...)\n(parameters may use T)" {
  width: 280
  height: 90
  style.fill: "#ffebee"
}
mods -> tparam
tparam -> ret
ret -> params
```

**Fig. 1.** The type parameter section sits between modifiers and return type and scopes over everything after it.

## Inference and explicit type witnesses

Normally the compiler infers the argument: `singleton("hi")` yields `List<String>`, and target typing picks it up from assignment context — the same mechanism that makes `List<String> s = Collections.emptyList()` type-safe. When inference has nothing to grip on or you want to force a wider type, supply the witness explicitly: `Collections.<String>emptyList()` or `this.<Number>singleton(42)`. A static method with a bound works like any generic method — the bound both restricts callers and unlocks body operations:

```java
import java.util.ArrayList;
import java.util.List;

public class StaticGenericDemo {

    // Type parameter declared before the return type:
    static <T> List<T> singleton(T value) {
        List<T> one = new ArrayList<>();
        one.add(value);
        return one;
    }

    static <T extends Comparable<T>> T firstOf(List<? extends T> items) {
        T best = items.get(0);
        for (T item : items) best = best.compareTo(item) >= 0 ? best : item;
        return best;
    }

    public static void main(String[] args) {
        List<String> words = singleton("hello");     // T inferred as String
        System.out.println(words.get(0).length());  // 5

        // Explicit type witness, same shape as Collections.<String>emptyList():
        List<Number> nums = StaticGenericDemo.<Number>singleton(42);
        System.out.println(nums.get(0)); // 42

        Integer top = firstOf(List.of(3, 9, 1)); // T inferred as Integer
        System.out.println(top); // 9

        // static T field; // compile-time error: no instance of the class T in static context
    }
}
```

**Listing 1.** Inference from arguments, an explicit witness, and a bounded static generic method.

## Why static fields cannot join in

A class type parameter like `class Holder<T>` describes the type of an **instance**: `Holder<String>` and `Holder<Integer>` are different parameterizations of one class, each with its own fields. Static members exist once per class, independent of any parameterization, so `static T field;` does not compile — [[How does type erasure work for Java generics]] removes the argument from the class entirely. A static method may declare its **own** `<T>`, which then has nothing to do with any `Holder<T>` parameterization.

> [!warning] A method type parameter shadows the class one
> Inside `class C<T>`, writing `static <T> void f(T x)` introduces a *different* `T` — and for instance methods a fresh `T` hides the class parameter silently, which confuses readers and reviewers. Either rename the method's parameter or drop it and use the class one (only possible for instance methods). And remember the classic error: `static T f()` **without** its own `<T>` never compiles in a generic class — static context has no type parameter.

> [!tip] Interview answer
> Put the type parameters right after the modifiers: `static <T> T foo(...)`. The compiler infers `T` from arguments and target type, or you force it with a witness like `Collections.<String>emptyList()`. Static methods cannot use the class's type parameters — those belong to instances — so a static member declares its own, and a static field typed by the class parameter is a compile error. Bounds work the same as on classes and make the body's operations available.

