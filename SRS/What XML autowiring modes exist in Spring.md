<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Autowiring #SRS

# What XML autowiring modes exist in Spring?

> [!abstract] Short answer
> XML `autowire` on `<bean>` (or `default-autowire` on `<beans>`) has **four** modes in current docs: **`no`** (default — explicit `ref` / `<constructor-arg>`), **`byName`**, **`byType`**, and **`constructor`**. Interview dumps that add **`autodetect`** are listing a **deprecated-since-3.0** strategy (`AutowireCapableBeanFactory.AUTOWIRE_AUTODETECT`: introspect the class, then pick constructor vs byType). `@Autowired` is a **separate** annotation processor, not a fifth XML mode ([[What is the difference between Autowired Resource and Inject]]).

## Four XML modes

The container can resolve collaborators by inspecting the `ApplicationContext` so you omit some `property` / `constructor-arg` entries ([[How would you explain dependency injection]]). You choose a mode **per bean**.

| Mode | What it matches | Missing / ambiguous |
| --- | --- | --- |
| `no` | Nothing. You write `ref`. | Default. Preferred for large XML. |
| `byName` | Setter property name = bean id (`setMaster` → bean `master`). | No name match → property stays unset. |
| `byType` | Exactly one bean of the setter’s type. | **Zero** matches → unset (not fatal). **Two+** → fatal for a single-valued property. |
| `constructor` | Like `byType` for **constructor arguments**. | Not exactly one bean of that argument type → **fatal**. |

`byType` / `constructor` can fill **arrays**, typed **collections**, and `Map<String, …>` (keys = bean names) with **all** matching candidates.

```xml
<beans default-autowire="no">
    <bean id="movieFinder" class="example.JpaMovieFinder"/>
    <bean id="movieLister" class="example.SimpleMovieLister" autowire="byName"/>
</beans>
```

**Listing 1.** Conceptual. `default-autowire` sets the container default; a bean’s `autowire` overrides it. No schema URLs in the snippet.

Ambiguity options from the same chapter: explicit `ref`, `autowire-candidate="false"` (type-based only — **`byName` still injects** if the id matches), or `primary="true"`. Limits of this mechanism live on [[What are the limitations of XML autowiring in Spring]].

```d2
direction: down
xml: "autowire= on bean" {
  width: 200
  height: 40
  style.fill: "#e3f2fd"
}
no: "no (explicit ref)" {
  width: 180
  height: 36
  style.fill: "#eceff1"
}
name: "byName (id = property)" {
  width: 200
  height: 36
  style.fill: "#fff3e0"
}
type: "byType / constructor" {
  width: 200
  height: 36
  style.fill: "#e8f5e9"
}

xml -> no
xml -> name
xml -> type
```

**Fig. 1.** XML autowire is a bean-definition attribute, not `@Autowired`.

> [!warning] `autodetect` is not a current XML mode
> The reference table has **four** modes. `AUTOWIRE_AUTODETECT` has been `@Deprecated(since = "3.0")` on `AutowireCapableBeanFactory`. Do not answer “five modes including autodetect” as if that were Spring Boot or Framework 6/7 XML.

> [!warning] `byType` missing vs `constructor` missing
> A setter in `byType` with **no** candidate is left **unset**. A constructor argument in `constructor` mode that is not uniquely satisfied is a **fatal** error. Zero and “too many” are not the same story.

> [!tip] Interview answer
> XML autowire has four modes: no, the default with explicit refs; byName matching the setter to a bean id; byType requiring exactly one bean of that type for a setter; and constructor, the same uniqueness rule for constructor args. Autodetect was a 3.0-deprecated introspection shortcut. Annotation @Autowired is a different mechanism.
