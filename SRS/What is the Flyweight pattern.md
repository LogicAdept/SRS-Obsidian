<!--
reps: 0
priority: 0
-->
#Patterns/GoF/Structural #SRS

# What is the Flyweight pattern

> [!abstract] Short answer
> Flyweight is a structural pattern that fits more objects into RAM by sharing the common, constant part of their state - the intrinsic state - instead of storing it in every object. The unique, changing part - the extrinsic state - moves outside and is passed to methods when needed.

## How the pattern works

Split the state first. Intrinsic state is the constant data many objects hold in identical copies - a bullet's color and sprite, a tree's species and texture. Extrinsic state is unique per object and changes over time - coordinates, velocity. The pattern stops storing extrinsic state inside the object: only intrinsic state remains, so thousands of context variations can share a handful of flyweight objects. The extrinsic state either moves into the container that aggregates the objects or arrives as method parameters; context-dependent behavior takes it as arguments.

In the particle-game example, three shared flyweights - bullet, missile, shrapnel - suffice for every particle on screen, while each particle's position and vector live with the particle, not in the flyweight.

```java
import java.util.HashMap;
import java.util.Map;

record TreeType(String name, String color, String sprite) {}   // intrinsic, shared, immutable

class Tree {
    private final int x, y;          // extrinsic, unique per tree
    private final TreeType type;     // shared reference

    Tree(int x, int y, TreeType type) {
        this.x = x;
        this.y = y;
        this.type = type;
    }
}

class TreeFactory {
    private static final Map<String, TreeType> types = new HashMap<>();

    static TreeType type(String name, String color, String sprite) {
        return types.computeIfAbsent(name, k -> new TreeType(name, color, sprite));
    }
}
```

**Listing 1.** The factory guarantees one TreeType per kind; every Tree carries only its coordinates plus a reference to the shared type.

```d2
direction: right
client: "Forest\n1,000,000 Tree objects" {
  width: 240
  height: 80
  style.fill: "#e3f2fd"
}
shared: "Shared flyweights\noak, pine, birch\n(3 objects)" {
  width: 220
  height: 90
  style.fill: "#e8f5e9"
}
ctx: "Extrinsic state\nx, y per tree" {
  width: 210
  height: 80
  style.fill: "#fff3e0"
}
client -> shared: references
client -> ctx: stores
```

**Fig. 1.** A million trees reference three shared type objects; the unique coordinates stay with each tree, which is where the memory saving comes from.

## Flyweights you already use in Java

The pattern is a runtime staple: [[What is the Java string pool]] interns identical string literals so every equal literal shares one object, and the boxed-value cache described in [[How would you explain Integer cache valueOf(100)==valueOf(100) true, valueOf(200) false]] shares Integer objects for small values - both are factory-managed shared instances with immutable intrinsic state. The relation to other patterns follows the same logic: shared leaf nodes of a composite tree are natural flyweights, and a flyweight collection resembles [[What is the Facade pattern]] only superficially - facade represents a whole subsystem with one object, flyweight multiplies little objects by sharing their state.

> [!warning] Immutability and the mixing trap
> Flyweight objects must be immutable: if shared state were mutable, one client's change would corrupt every other client using the same flyweight - which is also exactly why the pattern is not Singleton, since Singleton allows one mutable instance where flyweights allow many immutable ones per intrinsic-state combination. The classic bug is putting genuinely unique data - a coordinate, a timestamp - into the shared state, or letting extrinsic state leak into the flyweight; and applying the pattern to a few hundred short-lived objects is premature optimization that only complicates the design.

> [!tip] Interview answer
> Flyweight saves memory by splitting object state into shared intrinsic data kept inside immutable flyweight objects and unique extrinsic data stored by the context or passed into methods. A forest of a million trees shares three species objects; Java's string pool and the Integer cache are everyday examples. It pays off only with huge numbers of objects and heavy duplication, and the price is immutability plus careful separation of the two state kinds.
