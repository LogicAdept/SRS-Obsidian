<!--
reps: 0
priority: 0
-->
#Networking/OSI #SRS
# How many layers does the TCP IP model have

> [!abstract] Short answer
> Four by the source architecture (RFC 1122): Link, Internet, Transport, Application. Some textbooks teach five, splitting Physical out of Link. Both are accepted if you name where the split is; what never changes is that there is no separate Session or Presentation layer.

## The two variants

```d2
direction: right
v4: "4-layer (RFC 1122)\nLink | Internet | Transport | Application" { width: 380; height: 90; style.fill: "#e3f2fd" }
v5: "5-layer (common teaching)\nPhysical | Data Link | Internet | Transport | Application" { width: 440; height: 90; style.fill: "#e8f5e9" }
```

**Fig. 1.** The only difference is whether the bottom of the stack is one "Link" layer or two physical/link layers.

Layer by layer (4-layer view):

1. **Link** — moving frames over the local medium: Ethernet, Wi-Fi, drivers, MAC addressing.
2. **Internet** — host-to-host across networks: IP, ICMP, routing tables.
3. **Transport** — process-to-process: TCP (ordered, reliable), UDP (fast, message-oriented), QUIC (streams over UDP).
4. **Application** — everything above: HTTP, DNS, DHCP, TLS, SMTP, SSH.

> [!warning] "5 or 7" is a trap, not a debate
> If an interviewer hears "seven, like OSI" — that is a wrong answer, because it erases the model's key idea: the Internet merges the top layers. The safe formulation: "four per RFC 1122; five-layer variant separates Physical; and the reason it is never seven is that session/presentation duties moved into applications." The mapping mechanics are in [[How do the TCP IP model layers map to the OSI model]].

Related anchors: [[What is the TCP IP protocol suite]] for the protocols per layer, [[What is the difference between the OSI model and the TCP IP model]] for the model-level comparison, and [[What is the purpose of each OSI layer]] if the interviewer switches to the OSI ladder.

> [!tip] Interview answer
> Four: Link, Internet, Transport, Application — that is RFC 1122's own structure; teaching materials often show five by splitting Physical from Link. The invariant I state: no Session or Presentation layers exist in TCP/IP, those jobs live inside applications and TLS. This answer handles both the count question and the follow-up about why.
