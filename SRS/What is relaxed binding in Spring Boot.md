<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/Properties #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`@ConfigurationProperties` binding is tolerant of naming styles. Dumps: `app.mailHost`, `app.mail-host`, `app.mail_host`, and env `APP_MAILHOST` all bind to the same `mailHost` field.

That is why environment variables map onto properties in containers.

> [!warning] Unverified traps from the dump
> - `@Value` dumps contrast as exact-key (plus SpEL), not the same relaxed rules.
