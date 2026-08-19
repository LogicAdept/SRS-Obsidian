<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/JPA #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

findById returns an Optional containing the entity, or Optional.empty() if not found. Dumps call it a safe, immediate fetch.

getOne returns a reference without fetching immediately. It uses lazy loading and can throw EntityNotFoundException if the entity does not exist when you first access it.

```java
Optional<User> user = userRepository.findById(1L);
User user = userRepository.getOne(1L);
```
> [!warning] Unverified traps from the dump
> - Accessing a getOne reference for a missing id is delayed until you touch the proxy.
> - findById is the dump's default for a real load; getOne is a reference.
