<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC #SRS

# What is a Spring inner bean?

> [!abstract] Short answer
> An **inner bean** is a `<bean>` nested inside another bean’s `<property>` or `<constructor-arg>`. It is **always anonymous**: even if you write an `id`, the container does **not** use it as a lookup name. The `scope` attribute is **ignored** on creation — the inner instance is created **with** the outer bean and cannot be injected anywhere else. Inner beans usually **share the outer bean’s scope**, not a hidden prototype.

## Nested definition, private to the outer bean

Instead of `ref` to a top-level bean, XML can inline the collaborator ([[What is a Spring bean]]):

```xml
<bean id="outer" class="example.Outer">
    <property name="target">
        <bean class="example.Person">
            <property name="name" value="Fiona Apple"/>
            <property name="age" value="25"/>
        </bean>
    </property>
</bean>
```

**Listing 1.** Conceptual. The nested `Person` is an inner bean — no `id` required, and none you could `getBean`.

Rules from the container:

- No id/name is required. If you set one, it is **not** an identifier for `getBean` / `ref`.
- Always anonymous; always created together with the enclosing bean.
- `scope` on the inner definition is **ignored at creation**. Typical case: the inner instance follows the **containing** bean’s scope (a singleton outer → one inner for that outer). That is **not** “inner beans are prototypes.”
- You cannot inject the inner bean into any collaborator other than the enclosing bean.

**Destruction** is a corner case: a custom-scoped inner bean (for example **request**-scoped inside a **singleton**) can still receive that scope’s destroy callbacks while its **creation** stays tied to the outer bean. Uncommon. Ordinary inner beans just share the outer lifecycle ([[What destroy callbacks does Spring invoke when a bean is destroyed]]).

`BeanNameAware` may still see an internal name with a `#…` uniqueness suffix. That name is not a public id.

There is no XML-style inner bean in Java config. A `@Bean` method that `new`s a collaborator (or calls another `@Bean` method) creates a Java object; only a nested `<bean>` is this anonymous definition. Do not confuse that with injecting a **prototype** into a singleton, which is a named bean still resolved once ([[How does a prototype Spring bean behave when injected into a singleton]]).

```d2
direction: down
outer: "Outer bean\n(has an id)" {
  width: 180
  height: 60
  style.fill: "#e3f2fd"
}
inner: "Inner <bean>\nanonymous, scope ignored" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}
other: "Other beans\ncannot ref it" {
  width: 180
  height: 60
  style.fill: "#fce4ec"
}

outer -> inner
other -> inner: no
```

**Fig. 1.** The inner definition exists only as a nested property/constructor argument of the outer bean.

> [!warning] An `id` on an inner bean is not a shared singleton
> You cannot `ref="thatId"` or `getBean("thatId")` another collaborator to the same inner instance. If two outers need the same collaborator, define a **top-level** bean and `ref` it.

> [!warning] `scope="prototype"` on the inner `<bean>` does not do what you think
> The container ignores that flag when creating the inner instance. To get a new collaborator per lookup, use a **named** prototype (and mind singleton injection). Request-scoped inner beans are only a destroy-callback corner case.

> [!tip] Interview answer
> An inner bean is a bean element nested under property or constructor-arg. It is always anonymous and created with the outer bean; an id is ignored as a public name, and so is scope at creation. Nothing else in the container can inject it. That is an XML nesting trick, not Java config, and it is not the same as prototype scope.
