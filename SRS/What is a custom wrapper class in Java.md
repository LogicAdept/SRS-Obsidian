<!--
reps: 0
priority: 0
-->
#Java/Language/Wrappers #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

A dump: built-in wrappers wrap primitives. You can also write your own class that wraps a primitive; that user-defined class is a custom wrapper.

Example shape: a class holding a private `int`, constructors, `getValue` / `setValue`, and `toString` delegating to `Integer.toString`.

Unlike `Integer`, that example is mutable (`setValue`).

> [!warning] Unverified traps from the dump
> - A custom wrapper is not a `java.lang` wrapper and is not what collections autobox to.
> - The dump’s custom wrapper is mutable; `Integer` dumps call `Integer` immutable.
