<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Java/Spring/Boot #Java/Testing/Mockito #Testing/Mocking #Java/Annotations #SRS

# What is the difference between MockBean and SpyBean?

> [!abstract] Short answer
> Both put a Mockito stand-in **into the test `ApplicationContext`** so other beans inject it. **`@MockBean` / `@SpyBean`** were Boot APIs — **deprecated 3.4, removed in 4**. Today: **`@MockitoBean`** vs **`@MockitoSpyBean`** (Framework **6.2+**). **`@MockitoBean`**: **`REPLACE_OR_CREATE`** — a **full mock** (unstubbed methods return Mockito defaults). **`@MockitoSpyBean`**: **`WRAP`** — the **real bean instance** is captured and spied; **unstubbed methods run for real**. The spy **requires exactly one** matching bean. Cue names stay MockBean/SpyBean; Boot **4** source uses Mockito*.

## Replace vs wrap

`@MockitoBean` **bypasses** bean post-processing. The mock is a **bare object** — **not** wrapped in the production AOP proxy (`@Transactional`, `@Cacheable`, `@Retryable` on the original type **do not apply** to the mock). Missing bean: **created** unless **`enforceOverride = true`**.

`@MockitoSpyBean` wraps an **early instance**. If the original would have been an AOP proxy, that **proxy still exists** — it wraps the **spy**. Stub with **`doReturn(…).when(spy)`**, not **`when(spy).…`**, or you may invoke the real method while stubbing. **Cannot** spy a **scoped proxy** (`@Scope(proxyMode = TARGET_CLASS)`). Prototype / scoped definitions become a **singleton** spy (same as mocks).

Both are **context customizers**: field names belong in the **cache key**. Same mock/spy type, **inconsistent field names** → extra refreshes. Rename: [[What is the difference between MockitoBean and MockBean]]. Mockito-only `@Mock`: [[What is the difference between Mock and MockBean]]. Spy cue: [[What is SpyBean]]. Slice: [[What is the WebMvcTest annotation]]. Cache: [[How does the Spring TestContext framework cache the ApplicationContext]].

```java
@SpringJUnitConfig(TestConfig.class)
class BeanOverrideTests {
    @MockitoBean CustomService customService; // full mock in the context
}
```

**Listing 1.** Conceptual Framework **7** **`REPLACE_OR_CREATE`**. Boot **4** slices use the same annotation (`@WebMvcTest` + collaborator).

```java
@SpringJUnitConfig(TestConfig.class)
class SpyOverrideTests {
    @MockitoSpyBean CustomService customService; // real bean, stub selected methods
}
```

**Listing 2.** Conceptual **`WRAP`**. Unstubbed calls **hit production code** (DB, HTTP, …).

```d2
direction: down
mock: "@MockitoBean\nREPLACE_OR_CREATE\nbare mock, no AOP" {
  width: 300
  height: 55
  style.fill: "#e3f2fd"
}
spy: "@MockitoSpyBean\nWRAP real instance\nproxy may wrap the spy" {
  width: 300
  height: 55
  style.fill: "#fff3e0"
}
inject: "Other beans @Autowired\nthe override" {
  width: 280
  height: 45
  style.fill: "#e8f5e9"
}

mock -> inject
spy -> inject
```

**Fig. 1.** Isolation: mock. Partial real behavior: spy. Old **`@MockBean` / `@SpyBean`** imports **do not compile** on Boot 4.

> [!warning] A spy is not isolation
> Unstubbed methods **run the real collaborator**. That is the point — and the leak (network, database, extra `@Transactional` work).

> [!warning] `when(spy.method())` can call the real method
> Use **`doReturn` / `doThrow` / `doNothing`**. Scoped-proxy beans **cannot** be `@MockitoSpyBean`.

> [!warning] Mocking the type under test
> A `@MockitoBean` **service** has **no** class AOP. Mock **dependencies**; keep the real bean if you need interceptors.

> [!tip] Interview answer
> **MockBean (now `@MockitoBean`) replaces the bean with a full mock. SpyBean (now `@MockitoSpyBean`) wraps the real bean.** Unstubbed spy calls are real. On Boot 4 the Boot annotations are gone — say MockitoBean / MockitoSpyBean.
