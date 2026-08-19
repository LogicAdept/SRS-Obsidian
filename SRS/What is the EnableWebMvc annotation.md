<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`@EnableWebMvc` turns on Spring MVC Java config. Dumps equate it to XML `<mvc:annotation-driven/>`.

It imports configuration from `WebMvcConfigurationSupport` and enables `@Controller` classes that use `@RequestMapping`.

Typical class: `@Configuration @EnableWebMvc @ComponentScan(...) class WebConfig implements WebMvcConfigurer`.

> [!warning] Unverified traps from the dump
> - In Spring Boot, @EnableWebMvc takes over MVC config and can disable Boot’s WebMvc auto-configuration — often not what you want.
