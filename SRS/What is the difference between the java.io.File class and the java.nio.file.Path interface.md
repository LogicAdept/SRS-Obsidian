<!--
reps: 0
priority: 0
-->
#Java/NIO/Files #Java/IO/File #SRS

# What is the difference between the java.io.File class and the java.nio.file.Path interface?

> [!abstract] Short answer
> **`java.io.File` (Java 1.0) is a concrete class for an abstract pathname with filesystem queries bolted on; `java.nio.file.Path` (Java 7) is an interface — a pure path model inside a `FileSystem`, with all the operations moved to the `Files` utility class.** `Path` has the algebra `File` never had: `resolve`, `relativize`, `normalize`, `subpath`, iteration over name elements. Bridges are explicit: `file.toPath()` and `path.toFile()`. New code pairs `Path` + `Files`; `File` survives in legacy APIs ([[How would you explain the java.io.File class and path representation]], [[How do you read and write files with the Files utility class in Java]]).

## Model differences

`File` mixes two jobs: representing the pathname and asking the filesystem (exists, length, isDirectory). NIO.2 split them: `Path` is only the name; `Files` does the I/O and reports failures as **`IOException`** with a cause, while `File` methods return `boolean` and swallow the reason. `Path` comes from `Path.of(...)` (Java 11+) or `Paths.get(...)`; `File` from its constructors.

| | `java.io.File` | `java.nio.file.Path` |
| --- | --- | --- |
| Kind | final class (1.0) | interface (1.7) |
| Job | pathname + queries | pathname only |
| Join | `new File(parent, child)` | `p.resolve(child)` — child may be absolute and then wins |
| Difference | manual string surgery | `p.relativize(other)`, `p.normalize()` |
| Failure reporting | `boolean` returns | `IOException` with cause |
| Belongs to | the default filesystem only | any installed `FileSystem` (zip FS, in-memory FS) |

`equals`/`compareTo` on both follow the platform case rules; neither consults the filesystem for identity. Conversion is lossless in both directions for the default filesystem: `File.toPath()`, `Path.toFile()`.

```java
import java.io.File;
import java.nio.file.Path;

class Bridge {
    public static void main(String[] args) {
        File f = new File("/tmp/work/report.csv");
        Path p = f.toPath();                          // legacy -> modern
        System.out.println("parent: " + p.getParent());
        System.out.println("resolve: " + p.getParent().resolve("archive").resolve("2026.csv"));
        System.out.println("relativize: " + Path.of("/tmp/work").relativize(p));
        System.out.println("normalize: " + Path.of("/tmp/work/./x/../y").normalize());
        System.out.println("back: " + p.toFile());
    }
}
```

**Listing 1.** The path algebra that `File` lacks, plus the two-way bridge:

```text
parent: /tmp/work
resolve: /tmp/work/archive/2026.csv
relativize: report.csv
normalize: /tmp/work/y
back: /tmp/work/report.csv
```

**Listing 2.** Algebra on names; nothing touched the filesystem yet.

```d2
direction: right
file: "java.io.File\nlegacy APIs, boolean returns" {
  width: 270
  height: 55
  style.fill: "#fff8e1"
}
bridge: "toPath() / toFile()" {
  width: 200
  height: 45
  style.fill: "#e8f5e9"
}
path: "java.nio.file.Path\nresolve / relativize / normalize" {
  width: 300
  height: 55
  style.fill: "#e3f2fd"
}
files: "java.nio.file.Files\nIO with IOException detail" {
  width: 280
  height: 55
  style.fill: "#e8f5e9"
}
file <-> bridge <-> path
path -> files
```

**Fig. 1.** `Path` models, `Files` acts, `File` waits for the legacy callers ([[Which class is intended for working with filesystem entries]]).

> [!warning] Not a rename — the semantics moved too
> `resolve` with an absolute argument replaces the path instead of appending — forgetting that yields surprising paths. `normalize()` never touches the disk, so symlinked `..` components survive; `toRealPath()` is the one that resolves links. A `Path` from a non-default `FileSystem` (zip, in-memory) cannot be handed to `java.io` classes at all. And `Paths.get("C:readme.txt")`-style Windows drive-relative oddities behave exactly like the `File` rules — moving to `Path` did not make them portable.

> [!tip] Interview answer
> `File` is the 1.0 concrete class bundling a pathname with boolean-returning filesystem queries; `Path` is the Java 7 interface holding only the name, with resolve/relativize/normalize algebra, and `Files` doing the I/O with real exceptions. They interconvert via `toPath()`/`toFile()`; new code uses `Path` + `Files`, and `File` remains for legacy APIs.

