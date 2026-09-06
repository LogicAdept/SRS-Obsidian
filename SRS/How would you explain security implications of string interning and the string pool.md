<!--
reps: 0
priority: 0
-->
#Java/String #Java/Security #Java/JVM/Memory #SRS

# How would you explain security implications of string interning and the string pool

> [!abstract] Short answer
> **Interning makes a `String` the process-wide canonical instance for that character sequence. You still cannot overwrite it.** Secrets as literals stay interned while the class is loaded (bootstrap classes never unload). `intern()` of a password or token copies that immutability into the intern table: heap dumps, `==` sharing, and no `clearPassword`. Untrusted unique `intern()` is a heap-exhaustion path. Use `char[]`, zero it, and never intern secrets.

## Canonical, immutable, visible longer than you think

A `String` has a constant value. Crypto APIs take `char[]` for that reason: there is no way to overwrite a `String` when you are done (`PBEKeySpec`, `clearPassword`). `Console.readPassword` returns `char[]` and tells you to `Arrays.fill` afterward. Interning does **not** create a wipeable copy; it **publishes** the same immutable object as the interned identity for every equal sequence ([[How would you explain java.lang.String]], [[How do you turn a Java string into a char array]]).

Literals and compile-time constants are interned when the class is created. They are also `CONSTANT_String` in the class file. Anyone with the JAR or a heap dump can read them. Those interned instances stay reachable from the class’s run-time constant pool until the class can be unloaded — bootstrap types **cannot** unload ([[How do string literals enter the Java string pool]], [[How long do strings live in the Java string pool]]).

`intern()` of data you built at run time puts **that** object (or an equal one already pooled) in `String`’s private pool. HotSpot’s table holds only a weak handle, so an interned string with **no other refs** can be collected — it is not PermGen immortality. That does **not** make intern safe: while it lives it is shared and un-wipeable; GC movement also means even wiping a `char[]` is imperfect. Filling the table with attacker-chosen distinct strings still competes for **heap** (interned strings moved onto the heap with PermGen’s removal).

Do not intern passwords, session tokens, or untrusted payloads to “dedupe.” Do not log them (`toString` of internals). Deduplication of interned strings is a separate GC feature and is not a confidentiality control.

```d2
direction: down
secret: "Secret as String / literal" {
  width: 260
  height: 45
}
pool: "intern pool\ncanonical instance · cannot overwrite" {
  width: 300
  height: 50
}
leak: "class file · heap dump · == sharing · long-lived class CP" {
  width: 340
  height: 55
}
ok: "char[] · zero after use\nPBEKeySpec.clearPassword" {
  width: 280
  height: 50
}

secret -> pool: "intern() or literal"
pool -> leak
secret -> ok: "do this instead"
```

**Fig. 1.** Interning publishes an immutable canonical `String`. Secrets belong in arrays you can clear.

```java
public class InternSecurityDemo {
    static void wipe(char[] password) {
        java.util.Arrays.fill(password, '\0');
    }

    static void doNotIntern(String password) {
        password.intern(); // process-wide canonical String; no overwrite API
    }
}
```

**Listing 1.** `readPassword`-style handling: `char[]` then fill. `intern` on a secret is the opposite of minimizing lifetime.

> [!warning] Intern is not a vault and not a forever lock
> Do not treat the pool as encrypted storage. Do not assume an interned secret lives until JVM exit — HotSpot may collect it if nothing else refers to it — and do not assume it is gone after GC either. A literal `"hunter2"` in source is interned for as long as that class stays loaded. `intern()` of unbounded unique user input can exhaust the heap. Clearing arrays is still required and still not a perfect erase on a moving collector.

> [!tip] Interview answer
> **Interning shares one immutable `String` for equal text; you cannot wipe it.** Keep secrets in `char[]` and zero them; never intern passwords or untrusted unique strings. Literals of secrets live with the class (and in the class file). The pool is a canonical cache, not a security boundary.
