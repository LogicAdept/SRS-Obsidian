<!--
reps: 0
priority: 0
-->
#Java/JVM/JIT #SRS

# How would you explain Escape analysis?

> [!abstract] Short answer
> It is a **HotSpot server-compiler (C2)** analysis of a `new` object’s uses: does that object **escape** the allocating method and thread? From that, C2 may **delete the allocation** (scalar replacement) and **drop locks** on objects that are not globally escaped. It does **not** move the object onto the Java stack.

## Three escape states, then opts

Escape analysis is on by default (Java SE 6u23 onward; `-XX:+DoEscapeAnalysis`, disable with `-XX:-DoEscapeAnalysis`). It is **flow-insensitive**. C2 classifies each allocation:

| State | Meaning |
| --- | --- |
| `GlobalEscape` | Escapes the **method and the thread**. Stored in a `static`, stored in a field of an already-escaped object, or **returned**. |
| `ArgEscape` | Passed as an **argument** (or reachable from one) but does not globally escape during that call. C2 decides this by looking at the **callee bytecode**. |
| `NoEscape` | **Scalar-replaceable**: the allocation can be removed from the generated code. |

After that:

- **NoEscape** — C2 may **eliminate the allocation** and the locks that went with it. The object need not exist in the generated code; its fields are used as independent values.
- **Not `GlobalEscape`** — C2 may **elide synchronization** on that object (lock elision). Typical story: a local `StringBuffer` or `Vector`, whose methods are synchronized for sharing, but this instance never leaves the thread.
- C2 **does not** rewrite a heap `new` into a Java **stack allocation**.

So “it lives on the stack instead of the heap, therefore less GC” is the wrong mechanism. If the allocation is **gone**, there is no heap object. If it still **escapes**, it is a normal heap object. Stack-vs-heap for Java locals is a different question: [[Is it true that primitives live on the stack and reference instances live on the heap]].

Inlining often has to happen first. A defensive copy inside a getter stays an escape until C2 **inlines** the getter and sees that the caller never publishes or mutates the copy — then the copy can disappear. That pairing is why EA sits next to [[What is method inlining in the JIT]] on the JIT pipeline: [[How does JIT compilation work on the JVM]].

```d2
direction: down
alloc: "new T() in compiled method" {
  width: 280
  height: 50
}
ask: "does it escape?" {
  width: 240
  height: 50
}
ge: "GlobalEscape → real heap object" {
  width: 320
  height: 50
  style.fill: "#ffebee"
}
ae: "ArgEscape → heap, maybe lock opts" {
  width: 320
  height: 50
  style.fill: "#fff8e1"
}
ne: "NoEscape → delete allocation\n(+ associated locks)" {
  width: 320
  height: 70
  style.fill: "#e8f5e9"
}
alloc -> ask
ask -> ge: "static / field / return"
ask -> ae: "passed in, not published"
ask -> ne: "scalar replaceable"
```

**Fig. 1.** C2 escape states. Only `NoEscape` is “the object need not exist.” None of the arrows is “allocate it on the Java stack.”

```java
public final class EscapeDemo {
    static final class Point {
        int x, y;
        Point(int x, int y) { this.x = x; this.y = y; }
    }

    static int manhattan(int x, int y) {
        Point p = new Point(x, y);
        return Math.abs(p.x) + Math.abs(p.y);
    }

    static String join(String a, String b) {
        StringBuffer buf = new StringBuffer();
        buf.append(a);
        buf.append(b);
        return buf.toString();
    }

    static Point published(int x, int y) {
        return new Point(x, y);
    }

    public static void main(String[] args) {
        System.out.println(manhattan(-3, 4));
        System.out.println(join("a", "b"));
        System.out.println(published(1, 2).x);
    }
}
```

**Listing 1.** Shapes C2 looks at after it compiles this with EA on: `p` is a `NoEscape` candidate (never published); `buf` is a thread-local synchronized helper (lock-elision candidate); `published` is `GlobalEscape` because it **returns** the object. Whether a given run actually deletes `p` is a C2 decision, not a language guarantee.

> [!warning] Not stack allocation, and not a Java rule
> `NoEscape` means **scalar replacement**: the object can vanish from the native code. It does not mean “the instance lives in the current frame like a local `int`.” This is a **C2** opt, on by default; `-XX:-DoEscapeAnalysis` and `-Xint` turn it off. Returning the object, storing it in a field, or letting another thread see it is `GlobalEscape` — heap, locks, GC, all still real.

> [!warning] “Does not leave the method” is not `NoEscape`
> Passing the object into another method is **`ArgEscape`**, not `NoEscape`. C2 must prove from the callee that it is not published. A getter that returns `this.field` or a helper that stashes the argument in a collection makes it escape.

> [!tip] Interview answer
> Escape analysis is C2 asking whether a newly allocated object escapes the method and thread. No-escape objects can be scalar-replaced — the allocation and its locks disappear from the generated code — and objects that are not globally escaped can have their locks elided, which is why a local StringBuffer can lose its synchronization. HotSpot does not turn that object into a stack-allocated instance; if it still escapes, it is an ordinary heap object.
