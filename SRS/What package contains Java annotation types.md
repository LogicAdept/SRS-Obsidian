<!--
reps: 0
priority: 0
-->
#Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Language annotation types and meta-annotations live in `java.lang.annotation` (`Retention`, `Target`, `Inherited`, `Documented`, `Repeatable`, `RetentionPolicy`, `ElementType`, `Annotation`). Built-in code annotations `@Override`, `@Deprecated`, `@SuppressWarnings`, `@SafeVarargs`, `@FunctionalInterface` live in `java.lang` and need no extra import.

Some dumps answer “`java.text`” and “parent class is `Object`” for “the Annotation class.”
> [!warning] Unverified traps from the dump
> - Dump lie: package java.text. That is formatting, not annotations.
> - java.lang.annotation.Annotation is an interface, not a class under Object as the dump frames it.
