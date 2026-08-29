<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC #Java/Spring/Boot/Properties #SRS

# How does Spring resolve circular dependencies?

> [!abstract] Short answer
> A **cycle** is A needing B and B needing A (or a longer loop, or a bean needing **itself**). **Constructor** injection of that cycle is **unresolvable**: the container throws **`BeanCurrentlyInCreationException`**. If circular references are **allowed**, Spring can finish a **setter/field** cycle by injecting an **early reference** to a singleton that is **not fully initialized** yet (`getEarlyBeanReference`). That is **not recommended**. Framework `AbstractAutowireCapableBeanFactory` defaults **allow** it (`true`); **Boot 2.6+** turns it **off** (`spring.main.allow-circular-references` default **`false`**). Prefer a **third bean**, or `@Lazy` / `ObjectProvider` so nobody needs the unfinished instance. **AOT** still fails on explicit setter/field cycles.

## Constructor cycle vs “early” singleton

Creating A’s constructor needs a finished B; B’s constructor needs a finished A. Neither constructor can return → **`BeanCurrentlyInCreationException`**. Setter/field injection (and `@Autowired` on setters/fields) runs **after** `new`, so the factory can hand B a pointer to A **before** A’s remaining properties and init callbacks run — the chicken-and-egg the DI chapter describes ([[Which dependency injection styles do you know]]).

```d2
Ctor: {
  A1: "A(B)"
  B1: "B(A)"
  A1 -> B1
  B1 -> A1
  note: "fails: BeanCurrentlyInCreationException"
}
Setter: {
  A2: "A (constructed)"
  B2: "B needs A"
  A2 -> B2: "early reference\n(not fully initialized)"
}
```

**Fig. 1.** Constructor loop cannot complete. Setter loop, **if allowed**, injects an incomplete singleton.

`AbstractAutowireCapableBeanFactory.setAllowCircularReferences`: resolution means **one bean sees another that is not fully initialized**. Side effects on init and AOP wrapping are real. Javadoc: **do not rely on this**; extract a **third bean** that both call. `allowRawInjectionDespiteWrapping` (default **false**) is a last resort if the early object later gets wrapped (proxy) and a raw instance was already injected.

```java
@Component
public class Alpha {
	private final Beta beta;
	public Alpha(Beta beta) { this.beta = beta; }
}

@Component
public class Beta {
	private final Alpha alpha;
	public Beta(Alpha alpha) { this.alpha = alpha; }
}
```

**Listing 1.** Classic constructor cycle — fails at `refresh()` whether or not circular references are allowed.

## Boot and AOT change the default story

On a **plain** Framework `ApplicationContext`, circular-reference resolution defaults **on**. **`SpringApplication.setAllowCircularReferences`** (since Boot **2.6.0**) defaults **`false`**. Property: **`spring.main.allow-circular-references`** (default **`false`**). Turning it on only restores automatic early-singleton wiring; it does **not** make Listing 1 valid.

AOT-optimized contexts **fail** on those setter/field cycles even when the regular JVM might wire them. Official AOT guidance: avoid the cycle; else **`@Lazy` injection points** or **`ObjectProvider`** ([[What is the Lazy annotation in Spring]], [[How do you fix a circular dependency caused by self-injection in Spring]]).

`@Configuration` + `@PostConstruct` that calls a **non-static** `@Bean` method on the same class is the same class of error (Boot 2.6+).

## What to do instead of “resolving”

1. **Break the graph** — shared logic in a third bean (Framework’s recommended design).
2. **`@Lazy`** on one constructor argument — inject a lazy-resolution **proxy**, not the unfinished singleton.
3. **`ObjectProvider<T>`** — retrieve the collaborator when first used.
4. Do **not** switch mandatory deps to **field** injection just to hide the cycle.

> [!warning] Early references are half-built beans
> The injected object may not have run `@PostConstruct` / `InitializingBean` yet, and may not be the final AOP proxy. Using it in a constructor or init method of the other bean is a race against the remainder of creation. Constructor cycles never get this shortcut.

> [!tip] Interview answer
> Constructor A↔B: always `BeanCurrentlyInCreationException`. Setter/field: Framework *can* expose an early singleton; Boot 2.6+ and AOT refuse that by default. Fix the design or use `@Lazy` / `ObjectProvider`, not `allow-circular-references=true`.
