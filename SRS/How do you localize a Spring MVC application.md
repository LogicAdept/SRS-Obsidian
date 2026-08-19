<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps describe four pieces:

1. A resource bundle with localized strings.
2. A `MessageSource` bean (`ResourceBundleMessageSource`).
3. A `LocaleResolver` (dumps name `CookieLocaleResolver`) so the locale can be switched.
4. `spring:message` in the view; `DispatcherServlet` substitutes the localized text.

> [!warning] Unverified traps from the dump
> - Boot often auto-configures a `MessageSource` from `messages.properties`; classic XML still shows an explicit bean.
> - `AcceptHeaderLocaleResolver` vs cookie vs session is a follow-up the dump does not compare.
