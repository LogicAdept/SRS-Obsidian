<!--
reps: 0
priority: 0
-->
#DevOps/Tools/Docker #Security/AppSec #SRS

# How do you run a Docker container as a non-root user

> [!abstract] Short answer
> Three layers of control: the image's `USER app` instruction sets the default user; `docker run -u 1000:1000` overrides it at runtime; and **rootless mode** moves the entire daemon plus containers into a non-root user namespace so even daemon compromise is not root compromise. Without these, the container process runs as UID 0 — real host-kernel root ([[How does Docker isolate containers with Linux namespaces and cgroups]]).

## From Dockerfile to daemon

```dockerfile
FROM eclipse-temurin:21-jre
RUN useradd -r -u 1001 app
USER app                     # every following instruction + runtime default
WORKDIR /home/app
COPY --chown=app:app target/app.jar app.jar
ENTRYPOINT ["java", "-jar", "app.jar"]
```

**Listing 1.** The Dockerfile idiom: create the user, switch with USER, and fix ownership at COPY time (`--chown`) rather than with a later chown layer. Config snippet per the Dockerfile reference — not executed here.

```bash
docker run -u 1001 app:1.0            # runtime override (uid:gid), image default ignored
dockerd-rootless-setuptool.sh install  # rootless daemon: dockerd itself non-root
docker run --userns=remap ...          # userns-remap: container root -> host unprivileged UIDs
```

**Listing 2.** The daemon-side dials: a `-u` override for one-offs, rootless mode as the strongest default (no SETUID binaries beyond newuidmap/newgidmap), userns-remap when the daemon must stay root but containers must not be.

Two practical constraints shape the choice: ports below 1024 are privileged in the container (Java's 8080 habit dodges this, a Tomcat on 80 does not), and rootless mode has prerequisites — user namespaces enabled, subordinate UID ranges for the user.

> [!warning] USER after COPY does not retroactively fix ownership
> Switching to `USER app` after copying files owned by root leaves the app unable to read or write them — the error surfaces as `Permission denied` (or `AccessDeniedException`) at runtime, not at build time. And `docker run -u` against an image built for root hits the mirror image of the problem: home and cache directories do not exist for that UID. Fix ownership in the image (`COPY --chown`, `chown -R` in the same layer — which then bloats it, [[How do Docker image layers relate to a Dockerfile]]), not in the deploy command line. Privileged-mode comparisons live in [[What does it mean to run a Docker container in privileged mode]].

> [!tip] Interview answer
> **Default to a dedicated user: useradd plus USER in the Dockerfile, ownership via COPY --chown; override per-run with -u. Stronger still: rootless mode runs dockerd itself unprivileged in a user namespace, and userns-remap maps container root to host unprivileged UIDs. Because container UID 0 is host-kernel root without these, a non-root user is the cheapest hardening there is.**

