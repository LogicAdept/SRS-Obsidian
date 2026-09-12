<!--
reps: 0
priority: 0
-->
#Patterns/GoF/Structural #SRS

# What is the Facade pattern

> [!abstract] Short answer
> Facade is a structural pattern that provides a simplified interface to a library, framework, or any other complex subsystem of classes. The facade knows which subsystem objects to call and in what order; the client talks to the facade instead of the moving parts.

## How the pattern works

Wiring business logic directly into a sophisticated subsystem couples your classes to its implementation details: initializing objects, tracking dependencies, calling methods in the right order. A facade is one class that exposes only what clients actually need - possibly less than the subsystem can do - and performs the orchestration internally. The subsystem classes stay unaware of the facade and keep working with each other directly, and the facade adds no new functionality of its own: it routes and sequences what already exists.

The canonical scenario is wrapping a large third-party library: an app that uploads short videos only needs `encode(filename, format)`, not the professional conversion framework's dozens of classes.

```java
class VideoConverterFacade {
    VideoFile encode(String filename, String format) {
        VideoFile source = VideoFile.open(filename);       // subsystem: open
        Codec codec = CodecRegistry.forFormat(format);     // subsystem: pick codec
        BitrateReader reader = new BitrateReader(source, codec);
        FrameBuffer frames = reader.readFrames();          // subsystem: decode
        return frames.encodeTo(format);                    // subsystem: re-encode
    }
}
```

**Listing 1.** Conceptual facade over a video-conversion toolkit: the client sees one method, the framework's classes and their ordering stay hidden inside.

```d2
direction: right
client: "Client" {
  width: 150
  height: 70
  style.fill: "#e3f2fd"
}
facade: "Facade\nencode(filename, format)" {
  width: 270
  height: 80
  style.fill: "#fff3e0"
}
s1: "VideoFile" {
  width: 140
  height: 60
  style.fill: "#e8f5e9"
}
s2: "Codec" {
  width: 130
  height: 60
  style.fill: "#e8f5e9"
}
s3: "BitrateReader" {
  width: 160
  height: 60
  style.fill: "#e8f5e9"
}
s4: "FrameBuffer" {
  width: 150
  height: 60
  style.fill: "#e8f5e9"
}
client -> facade
facade -> s1
facade -> s2
facade -> s3
facade -> s4
```

**Fig. 1.** The facade is the client's single entry point into the subsystem; subsystem classes neither know about it nor talk through it.

## What a facade is not

A facade does not change the interface of one object the way an adapter does - adapters retrofit an existing interface into a usable one, and usually wrap a single object, while a facade works with an entire subsystem and defines a new, simpler interface. It is also not a mediator: both organize collaboration among tightly coupled classes, but subsystem objects never talk through the facade, while mediator components abandon direct communication entirely. And it is not a God object - the facade delegates, it does not absorb the subsystem's logic. The related comparisons live in [[What is the difference between the Builder and Facade design patterns]], [[How would you explain the Adapter design pattern]], and [[What is the Mediator pattern]]; the same delegation instinct at the responsibility level is the facade controller of [[What is the Controller principle in GRASP]], and the coupling rationale behind wrapping subsystems is [[What is the Indirection principle in GRASP]].

> [!warning] The facade can become a god class
> Piling every client's needs into one facade recreates the complexity it was meant to hide - an additional facade per client group is the standard remedy. Do not claim a facade "adds functionality" or that the subsystem depends on it: the facade may offer limited functionality compared to direct subsystem use, the subsystem classes operate unaware of it, and the client can still bypass it when it needs the raw power.

> [!tip] Interview answer
> A facade gives a complex subsystem one simple entry point: the client calls encode(filename, format), and the facade orchestrates the library's objects, ordering, and initialization internally while the subsystem stays unaware of it. It differs from Adapter - which makes one existing interface usable - and from Mediator - whose components actually communicate through it. I reach for a facade when clients need a small, stable slice of a big library.
