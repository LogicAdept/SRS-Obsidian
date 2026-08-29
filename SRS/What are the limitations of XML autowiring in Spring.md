<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Autowiring #SRS

# What are the limitations of XML autowiring in Spring?

> [!abstract] Short answer
> XML `autowire` cannot fill **simple** properties (primitives, `String`, `Class`, and arrays of those) — by design. Explicit `<property>` / `<constructor-arg>` **always override** autowire. Type-based modes (`byType`, `constructor`) refuse to guess: a **second** matching bean is a fatal error for a single-valued dependency. Autowiring is **less exact** than `ref`; the graph is no longer written in the XML, which is why the default mode is `no`.

## What XML autowire will not do

The `autowire` attribute on `<bean>` has four modes: `no` (default), `byName`, `byType`, `constructor` ([[What XML autowiring modes exist in Spring]]). The container inspects the `ApplicationContext` for collaborators. Official limits of that mechanism:

**Simple values are never autowired.** Primitives, `String`, `Class`, and arrays of those need an explicit `value` (or equivalent). That is XML autowire, not `@Value`, which is a different injection path ([[How does the Value annotation inject properties]]).

**Explicit wins.** A `<property>` or `<constructor-arg>` you write always overrides whatever autowire would have done for that slot.

**Less exact than `ref`.** Collaborators are no longer documented in the XML. Tools that generate documentation from the container may not see the wiring. Mixing autowire on one or two beans in a project that is otherwise explicit is confusing. For larger deployments the docs recommend keeping the default `no` so collaborators stay visible.

**Type ambiguity is not guessed.** `byType` / `constructor` need **exactly one** bean of the argument type for a single-valued dependency. Two matches → exception (do not use `byType` for that bean). Zero matches: `byType` **leaves the property unset**; `constructor` raises a fatal error. Arrays, typed collections, and `Map<String, ?>` can take **all** matching candidates instead ([[How do you inject all beans of a given type as a collection or map]]).

When several beans share a type, options are: drop autowire and use `ref`; `autowire-candidate="false"` on types you never want injected by type; `primary="true"` on one definition; or annotation configuration (`@Autowired` / `@Primary` / `@Qualifier`) ([[How do you choose among several matching beans with Primary and Qualifier]]). `autowire-candidate="false"` does **not** block a `ref` by name; `byName` still injects a matching **name**.

```xml
<bean id="engine" class="example.GasEngine"/>
<bean id="spare" class="example.GasEngine"/>

<bean id="car" class="example.Car" autowire="byType">
    <property name="name" value="fleet-1"/>
</bean>
```

**Listing 1.** Conceptual. `name` (`String`) is **not** autowired — the `value` is required. Two `GasEngine` beans make `byType` on `Car` fail unless one is `primary` or not an autowire candidate.

```d2
direction: down
xml: "autowire=byType|constructor|byName" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
simple: "primitive / String / Class\nnever autowired" {
  width: 260
  height: 70
  style.fill: "#fce4ec"
}
explicit: "<property> / constructor-arg\noverrides autowire" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
ambig: "two beans, one type\nfatal for a single slot" {
  width: 260
  height: 70
  style.fill: "#fce4ec"
}

xml -> simple
xml -> explicit
xml -> ambig
```

**Fig. 1.** XML autowire fills **bean** collaborators only, and only when the match is unique (or a collection). Scalars and explicit `ref`/`value` sit outside that guess.

> [!warning] The second bean of the same type is the usual outage
> `byType` looks fine with one `DataSource`. Add a test or replica bean and startup dies. `byName` instead depends on the setter name matching a bean **id**. Neither mode autowires `int` or `String` — a missing `value` stays at Java defaults, which is easy to misread as “autowire failed silently.”

> [!warning] Zero matches are not the same as two
> `byType` with **no** candidate does nothing (property unset). `constructor` autowire with zero or many candidates is fatal. Do not assume “optional” from `byType` silence; an unset collaborator is a later NPE.

> [!tip] Interview answer
> XML autowire cannot inject primitives, String, or Class — you still write value. Explicit property and constructor-arg always win over autowire. byType and constructor need exactly one matching bean for a single dependency, so a second implementation blows up; collections take all matches. It is less precise than ref, which is why the default mode is no.
