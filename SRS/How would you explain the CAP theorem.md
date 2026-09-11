<!--
reps: 0
priority: 0
-->
#DistributedSystems #SystemDesign/Consistency #SystemDesign/Availability #SystemDesign/PartitionTolerance #SystemDesign/Tradeoffs #SRS

# How would you explain the CAP theorem

> [!abstract] Short answer
> CAP says a distributed data system facing a network partition must choose between two guarantees: Consistency (every read sees the latest write) and Availability (every request receives a response). Partition tolerance — the system keeps operating despite the network splitting — is not optional in a distributed system: partitions will happen. So the real choice, made at partition time, is C over A or A over C.

## The three properties, precisely

Consistency in CAP means linearizability: after any write completes, every subsequent read — anywhere — returns that write or a newer one. Availability means every request to a live node gets a (non-error) response, with no promise of freshness. Partition tolerance means the system survives arbitrary message loss or splitting between nodes. The theorem's force comes from the impossibility proof's scenario: a network splits replicas into two groups that cannot talk. If a write lands on group A and a read lands on group B, group B can either refuse to answer until the partition heals (staying consistent, giving up availability) or answer from stale data (staying available, giving up consistency). It cannot do both — the two groups cannot even agree they are partitioned without exchanging a message. That is why the theorem constrains only partitioned operation: while the network is healthy, a system can offer both C and A, which is the point [[Why do some people say the CAP theorem is obsolete]] develops.

```text
        network partition between replica groups G1 | G2
write x=1 to G1.
read x from G2:
  choose C -> G2 answers: "unavailable until partition heals"
  choose A -> G2 answers: "x=0" (stale)
  both     -> impossible: G2 cannot know about x=1
```

**Listing 1.** The partition scenario that makes C and A mutually exclusive.

## How real systems take the trade

The practical reading is per-operation, not per-product. CP-leaning systems refuse reads or writes that would break linearizability during a partition (ZooKeeper-style consensus stores; a single-leader database that stops serving writes when it loses its quorum — synchronous replication in [[How would you explain database replication strategies]] tightens this further). AP-leaning systems keep answering and converge later — eventually consistent stores in the BASE posture ([[What is BASE as a consistency model]]). Many stores make it tunable: quorum reads/writes (R + W > N) move the same cluster between the corners, and a single-leader relational database is CP for writes, AP for its replica reads. Beyond CAP, the latency axis matters even without partitions — Abadi's PACELC formalizes that "else" branch: [[How would you explain consistency in distributed systems and data stores]] places the models on that spectrum.

> [!warning] "CA" is not a valid distributed choice
> Any system claiming C and A while distributed is claiming partition tolerance implicitly or lying: partitions are physical reality, not a preference. The honest labels are "CP under partition" or "AP under partition" — and which one a system is shows only during a partition, exactly when you did not test it.

> [!tip] Interview answer
> CAP says that when the network splits, a distributed store must sacrifice either linearizable consistency or availability — partition tolerance is forced by physics. Healthy networks allow both, which is why the choice is made per system or per operation: CP systems stop or block during partitions, AP systems keep answering and converge later, quorum settings tune between them.
