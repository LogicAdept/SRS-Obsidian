<!--
reps: 0
priority: 0
-->
#Java/JMM/HappensBefore #SRS

# What is the default value happens-before rule in the Java Memory Model

> [!abstract] Short answer
> **The write of the default value — zero, false, or null — to each variable synchronizes-with the first action in every thread (JLS 17.4.4).** Conceptually every object exists at the start of the program with default-initialized fields, so a read never observes garbage memory: it sees either the default value or some write ordered after it.

This rule is the floor of the whole visibility system. It is why a freshly created object has predictable `0`/`false`/`null` fields even when its constructor has not been reached by some racing thread, and why the model can say that "the default initialization of any object happens-before any other actions (other than default-writes) of the program" (JLS 17.4.5). Without it, a data race could theoretically expose machine-level garbage left in freshly allocated memory; with it, the worst a racing read can see is the benign default ([[What is memory visibility in the Java Memory Model]]). It also makes the classic racy check `if (obj != null)` well-defined: the answer is either null or a published non-null reference, never a fabricated pointer.

```d2
direction: right
dv: "Conceptual default writes\nat program start\n(0, false, null)" {
  width: 285
  height: 134
  style.fill: "#fff3e0"
}
t1: "Thread 1\nfirst action" {
  width: 200
  height: 104
  style.fill: "#e3f2fd"
}
t2: "Thread 2\nfirst action" {
  width: 200
  height: 104
  style.fill: "#e3f2fd"
}
t3: "Thread 3\nfirst action" {
  width: 200
  height: 104
  style.fill: "#e3f2fd"
}
dv -> t1: "synchronizes-with"
dv -> t2: "synchronizes-with"
dv -> t3: "synchronizes-with"
```

**Fig. 1.** One release side (the conceptual default write) fans out to the first action of every thread, anchoring the base value every later read starts from.

```java
class Job {
    int attempts;      // every thread starts from 0
    String owner;      // every thread starts from null
}

// even in a racy publication scenario:
static Job job;        // races are still possible (see warning)

void reader() {
    if (job != null) {
        int a = job.attempts;      // well-defined: 0 or a written value
        String o = job.owner;      // well-defined: null or a written value
    }
}
```

**Listing 1.** Fields never hold garbage: a racing read sees the default or a properly ordered write. Seeing the default *after* a write happened in real time is still allowed without synchronization.

> [!warning] Defaults are well-defined, publication still is not
> The rule guarantees only the value floor, not visibility of real writes: without an edge, a read may keep returning the default long after a non-default write "happened" — that is exactly a data race ([[What is the difference between a race condition and a data race]]). Stronger tools replace this floor where needed: volatile and final fields give publication guarantees beyond defaults ([[Why do final fields guarantee visibility for properly constructed objects]]), and the rule applies to variables, while array element defaults follow the same principle per element.

> [!tip] Interview answer
> **The JMM makes the write of each variable's default value synchronize-with the first action in every thread, so every read starts from a defined base: zero, false, or null — never garbage. That is the reason Java has no uninitialized-memory reads like C. It does not publish real writes though — only edges like volatile, monitors, or final-field semantics do that.**
