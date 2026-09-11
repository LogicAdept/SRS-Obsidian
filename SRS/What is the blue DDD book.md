<!--
reps: 0
priority: 0
-->
#Methodologies/DDD #SRS

# What is the blue DDD book?

> [!abstract] Short answer
> The blue book is Eric Evans' "Domain-Driven Design: Tackling Complexity in the Heart of Software", published in 2003 - "blue" from its cover, and the founding text of DDD. It introduced the vocabulary the whole discipline still uses: ubiquitous language, bounded contexts, entities, value objects, aggregates, repositories, domain services, context mapping. Its practical companion is the "red book", Vaughan Vernon's "Implementing Domain-Driven Design" (2013), which turns Evans' ideas into concrete implementation guidance.

## Why it matters

Before Evans, "domain modeling" mostly meant data modeling plus procedural services; the book's central claim is that maintainable software comes from a model of the business that lives in the code and in the team's shared language. It separates strategic design - where boundaries go, how contexts relate (context maps, partnership, anti-corruption layer) - from tactical design - the object-level patterns inside one context. The [[What is domain driven design|DDD approach]] interviewers probe (bounded contexts, [[What is ubiquitous language and why does it matter|ubiquitous language]], [[What are aggregate aggregate root entity and value object in DDD|aggregates]]) is straight out of this text.

```d2
direction: right
blue: "Blue book (Evans, 2003)\nfounding vocabulary" {
  width: 270
  height: 75
  style.fill: "#e3f2fd"
}
ref: "Blue book reference edition (Evans, 2014)\ndistilled reference" {
  width: 270
  height: 75
  style.fill: "#fff3e0"
}
red: "Red book (Vernon, 2013)\nimplementation guidance" {
  width: 270
  height: 75
  style.fill: "#fde8e8"
}
blue -> ref: "condensed into"
blue -> red: "operationalized by"
```

**Fig. 1.** The canonical shelf: the original text, its distilled reference edition, and the implementation-focused red book.

## What it does not cover

The blue book is a 2003 text: no microservices, no event sourcing as we run it today, no cloud patterns; its code examples are pre-generics Java. That is why teams usually read it for the strategic half and take tactical implementation details from later sources. Knowing this shows you actually read it rather than absorbed interview folklore - and it explains why modern practice mixes Evans' boundaries with newer integration patterns.

> [!warning] "Blue book = DDD checklist" misses the argument
> The book is often reduced to a pattern catalog, then dismissed as heavyweight when the patterns feel like overkill. The actual thesis is narrower: for complex domains, invest in the model and the language; for simple CRUD, Evans himself would skip the ceremony. Quoting aggregate rules without the modeling philosophy is the standard way teams apply DDD "by the book" and still end up with a distributed [[What is an anemic domain model and is it useful|anemic domain model]].

> [!tip] Interview answer
> The blue book is Evans' 2003 founding text of DDD - source of ubiquitous language, bounded contexts, aggregates, and context mapping. The red book is Vernon's 2013 implementation follow-up. I mention that the original predates microservices, so I apply its strategic thinking directly and its tactical patterns with modern tooling rather than copying 2003-era Java.
