<!--
reps: 0
priority: 0
-->
#Java/JMM #Problems/Concurrency #SRS

# What reads does the Java Memory Model allow in a data race

> [!abstract] Short answer
> **A read `r` of a variable may observe a write `w` to it if `r` is not ordered after `w` — `hb(r, w)` does not hold — and there is no intervening write `w'` with `hb(w, w')` and `hb(w', r)` (JLS 17.4.5, happens-before consistency).** In a data race a read may see the default value, a stale older write, or any racing write — but never a value nobody wrote.

The rule is the precise answer to "what can possibly go wrong without synchronization". Since the real-time order of two racing writes means nothing, both of the reader's outcomes in the classic two-flag example are legal: each thread can read the *other's* flag as 0 even after both writes "happened" — the JLS example `B = 1; r2 = A;` against `A = 2; r1 = B;` allows `r2 == 0 && r1 == 0`, which no sequential interleaving could produce but happens-before consistency allows ([[What is ordering as-if-serial semantics sequential consistency visibility atomicity happens-before mutual excl]]). One boundary keeps the madness bounded: no out-of-thin-air values — every observed value must come from some actual write to that variable, including the conceptual default write ([[What is the default value happens-before rule in the Java Memory Model]]).

```d2
direction: right
w1: "T1: B = 1" { style.fill: "#e3f2fd" }
w2: "T2: A = 2" { style.fill: "#e3f2fd" }
r1: "T1: r2 = A\nmay see 0" { style.fill: "#ffebee" }
r2: "T2: r1 = B\nmay see 0" { style.fill: "#ffebee" }
w1 -> r1: "program order"
w2 -> r2: "program order"
note: "no hb edges across threads:\nr2=0 and r1=0 is a legal outcome" { style.fill: "#fff3e0" }
```

**Fig. 1.** Two racing reads both observing initial values — allowed by happens-before consistency and impossible under sequential consistency. This is exactly the reordering-style surprise DRF-SC programs never see ([[What does the Java Memory Model guarantee for data race free programs]]).

```java
int a = 0;
int b = 0;

// thread 1
b = 1;
int r2 = a;      // legal: 0, 2, or any value "in between" a racing write

// thread 2
a = 2;
int r1 = b;      // legal: 0, 1, or any racing write to b
```

**Listing 1.** With no edges, both reads may return their defaults even though the writes precede them in source order — and both returning 0 simultaneously is legal, unlike in a sequentially consistent world.

> [!warning] Real time is not an argument; the rule is local
> "I wrote it before the other thread read it" carries no weight without an edge — allowedness is defined purely in happens-before terms ([[What is the difference between a race condition and a data race]]). Also note what the rule does not permit: an intervening ordered write — one with `hb(w, w')` and `hb(w', r)` — is *not* observable, so a thread cannot see a "very old" value once a properly published newer one exists on its path. The escape from this whole regime is adding an edge: one volatile, one monitor, one j.u.c hand-off turns the racing pair into ordered accesses and re-enters the DRF-SC guarantee ([[Is there a universal fix for race conditions in concurrent code]], [[What is the volatile visibility rule in the Java Memory Model]]).

> [!tip] Interview answer
> **In a data race a read may see any write it is not happens-before-ordered against, unless a newer properly-ordered write intervenes — so stale reads, defaults, and both-threads-see-zero outcomes are all legal; the only prohibition is out-of-thin-air values. This is the formal floor under races, and one synchronizes-with edge removes the pair from this regime entirely.**
