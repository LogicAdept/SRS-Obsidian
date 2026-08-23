<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #Java/Spring/Transactions #SRS

# How do you use AOP to manage transactions?

> [!abstract] Short answer
> Declare transaction boundaries with **`@Transactional`** (or XML transaction advice), enable **`@EnableTransactionManagement`**, and register a **`PlatformTransactionManager`**. Spring builds an **AOP proxy** whose **`TransactionInterceptor`** starts, commits, or rolls back around matching method invocations using that manager.

## Declarative transactions are AOP plus metadata

Spring’s declarative transaction support is not magic on the POJO itself. **`@Transactional` is metadata**; infrastructure reads it and configures a bean with transactional behavior. **`@EnableTransactionManagement`** (or XML `<tx:annotation-driven/>`) switches that infrastructure on at runtime.

The combination yields an AOP proxy wired with a **`TransactionInterceptor`** and a **`PlatformTransactionManager`** (or **`ReactiveTransactionManager`** for reactive return types). The interceptor drives imperative or reactive transaction demarcation around each advised [[What is a JoinPoint in Spring AOP]].

```d2
direction: right
client: "Caller" {
  width: 120
  height: 60
  style.fill: "#e3f2fd"
}
proxy: "Transactional\nAOP proxy" {
  width: 180
  height: 70
  style.fill: "#fff3e0"
}
interceptor: "TransactionInterceptor\n(read @Transactional metadata)" {
  width: 260
  height: 90
  style.fill: "#fff3e0"
}
ptm: "PlatformTransactionManager\ngetTransaction / commit / rollback" {
  width: 280
  height: 90
  style.fill: "#e8f5e9"
}
target: "Target bean method" {
  width: 180
  height: 70
  style.fill: "#fce4ec"
}

client -> proxy
proxy -> interceptor
interceptor -> ptm
interceptor -> target
```

**Fig. 1.** External calls hit the proxy; the interceptor opens a resource transaction before the target method and completes it afterward.

```java
@Configuration
@EnableTransactionManagement
public class AppConfig {

    @Bean
    PlatformTransactionManager transactionManager(DataSource dataSource) {
        return new DataSourceTransactionManager(dataSource);
    }
}

@Service
public class OrderService {

    @Transactional
    public void placeOrder(Order order) {
        // JDBC / JPA work participates in the thread-bound TX
    }
}
```

**Listing 1.** Conceptual setup: a transaction manager bean plus `@EnableTransactionManagement` and `@Transactional` on application methods.

## What the interceptor does at runtime

On each proxied call, the interceptor:

1. Resolves transaction attributes from class/method metadata (propagation, isolation, timeout, read-only, rollback rules — details live on [[What is the Spring Transactional annotation and its parameters]], not here).
2. Asks the configured **`PlatformTransactionManager`** to **`getTransaction`**, joining or suspending an existing thread-bound transaction per propagation.
3. Invokes the target method inside that transactional scope.
4. **`commit`s** on normal completion or **`rollback`s** on configured exceptions / rollback-only status.

Imperative methods use a **`PlatformTransactionManager`** and bind resources to the **current thread**. Reactive methods returning `Publisher` / Kotlin `Flow` (or subtypes) use **`ReactiveTransactionManager`** and Reactor context instead — mixing void/imperative signatures with a reactive manager requires explicit `transactionManager` selection on `@Transactional`.

## Proxy rules you must respect

Default mode is **`proxy`**: only **external** calls through the proxy are intercepted. **`this.inner()`** bypasses the interceptor, so a second `@Transactional` on the same class is ignored — same boundary as [[Why does a self-invocation skip Spring AOP advice]]. For bytecode weaving without a proxy, `@EnableTransactionManagement(mode = AdviceMode.ASPECTJ)` applies advice on self-calls too; see [[What is the difference between Spring AOP and AspectJ]].

> [!warning] Self-invocation skips the transaction interceptor
> Routing through `this` never reaches `TransactionInterceptor`. Extract another bean, inject a self-proxy, or switch to AspectJ mode if the inner annotation must run.

> [!warning] `@EnableTransactionManagement` scans its own application context
> Annotation-driven config in a **`WebApplicationContext`** for `DispatcherServlet` sees `@Transactional` on **controllers in that context**, not service beans defined elsewhere. Put transaction management on the context that owns your service layer (Boot’s single application context avoids this split).

## XML is the same AOP story

Before annotations, the same model used **`<tx:advice>`** plus an AOP advisor (for example `<aop:config>`) to attach **`TransactionInterceptor`** to pointcuts. Annotation-driven and XML-driven declarative transactions share the interceptor/manager pipeline; only the metadata source differs. Programmatic demarcation with `TransactionTemplate` skips this AOP path entirely — see [[What is the difference between programmatic and declarative transaction management in Spring]].

> [!tip] Interview answer
> **Turn on `@EnableTransactionManagement`, define a `PlatformTransactionManager`, and mark service methods with `@Transactional`.** Spring wraps the bean in an AOP proxy whose `TransactionInterceptor` reads the metadata and delegates begin/commit/rollback to the manager. Only calls through the proxy are advised — not same-class `this` calls.
