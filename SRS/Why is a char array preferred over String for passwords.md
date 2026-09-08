<!--
reps: 0
priority: 0
-->
#Java/String #Java/Security #SRS

# Why is a char array preferred over String for passwords

> [!abstract] Short answer
> **You can overwrite a `char[]`. You cannot overwrite a `String`.** `PBEKeySpec` stores passwords as `char[]` for that reason: a `String`’s value is constant, so there is no API to zero it when you are done. `Console.readPassword` returns `char[]` and tells you to `Arrays.fill` afterward. A password as `String` remains readable in the heap until the object is collected (and copies may linger). That is **not** the intern pool unless you interned it or used a literal.

## Wipe vs immutable text

A `String` has a constant value. Sharing is the point of immutability; it is the wrong property for a secret. Crypto APIs clone the `char[]`, let you `clearPassword()`, and make `getPassword()` your copy to zero ([[How would you explain java.lang.String]]). Zero that copy too — it is a second array.

`toCharArray()` is a **copy** of UTF-16 units; wiping that array does not change the `String` ([[How do you turn a Java string into a char array]]). `intern()` publishes a canonical un-wipeable instance — never intern a password ([[What are the security implications of string interning]]). Wrapping `char[]` in `new String(...)` creates that un-wipeable object on purpose.

Official advice still has a limit: clearing mutable structures has **reduced effectiveness** on typical JVMs because objects are moved in memory. Zeroing is still required; it is not a perfect erase. Do not log the password.

```d2
direction: down
s: "Password as String\nimmutable · no overwrite · heap until GC" {
  width: 320
  height: 50
}
a: "Password as char[]\nuse then Arrays.fill / clearPassword" {
  width: 320
  height: 50
}

s -> a: "prefer"
```

**Fig. 1.** The preference is overwriting, not “arrays skip the heap.”

```java
public class PasswordCharsDemo {
    static void useThenWipe(char[] password) {
        try {
            // PBEKeySpec / KeyStore / similar
        } finally {
            if (password != null) {
                java.util.Arrays.fill(password, '\0');
            }
        }
    }
}
```

**Listing 1.** Same pattern as `Console.readPassword`: process the `char[]`, then fill it (`'\0'` or spaces). Wipe in `finally` so exceptions still clear it. Do not wrap it in `new String(password)` unless you accept another un-wipeable copy.

> [!warning] Not “passwords live in the string pool”
> A typical `readLine()` / `new String(chars)` password is a heap `String`, not automatically interned. The risk is **immutability**, not PermGen. Interning or putting `"secret"` in source is worse. Wiping `char[]` does not erase copies already taken by logs, `String` constructors, `getPassword()`, or a moving collector.

> [!tip] Interview answer
> **`String` cannot be zeroed; `char[]` can.** That is why password APIs take arrays and why you `fill` them after use. Secrets as `String` sit in the heap until GC. They are not in the intern pool unless you interned them or wrote a literal.
