<!--
reps: 0
priority: 0
-->
#Patterns/GoF/Structural #SRS

# What is the Proxy pattern

> [!abstract] Short answer
> Proxy is a structural pattern that provides a substitute or placeholder for another object, with the same interface, controlling access to it. The proxy can do something before or after the request reaches the real service - defer its creation, cache results, check permissions, log calls.

## How the pattern works

The driving problem: a heavy object is needed occasionally, not always, and deferred initialization or access control scattered through every client is duplication - and sometimes impossible to add to a closed third-party class. The pattern creates a proxy class with the same interface as the service, hands the proxy to the clients, and lets it manage the real object: creating it lazily on first use, caching results, or gating calls. Because the interfaces match, the proxy is interchangeable with the real service, and the client cannot tell the difference.

```java
import java.util.HashMap;
import java.util.Map;

interface VideoService {
    String title(int id);
}

class HeavyVideoLibrary implements VideoService {
    @Override
    public String title(int id) {
        return "video-" + id;    // expensive to construct and to query
    }
}

class LazyVideoProxy implements VideoService {
    private HeavyVideoLibrary library;      // created on first use, not at wiring time

    @Override
    public String title(int id) {
        if (library == null) {
            library = new HeavyVideoLibrary();
        }
        return library.title(id);
    }
}
```

**Listing 1.** Same interface, deferred construction: the client holds a VideoService and never learns that a proxy sits in front of the library.

```d2
direction: right
client: "Client" {
  width: 150
  height: 70
  style.fill: "#e3f2fd"
}
proxy: "Proxy\nsame interface\ncreate / cache / check / log" {
  width: 270
  height: 100
  style.fill: "#fff3e0"
}
service: "Real service\nHeavyVideoLibrary" {
  width: 210
  height: 80
  style.fill: "#e8f5e9"
}
client -> proxy: request
proxy -> service: before / after work\ndelegates
```

**Fig. 1.** The proxy intercepts every request: whatever it does before or after, the delegation to the real service keeps the client unaware.

## The standard proxy varieties and their neighbors

Lazy-initialization (virtual proxy), result caching, protection proxies that check permissions, remote proxies standing in for objects on another machine, and logging proxies cover most real uses. The structural twin is Decorator - same composition, same interface - but the intents differ: a proxy usually manages its service's lifecycle itself, while decorators are stacked by the client to add behavior. Java's dynamic proxy mechanism is the standard tool for building proxies at runtime, covered in [[What is a dynamic proxy in Java reflection]]. The precise comparison lives in [[What is the difference between the Proxy and Decorator design patterns]]. And do not confuse the name with messaging: [[What is the Smart Proxy pattern]] is an enterprise-integration construct that forwards and replies on channels - a different pattern sharing only the word proxy.

> [!warning] Same interface, different intent than Decorator
> Answering "what is the difference" with "none, both delegate" is the classic failure: a proxy controls access - lifecycle, caching, authorization - while a decorator extends behavior and is layered by the client. Also mind the costs: an overzealous proxy hides remote or lazy failures behind the same interface, and every proxy is one more indirection to debug; if nothing happens before or after the call, the proxy is pure ceremony.

> [!tip] Interview answer
> A proxy is an interchangeable stand-in with the same interface as the real service, controlling access to it: lazy creation of a heavy object, caching, permission checks, or logging happen around the delegated call. Decorator shares the structure but adds behavior at the client's discretion, while the proxy typically owns the service's lifecycle. Java's dynamic proxies implement this pattern at runtime, which is how many AOP and remoting mechanisms work.
