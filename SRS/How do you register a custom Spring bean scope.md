<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Scopes #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Besides built-in scopes (`singleton`, `prototype`, and web `request` / `session` / `global session`), dumps say you can **define your own**. Registration goes through `CustomScopeConfigurer` (and a `Scope` implementation).

Out-of-the-box names dumps list as constants: `ConfigurableBeanFactory.SCOPE_SINGLETON` / `SCOPE_PROTOTYPE`, `WebApplicationContext.SCOPE_REQUEST` / `SCOPE_SESSION` / `SCOPE_GLOBAL_SESSION`.

> [!warning] Unverified traps from the dump
> - Custom scopes are a “we have an API” answer; dumps do not walk `Scope.get` / `remove` in most lists.
> - `global-session` is the Portlet scope; Spring 5 dumps say Portlet support was removed.
