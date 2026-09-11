<!--
reps: 0
priority: 0
-->
#Messaging #Patterns/Enterprise/Integration/Management/ProcessManager #SRS

# What is the Process Manager pattern?

> [!abstract] Short answer
> A **Process Manager** is a **central stateful coordinator**: it receives a trigger message, maintains the state of a multi-step process, and decides the **next step from intermediate results** — for flows whose steps are not known up front or are not a linear chain.

## When a routing slip runs out of assumptions

The routing slip assumes the step sequence is decided up front and linear. Many real processes are neither: the next step depends on intermediate outcomes, steps run in parallel, or branches loop. The process manager replaces the message-borne itinerary with a central unit: an incoming **trigger message** initializes the process; the manager sends the message to the first processing unit; each unit replies to the manager; the manager consults its rules and state, picks the next step, and sends again. All traffic runs through the hub — **hub-and-spoke** message flow — which is exactly what makes branching, parallel legs, and compensation manageable, and what makes the manager a potential bottleneck. It rounds off the routing family: simple linear flows stay with [[What is the Routing Slip pattern]], broadcasts with [[What is the Scatter-Gather pattern]]; the manager is the heavy tool, and using it for every integration is the classic overkill the EIP text itself warns about.

```d2
direction: down
trg: "Trigger message" {
  width: 180
  height: 55
  style.fill: "#e3f2fd"
}
pm: "Process Manager\nprocess state + rules" {
  width: 230
  height: 70
  style.fill: "#fff3e0"
}
a: "Step A" {
  width: 120
  height: 50
  style.fill: "#e8f5e9"
}
b: "Step B" {
  width: 120
  height: 50
  style.fill: "#e8f5e9"
}
c: "Step C" {
  width: 120
  height: 50
  style.fill: "#e8f5e9"
}
trg -> pm
pm -> a: "(1)"
a -> pm: "reply"
pm -> b: "(2)\nchosen by result"
b -> pm: "reply"
pm -> c: "(3)"```

**Fig. 1.** Every step is chosen by the hub after the previous reply: branching and parallelism become state-machine logic, not wiring.

## Hub-and-spoke responsibilities

```text
Responsibility      Lives in the process manager
------------------  --------------------------------------------
Process state       which instance, which step, which variables
Next-step decision  rules evaluated on intermediate results
Parallel legs       multiple outstanding steps per instance
Compensation        undo paths when a later step fails
Timeouts            per-step deadlines, stuck-instance policies
```

**Listing 1.** The manager is a state machine plus a scheduler — the more of these rows you need, the more a manager beats a slip.

> [!warning] The hub is both the power and the bottleneck
> Central state means a single store to persist, back up, and scale — and a single component every message transits twice. Keep process instances short-lived and their state minimal, partition if throughput demands, and resist modeling every three-step flow as a process; the book's own warning is that vendors sell everything as a process problem.

> [!tip] Interview answer
> A Process Manager is a central coordinator for multi-step message flows: a trigger message starts an instance, the manager tracks its state and decides each next step from intermediate results — branching, parallel steps, and compensation included. It is hub-and-spoke, so it is powerful but a potential bottleneck and a stateful component to operate. Routing slips cover linear known-itineraries; anything conditional or parallel belongs here.
