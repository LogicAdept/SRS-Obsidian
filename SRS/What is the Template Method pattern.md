<!--
reps: 0
priority: 0
-->
#Patterns/GoF/Behavioral #SRS

# What is the Template Method pattern

> [!abstract] Short answer
> Template Method is a behavioral pattern that defines the skeleton of an algorithm in a superclass and lets subclasses override specific steps without changing the algorithm's structure. One final template method calls the steps in a fixed order; subclasses supply the varying steps.

## How the pattern works

The trigger is duplicated algorithm structure across subclasses: three data-mining classes for DOC, CSV, and PDF share the same pipeline - open the file, extract data, analyze, compose the report - and differ only in the parsing steps. Template Method hoists the shared skeleton into a base class: the template method is a single method calling the steps in order, marked final or protected so its structure cannot drift. Steps become methods of their own - abstract when every subclass must supply them, default when most share one implementation. Clients instantiate a concrete subclass and call the template method; the variation happens inside the step overrides.

```java
abstract class DataMiner {
    final Report mine(String path) {            // template method: fixed skeleton
        String raw = openFile(path);            // step: varies by format
        Object data = extractData(raw);         // step: varies by format
        Analysis analysis = analyze(data);      // step: shared
        return composeReport(analysis);         // step: shared
    }

    protected abstract String openFile(String path);

    protected abstract Object extractData(String raw);

    private Analysis analyze(Object data) {
        return new Analysis(data);
    }

    private Report composeReport(Analysis analysis) {
        return new Report(analysis);
    }
}

class PdfMiner extends DataMiner {
    @Override
    protected String openFile(String path) {
        return "pdf:" + path;
    }

    @Override
    protected Object extractData(String raw) {
        return raw;                              // pdf-specific extraction
    }
}
```

**Listing 1.** Conceptual pipeline: the `final` template method pins the order of steps; the subclass overrides only the format-specific ones.

```d2
direction: down
t: "DataMiner.mine(path)\nopenFile -> extractData -> analyze -> report" {
  width: 380
  height: 90
  style.fill: "#fff3e0"
}
a: "openFile / extractData\nabstract: subclass supplies" {
  width: 300
  height: 80
  style.fill: "#e3f2fd"
}
b: "analyze / composeReport\nshared in base class" {
  width: 290
  height: 80
  style.fill: "#e8f5e9"
}
t -> a
t -> b
```

**Fig. 1.** The skeleton belongs to the base class; only the marked steps are hooks, so every miner runs the same pipeline in the same order.

## Inheritance-based variation - and its price

Template Method works at the class level through inheritance, which makes it static: which variation runs is fixed at instantiation time, unlike Strategy, which swaps behavior per object at runtime through composition - the comparison drawn in [[What is the Strategy pattern used for]]. The factory method pattern is a specialization of this one, and a factory method can serve as one overridable step inside a larger template method; both are traced in [[What is the Factory Method pattern]]. Because the algorithm lives in a superclass that subclasses reach into, the pattern leans on the base class being designed for extension - exactly the territory of [[What is the fragile base class problem]]. Among [[What are examples of behavioral design patterns]] it is the standard answer for "same pipeline, varying steps".

> [!warning] The skeleton is only as safe as the base class
> Overriding a step requires understanding the base class's calling order - change the skeleton and every subclass silently breaks, which is the fragile base class cost in its purest form. Step contracts must also survive Liskov-style scrutiny: a subclass step that skips side effects the skeleton depends on corrupts the pipeline while still compiling. That is why the template method is marked final, hooks are kept few, and frameworks expose callback hooks instead of raw inheritance when third parties must extend.

> [!tip] Interview answer
> Template Method pins the algorithm skeleton in a base class - one final method calling the steps in order - and subclasses override only the varying steps, like openFile and extractData for DOC, CSV, and PDF miners sharing one pipeline. It is inheritance-based, so variation is fixed per class rather than swappable at runtime like Strategy, and its real cost is the fragile base class: the skeleton and step contracts must be designed for extension up front.
