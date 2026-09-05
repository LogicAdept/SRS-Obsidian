<!--
reps: 0
priority: 0
-->
#Java/JVM/JIT #SRS

# How does JIT compilation work on the JVM?

> [!abstract] Short answer
> HotSpot **interprets** bytecode first, then **compiles hot methods to native code** while the process is running. Cold code stays interpreted. Default mixed mode (`-Xmixed`) is that split. A JIT is allowed, not required: a VM may keep interpreting every instruction.

## Interpreter, then hot spots

Launch uses a **standard interpreter**. As the program runs, HotSpot looks for **performance bottlenecks (hot spots)** — methods (and loop bodies) that actually execute a lot — and compiles those to machine code for a boost. **Seldom-used code is left interpreted.** Native results live in the **code cache**.

That mixed policy is the default `java` mode: execute bytecode in the interpreter **except** hot methods, which become native. `-Xint` turns compilation off entirely (no JIT benefit). `-Xcomp` forces compilation up front as a **testing** mode; it is not a production setting.

The abstract machine does not mandate a compiler. Translating JVM instructions into machine code is an implementation choice. HotSpot’s choice is adaptive compilation.

## Tiered compilation (C1 then C2)

On the **server VM**, **tiered compilation** is on by default (Java SE 7). Without it, the server VM profiles in the interpreter, then hands that profile to the **server compiler**. With it, the VM also uses the **client compiler** to emit **compiled, self-profiling** versions. That compiled profiling phase is substantially faster than the interpreter, so startup can look more like a client VM while the **final server-compiler** code still arrives — often earlier — and peak code can be better because profiling had more time.

There is no separate client VM in current JDK builds; the **client compiler (C1)** is still a compilation **tier** inside the server VM. The **server compiler (C2)** is the full optimizing backend.

HotSpot’s policy uses **five execution levels**:

| Level | What runs |
| --- | --- |
| 0 | Interpreter (counters / `MethodData`) |
| 1 | C1, fully optimized, **no** profiling |
| 2 | C1 with invocation and backedge counters |
| 3 | C1 with **full** profiling (into an MDO) |
| 4 | C2, profile-guided full optimization |

In mixed mode, execution **starts at 0**. A typical promotion is **0 → 3 → 4**. If the C2 queue is congested, the policy prefers **0 → 2** first (level 2 is cheaper than full C1 profiling) and later 2 → 3 → 4. **Trivial** methods can stop at **level 1** instead of 4. Transitions are driven by **invocation** and **backedge** counters; a hot loop can compile **on-stack (OSR)** from a backedge, not only from a method entry. Thresholds scale with compiler-queue load. `-XX:CompileThresholdScaling` scales first-compilation thresholds; `0` disables compilation. `-XX:-TieredCompilation` turns the tiered scheme off.

Compiled native code is stored in a **segmented code cache**: a small **non-method** heap (interpreter / compiler buffers), a **profiled** heap (lightly optimized, shorter-lived methods), and a **non-profiled** heap (fully optimized, longer-lived). Default reserved size is **240 MB** with tiered compilation, **48 MB** if you disable it.

## What the compilers actually change

Once a method is compiled, the adaptive compiler chooses extra optimizations. **Inlining** copies a callee into the caller so the call (and further opts on the combined body) go away — [[What is method inlining in the JIT]]. **Escape analysis** (on by default; `-XX:-DoEscapeAnalysis` disables it) classifies a `new` object as globally escaping, argument-escaping, or **no-escape / scalar-replaceable**. C2 may then **delete the allocation** and the locks around it, and may **elide locks** on objects that do not globally escape. That is **not** “allocate it on the Java stack instead of the heap.” Details: [[How would you explain Escape analysis]].

The same mixed story is why Java is both compiled and interpreted: [[Is Java a compiled or interpreted language]].

```d2
direction: down
bc: "bytecode in a class file" {
  width: 260
  height: 50
}
l0: "level 0: interpreter" {
  width: 280
  height: 50
  style.fill: "#fff8e1"
}
c1: "C1 client compiler\nlevels 1–3, often with profiling" {
  width: 300
  height: 70
  style.fill: "#e3f2fd"
}
c2: "C2 server compiler\nlevel 4, full optimization" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}
cc: "code cache (native nmethods)" {
  width: 280
  height: 50
}
bc -> l0: "-Xmixed starts here"
l0 -> c1: "hot (invocations / backedges)"
c1 -> c2: "profile mature"
c1 -> cc
c2 -> cc
```

**Fig. 1.** Default HotSpot path under `-Xmixed`: interpret, compile hot methods with C1, then C2. Cold methods stay interpreted.

```java
public final class HotSquare {
    static int square(int n) {
        return n * n;
    }

    public static void main(String[] args) {
        long acc = 0L;
        for (int i = 0; i < 1_000_000; i++) {
            acc += square(i);
        }
        System.out.println(acc);
    }
}
```

**Listing 1.** A tiny callee in a tight loop is the kind of **hot** method mixed mode will consider for compilation and inlining. The iteration count is not a published compilation threshold. Run the same program with `-Xint` and it never leaves the interpreter.

> [!warning] Escape analysis is not stack allocation
> HotSpot C2 **eliminates** scalar-replaceable allocations and may drop locks on objects that do not globally escape. It does **not** rewrite a heap `new` into a Java stack allocation. Saying “if it does not escape, it lives on the stack” is the interview myth.

> [!warning] First calls are still interpreted
> JIT is **after** the method has already run. Microbenchmarks and “first request” latency often measure the interpreter plus C1, not C2. `-Xcomp` compiles at first use to exercise the compilers; it is a test switch, not how you run production. A full code cache or `-Xint` also means you stay slow.

> [!tip] Interview answer
> The JVM interprets bytecode first. HotSpot counts calls and loop backedges, compiles the hot methods to native code in the code cache, and leaves cold methods interpreted. With default tiered compilation the client compiler (C1) produces fast profiled native code, then the server compiler (C2) produces the fully optimized version, including inlining and escape-analysis scalar replacement — not stack allocation.
