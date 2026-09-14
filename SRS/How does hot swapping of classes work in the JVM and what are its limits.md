<!--
reps: 0
priority: 0
-->
#Java/JVM/ClassLoaders #SRS

# How does hot swapping of classes work in the JVM and what are its limits

> [!abstract] Short answer
> **Hot swapping is replacing the bytes of already loaded classes without restarting the JVM, and the supported mechanism is a java.lang.instrument agent: the JVM hands the agent an Instrumentation object, and the agent calls redefineClasses or retransformClasses to install new class-file bytes for existing classes.** The swap keeps the same Class object — no re-running of initializers, static fields keep their values, live instances are untouched — but it may only change method bodies, the constant pool and attributes; it must not add, remove or rename fields or methods, change method signatures, modifiers or inheritance ([[How would you explain Java class loaders and dynamic class loading]]).

## Agents install the mechanism

The java.lang.instrument package provides services that allow Java programming language agents to instrument programs running on the JVM; the mechanism for instrumentation is modification of the bytecodes of methods. The class files that comprise an agent are packaged into a JAR file, and an attribute in the main manifest identifies one of the classes as the agent class. Agents packaged with the application in an executable JAR are started at JVM startup time; agents packaged into an agent JAR may be started at JVM startup time via a command line option, or — where an implementation supports it — started in a running JVM. The JVM invokes a special method (premain at startup, agentmain for a running JVM) and passes the Instrumentation object, and the manifest declares what the agent needs: Premain-Class, Agent-Class, Can-Redefine-Classes, Can-Retransform-Classes ([[How would you explain the Java class loader]]).

Agents can transform classes in arbitrary ways at load time by registering a ClassFileTransformer; redefineClasses and retransformClasses are the two calls that reach classes already loaded.

## Redefine and retransform

retransformClasses reruns the transformation: the supplied classes pass through the chain of registered transformers, and the class file bytes are not checked, verified and installed until after the transformations have been applied — if the resultant bytes are in error, the method throws and none of the classes are changed. redefineClasses installs supplied class files directly. Both operate on a set to allow interdependent changes to more than one class at the same time, and both are gated by support flags the agent can query: isRedefineClassesSupported, isRetransformClassesSupported, and per-class isModifiableClass, with UnmodifiableClassException naming the offender ([[What happens if two class loaders load the same class]]).

```d2
direction: down
jar: "agent JAR\nPremain-Class, Can-Redefine-Classes" {
  width: 300
  height: 60
  style.fill: "#fff3e0"
}
jvm: "JVM startup\npremain(agentArgs, instrumentation)" {
  width: 320
  height: 60
}
tr: "ClassFileTransformer registered" {
  width: 290
  height: 50
}
call: "redefineClasses / retransformClasses" {
  width: 330
  height: 50
  style.fill: "#e3f2fd"
}
same: "same Class object\nnew method bodies installed" {
  width: 300
  height: 60
  style.fill: "#e8f5e9"
}
jar -> jvm
jvm -> tr
tr -> call
call -> same
```

**Fig. 1.** The agent is wired in at startup and spends its capability later; the swap replaces definitions in place, with no new loader and no new Class.

## What survives and what cannot change

A redefinition does not cause initializers to be run: the values of static variables remain as they were prior to the call, and instances of the redefined class are not affected. If a redefined method has active stack frames, those frames continue to run the bytecodes of the original method — the redefined method is used on new invokes. What may change is equally precise: the retransformation may change method bodies, the constant pool and attributes; it must not add, remove or rename fields or methods, change the signatures of methods, change modifiers, or change inheritance, and it must not change the NestHost, NestMembers, Record or PermittedSubclasses attributes ([[What triggers class initialization in Java]]).

```java
import java.lang.instrument.ClassDefinition;
import java.lang.instrument.Instrumentation;

public class PatchAgent {
    private static Instrumentation inst;

    public static void premain(String args, Instrumentation inst) {
        PatchAgent.inst = inst;   // the JVM hands this over at startup
    }

    public static void swap(Class<?> target, byte[] patched) throws Exception {
        inst.redefineClasses(new ClassDefinition(target, patched));
        // same Class object: static fields keep their values, live
        // instances are untouched, running frames finish on old bytes
    }
}
```

**Listing 1.** The agent skeleton: premain captures the Instrumentation handle, and the swap is one call — subject to the schema limits above and the support flags reported by the JVM.

> [!warning] Schema changes need a new loader, not a redefine
> Adding a field, a method or changing a signature is not a failed patch — it is outside what redefineClasses can express, and the JVM rejects it. When the shape of a class must change, the escape hatch is class reloading: throw away the old defining loader and define the class again in a fresh one, at the cost of new Class identity and re-run static state ([[How do you write a custom class loader in Java]]). Spring Boot DevTools follows the reload road for application classes while agents and hot swap stay in the redefine world ([[What is Spring Boot DevTools]]).

> [!tip] Interview answer
> **Hot swap runs through java.lang.instrument: an agent gets Instrumentation at premain or agentmain and calls redefineClasses or retransformClasses to replace the bytes of loaded classes — same Class object, no initializers re-run, statics and instances preserved, active frames finish on the old bytecodes.** The limit is structural: method bodies, constant pool and attributes may change; fields, methods, signatures, modifiers and inheritance may not. Schema changes require a new class loader instead.
