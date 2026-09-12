<!--
reps: 0
priority: 0
-->
#Patterns/GRASP #Methodologies/Principles/SOLID #SRS

# What is the difference between GRASP and SOLID

> [!abstract] Short answer
> GRASP and SOLID are complementary object-design principle sets from different authors: GRASP - nine principles by Craig Larman - assigns responsibilities between objects while you design interactions; SOLID - five principles popularized by Robert C. Martin - shapes class and interface contracts around dependency management. They overlap in intent, not in wording.

## The two sets side by side

Both sets are principles rather than ready-made structures, and both aim at maintainable object-oriented designs, which is why interviews love to contrast them. The difference is where each set points your attention. GRASP is framed around a live design question - a system event arrives, a computation is needed - and answers which object should own that responsibility, with Low Coupling and High Cohesion as the evaluative yardsticks. SOLID is framed around class construction: single responsibility, open-closed extension, substitutability, interface segregation, and dependency inversion each constrain how classes and their dependencies are shaped.

| | GRASP | SOLID |
|---|---|---|
| Origin | Craig Larman, Applying UML and Patterns | principles popularized by Robert C. Martin |
| Form | nine principles, some evaluative | five principles (SRP, OCP, LSP, ISP, DIP) |
| Focus | assigning responsibilities between objects | dependency management and class contracts |
| Primary moment | while distributing behavior in a design | while defining classes and their interfaces |

## Where they map onto each other

The overlap is real but partial, and each mapping has a caveat. High Cohesion and the single responsibility principle both fight classes that do too much - but cohesion counts how related the responsibilities are, while SRP counts reasons to change; the distinction is spelled out in [[How would you explain the single responsibility principle in SOLID]]. Protected Variations and the open-closed principle both add behavior by extending behind a stable abstraction rather than editing clients, the connection drawn in [[What is the Protected Variations principle in GRASP]]. Low Coupling, Indirection, and the dependency inversion principle all push dependencies toward fewer and more stable elements; the SOLID side of that story is in [[How would you explain the Dependency Inversion Principle in SOLID]]. LSP and ISP have no dedicated GRASP counterpart - GRASP leaves substitutability and interface slimming implicit.

```d2
direction: right
grasp: "GRASP\nwho owns the responsibility\nExpert, Creator, Controller..." {
  width: 260
  height: 100
  style.fill: "#e3f2fd"
}
overlap: "Shared goals\nlow coupling, focused classes" {
  width: 240
  height: 90
  style.fill: "#fff3e0"
}
solid: "SOLID\nhow the class contract is shaped\nSRP, OCP, LSP, ISP, DIP" {
  width: 260
  height: 100
  style.fill: "#e8f5e9"
}
grasp -> overlap -> solid
```

**Fig. 1.** The sets are two lenses on one design: GRASP distributes the behavior, SOLID then shapes the contracts the distribution created.

In practice you apply them together: GRASP decides that a fabricated repository owns persistence, and SOLID checks that the repository's interface is slim, substitutable, and depended on in direction of stability. What happens when either lens is skipped is catalogued in [[What can violating SOLID principles lead to]], and the full SOLID picture stands in [[How would you explain the SOLID design principles as a set]].

> [!warning] Do not equate the overlapping pairs
> Saying "High Cohesion is just SRP" or "Protected Variations is just OCP" loses real information: a cohesive class can still have several reasons to change, and a class with one reason to change can still be incohesive. Neither set subsumes the other - they answer different questions about the same design, and an overview card like [[What is GRASP]] is the vantage point from which the mapping makes sense.

> [!tip] Interview answer
> GRASP and SOLID are complementary, not competing. GRASP - nine principles from Larman - tells me which object should own a responsibility while I distribute behavior; SOLID - five principles from Martin - constrains how the resulting classes and interfaces are shaped around dependencies. They partially map: High Cohesion meets SRP, Protected Variations meets OCP, Low Coupling meets DIP - but the pairs are not identical, and LSP and ISP have no GRASP counterpart at all.
