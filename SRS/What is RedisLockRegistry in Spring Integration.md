<!--
reps: 0
priority: 0
-->
#Java/Spring/Integration #Java/Spring/Data/Redis #SRS

# What is RedisLockRegistry in Spring Integration?

> [!abstract] Short answer
> **`RedisLockRegistry`** (`spring-integration-redis`) is Spring Integration’s **Redis-backed `LockRegistry`**: `obtain(key)` returns a distributed lock so only one thread across JVMs holds that key. Locks live under `registryKey:lockKey` and **expire** (default **60 seconds**) so a crashed holder cannot leave a hung lock forever.

## Role

Integration components such as aggregators/resequencers take a lock from a `LockRegistry` so only one thread mutates a message group. **`DefaultLockRegistry`** is in-process. Point those components (or your own code) at **`RedisLockRegistry`** when a shared `MessageGroupStore` spans instances and you need the same mutual exclusion cluster-wide.

You can also use it as a general Redis distributed lock: obtain by business key, `tryLock`, run the critical section, `unlock` in `finally`.

```java
@Bean
RedisLockRegistry redisLockRegistry(RedisConnectionFactory factory) {
  return new RedisLockRegistry(factory, "payment-locks"); // default 60s expire
}

// elsewhere
Lock lock = lockRegistry.obtain("order:" + orderId);
if (lock.tryLock(5, TimeUnit.SECONDS)) {
  try {
    return executePayment(orderId, amount);
  } finally {
    lock.unlock();
  }
}
```

**Listing 1.** Registry over a connection factory; obtain by key and guard the critical section (pattern from Spring Integration distributed-lock docs).

```d2
direction: right
a: "App instance A\nobtain(order:1)" {
  style.fill: "#e3f2fd"
}
b: "App instance B\nobtain(order:1)" {
  style.fill: "#fff3e0"
}
redis: "Redis key\nregistryKey:order:1\nTTL expireAfter" {
  style.fill: "#e8f5e9"
}

a -> redis
b -> redis
```

**Fig. 1.** Same lock key across instances; Redis holds ownership until unlock or TTL expiry.

## Expiration and renewal

To avoid hung locks after a JVM death, Redis keys expire after **`expireAfter`** (constructor overload; default **60s**). Docs warn: set expiry long enough that a healthy critical section finishes, but short enough that a dead holder recovers in acceptable time.

If the TTL expires while you still think you hold the lock, another instance can enter. Unlocking an **expired** ownership is a severe condition (resources may already be compromised): historically `IllegalStateException`; from **6.4**, `RedisLock.unlock()` throws **`ConcurrentModificationException`**.

From **6.4**, `setRenewalTaskScheduler(...)` renews the lock about every **1/3** of the expiration while held. From **7.0**, locks implement **`DistributedLock`** with per-acquire TTL (`lock(Duration)`, `tryLock(..., Duration ttl)`) and `renewLock(key, ttl)`.

> [!warning] Expiry while still in the critical section
> Without renewal (or with too short `expireAfter`), TTL can elapse mid-work. Another node can take the lock. Treat expired-unlock exceptions as critical.

> [!warning] Always unlock in `finally`
> Same as any `Lock`: leak the hold across returns/exceptions and you block peers until TTL. Restore the interrupt flag if you catch `InterruptedException`.

> [!tip] Interview answer
> `RedisLockRegistry` is Spring Integration’s Redis `LockRegistry`: `obtain(key)` gives a cluster-wide lock with a default 60s Redis TTL so dead holders recover. Use it for multi-instance mutual exclusion; configure expiry carefully, unlock in `finally`, and use 6.4+ renewal or 7.0+ per-lock TTL for longer sections.

See [[What is RedisTemplate]] and [[How do you use opsForValue with RedisTemplate]].
