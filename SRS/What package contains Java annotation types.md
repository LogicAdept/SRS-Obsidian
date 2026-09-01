<!--
reps: 0
priority: 0
-->
#Java/Annotations #SRS

# What package contains Java annotation types?

> [!abstract] Short answer
> **Two** packages. The **annotation facility** — `Annotation`, meta-annotations (`@Retention`, `@Target`, `@Inherited`, `@Documented`, `@Repeatable`), plus `RetentionPolicy` and `ElementType` — lives in **`java.lang.annotation`**. The everyday **declaration** annotations **`@Override`**, **`@Deprecated`**, **`@SuppressWarnings`**, **`@SafeVarargs`**, **`@FunctionalInterface`** live in **`java.lang`** and need **no** extra import. Not `java.text`.

## Split by role

`java.lang.annotation` is the home of the **mechanism**: the `Annotation` interface (every `@interface` implicitly extends it), the meta-annotations you put on custom types, and the two enums those meta-annotations use. You `import java.lang.annotation.*` (or individual types) when you **declare** an annotation. See [[What are meta-annotations in Java]] and [[How does the Target meta-annotation restrict annotation placement]].

`java.lang` holds the **predefined** annotations the compiler special-cases on ordinary code. They are already in scope, like `String`. That is why `@Override` compiles with zero imports.

`java.lang.annotation.Annotation` is an **interface**, not a class whose “parent is `Object`.” It is also **not** itself an annotation type: you do not write `@Annotation`.

```java
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;
import java.lang.annotation.ElementType;

@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.TYPE)
public @interface ApiMarker { }   // facility types from java.lang.annotation

@Override                         // java.lang — no import
public String toString() { return "ok"; }
```

**Listing 1.** Meta-annotations need `java.lang.annotation`; `@Override` does not.

```d2
direction: right
fac: "java.lang.annotation\nAnnotation, Target, Retention,\nInherited, Documented, Repeatable,\nElementType, RetentionPolicy" {
  width: 280
  height: 110
  style.fill: "#e3f2fd"
}
lang: "java.lang\n@Override @Deprecated\n@SuppressWarnings @SafeVarargs\n@FunctionalInterface" {
  width: 260
  height: 110
  style.fill: "#e8f5e9"
}
```

**Fig. 1.** Mechanism package vs compiler-known `java.lang` annotations. Related: [[What is a Java annotation]].

> [!warning] Not `java.text`, and `Annotation` is not a class
> `java.text` is **formatting** (`DateFormat`, `MessageFormat`). Naming it in this cue is a wrong-bank answer. Do not call `Annotation` a class under `Object`; it is the **interface** every annotation type implements. Answering only `java.lang.annotation` also misses `@Override` in `java.lang`.

> [!tip] Interview answer
> Meta-annotations and Annotation live in java.lang.annotation; you import that package when you write an @interface. Override, Deprecated, SuppressWarnings, SafeVarargs, and FunctionalInterface are in java.lang, so they need no import. java.text is unrelated, and Annotation is an interface, not a class.
