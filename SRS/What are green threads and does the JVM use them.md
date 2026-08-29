<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Threads #OperatingSystems/Concurrency #SRS

# What are green threads and does the JVM use them?

> [!abstract] Short answer
> **Green threads** are **user-mode** threads scheduled by the **runtime**, not 1:1 by the OS. **Early Java** used them: **M:1** — many Java threads on **one** OS thread. They **lost** to **platform threads** (OS **1:1** wrappers). **HotSpot today** does **not** implement `Thread` that way. **Virtual threads** (Java 21+) are also **user-mode**, but **M:N** (many VTs on **N** carriers). Do not call VTs “green threads” without that distinction. VTs: [[How would you explain Virtual Threads]]. Platform: [[How would you explain distinctive traits of the Java platform]]. Carriers/daemons: [[How would you explain daemon threads in Java]].

## M:1 then, 1:1 and M:N now

**Platform** `Thread`s map **1:1 to kernel threads**, large OS stacks, limited count — suitable for any work, including CPU. **Virtual** threads are scheduled by the **Java runtime** onto a **small set of carriers**; they suit **mostly-blocked** I/O, not long CPU loops. That is **not** classic green-thread **M:1**: many VTs can run on **several** OS threads (parallelism defaults to **available processors**; carrier max default **256** in the reference scheduler).

```java
Thread.ofPlatform().start(() -> {});   // 1:1 OS thread (not green)
Thread.ofVirtual().start(() -> {});    // M:N user-mode, not M:1 green
```

**Listing 1.** Current APIs. There is no `Thread.ofGreen()`.

```d2
direction: down
g: "early green M:1" {
  width: 180
  height: 36
  style.fill: "#ffebee"
}
p: "platform 1:1" {
  width: 160
  height: 36
  style.fill: "#fff8e1"
}
v: "virtual M:N" {
  width: 160
  height: 36
  style.fill: "#e8f5e9"
}
os: "OS threads" {
  width: 140
  height: 36
  style.fill: "#e3f2fd"
}
g -> os: "one"
p -> os: "one each"
v -> os: "N carriers"
```

**Fig. 1.** Green = all Java threads share **one** OS thread. That is not virtual threads.

> [!warning] M:1 cannot use multiple cores for Java threads
> One OS thread means one core for all green threads. That is why 1:1 platform threads won for a long time.

> [!warning] “The JVM uses green threads again” is imprecise
> Virtual threads are **user-mode M:N**. Interviewers who say “green” usually mean the **old M:1** model, which **is not** what `ofVirtual()` does.

> [!tip] Interview answer
> Green threads are user-mode threads; early Java ran many of them on a single OS thread. The JVM dropped that for one-to-one platform threads. Virtual threads are user-mode again but many-to-many on carriers, so I would not call them green threads without saying M-to-N.
