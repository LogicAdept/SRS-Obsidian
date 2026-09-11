<!--
reps: 0
priority: 0
-->
#Patterns/Architecture/UI #SRS

# What is the MVW pattern

> [!abstract] Short answer
> MVW — "Model-View-Whatever" — is Knockout's Steve Sanderson's deliberately open label for MVVM-style frameworks: the framework provides binding between view and view model (or presenter, or whatever intermediary a team prefers) and refuses to legislate the third letter. It records a real point: once the view is bound declaratively, MVC/MVP/MVVM blur into one family of view/state-separation patterns.

## Origin and the honest meaning

The term appeared in Knockout's documentation era: Knockout implements observable-based declarative binding — view models with observables, views binding to them — which is textbook MVVM; but Sanderson's framing was that Knockout does not care what you call the intermediary (presenter, view model, whatever), it supplies the binding mechanism. The suffix spread as a joke with a kernel of architecture theory: in bound-UI frameworks the differences between MVP's presenter and MVVM's view model reduce to who writes the synchronization — the developer (presenter pushes) or the binder (properties notify). Angular's early marketing adopted "MVW" the same way ("Angular supports Model-View-Whatever works for you"), and the term stuck as shorthand for framework-agnostic view binding.

```d2
direction: right
m: "Model" {style.fill: "#e8f5e9"}
x: "Whatever
presenter / view model / binder" {style.fill: "#fff3e0"}
v: "View" {style.fill: "#e3f2fd"}
m -> x
x <-> v: declarative binding
note: "The framework fixes the binding;
the team names the intermediary" {style.fill: "#eceff1"}
x -> note
```

**Fig. 1.** MVW keeps the model-view separation fixed and the intermediary deliberately unnamed — the binding is the framework's contract.

## The interview-relevant takeaway

As a trivia term MVW is minor; as a lens it is accurate. What frameworks like Knockout and Angular standardized is not a pattern but a mechanism: declarative binding between view and state container. On top of that mechanism a team can build MVVM (bind to view-model properties, [[What is the MVVM pattern]]), a supervising-controller MVP (bind simple state, delegate complex input, [[What is the MVP pattern]]), or even controller-ish flows ([[What is the MVC pattern]]'s family tree). The practical consequence for interviews and code review: when a candidate says "we use MVVM" about a binding framework, the meaningful questions are downstream of the label — where does input validation live, who formats, what is testable without the binder, where do business rules go. The "whatever" is exactly where the architecture decisions still live.

> [!warning] "Whatever" is not license for no architecture
> The term's humor reads sometimes as "patterns don't matter here" — the opposite of its point. Binding frameworks make it *easier* to put state and logic in views (bindables on components), which is how view-layer spaghetti accretes. The separation MVC/MVP/MVVM exist to enforce still needs an owner in code — a named state container with tested logic — whatever the third letter is called.

> [!tip] Interview answer
> MVW — Model-View-Whatever — is Steve Sanderson's open label from Knockout: the framework supplies declarative binding between view and some state intermediary and doesn't legislate whether you call it presenter, view model or anything else. The useful reading: binding frameworks standardized the mechanism, so MVP versus MVVM becomes "who writes the sync — you or the binder". I treat the label as a prompt to ask where validation, formatting and testability live — that's where the real pattern is.
