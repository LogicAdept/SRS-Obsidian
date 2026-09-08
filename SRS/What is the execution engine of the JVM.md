<!--
reps: 0
priority: 0
-->
#Java/JVM #SRS

# What is the execution engine of the JVM?

> [!abstract] Short answer
> The execution engine is the part of the JVM that turns loaded bytecode into actual CPU work. It is an interpreter plus JIT compilers working together: every instruction can be interpreted one at a time, and methods that turn out to be hot are compiled to native code while the program runs. Default HotSpot mode is exactly this mix (`-Xmixed`).

## Interpreter and compilers

The specification only requires that the semantics of each bytecode instruction are preserved; how is up to the implementation. The classic interpreter follows a fetch–decode–execute loop over the operand stack. Interpreting alone is portable but slow for hot loops, so HotSpot profiles running code and hands hot methods and loops to its compilers: the tiered scheme starts with quick-to-produce client-tier code (C1) and, with more profiling, promotes to the fully optimized server-tier code (C2). Compiled methods keep their interpreter entry as a fallback, so deoptimization — for example when an assumed class hierarchy changes — can drop a method back to interpretation.

```d2
direction: down
bytecode: "bytecode of a method" {
  width: 260
  height: 70
  style.fill: "#e3f2fd"
}
interp: "Interpreter\nfetch · decode · execute one by one" {
  width: 320
  height: 80
  style.fill: "#fff3e0"
}
hot: "Hot?\n(profile: invocation + loop counters)" {
  width: 300
  height: 80
  style.fill: "#fff3e0"
}
c1: "C1\nfast native code + profiling" {
  width: 280
  height: 80
  style.fill: "#e8f5e9"
}
c2: "C2\naggressively optimized native code\ninlining · escape analysis · deopt" {
  width: 340
  height: 100
  style.fill: "#e8f5e9"
}
bytecode -> interp
interp -> hot
hot -> c1: warm
hot -> interp: cold stays here
c1 -> c2: very hot
```

**Fig. 1.** Tiered execution: everything starts interpreted; only code that proves hot is compiled, and compiled code can still be thrown away (deoptimized).

## The mode flags make it observable

The launcher exposes the split directly. `-Xint` disables compilation — everything runs interpreted. `-Xmixed`, which is on by default, interprets all bytecode except hot methods, which are compiled to native code. `-Xcomp` forces compilation at first invocation; the man page labels it a testing mode that should not be used in production.

```java
// Mode checks (run and compare cold vs warm timings):
System.out.println(System.getProperty("java.vm.name")); // OpenJDK 64-Bit Server VM
// java -Xint App   → interpreted only
// java -Xmixed App → interpreter + JIT (default)
// java -Xcomp App  → compile-first, testing mode only
```

**Listing 1.** The engine itself is not configurable away — only the interpretation/compilation mix is.

> [!warning] `-Xcomp` is not a performance flag
> A popular "optimization" is to start the JVM with `-Xcomp` so nothing is ever interpreted. In reality it hurts: first invocations pay full compilation cost, startup slows down, and the man page explicitly calls it a testing mode to exercise the JIT compilers. Real tuning keeps the default mixed mode. See [[Which JVM flags are commonly set when launching a Java process]].

The execution engine cooperates closely with memory and the class libraries: compiled code relies on the same run-time data areas, and engine decisions (inlining, deoptimization) are why micro-benchmarks on the JVM need warm-up. For the compilation side in depth, see [[How does JIT compilation work on the JVM]] and [[What is method inlining in the JIT]]; for how "compiled or interpreted" should be answered, see [[Is Java a compiled or interpreted language]].

> [!tip] Interview answer
> The execution engine is the JVM component that executes bytecode. It combines an interpreter — a fetch-decode-execute loop over instructions — with JIT compilers: hot methods and loops are profiled, compiled to native code by C1 and then C2, and can be deoptimized back to interpretation. The default mode is this mixed scheme; -Xint forces pure interpretation and -Xcomp is a testing-only mode.
