<!--
reps: 0
priority: 0
-->
#Java/JVM/ClassLoaders #SRS

# What is the Java classpath?

> [!abstract] Short answer
> The classpath is the search list the application class loader uses to find class files and resources: directories, JAR files, and ZIP archives. You set it with `-cp` / `--class-path`; on Windows entries are separated by `;`, elsewhere by `:`. With no `-cp` and no `CLASSPATH` variable, the user class path is just the current directory.

## What the launcher says

The `-cp`, `-classpath`, and `--class-path` options all mean the same thing: a list of places to search for class files. An entry is a directory (classes are looked up as `package/path/ClassName.class` under it), a JAR, or a ZIP. A classpath element ending in `*` expands to every `.jar`/`.JAR` file in that directory — not recursive, and expansion order is unspecified. Setting `-cp` overrides the `CLASSPATH` environment variable, which is why relying on the env var is fragile.

```d2
direction: right
lookup: "application loader\nneeds demo.util.Util" {
  width: 280
  height: 90
  style.fill: "#e3f2fd"
}
dir: "entry: classes/\n→ demo/util/Util.class" {
  width: 280
  height: 90
  style.fill: "#fff3e0"
}
jar: "entry: lib/libu.jar\n→ demo/util/Util.class" {
  width: 280
  height: 90
  style.fill: "#fff3e0"
}
wild: "entry: lib/*\n→ every .jar in lib/" {
  width: 260
  height: 90
  style.fill: "#fff3e0"
}
miss: "not on classpath →\nClassNotFoundException" {
  width: 320
  height: 80
  style.fill: "#ffebee"
}
lookup -> dir
lookup -> jar
lookup -> wild
lookup -> miss: none match
```

**Fig. 1.** The classpath is consulted entry by entry; the first definition of the class wins, and a miss surfaces later as `ClassNotFoundException`.

```java
// All verified on JDK 21 (Linux: entries joined by ':'):
//   java -cp classes:. Main                  → classes dir + current dir
//   java -cp lib/libu.jar:classes Main       → JAR entry + dir entry
//   java -cp 'lib/*:classes' Main            → wildcard expands to lib's .jar files
// On Windows the same commands use ';' as the separator.
```

**Listing 1.** Directory, JAR, and wildcard entries — the three forms worth knowing from memory.

## How it interacts with class loading

The classpath is what the *application* class loader searches; JDK platform classes are not found through it (they belong to the platform loader, and `-Xbootclasspath` style injection is gone). The launcher logs make the split visible: `-Xlog:class+load` shows platform classes from the shared archive and your classes with `source: file:.../classes/`. This is also why `-cp` and the module path are different switches — a modular application is searched by module, not by scanning classpath entries.

> [!warning] Two versions of one class on the classpath is silent breakage
> The class loader takes the **first** matching entry in classpath order and never warns about the second copy. A stale copy of a library earlier on the classpath can shadow a fixed one, and the failure surfaces far from the cause: `NoSuchMethodError` or `LinkageError` at run time, only when the missing member is first used. Keeping one version — fat-JAR dedup, dependency shading checks, `-verbose:class` when debugging — is the defense. Related: [[What is the difference between ClassNotFoundException and NoClassDefFoundError]].

For the loader that walks the classpath, see [[How would you explain the Java class loader]] and [[How would you explain Classloader parent delegation model]]; for launching shapes, see [[Which JVM flags are commonly set when launching a Java process]].

> [!tip] Interview answer
> The classpath is the search list for application classes and resources — directories, JARs, and ZIPs, set with -cp and separated by semicolon on Windows or colon elsewhere; without it the classpath is just the current directory. The application class loader scans entries in order and the first match wins, which is why a duplicated old library can silently shadow the new one and blow up as NoSuchMethodError later.
