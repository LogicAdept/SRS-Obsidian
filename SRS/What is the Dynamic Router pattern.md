<!--
reps: 0
priority: 0
-->
#Messaging #Patterns/Enterprise/Integration/Routing/DynamicRouter #SRS

# What is the Dynamic Router pattern?

> [!abstract] Short answer
> A **Dynamic Router** is a router that **self-configures**: participating destinations announce themselves and their conditions on a control channel, the router stores these rules in a rule base, and incoming messages are evaluated against it — no recompile or redeploy when a new recipient appears.

## Destinations register, the router predicts

A plain router depends, at configuration time, on knowing all its destinations; a dynamic router inverts that. Besides input and output channels it consumes a **control channel**: at start-up (and on changes) each potential recipient sends a message announcing its presence and the conditions under which it handles traffic. The router stores these preferences in a rule base and, per incoming message, evaluates rules and routes to the matching recipient. The result is efficient **predictive** routing — every message evaluates stored rules — without the maintenance dependency of the router on each recipient. This is the decoupled-management sibling of the [[What is the Message Router pattern]] and the rule-base cousin of the [[What is the Routing Slip pattern]]; the control channel itself is a small [[What is the Control Bus pattern]], and rule churn is why the rule base needs lifecycle handling.

```d2
direction: down
d1: "Recipient A\nannounces: type=X" {
  width: 220
  height: 65
  style.fill: "#e3f2fd"
}
d2: "Recipient B\nannounces: amount>1000" {
  width: 240
  height: 65
  style.fill: "#e3f2fd"
}
cc: "Control channel\nregistrations" {
  width: 220
  height: 60
  style.fill: "#fff3e0"
}
rb: "Dynamic Router\nrule base" {
  width: 220
  height: 65
  style.fill: "#fff3e0"
}
in: "Incoming message" {
  width: 200
  height: 55
  style.fill: "#ffebee"
}
d1 -> cc
d2 -> cc
cc -> rb
in -> rb: "evaluate rules"
rb -> d1: "match"```

**Fig. 1.** Registration flows in through the control channel; messages are matched against the accumulated rule base.

## Rule base lifecycle

```text
Event                  Router action
---------------------  --------------------------------------------
Recipient starts       registers conditions on control channel
Recipient stops        deregistration message, or lease expires
Message arrives        evaluate rules in priority order
No rule matches        explicit no-match destination (never silent)
Rule conflict          deterministic resolution, logged
```

**Listing 1.** Registrations must expire: a crashed recipient that never deregisters otherwise keeps receiving traffic chosen by its stale rules.

> [!warning] The rule base is a distributed-state cache — treat it like one
> Stale registrations route to dead recipients, conflicting rules resolve nondeterministically unless prioritized, and a rule-base reboot must not erase topology. Leases with expiry, explicit no-match destinations, and a rebuildable persistent rule store are the difference between self-configuration and self-inflicted chaos.

> [!tip] Interview answer
> A Dynamic Router avoids compile-time dependency on all destinations: recipients announce their handling conditions on a control channel, the router keeps them in a rule base, and each message is evaluated against those stored rules. New recipients appear without reconfiguring the router. The hard parts are rule lifecycle — leases, deregistration, conflicts — and an explicit path for no-match messages.
