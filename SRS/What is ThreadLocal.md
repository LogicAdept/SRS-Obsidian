<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Threads #SRS

# What is ThreadLocal?

> [!abstract] Short answer
> A **`ThreadLocal<T>`** is a **per-thread copy** of a value: each thread’s **`get` / `set` / `remove`**. Threads do **not** see each other’s copies. **`set` in `main` does not initialize a worker** — that worker’s **`get()`** is **`initialValue()`** until **that** thread **`set`s** or you use **`withInitial`**. Copies are **references**: if two threads **`set` the same object**, they **share** it. On a **pool**, **`remove()`** in **`finally`** or the next task **sees leftover** state. Pools: [[How would you explain ThreadPoolExecutor]]. Spring’s holder: [[Why does SecurityContextHolder use ThreadLocal]]. Inherit: [[What is MODE_INHERITABLETHREADLOCAL in SecurityContextHolder]]. VTs: [[How would you explain Virtual Threads]].

## One object, many copies

`get()` returns this thread’s copy, calling **`initialValue()`** (default **`null`**) on first access unless **`set`** already ran. **`withInitial(Supplier)`** is the usual factory. After **`remove()`**, the next **`get()`** calls **`initialValue()`** again. Copies are **not** a happens-before with other threads: they are **different variables**.

**`InheritableThreadLocal`** copies the parent’s value when a child **`Thread` is created** (context class loader uses this). A `Thread.Builder` can turn inheritance off. Pool workers are **not** new children per task, so they do **not** get a fresh inheritable snapshot per `execute`. `Executors` default threads **need not** share the submitting thread’s locals; **`ThreadPoolExecutor.beforeExecute` / `afterExecute`** exist specifically to **reinitialize** them. Fork/Join common-pool workers are **not guaranteed** to keep locals across tasks.

```java
static final ThreadLocal<String> USER = ThreadLocal.withInitial(() -> "anon");

void handle(String user) {
    USER.set(user);
    try {
        // same thread: USER.get() is user
    } finally {
        USER.remove(); // next pooled task must not see user
    }
}
```

**Listing 1.** Static `ThreadLocal`, `set` for this request, **`remove` in `finally`** so a reused worker is clean.

```d2
direction: down
tl: "static ThreadLocal" {
  width: 170
  height: 36
  style.fill: "#fff8e1"
}
a: "thread A copy" {
  width: 140
  height: 36
  style.fill: "#e3f2fd"
}
b: "thread B copy" {
  width: 140
  height: 36
  style.fill: "#e8f5e9"
}
tl -> a: "get / set"
tl -> b: "get / set"
```

**Fig. 1.** One `ThreadLocal` object; each live thread holds its own value until `remove` or the thread dies.

> [!warning] Pools keep the thread, so they keep the value
> A worker that stays in a pool stays alive. Without `remove()`, the next task on that worker sees the previous copy (data leak and retained objects). `try` / `finally { remove(); }` is the cleanup, not optional style.

> [!warning] Not a substitute for passing a parameter across threads
> `submit(() -> USER.get())` reads the **worker’s** copy, not the caller’s, unless you set it on that worker (or wrap the task). Inheritance applies at **thread creation**, not at `execute`.

> [!tip] Interview answer
> ThreadLocal gives each thread its own copy of a value, usually stored in a static field so request context is available without extra parameters. I always remove in a finally when the thread might be pooled, because the worker stays alive and would otherwise leak the last task’s data. It is not a way to publish a value to another thread.
