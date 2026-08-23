<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/MongoDB #Java/Spring/Transactions #Java/Annotations #SRS

# How do you use multi-document transactions in Spring Data MongoDB?

> [!abstract] Short answer
> Register a **`MongoTransactionManager`** bean (and **`@EnableTransactionManagement`**), use the **same `MongoDatabaseFactory`** for **`MongoTemplate`**, then mark service methods **`@Transactional`**. Spring binds a MongoDB **`ClientSession`** to the thread; **`MongoTemplate`** / repositories participate automatically. MongoDB must be a **replica set** or **sharded cluster** — **standalone `mongod` does not support transactions**.

## Spring-side setup

Spring Data MongoDB docs: unless a **`MongoTransactionManager`** is in the application context, **transaction support is disabled** for declarative Spring transactions — registering the manager is what turns it on.

`MongoTransactionManager` binds a **`ClientSession`** to the thread. `MongoTemplate` detects the session and routes operations through it when created with the **same `MongoDatabaseFactory`** as the transaction manager.

```java
@Configuration
@EnableTransactionManagement
static class MongoTxConfig {

    @Bean
    MongoTransactionManager transactionManager(MongoDatabaseFactory dbFactory) {
        return new MongoTransactionManager(dbFactory);
    }

    @Bean
    MongoTemplate mongoTemplate(MongoDatabaseFactory dbFactory) {
        return new MongoTemplate(dbFactory);
    }
}

@Service
public class TransferService {

    private final AccountRepository accounts;

    @Transactional
    public void transferFunds(String fromId, String toId, BigDecimal amount) {
        accounts.debit(fromId, amount);
        accounts.credit(toId, amount);
    }
}
```

**Listing 1.** Conceptual declarative setup from Spring Data MongoDB reference. Same pattern as JDBC — [[How do you use AOP to manage transactions]].

```d2
direction: right
svc: "@Transactional\nservice method" {
  width: 220
  height: 80
  style.fill: "#e3f2fd"
}
mgr: "MongoTransactionManager\nClientSession on thread" {
  width: 280
  height: 80
  style.fill: "#fff3e0"
}
tpl: "MongoTemplate /\nMongoRepository" {
  width: 220
  height: 80
  style.fill: "#e8f5e9"
}
mongo: "MongoDB replica set\nor sharded cluster" {
  width: 260
  height: 80
  style.fill: "#fce4ec"
}

svc -> mgr -> tpl -> mongo
```

**Fig. 1.** Spring’s interceptor opens/commits the session-bound transaction; templates reuse the bound `ClientSession`.

Programmatic control without `@Transactional`: **`TransactionTemplate`** with `MongoTransactionManager`, or manual `ClientSession#startTransaction` / `commitTransaction` / `abortTransaction` via `MongoOperations.withSession` — [[What is the difference between programmatic and declarative transaction management in Spring]].

## MongoDB deployment requirements

MongoDB manual: **standalone deployments do not support transactions**. Use a **multi-node replica set** (FCV ≥ 4.0) or a **sharded cluster** (FCV ≥ 4.2). Spring Data also recommends a **`replicaSet`** name in the connection URI for primary detection during transactions.

Inside transactions, MongoDB restricts some operations (for example **on-the-fly collection creation** on first use) — create collections/indexes ahead of time.

> [!warning] Standalone MongoDB cannot run multi-document transactions
> Local dev on a single `mongod` process fails transaction APIs. Use a replica set (even single-node replica set) for transaction testing.

> [!warning] `MongoTemplate` must share the transaction manager’s factory
> A `MongoTemplate` built with a different `MongoDatabaseFactory` will **not** join `MongoTransactionManager` transactions with default `SessionSynchronization.ON_ACTUAL_TRANSACTION`.

> [!warning] Spring disables Mongo TX until you register the manager
> Adding `@Transactional` alone is not enough — you need **`MongoTransactionManager`** in the context. That is Spring configuration, not a MongoDB server toggle.

> [!tip] Interview answer
> **Register `MongoTransactionManager`, share the same `MongoDatabaseFactory` with `MongoTemplate`, enable transaction management, and put `@Transactional` on the service.** Spring binds a `ClientSession` per thread and commits or rolls back around the method. MongoDB must be a replica set or sharded cluster — not standalone.
