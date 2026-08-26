<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Java/Spring/Boot #Java/Testing/Mockito #Testing/Mocking #Java/Annotations #SRS

# What is SpyBean?

> [!abstract] Short answer
> Cue name **`@SpyBean`**: Boot’s old annotation that **wrapped an existing Spring bean as a Mockito spy** so **unstubbed methods still run**. **Deprecated 3.4, removed in Boot 4.** The replacement is Framework **`@MockitoSpyBean`** (`org.springframework.test.context.bean.override.mockito`) — strategy **`WRAP`**. It **requires exactly one** candidate bean. Contrast: **`@MockitoBean`** is a **full mock** (`REPLACE_OR_CREATE`), not a wrap. Mockito’s **`@Spy`** never enters the `ApplicationContext`.

## Wrap the real bean; stub a few methods

An **early instance** is captured and spied. Other beans `@Autowired` that type get the override. If the original would be an **AOP proxy** (`@Transactional`, `@Cacheable`, `@Retryable`), that **proxy is still created** with the **spy as target** — the injected object is the **proxy**, not the raw spy. **`verify()`** still works. Stubbing through a **caching** proxy is sharp: **`doReturn(…).when(proxy)`** can cache **`null`** during stub recording and **shadow** the spy. Prefer **`doReturn` / `doThrow`**, not **`when(spy.method())`**, so the real method is not invoked while stubbing.

**Cannot** spy a **scoped proxy** (`@Scope(proxyMode = TARGET_CLASS)`). A prototype/scoped bean definition becomes a **singleton** spy. **`FactoryBean`**: the spy is the **created object**, not the factory. Ambiguous types need **`@Qualifier`** or **`@MockitoSpyBean("beanName")`**. Field name is part of the **context cache key**. vs mock: [[What is the difference between MockBean and SpyBean]]. Rename: [[What is the difference between MockitoBean and MockBean]]. `@Spy` without Spring: [[What is the difference between Mock and MockBean]].

```java
@SpringJUnitConfig(TestConfig.class)
class BeanOverrideTests {
    @MockitoSpyBean CustomService customService;
}
```

**Listing 1.** Conceptual Framework **7**. If two `CustomService` beans exist, the one named **`customService`** is used; otherwise the test **fails**.

```java
@MockitoSpyBean("service")
CustomService customService;
```

**Listing 2.** Conceptual: wrap the bean named **`service`**. Boot **4** tests never import **`org.springframework.boot.test.mock.mockito.SpyBean`**.

```d2
direction: down
real: "Early bean instance" {
  width: 220
  height: 40
  style.fill: "#e8f5e9"
}
spy: "Mockito spy (WRAP)" {
  width: 220
  height: 40
  style.fill: "#e3f2fd"
}
aop: "AOP proxy if @Transactional / @Cacheable" {
  width: 320
  height: 50
  style.fill: "#fff3e0"
}

real -> spy -> aop
```

**Fig. 1.** Unstubbed calls **execute production code** (DB, HTTP). That is the feature and the leak.

> [!warning] `@SpyBean` does not compile on Boot 4
> Write **`@MockitoSpyBean`**. The interview may still say SpyBean.

> [!warning] Scoped proxies cannot be spied
> **`TARGET_CLASS` scoped-proxy** beans **fail**. JDK/CGLIB **transactional** proxies are **allowed** — you spy the target **inside** the proxy, then stub carefully.

> [!warning] `@Cacheable` + `doReturn().when(proxy)`
> Recording the stub on the **proxy** can cache an **empty** return and **hide** the spy for those arguments. Stub the **spy**, or avoid caching in that test.

> [!tip] Interview answer
> **SpyBean (now `@MockitoSpyBean`) wraps the real Spring bean as a Mockito spy.** Unstubbed methods are real. Use a **full `@MockitoBean` mock** when you need isolation. On Boot 4 the Boot `@SpyBean` annotation is gone.
