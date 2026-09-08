<!--
reps: 0
priority: 0
-->
#Java/String #Java/Security #Java/JVM/Memory/Heap #SRS

# What are the security implications of string interning?

> [!abstract] Short answer
> Interning makes a string a **process-global, shared, long-lived object** — and that is exactly what secrets must not be. A `String` that holds a password stays a canonical, reachable instance until GC decides otherwise, and it cannot be zeroed because `String` is immutable ([[Why is java.lang.String immutable and final]]). That is why `Console.readPassword` returns **`char[]`** and its javadoc tells you to "manually zero the returned character array after processing to minimize the lifetime of sensitive data in memory" — [[What does the String intern method do in Java]], [[What is the Java string pool]].

## Three concrete risks

- **Longer lifetime of secrets** — literals and `intern()`ed values sit in the global table as canonical instances; a credential that entered a `String` cannot be actively erased, only *eventually* collected. Use `char[]`/`byte[]` for credentials and overwrite them (`Arrays.fill(pwd, ' ')`) when done — the documented `readPassword` pattern.
- **Global sharing** — an interned string is the *same instance* for the whole JVM, so assumptions built on it (identity checks, lock objects, caching keyed by `==`) couple unrelated subsystems. Untrusted input flowing into `intern()` turns a per-request object into a process-wide one.
- **Unbounded interning as a resource vector** — an attacker who supplies millions of unique strings gives your string table millions of entries: churn, contention on the global table, and memory pressure. Intern only bounded, application-owned vocabularies ([[How do you find the cause of a memory leak in Java]]).

```java
import java.io.Console;
import java.util.Arrays;

public class Password {
    public static void main(String[] args) {
        Console cons = System.console();
        if (cons != null) {
            char[] pwd = cons.readPassword("Password: ");
            try {
                check(pwd);            // use it
            } finally {
                Arrays.fill(pwd, ' '); // zero it: minimize the lifetime
            }
        }
    }

    static void check(char[] pwd) { /* verify against stored hash */ }
}
```

**Listing 1.** The documented pattern: read the credential into a `char[]`, use it, and zero the array in `finally`. The credential never becomes an immutable, interned `String`.

```d2
direction: right
str: "String password\n(interned or literal)" {
  width: 260
  height: 60
  style.fill: "#fce4ec"
}
pool: "global string table\ncanonical instance" {
  width: 250
  height: 56
  style.fill: "#fff8e1"
}
share: "shared process-wide,\ncannot be zeroed" {
  width: 270
  height: 56
  style.fill: "#fce4ec"
}
arr: "char[] from readPassword\nzeroed in finally" {
  width: 280
  height: 60
  style.fill: "#e8f5e9"
}
str -> pool: "joins"
pool -> share
arr -> share: "avoids"
```

**Fig. 1.** A `String` credential is pinned as a global canonical instance; a zeroed `char[]` never enters that club.

> [!warning] "The pool makes strings faster to compare" is not a security argument
> Identity comparison (`==`) on interned strings is a micro-optimization that invites coupling and, worse, tempts people to intern **user input** "for performance". Hash-based lookups (`HashMap`, `equals`) already handle equality safely for arbitrary strings; global interning buys little and extends exposure for values that may outlive the request.

> [!tip] Interview answer
> Interning turns a string into a shared, canonical, process-global object that cannot be wiped — bad properties for secrets, which is why `readPassword` hands back a `char[]` that you zero after use. Interned values also couple unrelated code through one instance, and letting attacker-controlled input flood `intern()` stresses the global table. So: intern only bounded internal vocabularies, keep credentials in mutable arrays, and never key security decisions on interned identity.
