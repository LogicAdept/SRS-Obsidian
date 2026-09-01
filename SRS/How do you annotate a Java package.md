<!--
reps: 0
priority: 0
-->
#Java/Annotations #SRS

# How do you annotate a Java package?

> [!abstract] Short answer
> Put the annotations on the **`package` declaration** in **`package-info.java`** in that package’s source directory — not on a class in the package. At most **one** annotated `package` declaration is allowed per package. The annotation interface must be applicable to **package declarations** (`@Target` includes `ElementType.PACKAGE`, or `@Target` is omitted). Runtime readers load `package-info.class` through `java.lang.Package`.

## `package-info.java` is the home

A package annotation is a modifier on `package name;`. File-system compilers are strongly advised to keep that **sole** annotated declaration in `package-info.java`. That file must **not** declare a type named `package-info` (`package-info` is not a legal identifier). Keep other types out of it.

The same file is the recommended place for the **package documentation comment** (replacing `package.html`). Javadoc looks immediately before the (possibly annotated) `package` line.

```java
/**
 * Types for the audit API.
 */
@Audited
package com.example.audit;
```

**Listing 1.** Typical `package-info.java` — Javadoc comment, then package annotations, then `package`.

```java
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.PACKAGE)
public @interface Audited {}
```

**Listing 2.** Applicable only to package declarations. If `@Target` is **absent**, the type is applicable in **all declaration contexts**, including packages. `@Target(ElementType.TYPE)` does **not** include packages — that is a compile-time error on `package`. Placement rules: [[How does the Target meta-annotation restrict annotation placement]] and [[Which program elements can be annotated in Java]].

Annotating a **class** in `com.example.audit` does not annotate the package. Two compilation units that both write an annotated `package com.example.audit;` are illegal.

## Reading it at runtime

`Package` implements `AnnotatedElement`. The VM reads package annotations from **`package-info.class`** next to the package’s classes. That still requires **RUNTIME** retention, same as any other reflective lookup: [[How do Java annotation retention policies work]], [[How do you retrieve annotations at runtime]].

```java
Package pkg = com.example.audit.Api.class.getPackage();
Audited a = pkg.getAnnotation(Audited.class);
```

**Listing 3.** Use a class in the package (or `ClassLoader.getDefinedPackage("com.example.audit")`). `Package.getPackage(String)` is deprecated: with delegating loaders it can return a **parent** `Package` and hide this loader’s `package-info.class`.

```d2
direction: right
info: "package-info.java\n@Audited package p;" {
  width: 240
  height: 80
  style.fill: "#e3f2fd"
}
cls: "package-info.class" {
  width: 200
  height: 70
  style.fill: "#fff3e0"
}
pkg: "Package.getAnnotation" {
  width: 220
  height: 70
  style.fill: "#e8f5e9"
}

info -> cls: "javac"
cls -> pkg: "RUNTIME"
```

**Fig. 1.** Package metadata is compiled to `package-info.class`, not copied onto every type in the package.

> [!warning] SOURCE-only package annotations leave an empty `package-info.class`
> If every annotation on the package is `SOURCE`, javac may still emit `package-info.class` with **no** runtime-visible annotations — `getAnnotation` is then `null`. `@Deprecated` on a package also does **not** make the compiler warn on uses of that package name. Unnamed packages have **no** `package` declaration, so they have nowhere to write a package annotation.

> [!tip] Interview answer
> You annotate a package in package-info.java, on the package declaration itself, with a type whose @Target includes PACKAGE (or has no @Target). That file is also where package Javadoc goes; putting @Foo on a class does not mark the package. At runtime the VM reads package-info.class through Package, so you still need RUNTIME retention and should not rely on the deprecated Package.getPackage lookup.
