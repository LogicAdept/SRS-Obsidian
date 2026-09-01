<!--
reps: 0
priority: 0
-->
#Java/Annotations #SRS

# How do Java annotation retention policies work?

> [!abstract] Short answer
> `@Retention` names a `RetentionPolicy` that decides **where an annotation still exists**. **SOURCE** is discarded by the compiler (not in the class file). **CLASS** is written to the class file but **need not** be kept by the VM, so `getAnnotation` cannot see it. **RUNTIME** is in the class file **and** made available by the reflection libraries. Omit `@Retention` and the policy is **CLASS**.

## Three policies, one meta-annotation

`@Retention` applies to an annotation **interface**. Its `value` is one of:

| Policy | After `javac` | Core reflection (`AnnotatedElement`) |
| --- | --- | --- |
| `SOURCE` | **Not** in the binary | No |
| `CLASS` | In the class file (usual case) | No |
| `RUNTIME` | In the class file | **Yes** — `getAnnotation` / `getAnnotationsByType` |

```java
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.TYPE)
public @interface Audited {}
```

**Listing 1.** Runtime-visible marker. Drop `@Retention` and `Audited` defaults to **CLASS** — `Class.getAnnotation(Audited.class)` returns `null` even though the class file still carries it. See [[What happens if you omit Retention on a custom annotation]].

Platform examples:

- **SOURCE** — `@Override`, `@SuppressWarnings` (compiler-only checks / warning suppression)
- **RUNTIME** — `@Deprecated` (`@Retention(RUNTIME)` in the JDK). Runtime frameworks that call `getAnnotation` need this policy too

`@Retention` on a type used only as a **nested member** of another annotation does **not** control that nested value. Retention of the **outer** annotation instance is what the compiler and VM honor.

```d2
direction: right
src: "source\nall three policies" {
  width: 190
  height: 70
  style.fill: "#e3f2fd"
}
source: "SOURCE\ndiscarded" {
  width: 160
  height: 70
  style.fill: "#ffebee"
}
klass: "CLASS\n.class only" {
  width: 160
  height: 70
  style.fill: "#fff3e0"
}
rt: "RUNTIME\n.class + VM" {
  width: 180
  height: 70
  style.fill: "#e8f5e9"
}

src -> source
src -> klass
src -> rt
```

**Fig. 1.** Same `@Foo` syntax; the policy picks which artifacts still contain it.

## Who can still read it

- **Annotation processors** see SOURCE, CLASS, and RUNTIME while the **language model** is built from source. SOURCE **cannot** be recovered from a class file — a processor that needs SOURCE must see **source**, not a `.class` from an earlier compile. Details: [[How do annotation processors differ from runtime reflection]].
- **Class-file readers** can see CLASS and RUNTIME (they are in the binary).
- **`AnnotatedElement`** sees **RUNTIME** only. Lookup: [[How do you retrieve annotations at runtime]].

A local-variable annotation, or an annotation on a **lambda** formal parameter, is **never** kept in the binary — even if the interface is CLASS or RUNTIME. (A **type-use** annotation on the type of that variable or parameter can still be stored when the policy allows.)

> [!warning] CLASS is not “almost RUNTIME”
> Frameworks that reflect with `getAnnotation` need **RUNTIME**. CLASS is the **language default**, not a runtime-visible default. Flattening retention to “in the class file or not” **collapses CLASS and RUNTIME** — **both** are in the binary; the interview distinction is **reflection**. SOURCE never appears in bytecode; CLASS usually does, and still returns `null` from `getAnnotation`. Pairing SOURCE/CLASS with a runtime reader is a silent miss, not a compile error. Compiler-only example: [[How does the Override annotation work]].

> [!tip] Interview answer
> Retention is how long the annotation is kept: SOURCE dies at compile time, CLASS lives in the class file but not for reflection, RUNTIME is what getAnnotation can read. The default if you omit @Retention is CLASS, which is why a custom annotation often “disappears” at runtime until you set RUNTIME. Processors can still see SOURCE from source; they cannot fish it out of a .class.
