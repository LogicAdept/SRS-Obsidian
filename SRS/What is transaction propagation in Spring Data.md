<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/JPA #Java/Spring/Transactions/Propagation #SRS

# What is transaction propagation in Spring Data?

> [!abstract] Short answer
> Spring Data does **not** define its own propagation model — repository and service code use Spring’s **`Propagation`** on **`@Transactional`**. Default is **`REQUIRED`**: a repository call **joins** an active service transaction or **starts** one if none exists. Tune propagation on a **redeclared repository method** or, preferably, on the **service facade** that coordinates multiple repositories.

## Same `Propagation` enum as Spring Framework

Spring Data JPA inherits transactional behavior from **`SimpleJpaRepository`**: plain **`@Transactional`** on write CRUD ( **`REQUIRED`** defaults) and **`readOnly = true`** on reads. Custom derived/query methods have **no** transaction until you add **`@Transactional`** on the interface or invoke them from an already transactional service — [[What is the Transactional annotation in Spring Data]].

When a propagation attribute is set, it is the standard Spring attribute — same seven levels as [[What are Spring transaction propagation levels]].

```java
@Service
public class TransferService {

    @Transactional // REQUIRED — one TX for both repos
    public void transfer(Long from, Long to, BigDecimal amount) {
        Account debit = accounts.findById(from).orElseThrow();
        Account credit = accounts.findById(to).orElseThrow();
        debit.withdraw(amount);
        credit.deposit(amount);
        accounts.save(debit);
        accounts.save(credit);
    }
}

public interface AccountRepository extends JpaRepository<Account, Long> {

    @Override
    @Transactional(propagation = Propagation.MANDATORY)
    Optional<Account> findById(Long id);
}
```

**Listing 1.** Service owns the unit of work; repository can enforce `MANDATORY` on a redeclared CRUD method (Spring Data JPA reference pattern for overriding TX).

```d2
direction: down
svc: "@Transactional(REQUIRED)\nservice method" {
  width: 280
  height: 80
  style.fill: "#e8f5e9"
}
repo1: "Repository call\njoins same TX" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}
repo2: "Second repository\nsame physical TX" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}

svc -> repo1 -> repo2
```

**Fig. 1.** Typical Spring Data flow: one service propagation policy wraps multiple repository operations.

## Where to set propagation in practice

| Layer | Guidance |
| --- | --- |
| **Service / facade** | Primary place for `REQUIRED`, `REQUIRES_NEW`, etc. across multiple repos |
| **Repository interface** | Override inherited CRUD or annotate custom queries; defaults already `REQUIRED` on writes |
| **Cross-bean only** | Inner `REQUIRES_NEW` on a **separate bean** — not `this` self-call ([[What happens when one Spring Transactional method calls another]]) |

`REQUIRES_NEW` on an audit helper in another bean still follows Spring suspension semantics — [[How does REQUIRES_NEW transaction propagation work]]. JTA/JDBC caveats are unchanged — [[What are transaction propagation semantics in Spring or JTA]].

> [!warning] Per-repository `REQUIRES_NEW` splits atomic business work
> A `save` in `REQUIRES_NEW` commits before the service method finishes — outer failure will not roll it back. Use only for intentional side effects (audit/outbox), usually on a **separate service bean**.

> [!warning] Query methods without `@Transactional` are non-transactional alone
> Calling `findByLastname` on an unannotated repository outside any service TX runs without a Spring transaction unless the persistence provider or database auto-commit applies.

> [!warning] `readOnly` and propagation interact on new transactions only
> Isolation, timeout, and `readOnly` apply when propagation starts a **new** physical transaction (`REQUIRED` with none active, or `REQUIRES_NEW`) — same rules as core Spring ([[What is the Spring Transactional annotation and its parameters]]).

> [!tip] Interview answer
> **Spring Data uses Spring’s propagation unchanged — default `REQUIRED` on repository CRUD.** Put multi-repository rules on the service; repositories join that TX. Override propagation on a redeclared repository method when you need stricter helpers like `MANDATORY`, but independent commits belong in another bean with `REQUIRES_NEW`.
