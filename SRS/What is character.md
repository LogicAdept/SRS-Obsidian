<!--
reps: 0
priority: 0
-->
#Java/IO/File #Java/NIO #OperatingSystems/IO/Files #SRS

# What is a symbolic link?

> [!abstract] Short answer
> A **symbolic link** is a directory entry whose stored value is a **path** (absolute or relative), not the target’s bytes. `Files.createSymbolicLink` creates one (optional). The target **need not exist**; `Files.readSymbolicLink` returns that path without requiring the target. Most `java.nio.file.Files` reads **follow** the link to the final target unless `LinkOption.NOFOLLOW_LINKS` is passed. `Files.delete` removes the **link**, not the target. `java.io.File.getCanonicalPath()` typically **resolves** UNIX symlinks as part of making a unique absolute path ([[What is a symbolic link]], [[What is and]]).

## Path stored in an entry, then usually followed

`Files.createSymbolicLink(link, target, attrs…)`: `target` may be relative; later operations on the link then interpret that relative path **against the link’s location**. Unsupported store → `IOException` or `UnsupportedOperationException`. Some OSes need extra JVM privileges.

`Files.isSymbolicLink(path)` is **true** only if that path **is** a symlink. **False** if missing, not a link, or the type cannot be determined — it does **not** throw `IOException`. Use `readAttributes` + `BasicFileAttributes.isSymbolicLink()` when you must see I/O failures.

`Files.createLink(link, existing)` is a **hard link**: another directory entry for an **existing** file. Typically all such entries must live on the **same** file system. Directory hard links and privilege checks are **platform-specific**, not a Java-wide ban ([[What is a special file in Unix]], [[How would you explain in how is difference between IO and NIO]]).

| | Symbolic link | Hard link (`createLink`) |
| --- | --- | --- |
| Stores | A path (may dangle) | Another name for an existing file |
| Cross file store | Usual (path can point anywhere) | Typically **same** file system |
| Delete | Removes the link | Removes one name; file lasts while names remain |
| Java default I/O | Follow, unless `NOFOLLOW_LINKS` | N/A (no extra hop) |

Dump “several names and different attributes” mixes the two: extra **names** are hard links; a symlink is its **own** entry. Attributes you see depend on follow vs `NOFOLLOW_LINKS`. Dump “hard links cannot name directories” is **too strong** — Java only says some platforms need privileges to link directories.

```java
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.LinkOption;
import java.nio.file.Path;

class SymlinkDemo {
    static Path makeLink(Path link, Path target) throws IOException {
        return Files.createSymbolicLink(link, target);
    }

    static boolean dangling(Path link) throws IOException {
        Path stored = Files.readSymbolicLink(link); // target need not exist
        boolean isLink = Files.isSymbolicLink(link);
        boolean targetIsDir = Files.isDirectory(link); // follows by default
        boolean linkIsDir = Files.isDirectory(link, LinkOption.NOFOLLOW_LINKS);
        return isLink && !Files.exists(link); // exists() follows; dangling → false
    }
}
```

**Listing 1.** Create and read the stored path. `isDirectory(link)` follows; `NOFOLLOW_LINKS` inspects the link node. `exists` follows too — a dangling link is not “existing” in that call.

```d2
direction: down
link: "symlink path\nFiles.readSymbolicLink" {
  width: 260
  height: 50
  style.fill: "#fff8e1"
}
target: "target path\nmay be missing" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
follow: "default Files / File I/O\nfollow to final target" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
link -> target
target -> follow
```

**Fig. 1.** The link holds a path. Opening and most attribute calls walk to the target unless you pass `NOFOLLOW_LINKS` ([[How would you explain the java.io.File class and path representation]], [[Does a java.io.File instance represent only a path without opening the file]]).

> [!warning] `isSymbolicLink` swallows I/O, and `File` has no symlink type
> `false` is not proof the path is a regular file. `java.io.File` has no `isSymbolicLink`; `exists()` / `length()` follow. Canonicalization can change when the target is created or deleted. Creating links may need OS privileges even when the API exists.

> [!tip] Interview answer
> A symbolic link is a small directory entry that stores another path, which may not exist. Java NIO creates and reads it with `Files.createSymbolicLink` and `readSymbolicLink`; most other calls follow the target unless you pass `NOFOLLOW_LINKS`. A hard link is a second name for an existing file, usually on the same file system — not the same thing.
