<!--
reps: 0
priority: 0
-->
#Java/Streams #Paradigms/Functional #Java/Versions/8 #SRS

# Which programming paradigm does the Streams API follow?

> [!abstract] Short answer
> **Functional-style, declarative aggregate processing — not an imperative element-by-element loop.** Package doc: `java.util.stream` supports **functional-style** operations such as **map-reduce** on collections. Stream JavaDoc: streams **declaratively describe** a source and the computations in aggregate (a **query** on the source). Ops are **functional in nature**: they produce a result and do not modify the source. Lambdas are `Function` / `Predicate` / `Consumer` instances. Java is still an OO language; `forEach` is an imperative escape hatch.

## Describe the query, don’t mutate the bag

Package opening: classes for **functional-style operations** on streams of elements, such as **map-reduce transformations** on collections. The widgets example is `stream` → `filter` → `mapToInt` → `sum` — what to compute, not a `for` with a mutable `total` ([[What is the Java Stream API]], [[What is Stream]]).

Stream JavaDoc contrast with collections: collections **manage and access** elements; streams do **not** give direct access or in-place manipulation. They **declaratively** describe source + aggregate ops. A pipeline “can be viewed as a **query** on the stream source” ([[What is the difference between Collection and Stream in Java]]).

Package “functional in nature”: filtering a stream from a collection produces a **new** stream, rather than removing from the source. Behavioral parameters are functional-interface instances, usually lambdas or method references, and must be non-interfering and (usually) stateless ([[Which functional interface does Stream map use]], [[What kinds of stream operations exist in Java]]).

Laziness and fusion are how that style is implemented: intermediates don’t run until a terminal ([[When does a Java stream pipeline actually start executing]]). Parallelism is the same declarative pipeline with a mode flag — a `for` loop is “inherently serial” ([[How would you explain parallel streams in Java]]). Prefer `collect` / `reduce` over mutating a list in `forEach` ([[What is the collect terminal operation in Java streams]]).

```d2
direction: down
imp: "imperative for-loop\nmutate sum / list" {
  width: 260
  height: 50
  style.fill: "#fff8e1"
}
fn: "functional-style pipeline\nfilter / map / reduce" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
```

**Fig. 1.** Same sum, two styles. The Stream API’s documented style is the lower box.

```java
import java.util.List;

class Demo {
    static int imperative(List<Widget> widgets) {
        int sum = 0;
        for (Widget w : widgets) {
            if (w.color() == Color.RED) {
                sum += w.weight();
            }
        }
        return sum;
    }

    static int declarative(List<Widget> widgets) {
        return widgets.stream()
            .filter(w -> w.color() == Color.RED)
            .mapToInt(Widget::weight)
            .sum();
    }
}
```

**Listing 1.** Package-summary widgets query vs an equivalent loop. The stream version does not mutate `widgets`.

> [!warning] “Functional-style” is not a pure functional runtime
> `forEach` / `peek` exist for side effects; those are discouraged except where specified. A stateful lambda makes results nondeterministic, especially in parallel. The API sits on objects and collections — it does not turn Java into Haskell, and it is not the reactive `Publisher`/`Subscriber` model.

> [!tip] Interview answer
> **Functional-style / declarative map-reduce** (the package’s own words): describe a query (`filter`, `map`, `reduce`/`collect`) instead of a mutating loop. Name **does not modify the source**, **lambdas as functional interfaces**, and **lazy pipeline**. Contrast with imperative `for`.
