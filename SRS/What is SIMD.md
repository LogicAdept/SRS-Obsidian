<!--
reps: 0
priority: 0
-->
#ComputerArchitecture #Java/Performance #SRS

# What is SIMD

> [!abstract] Short answer
> **SIMD — Single Instruction, Multiple Data — is a CPU capability where one instruction operates on a vector of several data elements at once (a 256-bit vector holds eight 32-bit ints).** In Java you usually get it implicitly through JIT autovectorization of simple loops; the Vector API (incubator since JDK 16, JEP 448 in JDK 21) exposes it explicitly so vector computations compile reliably to those instructions.

## One instruction, a row of lanes

A scalar add does one `a[i] + b[i]` per instruction. The SIMD unit holds several lanes; one vector add processes eight ints (256-bit register, 32-bit lanes) in the time a scalar loop does one iteration. Languages reach it two ways: implicitly — the JIT recognizes a simple array loop and vectorizes it — or explicitly, by writing vector-shaped code.

```d2
direction: right
sc: "Scalar loop\ni: a[i]*b[i] -> c[i]\none element per instruction" {
  width: 330
  height: 100
  style.fill: "#e3f2fd"
}
ve: "SIMD\none instruction -> 8 lanes\na[i..i+7] * b[i..i+7]" {
  width: 330
  height: 100
  style.fill: "#e8f5e9"
}
jv: "Java access\n1) JIT autovectorization (implicit)\n2) Vector API (explicit, incubator)" {
  width: 340
  height: 110
  style.fill: "#fff3e0"
}
sc -> ve
ve -> jv
```

**Fig. 1.** SIMD widens the operation from one element to a register full of lanes; Java reaches it via the JIT or the Vector API.

The explicit Java path (from the Vector API JEP): pick a species (lane shape) — `IntVector.SPECIES_256` is eight ints — then loop over array chunks aligned to the species length, doing `va.mul(vb).intoArray(...)`, with a scalar tail for the remainder.

```java
static final VectorSpecies<Integer> SPECIES = IntVector.SPECIES_256; // 8 ints per vector

int[] a = {1, 2, 3, 4, 5, 6, 7, 8};
int[] b = {10, 20, 30, 40, 50, 60, 70, 80};
int[] c = new int[a.length];

int i = 0;
int bound = SPECIES.loopBound(a.length);
for (; i < bound; i += SPECIES.length()) {
    IntVector va = IntVector.fromArray(SPECIES, a, i);
    IntVector vb = IntVector.fromArray(SPECIES, b, i);
    va.mul(vb).intoArray(c, i);       // one instruction stream, 8 lanes
}
for (; i < a.length; i++) c[i] = a[i] * b[i];   // scalar tail

System.out.println(java.util.Arrays.toString(c));
```

**Listing 1.** Compiled and run on JDK 21 with `--add-modules jdk.incubator.vector`:

```java
[10, 40, 90, 160, 250, 360, 490, 640]
```

**Listing 2.** Elementwise products computed by a single vector multiply per eight elements — the demo array fits in exactly one 256-bit vector, so the scalar tail loop ran zero times.

> [!warning] SIMD is not automatic profit — alignment, tails, and "vectorized in my head" lie
> Three traps. First, autovectorization is a best-effort compiler pass: the JIT vectorizes simple, dependency-free loops — aliasing between arrays, early breaks, or boxed `Integer` streams defeat it, and there is no way to *see* whether it happened without JVM flags and JIT logs; the Vector API exists precisely because implicit vectorization is unreliable ("reliably compile at runtime to optimal vector instructions" is its stated goal). Second, the speedup is bounded by the lane width — eight lanes is at most ~8x, minus load/store and tail overhead; real gains are workload-specific, and memory-bound code may see none. Third, in JDK 21 the Vector API is an **incubator** module: `--add-modules jdk.incubator.vector` for both `javac` and `java`, API can change between releases, and it is not for production paths yet — answering "I just put vector instructions in my Java" without the incubator caveat dates the knowledge. SIMD speedups arrive only through the JIT, so the whole claim inherits JIT preconditions — see [[How does JIT compilation work on the JVM]] — and the analogous "state the precondition before claiming performance" rule shows up in [[How would you explain which design pattern ideas appear in StringBuilder and StringBuffer]].

> [!tip] Interview answer
> **SIMD is single instruction, multiple data — the CPU applies one instruction to a whole vector of elements, e.g. eight ints in a 256-bit register. Java gets it two ways: JIT autovectorization of simple loops, or explicitly via the Vector API, which in JDK 21 is an incubator module — you pick a species, loop in chunks, and one mul covers eight lanes with a scalar tail. Gains are real but bounded by lane width and data movement; autovectorization is best-effort, which is why the explicit API exists.**

