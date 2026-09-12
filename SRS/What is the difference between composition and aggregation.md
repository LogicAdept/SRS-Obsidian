<!--
reps: 0
priority: 0
-->
#Java/OOP #Paradigms/OOP #SRS

# What is the difference between composition and aggregation?

> [!abstract] Short answer
> Both are **has-a** (a field), not **is-a** (`extends`) ([[What do in OOP expressions is-a and has-a]]). **Composition** means a **part belongs to at most one whole** (exclusive ownership; interviewers also tie **lifetimes**). **Aggregation** is drawn as a weaker part-whole; in UML it has **no extra meaning** beyond a plain association unless the author defines one. Java has **neither keyword**—only references. Composition concept: [[How would you explain composition in object oriented design]]. vs inheritance: [[How does composition differ from inheritance]]. Inheritance: [[What is inheritance]].

## Exclusive part vs a shared link

**Association** is “these objects are connected,” usually a field ([[What is constructor]] to inject or construct the other object). **Composition** and **aggregation** are the part–whole stories people draw on that link.

**Composition (filled diamond in UML).** A given part instance is in **one** composite at a time (a menu bar is not owned by two windows). The dump’s book/pages picture: you do not rip a `Page` into another `Book`. In Java that is a **convention**: construct the parts **inside** the whole, keep the field `private`, do not publish a setter that lets a second owner store the same instance. When the `Book` becomes unreachable, its `Page` array is too—unless you leaked a page reference ([[How would you explain problems with public mutable fields in Java]]; [[What is encapsulation]]).

**Aggregation (hollow diamond).** The dump’s library/book: the same `Book` can move between libraries; it is not created solely for one library. In Java: a field that **holds a reference you did not exclusively create**, often passed into the constructor. UML **aggregation itself does not add rules**—treat it as a labeled association and ask what “shared” means on that diagram.

**Not inheritance.** `Car extends Engine` is the wrong tool if a car **has** an engine ([[How would you explain class inheritance in Java and tradeoffs]]). Prefer a field.

```d2
direction: down
comp: "composition\npart owned by one whole" {
  width: 280
  height: 45
  style.fill: "#e8f5e9"
}
agg: "aggregation\nshared reference, no extra Java rule" {
  width: 320
  height: 45
  style.fill: "#e3f2fd"
}
```

**Fig. 1.** Interview diamond: exclusive vs shared. The compiler only sees fields.

```java
class Page {
    final int number;

    Page(int number) {
        this.number = number;
    }
}

class Book {
    private final Page[] pages;

    Book(int count) {
        pages = new Page[count];
        for (int i = 0; i < count; i++) {
            pages[i] = new Page(i);
        }
    }
}

class Library {
    private final java.util.List<Book> books = new java.util.ArrayList<>();

    void add(Book book) {
        books.add(book);
    }
}
```

**Listing 1.** `Book` **composes** `Page` instances it constructs. `Library` **aggregates** `Book` references it is given. `add` can move the same book between libraries; pages stay inside one book unless you leak `pages`.

> [!warning] Java does not implement UML diamonds
> `private final Engine engine` is not automatically composition. If two cars store the same `Engine` instance, you modeled aggregation (or a bug). GC does not “delete the engine when the car dies” if another reference remains.

> [!warning] Aggregation is a modeling placebo
> Hollow-diamond aggregation has **no standard semantics** beyond association. If a slide says aggregation, ask whether they mean **shared lifetime** or just **has-a**. Do not invent a third Java construct.

> [!warning] DDD “aggregate” is a different word
> A domain aggregate (order + lines, one root) is not UML aggregation. Do not mix the two in an answer.

> [!tip] Interview answer
> Composition and aggregation are both has-a, implemented in Java as fields. Composition means exclusive ownership: the part is not shared by another whole, often created inside the owner. Aggregation means a shared or independent part—the same object can be referenced from several places. UML aggregation adds no extra language rule; composition’s exclusive-part rule is the one that actually means something.
