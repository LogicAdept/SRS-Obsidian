<!--
reps: 0
priority: 0
-->
#Java/Language/Records #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

The canonical constructor has the same parameter list as the record header. The compiler generates one that assigns each component. You can declare it yourself to add validation or normalisation.

Two dump styles:

```java
// Compact canonical constructor (no parameter list)
record Range(int min, int max) {
    Range {
        if (min > max)
            throw new IllegalArgumentException("min > max");
        // compiler appends: this.min = min; this.max = max;
    }
}

// Additional constructors must this(...) into the canonical one
record Point(double x, double y) {
    Point() { this(0.0, 0.0); }
}
```

Dumps call the canonical constructor the “source of truth” for field assignment. Compact form is inlined into that constructor before the generated assignments.

> [!warning] Unverified traps from the dump
> - You cannot have both a compact constructor and a separate explicit canonical constructor with the full parameter list (dump: one canonical form).
> - Checked exceptions from the compact/canonical path are claimed to need wrapping because the canonical constructor does not declare `throws`.
