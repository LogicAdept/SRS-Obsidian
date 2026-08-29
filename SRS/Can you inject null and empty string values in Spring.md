<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Configuration #SRS

# Can you inject `null` and empty strings in Spring?

> [!abstract] Short answer
> **Yes — as explicit values.** An empty `value=""` is the empty `String` `""`. Nested `<null/>` is a Java `null`. They are different. Java configuration does the same work by calling the setter (or constructor) with `""` or `null`. Autowiring a missing bean is a different rule.

## Empty `String` versus Java `null`

Spring treats empty arguments for properties and constructor arguments as empty `String`s. The beans schema therefore defines a dedicated `<null/>` element: an empty `<value/>` (or `value=""`) becomes `""`, and that empty string is **not** converted to `null` unless a special `PropertyEditor` does so.

```xml
<bean class="ExampleBean">
    <property name="email" value=""/>
</bean>
```

**Listing 1.** Empty `value` injects `""`. Same as `exampleBean.setEmail("")`.

```xml
<bean class="ExampleBean">
    <property name="email">
        <null/>
    </property>
</bean>
```

**Listing 2.** `<null/>` injects a Java `null`. Same as `exampleBean.setEmail(null)`.

The `value` attribute is a human-readable **string** that Spring’s conversion service then converts to the property’s type. `value="null"` is therefore the four-character string `"null"`, not a null reference.

```d2
direction: down
xml: "Explicit XML value" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
empty: "value=\"\" or empty <value/>\n→ empty String \"\"" {
  width: 280
  height: 80
  style.fill: "#e8f5e9"
}
nullEl: "<null/>\n→ Java null" {
  width: 240
  height: 80
  style.fill: "#fff3e0"
}
literal: "value=\"null\"\n→ String \"null\"" {
  width: 240
  height: 80
  style.fill: "#ffebee"
}

xml -> empty
xml -> nullEl
xml -> literal
```

**Fig. 1.** Three XML spellings, three Java values. Only `<null/>` denotes a null reference.

`<null/>` is also valid inside `<constructor-arg>` and as a list, set, or map entry — the same sub-element set as `<property>`.

```xml
<bean class="ExampleBean">
    <constructor-arg>
        <null/>
    </constructor-arg>
</bean>
```

**Listing 3.** Constructor injection of `null`. Same idea as Listing 2; the schema allows `<null/>` on `constructor-arg`.

`<null/>` is a **reference** value. A Java primitive property cannot store `null`, so this element is for types such as `String`, wrappers, and collaborators.

## Equivalent Java configuration

XML is only metadata for the same setter and constructor calls you would write in a `@Bean` factory. [[Which dependency injection styles do you know]] still applies: constructor versus setter is independent of whether the value is `""` or `null`.

```java
@Bean
ExampleBean example() {
    ExampleBean bean = new ExampleBean();
    bean.setEmail("");    // empty String
    // bean.setEmail(null); // Java null
    return bean;
}
```

**Listing 4.** Conceptual `@Bean` factory. There is no XML-style `<null/>` token in Java: you pass `null` in code.

## Explicit wiring, not autowiring

XML autowiring does not fill simple properties such as primitives, `String`, and `Class` (or arrays of those). That limit is by design. Explicit `<property>` and `<constructor-arg>` — including `value=""` and `<null/>` — always override autowiring. They are ordinary value injection, not autowire modes. See [[What are the limitations of XML autowiring in Spring]].

> [!warning] `@Autowired` does not inject a null literal
> Default `@Autowired` fails the context if no matching bean exists. `required = false` **skips** that injection point and leaves the field’s default (an uninitialized object field stays `null`). `Optional` and a parameter-level `@Nullable` (any package) mark the dependency as optional. That is “no collaborator,” not the XML `<null/>` value. See [[What does Autowired required false do]].

> [!warning] Placeholders do not mean Java `null`
> `${email}` does not become Java `null` by default. `PlaceholderConfigurerSupport.setNullValue` can treat a chosen token (for example `""` or `"null"`) as `null` for a **full** placeholder value. With no mapping, there is no way to express `null` through a property placeholder.

> [!warning] Nested property paths still need live intermediates
> `name="fred.bob.sammy"` walks `getFred().getBob().setSammy(...)`. After construction, `fred` and `bob` must be non-null or Spring throws `NullPointerException`. The last name is the property being set and may receive `null`; the walk fails if an intermediate is `null`.

> [!warning] A `@Bean` method that returns `null` is not a null property
> `BeanFactory.getBean(name)` never returns a Java `null`; a factory that returned `null` is represented by an internal NullBean stub that answers `equals(null)`. Typed `getBean(name, SomeType.class)` then raises `BeanNotOfRequiredTypeException`. That is a null **bean instance**, not a null **property** on another bean.

> [!tip] Interview answer
> Yes. In XML, `value=""` is the empty string and `<null/>` is Java null — they are not interchangeable, and `value="null"` is just the string `"null"`. Java config passes `""` or `null` to the setter or constructor. Do not mix that with `@Autowired(required = false)`, which skips a missing bean instead of injecting a null literal.
