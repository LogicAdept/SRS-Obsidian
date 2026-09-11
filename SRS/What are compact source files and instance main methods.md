<!--
reps: 0
priority: 0
-->
#Java/Versions/25 #SRS

# What are compact source files and instance main methods

> [!abstract] Short answer
> **JEP 512 (final in Java 25; previewed as unnamed classes in 21 via 445, then 463/477/495) lets a file with just a `void main()` method — and no class declaration — run directly: the compiler wraps it in an implicitly declared class, and `main` may be an instance method. Compact source files also implicitly `import module java.base`, so `List`, `Map`, `File` resolve without imports.**

## Hello World without ceremony

The 445 preview set the shape: a file whose members are fields and methods of an unnamed class, launched through an instance `main`. By 25 the naming and scope settled: compact source files (no class declaration), implicitly declared classes (you cannot reference the class by name from other code), and instance main (the JVM instantiates the class and invokes `main` on it). The implicit `import module java.base` means `List.of`, `Map.entry`, `Instant` all resolve in a fresh file ([[What are module import declarations]] covers the mechanism). Static `main` still works; explicit class declarations are unchanged — this is a new floor, not a replacement.

```java
// JEP 512 (final in 25); previewed as JEP 445 "Unnamed Classes and Instance Main Methods" (21),
// then 463 (22), 477 (23), 495 (24). No class declaration, no modifiers, instance main.
String greeting = "compact source";

void greet() {
    System.out.println("greet: " + greeting);
}

void main() {
    greet();
    System.out.println("instance main ran");
}
```

**Listing 1.** Verified on JDK 21 with `--enable-preview --source 21` (V47_CompactSource in empirics): `greet: compact source`, `instance main ran` (out/V47_CompactSource.txt) — a file with no class declaration, launched through instance main.

```d2
direction: right
file: "file: fields, methods,\nvoid main() - no class decl" { style.fill: "#e8f5e9"; width: 280; height: 90 }
wrap: "compiler wraps into\nimplicitly declared class" { style.fill: "#e3f2fd"; width: 300; height: 80 }
launch: "JVM instantiates it,\ninvokes instance main" { style.fill: "#fff3e0"; width: 280; height: 80 }
file -> wrap -> launch: ""
```

**Fig. 1.** Launch path of a compact source file: declaration-free source, implicit class wrapper, instance-method entry point.

> [!warning] The implicit class is unreachable by name
> Other files cannot import or reference the implicitly declared class, and relying on the implicit java.base import in large explicit classes is style drift — production code keeps explicit imports so review sees the dependency surface. Also "Java finally has functions at top level" is wrong: these are members of a class the compiler wrote ([[What was new in Java 25]]).

> [!tip] Interview answer
> **JEP 512, final in 25, is the beginner-syntax finale: a file can be just fields, methods, and void main — the compiler wraps it in an implicitly declared class and the JVM launches through an instance main, with java.base implicitly imported. It previewed for four trains starting as unnamed classes in 21. It lowers the hello-world ceremony without changing how explicit classes work.**
