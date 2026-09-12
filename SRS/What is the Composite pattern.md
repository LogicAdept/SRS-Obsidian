<!--
reps: 0
priority: 0
-->
#Patterns/GoF/Structural #SRS

# What is the Composite pattern

> [!abstract] Short answer
> Composite is a structural pattern that composes objects into tree structures and lets you work with the whole tree as if it were a single object. Leaf and container share one component interface, and operations called on a container recurse through the tree.

## How the pattern works

The pattern only fits when the core model really is a tree: products inside boxes inside bigger boxes, UI panels inside panels, folders inside folders. The classic example is pricing an order of products packed into nested boxes. Direct code would have to know the classes, the nesting levels, and unwrap everything itself. Composite instead declares one component interface with the operation - say, price - and lets each node answer for itself: a product returns its own price, a box sums the price of everything it contains. When you call the operation on the outermost box, the objects themselves pass the request down the tree, and the client never inspects concrete classes.

```java
import java.util.ArrayList;
import java.util.List;

interface Item {
    long priceCents();
}

record Product(String name, long priceCents) implements Item {
}

class Box implements Item {
    private final List<Item> items = new ArrayList<>();

    void add(Item item) {
        items.add(item);
    }

    @Override
    public long priceCents() {
        long total = 0;
        for (Item item : items) {
            total += item.priceCents();   // a nested Box recurses the same way
        }
        return total;
    }
}
```

**Listing 1.** Box and Product implement the same interface; the recursion lives inside the tree, not in the client.

```d2
direction: down
order: "Box (order)\npriceCents() sums" {
  width: 230
  height: 80
  style.fill: "#e3f2fd"
}
box: "Box (gift wrap)\npriceCents() sums" {
  width: 220
  height: 80
  style.fill: "#fff3e0"
}
p1: "Product\nown price" {
  width: 170
  height: 70
  style.fill: "#e8f5e9"
}
p2: "Product\nown price" {
  width: 170
  height: 70
  style.fill: "#e8f5e9"
}
p3: "Product\nown price" {
  width: 170
  height: 70
  style.fill: "#e8f5e9"
}
order -> box
order -> p1
box -> p2
box -> p3
```

**Fig. 1.** One operation name on one component interface; containers sum their children, leaves answer directly.

## The recursive-composition family

Composite and Decorator have similar diagrams because both rely on recursive composition - one object wrapping arbitrarily many others - but Decorator adds responsibilities to a single object while Composite aggregates many under one interface. The structure pairs naturally with other patterns: iterators traverse composite trees, the chain of responsibility can walk up the parent components, and shared leaf nodes can be implemented as flyweights to save memory. An operation applied over the entire tree is exactly the job of the Visitor pattern, drawn in [[How would you explain the Visitor design pattern]]. The structural sibling comparison lives in [[How would you explain the Decorator design pattern]], the traversal options in [[What is the Iterator design pattern in Java]], and the parent-walking combination in [[How would you explain the chain of responsibility design pattern]].

> [!warning] Do not force a tree onto a non-tree model
> The pattern earns its keep only when the domain is genuinely hierarchical; forcing it elsewhere yields artificial containers that nobody needs. Watch the interface trade-off too: putting child-management methods - add, remove - on the shared component means every leaf carries meaningless operations, and the design starts violating the interface-segregation instinct; moving them to the container breaks transparency, since the client must then distinguish leaves. Name your choice in an interview instead of pretending the dilemma does not exist.

> [!tip] Interview answer
> Composite builds tree structures where leaves and containers implement one component interface, and calling an operation on a container makes it recurse over its children - pricing a nested order or rendering a UI panel hierarchy is one call on the root. The client never checks concrete classes. It is recursive composition like Decorator, but for aggregating many objects; it pairs with Visitor for whole-tree operations, and its classic dilemma is whether child-management belongs on the common interface.
