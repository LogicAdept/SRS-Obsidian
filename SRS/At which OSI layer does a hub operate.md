<!--
reps: 0
priority: 0
-->
#Networking/OSI #SRS

# At which OSI layer does a hub operate?

> [!abstract] Short answer
> **Layer 1 — Physical.** An Ethernet **hub** is a multiport **repeater**: it regenerates bit-level signals onto other ports and does **not** forward by MAC address or IP. In OSI terms a repeater is a Physical-layer intermediate system.

## Hub vs switch vs router (interview map)

```d2
direction: down
l1: "Layer 1 Physical\nhub / repeater\nbit / signal repeat" {
  width: 280
  height: 90
  style.fill: "#e3f2fd"
}
l2: "Layer 2 Data Link\nbridge / L2 switch\nMAC frame forward" {
  width: 280
  height: 90
  style.fill: "#fff3e0"
}
l3: "Layer 3 Network\nrouter / L3 switch\nIP routing" {
  width: 280
  height: 90
  style.fill: "#e8f5e9"
}
l1 -> l2
l2 -> l3
```

**Fig. 1.** Classic device placement in the OSI stack for interview answers.

RFC 1208 (glossary): a **repeater** propagates electrical signals from one cable to another without routing or packet filtering — in OSI terminology a **Physical Layer** intermediate system. A **bridge** is Data Link; a **router** is Network. RFC 1907’s `sysServices` examples map layer 1 to physical functions such as **repeaters**. IEEE 802.3 repeater MIBs (e.g. RFC 1368) treat the repeater as **physical-layer** / bitwise store-and-forward, not as a MAC bridge.

A hub does not interpret frames or look up MAC destinations: an incoming electrical (or optical) signal is regenerated out the other ports. That is why exam answers pair hub → L1, switch → L2 ([[At which OSI layer does a switch primarily operate]]), router → L3 ([[At which OSI layer does a router primarily operate]]).

```text
Host A ──► Hub ──► Host B
              └──► Host C   (same regenerated signal on every other port)
```

**Listing 1.** Conceptual star wiring: one shared physical medium behavior despite a star cable layout.

## Collision domain (why hubs vanished)

Because the hub only repeats signals, simultaneous transmitters collide electrically. All ports of a classic hub sit in **one collision domain**; attached hosts share bandwidth with CSMA/CD on half-duplex Ethernet. A Layer 2 switch breaks that into per-port collision domains by buffering and forwarding frames. See [[Which OSI layer handles MAC addressing and local frame forwarding]] and [[What is the importance of the OSI Physical layer]].

> [!warning] “Smart hub” / dual-speed marketing
> Some products labeled “hub” internally bridge between speed domains. The **exam default** for a plain Ethernet hub remains Layer 1 multiport repeater — no MAC learning. If a device learns MACs or routes IP, it is not operating as a simple hub.

> [!warning] Physical star ≠ separate collision domains
> Star cabling through a hub still shares one collision domain. Topology shape does not promote the device to Layer 2.

> [!tip] Interview answer
> **A hub operates at OSI Layer 1 (Physical)** as a multiport repeater: it regenerates signals to all other ports with no MAC or IP decisions. Switches primarily work at Layer 2; routers at Layer 3. Hubs create one shared collision domain, which is why modern LANs use switches instead.
