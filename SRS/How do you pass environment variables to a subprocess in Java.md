<!--
reps: 0
priority: 0
-->
#Java/Runtime #SRS

# How do you pass environment variables to a subprocess in Java

> [!abstract] Short answer
> Call `ProcessBuilder.environment()` — it returns a modifiable `Map<String, String>` pre-filled with a copy of the current process environment. `put`, `putIfAbsent`, or `remove` entries, and every subsequent `start()` from that builder passes the map to the child as its environment. The parent's own environment (seen by `System.getenv`) is unmodifiable and unaffected.

Each `ProcessBuilder` owns an **independent** environment map: changes to one builder never leak into another builder or into the parent process. The child therefore receives exactly the parent's inherited set plus your modifications — the demo below adds one variable and the child reads it back, while the parent's own `System.getenv` still knows nothing about it.

## Parent puts, child reads

```java
public class EnvVarDemo {
    public static void main(String[] args) throws Exception {
        String javaBin = ProcessHandle.current().info().command().orElse("java");
        ProcessBuilder pb = new ProcessBuilder(javaBin, "-cp", ".", "ChildEnv");
        pb.environment().put("MY_TOOL_TOKEN", "secret-42");
        Process p = pb.start();
        p.waitFor();
        System.out.println(new String(p.getInputStream().readAllBytes()).trim());
        System.out.println("parent sees MY_TOOL_TOKEN=" + System.getenv("MY_TOOL_TOKEN"));
    }
}

class ChildEnv {
    public static void main(String[] args) {
        System.out.println("child MY_TOOL_TOKEN=" + System.getenv("MY_TOOL_TOKEN"));
        System.out.println("child has PATH=" + (System.getenv("PATH") != null));
    }
}
// Output (JDK 21):
// child MY_TOOL_TOKEN=secret-42
// child has PATH=true
// parent sees MY_TOOL_TOKEN=null
```

**Listing 1.** The child inherits `PATH` unchanged, sees the added variable, and the parent's own environment stays untouched.

> [!warning] Three common mistakes
> "The child's environment starts empty" is false — it starts from the parent's, which is usually what you want but leaks everything you did not remove. Mutating the map after `start()` does not affect the already-running child — modifications apply to future `start()` calls only. And the map may reject operations on some OSes: `environment()` can throw `UnsupportedOperationException` for unsupported systems, and null keys or values are rejected with `NullPointerException`. The older path — `Runtime.exec(cmdarray, envp)` with a `String[]` environment — exists but has none of the builder's ergonomics; see [[What is the difference between Runtime.exec and ProcessBuilder]].

The specification itself recommends system properties (`-Dkey=value`) over environment variables when the child is a Java program — env vars have global effect across all descendants and OS-specific case rules. Reading the child-side counterpart (`System.getenv`) connects to [[What is the purpose of the Runtime class and the System class]], and the launch mechanics around this are in [[How do you invoke an external process in Java]].

> [!tip] Interview answer
> I take `ProcessBuilder.environment()` — a mutable copy of the parent environment specific to this builder — and add or remove entries before `start()`. The child sees the modified set; other builders and the parent's `System.getenv` are untouched, and post-`start()` edits reach only future launches. For Java-to-Java communication, system properties are usually cleaner than environment variables.

