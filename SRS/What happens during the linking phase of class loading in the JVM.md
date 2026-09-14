<!--
reps: 0
priority: 0
-->
#Java/JVM/ClassLoaders #SRS

# What happens during the linking phase of class loading in the JVM

> [!abstract] Short answer
> Linking is the middle phase between loading and initialization: verification of the binary, preparation of static fields with default values, and — at some point — resolution of symbolic references ([[How would you explain the Java class loader]] walks the whole ladder). Two properties are fixed: a class is completely loaded before it is linked, and completely verified and prepared before it is initialized ([[What triggers class initialization in Java]] picks up at the initialization gate). When resolution happens is an implementation choice, so linkage errors surface at a use of the bad reference, not necessarily at load time.

## Verification

Verification ensures that the binary representation of a class or interface is structurally correct. If the binary violates the structural constraints, a `VerifyError` must be thrown at the point in the program that caused the class or interface to be verified. Verification may cause additional classes to be loaded, but need not cause them to be verified or prepared — loading cascades further than checking does. Failures are sticky: if verification fails because a `LinkageError` was thrown, subsequent attempts to verify the same class always fail with the same error.

## Preparation

Preparation involves creating the static fields for a class or interface and initializing such fields to their default values. This does not require the execution of any JVM code: explicit initializers for static fields are executed as part of initialization, not preparation. So after preparation `int` fields read `0` and reference fields read `null` no matter what the source assigns; the assignments happen later, inside `<clinit>`. During preparation the JVM also imposes loading constraints — type-name-and-loader pairs that overriding methods must agree on across the hierarchy.

## Resolution

Resolution is the process of dynamically determining one or more concrete values from a symbolic reference in the run-time constant pool ([[What is the JVM class constant pool]] is where those references live); initially, all symbolic references are unresolved. Instructions such as `new`, `getstatic`, `putstatic`, `invokestatic`, `checkcast`, `instanceof`, and `ldc` rely on symbolic references, and executing any of them requires resolving the reference. The spec allows an implementation flexibility as to when linking activities take place — lazy resolution per use or eager resolution up front — provided the ordering properties hold; HotSpot resolves per first use.

```java
class Service {
    static int port = 8080;        // preparation: 0  -> initialization: 8080
    static final int LIMIT = 10;   // constant variable: folded at compile time
    static { System.out.println("clinit runs"); }
}
// Linking of Service:      verify the class file, create port with value 0.
// No Java code has run yet.
// Initialization of Service (first active use): port = 8080, then "clinit runs".
```

**Listing 1.** Conceptual split of one class across the phases: preparation gives defaults without running any code; the source values appear only when initialization runs.

```d2
direction: right
load: "Load\nbinary -> Class" {
  width: 150
  height: 55
  style.fill: "#e3f2fd"
}
verify: "Verify\nstructure" {
  width: 140
  height: 55
  style.fill: "#fff3e0"
}
prepare: "Prepare\nstatics -> defaults" {
  width: 180
  height: 55
  style.fill: "#fff3e0"
}
resolve: "Resolve\nsymbolic refs (when?)" {
  width: 200
  height: 55
  style.fill: "#fff3e0"
}
init: "Initialize\n<clinit>" {
  width: 150
  height: 55
  style.fill: "#e8f5e9"
}
load -> verify
verify -> prepare
prepare -> resolve
resolve -> init
```

**Fig. 1.** The phases in order. Verification and preparation must complete before initialization; the resolve node sits in the flow without a fixed position, because the timing is an implementation choice.

> [!warning] Linkage errors are deferred by design
> Because resolution may be lazy, a missing or malformed dependency surfaces at the first instruction that touches it — sometimes minutes after startup, in a rarely taken branch. That is the mechanism behind `NoClassDefFoundError` appearing "far" from the actual problem ([[What is the difference between ClassNotFoundException and NoClassDefFoundError]]).

> [!tip] Interview answer
> **Linking is verification, preparation and resolution between loading and initialization. Verification checks the binary structure, `VerifyError` if it is broken; preparation creates static fields with default values and runs no code; resolution turns constant-pool symbolic references into concrete values, lazily per use or eagerly, an implementation choice. Loaded before linked, verified and prepared before initialized — errors surface at a use of the bad reference.**

