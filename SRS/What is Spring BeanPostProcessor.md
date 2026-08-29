<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Lifecycle #SRS

# What is Spring BeanPostProcessor?

> [!abstract] Short answer
> `BeanPostProcessor` is a **factory hook on already constructed instances**. After the container **instantiates** and **populates** a bean, it calls **`postProcessBeforeInitialization`**, then init callbacks (`InitializingBean` / `init-method`), then **`postProcessAfterInitialization`**. You may **return the same instance or a wrapper** (AOP / `@Transactional` proxies are built this way). It does **not** edit `BeanDefinition`s — that is `BeanFactoryPostProcessor` ([[What is the difference between BeanFactoryPostProcessor and BeanPostProcessor]]). Both methods default to **return the bean as-is**. `ApplicationContext` **auto-detects** BPP beans; a plain `BeanFactory` needs `addBeanPostProcessor`.

## Instance callbacks, not blueprints

The container extension chapter: plug this in instead of subclassing `ApplicationContext`. Typical work: check **marker interfaces**, or **wrap** the object. Javadoc split: **before-init** for population-style processors; **after-init** for **proxies** so init runs on the **raw** target ([[In what order do PostConstruct InitializingBean and init-method run]]). `@PostConstruct` is applied by `CommonAnnotationBeanPostProcessor` in the **before-init** wave.

```java
public class TracingBeanPostProcessor implements BeanPostProcessor {

    @Override
    public Object postProcessBeforeInitialization(Object bean, String beanName) {
        return bean; // already injected; init methods have not run
    }

    @Override
    public Object postProcessAfterInitialization(Object bean, String beanName) {
        return bean; // wrap here if you need a proxy
    }
}

@Configuration
class AppConfig {
    @Bean
    static TracingBeanPostProcessor tracingBeanPostProcessor() {
        return new TracingBeanPostProcessor();
    }
}
```

**Listing 1.** Conceptual. Return type of the `@Bean` method must be the **implementation** or `BeanPostProcessor` so the context can detect it **early**. Prefer **`static`** and **no dependencies**.

Each **created** instance is offered to **every** registered processor, **in order**. Auto-detected processors honor **`PriorityOrdered` then `Ordered`**. **`@Order` is ignored** on this type. `addBeanPostProcessor` uses **registration order**, **ignores** `Ordered`, and those processors run **before** auto-detected ones.

Processors are **per-container**: a parent-context BPP does not post-process child-context beans. For a `FactoryBean`, **`postProcessAfterInitialization` runs twice** — factory and product. After an `InstantiationAwareBeanPostProcessor.postProcessBeforeInstantiation` **short-circuit**, **only** after-init still runs.

```d2
direction: down
new: "instantiate + inject" {
  width: 220
  height: 40
  style.fill: "#e3f2fd"
}
before: "postProcessBeforeInitialization" {
  width: 280
  height: 40
  style.fill: "#fff3e0"
}
init: "@PostConstruct / afterPropertiesSet\n/ init-method" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
after: "postProcessAfterInitialization\n(often the proxy)" {
  width: 280
  height: 50
  style.fill: "#f3e5f5"
}

new -> before -> init -> after
```

**Fig. 1.** Properties are set **before** both hooks. Returning **`null`** skips **later** processors for **that** bean ([[In what order does Spring initialize a bean and its dependencies]]).

BPPs (and beans they **directly** reference) are created in an **early** startup phase. They are **not** eligible for full post-processing (no AOP auto-proxy). Autowiring a wide type into a BPP can pull extra beans into that early set — WARN: *not eligible for getting processed by all BeanPostProcessors*.

> [!warning] `null` is not “skip this processor”
> Return **`null`** and **no subsequent** `BeanPostProcessor`s run for that bean; the factory may then keep **`null`**. Returning `null` from an unconditional processor poisons **every** bean. Return the incoming instance if you have nothing to do.

> [!warning] Order is not “unknown sequential”
> Dump text that says processors run in an unknown order is wrong. Implement **`PriorityOrdered` / `Ordered`**. Do **not** expect `@Order`. Do **not** inject collaborators into a BPP `@Bean` instance method — use **`static`**.

> [!tip] Interview answer
> BeanPostProcessor customizes each instance after injection: before-init, then init methods, then after-init where Spring wraps AOP proxies. I return the bean or a wrapper, never null by accident. It is not BeanFactoryPostProcessor — that edits definitions before any instance exists. I register it as a static @Bean so the configuration class is not initialized too early.
