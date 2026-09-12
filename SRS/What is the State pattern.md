<!--
reps: 0
priority: 0
-->
#Patterns/GoF/Behavioral #SRS

# What is the State pattern

> [!abstract] Short answer
> State is a behavioral pattern that lets an object alter its behavior when its internal state changes: each state becomes its own class implementing a common interface, the context delegates current-state work to a state object, and transitions replace the giant conditional. The object behaves as if it changed its class.

## How the pattern works

The raw material is a finite-state machine: a document sits in Draft, Moderation, or Published, and the same method - publish - must do different things per state, with transitions predetermined. The conditional implementation picks behavior with a switch over a state field, which decays into hundreds of lines per method as states and transitions accumulate. State instead extracts each state into a class: the context holds a reference to the current state object and delegates state-dependent operations to it; state methods receive the context and can trigger transitions by swapping that reference. Behavior per state and transition rules become explicit, small classes.

```java
class Document {
    private DocumentState state = new Draft();   // current state object

    void publish(User user) {
        state.publish(this, user);               // delegation, no switch
    }

    void changeState(DocumentState next) {
        state = next;                            // transition = swap the reference
    }
}

class Draft extends DocumentState {
    @Override
    void publish(Document document, User user) {
        document.changeState(new Moderation());
    }
}

class Moderation extends DocumentState {
    @Override
    void publish(Document document, User user) {
        if (user.isAdmin()) {
            document.changeState(new Published());
        }
    }
}
```

**Listing 1.** The document's publish does different things in each state because the work lives in the state object, and the transition is just a new reference.

```d2
direction: down
draft: "Draft\npublish -> goes to moderation" {
  width: 260
  height: 80
  style.fill: "#e3f2fd"
}
mod: "Moderation\npublish -> published if admin" {
  width: 280
  height: 80
  style.fill: "#fff3e0"
}
pub: "Published\ndoes nothing" {
  width: 220
  height: 70
  style.fill: "#e8f5e9"
}
draft -> mod: transition
mod -> pub: admin only
```

**Fig. 1.** Each state is a class with its own behavior and its own transition rules; the context object just forwards and swaps.

## State, Strategy, and the conditional alternative

State and Strategy share the composition structure - context delegating to a pluggable helper - and differ in intent and wiring: strategy objects are independent and swapped by the client, while concrete states know the context and often each other's transitions, letting them alter it at will. The full comparison lives in [[What is the difference between the Strategy and State design patterns]], the strategy side in [[What is the Strategy pattern used for]], and the structural sibling with the same delegation shape in [[What is the Bridge pattern]]. Keeping the machine vocabulary explicit - states, transitions, guards - connects the pattern to the underlying model in [[How would you explain State Transition]].

> [!warning] Two costs interviewers probe
> First, the pattern does not remove the state machine - it relocates it: transition rules spread across state classes, so a hard-to-read switch can become hard-to-trace hops, and for two states with one conditional each the plain switch is simply better; reaching for State for every boolean flag is over-engineering. Second, states coupling back to the context - calling changeState from inside state methods - is by design, but it means state classes are rarely reusable outside this machine, unlike strategies.

> [!tip] Interview answer
> State replaces a conditional state machine with one class per state implementing a shared interface: the context delegates state-dependent calls to its current state object, and states trigger transitions by swapping that reference, so the object behaves as if it changed class. A document moving from Draft through Moderation to Published is the canonical example. It is structurally Strategy but with states knowing the context and each other's transitions - and I still use a plain switch when the machine has only a couple of states.
