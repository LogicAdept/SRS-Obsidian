<!--
reps: 0
priority: 0
-->
#Java/Generics #Java/Versions/5 #SRS

# In which Java version were generics introduced

> [!abstract] Short answer
> **Java 5 (J2SE 5.0 / JDK 5.0 / `@since 1.5`).** They are the JSR 14 type-system addition: a type or method can work on many types with **compile-time** checks. They are not a Java 8 feature, not C++ templates, and they do not exist on a pre-5.0 VM.

## JDK 5 type parameters, then erasure

The JDK 5 language guide lists **Generics** first among the 5.0 enhancements: compile-time type safety for the Collections Framework and an end to most element casts. The same release added the enhanced `for`, autoboxing, enums, varargs, static import, and annotations ([[In which Java version were enums introduced]], [[In which Java version were autoboxing and unboxing introduced]]). Assertions were earlier — JDK 1.4 ([[In which Java version was the assert keyword introduced]]).

Write `Collection<String>` (“collection of String”). The compiler checks inserts and inserts the casts on the way out. A program that compiles without unchecked warnings will not throw `ClassCastException` from those generated casts. Raw types remain legal so generic code can talk to pre-5 libraries ([[What is generics]], [[How would you explain parameterized types and generics in Java]]).

Implementation is **type erasure**: parameters exist at compile time and are erased afterward. There is no new class per `List<String>` vs `List<Integer>`. You cannot ask the VM for `T` at run time the way C++ templates specialize. That is the interop story with legacy collections — and the reason `Collections.checkedSet` (and friends) exist if you must catch a bad insert at the boundary ([[How would you explain type erasure for Java generics]], [[How does type erasure work for Java generics]]).

`Class` was generified (`Class<T>`). Holder types such as `ThreadLocal` and `WeakReference` were too. You must not compile Tiger/5 language features if the bytecode has to run on a pre-5.0 VM.

```d2
direction: down
pre: "Through 1.4\nraw Collection + casts" {
  width: 280
  height: 55
  style.fill: "#fff3e0"
}
v5: "Java 5 / J2SE 5.0 / JDK 1.5\nJSR 14 generics + erasure" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}

pre -> v5: "parameterized types"
```

**Fig. 1.** Generics are a 5.0 language feature. `List` as a type is older (Collections Framework); `List<E>` is 5.

```java
import java.util.Collection;
import java.util.Iterator;

class Demo {
    static void raw(Collection c) {
        for (Iterator i = c.iterator(); i.hasNext(); ) {
            String s = (String) i.next(); // unchecked by the compiler
        }
    }

    static void generic(Collection<String> c) {
        for (Iterator<String> i = c.iterator(); i.hasNext(); ) {
            i.next().length(); // no cast
        }
    }
}
```

**Listing 1.** Same loop. `Collection<String>` moves the element type into the signature. Bytecode after erasure still looks like a raw collection plus casts.

> [!warning] Not Java 8, not templates
> Interview answers that pin generics on lambdas/streams (8) or on C++-style reification are wrong. Erasure means `new T[]` and `instanceof List<String>` are not the model. Raw types still compile; mixing them with parameterized types is where the surprise `ClassCastException` comes back.

> [!tip] Interview answer
> **Generics arrived in Java 5 (J2SE 5.0, JSR 14).** `List<E>`, generic methods, and erasure. Same release as enums, autoboxing, and enhanced `for`. Java 8 did not introduce them.
