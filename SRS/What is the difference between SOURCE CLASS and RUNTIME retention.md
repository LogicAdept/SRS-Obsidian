<!--
reps: 0
priority: 0
-->
#Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps compare the three `RetentionPolicy` values as a lifecycle:

| Policy | In source | In `.class` | Via reflection |
| SOURCE | yes | no | no |
| CLASS (default) | yes | yes | no |
| RUNTIME | yes | yes | yes |

SOURCE: compiler-only checks and apt. CLASS: post-compile bytecode tools, no `getAnnotations()`. RUNTIME: frameworks that scan types after load.

`@Override` / `@SuppressWarnings` are cited as SOURCE; `@Deprecated` as RUNTIME.
> [!warning] Unverified traps from the dump
> - CLASS vs RUNTIME is the interview distinction people flatten to “in the class file or not” — both are in the class file.
> - Default CLASS means a forgotten @Retention looks like CLASS, not SOURCE.
