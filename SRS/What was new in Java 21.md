<!--
reps: 0
priority: 0
-->
#Java/Versions/21 #SRS

# What was new in Java 21

> [!abstract] Short answer
> **Java 21 (September 2023, LTS) finalized the Loom-and-patterns generation: virtual threads (JEP 444), pattern matching for `switch` (JEP 441), record patterns (JEP 440), and sequenced collections (JEP 431), plus generational ZGC (JEP 439), a Key Encapsulation Mechanism API (JEP 452), and — famously — string templates as a **preview** (JEP 430) that was later withdrawn.** Structured concurrency (453) and scoped values (446) entered preview here, not final ([[How would you explain Java 17 21]]).

## The final four, the runtime pair, the withdrawn one

**Virtual threads** (JEP 444) made thread-per-request scale: `Thread.ofVirtual()` / `Executors.newVirtualThreadPerTaskExecutor()`, cheap blocking, no pooling ([[How would you explain Virtual Threads]]). **Pattern `switch`** (JEP 441) finalizes selector patterns with `when` guards and null labels ([[What is the difference between pattern matching and a switch statement]]). **Record patterns** (JEP 440) deconstruct records, nestable ([[How do records work with pattern matching in switch]]). **Sequenced collections** (JEP 431) give ordered collections a positional API ([[What are sequenced collections]]).

Runtime: **generational ZGC** splits the heap into young/old generations for throughput at ZGC pause levels; **KEM API** (JEP 452) standardizes post-quantum-adjacent key encapsulation. Previews: structured concurrency, scoped values, string templates — and the templates story is the era's cautionary tale: previewed in 21 (430), again in 22 (459), then **withdrawn**, never final ([[What is a preview feature in Java]]).

```d2
direction: down
fin: "Final in 21" {
  shape: rectangle
  vt: "virtual threads (444)"
  ps: "pattern switch (441)"
  rp: "record patterns (440)"
  seq: "sequenced collections (431)"
}
run: "Runtime" {
  shape: rectangle
  zgc: "generational ZGC (439)"
  kem: "KEM API (452)"
}
prev: "Preview in 21" {
  shape: rectangle
  sc: "structured concurrency (453)"
  sv: "scoped values (446)"
  st: "string templates (430) -> withdrawn later"
}
```

**Fig. 1.** Four finals define the release; ZGC/KEM are the runtime work; the preview shelf holds structured concurrency and scoped values still climbing — and string templates, which never arrived.

```java
public class V24_Java21 {
    public static void main(String[] args) throws Exception {
        Thread vt = Thread.ofVirtual().name("v-worker").start(() -> {
            System.out.println("in thread: " + Thread.currentThread().getName()
                    + " virtual=" + Thread.currentThread().isVirtual());
        });
        vt.join();
        System.out.println("after join virtual=" + vt.isVirtual());
        System.out.println("still java.lang.Thread: " + (vt instanceof Thread));
    }
}
```

**Listing 1.** Verified on JDK 21 (V24_Java21 in empirics): `in thread: v-worker virtual=true`, `after join virtual=true`, `still java.lang.Thread: true` — the headline final: a virtual thread is an ordinary `Thread` the scheduler does not pin to an OS thread (out/V24_Java21.txt).

> [!warning] The 21 myths: string templates, pinning, and the 17-blend
> Citing "string templates" as a Java 21 feature is the modern classic error — they previewed (430) and died before finalization; never list them as shippable. Virtual threads in 21 **pin** inside `synchronized` blocks (fixed only in 24, JEP 491) — "no more pinning anywhere" is 24-era talk. And interviews routinely blend 17's sealed classes or 16's records into "21 features" — records were final in **16**, sealed in **17**; 21's language finals are pattern switch and record patterns ([[What was removed or deprecated in Java 17]]).

> [!tip] Interview answer
> **Java 21 LTS finalized virtual threads, pattern switch, record patterns, and sequenced collections; generational ZGC and the KEM API are the runtime work; structured concurrency and scoped values previewed here.** The honest footnote: string templates previewed in 21 and were later withdrawn — and virtual-thread pinning inside synchronized lasted until 24.
