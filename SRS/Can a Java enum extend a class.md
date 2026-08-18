<!--
reps: 0
priority: 0
-->
#Java/Language/Enum #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

No. Every enum already extends the abstract class `java.lang.Enum`. Java has no multiple inheritance of classes, so an enum cannot `extends` another class.

Because of that superclass, dumps list inherited members such as `ordinal()`, `name()`, `compareTo()`, and (incorrectly, in some lists) `values()` / `valueOf()`.

An enum is also described as implicitly `final`: it cannot be subclassed to add constants.

> [!warning] Unverified traps from the dump
> - Some dumps say `values()` and `valueOf()` come from `java.lang.Enum`; another dump says those two are compiler-generated and are *not* on `Enum` or `Object`.
> - You still cannot write `enum X extends Foo`.
