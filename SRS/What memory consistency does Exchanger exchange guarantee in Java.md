<!--
reps: 0
priority: 0
-->
#Java/JMM #Java/Concurrency/Synchronizers #SRS

# What memory consistency does Exchanger exchange guarantee in Java

> [!abstract] Short answer
> **For each pair of threads that successfully exchange objects via an `Exchanger`, actions prior to the `exchange()` in each thread happen-before those subsequent to the corresponding `exchange()` in the other thread.** Both directions at once: each side publishes to the other in a single rendezvous.

The Exchanger is symmetric, which distinguishes it from queues and latches: there is no producer and consumer role — both participants are simultaneously release and acquire sides ([[How does Exchanger swap data between two threads]]). The canonical use is swapping buffers or partially filled work batches: each thread fills its object, exchanges, and then processes the object it received with all of the partner's filling writes visible. Internally the rendezvous is a CAS-based slot/arena protocol in the JDK source, whose CAS and volatile accesses provide the ordering; the package documentation states the property for "each pair of threads that successfully exchange" — pairing is a precondition of the edge ([[What is a SynchronousQueue]]).

```d2
direction: right
a: "Thread A" {
  fa: "fill buffer A\n(plain writes)" { style.fill: "#e3f2fd" }
  xa: "exchange(bufferA)\nrelease + acquire" { style.fill: "#fff3e0" }
  fa -> xa: "program order"
}
b: "Thread B" {
  fb: "fill buffer B\n(plain writes)" { style.fill: "#e3f2fd" }
  xb: "exchange(bufferB)\nrelease + acquire" { style.fill: "#fff3e0" }
  fb -> xb: "program order"
}
xa -> xb: "A's writes visible to B"
xb -> xa: "B's writes visible to A"
```

**Fig. 1.** One rendezvous, two edges: each thread's pre-exchange writes are visible to the partner after the same exchange completes.

```java
Exchanger<Buffer> exchanger = new Exchanger<>();

// thread A
Buffer mine = acquireBuffer();
mine.fill(records);                       // plain writes
Buffer yours = exchanger.exchange(mine);  // rendezvous
process(yours);                           // sees all of thread B's filling writes

// thread B runs the same code with its own buffer
```

**Listing 1.** After the exchange returns, each thread processes the partner's buffer with complete visibility of the partner's pre-exchange writes — no locks, no volatile fields.

> [!warning] The edge requires a successful pairing
> The property is stated for successful exchanges: a lone thread that times out with `TimeoutException` never pairs and publishes nothing. Exchanging different objects on the two sides is fine — the edges attach to the rendezvous, not to object identity — but mutating the buffer *after* handing it over races with the partner's processing: the exchanged object should change ownership ([[What memory consistency do concurrent collections guarantee in Java]]). And each exchange pairs exactly two threads; a third thread arriving concurrently forms its own pair on its own slot ([[What memory consistency do barrier synchronizers guarantee in Java]]).

> [!tip] Interview answer
> **When two threads successfully exchange via Exchanger, the pre-exchange actions of each thread happen-before the post-exchange actions of the other — it is a bidirectional publication point, unlike one-way queue hand-off. The guarantee requires a successful pairing; ownership of the exchanged object transfers, so post-handover mutation is a race.**
