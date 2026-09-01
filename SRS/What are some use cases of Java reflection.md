<!--
reps: 0
priority: 0
-->
#Java/Language/Reflection #SRS

# What are some use cases of Java reflection?

> [!abstract] Short answer
> **Wherever the program must examine or use types that were not fixed in the calling source: load a class by name, inspect members, construct, invoke, or read fields.** Core reflection is specified for **debuggers, interpreters, object inspectors, class browsers**, and services such as **Object Serialization** and **JavaBeans**. The Oracle Reflection trail adds **extensibility** (instantiate a user class from its fully qualified name), **visual tools**, and **test harnesses** that discover and call APIs on a class.

## What the platform names, not a product list

`java.lang.reflect` plus `Class` exist so a program can obtain information about fields, methods, and constructors of **loaded** classes and then operate on those members, within encapsulation and security restrictions ([[What is reflection in Java]], [[How can you get the Class object in Java]]).

```d2
direction: down
need: "Runtime type unknown in source" {
  width: 280
  height: 50
}
ext: "Extensibility\nforName + newInstance" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
tools: "Browsers, IDEs,\ndebuggers, tests" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}
svc: "Serialization, JavaBeans,\nProxy, Array" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
need -> ext
need -> tools
need -> svc
```

**Fig. 1.** Official buckets. Frameworks and test runners are instances of these, not extra language features.

**Extensibility.** Create an instance from a **fully qualified name** that arrives at runtime (config, plugin). That is `Class.forName` plus `Constructor.newInstance` ([[How can you create an instance of a class using reflection]], [[How can you invoke a method using reflection]]).

**Class browsers and visual environments.** Enumerate members (`getFields` / `getMethods` / `getConstructors` and the declared variants) and use type information so a tool can show or generate correct calls.

**Debuggers and test tools.** Debuggers need **private** members; `setAccessible` exists so privileged code (and serialization) can suppress language access checks ([[What does setAccessible do in the Reflection API]], [[How do you invoke a private constructor using reflection]]). A test harness can discover methods on a class and invoke them systematically.

**Serialization, JavaBeans, arrays, proxies.** The package lists Object Serialization and JavaBeans as clients that need public members of a runtime class or declared members of a given class. `Array` creates and indexes arrays whose component type is a `Class`. `Proxy.newProxyInstance` builds a runtime class that implements given interfaces and forwards calls to an `InvocationHandler` ([[What is a dynamic proxy in Java reflection]]).

```java
class Plugin {
    static Object load(String binaryName) throws Exception {
        Class<?> type = Class.forName(binaryName);
        return type.getDeclaredConstructor().newInstance();
    }
}
```

**Listing 1.** Extensibility pattern from the trail: name in, instance out. The Java 9 replacement for `Class.newInstance()` is `getDeclaredConstructor().newInstance()`.

> [!warning] If the type is already in the source, call it directly
> The trail’s rule: if the operation is possible without reflection, prefer that. Reflective calls skip some VM optimizations, need extra permissions under a security manager, and can reach `private` state — which breaks abstractions and can change across platform upgrades ([[What are the drawbacks of using Java reflection]]).

> [!warning] Product names are examples of the buckets
> “Spring / Hibernate / JUnit” are not APIs in `java.lang.reflect`. They sit in extensibility, member inspection, serialization-style field access, proxies, and test discovery. Answer with those jobs; name a framework only as an illustration.

> [!tip] Interview answer
> **Reflection is for code that must work with classes it did not name at compile time: plugins, class browsers, debuggers, test runners, serializers, JavaBeans, and dynamic proxies.** You load a `Class`, inspect members, then construct or invoke. **If you already know the type, a normal call is the better design.**
