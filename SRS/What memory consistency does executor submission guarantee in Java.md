<!--
reps: 0
priority: 0
-->
#Java/JMM #Java/Concurrency/Executors #SRS

# What memory consistency does executor submission guarantee in Java

> [!abstract] Short answer
> **Actions in a thread prior to submitting a `Runnable` to an `Executor` happen-before the execution of that task begins; likewise for `Callable`s submitted to an `ExecutorService`.** A task always sees the state the submitter created before the submit call.

Submission is publication: the executor moves the task object through internal concurrent machinery — a work queue whose enqueue/dequeue and worker hand-off are built from locks and volatile/VarHandle state — which delivers the synchronizes-with edge from the submit call to the first action of the task in whatever worker thread picks it up ([[What memory consistency do concurrent collections guarantee in Java]]). This is why the standard pattern of building an immutable input, capturing it in a lambda, and submitting it to a pool needs no additional synchronization, and why thread pools can hand tasks to *different* threads each time without breaking visibility. It applies equally to platform-thread pools, `ForkJoinPool`, and virtual-thread-per-task executors ([[How would you explain the ExecutorService interface in Java]]).

```d2
direction: right
s: "Submitting thread" {
  b: "create input, capture in task" { style.fill: "#e3f2fd" }
  sub: "executor.submit(task)\n(release via work queue)" { style.fill: "#fff3e0" }
  b -> sub: "program order"
}
wk: "Worker thread" {
  st: "task starts executing\n(acquire)" { style.fill: "#fff3e0" }
  r: "reads input\n-> fully visible" { style.fill: "#e8f5e9" }
  st -> r: "program order"
}
sub -> st: "happens-before\n(submission -> execution begins)"
```

**Fig. 1.** The executor's work queue supplies the edge between submission and the start of execution, whichever thread runs the task.

```java
ExecutorService pool = Executors.newFixedThreadPool(4);

Snapshot input = loadSnapshot();      // plain writes in the submitting thread

Future<Integer> f = pool.submit(() -> {
    // guaranteed to see fully initialized input:
    return input.rows().size() * 2;
});
```

**Listing 1.** The lambda reads `input` with no locks or volatile — the submission edge makes the pre-submit construction visible at task start.

> [!warning] The edge ends where execution begins
> The guarantee is one-way: writes the task performs after starting are not ordered against the submitter's later reads — to receive results you need the paired property, `Future.get` ([[What memory consistency does Future get guarantee in Java]]). Also, mutating a shared captured object *after* submission races with the task, because only pre-submit writes are published; and scheduling methods follow the same property for the moment execution begins, not when the trigger fires ([[How would you explain the Callable interface in Java]]).

> [!tip] Interview answer
> **Submission of a Runnable or Callable to an executor happens-before the start of its execution: the internal work queue is built from synchronized/volatile state, so every worker thread that picks the task sees the state the submitter built before submitting. The edge is from submission to execution start — results flow back only through Future.get or another synchronizer.**
