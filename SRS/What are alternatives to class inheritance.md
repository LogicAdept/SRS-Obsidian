<!--
reps: 0
priority: 0
-->
#Paradigms/OOP #Patterns/GoF #SRS

# What are alternatives to class inheritance

> [!abstract] Short answer
> The main alternative is **composition with delegation**: an object holds a reference to a helper and forwards work to it, and the helper can be swapped at runtime. Decorator, Strategy, Adapter, and Proxy are all built on this idea — which is why the GoF advice is to favor object composition over class inheritance.

## Why inheritance is limiting

Inheritance is static: you cannot change the behavior of an existing object at runtime, you can only replace the whole object with one from another subclass. It also gives a single parent in most languages, so you cannot inherit behavior from two classes at once. Both limits bite exactly when you need flexible, runtime-configurable behavior — the situation the classic GoF notification example describes, where adding SMS, Slack, and Facebook sending by subclassing explodes into a combinatorial set of subclasses.

## How composition and delegation replace it

With composition, the container object stores a reference typed to an interface and delegates part of the work to it. The reference can point to different implementations during the object's lifetime, which is what [[What is the Strategy pattern used for]] exploits to swap algorithms, and what a Decorator stack exploits to layer behaviors: each wrapper implements the same interface as the wrapped object, so layers compose recursively. In Java the same mechanics power the JDK: `Collections.sort(list, comparator)` takes the ordering strategy as a parameter, and `InputStream` subclasses such as `BufferedInputStream` wrap any other stream. Both [[How would you explain the Decorator design pattern]] and [[What is the Strategy pattern used for]] are direct applications of this idea, and it underlies several of [[What are the main oop principles]].

```java
interface Notifier { void send(String text); }

class EmailNotifier implements Notifier {
    public void send(String text) { /* send email */ }
}

class SmsDecorator implements Notifier {
    private final Notifier wrappee;
    SmsDecorator(Notifier wrappee) { this.wrappee = wrappee; }
    public void send(String text) {
        wrappee.send(text);
        /* also send SMS */
    }
}

Notifier n = new SmsDecorator(new EmailNotifier());
n.send("deploy finished");
```

**Listing 1.** Delegation instead of subclassing: `SmsDecorator` adds behavior to any `Notifier` it wraps, and the composition is decided at runtime.

> [!warning] Composition is not automatically better
> It costs extra objects and boilerplate, and for stable is-a hierarchies inheritance stays the correct tool — `ArrayList extends AbstractList` in the JDK is not a design mistake. The trap is the absolute claim "never use inheritance"; the honest rule is to prefer composition when behavior must vary at runtime.

> [!tip] Interview answer
> The main alternative to inheritance is composition with delegation: keep a reference to a helper behind an interface and forward work to it, so the helper can be replaced at runtime. Decorator, Strategy, Adapter, and Proxy are all variations of this. Inheritance remains fine for stable type hierarchies; reach for composition when behavior must vary per object or per moment.
