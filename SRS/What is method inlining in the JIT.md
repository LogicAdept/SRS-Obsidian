<!--
reps: 0
priority: 0
-->
#Java/JVM/JIT #SRS

# What is method inlining in the JIT?

> [!abstract] Short answer
> The compiler **copies a callee’s body into the caller** and drops that call. HotSpot does this while compiling, on by default (`-XX:+Inline`). The point is not only a cheaper call: the combined method can then be optimized as one unit.

## Copy the callee, then optimize the mix

HotSpot’s adaptive compiler chooses extra opts on compiled code; **inlining** is the named example. After the caller is a JIT compilation candidate, a small or hot callee can be expanded in place. There is no `invoke*` for that site in the generated native code.

That rewrite is what lets later passes see through a getter. After a getter such as `getPerson` is inlined, C2 can prove a defensive copy is unused and delete it — [[How would you explain Escape analysis]]. Inlining is a step on the same pipeline as [[How does JIT compilation work on the JVM]], not a `javac` rewrite of your `.java` file.

It is **not guaranteed**. `-XX:CompileCommand=inline,…` **attempts** to inline a method; `dontinline` **prevents** it. Compiler-control directives are sharper: prefix a method pattern with `+` to **force** inlining or `-` to **prevent** it (first matching pattern in the `inline` array wins). `-XX:-Inline` turns the opt off globally.

C2 will not inline an arbitrarily large body:

| Limit (C2) | Role | Default in the `java` man / HotSpot flags |
| --- | --- | --- |
| `-XX:MaxInlineSize` | Cold method, bytecode size | **35** |
| `-XX:FreqInlineSize` | Hot method, bytecode size | platform-dependent (man example **325**) |
| `-XX:MaxTrivialSize` | Trivial method | **6** |
| `-XX:InlineSmallCode` | Already-compiled callee, native size | platform / tiered |
| `MaxInlineLevel` | Nested inlines (high-tier compiler) | **15** |
| `MaxRecursiveInlineLevel` | Nested recursive inlines | **1** |

C1 has parallel caps (`-XX:C1MaxInlineSize` **35**, `-XX:C1MaxTrivialSize` **6`). Diagnostic: `-XX:+UnlockDiagnosticVMOptions -XX:+PrintInlining`.

```d2
direction: down
before: "caller: invoke square\ncallee: return n*n" {
  width: 280
  height: 60
  style.fill: "#fff8e1"
}
after: "caller: … n*n …\nno call at that site" {
  width: 280
  height: 60
  style.fill: "#e8f5e9"
}
before -> after: "inline"
```

**Fig. 1.** Inlining replaces a call with the callee’s body. Size, depth, `dontinline`, and `-XX:-Inline` can keep the call.

```java
public final class InlineCandidate {
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

**Listing 1.** `square` is a few bytecodes — a **trivial / MaxInlineSize** candidate once `main` is compiled. The loop count is not a threshold. `java -XX:CompileCommand=dontinline,InlineCandidate.square` keeps a real call.

> [!warning] `inline` attempts; size still wins
> CompileCommand `inline` does **not** promise a successful inline. A callee over `MaxInlineSize` / `FreqInlineSize`, too much inline depth, or `-XX:-Inline` leaves a call. Directives with `+` request a force; they still compete with those limits. `dontinline` and directive `-` are the reliable “do not inline this.”

> [!warning] Inlining is a compiled-code opt
> Until the **caller** is JIT-compiled, you still pay interpreted calls. `-Xint` never inlines. A huge callee can still be invoked from compiled code; it just will not be pasted into that caller.

> [!tip] Interview answer
> JIT inlining copies a callee into its caller so that call disappears and later opts, including escape analysis, can see the combined body. HotSpot does this by default while compiling; tiny and hot methods are the usual candidates. It is not a language rule: bytecode-size caps, inline depth, `-XX:-Inline`, and `dontinline` all keep a real call.
