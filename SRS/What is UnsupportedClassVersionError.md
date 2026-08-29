<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Error #SRS

# What is `UnsupportedClassVersionError`?

> [!abstract] Short answer
> **An `Error` when the VM reads a class file whose major/minor version it does not support.** The usual interview case is **compiled on a newer JDK, launched on an older runtime**. It is a `ClassFormatError` (`LinkageError`), not a checked exception on `main`.

## Present class file, rejected version

`UnsupportedClassVersionError` extends `ClassFormatError`, hence `LinkageError` and `Error`. You do not declare it in `throws`. `catch (Exception)` does not catch it ([[What is LinkageError]], [[What is java.lang.Error]], [[Are Error subclasses checked or unchecked]], [[Does catch Exception also catch Error]]).

The VM can find the `.class` bytes. It then refuses them because the **class-file version** in the header is not one this runtime implements. That is not “class missing”: `NoClassDefFoundError` / `ClassNotFoundException` are a missing definition or a failed by-name load ([[What is the difference between ClassNotFoundException and NoClassDefFoundError]]). It is also not a missing method after a partial rebuild ([[What is NoSuchMethodError]]).

The usual mismatch is **compile newer, run older**. An older class file on a newer VM is the supported direction. `javac`/`java` version mix-ups and building on CI with JDK 21 then running on a Java 11 server are the stock stories. The launcher often prints `Exception in thread "main"` because the failure happens while loading the initial class, before `main` runs.

```d2
direction: down
file: ".class is on the classpath" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
ver: "major/minor not supported by this VM" {
  width: 340
  height: 50
  style.fill: "#ffebee"
}
ucve: UnsupportedClassVersionError {
  width: 300
  height: 50
  style.fill: "#ffebee"
}
file -> ver
ver -> ucve
```

**Fig. 1.** The bytes exist; the version is rejected.

```java
class Demo {
    public static void main(String[] args) {
        System.out.println("hello");
    }
}
```

**Listing 1.** `main` needs no `throws`. If this class is compiled with a **newer** JDK than the `java` that launches it, loading `Demo` throws `UnsupportedClassVersionError` **before** `hello` prints. Running the same bytes on a **newer** VM is the supported direction.

> [!warning] Not `NoClassDefFoundError`
> The class file is there. The VM rejected its **version**. Missing JAR / failed `<clinit>` is a different `Error` (or checked `ClassNotFoundException` for `Class.forName`).

> [!warning] “Compiled on one JDK, run on another” is one-way
> Dumps say “different JDKs” without direction. The failure is a class-file version this **runtime** does not support — almost always **newer compiler, older `java`**.

> [!tip] Interview answer
> **`UnsupportedClassVersionError` is an `Error` when the class-file version is newer than the VM that tries to load it.** The file is present; the version is rejected. It is not `NoClassDefFoundError`, and you do not declare it on `main`.
