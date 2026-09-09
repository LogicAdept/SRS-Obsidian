<!--
reps: 0
priority: 0
-->
#Java/Runtime #SRS

# In what order do shutdown hooks run

> [!abstract] Short answer
> No order is guaranteed. The specification says hooks are "started in some unspecified order" and are "allowed to run concurrently until they finish". Registration order means nothing, and because hooks run in parallel, one hook may finish long after another started. If you need an ordering, you must build it yourself with latches or sequencing inside the hooks.

The JVM starts every registered hook at the beginning of the shutdown sequence and then simply waits until all of them have terminated. With no ordering and no join between hooks, the same program prints different interleavings across runs — this is observable behavior, not an implementation accident.

## Observed on a real JVM

Registering hooks A, B, C in that order and letting each print "started"/"ended" produces different orders on consecutive runs of the same binary: C–A–B then A–C–B. Each hook sleeps 50 ms, so overlapping start/finish lines are visible — hooks genuinely run in parallel.

```java
public class ShutdownOrderDemo {
    public static void main(String[] args) {
        Runtime rt = Runtime.getRuntime();
        rt.addShutdownHook(new Thread(() -> log("A"), "hook-A"));
        rt.addShutdownHook(new Thread(() -> log("B"), "hook-B"));
        rt.addShutdownHook(new Thread(() -> log("C"), "hook-C"));
        System.out.println("main done");
    }

    private static void log(String name) {
        System.out.println("hook " + name + " started");
        try {
            Thread.sleep(50);
        } catch (InterruptedException ignored) {
        }
        System.out.println("hook " + name + " ended");
    }
}
// Output (JDK 21), run 1:
// main done
// hook C started
// hook A started
// hook B started
// hook C ended
// hook A ended
// hook B ended
// Output, run 3 of the same binary:
// main done
// hook A started
// hook C started
// hook B started
// hook A ended
// hook C ended
// hook B ended
```

**Listing 1.** Registered A, B, C — observed start orders C, A, B and A, C, B on different runs; the JVM gives no contract on which one you get.

> [!warning] Two popular lies
> "Hooks run in registration order" — false, the order is unspecified and varies between runs. "Hooks run one after another" — false, they are started together; one hook cannot assume another's cleanup already finished, which is why a shutdown that mixes a log-flush hook and a pool-close hook needs explicit coordination, not hope.

Because hooks are threads, you can impose an order with a `CountDownLatch` or by having one hook do everything sequentially; the alternative — encoding order in registration — works by luck only. The base mechanism is in [[What is a JVM shutdown hook]], and cases where hooks never start at all are in [[When does a JVM shutdown hook not run]].

> [!tip] Interview answer
> The JVM starts all shutdown hooks in an unspecified order and lets them run concurrently — registration order is not a contract, and I have seen different orders on consecutive runs of the same program. Treat hooks as independent parallel tasks; when cleanup has ordering requirements, coordinate explicitly with latches inside the hooks.

