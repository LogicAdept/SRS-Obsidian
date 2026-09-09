<!--
reps: 0
priority: 0
-->
#Java/JDK #Java/Tooling #SRS

# How would you explain the JAR manifest file and common entries

> [!abstract] Short answer
> **`MANIFEST.MF` is the JAR's metadata file, always at `META-INF/MANIFEST.MF`: `Main-Class` makes a jar executable with `java -jar`, `Class-Path` points at other jars it depends on, plus entries like `Manifest-Version`, `Created-By`, implementation/version info, and package sealing.** The `jar` tool generates a default one; you add entries via a text file passed to `jar cfm` (or `-e` to set the main class directly).

## The file and the entries that matter

Format rules are strict: each line is `header: value`, sections separated by blank lines, first section is the "main attributes" section applying to the whole archive. A minimal generated manifest holds two lines; the entries that make behavior change:

| Entry | What it does |
|---|---|
| `Main-Class: pkg.HelloJar` | entry point — enables `java -jar hello.jar` |
| `Class-Path: lib/other.jar lib/more.jar` | extra classpath entries, relative to the jar (does NOT include the jar itself) |
| `Manifest-Version: 1.0` | manifest format version (generated) |
| `Created-By: 21.0.12.1 (Eclipse Adoptium)` | which JDK built it (generated) |
| `Implementation-Version: 1.0.0` | package version metadata readable via `Package` API |
| `Sealed: true` | no class from another jar may join the package |

```d2
direction: right
jar: "hello.jar\nHelloJar.class" {
  width: 240
  height: 90
  style.fill: "#e3f2fd"
}
mf: "META-INF/MANIFEST.MF\nMain-Class: HelloJar" {
  width: 300
  height: 90
  style.fill: "#fff3e0"
}
run: "java -jar hello.jar\nJVM reads Main-Class -> runs main" {
  width: 330
  height: 90
  style.fill: "#e8f5e9"
}
jar -> mf -> run
```

**Fig. 1.** The manifest is the bridge between a plain zip of classes and a runnable artifact.

A real end-to-end run (JDK 21): `jar cfe hello.jar HelloJar HelloJar.class` — the `-e` flag writes the entry point — then the jar's own manifest and the run:

```java
// META-INF/MANIFEST.MF inside hello.jar (printed with unzip -p):
Manifest-Version: 1.0
Created-By: 21.0.12.1 (Eclipse Adoptium)
Main-Class: HelloJar

// java -jar hello.jar
main from manifest: HelloJar running
```

**Listing 1.** Verified on JDK 21: `jar cfe` placed `Main-Class: HelloJar` into the generated manifest, and `java -jar` used exactly that entry to find and run `main`.

> [!warning] Main-Class uses dots, Class-Path does not include the jar — and fat jars bypass Class-Path entirely
> The recurring failures. First, format sensitivity: the value is a fully-qualified class name with dots (`com.demo.HelloJar`) — a path with slashes, a missing colon, or a missing final newline in the manifest text file silently breaks `java -jar` with "no main manifest attribute" or class-not-found; the manifest must end with a newline. Second, `Class-Path` entries are relative URLs to *other* jars — `java -jar` ignores `-cp` and the environment CLASSPATH, so a "thin" runnable jar runs only if its neighbors sit exactly where the manifest says; that fragility is why assembly plugins (Shade, Spring Boot repackaging) build fat jars with everything inside — making `Class-Path` unnecessary. Third, version entries are read by tooling: `Package.getImplementationVersion()` returns them, Spring Boot's actuator info surfaces them — an empty value usually means the build never wrote them, not that the API is broken. Related mechanics: how the JVM actually loads those classes — [[How would you explain the Java class loader]] — and the packaging step that produced the jar — [[How would you explain mvn clean install]].

> [!tip] Interview answer
> **MANIFEST.MF sits in META-INF and is the jar's metadata. Key entries: Main-Class makes the jar executable via java -jar, Class-Path adds dependent jars relative to it, plus Manifest-Version, Created-By, implementation version entries and sealing. jar cfm or -e writes it. Gotchas: class name with dots and a trailing newline, java -jar ignores the external classpath, and fat jars exist precisely to avoid Class-Path fragility.**

