<!--
reps: 0
priority: 0
-->
#Java/Spring/Transactions #SRS

# What is the difference between programmatic and declarative transaction management in Spring?

> [!abstract] Short answer
> **Declarative** management attaches transaction boundaries with **`@Transactional`** (or XML advice) and an AOP **`TransactionInterceptor`**. **Programmatic** management opens and closes transactions in code via **`TransactionTemplate`** / **`TransactionalOperator`** or directly on **`PlatformTransactionManager`**. Spring recommends declarative for most services; programmatic for narrow, explicit control paths.

## Declarative: metadata + proxy

Declarative transactions combine **transaction metadata** (`@Transactional` or `<tx:advice>`) with Spring’s AOP infrastructure. `@EnableTransactionManagement` switches on a **`TransactionInterceptor`** wired to a **`PlatformTransactionManager`** (or reactive manager) that begins, commits, or rolls back around proxied method entry.

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
        orderRepository.save(order);
    }
}
```

**Listing 1.** Conceptual declarative setup — boundary declared on the method, enforced by the proxy. Mechanism detail: [[How do you use AOP to manage transactions]].

## Programmatic: explicit begin/commit in code

Programmatic management keeps boundary control in application code. Spring recommends:

* **`TransactionTemplate`** (imperative) or **`TransactionalOperator`** (reactive) — callback style, less boilerplate than raw manager calls.
* **`PlatformTransactionManager.getTransaction` / `commit` / `rollback`** — lowest level, similar to JTA `UserTransaction` usage.

```java
@Service
public class LegacyImportService {

    private final TransactionTemplate txTemplate;

    public LegacyImportService(PlatformTransactionManager txManager) {
        this.txTemplate = new TransactionTemplate(txManager);
        txTemplate.setPropagationBehavior(TransactionDefinition.PROPAGATION_REQUIRES_NEW);
    }

    public void importChunk(List<Row> rows) {
        txTemplate.executeWithoutResult(status -> {
            for (Row row : rows) {
                try {
                    process(row);
                } catch (RecoverableException ex) {
                    status.setRollbackOnly();
                }
            }
        });
    }
}
```

**Listing 2.** Conceptual programmatic boundary — propagation and rollback controlled in code, not `@Transactional`.

Spring’s docs note that **`TransactionTemplate` and `TransactionalOperator` couple code to Spring’s transaction APIs** — acceptable when you deliberately need fine-grained control (partial rollback flags, conditional commit, non-method-shaped scopes).

```d2
direction: right
decl: "@Transactional\n+ TransactionInterceptor\n(proxy)" {
  width: 260
  height: 90
  style.fill: "#e8f5e9"
}
prog: "TransactionTemplate\nor PlatformTransactionManager\n(in-method)" {
  width: 300
  height: 90
  style.fill: "#fff3e0"
}
mgr: "PlatformTransactionManager" {
  width: 240
  height: 70
  style.fill: "#fce4ec"
}

decl -> mgr
prog -> mgr
```

**Fig. 1.** Both styles delegate to the same transaction manager; only the demarcation mechanism differs.

## When to pick which

| | Declarative | Programmatic |
| --- | --- | --- |
| Boundary declaration | Annotations / XML on methods | Code blocks / callbacks |
| Typical use | Service-layer CRUD, default propagation | Conditional TX, non-method scopes, legacy integration |
| AOP / proxy rules | **Yes** — self-invocation bypasses advice | **No proxy** — you call the template directly |
| Spring recommendation | **Default for application services** | **Targeted** explicit control |

Programmatic **`TransactionTemplate`** can still honor propagation settings (`setPropagationBehavior`, isolation, timeout) without `@Transactional` on a separate method — useful when a `@Transactional` inner method would hit **self-invocation** limits anyway. See [[How do you make an inner Transactional method honor its annotation]].

> [!warning] Declarative is still AOP
> `@Transactional` on a method invoked as `this.other()` does **not** start a second boundary — the proxy is bypassed. Programmatic demarcation inside the same class avoids that pitfall but trades away declarative clarity.

> [!warning] Programmatic couples to Spring APIs
> `TransactionTemplate` / direct `PlatformTransactionManager` usage ties business code to Spring transaction types. Prefer declarative boundaries unless the control flow truly needs in-method demarcation.

> [!tip] Interview answer
> **Declarative = `@Transactional` plus AOP interceptor around proxied calls. Programmatic = `TransactionTemplate` or `PlatformTransactionManager` in code.** Both use the same transaction manager underneath. Use declarative by default; use programmatic for explicit, localized control where annotations and proxies do not fit.
