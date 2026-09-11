<!--
reps: 0
priority: 0
-->
#Messaging #Patterns/Enterprise/Integration #SRS

# What is the Detour pattern?

> [!abstract] Short answer
> A **Detour** is a **context-controlled router with two outputs**: normally messages go straight to the destination, but when signaled via the [[What is the Control Bus pattern]] they are routed through extra steps — validation, testing, debugging — and then continue to the same destination.

## Insert a detour without rewiring

A Wire Tap inspects copies; sometimes you need to **modify or reroute the real traffic** — run messages through an extra validator, capture the flow into a test rig, or exercise a new component on live data. The detour is a small context-based router placed in the flow with two output channels: the bypass (unmodified message, original destination) and the detour path (through additional components, ending at the same destination). Its context flag flips via the control bus, so the detour is temporary by construction and reversible without deployment. The pattern's whole value is that extra steps are **planned infrastructure, not emergencies**: the router, the extra components, and their output contract exist before the incident. Its inspection-only sibling is the [[What is the Wire Tap pattern]]; both exist to keep the main [[What is the Pipes and Filters pattern]] flow untouched.

```d2
direction: right
in: "Incoming message" {
  width: 190
  height: 55
  style.fill: "#e3f2fd"
}
r: "Detour router\ncontext flag" {
  width: 200
  height: 65
  style.fill: "#fff3e0"
}
ex: "Extra steps\nvalidate / test / debug" {
  width: 210
  height: 65
  style.fill: "#ffebee"
}
dest: "Original destination" {
  width: 200
  height: 60
  style.fill: "#e8f5e9"
}
in -> r
r -> dest: "normal: straight"
r -> ex: "detour: via steps"
ex -> dest```

**Fig. 1.** Both paths end at the same destination; only the middle of the journey changes.

## The two states, operationally

```text
State         Path                    Typical use
------------  ----------------------  ---------------------------------
Straight      in -> destination       default production behavior
Detour        in -> extra -> dest     hunting a bug, new validator trial
Switched by   control bus message     no redeploy, reversible
```

**Listing 1.** The detour is designed, installed, and idle long before anyone needs it — flipping it on is one command.

> [!warning] Detours change production semantics while active
> Traffic through the extra steps gains their latency, their failure modes, and possibly modification — a "temporary" debugging detour that forgets to flip back becomes the undocumented production path. Make detours auto-expiring (a timeout on the context flag), alert on their state, and never run side-effecting logic on the detour path unless the flow tolerates it.

> [!tip] Interview answer
> A Detour is a two-output router in the flow: straight to the destination normally, through extra validation or debugging steps when a control-bus signal says so, then to the same destination. It lets you insert inspection or modification temporarily without redeploying — the reversible, in-path cousin of the Wire Tap. Auto-expire the state so a forgotten detour does not become production.
