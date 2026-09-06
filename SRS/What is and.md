<!--
reps: 0
priority: 0
-->
#Java/IO/File #OperatingSystems/IO/Files #SRS

# What are an absolute path and a relative path?

> [!abstract] Short answer
> **Absolute:** complete — no other pathname is needed to locate the file. **Relative:** interpreted against another pathname (in `java.io`, the current user directory `user.dir`, typically where the JVM was started). On UNIX, absolute means prefix `"/"`. On Windows, absolute means a drive letter plus `"\"`, or a UNC prefix `"\\"`. `File.isAbsolute()` tests that; `getAbsolutePath()` fills in `user.dir` (or the named drive’s current directory on Windows). Canonical form is a further step: absolute **and unique** (`"."` / `".."` / symlinks) ([[What is the difference between an absolute path and a relative path]], [[How would you explain the java.io.File class and path representation]]).

## Completeness, not “starts with a slash”

A `File` is an immutable **abstract pathname** (prefix + names). It does not open the file. Absolute vs relative is a property of that pathname, system-dependent ([[Does a java.io.File instance represent only a path without opening the file]], [[What character separates path components in the Java File API]]).

| | Absolute | Relative |
| --- | --- | --- |
| Meaning | Complete; locates the file alone | Needs another pathname |
| UNIX prefix | always `"/"` | none |
| Windows prefix | `"C:\"`-style or `"\\"` UNC | none, or `"C:"` without `"\"` |
| `java.io` resolve | `getAbsolutePath()` returns `getPath()` unchanged | against `user.dir` (UNIX); against that drive’s cwd if a drive is named (Windows) |

The empty abstract pathname is relative; `getAbsolutePath()` then returns `user.dir`.

Dump “always begins at the root” is the UNIX picture. Windows `C:readme.txt` is **not** absolute (`isAbsolute()` is false): it is relative to **that drive’s** current directory, which may not be `user.dir`.

**Canonical vs absolute.** `getCanonicalPath()` first makes the path absolute, then uniquifies: drop `"."` / `".."`, resolve UNIX symlinks, normalize Windows drive case. Two absolute strings can name the same file; the canonical string is the unique form. It throws `IOException`. Existence can change the canonical string of a path.

```java
import java.io.File;
import java.io.IOException;

class AbsRel {
    static void show(String s) throws IOException {
        File f = new File(s);
        boolean abs = f.isAbsolute();
        String absolute = f.getAbsolutePath();
        String canonical = f.getCanonicalPath();
        // abs: prefix complete?
        // absolute: may prepend user.dir
        // canonical: unique; I/O
    }
}
```

**Listing 1.** `isAbsolute()` does not consult the disk. `getAbsolutePath()` uses `user.dir` (or a Windows drive cwd). `getCanonicalPath()` hits the filesystem.

```d2
direction: down
rel: "relative File(\"logs/app.log\")" {
  width: 260
  height: 45
  style.fill: "#fff8e1"
}
abs: "getAbsolutePath()\nuser.dir + names" {
  width: 260
  height: 50
  style.fill: "#e3f2fd"
}
can: "getCanonicalPath()\nabsolute + unique" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}
rel -> abs -> can
```

**Fig. 1.** Relative → absolute (`user.dir`) → canonical (unique). Absolute is not automatically canonical ([[How do you list directory entries that match a criterion in Java]]).

> [!warning] Absolute is not “the same file forever,” and `user.dir` is not `File.separator`
> Changing the process working directory (native, or rare JVM tricks) changes how **relative** paths resolve; an already-absolute `File` string does not. `getAbsolutePath()` does not remove `".."`. `C:\` vs `C:` matters on Windows. Do not treat `pathSeparator` (`:` / `;`) as a root marker.

> [!tip] Interview answer
> An absolute path is complete; a relative path is resolved against something else — in Java I/O, `user.dir`. `File.isAbsolute()` is `/` on UNIX and drive-plus-backslash or UNC on Windows. `getAbsolutePath()` fills that in; `getCanonicalPath()` then makes it unique.
