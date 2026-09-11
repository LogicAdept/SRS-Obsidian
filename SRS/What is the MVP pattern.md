<!--
reps: 0
priority: 0
-->
#Patterns/Architecture/UI #SRS

# What is the MVP pattern

> [!abstract] Short answer
> MVP — Model-View-Presenter — is Fowler's reworking of MVC for testable UIs: the view is a passive interface (no observers, no logic) and a presenter handles all input and pushes state into the view through that interface. Because the view is an interface, tests drive the presenter and assert against a mock view — presentation logic becomes unit-testable without a UI toolkit.

## The two MVP flavors and the contract

Fowler's MVP actually split into two variants he later renamed. Passive View: the view is maximally dumb — it forwards raw events (clicks, text changes) and exposes setters/getters; the presenter does literally everything else, including simple formatting. Supervising Controller: the view binds simple state directly to the model (or view model) while the presenter handles only complex input and multi-step logic — less presenter code, more coupling kept in the view. Both share the core contract: the view implements an interface the presenter depends on; the presenter has no dependency on the concrete UI. The mechanics: user event reaches the view's listener, the view delegates to the presenter, the presenter mutates the model (or calls services), then — passive view — pushes the new state back through the interface (`show(orderSummary)`), so the view never reads the model directly.

```d2
direction: right
u: "User" {style.fill: "#eceff1"}
v: "Passive view
forwards events, receives state" {style.fill: "#e3f2fd"}
p: "Presenter
all input + update logic" {style.fill: "#fff3e0"}
m: "Model" {style.fill: "#e8f5e9"}
u -> v: click
v -> p: delegate
p -> m: update
m -> p: state
p -> v: show(value)
```

**Fig. 1.** The presenter is the hub: input goes through it, state is pushed into the view — the view never observes the model.

```java
// MVP wiring: presenter pushes into the PassiveView interface
Presenter p = new Presenter(m2, new ConsolePassiveView());
p.bind(); p.click();
// console: [MVP presenter] handles click
//          [MVP passive view] presenter pushed value = 1
```

**Listing 1.** Verified on JDK 21 (G14_UiPatternsWiring in empirics): the presenter handles the click and the view only receives `presenter pushed value = 1` through its interface — no observer wiring, and the presenter is testable against any PassiveView fake (out/G14_UiPatternsWiring.txt).

## Why teams choose it — and where it hurts

The payoff is testability and toolkit independence: presentation logic (validation, enabled states, navigation decisions, formatting) lives in a plain object; unit tests construct a model, a mock view and the presenter, and assert on the pushed calls — no widget toolkit, no UI thread, no reflection magic. This made MVP the standard architecture for Swing, GWT, Android (pre-ViewModel) and WinForms teams that wanted real unit tests. The costs: interface and delegation boilerplate (every displayable property needs a view method and a presenter push — the presenter can become a giant, Fowler's warning about passive view verbosity), and anemic views that make simple screens feel over-engineered. The relationship to the family: MVC's observable model is replaced by explicit presenter pushes ([[What is the MVC pattern]]); MVVM automates those pushes with data binding ([[What is the MVVM pattern]]) — MVP is the manual, dependency-injected middle ground, which is exactly why it remains the easiest variant to test with plain JUnit ([[What is the MVW pattern]] notes frameworks that blur these lines).

> [!warning] The presenter must not become a mini-monolith
> All input and update logic in one place is the point — until one presenter owns several screens' logic, or business rules sneak in that belong to the domain layer. The boundary stays the same as in MVC: presenters orchestrate presentation; invariants and domain decisions live in the model. A presenter that computes credit eligibility is a bug, not a pattern variation.

> [!tip] Interview answer
> MVP replaces MVC's observable model with a presenter hub: the view is a passive interface that forwards events and receives pushed state; the presenter does input handling and updates, then calls back through the view interface. Because the presenter depends only on that interface, I unit-test presentation logic with a mock view — no toolkit needed. Fowler's flavors differ in how much state the view binds itself; the discipline either way is that domain rules never enter the presenter.
