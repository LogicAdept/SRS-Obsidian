<!--
reps: 0
priority: 0
-->
#Java/Language/Reflection #Java/Versions/9 #SRS

# What does setAccessible do in the Reflection API?

> [!abstract] Short answer
> **It sets the `accessible` flag on a `Field`, `Method`, or `Constructor` (`AccessibleObject`).** `true` means **that reflected object** suppresses Java language access checks when it is used; `false` means it enforces them again (with the documented readability variation). The member is still `private` in the language. Success is not unlimited: a package that is not **open** to the caller throws `InaccessibleObjectException` (Java SE 9), and the flag never grants **write** access to a non-modifiable `final` field.

## The flag is on the reflected object

`AccessibleObject` is the base of `Field`, `Method`, and `Constructor` (since 1.2). By default those objects **enforce** Java language access control when you get/set a field, invoke a method, or call `newInstance`. The documented variation is that the check **assumes readability**: the caller’s module is treated as reading the member’s module. `setAccessible(true)` is how privileged code (the JavaDoc names serialization and other persistence) turns those checks off **for that instance** ([[How do you invoke a private constructor using reflection]], [[How can you invoke a method using reflection]]).

A caller in class `C` may enable access to a member of declaring class `D` when any of these hold:

- `C` and `D` are in the **same** module.
- The member is **public**, `D` is public, and `D`’s module **exports** the package to at least `C`’s module.
- The member is **protected static**, `D` is public in a package exported to `C`, and `C` is a subclass of `D`.
- `D`’s package is **open** to at least `C`’s module. Every package in an **unnamed** or **open** module is open to all modules, so `setAccessible(true)` succeeds when `D` lives there (typical classpath code).

It **cannot** enable access to private, package-private, protected instance members, or protected constructors when `D` is in a **different** module and that package is **not** open to the caller. That failure is `InaccessibleObjectException` (a `RuntimeException` since 9), not `IllegalAccessException`. `IllegalAccessException` is what `get` / `set` / `invoke` / `newInstance` throw while the flag is still `false`.

```d2
direction: down
use: "Field / Method / Constructor" {
  width: 260
  height: 45
}
flag: "setAccessible(true)\nsuppress checks on this object" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
ok: "Same module, or package open / unnamed" {
  width: 300
  height: 55
  style.fill: "#e8f5e9"
}
deny: "InaccessibleObjectException\n(named module, not open)" {
  width: 300
  height: 70
  style.fill: "#ffebee"
}
use -> flag
flag -> ok
flag -> deny
```

**Fig. 1.** The flag does not rewrite the member. Cross-module deep reflection still needs the declaring package **open** to the caller ([[What are the drawbacks of using Java reflection]]).

`trySetAccessible()` (since 9) is `setAccessible(true)` that returns `false` instead of throwing `InaccessibleObjectException`. It is a no-op if the flag is already `true`. `canAccess(obj)` (since 9) is the real accessibility test: `true` if the flag is set **or** the caller could use the member under JLS 6.6. Pass the instance for an instance member; pass `null` for a static member or a constructor. `isAccessible()` only reads the flag and is `@Deprecated(since="9")` because its name sounds like `canAccess`.

A security manager, when present, is asked for `ReflectPermission("suppressAccessChecks")` first (`SecurityException` if denied). The static `setAccessible(array, flag)` does that check once for a batch. `setAccessible(true)` on a constructor of `java.lang.Class` throws `SecurityException`.

```java
class Secret {
    private int n = 1;
}

class Peek {
    static int read(Secret s) throws Exception {
        Field f = Secret.class.getDeclaredField("n");
        f.setAccessible(true);
        return f.getInt(s);
    }

    static Integer tryRead(Secret s) throws Exception {
        Field f = Secret.class.getDeclaredField("n");
        if (!f.trySetAccessible()) {
            return null; // declaring package not open to the caller
        }
        return f.getInt(s);
    }
}
```

**Listing 1.** Same-module / unnamed-module code: `setAccessible(true)` then `get`. Across named modules, prefer `trySetAccessible` so a closed package is a boolean, not a thrown `InaccessibleObjectException`.

The flag also **cannot enable write** to a non-modifiable `final`: static finals, finals on a hidden class, and finals on a record. `true` still allows **read** of those fields. `Field.set` may still throw `IllegalAccessException` afterward ([[Can you change the value of a final field using reflection]], [[How do you access static fields using reflection]]).

On JDK 17+, tools that used `setAccessible(true)` on non-public members of `java.*` packages fail unless the package is opened (module-info `opens`, or the launcher `--add-opens module/package=target`, with `ALL-UNNAMED` for classpath code).

> [!warning] The member is still private
> `setAccessible(true)` does not change modifiers, does not make the name compile from other classes, and applies only to **that** `AccessibleObject`. A second `Field` for the same field starts with checks on.

> [!warning] `setAccessible` is not a write grant for every `final`
> A successful flag still does not give `Field.set` write access to static finals, record component fields, or hidden-class finals. Enum constructors and `Class`’s constructor stay special-cased even after the flag.

> [!tip] Interview answer
> **`setAccessible(true)` on a `Field` / `Method` / `Constructor` suppresses Java language access checks for that object so you can use a non-public member — it does not make the member public.** Same-module and unnamed-module code usually succeeds; a named module whose package is not open throws `InaccessibleObjectException` (`trySetAccessible` returns `false` instead). **`isAccessible` is the wrong test — use `canAccess`. The flag still will not let you `Field.set` a static final, a record field, or construct `java.lang.Class`.**
