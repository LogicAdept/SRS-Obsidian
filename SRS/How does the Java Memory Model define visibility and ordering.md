<!--
reps: 0
priority: 0
-->
#Java/JMM #SRS

# How does the Java Memory Model define visibility and ordering

> [!abstract] Short answer
> **The Java Memory Model (JLS 17.4) answers both questions with one relation: happens-before.** A write is *visible* to a read only if an happens-before edge orders them; otherwise reads may see stale values, and both compiler and hardware may reorder freely as long as the per-thread (as-if-serial) result is preserved. Properly synchronized programs — every data-race pair ordered by happens-before — run with plain sequential-consistency semantics.

## The edges that create ordering

Actions (reads/writes, monitor ops, thread ops) are ordered two ways: program order inside one thread, and synchronizes-with edges across threads that happens-before then stitches transitively.

```d2
direction: right
po: "Program order\nwithin a thread" {
  width: 250
  height: 90
  style.fill: "#e3f2fd"
}
sw: "Synchronizes-with\nmonitor unlock/lock, volatile w/r,\nThread.start/join, interrupt" {
  width: 380
  height: 110
  style.fill: "#fff3e0"
}
hb: "Happens-before\ntransitive closure of both" {
  width: 290
  height: 90
  style.fill: "#e8f5e9"
}
vis: "Visibility + ordering\nguaranteed" {
  width: 260
  height: 80
  style.fill: "#e8f5e9"
}
po -> hb
sw -> hb
hb -> vis
```

**Fig. 1.** Happens-before is the transitive closure of program order and the synchronizes-with edges; that relation defines visibility and ordering.

The synchronizes-with pairs from the spec: an unlock synchronizes-with every subsequent lock of the same monitor; a volatile write with every subsequent read of that field; `start()` with everything in the started thread; everything in a thread with a `join()` that detects its termination; `interrupt` with the point where interruption is detected; and, transitively, the release/acquire pattern they compose.

```java
public class HappensBeforeDemo {
    static int data;                 // plain field
    static volatile boolean ready;   // volatile flag

    public static void main(String[] args) throws Exception {
        Thread writer = new Thread(() -> {
            data = 42;
            ready = true;
        });
        writer.start();
        writer.join();                 // join() creates the happens-before edge
        System.out.println("with HB edge (volatile + join): data = " + data);

        int stale = 0, tries = 2_000;
        for (int t = 0; t < tries; t++) {
            data = 0; ready = false;
            Thread w = new Thread(() -> { data = 42; ready = true; });
            w.start();
            while (!ready) { /* volatile spin */ }
            if (data != 42) stale++;
            w.join();
        }
        System.out.println("reads after volatile flag: stale " + stale + " out of " + tries);
    }
}
```

**Listing 1.** Verified on JDK 21:

```java
with HB edge (volatile + join): data = 42
reads after volatile flag: stale 0 out of 2000
```

**Listing 2.** Zero stale reads in 2 000 two-thread exchanges: the volatile read that observes `ready` synchronizes-with the volatile write, so `data = 42` — which precedes the flag write in program order — happens-before the data read. That is the model working, not luck.

> [!warning] Happens-before is not clock time and not atomicity
> Two misreadings cost interviews. First, HB orders *visibility*, not wall-clock execution: the spec says explicitly that actions ordered by happens-before need not execute in that order if the results stay consistent — reordering is legal whenever unobservable. Second, HB says nothing about atomicity of compound actions: knowing when a value becomes visible does not make `i++` safe — see [[Why is the Java increment operator not atomic]]. And the flip side: *without* an edge, "the write happened earlier in real time" guarantees nothing — the read may return the default value, an older value, or the new one, all legal. That unbounded behavior is what "data race" means — see [[What is the difference between a race condition and a data race]] and [[What is memory visibility in the Java Memory Model]].

> [!tip] Interview answer
> **The JMM defines everything through happens-before: the transitive closure of program order plus synchronizes-with edges — volatile write/read, monitor unlock/lock, thread start/join. Writes ordered by such an edge are visible and ordered to subsequent reads; without an edge, any staleness is legal and reordering is permitted as long as single-thread semantics hold. Properly synchronized programs get sequential consistency.**

