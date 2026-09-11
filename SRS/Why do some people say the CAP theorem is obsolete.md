<!--
reps: 0
priority: 0
-->
#SystemDesign/Consistency #SystemDesign/PartitionTolerance #SRS

# Why do some people say the CAP theorem is obsolete

> [!abstract] Short answer
> "CAP is obsolete" does not mean the theorem is wrong — it means CAP is too coarse to design with. It says nothing about latency (the common case, versus the rare partition), collapses many consistency models into one binary "C", and its C (linearizability) is rarely what systems need. PACELC and the spectrum of consistency models replaced the three-letter tradeoff in actual design discussions.

## The latency blindness: PACELC's "else"

CAP constrains behavior only during a partition — an exceptional event. Abadi's PACELC makes the everyday tradeoff explicit: if Partitioned, choose A or C; Else, choose Latency or Consistency. A synchronously replicated system pays a network round trip on every write even with a perfectly healthy network — that is a C-vs-L choice, invisible to CAP. Modern stores make exactly this choice per operation: quorum writes with R+W>N add latency to buy consistency; async replication returns fast and accepts staleness. Framing designs around PACELC explains actual product knobs (tunable consistency, read-your-writes routing) that CAP cannot express — the reason the paper's framing displaced CAP in design reviews about geo-distributed databases. [[How would you explain the CAP theorem]] gives the theorem itself; [[How would you explain consistency in distributed systems and data stores]] the model spectrum it hides.

## The collapse of "C" and the practical reframe

CAP's C is linearizability — the strongest consistency. Real systems use a ladder below it: read-your-writes, session, monotonic, causal — each cheaper, each sufficient for large parts of an application (a user seeing their own post does not need linearizability across all users). Calling every weaker model "AP" and everything else "CP" erases distinctions that drive design; the Jepsen-style analyses of databases (tests under real partitions and clocks) exposed that many "CP" products violate linearizability under realistic conditions, and many "AP" products offer stronger client-session guarantees than the label implies. The obsolescence argument, then: partition behavior is a corner case best handled by consensus protocols (Raft/Paxos libraries) rather than chosen globally; day-to-day tradeoffs are latency versus consistency level, per operation. The practical successor questions are "which consistency model per read?" and "how many round trips per write?" — not "C, A or P?".

```text
CAP:     partitioned? -> C or A (binary, rare case)
PACELC:  partitioned? -> C or A
         else?        -> Latency or Consistency (every request)
design:  per-operation consistency level + session guarantees
```

**Listing 1.** Why PACELC plus the consistency-model ladder supersede the three-letter choice.

> [!warning] Declaring CAP irrelevant does not remove partitions
> The theorem still bites: any "CA" distributed claim is wrong, and a partition will still force your system to reveal which corner it actually occupies. The mature position is "CAP is insufficient", not "CAP is false".

> [!tip] Interview answer
> The criticism is coarseness, not falsity: CAP speaks only about the rare partition and reduces consistency to linearizability. PACELC adds the everyday latency-versus-consistency tradeoff, and real designs choose per operation from a ladder of consistency models. So CAP survives as a boundary theorem, while PACELC and the model ladder do the actual design work.
