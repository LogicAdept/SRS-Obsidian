<!--
reps: 0
priority: 0
-->
#Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: `@Override` tells the compiler the method is meant to override a superclass (or implement an interface) method. If the signature does not match, compilation fails — catching typos like `makeSond`.

Retention is SOURCE: discarded after compile, not in the class file, not readable via reflection.

Dumps also use it as a marker annotation (no elements).
> [!warning] Unverified traps from the dump
> - @Override does not change dispatch; it only validates the override relationship at compile time.
> - A dump notes a private method cannot override a parent private method; @Override on that pattern is an error.
