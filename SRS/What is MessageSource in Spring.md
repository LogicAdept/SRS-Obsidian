<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC #Internationalization #SRS

# What is MessageSource in Spring?

> [!abstract] Short answer
> `MessageSource` is Spring’s **i18n lookup API**: resolve a code (+ optional `MessageFormat` arguments) for a `Locale`. `ApplicationContext` **extends** `MessageSource`, so every context **is** a message source. A plain `BeanFactory` is not. The context looks for a bean named **`messageSource`** (`AbstractApplicationContext.MESSAGE_SOURCE_BEAN_NAME`). If it finds none in this context or a parent, it installs an empty `DelegatingMessageSource` so `getMessage` still has a delegate.

## Context capability, pluggable bean

`ApplicationContext` adds framework services on top of `BeanFactory`: messages, resources, events, hierarchy ([[What is the difference between BeanFactory and ApplicationContext]], [[How does ApplicationContext publish events]]). Message resolution sits on `MessageSource` plus `HierarchicalMessageSource` (parent fallback).

Three lookup shapes:

- `getMessage(code, args, defaultMessage, locale)` — missing code → the default string; `{0}` placeholders via JDK `MessageFormat`.
- `getMessage(code, args, locale)` — missing code → `NoSuchMessageException`.
- `getMessage(MessageSourceResolvable, locale)` — same data packed in a resolvable (validation `Errors` / `ObjectError` use this).

Built-in implementations (all hierarchical): `ResourceBundleMessageSource` (JDK `ResourceBundle` on the classpath), `ReloadableResourceBundleMessageSource` (any Spring `Resource` location, hot-reload with caching), `StaticMessageSource` (programmatic; rarely used). Locale files follow JDK fallback: `exceptions_en_GB.properties` for `Locale.UK`. Bundles with the **same basename are not merged** — the first wins.

```xml
<beans>
    <bean id="messageSource"
          class="org.springframework.context.support.ResourceBundleMessageSource">
        <property name="basenames">
            <list>
                <value>format</value>
                <value>exceptions</value>
            </list>
        </property>
    </bean>
</beans>
```

**Listing 1.** Conceptual. The id **must** be `messageSource` or the context will not use this bean as its `MessageSource`.

```java
MessageSource resources = new ClassPathXmlApplicationContext("beans.xml");
String text = resources.getMessage("message", null, "Default", Locale.ENGLISH);
```

**Listing 2.** Conceptual. The context is the `MessageSource`; you can also inject the interface.

Injection options:

- `MessageSourceAware.setMessageSource` — container callback with the context’s source ([[What Aware interfaces does Spring invoke during bean initialization]]).
- `@Autowired MessageSource` (also `BeanFactory`, `ApplicationContext`, `ResourceLoader`, `ApplicationEventPublisher`) — well-known resolvable dependency; no extra collaborator bean required.
- Ordinary `ref="messageSource"` on a POJO property.

Web MVC still uses this same bean: controllers/`MessageSource`, JSP/Thymeleaf tags, and `LocaleResolver` pick the `Locale` ([[What is LocaleResolver in Spring MVC]]).

Spring Boot auto-configures a `MessageSource` when a default bundle file exists (`messages.properties` at classpath root by default). `spring.messages.basename` (and related properties) customize it. **Language-only files without the default basename file** mean **no** auto-configured source.

```d2
direction: down
ctx: "ApplicationContext\nextends MessageSource" {
  width: 260
  height: 60
  style.fill: "#e3f2fd"
}
bean: "bean named messageSource" {
  width: 240
  height: 50
  style.fill: "#fff3e0"
}
empty: "else DelegatingMessageSource" {
  width: 260
  height: 50
  style.fill: "#fce4ec"
}
impl: "ResourceBundle / Reloadable / Static" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}

ctx -> bean: lookup
bean -> impl
ctx -> empty: missing
```

**Fig. 1.** The context delegates `getMessage` to the `messageSource` bean or to an empty delegate.

> [!warning] Wrong bean name is a silent miss
> `id="messages"` or a `@Bean` method named `bundle` is just another bean. `ApplicationContext.getMessage` still hits `DelegatingMessageSource` (or a parent’s `messageSource`). Name it `messageSource`.

> [!warning] Missing code vs missing default bundle
> Framework `getMessage` without a default throws `NoSuchMessageException`. Boot will **not** auto-configure at all if only `messages_en.properties` exists and there is no matching default file for the configured basename.

> [!tip] Interview answer
> MessageSource is how Spring resolves parameterized, localized strings. ApplicationContext implements it and delegates to a bean that must be named messageSource — ResourceBundleMessageSource is the usual XML choice. BeanFactory has no i18n API. Boot wires one from messages.properties when that default file is present; MVC views use the same source with a LocaleResolver.
