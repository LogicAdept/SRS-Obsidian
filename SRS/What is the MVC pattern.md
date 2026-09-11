<!--
reps: 0
priority: 0
-->
#Patterns/Architecture/UI #SRS

# What is the MVC pattern

> [!abstract] Short answer
> MVC — Model-View-Controller — is the original GUI architecture from Smalltalk: the Model holds state and business logic and notifies observers of changes; the View renders the model and forwards user input; the Controller interprets input and updates the model. Its enduring value is the separation of concerns it imposes; its many modern descendants (MVP, MVVM, web MVC) differ mainly in who updates the view and how input reaches the model.

## The roles and the information flow

Model: domain state plus the rules that govern it, deliberately UI-agnostic; in the classic Smalltalk form it is an observable — views subscribe to change notifications and re-read state on update. View: the presentation; it renders model state and captures user events. Controller: the input interpreter — it receives events from the view, translates them into model operations, and decides whether the view re-reads the model or the model's notification drives the refresh. Fowler's GUI-architectures analysis is precise on the dividing line: MVC splits **display from domain** (view never contains business rules) and splits input handling from both — the exact responsibilities that rot fastest when mixed.

```d2
direction: right
user: "User input" {style.fill: "#eceff1"}
v: "View
renders, captures input" {style.fill: "#e3f2fd"}
c: "Controller
interprets input" {style.fill: "#fff3e0"}
m: "Model
state + rules, notifies" {style.fill: "#e8f5e9"}
user -> v
v -> c: events
c -> m: update
m -> v: change notification
```

**Fig. 1.** Input flows view-to-controller-to-model; state changes flow back as model notifications that views observe.

```java
// MVC wiring: the view observes the model; the controller only mutates it
CounterModel m1 = new CounterModel();
new MvcView(m1);                 // view subscribes: on notify, re-reads value
new MvcController(m1);           // controller: model.increment()
// console: [MVC view] pulled value = 1
```

**Listing 1.** Verified on JDK 21 (G14_UiPatternsWiring in empirics): the controller's single `increment()` call produces the view's own `[MVC view] pulled value = 1` — the view reacted to the model notification by pulling state, and the controller never touched the view (out/G14_UiPatternsWiring.txt).

## The family tree: where modern variants diverge

The classic form has known strains: views observing models tightly couples both; complex input logic bloats controllers; testable presentation logic hides inside views. Each descendant relocates a responsibility. Web MVC (Spring MVC, Rails) reinterpreted the roles for stateless HTTP: the controller receives a request, calls domain services (the "model" broadened to application layer), and picks a view template — the observer wiring became a render step ([[What is the Front Controller pattern in Spring MVC]] is the dispatch half of that reinterpretation; [[What is the MVC pattern]]'s web form differs from Smalltalk's in exactly this). MVP moves view updates into a presenter that pushes state into a passive view interface — testability without observers ([[What is the MVP pattern]]). MVVM introduces a bindable view model so the view synchronizes by data binding ([[What is the MVVM pattern]]). MVW is the marketing shrug that its framework supports whichever you call it ([[What is the MVW pattern]]). The interview-relevant skill is not reciting the family but naming the moved responsibility per variant.

> [!warning] The word "MVC" is false friends between worlds
> Smalltalk MVC, server-side web MVC and client-side component "MVC/MVVM" share vocabulary, not mechanics — a candidate who argues that a Spring controller "must not talk to the view" is importing Smalltalk rules into a stateless template world. Always qualify which MVC you mean; the pattern is a family of related contracts, not one contract.

> [!tip] Interview answer
> MVC splits a GUI into model — state and rules, UI-agnostic and notifying observers — view, which renders and captures input, and controller, which interprets input into model updates. Its value is the display/domain separation; its descendants differ in where view updates happen: web MVC renders templates from controllers, MVP pushes into a passive view, MVVM binds through a view model. I always clarify which variant is meant — the word covers several different contracts.
