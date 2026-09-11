<!--
reps: 0
priority: 0
-->
#Patterns/GoF #SRS

# What are the main characteristics of software design patterns

> [!abstract] Short answer
> A design pattern is a **typical solution to a commonly recurring design problem**: a general concept rather than code, described formally, classified by intent into creational, structural, and behavioral groups, and ranging in scale from language-specific idioms to whole-application architectural patterns.

## Defining characteristics

A pattern always binds a recurring problem to a proven solution core. It is a blueprint, not an off-the-shelf function: you study the shape of the solution and adapt it to your program, so two implementations of the same pattern can look quite different. Catalogs describe patterns in standard sections — intent, motivation, structure of classes, and a code example — which makes them comparable and reproducible. The classic GoF catalog classifies patterns by intent: creational patterns provide object-creation mechanisms, structural patterns explain how to assemble objects into larger structures, behavioral patterns distribute responsibilities and communication. Finally, patterns differ in scale. The most language-bound, low-level ones are called idioms; the most universal ones are architectural patterns, which can shape an entire application rather than a few classes. Concrete members of each intent group are listed in [[What are examples of behavioral design patterns]], and the case for learning the catalog at all is made in [[What are programming design patterns for]].

```d2
direction: right
idiom: "Idiom\none language,\nlow level" { width: 200; height: 100; style.fill: "#e3f2fd" }
pattern: "Design pattern\nrecurring problem,\nformal structure" { width: 230; height: 100; style.fill: "#fff3e0" }
arch: "Architectural pattern\nwhole application,\nany language" { width: 230; height: 100; style.fill: "#e8f5e9" }
idiom -> pattern -> arch: increasing scale
```

**Fig. 1.** The scale spectrum: idioms are language tricks, classic GoF patterns solve recurring class-level problems, architectural patterns shape entire systems.

## Pattern versus algorithm

People often confuse patterns with algorithms because both are known solutions to known problems. The difference is the level of description: an algorithm defines a clear set of steps that achieves a goal — like a cooking recipe — while a pattern defines participants and responsibilities — like a blueprint where you see the result, but the exact construction order is yours to choose.

> [!warning] The most common trap
> Answering "a pattern is a ready template you insert into code" fails the question. The concept, not the snippet, is the pattern: the code of the same pattern differs from program to program.

> [!tip] Interview answer
> Design patterns are typical solutions to recurring problems. They are general concepts rather than code, described in a standard format — intent, structure, examples — and grouped by intent into creational, structural, and behavioral. They also span a scale: from language-specific idioms up to architectural patterns that define whole applications.
