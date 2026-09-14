<!--
reps: 0
priority: 0
-->
#Java/JMM/HappensBefore #SRS

# What is the transitivity of happens-before in the Java Memory Model

> [!abstract] Short answer
> **Happens-before is closed under transitivity: if action A happens-before action B and B happens-before C, then A happens-before C (JLS 17.4.5: "If hb(x, y) and hb(y, z), then hb(x, z)").** The relation is defined as the transitive closure of program order plus the synchronizes-with edges, so guarantees compose across any chain of synchronization actions, however long.

The individual edges are tiny contracts: program order inside one thread ([[What is the program order rule in the Java Memory Model]]), volatile write-to-read ([[What is the volatile visibility rule in the Java Memory Model]]), monitor unlock-to-lock, `start()`, termination detection, interrupt. Transitivity is what turns them into a real memory model: each edge can be glued to the next, so a visibility guarantee made by one thread can travel through any number of intermediate threads and synchronization points. This composition is why "correctly synchronized" programs behave sequentially consistent ([[What does the Java Memory Model guarantee for data race free programs]]) — a data read is race-free exactly when a happens-before chain connects its write to its read.

The classic pattern built on transitivity is **piggybacking**: publish cheap plain writes alongside one synchronized or volatile write, and the reader gets all of them from the single edge. A monitor-protected map mutation makes every field of the values it stores visible to a thread that later locks the same monitor; a volatile flag makes the data written before it visible after the read sees the flag. Nothing about the plain fields is special — the guarantee is borrowed from the edge they sit behind, transitively.

```d2
direction: right
a: "T1: data = 42\nplain write" {
  width: 240
  height: 84
  style.fill: "#e3f2fd"
}
b: "T1: ready = true\nvolatile write" {
  width: 250
  height: 84
  style.fill: "#fff3e0"
}
c: "T2: reads ready == true\nvolatile read" {
  width: 250
  height: 84
  style.fill: "#fff3e0"
}
d: "T2: reads data\nsees 42, derived edge" {
  width: 250
  height: 84
  style.fill: "#e8f5e9"
}
a -> b: "program order"
b -> c: "synchronizes-with"
c -> d: "program order"
b -> d: "hb by transitivity" {
  style.stroke: "#2e7d32"
  style.stroke_dash: 4
}
```

**Fig. 1.** Transitivity derives the missing edge: two program-order edges and one synchronizes-with edge compose into a happens-before guarantee from the plain write in T1 to the plain read in T2.

```java
class Piggyback {
    private int data;                  // plain, no volatile
    private volatile boolean ready;    // the only synchronization

    void producer() {
        data = 42;                     // hb(1, 2) by program order
        ready = true;                  // (2) volatile write
    }

    int consumer() {
        if (ready) {                   // (3) volatile read: hb(2, 3)
            return data;               // (4) hb(3, 4) by program order
        }                              // hb(1, 4) by transitivity: sees 42
        return -1;
    }
}
```

**Listing 1.** One volatile variable carries the whole publication: the plain write to `data` becomes visible because a happens-before chain links it to the read, even though `data` itself is never synchronized.

> [!warning] One missing link breaks the chain
> Transitivity only helps while the chain is unbroken. Two different volatile variables do not compose: a write to `a` and a read of `b` share no edge, so the plain writes next to them stay racy. The same holds for a chain that passes through an unsynchronized hand-off — the derived guarantee is only as strong as its weakest step. And transitivity says nothing about wall-clock time: happens-before is a visibility contract, not a timestamp; actions can be ordered without any real-world clock agreeing.

> [!tip] Spell out the chain in interviews
> When asked "is this write visible?", answer by naming every edge: which pair is program order, which action creates the synchronizes-with edge, and what the closure adds. A `start()` plus `join()` pair, for example, chains into "everything the worker thread did is visible to the thread that joined it" — two edges, transitively closed ([[What is the thread start rule in the Java Memory Model]], [[What is the thread termination rule in the Java Memory Model]]). The synchronizes-with relation itself catalogs the raw edges ([[What is the synchronizes-with relation in the Java Memory Model]]); transitivity is the glue that makes them reusable.
