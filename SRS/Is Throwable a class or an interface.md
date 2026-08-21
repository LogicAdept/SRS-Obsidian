<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Hierarchy #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

One dump calls `Throwable` a unified interface for anything that can be thrown. The type in `java.lang` is a concrete class whose direct subclasses are `Exception` and `Error`. Only instances of that class or its subclasses may be thrown or caught.
> [!warning] Unverified traps from the dump
> - Throwable is a class that implements Serializable, not an interface.
> - It is not abstract: new Throwable() compiles, but dumps advise not to use it as an application type.
