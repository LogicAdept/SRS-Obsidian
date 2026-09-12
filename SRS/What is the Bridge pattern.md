<!--
reps: 0
priority: 0
-->
#Patterns/GoF/Structural #SRS

# What is the Bridge pattern

> [!abstract] Short answer
> Bridge is a structural pattern that splits one large class - or a set of closely related classes - into two independent hierarchies, abstraction and implementation, connected by a reference. Each hierarchy can then grow without multiplying the class combinations.

## How the pattern works

The problem it attacks is class explosion from extending along two independent dimensions. A Shape hierarchy extended with colors produces BlueCircle, RedSquare, and friends: adding a triangle means one subclass per color, adding a color means one subclass per shape - the number of combinations grows geometrically. Bridge switches from inheritance to composition: extract one dimension - say, Color - into its own hierarchy, and give the Shape hierarchy a reference to a Color object. Any color work delegates through that reference, which is the bridge between the hierarchies. New colors no longer touch shapes, and new shapes no longer touch colors.

The GoF wording calls the two sides Abstraction and Implementation; they do not mean abstract class and interface here - they are simply the two orthogonal dimensions, and either side can have several levels of its own.

```java
interface Color {
    String fill();
}

class Red implements Color {
    @Override
    public String fill() {
        return "red";
    }
}

abstract class Shape {                     // abstraction hierarchy
    private final Color color;             // the bridge into the second hierarchy

    Shape(Color color) {
        this.color = color;
    }

    String describe() {
        return getClass().getSimpleName() + " filled with " + color.fill();
    }
}

class Circle extends Shape {
    Circle(Color color) {
        super(color);
    }
}
```

**Listing 1.** Shape never inherits from color; it holds one and delegates - two hierarchies, one reference between them.

```d2
direction: right
shapes: "Shape hierarchy\nCircle, Square, Triangle" {
  width: 240
  height: 90
  style.fill: "#e3f2fd"
}
ref: "reference\n(the bridge)" {
  width: 190
  height: 70
  style.fill: "#fff3e0"
}
colors: "Color hierarchy\nRed, Blue, Green" {
  width: 230
  height: 90
  style.fill: "#e8f5e9"
}
shapes -> ref -> colors
```

**Fig. 1.** Adding a shape or a color adds one class in its own hierarchy - the combinations compose at runtime instead of exploding at compile time.

## Same shape as Strategy and State, different intent

Bridge, State, and Strategy - and to a degree Adapter - share the composition structure: a context holding a reference to a helper hierarchy and delegating to it. What separates them is the problem being solved, which is why a pattern name communicates intent and not just a diagram. The comparison between the two behavioral twins is drawn in [[What is the difference between the Strategy and State design patterns]]. Bridge is usually designed up-front to keep two dimensions developing independently, while [[How would you explain the Adapter design pattern]] is retrofitted to make an existing incompatible class usable. Beware the name collision: [[What is the Messaging Bridge pattern]] moves messages between messaging systems and has nothing to do with this class-structure pattern.

> [!warning] Two interview traps
> First, "bridge" in the pattern sense is not the EIP Messaging Bridge and not a network bridge - quoting a database link or a message bridge as an example shows you do not know the GoF pattern. Second, calling Bridge "just Strategy with another name" ignores intent: Strategy swaps interchangeable algorithms behind one context, while Bridge permanently splits a class into two independently extendable hierarchies - if you cannot name the two dimensions and the reason they must grow separately, you have not found a Bridge.

> [!tip] Interview answer
> Bridge splits a class extended along two independent dimensions into two hierarchies joined by one reference: the abstraction holds the implementation interface and delegates to it. Shape and Color is the canonical pair - instead of RedCircle and BlueSquare subclasses, you compose at runtime. Adding either dimension becomes adding one class, and the structure looks like Strategy but answers a different question: independent growth of two hierarchies rather than swapping one behavior.
