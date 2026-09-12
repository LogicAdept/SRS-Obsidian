<!--
reps: 0
priority: 0
-->
#Methodologies/DDD #SRS

# What is knowledge crunching in DDD?

> [!abstract] Short answer
> Knowledge crunching is the collaborative modeling loop where developers and domain experts chew through a problem together: walking through concrete scenarios, questioning every term, sketching, and rapidly testing ideas against code - until a distilled model with a shared vocabulary falls out. It is the activity that produces the domain model; the model is not handed to developers in a document, it is forged in this loop.

## The loop

The crunching session starts from raw material - existing documents, expert stories, edge cases, incident reports. Experts throw facts; developers push back with contradictions the facts imply ("if a cancelled order keeps its number, can two orders share a number?"); the group tries alternative models on the spot. The key discipline is rapid feedback: promising ideas get expressed in code or in runnable behavior examples almost immediately, because prose hides model defects that a unit test exposes the same afternoon. The output of a crunching cycle is not a stack of diagrams - it is a sharpened [[What is a domain model]] and a sharpened [[What is ubiquitous language and why does it matter]], both of which changed since yesterday.

Iteration is not a bug of the process but its engine. The first model is wrong in ways nobody can articulate yet; each pass through expert scenarios discards a concept, merges two others, or renames one - and the vocabulary shifts with every such change. A model that stops changing for weeks is usually a model that stopped being tested against reality, not one that is finally correct.

```java
// A crunching artifact: the model expressed as a test a domain expert can read.
Order order = Order.place(100, "EUR");
order.addLine(new Money(2500, "EUR"));
assert order.status() == Status.OPEN;          // placed but not paid yet
order.cancel("customer changed mind");
assert order.status() == Status.CANCELLED;
```

**Listing 1.** Conceptual. A behavior example from a crunching session: the expert confirms the rule that an open order can be cancelled, and the same line as a runnable test rejects the model if the rule was misunderstood.

```d2
direction: right
experts: "Domain experts\nfacts, scenarios, edge cases" {
  width: 240
  height: 90
  style.fill: "#e3f2fd"
}
devs: "Developers\ncontradictions, options, code" {
  width: 240
  height: 90
  style.fill: "#fff3e0"
}
model: "Distilled model\n+ ubiquitous language" {
  width: 240
  height: 90
  style.fill: "#e8f5e9"
}
code: "Runnable examples\nand fast tests" {
  width: 220
  height: 90
  style.fill: "#f3e5f5"
}
experts -> devs: "stories"
devs -> experts: "questions"
devs -> model: "shape"
model -> code: "express"
code -> experts: "feedback"
```

**Fig. 1.** Knowledge crunching cycles between experts, developers, model, and code until the vocabulary and the code agree.

## Why documents do not replace it

A requirements document written by experts alone encodes their misunderstandings as certainty, and nobody is present to challenge them. Crunching forces the misunderstandings to the surface while they are still cheap, because two professions with different instincts are in the same room arguing about the same sentence. It also spreads model ownership: after crunching, both sides can defend the model to their own colleagues, which is what keeps the language alive in later conversations. This is also the practical answer to where the tactical patterns come from - aggregates and value objects are discovered here, not imposed afterwards ([[What are aggregate aggregate root entity and value object in DDD]]).

> [!warning] The handoff trap
> The classic failure is the waterfall handoff: analysts interview experts, write specs, and hand them to developers who "implement the model" without ever meeting an expert. Nothing crunches, so the model is really just a data-entry form schema. The opposite failure looks similar from outside - meetings happen, but nobody writes behavior examples, so nothing falsifies the model either. Crunching without code is a discussion; code without crunching is a guess.

> [!tip] Interview answer
> Knowledge crunching is DDD's name for collaborative modeling: developers and domain experts iterate over scenarios, documents, and edge cases together, express candidate models in quickly runnable code, and distill both the model and the ubiquitous language out of that loop. It matters because a domain model cannot be handed over - it has to be forged by people who both understand the business and can test an idea in code.

