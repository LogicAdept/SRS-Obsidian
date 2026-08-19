<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/SpEL #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`PropertySourcesPlaceholderConfigurer` is a `BeanFactoryPostProcessor` that rewrites bean definitions so `${…}` placeholders become real values **before** instances are created. Dumps list it as the example BFPP during IoC startup (after `BeanDefinition`s are parsed, before `BeanFactory` instantiates beans).

`@Value("${maxReadResults}")` and XML `property-placeholder` sit on this mechanism. You can also declare a property-configurer bean in XML.

> [!warning] Unverified traps from the dump
> - Placeholders in `@Value` are resolved against the `Environment` / property sources; the configurer is the XML-era hook that dumps still name in interviews.
> - Using both a legacy `PropertyPlaceholderConfigurer` and `PropertySourcesPlaceholderConfigurer` is a classic double-resolution mess; dumps rarely spell the difference.
