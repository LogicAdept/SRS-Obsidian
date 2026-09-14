<!--
reps: 0
priority: 0
-->
#Java/JMM #Java/Concurrency/Synchronization/Locks #Java/Concurrency/Synchronizers #SRS

# What memory consistency do synchronizer release and acquire guarantee in Java

> [!abstract] Short answer
> **Actions prior to "releasing" synchronizer methods — `Lock.unlock`, `Semaphore.release`, `CountDownLatch.countDown` — happen-before actions subsequent to a successful "acquiring" method — `Lock.lock`, `Semaphore.acquire`, `Condition.await`, `CountDownLatch.await` — on the same synchronizer object in another thread.** This single j.u.c property covers locks, semaphores, latches, and conditions at once.

It is the generalized monitor rule: the same release-to-acquire edge, extended to the explicit synchronizers built on `AbstractQueuedSynchronizer`. In the JDK source the delivery is visible: `AQS.release` calls `tryRelease` and then `signalNext(head)` to unpark the successor, and synchronizer state is a volatile field written with release/acquire mode accessors — the queued waiter that observes the state change receives every write the releaser made before releasing ([[What is the monitor lock rule in the Java Memory Model]]). For `CountDownLatch` this yields the familiar orchestration pattern: all setup done before `countDown()` is visible to every thread after `await()` returns ([[What is CountDownLatch]]).

```d2
direction: right
p: "Releasing thread" {
  width: 204
  height: 74
  w: "populate state\n(plain writes)" {
    width: 200
    height: 104
    style.fill: "#e3f2fd"
  }
  rel: "unlock / release / countDown\n(release)" {
    width: 312
    height: 104
    style.fill: "#fff3e0"
  }
  w -> rel: "program order"
}
aqs: "Synchronizer object\n(AQS volatile state + CLH queue)" {
  width: 340
  height: 104
  style.fill: "#f3e5f5"
}
c: "Acquiring thread" {
  width: 204
  height: 74
  acq: "lock / acquire / await returns\n(acquire)" {
    width: 330
    height: 104
    style.fill: "#fff3e0"
  }
  r: "reads state\n-> fully visible" {
    width: 204
    height: 104
    style.fill: "#e8f5e9"
  }
  acq -> r: "program order"
}
rel -> aqs: "release writes state"
aqs -> acq: "waiter observes state,\nunparks via signalNext"
```

**Fig. 1.** All AQS-based synchronizers publish through volatile synchronizer state plus the wait queue — the same shape as monitor unlock→lock, parameterized per synchronizer type.

```java
CountDownLatch ready = new CountDownLatch(1);
List<String> sharedConfig = new ArrayList<>();     // plain field

// initializer thread
sharedConfig.add("feature-a");
sharedConfig.add("feature-b");
ready.countDown();                                  // release

// worker thread
ready.await();                                      // acquire (successful return)
sharedConfig.forEach(System.out::println);          // both entries visible
```

**Listing 1.** The latch count-down publishes the pre-release list mutations to every worker that passes `await()` — no locks or volatile needed anywhere.

> [!warning] Same object, successful acquisition
> The edge requires the *same* synchronizer instance — releasing one `Semaphore(1)` and acquiring another publishes nothing ([[What is Semaphore]]). Failed attempts give no edge: an `tryLock` that returns false, or an `await` that times out or throws, is not a successful acquisition, and reads afterwards are unordered. `Condition.await` participates through its associated lock — it must be held on entry and is released and reacquired around the wait, weaving the same edges as monitor wait/notify ([[What is the difference between synchronized and ReentrantLock]], [[What is ReadWriteLock]]).

> [!tip] Interview answer
> **Releasing any j.u.c synchronizer — Lock.unlock, Semaphore.release, CountDownLatch.countDown — happens-before a subsequent successful acquire — lock, acquire, await — of the same synchronizer in another thread. It is the generalized monitor rule implemented through AQS volatile state and queue unparking. The traps: the edge is per instance, and timed or failed acquisitions deliver nothing.**
