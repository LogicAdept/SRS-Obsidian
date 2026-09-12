<!--
reps: 0
priority: 0
-->
#Paradigms/OOP #Paradigms/Procedural #Paradigms/Functional #SRS

# What are the pros and cons of OOP versus procedural and functional programming

> [!abstract] Short answer
> The three paradigms differ mainly in **how they organize state**. **OOP** bundles state with the methods that guard it: strong modularity and invariants, substitutable designs, huge ecosystems — at the price of hidden mutable state, temporal coupling, and inheritance abuse. **Procedural** keeps data as plain structures and logic in functions: direct, cheap, fast to reason about locally — but no invariant protection, so as the code base grows, invariants scatter across every caller. **Functional** avoids mutation altogether: pure functions, referential transparency, trivially testable and concurrency-friendly — at the price of allocation, indirection, and friction against a stateful world. Java is deliberately hybrid: objects for boundaries, procedural core where it fits, lambdas/streams for transformations ([[What are the main paradigms programming]]).

## One task, three styles

The honest comparison keeps the *same* task and changes only the organization. The procedural version is a static function over records — nothing hidden, but nothing *enforced* either: any code path could double-count prices, and nothing in the type system stops it. The OO version puts the rule behind a type (`Checkout` over a `Pricing` contract) — swappable and testable, more ceremony. The functional version is a transformation expression — no intermediate mutable state at all.

```java
import java.util.List;

record Item(String name, double price) {}

public class Demo {
    static double totalProcedural(List<Item> items) {     // functions over data
        double sum = 0;
        for (Item i : items) sum += i.price();
        return sum;
    }

    interface Pricing { double total(List<Item> items); }  // behavior as a type

    static class Checkout {                                // object encapsulates the rule
        private final Pricing pricing;
        Checkout(Pricing pricing) { this.pricing = pricing; }
        double total(List<Item> items) { return pricing.total(items); }
    }

    public static void main(String[] args) {
        List<Item> cart = List.of(new Item("usb-c", 10.0), new Item("case", 5.0));

        System.out.println("procedural: " + totalProcedural(cart));

        Checkout checkout = new Checkout(items -> {        // lambda: FP-style composition
            double s = 0;
            for (Item i : items) s += i.price();
            return s;
        });
        System.out.println("oo/strategy: " + checkout.total(cart));

        double fp = cart.stream().mapToDouble(Item::price).sum();
        System.out.println("functional: " + fp);
    }
}
```

**Listing 1.** Identical totals, three contracts: a bare function, an injected strategy, a pipeline.

```text
procedural: 15.0
oo/strategy: 15.0
functional: 15.0
```

**Listing 2.** Verbatim run (JDK 21.0.12.1, sandbox `oop_5`): same answer — the paradigms differ in *who may mutate what*, not in raw capability.

## Trade-offs that actually decide designs

**Where OOP wins:** long-lived systems with many kinds of stateful things — invariants live with their state, clients depend on contracts, substitutability enables plugins and test doubles; IDE tooling, frameworks and decades of enterprise libraries reinforce it ([[What are the advantages and disadvantages of object oriented programming]]). **Where it costs:** shared mutable objects are the classic source of concurrency bugs; deep hierarchies ossify; "everything is an object" forces ceremony on genuinely data-shaped problems (that is why records were added). **Procedural wins** for algorithmic, state-transforming code — parsers, batch jobs, hot paths — and its cost is architectural: nothing prevents two modules from corrupting the same structure. **Functional wins** where reasoning about *when and who mutated* is the pain — pipelines, parallelism, tests — and costs performance on boxing/allocation and a genuinely different way of modeling I/O and state machines ([[What is OOP]]).

> [!warning] "OOP vs FP is a war" is the junior answer
> The mainstream JVM style is a blend on purpose: immutable inputs (records), pure transformations (streams), objects at the boundaries, procedural cores where allocation matters. Describing yourself as an OOP partisan *or* a functional zealot reads as inexperience; describing *which organization of state fits which problem* reads as seniority ([[What are the main paradigms programming]]).

> [!warning] Procedural is not "C is legacy"
> Structure-of-data-plus-functions is the right tool far more often than beginners admit — most service methods are procedural cores behind an OO facade. The paradigm question is not which to banish but where each one starts hurting: procedural hurts when invariants must survive many callers; OOP hurts when state is really just data; FP hurts when the domain is inherently stateful and you fight it with purity.

```d2
direction: right
state: "state?" { width: 110; height: 34 }
oop: "OOP: state owned + guarded\nby methods" { width: 240; height: 46; style.fill: "#e3f2fd" }
proc: "procedural: state in structures,\nlogic in functions" { width: 260; height: 46 }
fp: "functional: state avoided —\npure transformations" { width: 250; height: 46; style.fill: "#e8f5e9" }
state -> oop: "many stateful objects"
state -> proc: "data-centric algorithms"
state -> fp: "pipelines, no mutation"
```

**Fig. 1.** The paradigms as answers to one question — where does state live and who may touch it.

> [!tip] Interview answer
> The core difference is state organization. OOP hides state inside objects behind methods — good invariants, substitutability and ecosystems, but hidden mutation and hierarchy abuse are real costs. Procedural keeps data plain and logic in functions — direct and efficient, but nothing protects invariants as the code base grows. Functional avoids mutation with pure functions — easy to test and parallelize, but heavier on allocation and awkward with inherently stateful domains. In Java I mix them deliberately: objects at module boundaries, streams and pure functions for transformations, plain procedural code where it is the clearest — and I would argue the mix, not a single paradigm, is the modern mainstream.
