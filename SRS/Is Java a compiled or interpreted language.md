<!--
reps: 0
priority: 0
-->
#Java/JVM #Java/Bytecode #SRS

# Is Java a compiled or interpreted language?

> [!abstract] Short answer
> Both, in two stages. Java source is always compiled ahead of time by `javac` into bytecode (class files). Then the JVM executes that bytecode with an interpreter and, for hot code, JIT-compiles it to native machine code at run time. "Compiled" and "interpreted" are not opposites here — they are two phases of one pipeline.

## Stage 1: ahead-of-time to bytecode

The compiler (`javac`) parses sources and produces class files containing JVM instructions. This step happens before deployment, on the developer's machine, and its output is host-independent: class files contain bytecodes — the machine language of the JVM — not instructions for any real CPU. This is the sense in which Java is a compiled language: there is a distinct, mandatory compilation step and an intermediate binary artifact.

## Stage 2: interpreter plus JIT at run time

At run time the JVM starts by *interpreting* bytecode — a fetch-decode-execute loop over each instruction. The default mode (`-Xmixed`, on by default) also profiles running code and compiles hot methods to native code with the JIT compilers, so long-running code gets compiled performance while cold code pays no compile cost. The JVM specification even notes the machine is not inherently interpreted: an implementation may compile instructions directly to CPU code.

```d2
direction: right
src: "App.java\n(source)" {
  width: 200
  height: 80
  style.fill: "#e3f2fd"
}
javac: "javac\nAOT compilation" {
  width: 220
  height: 80
  style.fill: "#fff3e0"
}
classfile: "App.class\n(bytecode)" {
  width: 200
  height: 80
  style.fill: "#fff3e0"
}
jvm: "JVM" {
  width: 160
  height: 60
  style.fill: "#e8f5e9"
}
interp: "interpreter\n(all code)" {
  width: 230
  height: 80
  style.fill: "#e8f5e9"
}
jit: "JIT → native\n(hot code only)" {
  width: 240
  height: 80
  style.fill: "#e8f5e9"
}
src -> javac: ahead of time
javac -> classfile
classfile -> jvm
jvm -> interp
interp -> jit
```

**Fig. 1.** One compiled artifact, then a mixed interpreter/JIT execution phase — the reason both labels apply.

```java
// Observable pipeline:
//   javac Hello.java        → Hello.class    (compiled stage)
//   java Hello              → interpreted + JIT (run-time stage)
//   java -Xint Hello        → interpreted only (slower loops)
//   java -Xmixed Hello      → default: interpreter + JIT
```

**Listing 1.** The flags expose the two stages; `-Xmixed` is the default mix.

> [!warning] "Java is interpreted, so it is slow" is a stale lie
> The claim dies on two facts. First, the JVM is not inherently interpreted — the specification allows compiling instructions straight to CPU code, and real implementations JIT-compile hot paths to native speed. Second, "compiled vs interpreted" describes *how code reaches the CPU*, not *how fast the ecosystem runs*; Java's peak throughput comes from the JIT tier, and startup-heavy use cases are addressed by tools like class data sharing and ahead-of-time experiments. Answer the mechanism, not the legend. See [[How does JIT compilation work on the JVM]] and [[What is the execution engine of the JVM]].

For the portability consequence of the two-stage design, see [[Why is Java described as platform independent]]; for the machine that runs the bytecode, see [[What is the JVM]].

> [!tip] Interview answer
> Java is both. javac compiles source to bytecode ahead of time — that is the compiled part, and the class file is the portability artifact. Then the JVM executes the bytecode by interpreting it and JIT-compiling hot methods to native code — the default mixed mode. So: compiled to an intermediate form, then interpreted and dynamically compiled at run time.
