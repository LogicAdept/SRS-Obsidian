<!--
reps: 0
priority: 0
-->
#Java/Language/Enum #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

No. You cannot `new` an enum type. Constants must be declared inside the enum body. The compiler does not allow a public constructor, so instances cannot be created outside the enum.

```java
enum Week { Sun, Mon, Tue, Wed, Thu, Fri, Sat }
// Week w = new Week();  // not allowed
```

Dumps: if you wanted another value, you would add another constant in the enum declaration, not allocate with `new`.

> [!warning] Unverified traps from the dump
> - Reflective instantiation is also described as prohibited, together with `clone` being final on `Enum`.
