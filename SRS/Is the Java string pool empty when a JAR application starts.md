<!--
reps: 0
priority: 0
-->
#Java/String #Java/JVM/Memory #SRS

# Is the Java string pool empty when a JAR application starts

> [!abstract] Short answer
> **No — not by the time `main` runs.** `String`’s intern pool is specified as **initially empty**, then it fills as classes are **created**. Startup loads, links, and initializes the initial class (and `Object` above it) **before** invoking `main`. Those creations intern literals. Bootstrap `java.lang` types are already in play. Your JAR’s main class interns its own `CONSTANT_String`s when it is created, still before `main`.

## Empty at birth, not empty at `main`

The pool is private to `String` and starts empty. Entry is intern: literals and constant concatenations when the class is created; anything else only via `intern()` ([[What is the Java string pool]], [[How do string literals enter the Java string pool]]).

Virtual machine startup does **not** jump to your `main` on a blank slate. It **creates** the initial class (bootstrap loader or a user-defined loader), **links**, **initializes** it, then calls `public static void main(String[])`. Initialization of that class requires initializing superclasses, in the simple case all the way to `Object`. Creating a class builds its run-time constant pool and interns each `CONSTANT_String`. Loading a class that contains a literal **may** allocate a new interned `String` if that sequence is not already pooled.

So when `main` first executes:

- Many bootstrap / `java.base` literals are already interned.
- Literals in your main class (and classes initialized as a consequence of its init) are already interned.
- `main`’s `String[] args` are ordinary arguments, not a spec promise of interned content.
- The pool is **not** preloaded with every string in the JAR — only classes that have actually been created.

HotSpot interned objects live on the heap; bootstrap classes never unload, so those interned literals stay ([[How long do strings live in the Java string pool]]).

```d2
direction: down
empty: "Pool initially empty" {
  width: 220
  height: 40
}
boot: "Create java.base / Object / …\nintern CONSTANT_String" {
  width: 300
  height: 50
}
app: "Create Main-Class\nintern its literals" {
  width: 260
  height: 50
}
main: "invoke main(String[])" {
  width: 220
  height: 40
}

empty -> boot -> app -> main
```

**Fig. 1.** “Application start” in a JAR is `main`. Interning of bootstrap and main-class literals has already happened.

```java
public class PoolAtStart {
    static final String MINE = "app-only-token";

    public static void main(String[] args) {
        boolean alreadyInterned = MINE == "app-only-token"; // true — class created before main
    }
}
```

**Listing 1.** The main class’s literals are interned at class creation, which startup performs before calling `main`.

> [!warning] “Initially empty” is not “empty in main”
> The intern javadoc describes VM-lifetime start of the table, not the first line of your program. Do not assume the JAR was scanned into the pool, and do not assume `args[i]` is interned. A class you never load contributes no literals.

> [!tip] Interview answer
> **The pool starts empty, then fills as classes are created.** Before `main`, the VM has already created bootstrap types and your initial class, so their string literals are interned. It is not empty when a JAR’s `main` runs, and it is not filled with the whole archive either.
