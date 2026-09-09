<!--
reps: 0
priority: 0
-->
#Java/Generics #SRS

# What are generics in Java

> [!abstract] Short answer
> Generics are compile-time parameters for types and methods: a generic declaration takes type parameters (`class Box<T>`), and each use supplies type arguments (`Box<String>`). The compiler checks every use against the argument, so wrong element types fail to compile instead of throwing `ClassCastException` in production, and use-site casts disappear.

A generic class or interface defines a family of **parameterized types**. `List<String>` and `List<Integer>` are two parameterizations of the same generic interface `List`, each fixing what `E` means inside that use. A generic method works the same way at method level: `static <T> T pick(T a, T b)` introduces its own type parameter, independent of the class.

## Type parameters and parameterized types

The type parameter is written in angle brackets after the name; the type argument must be a reference type — primitives are not valid arguments (`List<int>` is illegal, use `List<Integer>` and pay for [[How does adding an int to an ArrayList of Integer autobox]] boxing). If a parameter declares a bound (`<T extends Number>`), arguments are restricted to that bound and unbounded parameters behave as `Object`. Generics arrived in [[In which Java version were generics introduced|Java 5]].

```d2
direction: right
decl: "class Box<T>\n(type parameter)" {
  width: 240
  height: 90
  style.fill: "#e3f2fd"
}
use: "Box<String> b\n(type argument)" {
  width: 230
  height: 90
  style.fill: "#fff3e0"
}
check: "Compiler: put(String) ok\nput(Integer) rejected" {
  width: 290
  height: 90
  style.fill: "#e8f5e9"
}
run: "Runtime: plain Box\ntype argument erased" {
  width: 240
  height: 90
  style.fill: "#ffebee"
}
decl -> use: instantiate
use -> check: every call checked
check -> run
```

**Fig. 1.** A type parameter on the declaration becomes a fixed argument at each use; checks are compile-time only, and the argument does not survive to runtime.

## Compile-time safety instead of runtime casts

Reading back needs no cast, and inserting a wrong type is a compile-time error, not a runtime surprise:

```java
import java.util.ArrayList;
import java.util.List;

public class GenericsDemo {

    static class Box<T> {
        private T value;
        void put(T value) { this.value = value; }
        T get() { return value; }
    }

    static <T> T pick(T a, T b) { return b; }

    public static void main(String[] args) {
        Box<String> box = new Box<>();
        box.put("42");
        String s = box.get();          // no cast needed
        System.out.println(s.length()); // 2 characters

        List<String> words = new ArrayList<>();
        words.add("generics");
        // words.add(42);  // compile-time error, not a runtime ClassCastException

        String chosen = pick("a", "b"); // T inferred as String
        System.out.println(chosen);
    }
}
```

**Listing 1.** A generic class and a generic method: the compiler knows what `T` is at each use site.

## What generics do not change

A parameterized type is still one class at runtime — [[How does type erasure work for Java generics]] explains how the compiler deletes type arguments before bytecode is emitted. Two consequences interviewers probe: `List<String>` is **not** a subtype of `List<Object>` (see [[How would you explain wildcard bounded and unbounded types in Java generics]] for the wildcard mechanism that restores flexibility), and collections still need wrapper objects, so [[Why cannot Java collections store primitive types]] stays true. Records, enums, and classes can all declare type parameters — [[Can a Java record be generic]].

> [!warning] Raw types silently switch checks off
> Using `List` without arguments (a raw type) compiles, but turns every parameterized operation into unchecked: you lose compile-time safety and collect `unchecked` warnings plus deferred `ClassCastException` risk. Always supply type arguments (`List<String>`); a bare `List` is legacy pre-Java-5 style, not a shortcut.

> [!tip] Interview answer
> Generics parameterize types and methods so the compiler can enforce element types: `List<String>` only accepts strings, reads need no cast, and mistakes fail at compile time. Declarations take type parameters, uses supply type arguments, bounds restrict them. At runtime the arguments are erased, which is why `List<String>` and `List<Integer>` are the same class — the safety is purely a compile-time contract.

