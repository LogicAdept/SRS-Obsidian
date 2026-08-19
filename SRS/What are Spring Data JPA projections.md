<!--
reps: 0
priority: 0
-->
#Java/Spring/Data/JPA #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Projections fetch only the columns you need instead of the full entity, which dumps say reduces memory and database load.

Interface-based projection: define an interface with getters for the properties to extract.

```java
public interface UserSummary {
    String getFirstname();
    String getLastname();
}

public interface UserRepository extends JpaRepository<User, Long> {
    List<UserSummary> findByRole(String role);
}
```

Class-based projection (DTO): a class with a constructor matching the projected properties.

```java
public class UserDto {
    private String firstname;
    private String lastname;
    public UserDto(String firstname, String lastname) {
        this.firstname = firstname;
        this.lastname = lastname;
    }
}
```
> [!warning] Unverified traps from the dump
> - Dumps claim the interface projection will only select firstname and lastname.
> - DTO projections need a constructor that matches the selected properties.
