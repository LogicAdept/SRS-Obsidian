<!--
reps: 0
priority: 0
-->
#Java/OOP #DataAndState/Objects #Patterns/Enterprise #SRS

# How would you explain the term plain old Java object POJO?

> [!abstract] Short answer
> **POJO** means **Plain Old Java Object**: an **ordinary Java class**, not a special component type. The name was coined so that **regular objects holding business logic** would sound as legitimate as **Entity Beans**. It is **not** a language keyword, **not** a type in the JDK, and **not** “fields plus getters and setters.” A DTO can be a POJO ([[How would you explain DTO]]); a JPA `@Entity` is still a class ([[How would you explain DTO Entity]]). Class vs object: [[How would you explain main concepts OOP class object interface]].

## A fancy name for a normal class

The term is marketing for **Java types that follow the language**, not a framework component model. In 2000 the contrast was **EJB 2 Entity Beans** (home/remote interfaces, container callbacks, a heavy programming model) versus **encoding domain logic in ordinary classes**. Nothing in the language changed: you already had classes, fields, constructors, and methods ([[How would you explain encapsulation in object oriented design]]).

**What interviewers usually mean.** The class does not have to **extend** a framework base type or **implement** a framework interface in order to exist. You can `new` it in a unit test without a container. Persistence, remoting, or JSON mapping—if used—are **outside** the object, or later annotations that you could strip and still have a valid class.

**What it does not mean.** JavaBeans (`Serializable`, no-arg constructor, `getX`/`setX`) are a **separate** convention. An immutable `Money` with behavior is a POJO. A public-field struct is a POJO and a bad one ([[How would you explain problems with public mutable fields in Java]]). `record` types are still “plain” objects. Spring/JPA types are often still called POJOs because they are classes first; they are **not** POJOs if they only work as subclasses of a vendor base class.

```d2
direction: down
ejb: "EJB 2 entity bean\ncontainer types, callbacks" {
  width: 280
  height: 45
  style.fill: "#ffebee"
}
pojo: "POJO\nordinary class, domain logic" {
  width: 280
  height: 45
  style.fill: "#e8f5e9"
}
```

**Fig. 1.** The term exists to name the right-hand box. It is not a third kind of type beside class and interface.

```java
class Money {
    private final int cents;

    Money(int cents) {
        this.cents = cents;
    }

    Money plus(Money other) {
        return new Money(this.cents + other.cents);
    }

    int cents() {
        return cents;
    }
}
```

**Listing 1.** A POJO: a class the compiler already understands. No getters-and-setters requirement, no framework supertype.

> [!warning] POJO ≠ JavaBean ≠ DTO
> Getters, setters, and a no-arg constructor are **JavaBean** rules (and convenient for some mappers). A **DTO** is a **role** (data across a process boundary). A class can be all three, one, or none of the extra labels. Calling every anemic setter bag a “POJO” is the dump’s mistake.

> [!warning] There is no `extends POJO` and no JLS section
> If a framework requires you to extend `SpecialEntity`, that instance is not “plain.” Annotations on an otherwise ordinary class are a gray area: the **idea** was the object still makes sense with the annotations removed.

> [!warning] “POJO” does not mean “no behavior”
> The original pitch was to put **business logic** in regular objects instead of leaving them as dumb bags for a container. Anemic getters-only types are POJOs in the weak sense and miss the point.

> [!tip] Interview answer
> POJO is Plain Old Java Object: a normal class used for domain logic, named that way to contrast with heavy component models such as EJB 2 Entity Beans. It is not a JDK type and it does not require getters, setters, or a no-arg constructor. A DTO or a JPA entity might be implemented as a POJO; JavaBean is a stricter property convention on top.
