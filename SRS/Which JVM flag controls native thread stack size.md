<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Threads #Java/JVM/Tuning #SRS

# Which JVM flag controls native thread stack size?

> [!abstract] Short answer
> On the **`java` launcher (HotSpot):** **`-Xss`** *size* — stack size in **bytes** (`k`/`m`/`g` suffixes). Similar: **`-XX:ThreadStackSize=`** *size* in **kilobytes** (a suffix **scales that KB value**). Default **depends on the OS/CPU**. The VM may **round up** to a page. JVM stacks: [[What are Java threads composed of]]. What is a thread: [[What is thread]]. `StackOverflowError`: too little stack; many platform threads can **`OutOfMemoryError`** if stacks are huge.

## `-Xss`, not a JLS keyword

**JVMS** lets an implementation expose stack-size control. **HotSpot** does it with **`-Xss`**. Examples that all mean **1024 KB:** `-Xss1m`, `-Xss1024k`, `-Xss1048576`. Linux/x64 default in the man page: **1024 KB**; AArch64: **2048 KB**; Windows: **depends on virtual memory**.

Per-thread: **`Thread` constructors / `Thread.ofPlatform().stackSize(n)`** take an **approximate byte** hint that the VM **may ignore or clamp**. **Virtual** threads are **not** “one native stack of `-Xss` each.”

```text
java -Xss1m -jar app.jar
```

**Listing 1.** Process-wide default for **platform** thread stacks (HotSpot `java`).

```d2
direction: down
xss: "-Xss size (bytes)" {
  width: 200
  height: 36
  style.fill: "#e8f5e9"
}
xx: "-XX:ThreadStackSize (KB)" {
  width: 240
  height: 36
  style.fill: "#fff8e1"
}
st: "platform thread stack" {
  width: 200
  height: 36
  style.fill: "#e3f2fd"
}
xss -> st
xx -> st
```

**Fig. 1.** Two flags, **different units**. Mix them up and you are off by 1024.

> [!warning] `-XX:ThreadStackSize=1k` is not 1 KB
> The size is **already in KB**; `k` **multiplies again** → **1 MB**.

> [!warning] Not portable JLS
> `-Xss` is a **HotSpot/`java` tool** option. Another VM may use a different switch. `stackSize` in `Thread` is **platform-dependent**.

> [!tip] Interview answer
> Thread stack size is controlled with minus Xss on the java command, in bytes, with k or m suffixes. ThreadStackSize is the similar XX flag but the number is in kilobytes. Defaults depend on the platform, and a per-thread constructor stack size is only a hint.
