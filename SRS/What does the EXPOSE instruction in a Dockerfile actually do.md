<!--
reps: 0
priority: 0
-->
#DevOps/Tools/Docker #SRS

# What does the EXPOSE instruction in a Dockerfile actually do

> [!abstract] Short answer
> Nothing functional. `EXPOSE 8080` is documentation and a convention: it declares which ports the image intends to listen on (TCP by default, UDP optional). It does **not** publish anything to the host — publishing happens with `docker run -p` (specific mapping) or `-P` (all EXPOSEd ports mapped to ephemeral host ports).

## Publishing vs exposing

The distinction matters for every Java service behind a reverse proxy or orchestrator. Inside a Docker network, containers reach each other on any port with no EXPOSE at all; EXPOSE exists for the humans and tooling that read the image metadata.

```dockerfile
FROM eclipse-temurin:21-jre
COPY target/app.jar app.jar
EXPOSE 8080/tcp 9090        # 9090 defaults to TCP
ENTRYPOINT ["java", "-jar", "app.jar"]
```

**Listing 1.** Declares intent: 8080 (TCP) and 9090. `docker run -p 8080:8080 app:1.0` actually publishes 8080 on the host; `-P` would publish both to random high ports.

```d2
direction: right
host: "Host\n-p 8080:8080" {
  width: 220
  height: 80
  style.fill: "#e3f2fd"
}
c: "Container\nlistens on 8080\n(EXPOSE was metadata)" {
  width: 300
  height: 100
  style.fill: "#e8f5e9"
}
peer: "Peer container\nreaches 8080 directly\nno -p, no EXPOSE needed" {
  width: 300
  height: 100
  style.fill: "#fff3e0"
}
host -> c: "published"
peer -> c: "on user-defined bridge"
```

**Fig. 1.** Two different reach paths: host access needs `-p` publishing; container-to-container traffic on a shared network never needs either EXPOSE or -p ([[How do containers find each other by name on a Docker network]]).

> [!warning] "I added EXPOSE but still cannot connect"
> Two classics hide here. First: EXPOSE without `-p` — the host has no route to the port, so the fix is publishing, not more EXPOSE lines. Second: `-p 8080:8080` while the app binds only to localhost inside the container — the bind address, not Docker, refuses the connection; server configuration (e.g. Spring Boot's `server.address`) must listen on the container interface ([[How do you change the port of the embedded server]] is the Boot-side equivalent knob).

> [!tip] Interview answer
> **EXPOSE is metadata: it documents intended ports and feeds -P auto-publishing, but opens nothing. Traffic from the host needs -p host:container; container-to-container traffic on a user-defined network works on all ports without EXPOSE. So EXPOSE is for humans and tooling, -p is the actual switch.**

