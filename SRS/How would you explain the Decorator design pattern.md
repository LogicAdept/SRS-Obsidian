<!--
reps: 0
priority: 0
-->
#Patterns/GoF/Structural #SRS

# How would you explain the Decorator design pattern

> [!abstract] Short answer
> Decorator is a structural pattern that attaches new behavior by **wrapping an object in another object with the same interface**. Wrappers compose recursively into a stack, so combinations of behavior are assembled at runtime instead of being subclassed at compile time.

## The mechanism

The component interface is shared by the wrapped object and all wrappers. A base decorator holds a reference typed to that interface and delegates every call; concrete decorators add their behavior before or after the delegated call. Because the field type is the interface, a decorator can wrap a plain component or another decorator — that is the recursive composition that produces stacks like `Encryption(Compression(File))` for a data source, or the layered `InputStream` construction `new BufferedReader(new InputStreamReader(in))` in the JDK. The motivation is the failure mode of inheritance: it is static and single-parent, so covering every behavior combination with subclasses explodes combinatorially — the classic notifier example where email plus SMS plus Slack channels multiply into one subclass per combination.

```java
interface DataSource { void write(String data); }

class Compression implements DataSource {
    private final DataSource wrappee;
    Compression(DataSource wrappee) { this.wrappee = wrappee; }
    public void write(String data) {
        wrappee.write(compress(data));   // before the call
    }
    private String compress(String s) { return s; }
}
```

**Listing 1.** A decorator does its own work around the delegated call — here compressing before writing through to the wrapped source.

## The costs the catalog names

Two structural costs are worth naming in an interview. First, removing one specific wrapper from a stack is hard: the client holds the outermost reference, and the layers are opaque behind the shared interface. Second, decorator behavior can depend on the order of the stack — compressing before encrypting is not the same as encrypting before compressing — so the client, who assembles the stack, owns an ordering decision the type system cannot check. This is also why the pattern pairs naturally with [[What are alternatives to class inheritance]]: it is the canonical composition-over-inheritance demonstration.

> [!warning] Order matters and is invisible in the type
> The interface of the stack is the same no matter how you layer it, so a wrong order — logging after closing a stream, encryption after compression with a shared key — compiles fine and fails at runtime. The wrapper family comparison continues in [[What is the difference between the Proxy and Decorator design patterns]].

> [!tip] Interview answer
> Decorator layers behavior by wrapping an object in same-interface objects: the base decorator delegates, concrete decorators add work before or after the delegation, and the client composes a stack at runtime. It replaces subclass explosion with recursive composition, costs the ordering subtleties of a stack, and differs from Proxy by intent: Decorator adds behavior, Proxy controls access.
