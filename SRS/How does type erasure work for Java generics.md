<!--
reps: 0
priority: 0
-->
#Java/Generics #SRS

# How does type erasure work for Java generics

> [!abstract] Short answer
> The compiler maps every generic type to its erasure: a parameterized type `G<...>` becomes the raw `G`, a type variable becomes the erasure of its leftmost bound (usually `Object`), and `T[]` becomes `|T|[]`. It then inserts casts at use sites and bridge methods where overriding needs them, so bytecode contains no type arguments at all.

Erasure exists for migration compatibility: pre-Java-5 bytecode and libraries keep working unchanged, and every program compiled before generics still runs on a modern JVM. The price is that type arguments are a compile-time contract only — the runtime never sees them.

## The erasure mapping

The compiler applies three rules: the erasure of `G<T1,...,Tn>` is `G`; the erasure of a type variable is the erasure of its leftmost bound (`<T>` erases to `Object`, `<T extends Number>` to `Number`); the erasure of `T[]` is the array of erased `T`. Method signatures erase the same way — `void add(String)` on `ArrayList<String>` is really `add(Object)` in the class file.

```d2
direction: right
src: "Source with generics\nList<String>, T extends Number" {
  width: 280
  height: 100
  style.fill: "#e3f2fd"
}
check: "Type check against\ntype arguments" {
  width: 250
  height: 90
  style.fill: "#fff3e0"
}
erase: "Erase: List<String> -> List\nT -> leftmost bound" {
  width: 290
  height: 100
  style.fill: "#fff3e0"
}
synth: "Insert casts and\nbridge methods" {
  width: 270
  height: 100
  style.fill: "#e8f5e9"
}
run: "Bytecode: raw types only\none class per generic type" {
  width: 290
  height: 100
  style.fill: "#ffebee"
}
src -> check
check -> erase
erase -> synth
synth -> run
```

**Fig. 1.** Generics live only in the first stage: the compiler checks, erases, and synthesizes; the JVM runs raw classes.

## What the compiler inserts

At a use site like `String s = list.get(0)` the compiler inserts the downcast that the programmer no longer writes. When a subclass overrides a generic method with a specialized signature, the compiler adds a synthetic **bridge method** with the erased signature that delegates to the real one. Both mechanisms are why erased code still behaves as if types were tracked:

```java
import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.List;

public class ErasureDemo {

    public static void main(String[] args) {
        List<String> strings = new ArrayList<>();
        List<Integer> numbers = new ArrayList<>();

        // One Class object for every parameterization of ArrayList:
        System.out.println(strings.getClass() == numbers.getClass()); // true
        System.out.println(strings.getClass().getName());            // java.util.ArrayList

        // Erased method signature: add(Object), not add(String):
        for (Method m : strings.getClass().getMethods()) {
            if (m.getName().equals("add") && m.getParameterCount() == 1) {
                System.out.println(m.getParameterTypes()[0].getName()); // java.lang.Object
            }
        }

        // new ArrayList<String>().getClass() also equals the raw class:
        System.out.println(new ArrayList<String>().getClass() == new ArrayList<Integer>().getClass()); // true
    }
}
```

**Listing 1.** Every parameterization shares one runtime class, and the element type of `add` is erased to `Object`.

## What erasure forbids

Because `T` does not exist at runtime, `new T()`, `new T[...]`, `x instanceof List<String>`, and generic exception classes are compile-time errors. Primitive type arguments are also impossible, which is the root of [[Why does type erasure prevent a List of int in Java]]. `instanceof List<?>` is legal because a parameterized type with only unbounded wildcards is reifiable — runtime-fully-known. Overloads differing only in type arguments clash after erasure (`void f(List<String>)` vs `void f(List<Integer>)`), since both erase to the same descriptor.

> [!warning] Unchecked casts defer the failure away from the bug
> A cast from a raw or unrelated parameterized type compiles with only an `unchecked` warning — the compiler trusts you, inserts no element checks, and [[When can a ClassCastException be thrown in Java|the exception]] explodes later at a random read site, far from the code that actually violated the contract. Treat `unchecked` warnings as errors in code review; erasure means nothing will catch this at the boundary.

> [!tip] Interview answer
> Erasure is how the compiler implements generics for a JVM that runs raw classes: type arguments are checked and then deleted — `G<String>` becomes `G`, `T` becomes its leftmost bound — while the compiler re-inserts casts at use sites and bridge methods for overriding. That is why `ArrayList<String>` and `ArrayList<Integer>` share one `Class`, why `new T()` and `instanceof List<String>` do not compile, and why an unchecked cast can push a `ClassCastException` far away from the faulty line.

