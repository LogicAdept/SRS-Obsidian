<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`LocaleResolver` decides the current `Locale` from the request (and may store a change). Used for i18n with message bundles.

Dump example: `SessionLocaleResolver` with a default locale, plus `LocaleChangeInterceptor` (`paramName = "lang"`) registered on `WebMvcConfigurer`.

Other dump names: `CookieLocaleResolver`, `AcceptHeaderLocaleResolver`.

> [!warning] Unverified traps from the dump
> - Localization is also a separate card; this one is the LocaleResolver SPI.
