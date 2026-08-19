<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`ApplicationContext` implements `MessageSource`: resolve parameterized, internationalized text. The implementation is pluggable. Dumps contrast this with a plain `BeanFactory`, which has no i18n API.

Typical wiring in MVC dumps: a bean named `messageSource` (`ResourceBundleMessageSource`). `MessageSourceAware` is the Aware callback if a bean wants the strategy injected by the container.

`@Autowired` on a `MessageSource` field (same as `BeanFactory`, `ApplicationContext`, `ResourceLoader`, `ApplicationEventPublisher`) is resolved to the context’s built-in instance without declaring an extra collaborator bean.

> [!warning] Unverified traps from the dump
> - Boot often auto-configures a `MessageSource` from `messages.properties`; classic XML still shows an explicit bean.
> - Web MVC localization cards are the same `MessageSource`, used from views/controllers.
