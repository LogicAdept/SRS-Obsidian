<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC #Patterns/GoF/Behavioral/Observer #SRS

# How does `ApplicationContext` publish events?

> [!abstract] Short answer
> `ApplicationContext` **is** an `ApplicationEventPublisher`. `publishEvent` hands the event to a context-wide `ApplicationEventMulticaster` (default `SimpleApplicationEventMulticaster`), which notifies matching `ApplicationListener` beans and `@EventListener` methods — the Observer pattern. A plain `BeanFactory` has no event bus. By default the call is **synchronous on the publisher thread**.

## Publisher, multicaster, listeners

`ApplicationContext` inherits event publication from `ApplicationEventPublisher`. The context package adds that capability on top of `BeanFactory`; see [[What is the difference between BeanFactory and ApplicationContext]]. Two overloads exist:

- `publishEvent(ApplicationEvent)` — framework events (`ContextRefreshedEvent`, `ContextClosedEvent`, …) or your subclass.
- `publishEvent(Object)` — since Spring **4.2**, an arbitrary payload is wrapped in `PayloadApplicationEvent`.

The object you publish with is usually the container itself. Implement `ApplicationEventPublisherAware` and Spring injects the context through `setApplicationEventPublisher`. You can also call `publishEvent` on an `ApplicationContext` you already hold.

At runtime, `AbstractApplicationContext` looks for a bean named `applicationEventMulticaster`. If none is defined, it uses `SimpleApplicationEventMulticaster`. That class defaults to **`SyncTaskExecutor`**: every matching listener runs in the **calling thread**, and `publishEvent` **blocks** until they finish. A listener then sees the publisher’s thread-locals, including an active transaction if one exists. `BeanFactory` does not implement `ApplicationEventPublisher` and does not run this path.

Receive side:

- A bean that implements `ApplicationListener<E>` is notified for matching `E`.
- Since **4.2**, any managed bean method annotated `@EventListener` is registered as an `ApplicationListener` by `EventListenerMethodProcessor`.
- Built-in lifecycle events include `ContextRefreshedEvent` (context initialized or refreshed: beans loaded, singletons pre-instantiated, context ready), `ContextStartedEvent` / `ContextStoppedEvent`, and `ContextClosedEvent` ([[How do you shut down a Spring ApplicationContext]]). That refresh event is the container’s “everything is up” signal — not a second `BeanPostProcessor`.

Transaction **phase** binding (`AFTER_COMMIT` and the rest) is `@TransactionalEventListener`, not the default multicaster: [[How does TransactionalEventListener work]].

```java
public class BlockedListEvent extends ApplicationEvent {
    private final String address;
    public BlockedListEvent(Object source, String address) {
        super(source);
        this.address = address;
    }
    public String getAddress() { return address; }
}

public class EmailService implements ApplicationEventPublisherAware {
    private ApplicationEventPublisher publisher;
    @Override
    public void setApplicationEventPublisher(ApplicationEventPublisher publisher) {
        this.publisher = publisher;
    }
    public void sendEmail(String address) {
        publisher.publishEvent(new BlockedListEvent(this, address));
    }
}

public class BlockedListNotifier implements ApplicationListener<BlockedListEvent> {
    @Override
    public void onApplicationEvent(BlockedListEvent event) {
        // notify for event.getAddress()
    }
}
```

**Listing 1.** Conceptual. The container injects itself as `ApplicationEventPublisher`; a typed `ApplicationListener` receives the custom event.

```java
public class BlockedListNotifier {
    @EventListener
    public void processBlockedListEvent(BlockedListEvent event) {
        // same receive path, no ApplicationListener interface
    }
}

@Bean
ApplicationEventMulticaster applicationEventMulticaster() {
    SimpleApplicationEventMulticaster multicaster = new SimpleApplicationEventMulticaster();
    multicaster.setTaskExecutor(taskExecutor);
    multicaster.setErrorHandler(errorHandler);
    return multicaster;
}
```

**Listing 2.** Conceptual. `@EventListener` (4.2+) on a managed bean; optional `applicationEventMulticaster` bean for a thread pool and an `ErrorHandler`. Per-method `@Async` on an `@EventListener` is the other async switch.

```d2
direction: right
pub: "Bean\npublishEvent" {
  width: 160
  height: 70
  style.fill: "#e3f2fd"
}
ctx: "ApplicationContext\nApplicationEventPublisher" {
  width: 240
  height: 80
  style.fill: "#fff3e0"
}
mc: "ApplicationEventMulticaster\n(default Simple, sync)" {
  width: 260
  height: 80
  style.fill: "#fff3e0"
}
l1: "ApplicationListener" {
  width: 180
  height: 55
  style.fill: "#e8f5e9"
}
l2: "@EventListener" {
  width: 180
  height: 55
  style.fill: "#e8f5e9"
}

pub -> ctx -> mc
mc -> l1
mc -> l2
```

**Fig. 1.** Publication is a hand-off to the multicaster. Default `SimpleApplicationEventMulticaster` invokes listeners on the publisher thread; a custom executor or `@Async` changes that.

`EventListenerMethodProcessor` is a `SmartInitializingSingleton`: it registers `@EventListener` methods in `afterSingletonsInstantiated()`, after regular singleton creation (including `@PostConstruct` / `InitializingBean`). A lazy `@EventListener` bean is **not** registered — the context honors lazy and skips the method.

To change **global** dispatch, define that `applicationEventMulticaster` bean (`setTaskExecutor`, `setErrorHandler`). Listeners that return `supportsAsyncExecution() == false` (for example transaction-synchronized ones) still run on the original publisher thread even when an executor is set. `@EventListener` can also return an event (or a collection/array) to publish a follow-up; that return-value publication is **not** supported on `@Async` listeners.

> [!warning] Default multicast is blocking and fail-fast
> A slow or blocking listener stalls `publishEvent` and the publisher’s transaction. With no `ErrorHandler` and no async executor, a thrown exception **stops** the current multicast and propagates to the publisher. `@Async` listeners do **not** propagate exceptions to the caller. Async paths also drop the publisher’s thread-locals unless the executor copies them.

> [!warning] Too early to publish: `@PostConstruct` versus `@EventListener`
> Publishing from `@PostConstruct` (or another init callback) can miss `@EventListener` methods: `EventListenerMethodProcessor` registers them only in `afterSingletonsInstantiated()`, after regular singletons already exist. Do not mark `@EventListener` beans lazy. Prefer `ContextRefreshedEvent` or a call after the context is up ([[How do you call a method after a Spring bean is initialized]]).

> [!tip] Interview answer
> ApplicationContext extends ApplicationEventPublisher: publishEvent hands the event to an ApplicationEventMulticaster. Listeners are ApplicationListener beans or @EventListener methods in the same context. The default SimpleApplicationEventMulticaster is synchronous on the caller thread, so a listener shares the publisher’s transaction and can block it. BeanFactory has no event publication; for after-commit work use TransactionalEventListener, not the default bus.
