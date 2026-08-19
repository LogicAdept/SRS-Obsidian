<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`ApplicationContext` is an `ApplicationEventPublisher`. Beans that implement `ApplicationListener` (or use `@EventListener`) receive `ApplicationEvent`s — Observer. `BeanFactory` does not publish events.

After beans are in the container, dumps still mention ApplicationListeners as a late customization hook. Transaction-bound listeners are `@TransactionalEventListener` (separate card).

> [!warning] Unverified traps from the dump
> - Events are synchronous on the publisher thread by default unless you configure an async multicaster.
> - Publishing from a `@PostConstruct` can miss listeners that are not yet registered.
