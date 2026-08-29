<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Autowiring #Java/Annotations #SRS

# What is the difference between Autowired Resource and Inject?

> [!abstract] Short answer
> All three inject a collaborator, but **matching is not the same**. `@Autowired` (Spring) and `@Inject` (`jakarta.inject`, JSR-330) are **type-first**: pick candidates by type, then narrow with `@Qualifier` / `@Named` (or, if still ambiguous, the injection-point name). `@Resource` (`jakarta.annotation`, JSR-250) is **name-first**: `name` or the field/setter property name identifies a unique bean; the declared type is **irrelevant** to matching. `@Autowired(required = false)` is Spring-only; `@Inject` has **no** `required` (use `Optional` / `@Nullable`). `@Resource` is **fields and single-arg setters only** — not constructors or multi-arg methods.

## Three annotations, two matching models

`@Autowired` and `@Inject` are handled by `AutowiredAnnotationBeanPostProcessor`. `@Resource` is handled by `CommonAnnotationBeanPostProcessor`. `context:annotation-config` / component scanning registers both ([[What does context annotation-config register]]). None of them work on your own `BeanPostProcessor` / `BeanFactoryPostProcessor` types.

**`@Autowired`** — Spring. Fields, constructors, multi-arg methods, parameters. Type matching, then `@Qualifier` (semantic label among **already type-selected** beans — not “this unique id”). Fallback: bean name as qualifier; since 6.1, parameter/field name vs bean name / alias when there is no other indicator (`-parameters` needed). `required` default `true`; `false` skips that injection point ([[What does Autowired required false do]]). Well-known types (`ApplicationContext`, `BeanFactory`, …) inject without a matching user bean ([[Which well-known types can Autowired inject without a matching bean]]).

**`@Inject`** — drop-in **alternative** at field / method / constructor. Same type-first story. Qualifier via `@Named("main")` or a custom annotation meta-annotated with `jakarta.inject.Qualifier`. No `required`; use `Optional`, `@Nullable`, or Kotlin `?`. `Provider<T>` is the JSR-330 `ObjectProvider` analogue (`get()`). JSR-330 `@Named` is also a `@Component` stand-in but is **not composable**. A JSR-330 bean in Spring is still a **singleton by default** (the spec’s default is prototype-like; Spring does not follow that).

**`@Resource`** — by-name. `name="myMovieFinder"` or, if omitted, field name / setter property name. Only if **no explicit name**: look up that default name, then **primary type** match, plus the same well-known resolvable types as `@Autowired`. Use it when you mean a **unique bean id** (including a named `List`/`Map` bean). Do **not** use `@Autowired` + `@Qualifier` as your primary “inject by id” tool.

```java
public class MovieRecommender {

    @Autowired
    @Qualifier("main")
    private MovieCatalog movieCatalog;

    @Inject
    public void setFinder(@Named("main") MovieFinder movieFinder) {
        this.movieFinder = movieFinder;
    }

    @Resource(name = "myMovieFinder")
    public void setNamedFinder(MovieFinder namedFinder) {
        this.namedFinder = namedFinder;
    }
}
```

**Listing 1.** Conceptual. Type + qualifier (`@Autowired` / `@Inject`) vs unique name (`@Resource`).

```d2
direction: down
aw: "@Autowired / @Inject\ntype → qualifier → name fallback" {
  width: 300
  height: 60
  style.fill: "#e3f2fd"
}
rs: "@Resource\nunique name (type ignored)" {
  width: 280
  height: 55
  style.fill: "#fff3e0"
}
opt: "optional?\n@Autowired required=false\n@Inject: Optional / @Nullable" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}

aw -> opt
```

**Fig. 1.** Same container; different matching and optionality.

> [!warning] `@Resource` cannot target a constructor
> Only fields and single-argument setters. Constructor or multi-arg factory method → `@Autowired` / `@Inject` plus qualifiers.

> [!warning] Spring `@Qualifier` is not `@Resource` matching
> `@Qualifier` filters **type** candidates. Putting Spring `@Qualifier` next to `@Resource` does not turn `@Resource` into that algorithm. For a unique id, set `@Resource(name = "…")` (or the field name).

> [!tip] Interview answer
> Autowired and Inject resolve by type, then qualifier; Inject is the JSR-330 twin without required. Resource is JSR-250 name lookup on a field or setter, and the type is not used to choose the bean. Use Resource when you mean a specific bean name; use Autowired or Inject for constructors and type-based wiring.
