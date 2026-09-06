<!--
reps: 0
priority: 0
-->
#Java/MethodReferences #Java/Lambdas #Java/Versions/8 #SRS

# What kinds of method references exist in Java?

> [!abstract] Short answer
> **Four source kinds, plus `::new` for arrays and `super::`.** Static: `Class::staticMethod`. Bound instance: `expr::instanceMethod`. Unbound instance: `Type::instanceMethod` (receiver is the first SAM argument). Constructor: `Class::new`. Java 8. `int[]::new` is array creation; `super::name` / `Outer.super::name` are the `super` forms. All of them are poly expressions that become a functional-interface instance without calling the method yet.

## Four kinds, then the extra JLS forms

A method reference names an invocation (or a construction) without performing it. The target functional interface supplies the argument types for overload resolution — you cannot write `Arrays::sort(int[])` ([[What is method reference]], [[How would you explain Java method references and their bytecode form]], [[What is functional interface]]). Interview lists often name **three** kinds and fold bound plus unbound into one “instance” line; split those two.

| Kind | Syntax | What the SAM arguments mean |
| --- | --- | --- |
| Static method | `ContainingClass::staticMethod` | all SAM args → method args |
| Bound instance | `expr::instanceMethod` | SAM args → method args; receiver is `expr` |
| Unbound instance | `ContainingType::instanceMethod` | **first** SAM arg is the receiver |
| Constructor | `ClassName::new` | SAM args → constructor args |

`Person::compareByAge` is `(a, b) -> Person.compareByAge(a, b)`. `myApp::appendStrings2` is `(a, b) -> myApp.appendStrings2(a, b)`. `String::compareToIgnoreCase` is `(a, b) -> a.compareToIgnoreCase(b)`. `HashSet::new` is `() -> new HashSet<>()`. Bound `System.out::println` is the particular-object kind ([[What does the System.out println method reference mean]]).

```d2
direction: down
kinds: "static · bound · unbound · ::new" {
  width: 300
  height: 45
  style.fill: "#e8f5e9"
}
extra: "ArrayType::new\nsuper:: / Type.super::" {
  width: 280
  height: 50
  style.fill: "#fff3e0"
}
tgt: "functional interface\n(assignment / invocation / cast)" {
  width: 300
  height: 50
  style.fill: "#e3f2fd"
}
kinds -> tgt
extra -> tgt
```

**Fig. 1.** Tutorial four kinds plus constructor/array/`super` forms from the language. Same target-typing as a lambda ([[How would you explain lambda expressions in Java]]).

JLS also allows:

- **`ArrayType::new`** — always exact; notional method is one `int` (length) and returns that array type (`int[]::new`). The type must be reifiable.
- **`super::identifier`** / **`TypeName.super::identifier`** — invocation mode `super`; illegal in a static context; the compile-time declaration must not be `abstract`.
- Generic explicit type args: `Arrays::<String>sort`, `Foo::<Integer>new`.

`ReferenceType::identifier` is searched twice (arity `n` and `n-1`) because it might be **static** or **unbound instance**. If both apply, it is a compile-time error (`C::size` with `size()` and `static size(Object)`). Bound `expr::m`: `expr` is evaluated **immediately**; `null` throws `NullPointerException` then. Unbound `String::length` has no qualifier to NPE at creation.

```java
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.function.Function;
import java.util.function.IntFunction;
import java.util.function.Supplier;
import java.util.function.ToIntFunction;

class Demo {
    static int sum(int a, int b) {
        return a + b;
    }

    static void kinds() {
        Supplier<List<String>> ctor = ArrayList::new;
        Supplier<HashSet<String>> ctor2 = HashSet::new;
        ToIntFunction<String> unbound = String::length;
        Function<String, String> bound = "x"::concat;
        java.util.function.IntBinaryOperator stat = Demo::sum;
        IntFunction<int[]> arrayCtor = int[]::new;
        int[] buf = arrayCtor.apply(3);
        String[] names = { "b", "a" };
        Arrays.sort(names, String::compareToIgnoreCase);
        List<String> list = ctor.get();
        int n = unbound.applyAsInt("ab");
        String xy = bound.apply("y"); // "xy"
    }
}
```

**Listing 1.** Constructor, unbound instance, bound instance (`"x"::concat`), static method, array `::new`. `String::compareToIgnoreCase` is the unbound kind used as a `Comparator`.

> [!warning] `Type::name` is not always unbound instance
> If `Type` also has a matching **static** method, the reference is ambiguous and does not compile. Bound `expr::m` cannot refer to a `static` method; a null `expr` NPEs when the reference is created, not when the SAM is later invoked.

> [!warning] Constructor references are not a fifth unrelated feature
> `Class::new` is a method reference whose compile-time declaration is a notional constructor. Inner-class `Outer.Inner::new` still needs the enclosing instance from the site. You cannot pick an overload with `Foo::new(int)` — the target SAM does that. Use a lambda when overload resolution on `::` is not enough.

> [!tip] Interview answer
> **Four kinds: static `Class::m`, bound `obj::m`, unbound `Type::m` (receiver first), and `Class::new`.** Add `int[]::new` and `super::m`. They are named one-call lambdas; the functional interface chooses the overload. Bound receivers are evaluated immediately; `Type::m` is an error if both a static and an instance method apply.
