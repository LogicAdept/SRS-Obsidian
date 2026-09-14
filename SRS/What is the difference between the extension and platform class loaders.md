<!--
reps: 0
priority: 0
-->
#Java/JVM/ClassLoaders #SRS

# What is the difference between the extension and platform class loaders

> [!abstract] Short answer
> **The extension loader is the pre-Java 9 middle loader that loaded JARs from the extension directories; the platform loader is its Java 9 successor that loads the platform classes from named modules instead.** Both occupy the same slot — child of the bootstrap loader, parent of the system loader — but nothing else carries over: the extension mechanism, the java.ext.dirs property and the lib/ext directory were removed by JEP 220, the loader is no longer a URLClassLoader, and it is reached today via getPlatformClassLoader ([[What is the platform class loader in Java and what does it load]]).

## The extension loader (through Java 8)

The extension mechanism allowed JAR files containing APIs that extend the Java SE Platform to be installed into a run-time image so that their contents were visible to every application compiled with or running on that image. The mechanism was defined in terms of a path-like system property, java.ext.dirs, with a default value composed of the JDK lib/ext directory plus a platform-specific system-wide directory. JAR files placed in an extension directory were loaded by the run-time environment's extension class loader, which is a child of the bootstrap class loader and the parent of the system class loader, the loader that actually loads the application from the class path ([[How would you explain the Java class loader]]).

The practical consequence was deployment by file drop: any JAR parked in lib/ext appeared on the classpath of every application using that JDK, with no per-application control and no way to see which JAR contributed which type. It was the module system's job to make this kind of shared, invisible dependency manageable, and Java 9 removed the mechanism entirely.

## The platform loader (Java 9 and later)

JEP 220 removed rt.jar, the extension mechanism and the endorsed-standards mechanism; the compiler and the launcher now fail if java.ext.dirs is set. The loader itself survived in a new role: it is no longer an instance of URLClassLoader but of an internal class, and it no longer loads classes via the extension mechanism. Instead it defines selected Java SE and JDK modules. In its new role this loader is known as the platform class loader, it is available via the ClassLoader.getPlatformClassLoader method, and its built-in name is platform ([[What is the Java Platform Module System]]).

```d2
direction: right
boot: "bootstrap" {
  width: 160
  height: 45
}
ext: "extension loader\nJDK 1.2 - 8\nlib/ext, java.ext.dirs" {
  width: 260
  height: 70
  style.fill: "#ffebee"
}
sys8: "system loader" {
  width: 170
  height: 45
}
plat: "platform loader\nJava 9+\nSE + JDK modules" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}
sys9: "application loader\nname app" {
  width: 210
  height: 55
}
boot -> ext: "child"
ext -> sys8: "parent"
boot -> plat: "child"
plat -> sys9: "parent"
```

**Fig. 1.** Same position in the hierarchy, different world behind it: a JAR-dropping extension mechanism became a module-defining platform loader with a public accessor.

## What actually changed

The lookup source moved from directories of JARs named by java.ext.dirs to named modules defined to the loader. The loader type moved from URLClassLoader to an internal implementation, so code that down-cast the system or platform loader to URLClassLoader and poked at its URLs broke on 9 — the supported API is getPlatformClassLoader, plus the resource and class lookup methods every ClassLoader carries. The visibility guarantee stayed close: platform classes remain visible to everything below, and the platform loader can still delegate sideways to the application loader for upgraded modules ([[What is the application class loader in Java and what does it load]]).

```java
class LoaderToday {
    public static void main(String[] args) {
        ClassLoader platform = ClassLoader.getPlatformClassLoader();
        System.out.println(platform.getName());   // platform
        // There is no getExtensionClassLoader anywhere in the API:
        // the pre-9 loader had no public accessor, and its JAR-drop
        // lookup (java.ext.dirs, lib/ext) no longer exists at all.
        // Extensions today: put JARs on the class path, or build a
        // module layer with the modules your application needs.
    }
}
```

**Listing 1.** The modern middle loader is named and reachable; the extension lookup it replaced has no API trace left beyond migration notes.

> [!warning] Migration breakage lives in three places
> Environments that set java.ext.dirs now fail at launcher or compile time rather than silently extending the classpath. Code that assumed the middle loader was a URLClassLoader lost its down-cast target. And JARs previously parked in lib/ext simply stopped being visible — the fix is the class path, the module path, or an explicit custom loader ([[How do you write a custom class loader in Java]]).

> [!tip] Interview answer
> **Same slot in the hierarchy, different mechanism: the extension loader (through Java 8) loaded JARs from java.ext.dirs and lib/ext, child of bootstrap, parent of system; the platform loader (Java 9+) defines selected SE and JDK modules instead.** JEP 220 removed the extension mechanism, the loader is no longer a URLClassLoader, and the public accessor is getPlatformClassLoader with the built-in name platform. Visibility moved from dropped JARs to named modules; the security bonus is de-privileged modules off the all-permissions bootstrap boundary.
