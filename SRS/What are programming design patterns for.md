<!--
reps: 0
priority: 0
-->
#Patterns/GoF #SRS

# What are programming design patterns for

> [!abstract] Short answer
> Design patterns give you **tried, reusable blueprints** for problems that keep coming back in software design. The two real payoffs: proven structure for recurring problems, and a **shared vocabulary** that lets a team say "use a Strategy here" instead of describing the whole idea.

## What a pattern actually gives you

A pattern is not a piece of code you plug in. It is a general concept: the same pattern implemented in two programs produces different code, adapted to each context. Learning the catalog still pays off in three ways. First, you reuse solutions that many teams have already tested, so you avoid rediscovering known trade-offs. Second, patterns define a common language: "just use a Singleton for that" transfers an entire design decision in one phrase, with no long explanation. Third, even the problems themselves teach object-oriented design — most patterns are exercises in composition, encapsulation, and programming to interfaces. The formal traits of a pattern are collected in [[What are the main characteristics of software design patterns]], and how the catalog splits them by intent is in [[How would you explain categories of design patterns creational structural behavioral]].

```d2
direction: right
problem: "Recurring\ndesign problem" { width: 220; height: 80; style.fill: "#e3f2fd" }
pattern: "Pattern\n(a blueprint)" { width: 220; height: 80; style.fill: "#fff3e0" }
solution: "Solution adapted\nto your program" { width: 240; height: 80; style.fill: "#e8f5e9" }
problem -> pattern: name it
pattern -> solution: customize
```

**Fig. 1.** A pattern sits between the problem and your implementation: it names the problem and sketches the solution shape, but you still write the actual code.

## Pattern versus library and algorithm

You cannot import a pattern the way you import a library function. A library ships finished code; a pattern ships a description of intent, structure, and trade-offs, and catalogs present it in standard sections such as intent, motivation, structure, and a code example. A pattern is also more high-level than an algorithm: an algorithm defines a concrete sequence of steps to reach a goal, while a pattern describes the participants and their responsibilities, leaving the implementation open.

> [!warning] Patterns are not ready-made code
> Treating catalog names as copy-paste snippets is the classic misuse. If a candidate says "apply Singleton" and means "paste one shared object somewhere", the vocabulary has replaced the thinking it was meant to support. See [[What are downsides of design patterns]] for where that leads.

> [!tip] Interview answer
> Design patterns are standard solutions to recurring design problems. They are useful in two ways: they give proven structures you can adapt instead of inventing your own, and they give the team a shared vocabulary, so one word like Strategy communicates a whole design. They are concepts, not code — you still adapt them to the program.
