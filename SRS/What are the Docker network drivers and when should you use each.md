<!--
reps: 0
priority: 0
-->
#DevOps/Tools/Docker #SRS

# What are the Docker network drivers and when should you use each

> [!abstract] Short answer
> Five built-ins on Linux: **bridge** (default — private network per user-defined net, NAT to the host), **host** (no network isolation; container shares the host's stack), **none** (loopback only), **overlay** (spans multiple Docker hosts for Swarm), and **macvlan**/**ipvlan** (container gets its own MAC/IP on the physical LAN). Choose by topology: single host, performance, isolation, multi-host, or LAN identity.

## The five drivers in one map

```d2
direction: right
br: "bridge (default)\nuser-defined net + NAT\nDNS by container name" {
  width: 280
  height: 100
  style.fill: "#e8f5e9"
}
ho: "host\nno namespace for net\nbest raw performance" {
  width: 280
  height: 100
  style.fill: "#fff3e0"
}
no: "none\nloopback only\nhand-wired networking" {
  width: 240
  height: 100
  style.fill: "#e3f2fd"
}
ov: "overlay\nacross hosts (Swarm)\nencrypted option" {
  width: 280
  height: 100
  style.fill: "#e8f5e9"
}
mv: "macvlan / ipvlan\nown MAC/IP on the LAN\nno NAT hop" {
  width: 300
  height: 100
  style.fill: "#fff3e0"
}
br -> ov: "scale out"
```

**Fig. 1.** The decision axes: isolation (bridge/none), performance (host), multi-host (overlay), LAN identity (macvlan).

A user-defined bridge is the daily driver: `docker network create -d bridge app-net` gives a private L2/L3 segment where containers talk by name ([[How do containers find each other by name on a Docker network]]) and the host forwards published ports into it. Host mode deletes the net namespace: the process binds host ports directly — maximal throughput and no `-p`, but no isolation and no port multiplexing. Overlay networks span daemons so services on different hosts find each other; macvlan attaches the container as if it were a physical machine with its own MAC — useful for legacy apps that expect LAN presence, awkward where the network forbids extra MACs.

> [!warning] The default bridge is not the same as a user-defined bridge
> Two built-in bridge flavors differ sharply: containers on the *default* `bridge` resolve each other **only by IP** (the `--link` flag is legacy), while user-defined bridges have automatic DNS by container name. Interviews probe exactly this: "why can't my containers see each other by name?" — because they sat on the default bridge. The default bridge also occupies the fixed `172.17.0.0/16` subnet with the host gateway at `172.17.0.1`, which collides with corporate VPN ranges — a user-defined network picks a non-conflicting pool. Host mode, meanwhile, silently breaks `-p` port mappings and port multiplexing, and its security posture equals any host process ([[What does the EXPOSE instruction in a Dockerfile actually do]] covers the publish side).

> [!tip] Interview answer
> **Bridge is the default per-network private segment with name DNS on user-defined nets; host removes the network namespace for raw performance at the cost of isolation; none is loopback-only; overlay stitches containers across hosts for Swarm; macvlan gives containers their own LAN identity. Pick by topology and isolation needs — and remember the default bridge has no DNS.**

