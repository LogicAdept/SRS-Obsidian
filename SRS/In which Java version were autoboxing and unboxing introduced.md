<!--
reps: 0
priority: 0
-->
#Java/Language/Wrappers/Autoboxing #Java/Language/Primitives #Java/Versions/5 #SRS

# In which Java version were autoboxing and unboxing introduced?

> [!abstract] Short answer
> **Java 5** (JDK 1.5, J2SE 5.0), as a language feature under **JSR 201**. From that release the compiler inserts boxing and unboxing conversions (`Integer j = a;` → `Integer.valueOf(a)`, `int i = wrapper;` → `wrapper.intValue()`). Before 5.0 you converted by hand, typically `new Integer(i)` and `xxxValue()`.

## Java 5 language feature, not a later library add-on

J2SE 5.0’s new-features list names **Autoboxing/Unboxing** among the Java language features introduced since 1.4, with the dedicated guide “This facility eliminates the drudgery of manual conversion between primitive types (such as `int`) and wrapper types (such as `Integer`). Refer to JSR 201.” The same JDK 5 enhancements page lists it next to the enhanced `for` loop, enums, varargs, and static import (all JSR 201). **Generics** arrived in the same product release (JSR 14), which is why interview lists often name them together — they are sibling 5.0 features, not the same JSR.

The compiler applies those conversions when a primitive is assigned to the matching wrapper, or passed where the wrapper is required (and the reverse for unboxing). That is [[What are autoboxing and unboxing in Java]] / [[When does autoboxing occur in Java]]: `List<Integer>` plus `add(i)` became legal without an explicit box, which is why 5.0’s collections notes call autoboxing one of the three language features aimed at collections.

```d2
direction: down
pre: "Java 1.4 and earlier\nnew Integer(i) / i.intValue()" {
  width: 320
  height: 80
  style.fill: "#fff3e0"
}
v5: "Java 5 / JDK 1.5 / J2SE 5.0\nJSR 201 autoboxing & unboxing" {
  width: 340
  height: 80
  style.fill: "#e8f5e9"
}
code: "Integer j = a;\nint i = wrapper;" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}

pre -> v5: "compiler inserts conversions"
v5 -> code
```

**Fig. 1.** The language change is 5.0; the inserted calls are the old wrapper factories and `xxxValue` methods.

```java
int a = 7;
Integer j = a;          // Java 5+: Integer.valueOf(a)
int i = j;              // Java 5+: j.intValue()

Integer old = new Integer(a); // pre-5 style; constructor deprecated since 9
int raw = old.intValue();
```

**Listing 1.** Conceptual: assignment boxing/unboxing vs the explicit conversions 5.0 automated.

`Integer.valueOf(int)` is marked **since 1.5** — the factory autoboxing uses. `intValue()` and the type itself are older (`Integer` since 1.0). So “before 5 you used `valueOf`” is the wrong memory: **`valueOf(int)` is a 5.0 API**; pre-5 code used `new Integer(int)`.

> [!warning] 5.0, not 8, and not “just a method”
> Autoboxing is a **compiler conversion** added with J2SE 5.0. Java 8 lambdas / streams did not introduce it. You still cannot write `List<int>` after 5.0; generics still need reference types, which is why boxing exists.

> [!warning] Same release as generics does not make them one feature
> Generics (JSR 14) and autoboxing (JSR 201) shipped together so `Map<String, Integer>` and `m.put(word, freq + 1)` work without manual `Integer` plumbing. They remain separate specifications. Unboxing `null` still throws `NullPointerException`; `==` on two `Integer`s is still reference identity — 5.0 did not turn wrappers into primitives.

> [!tip] Interview answer
> **Autoboxing and unboxing arrived in Java 5 (JDK 1.5 / J2SE 5.0) via JSR 201.** The compiler inserts `valueOf` / `xxxValue` so you can assign `int` ↔ `Integer`. Before that you boxed with `new Integer` and unboxed with `intValue()`; `Integer.valueOf(int)` itself is a 1.5 factory.
