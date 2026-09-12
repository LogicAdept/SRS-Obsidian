<!--
reps: 0
priority: 0
-->
#Networking/OSI #SRS
# What is the importance of the OSI Physical layer

> [!abstract] Short answer
> The Physical layer (Layer 1) turns frames into real signals — voltages on copper, light in fiber, radio waves in the air — and back. It defines media, connectors, line codes, bit rates and timing; without a shared physical contract there is no meaningful "bit" to transmit, so everything above it is theoretical.

## What Layer 1 actually specifies

- **Media and connectors:** twisted pair categories (Cat 5e/6/6a), fiber single-mode vs multi-mode, radio bands for Wi-Fi, pinouts (T568A/B), SFP/QSFP module shapes.
- **Signaling and line coding:** how a 0 and a 1 are represented and clocked — voltage levels, modulation (QAM on Wi-Fi/DSL), optical pulses; multi-bit symbols (e.g. 1000BASE-T sends symbols per clock) matter for the nominal rate.
- **Bit rate and duplex:** 100 Mb/s, 1/10/25/100 Gb/s; full vs half duplex (half is legacy — CSMA/CD lived here).
- **Synchronization:** where one symbol ends and the next begins; clock recovery from the signal itself.

```d2
direction: right
frame: "Data Link hands over a frame\n(as a sequence of bits)" { width: 320; height: 90; style.fill: "#e3f2fd" }
phy: "Physical layer\nencode symbols, drive the medium" { width: 320; height: 90; style.fill: "#fff3e0" }
wire: "Copper / fiber / radio\nactual signal" { width: 260; height: 80; style.fill: "#e8f5e9" }
frame -> phy -> wire
```

**Fig. 1.** Layer 1 is a serializer/deserializer between the digital world of frames and analog reality of the medium.

## Why it matters in practice

Attenuation, noise and cable quality set the real throughput far more than switch model names do; a damaged patch cable or a bad SFP produces FCS errors that only show up as retransmissions at higher layers. Duplex or speed mismatches (autonegotiation failures) appear as late collisions and stuttering performance. Wi-Fi channel width and band choice are Layer 1 decisions that dominate latency in offices. When a network is "slow", a structured bottom-up pass starts here (see [[How do you use a bottom-up OSI approach when troubleshooting]]).

> [!warning] A repeater is not a switch
> Hubs and repeaters work purely at Layer 1: they copy electric signal, they neither read MAC addresses nor create separate collision domains. If an answer says "the hub filters traffic by MAC", it confused Layer 1 with Layer 2 — [[At which OSI layer does a hub operate]] covers exactly this trap.

Layer 1 only moves bits; framing, addressing and error detection arrive at Data Link — [[What is a frame at the Data Link layer]] and [[What PDU is associated with each OSI layer]] continue the stack upward.

> [!tip] Interview answer
> Layer 1 is the contract with the medium: cables and connectors, modulation and line coding, bit rate, duplex and timing. Its importance is practical — media quality, autonegotiation and radio conditions silently cap everything above; that is why troubleshooting methodology starts at the bottom, checking link and speed before blaming DNS or HTTP.
