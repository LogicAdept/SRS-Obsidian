<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Synchronizers #SRS

# How can you emulate CountDownLatch with Phaser?

> [!abstract] Short answer
> Use a Phaser as a one-shot gate with a **variable** party count: `new Phaser(1)` so the coordinator is already registered, `register()` each worker, have workers block in `arriveAndAwaitAdvance()`, then open the gate with the coordinator's `arriveAndDeregister()`. For a completion latch, invert the roles — workers `arriveAndDeregister()` when they finish; the coordinator `arriveAndAwaitAdvance()`. That replaces `countDown` / `await` when the number of parties is not fixed in advance. It is not a drop-in: `CountDownLatch` is one-shot and interruptible; a Phaser advances a phase number and can be reused until it terminates.

## Starting gate (CountDownLatch of one)

A `CountDownLatch(1)` is an on/off gate: waiters call `await()`, one opener calls `countDown()`. The Phaser sample for that job registers the setup thread first, registers each action as it is started, then deregisters the setup thread so the waiting parties can advance phase 0. Workers stay registered; they arrived with `arriveAndAwaitAdvance()`, they did not leave. After the gate opens they just run. [[How do you use CountDownLatch so several threads start together]] is the latch form of the same race.

```java
import java.util.List;
import java.util.concurrent.Phaser;

public final class PhaserStartGate {
    public void runTasks(List<Runnable> tasks) {
        Phaser startingGate = new Phaser(1); // register the coordinator
        for (Runnable task : tasks) {
            startingGate.register();
            new Thread(() -> {
                startingGate.arriveAndAwaitAdvance();
                task.run();
            }).start();
        }
        startingGate.arriveAndDeregister(); // last arrival for phase 0
    }
}
```

**Listing 1.** Coordinator holds one party so workers can register without the phase advancing early. `arriveAndDeregister()` on that extra party opens the gate. `Phaser` exists since Java 7; `CountDownLatch` since 1.5.

```d2
direction: down
init: "new Phaser(1)\ncoordinator registered" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
reg: "register() each worker\narriveAndAwaitAdvance()" {
  width: 320
  height: 70
  style.fill: "#fff3e0"
}
open: "coordinator\narriveAndDeregister()" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
run: "phase 0 advances\nworkers run their tasks" {
  width: 300
  height: 70
  style.fill: "#fce4ec"
}
init -> reg
reg -> open
open -> run
```

**Fig. 1.** Why the constructor argument is **1**, not `tasks.size()`: the party count is allowed to grow with `register()` while the coordinator still holds the phase closed.

If the worker count is known and fixed, `new Phaser(n)` plus `n` arrivals is the count-for-count analogue of `new CountDownLatch(n)`. Parties are **anonymous counts**, not thread identities, so any thread may `arrive()` on behalf of a slot — the same split as latch waiters versus threads that only `countDown()`. Prefer the `Phaser(1)` plus `register()` idiom when the set of tasks is built dynamically.

## Completion wait (CountDownLatch of N)

A latch initialized to N makes one thread wait until N actions `countDown()`. Keep the extra coordinator party, register each worker, have workers arrive **and leave** when they finish, then have the coordinator arrive-and-wait:

```java
import java.util.List;
import java.util.concurrent.Phaser;

public final class PhaserCompletion {
    public void awaitTasks(List<Runnable> tasks) {
        Phaser done = new Phaser(1);
        for (Runnable task : tasks) {
            done.register();
            new Thread(() -> {
                try {
                    task.run();
                } finally {
                    done.arriveAndDeregister();
                }
            }).start();
        }
        done.arriveAndAwaitAdvance();
    }
}
```

**Listing 2.** Dual of Listing 1. If every worker has already deregistered, the coordinator is the only remaining party and `arriveAndAwaitAdvance()` returns at once — the same “count already zero” property as `CountDownLatch.await()`.

A thread that must both consume a party and wait uses the documented split `awaitAdvance(arriveAndDeregister())` (arrive without blocking, then wait for that phase to pass). `arriveAndAwaitAdvance()` is `awaitAdvance(arrive())` and **keeps** the party registered for later phases. Method roles: [[What Phaser methods register arrive and awaitAdvance do]].

## What does not carry over

| Latch | Phaser stand-in | Do not assume |
| --- | --- | --- |
| `countDown()` | `arrive()` or `arriveAndDeregister()` | Extra `arrive()` when unarrived would go negative is a usage error (`IllegalStateException` may show up only on a later call) |
| `await()` | `arriveAndAwaitAdvance()` / `awaitAdvance(phase)` | `awaitAdvance` **ignores** interrupts; `CountDownLatch.await` throws `InterruptedException` |
| `getCount()` | `getUnarrivedParties()` (monitoring) | Monitoring values are transient; they are not a wait API |
| spent after zero | still at phase 1 unless `onAdvance` terminates | default `onAdvance` **does** terminate when `arriveAndDeregister` drops parties to zero |
| unbounded waiters | max **65535** parties per phaser | tier child phasers if you need more |

Phase numbers start at 0 and wrap after `Integer.MAX_VALUE`. `awaitAdvance(phase)` returns immediately if the current phase is **already not** that value, or if the phaser is terminated. Pass the int returned by `arrive` / `arriveAndDeregister()`, not a hardcoded `0`, unless you are still sure you are in phase 0. A Phaser can replace a latch for one generation and then be awaited again; [[How does Phaser differ from CyclicBarrier]] is that reuse. [[What is CountDownLatch]] stays spent after the count hits zero. Actions before `arrive*` happen-before the phase advance, which happens-before work after the wait; the latch analogue is `countDown` happen-before a successful `await`.

> [!warning] Do not spin on `getRegisteredParties()`
> `getRegisteredParties()`, `getArrivedParties()`, and `getUnarrivedParties()` are snapshots for monitoring. They are not synchronization. A `while (getRegisteredParties() > k) Thread.sleep(...)` loop is not a Phaser wait — use `awaitAdvance` / `arriveAndAwaitAdvance`. Sleep-polling also misses termination and phase wrap.

> [!warning] `awaitAdvance` is not `CountDownLatch.await`
> Plain `awaitAdvance` keeps waiting after an interrupt. Use `awaitAdvanceInterruptibly` (or the timeout overload) when cancellation matters. After a timeout or interrupt the phaser state is unchanged; recover with `forceTermination` if waiters must be released.

> [!tip] Interview answer
> Build `new Phaser(1)`, register each worker, have workers `arriveAndAwaitAdvance()`, then `arriveAndDeregister()` on the extra party to open the gate — that is the documented CountDownLatch substitute when the party count varies. For “wait until N tasks finish”, workers `arriveAndDeregister()` and the coordinator `arriveAndAwaitAdvance()`. Do not treat it as the same class: the latch is one-shot and interruptible; a Phaser uses phases, can be reused until `onAdvance` terminates, and `awaitAdvance` ignores interrupts unless you pick the interruptible form.
