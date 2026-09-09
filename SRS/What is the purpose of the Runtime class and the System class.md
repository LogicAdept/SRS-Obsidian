<!--
reps: 0
priority: 0
-->
#Java/Runtime #SRS

# What is the purpose of the Runtime class and the System class

> [!abstract] Short answer
> `Runtime` is the per-application singleton (`Runtime.getRuntime()`) that interfaces with the JVM itself: launching processes (`exec`), shutdown control (`exit`, `halt`, `addShutdownHook`), memory probes (`maxMemory`, `freeMemory`, `totalMemory`), `availableProcessors`, `gc`, and native library loading. `System` is an all-static utility for system-wide services: standard streams (`in`, `out`, `err`), `getenv`, system properties, clocks (`currentTimeMillis`, `nanoTime`), `arraycopy`, and convenience delegates such as `System.exit(n)` → `Runtime.getRuntime().exit(n)`.

An application cannot create its own `Runtime` instance — the class exposes exactly one object through `getRuntime()`, and its constructor is private. `System` cannot be instantiated either: everything is static. The two classes overlap deliberately: `System.exit`, `System.gc`, and (before deprecation) `System.runFinalization` are thin wrappers that call the same method on the `Runtime` singleton, so there is one underlying JVM service, not two.

## What each side really owns

`Runtime` owns the JVM lifecycle and resources: the shutdown sequence (hooks, `exit`, `halt`), subprocess creation, memory bookkeeping, and `loadLibrary`. `System` owns process-wide facilities the code touches constantly: standard I/O, the environment and properties, monotonic timing via `nanoTime` (measured from an arbitrary origin, usable only for differences within one JVM instance), and low-level primitives like `arraycopy` and `identityHashCode`.

```d2
direction: right
app: "Your application" {
  width: 220
  height: 70
  style.fill: "#e3f2fd"
}
runtime: "Runtime.getRuntime()\none instance per JVM\nexec · exit · halt\naddShutdownHook\ngc · maxMemory" {
  width: 250
  height: 130
  style.fill: "#e8f5e9"
}
system: "System (static)\nin · out · err\ngetenv · properties\nnanoTime · arraycopy" {
  width: 250
  height: 130
  style.fill: "#fff3e0"
}
app -> runtime
app -> system
system -> runtime: "exit(n) and gc()\ndelegate to the singleton"
```

**Fig. 1.** `System` is a static facade in front of JVM services; `Runtime` is the singleton behind them.

```java
public class RuntimeSystemDemo {
    public static void main(String[] args) {
        Runtime rt = Runtime.getRuntime();
        System.out.println("processors = " + rt.availableProcessors());
        System.out.println("maxMemory > 0 = " + (rt.maxMemory() > 0));
        long start = System.nanoTime();
        long sum = 0;
        for (int i = 0; i < 1_000_000; i++) {
            sum += i;
        }
        System.out.println("measured nanos > 0 = " + (System.nanoTime() - start > 0));
        System.out.println("sum = " + sum);
        System.out.println("same singleton = " + (Runtime.getRuntime() == rt));
    }
}
// Output (JDK 21):
// processors = 2
// maxMemory > 0 = true
// measured nanos > 0 = true
// sum = 499999500000
// same singleton = true
```

**Listing 1.** `Runtime` answers JVM-level questions; `System.nanoTime` measures elapsed time inside the same instance; `getRuntime()` returns the same object every time.

> [!warning] The lazy-brain trap
> "System class = system operations, Runtime class = running programs" is a false split: `System.exit` **is** `Runtime.exit` and `System.gc` **is** `Runtime.gc`. Also `System.gc()` is only a suggestion — no guarantee that any object is collected by the time it returns, and `System.nanoTime` is useless as a wall clock because its origin is arbitrary per JVM instance.

Shutdown behavior on both sides is covered by [[How would you explain System.exit()]] and [[What is the difference between System.exit and Runtime.halt]]; the environment half of `System` meets its subprocess counterpart in [[How do you pass environment variables to a subprocess in Java]].

> [!tip] Interview answer
> `Runtime` is a single instance per application that talks to the JVM: process launching, shutdown hooks, exit and halt, memory and processor info, `gc`. `System` is a static utility layer for the process: standard streams, environment, properties, timing, `arraycopy`. Several `System` methods just delegate to `Runtime`, so for exit and GC they are literally the same call.

