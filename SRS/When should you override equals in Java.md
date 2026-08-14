<!--
reps: 0
priority: 0
-->
#Java/HashCodeEquals #Java/Language/Enum #Java/Language/Records #Java/Versions/16 #SRS

# When should you override `equals` in Java?

> [!abstract] Short answer
> When **distinct instances should count as the same logical value** — a coordinate, a money amount, a value object, a lookup key. Keep the inherited identity `equals` when each instance is unique (a listener, a thread, a service). If you override `equals`, override `hashCode` as well. Do not override it on an `enum`: `Enum.equals` is `final`.

## The question is semantic, not syntactic

`Object.equals` is identity. That is already a valid equivalence relation: one instance, one class. Override only when your type’s meaning is “these two copies represent the same thing.” The contract then constrains *how* that new relation must behave; it does not tell you *which* fields matter. [[How would you explain the Object equals method contract]] is the constraint. [[In a business context must equals consider all entity fields]] is a domain choice (often a stable id, not every column).

```d2
direction: down
q: "Can two instances\nbe the same value?" {
  width: 260
  height: 80
  style.fill: "#e3f2fd"
}
no: "Keep Object.equals\n(identity)" {
  width: 240
  height: 80
  style.fill: "#e8f5e9"
}
yes: "Override equals + hashCode" {
  width: 280
  height: 80
  style.fill: "#fff3e0"
}

q -> no
q -> yes
```

**Fig. 1.** Override when value equality is part of the type. Otherwise do nothing.

Typical yes: types you will put in a `HashSet` / as `HashMap` keys and look up with a **new** instance that has the same fields. Typical no: objects you always retrieve with the same reference you stored, or types whose identity *is* the instance.

A `record` already provides component `equals` and `hashCode`. An `enum` constant’s `equals` and `hashCode` are `final`; each constant is a singleton for practical purposes. Do not try to give enums value equality beyond identity.

## Cost of overriding

You must keep symmetry, transitivity, and `hashCode` in lockstep. Subclassing a value type is the usual way to break that. Prefer a final immutable class, or a record. [[Why should equals and hashCode be overridden together]] and [[How do you override equals correctly in Java]] are the follow-through. If you only needed a sort order, write a `Comparator`; that is not a reason to change `equals`.

> [!warning] “We put it in a HashMap, so we must override equals”
> Only if lookup is by **value**. If the map is `listeners.put(this, …)` and you always `get(this)`, identity is correct. Overriding `equals` on a mutable entity by every field will lose keys after an update. Overriding on a JPA entity by all columns fights the persistence identity; that policy belongs on the business card, not as a blanket “always override.”

> [!tip] Interview answer
> **Override `equals` when two different objects should be interchangeable as the same value, especially as hash-map keys. Keep identity when the instance is the identity. Then override `hashCode` too. Records already do this; enums forbid it (`equals` is final). A comparator is for order, not a substitute for this decision.**
