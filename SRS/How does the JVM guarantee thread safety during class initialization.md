<!--
reps: 0
priority: 0
-->
#Java/OOP/Initialization #Java/JVM/ClassLoaders #SRS

# How does the JVM guarantee thread safety during class initialization

> [!abstract] Short answer
> **Every class or interface has a unique initialization lock, and the JVM runs each `<clinit>` exactly once under that lock: the first thread to initialize a class synchronizes on the lock and marks initialization in progress; every other thread that arrives blocks until it is told initialization has completed.** Because the lock is held across the whole run of `<clinit>`, a class's static state is fully built before any other thread can observe it — which is what makes the lazy holder idiom thread-safe without any explicit synchronization ([[What triggers class initialization in Java]]).

## The per-class lock

The JVM specification gives each class or interface C a unique initialization lock LC; the mapping from C to LC is left to the discretion of the implementation — for example, LC could be the Class object for C, or the monitor associated with that Class object. That detail is why the guarantee is invisible in code: there is no synchronized block in your source, because the VM takes the lock for you before `<clinit>` can run ([[How would you explain the Java class loader]]).

## The procedure

The procedure for initializing C runs as follows. The thread synchronizes on LC, waiting until it can acquire it. If the Class object for C indicates that initialization is in progress by some other thread, the thread releases LC and blocks until informed that the in-progress initialization has completed, at which point it repeats the check. If initialization is in progress by the current thread, that is a recursive request: release LC and complete normally. If C is already initialized, no further action is required. If C is in an erroneous state, initialization is not possible: release LC and throw NoClassDefFoundError ([[What happens if you use a class after ExceptionInInitializerError]]). Otherwise the thread records that initialization is in progress by the current thread, releases LC, initializes superclasses first, and only then runs `<clinit>` ([[How would you explain static initialization order in Java]]). Two details worth remembering: thread interrupt status is unaffected by the whole procedure, and once a class passes the erroneous check, the state recorded on the Class object makes every later race a no-op.

```d2
direction: right
t1: "thread 1\nfirst active use" {
  width: 180
  height: 55
}
t2: "thread 2\nfirst active use" {
  width: 180
  height: 55
}
lc: "initialization lock LC\nunique per class" {
  width: 260
  height: 60
  style.fill: "#fff3e0"
}
clinit: "<clinit> runs once\nunder the lock" {
  width: 220
  height: 55
  style.fill: "#e8f5e9"
}
wait: "block until informed\ninitialization completed" {
  width: 240
  height: 60
  style.fill: "#ffebee"
}
t1 -> lc: "acquire"
t2 -> lc: "acquire"
lc -> clinit: "winner"
lc -> wait: "loser"
```

**Fig. 1.** Two threads racing to first use meet at LC; one runs `<clinit>`, the other blocks and then repeats the check instead of re-running it.

## Why the lazy holder works

Put the triggers and the lock together and the classic initialization-on-demand holder falls out. The inner Holder class is not initialized until something actively uses it — reading Holder.INSTANCE is a non-constant static read, the one trigger in the closed list. The first read acquires LC, runs the Holder `<clinit>`, and installs INSTANCE; concurrent first reads block on LC and then observe a completed initialization. No volatile, no synchronized in user code, and yet every thread sees a fully constructed instance — the same guarantee that makes class initialization a memory barrier ([[What does class initialization guarantee about static field visibility in Java]]).

```java
class Registry {
    private Registry() { }

    private static class Holder {
        static final Registry INSTANCE = new Registry();
        static { System.out.println("Holder initialized once"); }
    }

    static Registry getInstance() {
        return Holder.INSTANCE;   // first read triggers Holder's <clinit>
    }
}
```

**Listing 1.** The lazy holder: the JVM's LC lock plus the trigger rules give a thread-safe singleton with zero explicit synchronization; the block prints once no matter how many threads call getInstance first.

> [!warning] Failure is sticky for every waiter too
> The blocking threads repeat the procedure after being informed, and the repeat hits the same checks: a class whose `<clinit>` threw is marked erroneous, and the waiter's next attempt fails with NoClassDefFoundError rather than re-running the initializer. The lock serializes success and failure alike — only the first thread gets to run the code ([[What happens if you use a class after ExceptionInInitializerError]]).

> [!tip] Interview answer
> **Class initialization is thread-safe by construction: each class has a unique initialization lock, the first thread takes it and runs `<clinit>` once, and every other first-use thread blocks until initialization completes.** Recursive initialization by the same thread completes normally, already-initialized and erroneous states short-circuit (erroneous means NoClassDefFoundError forever), superclasses initialize first, and interrupt status is untouched. That machinery is exactly why the lazy holder idiom needs no volatile or synchronized.
