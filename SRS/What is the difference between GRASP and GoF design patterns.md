<!--
reps: 0
priority: 0
-->
#Patterns/GRASP #Patterns/GoF #SRS

# What is the difference between GRASP and GoF design patterns

> [!abstract] Short answer
> GRASP is a set of nine responsibility-assignment principles from Craig Larman that guide who owns what during object design; the GoF catalogue is twenty-three named collaboration structures in three categories. GRASP answers "where does this responsibility go", GoF answers "which proven structure models this recurring collaboration".

## Same craft, different altitude

The two bodies of knowledge come from the same object-oriented tradition and even overlap in vocabulary - GRASP calls its items patterns or principles - but they operate at different altitudes. GRASP works at the level of decisions: you are designing interactions and must choose which object receives a responsibility. GoF works at the level of structures: a recurring problem has a named arrangement of classes and interfaces that solves it. One is the reasoning, the other is the shapes that reasoning produces.

| | GRASP | GoF |
|---|---|---|
| Origin | Craig Larman, Applying UML and Patterns | Gang of Four, Design Patterns |
| Form | nine principles for assigning responsibilities | twenty-three patterns in creational, structural, behavioral |
| Question answered | which object should own this responsibility | which structure solves this recurring collaboration problem |
| Nature | heuristics and evaluative yardsticks | ready-made class and object arrangements |
| When used | continuously, while designing interactions | when a problem matches a catalogued structure |

```d2
direction: right
p: "GRASP principles\nwho owns what" {
  width: 230
  height: 80
  style.fill: "#e3f2fd"
}
d: "Design decisions\nresponsibilities assigned" {
  width: 230
  height: 80
  style.fill: "#fff3e0"
}
g: "GoF structures\nnamed collaborations" {
  width: 230
  height: 80
  style.fill: "#e8f5e9"
}
p -> d -> g
```

**Fig. 1.** The layers stack: principles shape the decisions, and well-shaped decisions crystallize into the catalogued structures - not the other way round.

## How the two sets map onto each other

The connection is direct enough to memorize. The Polymorphism principle - pushing type-varying behavior into the varying types - is the ground the Strategy and State structures stand on, as drawn in [[What is the difference between the Strategy and State design patterns]]. Creator escalates into the creational catalogue when plain creation would hurt, which is the bridge to [[What are examples of creational design patterns]]. Indirection is instantiated by the structural shapes of Adapter, Proxy, and Facade. And Protected Variations is the broadest of all - many GoF patterns read as concrete applications of that one principle. The survey of what patterns even are supports the picture: [[What are the main characteristics of software design patterns]] and the behavioral examples in [[What are examples of behavioral design patterns]].

> [!warning] Two interview traps
> First, calling GRASP a pattern catalogue: it offers no structures to instantiate, only assignment rules and evaluative yardsticks - if you cannot name a GRASP "interface diagram", that is the point. Second, claiming one replaces the other: a GoF pattern applied against the principles still produces bad design - a controller structure stuffed with domain logic breaks the Controller principle it is named after. The principles judge the patterns you add; the patterns give the principles concrete vocabulary. Even the obvious-looking mappings deserve care, as the singleton story shows in [[How does a Spring singleton differ from the Gang of Four Singleton pattern]].

> [!tip] Interview answer
> GRASP and GoF operate at different altitudes: GRASP is nine principles for assigning responsibilities - who should own this work, how to keep coupling low - while GoF is twenty-three named structures for recurring collaboration problems. They connect directly: the Polymorphism principle grounds Strategy, Creator escalates to creational patterns, Indirection shows up as Adapter or Proxy, and Protected Variations underlies many GoF patterns. I use GRASP to reason about assignments and GoF vocabulary to name the structures that result.
