<!--
reps: 0
priority: 0
-->
#Java/Language/Object #SRS

# Which `java.lang.Object` methods are most commonly used?

> [!abstract] Short answer
> There is **no official usage ranking**. In ordinary code you **call or override** **`equals`**, **`hashCode`**, and **`toString`** constantly (maps, sets, logs). You use **`getClass`** when you need the **runtime** `Class`. **`wait` / `notify` / `notifyAll`** show up only when you implement a monitor. **`clone` and `finalize` are not “common tools”** — `clone` is a shallow `protected` API; `finalize` is deprecated. A full list is [[How would you explain key methods declared on java.lang.Object]]; interview ranking is [[How would you explain the most important methods declared on java.lang.Object]].

## Everyday: identity and display

`hashCode` exists **for hash tables** such as `HashMap`. `equals` on `Object` is **`==`**. Any type you put in a `HashSet` / as a `HashMap` key either **keeps** that identity pair or **overrides both** ([[How would you explain default equals and hashCode inherited from Object]]). Logging, exceptions, and the debugger go through **`toString`**, whose default is `ClassName@hex`.

**`getClass`** is **`final`**. Frameworks and `equals` implementations that want the exact class call it often; you never override it.

These four are “most used” only in the sense that **almost every object is compared, hashed, printed, or reflected** — not because the spec prints a popularity table.

```d2
direction: down
hot: "Called all the time\nequals · hashCode · toString · getClass" {
  width: 320
  height: 70
  style.fill: "#e8f5e9"
}
mid: "When you own a monitor\nwait · notify · notifyAll" {
  width: 300
  height: 70
  style.fill: "#fff3e0"
}
cold: "Rare / avoid\nclone · finalize" {
  width: 240
  height: 70
  style.fill: "#ffebee"
}
```

**Fig. 1.** Usage in application code, not a JDK leaderboard.

```java
Map<String, Integer> counts = new HashMap<>();
counts.merge("a", 1, (a, b) -> a + b); // String hashCode / equals
Object o = counts;
String debug = o.toString();          // map’s toString, not Object’s
Class<?> c = o.getClass();            // java.util.HashMap
```

**Listing 1.** Conceptual: library types override `equals` / `hashCode` / `toString`; you still inherit `getClass`.

## Specialized and leftover

**`wait` / `notify` / `notifyAll`** are **`final`** on **`Object`** because the wait set is the **monitor**, not `Thread`. You use them inside `synchronized (theSameObject)` (or they throw `IllegalMonitorStateException`). Most business code never calls them; `java.util.concurrent` usually sits in front ([[How would you explain the Object wait method and waiting on monitors]]).

**`clone`** is **`protected`** and shallow. You do not “use it all the time”; arrays are the type that actually expose a public `clone()` ([[How would you explain the Object clone method and its issues]]).

**`finalize`** is **`protected`** and **deprecated for removal**. It is not part of a modern cleanup path ([[How would you explain the finalize method in Java and why it is discouraged]]).

> [!warning] “Most commonly used” is not a spec list
> Dumps that recite all eleven methods as equally “common,” or that put `clone` / `finalize` next to `equals`, are cataloging **declarations**, not **use**. `Object` declares them all; you **override three**, **call `getClass`**, and **leave the rest alone** unless you are writing a monitor, an array copy, or legacy cleanup.

> [!tip] Interview answer
> **The methods you actually live with are `equals`, `hashCode`, `toString`, and `getClass`.** Then mention `wait`/`notify` as monitor methods you rarely call yourself, and `clone`/`finalize` as APIs you know exist and usually avoid. There is no official frequency ranking.
