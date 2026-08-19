<!--
reps: 0
priority: 0
-->
#Java/Spring/Data #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Spring Data can publish events when repositories process entities.

Spring Data REST: @HandleBeforeCreate, @HandleAfterCreate, @HandleBeforeSave, @HandleAfterSave, @HandleBeforeDelete, @HandleAfterDelete.

Standard Spring Data JPA: @DomainEvents and @AfterDomainEventPublication on the aggregate root. Collect events, return them from the @DomainEvents method, clear them after publication.

```java
@DomainEvents
Collection<Object> domainEvents() {
    return domainEvents;
}

@AfterDomainEventPublication
void clearEvents() {
    domainEvents.clear();
}
```
> [!warning] Unverified traps from the dump
> - REST handler annotations are not the same API as @DomainEvents on an entity.
> - Events are published around repository save, not around an arbitrary field setter.
