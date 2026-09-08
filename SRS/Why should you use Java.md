<!--
reps: 0
priority: 0
-->
#Java/JVM #Java/Language #SRS

# Why should you use Java?

> [!abstract] Short answer
> Java buys you a managed, portable run time with a 30-year-compatible ecosystem: bytecode runs on any JVM for the target platform, the GC frees you from manual memory management, JIT gives near-native steady-state performance, static typing catches whole error classes at compile time, and LTS releases plus the largest enterprise library ecosystem make long-lived systems maintainable.

## The reasons that hold up technically

**Portability.** One compiled artifact runs on every platform that has a JVM — recompilation is per-platform only for native code; see [[Why is Java described as platform independent]]. **Managed memory.** Allocation is a pointer bump and reclamation is the garbage collector's job; whole bug classes (use-after-free, double free) do not exist in safe Java code. **Steady-state performance.** The JIT compiles hot paths to native code while the program runs; long-running services spend most of their life compiled, not interpreted — see [[What is the execution engine of the JVM]]. **Static typing at scale.** Compile-time types, interfaces, and (since 21) records make refactoring tools reliable on million-line codebases. **Ecosystem and continuity.** Build tools, drivers, frameworks, and monitoring agents for Java are mature, and the platform's backward-compatibility discipline means old bytecode still runs on new JVMs.

```d2
direction: right
code: "your code" {
  width: 160
  height: 60
  style.fill: "#e3f2fd"
}
pillars: "what the platform gives" {
  width: 260
  height: 60
  style.fill: "#fff3e0"
}
port: "portability\none class file, many OS" {
  width: 280
  height: 90
  style.fill: "#fff3e0"
}
mem: "managed memory\nGC, no manual free" {
  width: 260
  height: 90
  style.fill: "#fff3e0"
}
perf: "performance\nJIT native code" {
  width: 240
  height: 90
  style.fill: "#fff3e0"
}
eco: "ecosystem\nLTS · libraries · tooling" {
  width: 280
  height: 90
  style.fill: "#fff3e0"
}
code -> pillars
pillars -> port
pillars -> mem
pillars -> perf
pillars -> eco
```

**Fig. 1.** The four pillars interviewers expect: portability, managed memory, JIT performance, ecosystem continuity.

```java
import java.util.concurrent.Executors;

public class ModernJava {
    record Money(long cents) {                     // concise, typed value model
        Money add(Money other) {
            return new Money(Math.addExact(cents, other.cents));
        }
    }

    public static void main(String[] args) {
        var pool = Executors.newFixedThreadPool(4); // concurrency in the standard library
        pool.submit(() -> System.out.println("on a worker thread"));
        pool.shutdown();
        System.out.println(new Money(2).add(new Money(3)).cents());
    }
}
```

**Listing 1.** Modern Java is compact: records for values, lambdas for behavior, executors for threads — no framework required.

> [!warning] "Java suits everything" is the wrong takeaway
> The same properties have costs. GC-managed memory means you do not control reclamation timing — latency-critical, allocation-light code needs GC tuning or native alternatives; see [[How does garbage collection work on the JVM]]. Startup and memory footprint are worse than native or scripting alternatives for short-lived scripts. And write-once-run-anywhere stops at native dependencies: JNI libraries and OS paths stay platform-specific. Choosing Java is choosing managed long-lived services — not a universal default.

For what "Java" even names, see [[What is Java]]; for the machine under the promises, [[What is the JVM]].

> [!tip] Interview answer
> I choose Java when a system is long-lived and needs portability, safe memory management, and steady throughput: one bytecode runs anywhere a JVM exists, the GC removes manual memory bugs, the JIT compiles hot code to native speed, and the static type system plus a huge backward-compatible ecosystem keep big codebases maintainable. The trade-offs are GC timing you do not control, higher startup cost, and native dependencies that break portability.
