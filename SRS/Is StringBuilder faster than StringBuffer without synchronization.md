<!--
reps: 0
priority: 0
-->
#Java/StringBuilder #Java/String #SRS

# Is StringBuilder faster than StringBuffer without synchronization?

> [!abstract] Short answer
> **Yes.** **`StringBuilder`** is an API-compatible **`StringBuffer`** with **no synchronization**. The API recommends it as a **drop-in for a single thread** and states it **will be faster under most implementations**. **`StringBuffer`** methods are **synchronized** so concurrent calls on one instance serialize; since JDK 5 it says **`StringBuilder` should generally be preferred** because it is **faster, as it performs no synchronization**. Difference: [[What is the difference between StringBuilder and StringBuffer]]. Immutability of `String`: [[How would you explain immutability and its benefits in Java]]. Design: [[How would you explain which design pattern ideas appear in StringBuilder and StringBuffer]].

## Same API, no monitor on each append

Both are **mutable** character sequences (`append` / `insert`, growing **capacity**, default **16**). **`StringBuffer`** is **thread-safe**: operations on one instance behave as if they occur in a **serial order** consistent with each thread’s calls. It synchronizes on the **buffer**, not on a **source** sequence you append. **`StringBuilder`** is **not** safe for multiple threads; if you need that, use **`StringBuffer`**.

“Without synchronization” means **use `StringBuilder`**, not a hand-stripped `StringBuffer`. There is **no** specified speedup factor — only **no per-call monitor** in the usual implementation. Shared **`StringBuilder`** is a **data race**, not a faster buffer.

```java
StringBuilder sb = new StringBuilder();
sb.append("a").append("b");
StringBuffer buf = new StringBuffer();
buf.append("a").append("b");
```

**Listing 1.** Same fluent `append`. The builder skips the lock `StringBuffer` takes on each mutating call.

```d2
direction: down
sb: "StringBuilder" {
  width: 160
  height: 36
  style.fill: "#e8f5e9"
}
buf: "StringBuffer" {
  width: 160
  height: 36
  style.fill: "#fff8e1"
}
sb -> buf: "compatible API"
buf -> sb: "plus synchronized methods"
```

**Fig. 1.** Prefer the builder unless one instance is shared across threads.

> [!warning] Faster is not a license to share a builder
> Concurrent `append` on one `StringBuilder` is **undefined**. Use **`StringBuffer`**, or one builder **per thread**, or a **lock you own**.

> [!warning] No promised “N times faster”
> The specification says **faster under most implementations** / **faster because no synchronization**. Benchmark your JDK if the difference matters.

> [!tip] Interview answer
> Yes: StringBuilder is the unsynchronized StringBuffer, and the API says it is faster for that reason and should be the default. StringBuffer still exists for a buffer shared by threads. I never share a StringBuilder to go faster.
