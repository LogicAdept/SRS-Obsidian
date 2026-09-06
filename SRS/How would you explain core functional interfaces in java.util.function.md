<!--
reps: 0
priority: 0
-->
#Java/FunctionalInterfaces #Java/Lambdas #SRS

# How would you explain core functional interfaces in java.util.function?

> [!abstract] Short answer
> **Four basic shapes, then arity and operators.** `Function<T,R>` is `T` → `R`. `Consumer<T>` is `T` → `void`. `Predicate<T>` is `T` → `boolean`. `Supplier<R>` is `()` → `R`. `UnaryOperator<T>` extends `Function<T,T>`; `BinaryOperator<T>` extends `BiFunction<T,T,T>`. The package (Java 8) is **not** every possible SAM — it covers common JDK and user needs. `@FunctionalInterface` documents intent; it is not what makes the type a lambda target.

## Four shapes, then names

Functional interfaces in this package are **target types** for lambdas and method references. The lambda’s parameters and return are matched to the **functional method**. That works in assignment, invocation, and cast contexts (`Predicate<String> p = String::isEmpty`, `stream.filter(...)`, a cast to `ToIntFunction`). A method that “applies the provided function” means a **non-null** implementation unless the API says otherwise ([[What is functional interface]]).

The package names four **basic** shapes:

| Shape | Meaning | SAM |
| --- | --- | --- |
| `Function<T,R>` | unary `T` → `R` | `apply` |
| `Consumer<T>` | unary `T` → `void` (side effects) | `accept` |
| `Predicate<T>` | unary `T` → `boolean` | `test` |
| `Supplier<R>` | nullary → `R` | `get` |

`BiFunction` / `BiConsumer` / `BiPredicate` are the same ideas with a **Bi** arity prefix. `UnaryOperator` is `Function` where operand and result are the same type (`apply` unchanged; extra static `identity()`). `BinaryOperator` is `BiFunction<T,T,T>` ([[How would you explain BinaryOperator DoubleBinaryOperator IntBinaryOperator and LongBinaryOperator]], [[How does Supplier differ from Consumer in Java]]).

```d2
direction: down
four: "Function · Consumer\nPredicate · Supplier" {
  width: 280
  height: 55
  style.fill: "#e8f5e9"
}
arity: "BiFunction / BiConsumer / BiPredicate" {
  width: 300
  height: 45
  style.fill: "#e3f2fd"
}
ops: "UnaryOperator · BinaryOperator" {
  width: 280
  height: 45
  style.fill: "#fff3e0"
}
prim: "ToInt… / Int… / ObjInt…" {
  width: 260
  height: 45
  style.fill: "#f3e5f5"
}
four -> arity: "arity prefix"
four -> ops: "same-type derived"
four -> prim: "primitive prefixes"
```

**Fig. 1.** Core catalog: four shapes, then arity, same-type operators, primitive name prefixes. Stream `filter` is a `Predicate`; `map` is a `Function` ([[Which functional interface represents a filter or predicate in the Stream API]], [[Which functional interface does Stream map use]]).

Primitive specializations are **separate types**, named left-to-right: `ToIntFunction` specializes the **return**; `DoubleConsumer` / `ObjIntConsumer` specialize arguments (`Obj` means “leave this parameter as a reference and continue”). Combine them (`IntToDoubleFunction`). If every argument already has a prefix, the arity prefix may be omitted (`ObjIntConsumer`). They do not extend the boxed `Function` / `Consumer` / … types ([[How would you explain Consumer DoubleConsumer IntConsumer and LongConsumer]], [[How would you explain Function DoubleFunction IntFunction and LongFunction variants]]).

`Predicate` adds short-circuit `and` / `or` (skip the other side; `NullPointerException` if `other` is null), `negate`, `isEqual` (`Objects.equals`, target may be `null`), and `Predicate.not` (**since 11**). `Supplier.get()` need not return a new object. `Consumer` is expected to work by side effects. `Function` has `compose` / `andThen` / `identity`.

The package is **not** a complete set of SAM shapes. `Comparator`, `Runnable`, `Callable`, `FileFilter`, and many others stay next to the API that uses them. A no-arg `boolean` result is `BooleanSupplier`, not `Predicate`. Do not invent a parallel `Function2` when `BiFunction` already exists. `@FunctionalInterface` is on these types as a design check; any single-abstract-method interface is still a lambda target without it.

```java
import java.util.function.Consumer;
import java.util.function.Function;
import java.util.function.Predicate;
import java.util.function.Supplier;
import java.util.function.UnaryOperator;
import java.util.stream.Stream;

class Demo {
    static void cores() {
        Predicate<String> empty = String::isEmpty;
        Function<String, Integer> len = String::length;
        Consumer<Integer> sink = n -> { };
        Supplier<String> supply = () -> "x";
        UnaryOperator<String> id = UnaryOperator.identity();

        Stream.of("a", "").filter(empty.negate()).map(len).forEach(sink);
        Predicate<String> both = empty.and(s -> s.length() == 0);
        Predicate<String> eqNull = Predicate.isEqual(null);
        Predicate<String> nonempty = Predicate.not(empty); // Java 11
        String same = id.apply("z");
        // Predicate.not(null); // NPE
    }
}
```

**Listing 1.** Assignment targets for the four basic shapes plus `UnaryOperator.identity`. `filter` / `map` / `forEach` are the package’s own invocation-context examples. `Predicate.not` is Java 11; the rest of this package is Java 8. Predicate combinators in detail: [[How would you explain Predicate DoublePredicate IntPredicate and LongPredicate]].

> [!warning] `@FunctionalInterface` does not create the SAM
> The compiler already treats one-abstract-method types as functional. The annotation only fails the build if you then add a second abstract method. These types also do **not** cover every shape you might write — `FileFilter` lives with I/O, `Comparator` / `Runnable` / `Callable` live with their APIs, and a custom SAM is still a lambda target.

> [!warning] Names are not subtypes
> `IntPredicate` is not a `Predicate<Integer>`. `UnaryOperator<T>` **is** a `Function<T,T>`; `IntUnaryOperator` is not a `UnaryOperator<Integer>`. `and` / `or` throw if the other predicate is null, and they **skip** the other side on a decided `false` / `true`. Passing `null` where an API “accepts a function” is a `NullPointerException` unless that method documents nullity.

> [!tip] Interview answer
> **`java.util.function` is four shapes: `Function` (`apply`), `Consumer` (`accept`), `Predicate` (`test`), `Supplier` (`get`).** `UnaryOperator` / `BinaryOperator` are same-type `Function` / `BiFunction`; `Bi*` raises arity; `ToInt` / `Int` / `Obj` prefixes specialize primitives as **new** types. The package is Java 8, common SAMs for lambdas, not a closed catalog, and `@FunctionalInterface` is optional documentation.
