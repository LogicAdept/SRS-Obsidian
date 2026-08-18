<!--
reps: 0
priority: 0
-->
#Java/Language/Records #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

A compact constructor is a record-only constructor with no parameter list. Dumps use it for validation and normalisation. The compiler inlines the body into the canonical constructor, then assigns fields.

```java
public record Email(String value) {
    public Email {
        if (value == null || !value.contains("@"))
            throw new IllegalArgumentException("Invalid email");
        value = value.toLowerCase().trim();  // dumps: reassign the parameter
    }
}
```

Generated shape dumps show:

```java
public Email(String value) {
    if (value == null || !value.contains("@"))
        throw new IllegalArgumentException("Invalid email");
    value = value.toLowerCase().trim();
    this.value = value;
}
```

> [!warning] Unverified traps from the dump
> - Do not write `this.name = ...` in the compact body — dumps say that is a compile error; reassign the implicit parameter (`name = name.toUpperCase()`).
> - Dumps also say you cannot use `this` before the generated assignments complete.
> - One dump table said compact constructors cannot change parameters; the same dump’s examples then reassign parameters. Treat that as an internal contradiction to verify.
