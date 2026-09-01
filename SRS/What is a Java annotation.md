<!--
reps: 0
priority: 0
-->
#Java/Annotations #SRS

# What is a Java annotation?

> [!abstract] Short answer
> An annotation is a **marker that associates information with a program element**. It denotes an instance of an **annotation interface** (`@interface`) and usually supplies element values. It is **not** part of the algorithm: by itself it has **no effect at run time** until a compiler, processor, or reflective reader acts on it.

## A specialized interface, since Java 5

An annotation interface is declared with `@` immediately before `interface`. It is a specialized interface whose only direct superinterface is `java.lang.annotation.Annotation`. You **cannot** write `extends` on `@interface`: [[Can you extend an annotation type in Java]]. The type and the facility appear in the platform **since 1.5** (`Annotation`, `@Override`, `@Target`, `@Retention`).

```java
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.TYPE)
public @interface Audited {
    String value() default "";
}

@Audited("payments")
public class Ledger {}
```

**Listing 1.** Declaration (`@interface`) and use (`@Audited`). Meta-annotations such as `@Target` / `@Retention` configure the type: [[What are meta-annotations in Java]], [[How do you declare a custom annotation in Java]].

Three things actually **consume** annotations:

1. **The compiler** — e.g. `@Override` errors, `@SuppressWarnings` (SOURCE).
2. **Annotation processors** — `javax.annotation.processing.Processor` during compilation (generate sources, fail the build).
3. **Runtime reflection** — `AnnotatedElement.getAnnotation`, only with **RUNTIME** retention.

They do not “run” the annotated method by themselves: [[Why do annotations have no direct effect on annotated code]], [[How do annotation processors differ from runtime reflection]].

Java **8** added **repeating** annotations (`@Repeatable`) and **type-use** annotations (`ElementType.TYPE_USE`): [[How are repeating annotations stored for compatibility]], [[How does TYPE_USE differ from TYPE as an annotation target]].

```d2
direction: right
anno: "@Audited on Ledger" {
  width: 180
  height: 70
  style.fill: "#e3f2fd"
}
tools: "javac / Processor" {
  width: 180
  height: 70
  style.fill: "#fff3e0"
}
rt: "getAnnotation\n(RUNTIME only)" {
  width: 180
  height: 70
  style.fill: "#e8f5e9"
}

anno -> tools: "compile"
anno -> rt: "if retained"
```

**Fig. 1.** The annotation is data. Behavior comes from tools that read it.

> [!warning] `@interface` is not a freely extensible interface
> It always extends `Annotation` and cannot declare `extends`, type parameters, or arbitrary methods. Putting `@Audited` on a class does not change `Ledger`’s bytecode algorithm; a missing `@Retention(RUNTIME)` makes runtime frameworks see **nothing**. Annotations were **not** “always in the language” — they arrived in **Java 5**.

> [!tip] Interview answer
> An annotation is metadata on a program element, declared with @interface, a special interface that extends Annotation. It has no effect by itself; the compiler, an annotation processor, or reflection has to interpret it. They shipped in Java 5; Java 8 added repeating annotations and type-use targets.
