<!--
reps: 0
priority: 0
-->
#Patterns/GoF/Behavioral #SRS

# What is the difference between the Strategy and State design patterns

> [!abstract] Short answer
> Same composition skeleton, different intent and wiring. **Strategy** swaps **algorithms**: the variants are independent, unaware of each other, and chosen by the client. **State** swaps **behavior by internal condition**: the state objects represent the context's current state, know about it, and **drive the transitions themselves**.

## Where the wiring differs

Both patterns give the context an interface, a field pointing at the helper, and delegation instead of conditionals. In Strategy the client sets the helper once — or re-sets it from outside — and the concrete strategies never reference each other; the context's behavior changes only because somebody injected a different algorithm. In State the helper is a state of the context, and the crucial catalog line is that concrete states may be aware of each other and initiate transitions: a state method typically acts and then calls `context.changeState(new NextState(...))`. That is why the pattern reads as "the object changed its class" — the same method call on the context produces different behavior depending on which state object is currently linked, and the object itself moves between states while the client keeps the same reference.

```d2
direction: right
client: "Client" { width: 130; height: 70; style.fill: "#e3f2fd" }
ctx: "Context" { width: 140; height: 70; style.fill: "#fff3e0" }
s1: "StrategyA" { width: 160; height: 70; style.fill: "#e8f5e9" }
s2: "StrategyB" { width: 160; height: 70; style.fill: "#e8f5e9" }
client -> ctx: sets strategy
ctx -> s1: delegates
ctx -> s2: delegates
```

**Fig. 1.** Strategy: the client picks the variant; strategies stay parallel and isolated.

```d2
direction: down
c: "Context" { width: 150; height: 70; style.fill: "#fff3e0" }
st1: "StateA\nchangeState()" { width: 170; height: 80; style.fill: "#e3f2fd" }
st2: "StateB\nchangeState()" { width: 170; height: 80; style.fill: "#e3f2fd" }
c -> st1: delegates
c -> st2: delegates
st1 -> st2: transitions the context
```

**Fig. 2.** State: the states know the context and hand control to each other.

## A concrete pair

For a document workflow, Strategy is choosing a rendering algorithm the user selects in settings; State is Draft, Moderation, and Published, where `publish` moves the document forward and each state decides what `publish` means next. The behaviors live in state classes, and the transition rules — which the conditional-based version scatters across `switch` statements — sit inside the states as explicit `changeState` calls. The broader behavior-family context is in [[What are examples of behavioral design patterns]], and the Strategy side alone in [[What is the Strategy pattern used for]].

> [!warning] "State is Strategy with another name" is the trap
> The observable difference is transition ownership: with Strategy the variants are parallel and silent, with State they form a graph and actively swap themselves in. If the follow-up is "how does the state machine move", answering with a client-side setter means you described Strategy, not State.

> [!tip] Interview answer
> Both delegate to a helper behind an interface. Strategy encapsulates interchangeable algorithms that know nothing about each other, and the client chooses. State encapsulates the context's current condition, states hold a backreference to the context and trigger transitions to the next state, so behavior changes from inside. Same structure, different intent — algorithms versus a state machine.
