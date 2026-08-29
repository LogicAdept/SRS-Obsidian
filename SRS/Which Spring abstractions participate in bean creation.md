<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC #SRS

# Which Spring abstractions participate in bean creation?

> [!abstract] Short answer
> **Creation** is `createBean` on `AutowireCapableBeanFactory` (implemented by `AbstractAutowireCapableBeanFactory`): **recipe → instantiate → populate → initialize.** The recipe is a **`BeanDefinition`**. Construction uses an **`InstantiationStrategy`** (default CGLIB subclassing strategy). **`InstantiationAwareBeanPostProcessor`** can **replace** instantiation, run **after** `new` / factory-method, and **edit properties** (field injection). **`SmartInstantiationAwareBeanPostProcessor`** picks **constructors**. A **`FactoryBean`** manufactures the **product** during instantiate. **`BeanPostProcessor`** wraps the **already populated** instance around init. **`BeanFactoryPostProcessor` does not create beans** — it only edits definitions first ([[What is the difference between BeanFactoryPostProcessor and BeanPostProcessor]], [[What is the Spring bean lifecycle and extension points]]).

## SPIs on the `createBean` path

`BeanFactory` is the **container API**; it **holds** definitions and **returns** instances. Application code should still **push** constructors, not `getBean` ([[How does Spring work under the hood]]).

| Abstraction | Role in **creation** |
|---|---|
| **`BeanDefinition`** | Metadata: class, factory-method, ctor args, properties, scope ([[What is Spring BeanDefinition]]) |
| **`InstantiationStrategy`** | Performs the actual construct (`CglibSubclassingInstantiationStrategy` by default) |
| **`SmartInstantiationAwareBeanPostProcessor`** | `determineCandidateConstructors` (e.g. `@Autowired` ctor selection) |
| **`InstantiationAwareBeanPostProcessor`** | `postProcessBeforeInstantiation` (non-null → **skip** default `new`; only **after-init** BPP still runs); `postProcessAfterInstantiation`; `postProcessProperties` (since 5.1) |
| **`MergedBeanDefinitionPostProcessor`** | Touch the **merged** definition just before instantiate |
| **`FactoryBean`** | Declared bean **is** the factory; `getObject()` is the exposed instance ([[What is FactoryBean and how do you retrieve the factory itself]]) |
| **`BeanPostProcessor`** | After populate: before-init (`@PostConstruct`) then after-init (**AOP proxy**) ([[What is Spring BeanPostProcessor]]) |
| **`Aware` / `InitializingBean` / `init-method`** | `BeanFactory` javadoc steps 1–13 between populate and after-init |

```java
public class SkipNewProcessor implements InstantiationAwareBeanPostProcessor {
	@Override
	public Object postProcessBeforeInstantiation(Class<?> beanClass, String beanName) {
		return null; // proceed with InstantiationStrategy
	}

	@Override
	public boolean postProcessAfterInstantiation(Object bean, String beanName) {
		return true; // allow populateBean
	}
}
```

**Listing 1.** Conceptual. Returning a non-null object from `postProcessBeforeInstantiation` **is** creation — default construction never runs.

```d2
direction: down
bd: "BeanDefinition" {
  width: 180
  height: 36
  style.fill: "#e3f2fd"
}
ia: "InstantiationAware BPP\n(+ Smart ctor pick)" {
  width: 240
  height: 50
  style.fill: "#fff3e0"
}
new: "InstantiationStrategy / FactoryBean" {
  width: 260
  height: 40
  style.fill: "#e8f5e9"
}
pop: "populateBean\n(postProcessProperties)" {
  width: 240
  height: 50
  style.fill: "#f3e5f5"
}
bpp: "BeanPostProcessor + init" {
  width: 220
  height: 40
  style.fill: "#c8e6c9"
}

bd -> ia -> new -> pop -> bpp
```

**Fig. 1.** `BeanFactoryPostProcessor` sits **before** this diagram ([[What is BeanDefinitionRegistryPostProcessor]]). `DestructionAwareBeanPostProcessor` sits on **shutdown**, not create.

`AutowiredAnnotationBeanPostProcessor` is an **instantiation-aware** BPP: constructors, then **fields then methods** in populate. That is how annotation injection **participates** in creation without being a fourth container.

> [!warning] `BeanFactoryPostProcessor` is not a creation SPI
> It runs on **`BeanDefinition`s** with **no** ordinary instances. `getBean` there pre-creates objects and **skips** later processors. Do not put it on this list.

> [!warning] Plain `BeanPostProcessor` is too late to `new` the target
> Before-init already has a constructed, injected object. To **suppress** default instantiation or to inject **fields**, implement **`InstantiationAwareBeanPostProcessor`**. Javadoc: that interface is **special-purpose**; prefer plain BPP when you only wrap.

> [!tip] Interview answer
> Bean creation is BeanDefinition plus AutowireCapableBeanFactory.createBean. InstantiationStrategy constructs, InstantiationAwareBeanPostProcessor can replace new or inject fields, FactoryBean.getObject can be the instance, then BeanPostProcessor and init callbacks finish. BeanFactoryPostProcessor only edits recipes beforehand. I do not call Tomcat a Spring creation abstraction.
