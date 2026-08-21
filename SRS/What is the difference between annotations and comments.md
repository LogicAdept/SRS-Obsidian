<!--
reps: 0
priority: 0
-->
#Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: comments are for humans and are ignored by the compiler (aside from Javadoc tooling). Annotations are typed metadata the compiler, processors, and (if RUNTIME) reflection can read.

A ClassPreamble dump replaces a block of author/date comments with an `@interface` plus an annotation instance so tools can parse fields instead of scraping comments.

Annotations can fail compilation (`@Override` mismatch) or drive code generation; comments cannot.
> [!warning] Unverified traps from the dump
> - Javadoc tags are still comments; @Documented only copies the annotation into generated Javadoc, it does not turn comments into annotations.
