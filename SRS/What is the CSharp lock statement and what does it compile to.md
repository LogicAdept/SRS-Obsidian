<!--
reps: 0
priority: 0
-->
#ProgrammingLanguages/CSharp #SRS

# What is the CSharp lock statement and what does it compile to?

> [!abstract] Short answer
> C# **`lock (x) { … }`** takes a **mutual-exclusion lock**, runs the block, then **releases** it even if the body throws. The **same thread** may **reenter**. You **cannot `await`** inside. **Compile:** if `x` is **precisely** **`System.Threading.Lock`** (C# 13 / .NET 9+), it is **`using (x.EnterScope()) { … }`**. Otherwise it is **`Monitor.Enter(obj, ref taken)`** in **`try`/`finally`**, and **`Monitor.Exit`** only if **`taken`**. Java cousin: [[What is the synchronized keyword for in Java]]. Vs `Lock` API in Java: [[What is the difference between synchronized and ReentrantLock]]. Private mutex habit: [[Why might you synchronize on a private mutex object in Java]].

## Two expansions, one statement

**`lock (x)`** needs a **`Lock`** or any **reference**. Prefer a **dedicated** field (a **`Lock`** on modern runtimes, else a private **`object`**). Do **not** lock **`this`**, a **`Type`**, or a **`string`** (interning / callers / reflection share those). Hold it **briefly**.

The **`ref bool`** form exists so **`Exit` is skipped** if **`Enter` failed** (exception before the lock was taken). Casting a known **`Lock`** to **`object`** and locking that uses **`Monitor`**, not **`Lock`** — the compiler **warns**. **`Lock`** has **no owner token** you pass around; **`Enter`/`Exit`** must be **balanced** on the **same thread**. Deadlock if two locks are taken in **opposite orders**.

```csharp
lock (x) { Work(); }

// x is System.Threading.Lock:
using (x.EnterScope()) { Work(); }

// otherwise:
object o = x;
bool taken = false;
try { Monitor.Enter(o, ref taken); Work(); }
finally { if (taken) Monitor.Exit(o); }
```

**Listing 1.** Language reference expansions. `EnterScope` returns a disposable **`ref struct`**.

```d2
direction: down
stmt: "lock (x) { body }" {
  width: 180
  height: 36
  style.fill: "#fff8e1"
}
lockt: "x is Lock?" {
  width: 120
  height: 36
  style.fill: "#e3f2fd"
}
scope: "using EnterScope()" {
  width: 180
  height: 36
  style.fill: "#e8f5e9"
}
mon: "Monitor.Enter ref taken" {
  width: 200
  height: 36
  style.fill: "#ffebee"
}
stmt -> lockt
lockt -> scope: "yes"
lockt -> mon: "no"
```

**Fig. 1.** The statement is syntax. The IL/runtime path depends on the **static type** of `x`.

> [!warning] No `await` inside `lock`
> Locks are **per thread**. After `await` you may be on **another** thread and would not own the lock.

> [!warning] Do not lock `this`, `typeof(T)`, or a string
> Other code can take the **same** object and **deadlock** or **block** you. Use a **private** `Lock`/`object`.

> [!tip] Interview answer
> lock takes a mutex, runs the block, and always releases, and the same thread may enter again. If x is System.Threading.Lock it becomes using EnterScope, otherwise Monitor.Enter with a lockTaken flag in try finally. You cannot await inside, and you lock a private object, not this or a string.
