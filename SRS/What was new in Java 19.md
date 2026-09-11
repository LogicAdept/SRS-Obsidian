<!--
reps: 0
priority: 0
-->
#Java/Versions/19 #SRS

# What was new in Java 19

> [!abstract] Short answer
> **Java 19 (September 2022) is the Project Loom preview train: virtual threads preview (JEP 425), structured concurrency incubator (428), scoped values not yet here; plus record patterns preview (405), pattern matching for switch third preview (427), the Foreign Function & Memory API first preview (424), and the Linux/RISC-V port (422). Nothing in 19 was final except the RISC-V port.**

## The preview pipeline fills up

Virtual threads previewed here as `Thread.ofVirtual()` and `Executors.newVirtualThreadPerTaskExecutor()`, with the semantics — cheap blocking, mount/unmount on carriers — already recognizable, and finalized in 21 (JEP 444) ([[How would you explain Virtual Threads]]). Record patterns previewed the deconstruction syntax that finalized in 21 alongside pattern switch. The FFM API previewed the modern JNI replacement (Linker, Arena, MemorySegment) that finalized in 22 (454). The release shows how the six-month model works: 19 is a pipeline stage where almost everything is a flag away from being invisible.

```java
public class V33_VirtualThread19 {
    public static void main(String[] args) throws Exception {
        Thread vt = Thread.ofVirtual().name("vt").start(() -> {   // preview 19 (JEP 425), final 21 (JEP 444)
            System.out.println("virtual=" + Thread.currentThread().isVirtual()
                    + " name=" + Thread.currentThread().getName());
        });
        vt.join();
        System.out.println("threadClass=" + vt.getClass().getName());
    }
}
```

**Listing 1.** Verified on JDK 21 (V33_VirtualThread19 in empirics): `virtual=true name=vt`, `threadClass=java.lang.VirtualThread` (out/V33_VirtualThread19.txt) — the API was preview in 19, final in 21.

```d2
direction: right
loom: "virtual threads PREVIEW (425)\nstructured concurrency INCUBATOR (428)" { style.fill: "#fff3e0"; width: 340; height: 90 }
lang: "record patterns PREVIEW (405)\nswitch 3rd preview (427)" { style.fill: "#fff3e0"; width: 280; height: 90 }
ffi: "FFM API PREVIEW (424)\nRISC-V port (422)" { style.fill: "#e3f2fd"; width: 250; height: 90 }
loom -> lang -> ffi: ""
```

**Fig. 1.** Java 19: the Loom and pattern pipelines all in preview/incubator state, one port final.

> [!warning] Do not claim virtual threads "shipped" in 19
> In 19 they needed `--enable-preview` and could have changed. Statements like "virtual threads since Java 19" misstate supportability: production use starts at 21 (LTS, final semantics). The same caution applies to record patterns and FFM in 19 ([[What are the typical problems when upgrading from Java 8 to 17]] has the support-model version of this trap).

> [!tip] Interview answer
> **Java 19 is the preview train: virtual threads, record patterns, and the FFM API all previewed, structured concurrency incubated — nothing user-visible was final except a RISC-V port. The version fact to hold: virtual threads previewed in 19 and finalized in 21, the LTS where thread-per-request scalability became production reality.**
