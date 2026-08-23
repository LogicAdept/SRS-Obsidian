<!--
reps: 0
priority: 0
-->
#Networking/OSI #SRS

# At which OSI layer does a duplicate IP address problem occur?

> [!abstract] Short answer
> **Layer 3 (Network).** A duplicate IP address is a clash of **network-layer logical addresses** on the same link. Detection often uses ARP or Neighbor Discovery frames, but those are symptoms and probes — the broken contract is still the IP identity at Layer 3.

IP is the usual Internet mapping of OSI Network-layer addressing and routing. See [[Which OSI layer handles logical addressing and routing]] and [[What is the job of the Network layer under the OSI model]].

## Why it is Layer 3

Under the OSI reference model, the **Network layer** provides **network-addresses** that identify end systems for the network service, independently of the addressing used by layers below. In TCP/IP networks that role is filled by **IP addresses**: the Internet Protocol’s two basic functions are **addressing** and fragmentation, and internet modules use those addresses to route datagrams.

Two hosts that both claim the same unicast IP on the **same link** break that uniqueness. Peers then cannot tell which host owns the address, so delivery and return paths become unreliable.

```d2
direction: down
l3: "Layer 3 Network\nIP address A claimed twice" {
  width: 300
  height: 90
  style.fill: "#ffebee"
}
l2: "Layer 2 Data Link\nARP / ND frames expose the clash" {
  width: 320
  height: 90
  style.fill: "#fff3e0"
}
hosts: "Host X and Host Y\ndifferent MACs, same IP A" {
  width: 300
  height: 90
  style.fill: "#e3f2fd"
}

l3 -> hosts
hosts -> l2: "conflict visible in\nARP/ND traffic"
```

**Fig. 1.** The misconfiguration is shared Layer 3 identity; link-layer traffic is how neighbors notice it.

A duplicate **MAC** on the same segment is a different problem and belongs with [[Which OSI layer handles MAC addressing and local frame forwarding]]. Unique MACs do not prevent an IP conflict.

## How the conflict is usually discovered

On IPv4 Ethernet, hosts map a known IP to a MAC with **ARP** (Address Resolution Protocol). Address Conflict Detection (ACD) sends **ARP Probes** (ARP Requests with a zero sender IP) and watches for replies or other ARP traffic claiming the address. If another host already uses it, the probe fails and the new host must not take the address.

```text
# Conceptual — IPv4 ACD probe shape (RFC 5227 / ARP)
ARP Request:
  sender hardware address = my MAC
  sender IP address       = 0.0.0.0
  target IP address       = candidate address A
# Any ARP claiming A from a foreign MAC → conflict
```

**Listing 1.** Conceptual ARP Probe used before (and while) claiming an IPv4 address.

IPv6 uses **Duplicate Address Detection** with Neighbor Solicitation before a unicast address becomes preferred. Same idea: verify the **network-layer** address is free on the link; ND is the link-local mechanism.

[[How does ARP relate to the OSI layers]] places ARP at the Network / Data Link boundary: it serves IP delivery using link-layer addresses.

> [!warning] ARP traffic is not a Layer 2 root cause
> Interview traps say “duplicate IP is Layer 2 because you see it in ARP.” ARP (or ND) is how the conflict is **observed**. The configuration error is still two interfaces using one IP. Fixing only switching or cabling does not assign unique Layer 3 addresses.

> [!warning] Same IP on different links is not this problem
> Private addresses like `10.0.0.1` appear on countless separate links without conflict. ACD and DAD apply to hosts on the **same link**. Also, intentional sharing (for example a coordinated virtual IP or anycast) is arranged on purpose — accidental static/DHCP collisions are the usual exam case.

## What breaks in practice

Peers cache IP→MAC bindings. When two MACs answer for one IP, ARP/ND caches flip, TCP sessions reset, and intermittent reachability appears. The administrator still corrects **IP assignment** (static config, DHCP scope, or reclaiming a defended address), not MAC uniqueness.

> [!tip] Interview answer
> **A duplicate IP address is a Layer 3 Network problem: IP is the logical network address, and two hosts on the same link must not share one unicast identity.** You often spot it through ARP or Neighbor Discovery at the link, but that traffic is detection, not the layer of the misconfiguration. Contrast that with a duplicate MAC, which is a Data Link issue.
