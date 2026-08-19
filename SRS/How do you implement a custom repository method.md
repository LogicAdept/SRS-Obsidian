<!--
reps: 0
priority: 0
-->
#Java/Spring/Data #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

When query derivation cannot express the logic:

1. Declare a custom interface with the extra methods.
2. Implement it. The implementation class name uses the Impl suffix by default relative to the repository.
3. Extend both JpaRepository (or the store repository) and the custom interface from the main repository.

```java
public interface CustomRepository {
    List<CustomEntity> customQueryMethod();
}

public class CustomRepositoryImpl implements CustomRepository {
    @PersistenceContext
    private EntityManager em;
    public List<CustomEntity> customQueryMethod() {
        return em.createQuery("SELECT c FROM CustomEntity c WHERE c.someField = :value", CustomEntity.class)
                 .setParameter("value", "someValue")
                 .getResultList();
    }
}

public interface MainRepository extends JpaRepository<CustomEntity, Long>, CustomRepository {
}
```

Mongo dumps do the same with a *Impl class that injects MongoTemplate.
> [!warning] Unverified traps from the dump
> - The Impl suffix is the default naming Spring Data looks up; a dump that registers the Impl as a @Bean is extra and easy to get wrong.
> - The fragment interface must be mixed into the repository Spring Data proxies.
