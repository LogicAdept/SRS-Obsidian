<!--
reps: 0
priority: 0
-->
#Java/Quarkus #SRS #New

> [!warning] Untrusted draft
> Drafted from general framework knowledge, not from an opened question dump. Not yet checked against official documentation. Do not treat this as a review answer.

Draft: ArC is Quarkus's dependency injection container, an implementation of Jakarta CDI Lite (based on CDI 4.1 spec) plus selected extras; it passes the CDI Lite TCK.
Key design: the container is resolved at build time. Bean discovery works on a single synthetic bean archive with annotated discovery mode; no visibility boundaries.
Normal scopes (@ApplicationScoped, @RequestScoped) inject client proxies and instantiate lazily on first method call; pseudo-scopes (@Dependent, @Singleton) instantiate at injection time.
Extras beyond CDI Lite: @Startup eager instantiation, simplified constructor injection, removal of unused beans at build time, build-time-conditioned beans.
Limitations: not full CDI — e.g. @SessionScoped only with Undertow, no decoration of built-in beans, no runtime bean registration; dynamic features are restricted by design.

> [!warning] Unverified traps from the draft
> - Facts above are plausible but unchecked; version numbers and exact API names must be confirmed against official docs before this card is used as a review answer.
> - Comparison cards must keep both sides tagged and avoid absolute always/never claims.
