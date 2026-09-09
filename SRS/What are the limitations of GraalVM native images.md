<!--
reps: 0
priority: 0
-->
#Java/Quarkus #SRS

# What are the limitations of GraalVM native images?

> [!abstract] Short answer
> Native compilation runs a **closed-world analysis**: everything reachable must be known at build time. Consequences — reflection, dynamic proxies, JNI and serialization need explicit registration metadata; **resources must be included deliberately** (`quarkus.native.resources.includes/excludes`); no runtime class generation or arbitrary classloading; some libraries simply do not work. Build cost is real (minutes and gigabytes of RAM), startup becomes near-instant but there is **no JIT** — sustained peak throughput of long-running services can be lower than the JVM's warmed-up profile.

## What the closed world forbids, and how Quarkus mitigates

The image builder starts from the main entry point and transitively includes only reachable code; anything invoked reflectively is invisible unless registered. Quarkus' answer is architectural: the **augmentation phase does the dynamic work at build time** — bean discovery over the Jandex index, bytecode recording instead of runtime generation, and automatic registration of reflection/proxy/resource metadata for the frameworks it ships ([[What happens at build time in Quarkus]]). That is why a Quarkus REST application "just compiles natively" while a plain Java app using `Class.forName` on unregistered classes fails at runtime with a missing-class or wrong-method error. What remains the developer's job: resources loaded by name (`quarkus.native.resources.includes` — by default **no resources are included** beyond what extensions register), reflection on user classes (`@RegisterForReflection`), and runtime-initialized singletons — code executed in native runs during image build unless it is explicitly runtime-initialized.

```java
// Resource inclusion - the documented knob (native guide), JDK 21 + Quarkus 3.39.2 shape:
//
// Given src/main/resources/ignored.png, src/main/resources/foo/selected.png and
// bar/some.txt inside a dependency jar:
//
// quarkus.native.resources.includes = foo/**,bar/**/*.txt
// -> foo/selected.png and bar/some.txt are inside the image; ignored.png is not.
//
// User-class reflection for JSON mapping (common interview example):
// import io.quarkus.runtime.annotations.RegisterForReflection;
//
// @RegisterForReflection                   // registers constructor/methods/fields metadata
// public class CustomerDto {
//     public String name;
//     public int age;
// }
// (Conceptual listing: native builds require the GraalVM/Mandrel native-image toolchain,
//  absent from this deck's verified JDK-only run; the properties and annotations are quoted
//  from the official native-image guide's sections on resources and reflection.)
```

**Listing 1.** Marked `Conceptual` for the native build itself. The mechanism to narrate: the image only contains what the analysis proved reachable, and the two properties/annotations above are how user code tells it about otherwise-invisible things.

```d2
direction: down
build: "native-image build\nclosed-world reachability analysis" {
  width: 360
  height: 65
  style.fill: "#fff3e0"
}
reg: "Registration needed\nreflection | proxies | JNI | resources | serialization" {
  width: 420
  height: 65
  style.fill: "#f5c6c6"
}
qk: "Quarkus mitigations\naugmentation records metadata,\nextensions register for you" {
  width: 380
  height: 65
  style.fill: "#e8f5e9"
}
you: "Your job\nresources.includes, @RegisterForReflection,\nlibrary compatibility checks" {
  width: 400
  height: 65
}
reg -> qk: "framework-owned dynamics"
reg -> you: "application-owned dynamics"
build -> reg
```

**Fig. 1.** The limitation splits into two ownership lanes: the framework's dynamic features are pre-registered by the build, application-specific dynamics stay the developer's responsibility.

## Trade-offs to state explicitly

Startup: native wins by an order of magnitude — relevant for scale-to-zero, serverless, frequent restarts ([[Why does Quarkus use less memory than traditional Java stacks]] covers the memory half of that story). Peak throughput: the JVM's JIT (profile-guided inlining, escape analysis) typically overtakes the AOT image on hot long-running paths — relevant for steady high-traffic services. Build cycle: native compilation is slow and memory-hungry; debugging native images is harder (JVM-mode debugging first). Mandrel — the downstream distribution Quarkus CI tests — exists for exactly this purpose.

> [!warning] "Native is automatically better" — the wrong default
> The honest decision matrix: instant-start, small-RSS, scale-to-zero workloads pick native; sustained-throughput services usually run better on the JVM fast-jar with warm JIT, at equal engineering cost. Two technical traps: a static initializer that touches environment, files or sockets executes during image build unless marked runtime-init — the value gets frozen into the binary; and Class.forName-style plugin loading cannot discover classes that the analysis never saw — third-party plugin architectures need their own registration story or stay JVM-only.

> [!tip] Interview answer
> Native images are closed-world: only provably reachable code ships, so reflection, dynamic proxies, JNI and serialization need registration metadata, and resources must be explicitly included with quarkus.native.resources.includes. Quarkus handles the framework side — augmentation does discovery at build time and records bytecode, so its stack compiles natively — while developers register their own reflective DTOs with @RegisterForReflection. The trade-off I name: unbeatable startup and RSS, but no JIT — long-running high-throughput services often stay on the JVM.
