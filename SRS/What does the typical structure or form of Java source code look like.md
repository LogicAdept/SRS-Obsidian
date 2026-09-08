<!--
reps: 0
priority: 0
-->
#Java/Language #SRS

# What does the typical structure or form of Java source code look like?

> [!abstract] Short answer
> A typical `.java` file is an **ordinary compilation unit**: optional `package`, then `import`s, then **top-level** class or interface declarations. Every unit implicitly imports `java.lang.*`. File-system compilers (javac) keep a **`public`** top-level type in a file named **`Type.java`**, at most **one** such public type per file. Java SE 25 also has a **compact** unit (`void main() { … }` with no class wrapper) and a **modular** unit (`module-info.java`). What is inside a class: [[What does a Java class consist of]].

## Three compilation-unit shapes

**Ordinary** (the interview default): `[package] {import} {top-level type}`. No `package` means the **unnamed** package. Top-level types may be `public` or package-private; they cannot be `private`, `protected`, or `static`. Extra `import java.lang.String;` is legal and redundant. Kinds of class: [[Which types classes exist in Java]]. Nested types live **inside** a type, not as extra top-level names ([[How would you explain categories of Java classes such as nested and anonymous]]).

**Compact** (SE 25): `import`s, then class members that include **at least one method**. The compiler implicitly declares a top-level class whose members are those declarations. There is **no** `package` line. Compact units also implicitly `import module java.base`, so `List` and `Path` resolve without writing `java.util`.

**Modular:** `import`s then a `module` declaration — the `module-info.java` of a named module.

Package annotations and package Javadoc belong in **`package-info.java`**, not on a random class ([[How do you annotate a Java package]]). `import static` is an import, not a modifier on the class ([[What does the static keyword mean in Java]]).

When packages live on a **file system**, the host **may** require that a `public` type, or a type referenced from other units of the package, sit in `Name.java`. javac does. That implies **at most one** public top-level type per file. Package-private helpers in the same file are allowed. Putting every class in its own file is a habit, not a language requirement for non-public types.

```d2
direction: down
pkg: "package com.example.app;" {
  width: 280
  height: 40
  style.fill: "#fff8e1"
}
imp: "import …\n(implicit java.lang.*)" {
  width: 280
  height: 50
  style.fill: "#fff3e0"
}
types: "public class App { … }\nclass Helper { … }" {
  width: 280
  height: 55
  style.fill: "#e8f5e9"
}
pkg -> imp
imp -> types
```

**Fig. 1.** Ordinary unit order: package, imports, top-level types. Compact units skip `package` and the class header.

```java
package com.example.app;

import java.util.List;

public class App {
    public static void main(String[] args) {
        List<String> ignored = List.of();
        new Helper();
    }
}

class Helper {}
```

**Listing 1.** Ordinary unit in `App.java`. `Helper` is package-private in the same file. `List` needs an import; `String` does not.

```java
void main() {
    System.out.println("Hello, World!");
}
```

**Listing 2.** Compact compilation unit. Launch with `java HelloWorld.java` (source-file mode) or compile the implicitly declared class.

> [!warning] `public class Foo` must match `Foo.java` under javac
> Two `public` top-level types in one file are a compile-time error on a file-system host. A `public` type in a wrongly named file is also an error. Package-private extras in that file are fine. Compact source cannot add a `package` declaration; that would make it an ordinary unit.

> [!warning] Order is grammar, not Code Conventions
> `package` before `import` before types is the language. Beginning copyright banners, “public class first,” and 2000-line file limits are **style**, not javac ([[Which recommendations to style code on Java]]). `module-info.java` is a different unit kind, not an ordinary class file.

> [!tip] Interview answer
> **A normal Java file is package, then imports, then one public class whose name matches the file, plus optional package-private helpers.** `java.lang` is imported automatically. Java 25 compact source can be just a `main` method with no class wrapper; `module-info.java` declares a module, not a class.
