<!--
reps: 0
priority: 0
-->
#Java/JMM #Java/Language/Object/Finalize #SRS

# What is the finalizer happens-before rule in Java

> [!abstract] Short answer
> **There is a happens-before edge from the end of an object's constructor to the start of its finalizer (JLS 17.4.5).** By the time finalization runs, the object's fields are guaranteed to hold the values the constructor left — the finalizer observes a fully constructed object.

The rule exists because finalization is inherently cross-thread: the finalizer is invoked by the garbage collector machinery, typically on a different thread than the one that constructed the object, long after the constructor returned. Without the edge, finalizer logic would race with construction and could see default values mid-construction ([[What is the default value happens-before rule in the Java Memory Model]]). The same concern drives the related rule that the `finalize` method may be called at most once and is not invoked before the constructor completes. Worth remembering the timeline: finalization was deprecated in Java 9 and removed from the language in later JDKs in favor of `Cleaner` and `PhantomReference`, but the memory-model edge describes the era when `finalize` was a language feature and explains why successor APIs document equivalent construction-visibility guarantees ([[How would you explain the finalize method in Java and why it is discouraged]]).

```d2
direction: right
c: "Thread A" {
  ctor: "new Resource()\nconstructor writes fields" { style.fill: "#e3f2fd" }
  end: "constructor completes" { style.fill: "#fff3e0" }
  ctor -> end: "program order"
}
g: "GC / finalizer thread" {
  fin: "finalize() starts\n(acquire)" { style.fill: "#fff3e0" }
  r: "sees all constructor writes" { style.fill: "#e8f5e9" }
  fin -> r: "program order"
}
end -> fin: "happens-before\n(constructor end -> finalizer start)"
```

**Fig. 1.** The constructor-completion edge hands the object over to the finalizer thread with all its field writes visible.

```java
class Resource {
    final int handle;

    Resource() {
        handle = openDevice();   // write inside the constructor
    }

    @Override
    protected void finalize() {
        // guaranteed: handle == the value set by the constructor
        closeDevice(handle);
    }
}
```

**Listing 1.** The finalizer can safely read `handle`: construction is ordered before finalization, so no re-initialization or null/garbage observation is possible.

> [!warning] The edge orders construction before finalization — nothing else
> The rule says nothing about resource lifetime: a finalizer may run arbitrarily late, on any thread, or never within any useful deadline — which is exactly why it was removed ([[What happens to finalization if finalize runs slowly or throws an exception]]). It also does not make mutable state safe for other racing readers; only the finalizer receives the edge. Modern code uses `Cleaner`/`PhantomReference` with explicitly documented memory guarantees instead of relying on this path.

> [!tip] Interview answer
> **JLS 17.4.5 adds a happens-before edge from the end of an object's constructor to the start of its finalizer, so the finalizer always sees a fully constructed object even though it runs on GC-owned threads. The rule addresses visibility only — timing and liveness of finalization are still unspecified, which is why finalization was deprecated and replaced by Cleaner.**
