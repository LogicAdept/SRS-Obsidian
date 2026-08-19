<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/Build #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`spring-boot-starter-parent` (or the `spring-boot-dependencies` BOM) supplies a curated `dependencyManagement`. You declare the starter artifact, not a version for Jackson/Tomcat/Hibernate.

If you already have a corporate parent, import the BOM with `scope=import` instead of using the Boot parent.

> [!warning] Unverified traps from the dump
> - Omitting the Boot parent without importing the BOM is how version fights come back.
