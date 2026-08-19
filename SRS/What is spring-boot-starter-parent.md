<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/Build #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

The Boot parent POM. It supplies plugin defaults and a curated `dependencyManagement` so starters do not need versions. Corporate parent: import `spring-boot-dependencies` as a BOM instead.

> [!warning] Unverified traps from the dump
> - It is a Maven parent, not a runtime starter you put on the classpath of the running app.
