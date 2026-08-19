<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Override `WebMvcConfigurer.configureMessageConverters` (or `extendMessageConverters`) and add converters:

```java
@Override
public void configureMessageConverters(List<HttpMessageConverter<?>> converters) {
    converters.add(new MappingJackson2HttpMessageConverter());
}
```

`configureMessageConverters` in dumps **replaces** defaults if you only add your own list — Boot/MVC auto-config may differ.

> [!warning] Unverified traps from the dump
> - configureMessageConverters vs extendMessageConverters: one dump pattern wipes defaults; check which method you override.
