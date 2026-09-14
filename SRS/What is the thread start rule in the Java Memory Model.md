<!--
reps: 0
priority: 0
-->
#Java/JMM #Java/Concurrency/Threads #SRS

# What is the thread start rule in the Java Memory Model

> [!abstract] Short answer
> **An action that starts a thread synchronizes-with the first action in the thread it starts (JLS 17.4.4) — a call to `Thread.start()` happens-before any action in the started thread.** Everything the parent thread wrote before calling `start()` is visible inside `run()` without any extra synchronization.

The edge makes `start()` a safe-publication point for the initial work item: configuration objects, immutable inputs, and collections populated before the start are all guaranteed visible to the new thread ([[How do you create a thread in Java]]). Together with the termination rule it closes the loop for a thread's whole lifetime — parent publishes to child at start, child publishes back to the parent (or any joiner) at termination ([[What is the thread termination rule in the Java Memory Model]]). The JDK source guards `start()` with a `synchronized (this)` block that checks `threadStatus` and throws `IllegalThreadStateException` on a second call, so a thread is started exactly once and the memory edge is delivered exactly once.

```d2
direction: right
p: "Parent thread" {
  w: "build config\n(plain writes)" { style.fill: "#e3f2fd" }
  s: "thread.start()\n(release)" { style.fill: "#fff3e0" }
  w -> s: "program order"
}
c: "Child thread" {
  f: "first action in run()\n(acquire)" { style.fill: "#fff3e0" }
  r: "reads config\n-> fully visible" { style.fill: "#e8f5e9" }
  f -> r: "program order"
}
s -> f: "synchronizes-with"
```

**Fig. 1.** The start edge: plain pre-start writes ride into the child thread through the single synchronizes-with edge from `start()` to the first action of `run()`.

```java
Map<String, Integer> config = new HashMap<>();
config.put("retries", 3);          // plain writes before start

Thread worker = new Thread(() -> {
    // guaranteed to see the populated map:
    int retries = config.get("retries");
    // ... but NOT guaranteed to see anything
    // the parent writes AFTER start() returns
});
worker.start();
config.put("timeout", 100);        // races with the child
```

**Listing 1.** `retries` is safely published through the start edge; the `timeout` entry written after `start()` is a data race and must be published some other way, for example via a concurrent queue or a `join()`.

> [!warning] Calling run() is not starting a thread
> Calling `run()` directly executes in the current thread — no new thread, no edge semantics beyond program order, and a second `start()` throws `IllegalThreadStateException` ([[What is the difference between Thread start and run]]). Two more traps. One: writes made by the parent *after* `start()` are outside the edge — the rule is one-way and one-shot. Two: for pools the same publication property is stated at the executor level: submission happens-before execution begins ([[What memory consistency does executor submission guarantee in Java]]).

> [!tip] Interview answer
> **`Thread.start()` happens-before every action in the started thread: the call to start is a release and the first action of `run()` is an acquire. So the child sees everything the parent wrote before starting it — that is the standard way initial state reaches a thread. The edge is one-shot: it covers pre-start writes only, and re-starting or calling run() directly gives neither a thread nor the guarantee.**
