<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Lifecycle #SRS

# In what order does Spring initialize a bean and its dependencies?

> [!abstract] Short answer
> **Collaborators first, then the bean that needs them.** If A depends on B and there is **no** cycle, the container **fully configures B** (instantiate, inject B’s deps, run B’s init callbacks) **before** it injects B into A. Then A finishes: remaining properties, **`Aware`**, **`@PostConstruct` → `InitializingBean.afterPropertiesSet()` → `init-method`**, then **`postProcessAfterInitialization`** (AOP proxy). Eager singletons run during `refresh()` / `preInstantiateSingletons`. **`@DependsOn`** only adds order when there is **no** injection edge. **`@Order` does not** control singleton startup. A circular setter/field injection can see a bean that is **not** finished ([[How does Spring resolve circular dependencies]]).

## Dependencies are created inside `createBean`, not “later”

The DI chapter’s rule: with **no** circular dependencies, each collaborator is **totally configured** before it is injected. For setter injection that means: instantiate A, then **before** `setB`, finish B (including `InitializingBean` / `init-method`). Constructor injection is stricter: **B’s constructor and init must complete** so a finished B can be passed into `new A(b)`.

```d2
direction: down
Bnew: "instantiate B"
Binit: "B: inject → Aware → @PostConstruct\n→ afterPropertiesSet → init-method"
Anew: "instantiate A (ctor gets B)"
Ainit: "A: remaining inject → Aware → init"
Bnew -> Binit -> Anew -> Ainit
```

**Fig. 1.** A’s constructor body runs **after** B is a finished singleton (no cycle). Independent singletons follow **definition registration** order when `preInstantiateSingletons` walks names; a **dependency** still pulls the collaborator forward.

`@Autowired` / constructor / `<property>` already imply this. **`@DependsOn("b")`** is for **side effects** with **no** `ref` (static init, driver registration) and, for singletons, also **destroy** order ([[What is the DependsOn annotation in Spring]]).

```java
@Component
public class Beta {
	@PostConstruct
	void ready() { /* runs before Alpha is constructed */ }
}

@Component
public class Alpha {
	public Alpha(Beta beta) { /* beta is fully initialized */ }
}
```

**Listing 1.** Constructor injection: `Beta`’s init callbacks complete before `Alpha`’s constructor runs.

## Order *inside* one bean (after its deps are in)

Once the instance exists and properties are set ([[In what order do PostConstruct InitializingBean and init-method run]]):

1. Instantiation (constructor / factory / `FactoryBean.getObject()` — the **factory bean** itself is created first).
2. Populate remaining injection points.
3. `BeanNameAware` / `BeanFactoryAware` / `ApplicationContextAware` / other `Aware`.
4. `BeanPostProcessor.postProcessBeforeInitialization` (this is where `@PostConstruct` runs).
5. `InitializingBean.afterPropertiesSet()`, then custom `init-method` / `@Bean(initMethod)`.
6. `postProcessAfterInitialization` — may **replace** the instance with an AOP proxy.

Init callbacks run on the **raw** target; interceptors are not on yet.

`@Lazy` on a dependency **defers** that collaborator until first use (or until an eager bean still requires it). `@Order` / `Ordered` sort **lists** of the same type; they **do not** choose singleton **startup** order — that is **dependency graph + `@DependsOn`**.

## After all singletons exist

`finishRefresh` then runs `LifecycleProcessor.onRefresh()` (`Lifecycle` / `SmartLifecycle.start()`). That is **container** startup, **not** a substitute for `@PostConstruct` on an ordinary bean.

> [!warning] Cycles break “fully configured first”
> Setter/field cycles (when allowed) inject an **early** singleton: properties and init on that object may **not** have run. Using it from the other bean’s constructor or `@PostConstruct` is unsafe. Constructor cycles never get that shortcut (`BeanCurrentlyInCreationException`).

> [!tip] Interview answer
> Spring initializes **dependencies completely** (including their init methods) **before** injecting them, then initializes **this** bean: inject → Aware → `@PostConstruct` → `afterPropertiesSet` → `init-method` → after-init / proxy. `@DependsOn` for side effects; `@Order` is not startup order.
