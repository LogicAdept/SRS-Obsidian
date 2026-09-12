<!--
reps: 0
priority: 0
-->
#Patterns/GoF/Creational #SRS

# What is the Prototype pattern

> [!abstract] Short answer
> Prototype is a creational pattern that lets you copy existing objects without making your code dependent on their concrete classes. The objects themselves implement cloning - usually one `clone` method that copies their field values - so the client asks a configured object for a copy instead of constructing one from scratch.

## How the pattern works

Copying an object from the outside has two traps: some fields are private and invisible to the copier, and doing the copy requires knowing the object's concrete class in the first place. Prototype delegates the cloning to the object itself. A common interface declares a clone method; each class implements it by creating an object of its own class and carrying over the field values - and since the clone runs inside the same class, it can copy private fields too. A set of pre-configured objects then acts as an alternative to subclassing: instead of constructing and configuring a fresh object, the client clones the prototype that is already configured the right way.

```java
class Style {
    String outline;
}

class Circle implements Cloneable {
    private final int radius;
    private Style style;

    Circle(int radius, Style style) {
        this.radius = radius;
        this.style = style;
    }

    @Override
    public Circle clone() {
        try {
            return (Circle) super.clone();  // shallow: the style reference is copied, not the Style object
        } catch (CloneNotSupportedException e) {
            throw new AssertionError(e);
        }
    }
}
```

**Listing 1.** The clone lives inside the class, so it can copy private fields; `super.clone()` performs the field-by-field copy.

```d2
direction: down
proto: "Pre-configured prototypes\nCircle(30), Circle(60)..." {
  width: 280
  height: 80
  style.fill: "#e3f2fd"
}
client: "Client needs a similar object" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}
clone: "proto.clone()" {
  width: 180
  height: 60
  style.fill: "#e8f5e9"
}
copy: "New object with the same field values\nno constructor chain, no concrete class in client" {
  width: 360
  height: 90
  style.fill: "#e8f5e9"
}
proto -> client
client -> clone -> copy
```

**Fig. 1.** Cloning replaces construction: the client never names the concrete class and never re-runs expensive configuration.

## Cloning in Java specifically

Java ships the machinery but with sharp edges: `Object.clone()` is protected, `Cloneable` is a marker interface with no methods, and forgetting to implement it makes `clone()` throw `CloneNotSupportedException`. The default copy is shallow - reference fields are copied as references, so the clone shares mutable objects with the original, which is why deep copy needs explicit handling. Many teams prefer copy constructors or static copy factories instead of `Cloneable` for new APIs. The pattern still shows up through its idea: pre-configured prototypes as alternatives to subclassing, and cloning complex Composite or Decorator structures instead of rebuilding them. The relation to the other creational names is traced in [[What is the difference between the Singleton and Prototype design patterns]], the simpler-than-Memento trade-off appears in [[What is the Memento pattern]], and the catalogue context is in [[What are examples of creational design patterns]].

> [!warning] Shallow copy shares mutable internals
> A cloned object that shares a `Style`, list, or map with its original is a bug farm: a mutation through one object visibly changes the other. Decide explicitly, per reference field, whether the clone needs a deep copy - and say "shallow by default" out loud in the interview, because claiming `clone()` produces an independent object unconditionally is a classic trap.

> [!tip] Interview answer
> Prototype moves copying into the object itself: a clone method on the class copies the field values - including private ones - and the client clones a pre-configured prototype instead of constructing and configuring a new object. It avoids coupling the client to concrete classes and works as an alternative to subclassing for heavily configured objects. In Java the default is a shallow copy, so mutable reference fields need an explicit deep-copy decision.
