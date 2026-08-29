<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Autowiring #Java/Annotations #SRS

# How do you choose among several matching beans with `@Primary` and `@Qualifier`?

> [!abstract] Short answer
> `@Autowired` still matches **by type**. If more than one bean has that type, a **single-valued** injection point fails with `NoUniqueBeanDefinitionException` unless you narrow the set. **`@Primary`** (XML `primary="true"`) picks the default when **exactly one** candidate is primary. **`@Qualifier`** (or a custom qualifier) further **filters** the type matches at that injection point. They do not replace type matching, and they do not read `application.properties`.

## Type first, then a default or a label

```d2
direction: down
type: "1. Candidates by type\n(e.g. MovieCatalog)" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
narrow: "2. Qualifier filter?" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
primary: "3. Exactly one @Primary\n(or one non-@Fallback)?" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
one: "Inject that bean" {
  width: 220
  height: 55
  style.fill: "#e8f5e9"
}
fail: "NoUniqueBeanDefinitionException" {
  width: 260
  height: 55
  style.fill: "#ffebee"
}

type -> narrow
narrow -> one: unique
narrow -> primary: still several
primary -> one: unique primary
primary -> fail: several primaries or still tied
```

**Fig. 1.** Single-valued `@Autowired` never picks arbitrarily. Qualifiers **narrow** the type set; `@Primary` / `@Fallback` then pick a default among what remains. If still several, `DefaultListableBeanFactory.determineAutowireCandidate` consults `jakarta.annotation.Priority` (lowest value wins).

Use **`@Primary`** when one implementation should win at every **unqualified** injection point of that type (for example a Hibernate repository over a JDBC one).

```java
@Bean
@Primary
public MovieCatalog firstMovieCatalog() { /* ... */ }

@Bean
public MovieCatalog secondMovieCatalog() { /* ... */ }
```

**Listing 1.** Conceptual `@Bean` pair. `MovieRecommender` with a plain `@Autowired MovieCatalog` receives `firstMovieCatalog`.

As of Spring Framework **6.2**, **`@Fallback`** marks the other beans instead: if every candidate but one is `@Fallback`, the remaining bean is effectively primary. XML equivalent of `@Primary` is `primary="true"` on `<bean>`.

Use **`@Qualifier`** when the injection point must name **which** characteristic it wants, not “whatever is default”:

```java
@Autowired
@Qualifier("main")
private MovieCatalog movieCatalog;
```

**Listing 2.** Conceptual injection point. Matching metadata is a nested `<qualifier value="main"/>`, a type-level `@Qualifier` on the candidate, or — as a **fallback** — a bean **name** / alias `main`. See [[Can Qualifier be used on a class instead of a Component name]].

`@Autowired` stays type-driven. A qualifier value, even when it happens to equal a bean id, only **narrows** the type matches. Prefer labels such as `main` or `EMEA`. For true lookup **by unique name**, use `@Resource` on a field or single-arg setter — not a constructor.

You can compose a custom annotation that is itself `@Qualifier` (`@Genre("Action")`) and match it on both the injection point and the candidate.

## When neither annotation is the whole answer

If there is **no** qualifier, primary, or fallback marker, Spring may still resolve a non-unique type by matching the **field or parameter name** to a bean name. Spring Framework **6.1+** needs the `-parameters` compiler flag for that; **6.2** adds a fast shortcut that can skip the full type-matching algorithm when the parameter name already matches a bean name. Name the parameter after the bean you want.

To use **every** implementation, inject an array, `List`/`Set`, or `Map<String, T>` (keys are bean names). `@Primary` does **not** hide extras from those multi-element points. Qualifiers on a collection **filter** (they need not be unique). See [[How do you inject all beans of a given type as a collection or map]].

> [!warning] Two primaries are still ambiguous
> `@Primary` works only if **exactly one** candidate is primary. Two `@Primary` beans of the same type throw `NoUniqueBeanDefinitionException` at a single-valued point. Class-level `@Primary` is ignored if that class is registered **in XML** — the `primary` attribute on `<bean>` wins.

> [!warning] `@Primary` cannot express “inject A here and B there”
> It only supplies a default for **unqualified** single-valued points. Injection points that must see a specific non-default bean still need `@Qualifier` (or a parameter name / `@Resource`). If you need several implementations in one class, qualify each parameter or inject a collection.

> [!warning] These annotations do not read configuration properties
> `@Primary` and `@Qualifier` are static metadata. A runtime switch (which impl a property selects) is a **factory** problem: a `@Bean` method can take `Environment` or `@Value` and return one object. That is ordinary Java config, not another qualifier.

> [!tip] Interview answer
> Autowire by type first. If several beans match, mark one @Primary for the usual injection point, and put @Qualifier on the points that must pick a specific characteristic. Qualifiers narrow the type set; they are not getBean-by-id. Collections still receive every matching bean unless you filter them.
