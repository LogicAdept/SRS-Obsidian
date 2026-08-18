<!--
reps: 0
priority: 0
-->
#Java/Language/Enum #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: each enum constant is an object. When the enum type is first used (class load / first reference), the constructor runs once per constant.

```java
public enum MySingleton {
    INSTANCE;
    private MySingleton() {
        System.out.println("Inside constructor of MySingleton");
    }
}
System.out.println(MySingleton.INSTANCE);
// constructor once, then INSTANCE
System.out.println(MySingleton.INSTANCE);
// constructor does not run again
```

Parameterized constants (`Sun("Holiday")`) pass arguments into that constructor.

> [!warning] Unverified traps from the dump
> - Treat “compile-time constants” vs “constructed on first reference” as a dump wording clash to check.
