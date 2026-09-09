<!--
reps: 0
priority: 0
-->
#Java/Testing/Mockito #SRS

# How would you explain when thenReturn vs doReturn when in Mockito

> [!abstract] Short answer
> **`when(mock.call()).thenReturn(x)` is the readable default; `doReturn(x).when(mock).call()` is the escape hatch.** The `when` form evaluates the real call inside the expression, so it breaks on spies whose real method has side effects and on re-stubbing of an exception stub. The `doReturn` family passes the stubber first and never touches the real method.

## Why the when form can explode

`when(...)` is not a language construct — it is a static method that receives the result of `mock.call()`. Mockito arranges the proxy so this call lands in "stubbing mode", but the call itself happens: on a mock the do-nothing default is harmless, on a **spy** the real method runs. The other failure is re-stubbing: once `foo()` is stubbed to throw, the inner `mock.foo()` inside `when(mock.foo())` replays the throw.

```d2
direction: right
w1: "when(spy.get(0))\nJava evaluates spy.get(0)\nBEFORE when() runs" {
  width: 300
  height: 100
  style.fill: "#ffebee"
}
w2: "Real method fires ->\nside effect or exception" {
  width: 290
  height: 90
  style.fill: "#ffebee"
}
d1: "doReturn(\"foo\").when(spy).get(0)\nstubber installed first,\nproxy call stays inside stubbing mode" {
  width: 340
  height: 100
  style.fill: "#e8f5e9"
}
d2: "Real method never runs" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}
w1 -> w2
d1 -> d2
```

**Fig. 1.** The evaluation order is the whole story: `when(...)` needs the call's result, `doReturn(...).when(spy)` registers the stubber before the method is named.

```java
// Case 1: re-stubbing an exception stub with when(...) blows up
Db db1 = mock(Db.class);
when(db1.query("select 1")).thenThrow(new IllegalStateException("db down"));
try {
    when(db1.query("select 1")).thenReturn("rows");
} catch (Throwable e) {
    System.out.println("re-stub with when(): " + e.getClass().getSimpleName());
}

// Case 2: doReturn(...) re-stubs fine
Db db2 = mock(Db.class);
when(db2.query("select 1")).thenThrow(new IllegalStateException("db down"));
doReturn("rows").when(db2).query("select 1");
System.out.println("re-stub with doReturn(): " + db2.query("select 1"));
```

**Listing 1.** Both cases verified on JDK 21 with Mockito 5.11:

```java
re-stub with when(): IllegalStateException
re-stub with doReturn(): rows
```

**Listing 2.** The inner `db1.query(...)` replayed the `db down` throw; the `doReturn` form never invoked the method.

The spy version of the same trap: `when(emptySpy.get(0))` throws `IndexOutOfBoundsException` because `get(0)` really executes on an empty list — see [[How would you explain mock vs spy]] for that run.

> [!warning] doReturn is the exception, not the new normal
> Mockito's javadoc is explicit: prefer `when(...)` because it is compile-time type-safe against the method's return type and reads as consecutive calls; `doReturn` takes an untyped `Object` and silently accepts a wrong type until the call happens. Mockito positions `doReturn` for "rare occasions": spying real objects where a real call has side effects, and overriding a previous exception-stubbing. Overriding stubbing in general is a smell — if a test keeps re-stubbing, the arrange phase is fighting itself. For void methods there is no choice at all: `doThrow(...).when(mock).voidCall()`, since `when(mock.voidCall())` cannot compile.

## The full do-family

`doReturn` / `doThrow` / `doAnswer` / `doNothing` / `doCallRealMethod` all share the `doX(...).when(mock).method(...)` shape. `doAnswer` covers computed returns (inspect arguments, mutate captured state), `doNothing` is the default for void methods but useful when sequence-stubbing, `doCallRealMethod` re-enables the real implementation on a spy or partial mock. Verification of those interactions goes through [[How would you explain verify]], and captured arguments through [[How would you explain ArgumentCaptor]].

> [!tip] Interview answer
> **when/thenReturn is the standard, type-safe stubbing form. doReturn/when exists for two cases: spies, where when(...) would execute the real method (side effects, exceptions on empty state), and re-stubbing something already stubbed to throw. doReturn is weaker — untyped, no compile check — so Mockito treats it as the rare escape hatch, not the default. Void methods always use the do-family because when() can't take them.**

