<!--
reps: 0
priority: 0
-->
#Java/Testing/Mockito #SRS

# How would you explain mock vs spy

> [!abstract] Short answer
> **A mock is a full stand-in: every method returns a default value until stubbed. A spy wraps a real object: unstubbed calls execute real code, stubbed calls return your answers.** For spies, stub with the `doReturn(...).when(spy).method()` form — the usual `when(spy.method())` actually calls the real method first.

## Same interface, different behavior

`mock(List.class)` gives you a fake `List` that records calls and returns defaults: `null`, `0`, `false`, empty collections. `spy(new LinkedList<String>())` gives you a proxy over a real instance — `add`, `get`, `size` all run for real, and you override only what you need.

```d2
direction: right
mock: "mock(List.class)\nno real code inside\ndefaults: null / 0 / empty" {
  width: 280
  height: 100
  style.fill: "#e3f2fd"
}
spy: "spy(new LinkedList())\nreal object wrapped\ncalls delegate for real" {
  width: 280
  height: 100
  style.fill: "#fff3e0"
}
stub: "Stubbed method?\n-> stubbed answer wins" {
  width: 270
  height: 90
  style.fill: "#e8f5e9"
}
mock -> stub: "stub via when(mock.x())"
spy -> stub: "stub via doReturn().when(spy).x()"
```

**Fig. 1.** Both are Mockito proxies with a recording journal; the difference is what an unstubbed call does.

```java
List<String> mock = mock(List.class);
mock.add("one");
mock.add("two");
System.out.println("mock.get(0) = " + mock.get(0));   // default: null
System.out.println("mock.size() = " + mock.size());   // default: 0

List<String> spy = spy(new LinkedList<String>());
spy.add("one");
spy.add("two");
System.out.println("spy.get(0)  = " + spy.get(0));    // real method ran
System.out.println("spy.size()  = " + spy.size());    // real method ran

doReturn(100).when(spy).size();                       // stubbing a spy
System.out.println("spy.size() stubbed = " + spy.size());
```

**Listing 1.** Run on JDK 21 with Mockito 5.11:

```java
mock.get(0) = null
mock.size() = 0
spy.get(0)  = one
spy.size()  = 2
spy.size() stubbed = 100
```

**Listing 2.** The mock dropped both `add` calls on the floor; the spy really stored "one" and "two", and only `size()` was overridden.

> [!warning] when(...) on a spy executes the real method
> `when(spy.get(0)).thenReturn("foo")` has to evaluate `spy.get(0)` to enter the stubbing mode — and that is a real call. On an empty list it throws `IndexOutOfBoundsException` before Mockito can stub anything. The `doReturn` family avoids the inner call entirely. Mockito's docs also note two more traps: a spy is a **copy** of the passed instance, not a delegate — interactions with the original object are invisible to the spy — and final methods can neither be stubbed nor verified on a spy.

```java
List<String> emptySpy = spy(new LinkedList<String>());
try {
    when(emptySpy.get(0)).thenReturn("foo");   // real get(0) -> boom
} catch (Exception e) {
    System.out.println("when() trap: " + e.getClass().getSimpleName());
}
doReturn("foo").when(emptySpy).get(0);
System.out.println("doReturn works: " + emptySpy.get(0));
```

**Listing 3.** The trap and the fix, verified on JDK 21:

```java
when() trap: IndexOutOfBoundsException
doReturn works: foo
```

**Listing 4.** Same spy, same method: only the `doReturn(...).when(spy)` form survives.

## When to use which

Mocks are the default for collaborators (repositories, gateways) — a test should not depend on their internals. Spies are for partial mocking: a real object whose expensive or external method you shave off (`doReturn` on one method, everything else real). Mockito itself recommends spies sparingly, mainly for legacy code you cannot restructure; for new code, if you keep stubbing half of a class, that class wants to be split. The Spring wrappers follow the same split — see [[What is the difference between MockBean and SpyBean]] and [[What is SpyBean]], and [[What is the difference between Mock and MockBean]] for the unit-test versus context-test boundary. Stubbing syntax differences continue in [[How would you explain when thenReturn vs doReturn when in Mockito]].

> [!tip] Interview answer
> **mock gives a blank fake: all methods return defaults until stubbed. spy wraps a real object and delegates every unstubbed call to it. On a spy you stub with doReturn(...).when(spy).method(), because when(spy.method()) triggers the real method first — on an empty collection that already throws. Also remember spy copies the instance and cannot stub final methods.**

