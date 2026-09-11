<!--
reps: 0
priority: 0
-->
#Patterns/GoF/Creational #Patterns/GoF/Structural #SRS

# What is the difference between the Builder and Facade design patterns

> [!abstract] Short answer
> They live in different categories and solve different problems. **Builder is creational**: it constructs one complex object step by step and hands over the finished product at the end. **Facade is structural**: it exposes a simple entry point to an already existing subsystem and forwards calls into it. Both reduce client complexity — one by hiding construction, the other by hiding usage.

## What each pattern actually does

Builder moves construction out of the product class: a builder interface declares steps, concrete builders implement them, and an optional director fixes the order of steps for standard configurations. The product does not exist in finished form until the client calls the fetch step, and different builders can produce different representations from the same sequence of steps. Facade does not create anything: it wraps a subsystem of many classes, knows where to route each client request, and performs the initialization and sequencing internally, so the client talks to one object instead of a dozen. The subsystem classes are not even aware of the facade. The catalog's canonical example is a video-conversion facade whose single `convert(filename, format)` method hides codecs, bitrate readers, and audio mixing.

```java
// Builder: the client drives construction, the product appears at build()
Car car = new CarBuilder()
        .seats(2)
        .engine(new SportEngine())
        .build();

// Facade: the client makes one call, the facade sequences the subsystem
File mp4 = new VideoConverter().convert("clip.ogg", "mp4");
```

**Listing 1.** The client-facing difference: Builder assembles a new object through chained steps, Facade forwards one call into an existing subsystem.

## The comparison in one line each

Builder answers "how do I construct a complex object cleanly"; Facade answers "how do I hide a complex subsystem behind one object". A facade can later become a Singleton — one facade object is usually enough — while a builder is stateful per construction and typically reset between builds. When the question pushes further, the Builder side extends into [[What are the advantages of the Builder pattern over constructors]], and the Facade side into the wrapper family overview in [[What are examples of structural design patterns]].

> [!warning] "Both simplify" is where answers go wrong
> Simplification is the shared vibe, not the shared mechanism. Saying the Facade builds objects or that the Builder wraps a subsystem collapses the creational/structural boundary — the exact boundary this comparison tests. A related trap: a facade that grows methods for every client need becomes a god object coupled to everything, which is the pattern's own listed con.

> [!tip] Interview answer
> Builder is creational: it constructs a complex object step by step, often with a director defining the order, and returns the product only when construction finishes. Facade is structural: it gives one simplified interface over an existing subsystem and routes calls into it without adding new functionality. Builder hides construction complexity, Facade hides usage complexity.
