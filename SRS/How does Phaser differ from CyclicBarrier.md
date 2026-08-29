<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Synchronizers #SRS

# How does Phaser differ from CyclicBarrier?

> [!abstract] Short answer
> Both are reusable barriers. `CyclicBarrier` is a **fixed-size** party: every thread `await()`s, an optional constructor `Runnable` runs on the **last arriver**, then the generation can repeat or **break**. `Phaser` adds a **phase number**, **register / deregister**, **arrive without waiting**, and `onAdvance` instead of that constructor `Runnable`. Monitoring is open to any caller; arrival and waiting are for registered parties.

## Flexibility vs a fixed party

`CyclicBarrier` is for “a fixed sized party of threads that must occasionally wait for each other.” Party count is chosen in the constructor (`parties < 1` is illegal). There is no `register`. `await()` always waits for the rest of that party (or the last arriver runs the action and then everyone proceeds). [[How does CyclicBarrier run a barrier action when all parties arrive]] is that trip.

`Phaser` is “similar in functionality to `CyclicBarrier` and `CountDownLatch` but supporting more flexible usage.” `arriveAndAwaitAdvance()` is the documented analogue of `CyclicBarrier.await`. Extra knobs:

| | `CyclicBarrier` | `Phaser` |
| --- | --- | --- |
| Party count | Fixed at construction | `register` / `bulkRegister` / `arriveAndDeregister` |
| Generation id | Implicit cycle | Phase starts at 0, advances when all arrive, wraps after `Integer.MAX_VALUE` |
| Arrive without wait | No | `arrive()`, `arriveAndDeregister()` do not block |
| Barrier action | Constructor `Runnable`, last thread, others still parked | Override `onAdvance(phase, registeredParties)` on the advancing party (root only if tiered) |
| Interrupt while waiting | Breaks the barrier (`BrokenBarrierException` for the others) | `awaitAdvance` **keeps waiting**; interruptible overloads do not change phaser state |
| Failure model | All-or-none **broken** until `reset()` / new instance | `onAdvance` exception → **no advance**; `forceTermination()`; negative phase |
| Who may watch | `getNumberWaiting()` for debug | Any caller: `getPhase`, `getRegisteredParties`, … |
| Scale | One barrier | Max **65535** parties per phaser; tree of child phasers to spread contention |
| Since | 1.5 | 1.7 |

```java
import java.util.concurrent.CyclicBarrier;
import java.util.concurrent.Phaser;

public final class BarrierStyles {
    static CyclicBarrier cyclic(int n) {
        return new CyclicBarrier(n, () -> merge());
    }

    static Phaser phaser(int n, int rounds) {
        return new Phaser(n) {
            @Override
            protected boolean onAdvance(int phase, int registeredParties) {
                merge();
                return phase >= rounds - 1 || registeredParties == 0;
            }
        };
    }

    private static void merge() { /* shared state while others are dormant */ }
}
```

**Listing 1.** Same “run merge when the generation trips” idea. `CyclicBarrier` takes a `Runnable` and does not encode “stop after *k* rounds” in the constructor. `Phaser` overrides `onAdvance` and can **terminate** by returning `true` (default: terminate when deregister drops parties to zero). Returning `false` keeps the phaser alive for later `register`s.

```d2
direction: down
cb: "CyclicBarrier(n, action)\nall await(); last runs action" {
  width: 340
  height: 80
  style.fill: "#fff3e0"
}
ph: "Phaser: register / arrive\narriveAndAwaitAdvance / onAdvance" {
  width: 360
  height: 80
  style.fill: "#e8f5e9"
}
cb -> ph: "variable parties, phases,\narrive-only, termination"
```

**Fig. 1.** Phaser is not “CyclicBarrier plus a phase field” only: split arrival vs waiting, dynamic membership, and tiered parents (`Phaser(parent)`, `Phaser(parent, parties)`) have no CyclicBarrier equivalent.

`new Phaser()` starts at phase 0 with **zero** parties — every user must `register()` first. The phase advances when every **currently registered** party has arrived, not when “the last party is removed.” Removing the last party via `arriveAndDeregister` trips default `onAdvance` and **terminates**. That termination is how a Phaser replaces a one-shot latch — [[How can you emulate CountDownLatch with Phaser]] — not how a CyclicBarrier “opens.” Method split: [[What Phaser methods register arrive and awaitAdvance do]].

> [!warning] Phaser is not “CyclicBarrier with no action”
> There is no `Phaser(int, Runnable)`. The hook is `onAdvance`. If it throws, that exception goes to the advancing party and **the phase does not advance**. A throwing CyclicBarrier action **breaks** the barrier and the other waiters see `BrokenBarrierException`.

> [!warning] Unregistered waiting is not an observer API
> Synchronization methods are for **registered** parties. After `arriveAndDeregister` you wait with `awaitAdvance(phase)` using the phase that call returned. Any thread may **read** `getPhase()` / party counts (snapshots, not a wait). Do not treat monitoring as `CyclicBarrier.await`.

> [!tip] Interview answer
> CyclicBarrier is a fixed N-party reusable `await()`, with an optional last-arriver `Runnable` and a broken state. Phaser does the same job with a phase number, dynamic register/deregister, `arrive()` without blocking, and `onAdvance` for the trip action and termination. Use CyclicBarrier when the party size is stable and you want all-or-none breakage; use Phaser when membership changes, some tasks only report arrival, or you need a tree of phasers.
