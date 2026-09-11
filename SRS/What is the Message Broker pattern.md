<!--
reps: 0
priority: 0
-->
#Messaging #Patterns/Enterprise/Integration/Messaging #SRS

# What is the Message Broker pattern?

> [!abstract] Short answer
> A **Message Broker** is a **central hub** that receives messages from multiple destinations, determines the correct destination, and routes them to the right channel — an **architecture pattern** (hub-and-spoke) whose internals are composed from the individual routing patterns.

## Central control over the flow, at a named price

The routing patterns each solve one routing problem; the broker is what you get when that logic is gathered into one entity every participant talks to. Senders no longer know destinations; the broker — using routers, translators, and stores internally — owns the flow topology, which is why the style is called hub-and-spoke and why the broker is sometimes called an architecture pattern comparable to Pipes and Filters rather than a design pattern. The classic advantage is central maintenance: rules change in one place. The classic disadvantage is the same centrality: route everything through one broker and it becomes a bottleneck. The standard mitigations are explicit: the pattern says **develop** a single routing entity, not **deploy** one instance — a stateless broker design can run as multiple instances, with point-to-point channel semantics guaranteeing each message is consumed by exactly one of them; and large estates often split into several specialized brokers instead of one über-broker, trading away single-point maintenance to avoid broker spaghetti. The bus-shaped evolution of the same idea is the [[What is the Message Bus pattern]]; the routing building blocks are [[What is the Message Router pattern]] and friends.

```d2
direction: down
s1: "Sender A" {
  width: 130
  height: 50
  style.fill: "#e3f2fd"
}
s2: "Sender B" {
  width: 130
  height: 50
  style.fill: "#e3f2fd"
}
br: "Message Broker\nrouting rules, translation" {
  width: 260
  height: 75
  style.fill: "#fff3e0"
}
r1: "Channel 1" {
  width: 130
  height: 50
  style.fill: "#e8f5e9"
}
r2: "Channel 2" {
  width: 130
  height: 50
  style.fill: "#e8f5e9"
}
r3: "Channel 3" {
  width: 130
  height: 50
  style.fill: "#e8f5e9"
}
s1 -> br
s2 -> br
br -> r1
br -> r2
br -> r3```

**Fig. 1.** All senders point at the hub; only the hub knows where messages actually go.

## Scaling the hub honestly

```text
Bottleneck risk            Mitigation
-------------------------  ----------------------------------------------
Single broker instance     deploy N stateless instances; P2P channels
                           ensure one consumer per message
Complexity of one broker   several specialized brokers per domain
Central maintenance        keep — this is the point of the pattern
```

**Listing 1.** The pattern prescribes one routing *entity*, not one *process*; the entity can be a cluster.

> [!warning] Hub-and-spoke concentrates failure and politics
> The broker's availability window is the estate's availability window, and its rule base becomes the most contested configuration in the organization — every team's change lands there. Cluster it for availability, partition it by domain for change safety, and version its rules like code; "one place to change everything" cuts both ways.

> [!tip] Interview answer
> A Message Broker is a central routing hub: senders deliver to the broker, which determines destinations and routes to the right channels — an architecture pattern built internally from routers, translators, and stores. It buys central control and maintenance at the cost of a potential bottleneck; the standard answers are deploying multiple stateless instances (point-to-point channels keep consumption correct) or splitting into specialized brokers.
