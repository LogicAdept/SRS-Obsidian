<!--
reps: 0
priority: 0
-->
#Java/Spring/Integration #Java/Spring/Data/Redis #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`RedisLockRegistry` (module `spring-integration-redis`) is a lightweight distributed lock on Redis. You obtain a `Lock` by key and `tryLock` around a critical section (for example one payment per `orderId` across instances).

Dumps contrast it with Redisson: RedisLockRegistry has no watchdog auto-renewal, no fair/read-write/RedLock extras, and a smaller dependency. Use it for simple mutual exclusion; use Redisson when you need lease extension on long critical sections.

```java
Lock lock = lockRegistry.obtain("payment:" + orderId);
if (lock.tryLock(5, TimeUnit.SECONDS)) {
    try { return executePayment(orderId, amount); }
    finally { lock.unlock(); }
}
```

> [!warning] Unverified traps from the dump
> - Without a watchdog, a lock TTL can expire while the critical section still runs — another instance can enter.
> - Always unlock in `finally`; interrupt handling should restore the interrupt flag.
