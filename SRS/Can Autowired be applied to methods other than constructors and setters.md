<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Autowiring #Java/Annotations #SRS

# Can Autowired be applied to methods other than constructors and setters?

> [!abstract] Short answer
> **Yes.** `@Autowired` (since **2.5**) applies to **constructors**, **fields**, **setter methods**, **any other method** (arbitrary name, one or many arguments — a “config method”), and **parameters**. `AutowiredAnnotationBeanPostProcessor` injects those points. `@Resource` does **not**: it is **fields and single-arg setters only** ([[What is the difference between Autowired Resource and Inject]]).

## Config methods are first-class

The reference shows a method that is **not** a JavaBean setter. The container still calls it while **populating** the bean (after construction) and supplies each argument from the context by type (then qualifiers), same as a setter:

```java
public class MovieRecommender {

    private MovieCatalog movieCatalog;
    private CustomerPreferenceDao customerPreferenceDao;

    @Autowired
    public void prepare(MovieCatalog movieCatalog,
            CustomerPreferenceDao customerPreferenceDao) {
        this.movieCatalog = movieCatalog;
        this.customerPreferenceDao = customerPreferenceDao;
    }
}
```

**Listing 1.** From the Framework autowiring chapter. `prepare` is a config method: any name, multiple collaborators in one call.

You can **mix** constructor injection, field injection, and config methods on the same type. A **single** constructor does not need `@Autowired` at all ([[Why is Autowired often omitted on a single constructor in modern Spring]]). Extra constructors: mark the one to use (or use a primary/default constructor per the resolution rules).

`required` on a **method** applies to **the whole method**: if any argument cannot be satisfied and `required` is `false`, Spring **does not invoke** the method ([[What does Autowired required false do]]). Default `required = true` fails startup instead.

Do **not** put `@Autowired` on your own `BeanPostProcessor` / `BeanFactoryPostProcessor` types — those processors are not applied to themselves; wire them in XML or with `@Bean`.

```d2
direction: down
ctor: "constructor\n(create instance)" {
  width: 200
  height: 45
  style.fill: "#e3f2fd"
}
pop: "populateBean" {
  width: 160
  height: 36
  style.fill: "#fff3e0"
}
cfg: "@Autowired config method\n(any name, N args)" {
  width: 240
  height: 50
  style.fill: "#e8f5e9"
}

ctor -> pop
pop -> cfg
```

**Fig. 1.** Constructors run at instantiation; setters and other `@Autowired` methods run during property population.

> [!warning] Not `@Resource`, not a random later call
> `@Resource` cannot annotate `prepare(A, B)`. `@Autowired` on a config method is **container lifecycle**, not something you call from business code to “look up beans again.”

> [!warning] Multi-arg `required = false` is all-or-nothing
> One missing collaborator skips **every** argument. Use `Optional` / `@Nullable` on a **parameter** when only one argument is optional.

> [!tip] Interview answer
> Yes — Autowired is not limited to constructors and setters. Spring documents config methods with arbitrary names and multiple arguments, plus fields and parameters. The processor injects them after construction. Resource cannot do that; it is name-based fields and single-arg setters only.
