<!--
reps: 0
priority: 0
-->
#Java/Spring/Data #SRS

# How do you implement a custom repository method?

> [!abstract] Short answer
> Add a **repository fragment**: a small custom interface, a class named `{FragmentName}Impl` that implements it, and extend both the store repository and the fragment from your main repository interface. Spring Data auto-detects the `Impl` class and composes it into the repository proxy — you do not `@Bean` the implementation.

## Fragment + `Impl` composition

When derived query methods, `@Query`, or Specifications are not enough, implement logic in a fragment class and expose it through the main repository.

```java
public interface OrderRepositoryCustom {
  List<Order> findHighValueOrders(BigDecimal threshold);
}

public class OrderRepositoryCustomImpl implements OrderRepositoryCustom {

  @PersistenceContext
  private EntityManager em;

  @Override
  public List<Order> findHighValueOrders(BigDecimal threshold) {
    return em.createQuery(
            "SELECT o FROM Order o WHERE o.total >= :threshold", Order.class)
        .setParameter("threshold", threshold)
        .getResultList();
  }
}

public interface OrderRepository
    extends JpaRepository<Order, Long>, OrderRepositoryCustom {}
```

**Listing 1.** JPA custom fragment with `EntityManager` (Spring Data Commons custom repository pattern).

Spring Data scans for `{CustomInterfaceName}Impl` in the repository’s package (default postfix **`Impl`**, overridable via `@EnableJpaRepositories(repositoryImplementationPostfix = …)`). The composed proxy delegates custom methods to the fragment and CRUD/query methods to the generated base.

```d2
direction: right
main: "OrderRepository\nextends JpaRepository\n+ OrderRepositoryCustom" {
  width: 280
  height: 90
  style.fill: "#e3f2fd"
}
proxy: "Spring Data proxy" {
  width: 180
  height: 70
  style.fill: "#fff3e0"
}
base: "Generated CRUD\n/ @Query methods" {
  width: 200
  height: 70
  style.fill: "#e8f5e9"
}
impl: "OrderRepositoryCustomImpl\n(EntityManager / MongoTemplate)" {
  width: 280
  height: 70
  style.fill: "#f3e5f5"
}

main -> proxy
proxy -> base
proxy -> impl
```

**Fig. 1.** One repository interface; runtime composition merges base repository + custom fragment.

For MongoDB, the same pattern uses `OrderRepositoryCustomImpl` with **`MongoTemplate`** or `MongoOperations` instead of `EntityManager`. You can mix **multiple** fragment interfaces on one repository; declaration order controls precedence when signatures overlap.

> [!warning] Do not register `Impl` as a `@Bean`
> The fragment implementation is picked up by naming convention and composed into the repository factory. Manually declaring it as a Spring bean is unnecessary and can break the expected `…Impl` lookup. The fragment interface must be **extended by the repository interface** — a standalone custom class is not reachable through the repository proxy.

See [[What is Spring Data JPA]], [[What is MongoTemplate]], and [[How do you define a native query in Spring Data JPA]].

> [!tip] Interview answer
> I declare a custom fragment interface, implement it in a class suffixed `Impl`, and extend both `JpaRepository` and that fragment from the main repository. Spring Data finds `OrderRepositoryCustomImpl` automatically and merges it into the proxy. For Mongo I inject `MongoTemplate` the same way I use `EntityManager` in JPA.
