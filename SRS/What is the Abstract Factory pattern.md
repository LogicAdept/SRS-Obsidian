<!--
reps: 0
priority: 0
-->
#Patterns/GoF/Creational #SRS

# What is the Abstract Factory pattern

> [!abstract] Short answer
> Abstract Factory is a creational pattern that produces families of related objects without specifying their concrete classes. You declare one factory interface with a creation method per product in the family, and one concrete factory per variant, so a client that holds a factory always gets mutually matching products.

## How the pattern works

The problem it solves: your code deals with a family of related products - chair, sofa, coffee table - that comes in several variants such as Modern, Victorian, and ArtDeco, and mixing products from different variants is a bug. The solution has two moves. First, declare an interface per product type and make every variant implement it. Second, declare the abstract factory: an interface with one creation method for each product in the family, plus one concrete factory class per variant. The client works only through these interfaces, so switching the whole product family means switching the factory object - usually selected once at initialization from configuration or environment.

```java
interface Chair {
    void sitOn();
}

interface Sofa {
    void lieOn();
}

interface FurnitureFactory {            // one creation method per family member
    Chair createChair();
    Sofa createSofa();
}

record ModernChair() implements Chair {
    public void sitOn() {}
}

record ModernSofa() implements Sofa {
    public void lieOn() {}
}

class ModernFurnitureFactory implements FurnitureFactory {
    @Override
    public Chair createChair() {
        return new ModernChair();
    }

    @Override
    public Sofa createSofa() {
        return new ModernSofa();
    }
}

class OrderForm {                       // client sees only interfaces
    private final Chair chair;
    private final Sofa sofa;

    OrderForm(FurnitureFactory factory) {
        this.chair = factory.createChair();
        this.sofa = factory.createSofa();
    }
}
```

**Listing 1.** Whatever factory the client receives, the chair and sofa it gets are guaranteed to belong to the same variant.

```d2
direction: right
factory: "FurnitureFactory\ncreateChair()\ncreateSofa()" {
  width: 230
  height: 100
  style.fill: "#fff3e0"
}
modern: "ModernFurnitureFactory" {
  width: 230
  height: 70
  style.fill: "#e8f5e9"
}
victorian: "VictorianFurnitureFactory" {
  width: 240
  height: 70
  style.fill: "#ffebee"
}
client: "Client\nholds one factory" {
  width: 220
  height: 80
  style.fill: "#e3f2fd"
}
client -> factory: depends on
modern -> factory: implements
victorian -> factory: implements
```

**Fig. 1.** One factory interface per family, one concrete factory per variant; the client binds to the interface and receives only matching products.

## Family of methods, family of products

Abstract Factory classes are often built out of a set of Factory Methods - each creation method is a hook a subclass fills in. The difference in scale matters: Factory Method defers one product choice to a subclass, while Abstract Factory defers an entire consistent family, and Abstract Factory returns finished products immediately where Builder concentrates on constructing one complex object step by step. Both comparisons are drawn in [[What is the Factory Method pattern]] and [[How would you explain the Builder design pattern]]. The pattern is also a concrete realization of the creation-ownership question in [[What is the Creator principle in GRASP]], and it sits in the catalogue alongside the rest of [[What are examples of creational design patterns]].

> [!warning] Variants are cheap, new product types are not
> Adding a new variant - ArtDeco furniture - means one new factory class and done. Adding a new product type - a Table - means changing the factory interface itself and touching every existing factory and every client that uses it. That asymmetry is the pattern's real cost, so reserve it for families that are stable in membership but rich in variants. Also do not answer "just use Abstract Factory" when a single Factory Method would do: extra indirection for one product is over-engineering.

> [!tip] Interview answer
> Abstract Factory creates families of related objects without naming concrete classes: one factory interface declares a creation method per product in the family, and each variant gets its own concrete factory. A client holding a ModernFurnitureFactory can only receive matching Modern products, so variants never mix. It is typically assembled from several Factory Methods and is worth its weight when whole families must switch together - at the price of painful extension when a new product type joins the family.
