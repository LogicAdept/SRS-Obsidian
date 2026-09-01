<!--
reps: 0
priority: 0
-->
#Java/Versions/8 #Java/Library/Nashorn #SRS

# What is Nashorn

> [!abstract] Short answer
> **Nashorn is the JDK 8 JavaScript engine: ECMAScript-262 Edition 5.1 on the JVM.** Java apps embed it through `javax.script`; the CLI is `jjs`. It compiles scripts to bytecode, loads them with a dedicated class loader, and can call Java (`Java.type`, JavaBeans). It **replaced Rhino**, was **deprecated in 11**, **removed in 15**. It is not a browser, not ES6, not Node. The dump’s “2–10× faster” is not a spec number.

## ES5.1 on HotSpot, then gone

Nashorn shipped in Java 8 (JEP 174) as a new engine in the JDK: `javax.script` (JSR 223) plus `jjs`. The language target is **ES5.1** only — no Edition 6, no DOM/CSS, no jQuery, no browser plugin ([[How would you explain the Nashorn JavaScript engine on the JVM]], [[What is jjs]], [[How would you explain the jjs command line tool for Nashorn]]).

Pipeline: lexer → parser → bytecode (ASM) → `defineClass` on a **custom class loader** → run. Calls use `invokedynamic`. A Java receiver can bind to a Java method, including JavaBean getters/setters as script properties. From Java you obtain an engine via `ScriptEngineManager` / `NashornScriptEngineFactory` and `eval`. From JS, `Java.type("java.lang.System")` (preferred over walking `Packages`).

Rhino (the older JDK engine) was interpreter-heavy; Nashorn’s **goal** was significantly better performance and memory by compiling to JVM bytecode. That is not a guaranteed “2 to 10 times” figure.

Java 11 terminally deprecated the `jdk.scripting.nashorn*` modules and `jjs`. Java 15 **removed** them. **`javax.script` itself stayed** — only the Nashorn implementation left ([[How are JavaScript and Java related if at all]]).

```d2
direction: down
js: "ES5.1 source" {
  width: 180
  height: 40
  style.fill: "#fff8e1"
}
bc: "bytecode + custom loader" {
  width: 240
  height: 45
  style.fill: "#e8f5e9"
}
api: "javax.script / jjs / Java.type" {
  width: 280
  height: 45
  style.fill: "#e3f2fd"
}

js -> bc
bc -> api
```

**Fig. 1.** Compile-in-memory is the Rhino contrast. No zone in the heap for a browser DOM — there isn’t one.

```text
jjs
jjs> var System = Java.type("java.lang.System")
jjs> System.currentTimeMillis()
```

```java
import javax.script.ScriptEngine;
import jdk.nashorn.api.scripting.ClassFilter;
import jdk.nashorn.api.scripting.NashornScriptEngineFactory;

class Demo {
    static void embed() throws Exception {
        NashornScriptEngineFactory factory = new NashornScriptEngineFactory();
        ScriptEngine engine = factory.getScriptEngine((ClassFilter) name -> true);
        engine.eval("print(java.lang.System.getProperty(\"java.home\"));");
    }
}
```

**Listing 1.** JS→Java via `Java.type`. Java→JS via `javax.script` + `NashornScriptEngineFactory.getScriptEngine(ClassFilter)` from the Java 8 Nashorn guide (`jdk.nashorn.api.scripting` **dies in 15**). Interactive `jjs` is the same engine.

> [!warning] Not on a current LTS
> Interview dumps treat Nashorn as “how you run JS in Java.” On JDK 15+ there is no Nashorn and no `jjs`. `javax.script` remains; you supply another engine. ES6/`let`/DOM answers are out of spec. The 2–10× claim is folklore.

> [!warning] Embedding untrusted scripts
> Generated classes still go through the Java security model. `ClassFilter` can hide classes such as `java.io.File`; reflection can punch through unless you also deny `nashorn.javaReflection`. Concatenated JS strings may be `ConsString`, not `java.lang.String`.

> [!tip] Interview answer
> **Nashorn = JDK 8’s ES5.1 JavaScript engine on the JVM** (`javax.script` + `jjs`), compiling to bytecode. Java↔JS interop via `Java.type` / `eval`. Faster-than-Rhino was the design goal. Deprecated in 11, removed in 15. Not a browser.
