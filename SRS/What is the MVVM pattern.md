<!--
reps: 0
priority: 0
-->
#Patterns/Architecture/UI #SRS

# What is the MVVM pattern

> [!abstract] Short answer
> MVVM — Model-View-ViewModel — John Gossman's 2005 WPF pattern: an intermediary view model exposes the view's state and commands as bindable properties, and the view synchronizes via the platform's data binding — so view logic becomes testable without a UI and the glue code of MVP is automated by the binder. Standard in WPF, MAUI, Vue and (in adapted form) Angular-era frameworks.

## The mechanics: bindable state plus commands

The view model is presentation state shaped for the view: not the domain model, but its projection — flattened flags, formatted strings, enabled/disabled flags, collection views — plus commands (encapsulated actions with can-execute state). The view binds to these via the toolkit's binding system: a change in the view model's property propagates to the control, and a control's input propagates back through two-way bindings — the presenter's manual push loop from MVP, automated ([[What is the MVP pattern]] is the manual version of the same separation). The view model raises property-change notifications (`INotifyPropertyChanged` in WPF); it references the model/domain services and translates between them, but knows nothing about concrete controls — which is exactly what makes it unit-testable: construct the view model, drive commands, assert on properties, no UI required.

```d2
direction: right
u: "User" {style.fill: "#eceff1"}
v: "View
binds to VM" {style.fill: "#e3f2fd"}
vm: "View model
bindable state + commands" {style.fill: "#fff3e0"}
m: "Model
domain" {style.fill: "#e8f5e9"}
u -> v: interacts
v <-> vm: two-way data binding
vm -> m: calls, updates
m -> vm: state
```

**Fig. 1.** The binder replaces the presenter: view and view model synchronize declaratively; the view model mediates with the domain.

## Where it shines — and where binding cuts back

Strengths: designer-developer split (XAML-family views are declarative and bindable without code), testable presentation without mocks of controls (assert on the view model directly), and large forms-over-data screens stay declarative. Costs and known traps: the binder is a black box — binding errors fail silently at runtime (path typos surface as blank fields, not exceptions), which moves debugging to converter diagnostics; heavy two-way binding obscures the data flow that MVP made explicit; and view-model state can drift from domain truth when teams start "temporarily" putting business rules in the view model. The framework landscape: Gossman introduced it for WPF and it became the silverlight/WPF/MAUI standard; Knockout popularized it in JavaScript and coined the umbrella term for its own flexibility ([[What is the MVW pattern]]); React-era component models are explicitly not MVVM — unidirectional data flow replaced two-way binding there ([[What is the MVC pattern]] sketches the family tree; [[What is the MVW pattern]] records the terminology shrug).

> [!warning] A view model is not a place for domain rules
> The temptation is structural: the property is right there, the rule is one line — add the discount calculation to the view model. Every such line makes the view model the de facto business layer, untestable by domain tests and duplicated across screens. The view model formats, projects, enables and commands; invariants stay in the model — the same boundary discipline MVP enforces on its presenter.

> [!tip] Interview answer
> MVVM inserts a bindable view model between view and model: it exposes the view's state and commands as properties, the platform's data binding keeps the view synchronized — two-way where needed — and the view model mediates with the domain. I get declarative views, designer-friendly separation and view-model unit tests without any UI; the costs are silent binding failures and the discipline of keeping business rules out of the view model. It's MVP's separation with the presenter automated by the binder.
