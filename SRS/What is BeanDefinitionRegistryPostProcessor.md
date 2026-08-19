<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Lifecycle #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

After annotation/`@Configuration` parsing, Spring registers a `BeanDefinitionRegistryPostProcessor` (a kind of `BeanFactoryPostProcessor`). Dumps name `ConfigurationClassParser` as the piece that walks Java config and fills `Map<String, BeanDefinition>`.

`BeanFactoryPostProcessor` adjusts **definitions** (or the factory) **before** beans are created — one method, `postProcessBeanFactory`. `PropertySourcesPlaceholderConfigurer` is the usual example: it substitutes `${…}` in bean definitions.

`BeanDefinitionRegistryPostProcessor` is the variant dumps mention when Java config must **register additional bean definitions**, not only mutate existing ones.

> [!warning] Unverified traps from the dump
> - This runs on `BeanDefinition`s, not instances. You must not touch live beans here; they do not exist yet.
> - Ordinary `BeanPostProcessor` is later and works on instances.
