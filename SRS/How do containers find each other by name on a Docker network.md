<!--
reps: 0
priority: 0
-->
#DevOps/Tools/Docker #Networking/DNS #SRS

# How do containers find each other by name on a Docker network

> [!abstract] Short answer
> On a **user-defined** bridge network, Docker runs an embedded DNS resolver (reachable at 127.0.0.11 inside the container) that resolves container names and network aliases to current container IPs. On the default bridge there is no name resolution — only IP addresses (or legacy `--link`). The name tracks the container through restarts and IP changes.

## The embedded resolver

When you `docker network create app-net` and attach containers, the daemon programs each container's `/etc/resolv.conf` toward the embedded DNS. Requests for unknown names fall through to the host's upstream resolvers, so `db` resolves locally and `api.example.com` still resolves externally.

```bash
docker network create app-net
docker run -d --name db --network app-net postgres:18
docker run -d --name web --network app-net myapp:1.4
# inside web:  jdbc:postgresql://db:5432/app  — 'db' is resolved by the embedded DNS
```

**Listing 1.** The whole discovery story in three lines: same user-defined network, name-based addressing. Daemon-dependent commands shown for the mechanism; not executed in the review environment.

The scope is per-network: a container attached to two networks resolves names within each, and service aliases (or Compose service names — [[How does depends_on work in Docker Compose]]) add extra resolvable names on top. Because the resolver answers with the *current* IP, restart-dance IP churn is absorbed — the classic static-`/etc/hosts`-entry failure mode disappears.

> [!warning] Same image, different network, no DNS
> The single most common discovery bug: containers ran with `docker run` without a network, so they all sit on the **default bridge**, where name lookup simply does not exist — connection by hostname fails with `UnknownHostException`-style errors while `docker inspect` shows both containers alive. The fix is attaching both to a user-defined network, not editing hosts files. On the default bridge, IP-based access also breaks on restart, since Docker reassigns addresses ([[What are the Docker network drivers and when should you use each]]).

> [!tip] Interview answer
> **User-defined networks ship an embedded DNS at 127.0.0.11 that maps container names and aliases to live IPs, falling through to upstream resolvers for external names. Default bridge gives you nothing — IPs only, --link is legacy. Names are per-network scoped and survive restarts, which is why every Compose or Swarm setup relies on service names instead of addresses.**

