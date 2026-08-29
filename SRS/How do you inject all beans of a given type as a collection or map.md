<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Autowiring #Java/Annotations #SRS

# How do you inject all beans of a given type as a collection or map?

> [!abstract] Short answer
> Annotate an **array**, a typed **`Collection`** (`List`/`Set`, …), or a **`Map<String, T>`** with `@Autowired` (or use XML `autowire="byType"` / `constructor`). The container gathers **every autowire candidate** whose type matches the **element** (map **value**) type. Map **keys are bean names**. `@Primary` does not hide extras; `@Qualifier` on the collection **filters**.

## Multi-element type matching

A single-valued `T` is unique-or-fail. A multi-element point is the opposite: several matches are the point.

```java
public class MovieRecommender {

    @Autowired
    private MovieCatalog[] movieCatalogs;

    @Autowired
    private Set<MovieCatalog> catalogSet;

    @Autowired
    private Map<String, MovieCatalog> catalogsByName;
}
```

**Listing 1.** Conceptual array, `Set`, and `Map` injection points. The array and `Set` receive every `MovieCatalog` bean. The map values are those same beans; each key is that bean’s **name**.

The map key type **must be `String`**. A `Map<Integer, MovieCatalog>` is not this “all beans of T” feature.

XML `byType` and `constructor` autowiring do the same for arrays, typed collections, and `String`-keyed maps ([[What XML autowiring modes exist in Spring]]).

```d2
direction: down
type: "Candidates of type T\n(autowire candidates)" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
qual: "@Qualifier on the point?\nfilter; need not be unique" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
build: "Array / Collection / Map<String,T>\n(+ ObjectProvider stream)" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}

type -> qual -> build
```

**Fig. 1.** Multi-element injection still starts by type. Qualifiers **narrow the set**; they do not switch the keys of a map to qualifier labels. See [[How do you choose among several matching beans with Primary and Qualifier]].

`@Primary` / `@Fallback` apply only to **single-valued** points. Arrays, collections, maps, and `ObjectProvider` streams still include **all** type matches.

A container-built array or collection is ordered by `Ordered` / `@Order` (and the reference also lists `@Priority`) on the **target beans**, otherwise by **registration order**. `@Order` on a `@Configuration` class does **not** order the `@Bean` methods inside it; put `@Order` on each factory method. `@Order` does not change singleton **startup** order (`@DependsOn` / dependency graph).

`autowireCandidate = false` (XML `autowire-candidate="false"`) drops a bean from type-based collection as well. As of **6.2**, `defaultCandidate = false` keeps it out of plain type matches unless the injection point also has a qualifier.

## Empty sets, collection beans, and names

By default a field or config-method array/collection/map is **required**: **at least one** matching element. Zero matches fail autowiring.

A **single constructor** (typical modern style) is special: multi-element arguments may resolve to **empty** instances when nothing matches, so `List<T>` in that constructor does not demand a bean of type `T`.

`@Autowired(required = false)` on a field or setter, if nothing matches, **skips** the point and leaves the field’s default (`null` for a reference) — it does not guarantee an empty `List`. That is not the same as `required = false` on a single `T` ([[What does Autowired required false do]]).

```java
@Autowired
@Qualifier("action")
private Set<MovieCatalog> actionCatalogs;
```

**Listing 2.** Conceptual. Every `MovieCatalog` whose qualifier is `action` is included. The same qualifier may appear on **several** beans; it is a **filter**, not a unique id. Map keys remain **bean names**, even if a qualifier string happens to equal a name.

If you declared a **bean whose type is** `List`/`Map`/array (a pre-built collection), `@Autowired` may inject **that bean** instead of aggregating element-typed beans. `@Resource` by unique name is the documented way to take that collection bean as-is. Preserve generics on `@Bean` return types so the element type is visible.

> [!warning] Zero beans is not “empty list” on a field
> A required `@Autowired List<T>` field with no `T` beans fails. `required = false` leaves `null`. Only the unique-constructor (and similar factory-method) path is documented to inject an **empty** collection when nothing matches.

> [!warning] `@Primary` does not shrink a `List`
> Marking one implementation `@Primary` still puts every type match into the list or map. To take a subset, qualify the collection or exclude beans with `autowireCandidate`.

> [!tip] Interview answer
> Inject an array, List or Set of T, or Map from String to T, and Spring collects every matching autowire candidate. Map keys are bean names. Primary is ignored for that; Qualifier filters the set. A required collection field needs at least one element; a single constructor may receive an empty collection.
