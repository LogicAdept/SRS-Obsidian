<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Synchronizers #SRS

# What Phaser methods `register`, `arrive`, and `awaitAdvance` do?

> [!abstract] Short answer
> `register()` adds an **unarrived** party and returns the phase that registration applied to. `arrive()` records that this party finished the current phase and **does not wait**. `awaitAdvance(phase)` **waits** until the phaser leaves that phase (or returns at once if it already has, or is terminated). `arriveAndAwaitAdvance()` is `awaitAdvance(arrive())` — the `CyclicBarrier.await` analogue.

## Arrival and waiting are separate

Phase numbers start at 0 and advance when **all registered** parties have arrived. `arrive` / `arriveAndDeregister` never block; they return the arrival phase (negative if the phaser is already terminated). Waiting is a second call that takes that int. How this differs from a fixed `await()` barrier: [[How does Phaser differ from CyclicBarrier]]. Latch-style gates use the same split: [[How can you emulate CountDownLatch with Phaser]].

| Method | Effect |
| --- | --- |
| `register()` | One new **unarrived** party. May wait for an in-flight `onAdvance`. Returns the arrival phase for this registration; **negative** if terminated (registration ignored). `bulkRegister(n)` adds n. Max **65535** parties (`IllegalStateException`). |
| `getPhase()` | Current phase, or **negative** if terminated. Wraps after `Integer.MAX_VALUE`. |
| `arrive()` | This party arrived; **keep** membership; do not wait. Usage error if not registered (the `IllegalStateException` may show up only on a later call). |
| `arriveAndDeregister()` | Arrive **and leave**. Later phases need one fewer party. Not “this party finished every future phase of the phaser” — it only drops this membership. |
| `awaitAdvance(phase)` | If `getPhase()` still equals `phase` and the phaser is live, block until it advances. Else return immediately (`phase` if the argument was already negative; otherwise the new / terminated phase). **Ignores** interrupts. |
| `arriveAndAwaitAdvance()` | `awaitAdvance(arrive())`. Documented analogue of `CyclicBarrier.await`. |

`phase` is “normally the value returned by a previous `arrive` or `arriveAndDeregister`.” Passing a **stale** number (already not the current phase) is a no-op wait.

```java
import java.util.concurrent.Phaser;

public final class PhaserArriveWait {
    public void onePhase(Phaser phaser) {
        int p = phaser.register();
        doWork();
        int arrived = phaser.arrive();           // do not wait
        phaser.awaitAdvance(arrived);            // wait for the others
        // same as: phaser.arriveAndAwaitAdvance();
    }

    public void leaveAfterThisPhase(Phaser phaser) {
        phaser.awaitAdvance(phaser.arriveAndDeregister());
    }

    private static void doWork() {}
}
```

**Listing 1.** Register, then either `arrive` + `awaitAdvance` or the combined form. Deregister-and-wait is `awaitAdvance(arriveAndDeregister())`, not a second `register`.

```d2
direction: down
reg: "register()\nunarrived party++" {
  width: 260
  height: 70
  style.fill: "#e3f2fd"
}
arr: "arrive()\nphase recorded, no block" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
wait: "awaitAdvance(phase)\nblock only if still that phase" {
  width: 320
  height: 80
  style.fill: "#e8f5e9"
}
reg -> arr
arr -> wait
```

**Fig. 1.** `arriveAndAwaitAdvance()` is the last two boxes glued together. Interruptible / timed waits are `awaitAdvanceInterruptibly`. Monitoring (`getRegisteredParties`, …) is not a wait.

> [!warning] Stale `phase` does not wait
> `awaitAdvance(0)` after the phaser has already moved on returns immediately. Use the int from `arrive` / `register`, not a hardcoded `0`, unless you still know you are in phase 0.

> [!warning] `awaitAdvance` is not `CyclicBarrier.await` for interrupts
> Plain `awaitAdvance` keeps waiting after an interrupt. Use `awaitAdvanceInterruptibly` if cancellation matters. `arriveAndAwaitAdvance` follows the non-interruptible wait.

> [!tip] Interview answer
> `register` adds a party. `arrive` reports done for this phase and continues. `awaitAdvance(phase)` blocks only while the phaser is still on that phase. The usual barrier is `arriveAndAwaitAdvance()`; to leave after this generation use `awaitAdvance(arriveAndDeregister())`. Pass the phase those methods return — a stale argument is an immediate return.
