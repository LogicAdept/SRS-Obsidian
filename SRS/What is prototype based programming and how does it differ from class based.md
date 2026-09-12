<!--
reps: 0
priority: 0
-->
#Paradigms/OOP #ProgrammingLanguages #SRS

# What is prototype based programming and how does it differ from class based?

> [!abstract] Short answer
> **Class-based** (Java): the class is the template; instances are produced by constructors and share structure through a fixed class chain. **Prototype-based** (Self, 1987; JavaScript): there are only **objects**; new ones are created by **cloning** an existing object and overriding selected members, and behavior is shared by **delegation** up a prototype chain resolved at run time. The concepts map loosely — cloning stands in for instantiation, delegation for inheritance — but the machinery differs fundamentally: nothing is fixed at compile time.

## Class-based mechanics

In Java, member layout and which method overrides which are settled by the class declarations long before any object exists; dispatch walks the class chain of the receiver ([[What is the difference between static and dynamic binding in Java]]). Classes are also **types**: assignment compatibility is decided by the declaration (`implements`, `extends`), not by the object's shape. The hierarchy is a closed, compiler-checked structure — the property the whole nominal-type safety story rests on ([[What is the difference between subtyping and inheritance]]).

## Prototype mechanics

In a prototype language, an object literal *is* a complete object; a "subclass" is made by linking a new object's internal prototype slot to an exemplar. Property lookup walks that chain **at run time**, and the chain is mutable — repointing or extending a prototype changes the behavior of every dependent object instantly, including ones already created. There is no class/type distinction: an object is simultaneously instance and template. JavaScript's `class` keyword is syntax over this machinery — behind it remain objects, slots, and delegation, which is why a JS class can be extended at run time and methods can be patched onto prototypes ([[What is polymorphism]] — the shape-based dispatch remains, but it is resolved dynamically against object structure).

## What transfers and what does not

The pillars translate: encapsulation via closures and private slots, polymorphism via shared shapes, reuse via delegation. What does not transfer: static typing, compile-time override checks, and the class-as-type contract — prototype systems trade exactly those for runtime mutability. Java adjacency is thin and often confused: `Cloneable` copies objects but builds no delegation; Spring's "prototype scope" is a **bean lifecycle policy** (a fresh instance per injection point), unrelated to the programming paradigm ([[What is the difference between the Singleton and Prototype design patterns]]).

```d2
direction: right
cls: "class-based\nAnimal -> Dog (fixed, typed)" {
  width: 260
  height: 64
  style.fill: "#e3f2fd"
}
inst: "new Dog()\ndispatch: class chain" {
  width: 220
  height: 56
  style.fill: "#e8f5e9"
}
proto: "prototype-based\nproto = { speak() }\nobj = clone(proto) + overrides" {
  width: 280
  height: 64
  style.fill: "#fff3e0"
}
deleg: "obj.speak()\ndelegation chain, resolved at run time" {
  width: 280
  height: 64
  style.fill: "#fff8e1"
}
cls -> inst: "constructs"
proto -> deleg: "delegates"
```

**Fig. 1.** Construction from a typed template versus delegation along a mutable object chain.

```javascript
// prototype-based (JavaScript): objects clone and delegate
const greeter = {
    greet: () => "hello",
};
const formal = Object.create(greeter);        // clone with delegation link
formal.greet = () => "good evening";          // override on the clone
formal.greet();                               // "good evening"  (own member)
delete formal.greet;
formal.greet();                               // "hello"  (delegated again)
```

**Listing 1.** Conceptual. Deleting the override silently falls back to the prototype — structure is data, editable at run time; a Java class offers no such move ([[What is inheritance]]).

> [!warning] "JavaScript classes changed the object model" is false
> `class` is sugar: lookup still walks prototype chains, prototypes stay mutable at run time, and `Object.create` builds the same objects without the keyword. Confusing Java-style class semantics with JS syntax sugar breaks exactly when deletion, patching, or chain re-pointing shows up. And Spring's "prototype" scope belongs to bean lifecycles, not to this paradigm ([[What is the difference between the Singleton and Prototype design patterns]]).

> [!tip] Interview answer
> Class-based: classes are the templates, instances are constructed, and dispatch follows a fixed, compiler-checked class chain. Prototype-based: only objects exist — new ones clone an exemplar and delegate lookups up a mutable chain resolved at run time; JavaScript's `class` is sugar over that. Same pillars, different machinery: delegation replaces inheritance, cloning replaces construction, and structure becomes run-time data.
