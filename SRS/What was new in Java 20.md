<!--
reps: 0
priority: 0
-->
#Java/Versions/20 #SRS

# What was new in Java 20

> [!abstract] Short answer
> **Java 20 (March 2023) is the only release where every JEP is a preview or incubator: scoped values incubator (JEP 429), record patterns second preview (432), pattern switch fourth preview (433), FFM second preview (434), virtual threads second preview (436), structured concurrency second incubator (437), Vector API fifth incubator (438). Runtime note: `Thread.stop` became unconditionally inert here.**

## The holding pattern, and why it exists

All seven JEPs continued work started in 19 or 21-pipeline efforts — the model needs releases even when nothing finalizes, because preview APIs must ship, be tested by real users, and iterate before graduation. Scoped values (429) previewed the ThreadLocal replacement that finalized in 25 (506) ([[What are scoped values]]). Thread-level cleanup: JEP 425 groundwork made `Thread.stop` throw `UnsupportedOperationException` unconditionally (on virtual threads it was already inert from 19); `suspend`/`resume` had been dead since 14.

```java
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;

public class V34_ThreadStop20 {
    public static void main(String[] args) throws Exception {
        Thread t = new Thread(() -> {});
        t.start();
        t.join();
        for (String name : new String[]{"stop", "suspend"}) {
            Method m = Thread.class.getMethod(name);
            try {
                m.invoke(t);
                System.out.println(name + "() returned normally");
            } catch (InvocationTargetException e) {
                System.out.println(name + "() -> " + e.getCause().getClass().getSimpleName());
            }
        }
    }
}
```

**Listing 1.** Verified on JDK 21 (V34_ThreadStop20 in empirics): `stop() -> UnsupportedOperationException`, `suspend() -> UnsupportedOperationException` (out/V34_ThreadStop20.txt) — the methods exist but are permanently inert.

```d2
direction: right
a: "scoped values INCUBATOR (429)" { style.fill: "#fff3e0"; width: 250; height: 70 }
b: "record patterns 2nd (432)\nswitch 4th (433)\nFFM 2nd (434)" { style.fill: "#fff3e0"; width: 230; height: 110 }
c: "virtual threads 2nd (436)\nstructured concurrency 2nd (437)\nVector 5th (438)" { style.fill: "#fff3e0"; width: 300; height: 110 }
a -> b -> c: ""
```

**Fig. 1.** Java 20: every JEP orange (preview/incubator) — a pipeline-maintenance release between two feature trains.

> [!warning] Running previews in 20 means running experiments
> There is no final feature to justify choosing 20 in production: virtual threads were still `--enable-preview`, structured concurrency still incubating (module `jdk.incubator.concurrent`). "We run Java 20 for virtual threads" means unflagged-experiment semantics, not stability ([[What is a preview feature in Java]]).

> [!tip] Interview answer
> **Java 20 is the all-preview release: seven JEPs, all previews or incubators — scoped values, record patterns, pattern switch, FFM, virtual threads, structured concurrency, Vector API. The durable fact: `Thread.stop` became unconditionally inert here, and the APIs involved finalized across 21 through 25.**
