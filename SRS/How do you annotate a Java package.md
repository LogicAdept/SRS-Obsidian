<!--
reps: 0
priority: 0
-->
#Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: package annotations go in `package-info.java` for that package, not on an arbitrary class.

```java
@PackageAnnotation
package com.example.interview.annotations;
```

The annotation type must allow `ElementType.PACKAGE` (explicit `@Target` including PACKAGE, or a target that permits it). Runtime readers load the package via `Package` / `Class.getPackage()` and then the same `getAnnotation` APIs, still requiring RUNTIME retention.
> [!warning] Unverified traps from the dump
> - Annotating one class in the package does not annotate the package.
> - package-info.java is also where package Javadoc lives; mixing the two is easy to miss in review.
