<!--
reps: 0
priority: 0
-->
#Java/JVM #Java/Bytecode #SRS

# Why is Java described as platform independent?

> [!abstract] Short answer
> Because Java programs are distributed as bytecode, not as machine code: `javac` compiles sources to class files that any JVM can execute, so the same application runs on Windows, Linux, and macOS without recompilation. The platform independence lives in the class file format plus the per-platform JVM; it does not automatically cover native libraries or OS specifics in your code.

## The mechanism: one bytecode, many JVMs

The split of labor is fixed by the platform design. The compiler emits class files — the machine language of the JVM, not of any CPU. Each operating system ships its own JVM build, and that JVM is the platform-specific component: it reads the same class files and maps them onto its host. Compile once on Linux, copy the class files or JAR to Windows or macOS, and run — no per-OS recompilation. That is the historical "write once, run anywhere" promise, and the specification frames the JVM as exactly the component responsible for hardware- and operating-system independence.

```d2
direction: right
src: "App.java" {
  width: 180
  height: 70
  style.fill: "#e3f2fd"
}
classfile: "javac → App.class\n(bytecode, host-independent)" {
  width: 300
  height: 90
  style.fill: "#fff3e0"
}
win: "JVM for Windows\nx86-64" {
  width: 220
  height: 80
  style.fill: "#e8f5e9"
}
lin: "JVM for Linux\nx86-64 / aarch64" {
  width: 240
  height: 80
  style.fill: "#e8f5e9"
}
mac: "JVM for macOS\nx86-64 / aarch64" {
  width: 220
  height: 80
  style.fill: "#e8f5e9"
}
src -> classfile
classfile -> win
classfile -> lin
classfile -> mac
```

**Fig. 1.** One compiler output feeds three platform JVMs. Recompilation is never needed; only the JVM underneath changes.

```java
public class Hello {
    public static void main(String[] args) {
        System.out.println("any JVM can run me");
    }
}
// javac Hello.java      → Hello.class (identical on every OS)
// java Hello            → runs on Windows, Linux, macOS alike
```

**Listing 1.** The class file is the portability unit — the same artifact, not recompiled sources.

> [!warning] Bytecode is portable; your whole stack is not
> "Platform independent" is a property of the class file format and the JVM, and people over-extend it. The moment the application loads a native library with JNI/FFI, shells out to OS tools, or uses file paths and line separators directly, those parts stay platform-specific — hence the seasoned wording "write once, test everywhere". The JVM abstracts the execution model, not every OS difference your code can touch. See [[What is off-heap memory in the JVM]] for native memory and [[How do you invoke an external process in Java]] for OS integration.

This independence is also the door for other languages: anything that can be expressed in valid class files can be hosted by the JVM, which is why Kotlin and Scala ride the same mechanism — see [[Which languages besides Java run on the JVM]]. The engine that executes the bytecode is neither purely interpreter nor purely compiler — see [[What is the execution engine of the JVM]] and [[Is Java a compiled or interpreted language]].

> [!tip] Interview answer
> Java is platform independent because compilation targets the class file format, not a CPU: javac produces bytecode, and each operating system has its own JVM that runs the same bytecode. Portability is a property of the JVM layer; native libraries, file paths, and OS-specific code in the application remain platform-dependent, so in practice it is write once, test everywhere.
