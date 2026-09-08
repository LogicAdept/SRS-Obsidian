<!--
reps: 0
priority: 0
-->
#Java/String #SRS

# What does the String intern method do in Java?

> [!abstract] Short answer
> `intern()` returns the **canonical instance** of the string's contents. Contract (from the javadoc): a pool of strings is "maintained privately by the class `String`"; if the pool already contains an `equals`-equal string, that pooled instance is returned — otherwise **this** object is added to the pool and returned. Therefore `s.intern() == t.intern()` holds **if and only if** `s.equals(t)`. Literals and constant expressions are interned automatically; `intern()` lets runtime-built strings join the same club — [[What is the Java string pool]], [[How do string literals enter the Java string pool]].

## What it buys and what it costs

- **Deduplication** — long-lived, repeated strings (country codes, statuses, parsed identifiers) collapse to one instance each; a stream of duplicates stops multiplying heap usage.
- **Identity shortcut** — after interning, `==` is a valid equality check for those references (canonical instance per content), which is why interning is sometimes used before cheap comparisons.
- **Cost** — every `intern()` is a hash lookup in the JVM's string table (HotSpot default capacity 65536 buckets, `-XX:StringTableSize`); runtime-interned strings stay reachable as long as referenced, and churn adds table maintenance. HotSpot's table is cleaned by GC, so entries for unreachable strings do go away — but interning unbounded user input is still a footgun ([[What are the security implications of string interning]]).

```java
public class InternDemo {
    public static void main(String[] args) {
        String s1 = "2026-09-09";                      // literal: pooled
        String s2 = new StringBuilder("2026-0")        // runtime-built
                .append(9).append("-09").toString();
        System.out.println(s1 == s2);                  // false
        System.out.println(s1 == s2.intern());         // true: canonical
        String s3 = s2.intern();
        System.out.println(s2.intern() == s3.intern()); // true: contract
    }
}
```

**Listing 1.** A runtime-built copy is a distinct object until `intern()` maps it to the canonical pooled instance; two `intern()` calls with equal contents always return the same reference. Verified on JDK 21.

```d2
direction: right
rt: "runtime String\n\"2026-09-09\" (fresh)" {
  width: 260
  height: 60
  style.fill: "#fce4ec"
}
pool: "String.intern()" {
  width: 200
  height: 50
  style.fill: "#fff8e1"
}
canon: "canonical instance\n(the pooled one)" {
  width: 260
  height: 56
  style.fill: "#e8f5e9"
}
lit: "literal \"2026-09-09\"\n(same instance)" {
  width: 260
  height: 56
  style.fill: "#e3f2fd"
}
rt -> pool: "lookup"
pool -> canon: "existing: return it\nmissing: add this object"
canon == lit
```

**Fig. 1.** `intern()` either hands back the pooled instance for equal contents or installs the argument as the new canonical one; the literal already points at that instance.

> [!warning] Never lock on an interned string
> Interned strings are **globally shared**, so `synchronized (someInternedString)` can interleave with completely unrelated code that interned the same contents — same monitor, unrelated subsystems, deadlocks that make no sense in a stack trace. And do not `intern()` unbounded, attacker-shaped input: the table is JVM-global, and churn there is felt process-wide.

> [!tip] Interview answer
> `intern()` gives me the one canonical instance for the string's contents: if the pool already has an equal string it returns that, otherwise it adds this object. So `s.intern() == t.intern()` iff `s.equals(t)`. I use it to dedup long-lived repeated values; literals and compile-time constants are interned anyway. I avoid it for unbounded input and never use interned strings as lock objects, because the monitor is shared process-wide.
