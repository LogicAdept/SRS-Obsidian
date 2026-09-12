<!--
reps: 0
priority: 0
-->
#DevOps/Tools/Docker #Security/AppSec #SRS

# What does it mean to run a Docker container in privileged mode

> [!abstract] Short answer
> `--privileged` strips nearly every isolation knob at once: the container gets all Linux kernel capabilities, the default seccomp and AppArmor profiles are disabled, the SELinux label is dropped, it gains access to **all host devices**, and `/sys` and cgroups become writable. Docker's own docs warn the result "is not a securely sandboxed process" — it can get a root shell on the host.

## What exactly switches off

Capabilities are the fine-grained units of root power (CAP_NET_ADMIN, CAP_SYS_ADMIN, ...); a default container runs with a small allowlist and drops root's extras. Privileged mode hands back all of them and opens the device tree — which is why it is the escape hatch for Docker-in-Docker, FUSE, raw device work, and legacy software that inspects hardware, and simultaneously why security review treats it as an incident waiting to happen.

```bash
docker run --privileged -d my/dind:1.0        # all caps, all devices, no seccomp/AppArmor
docker run --cap-add=NET_ADMIN --device /dev/fuse myjob:1.0   # targeted alternative
```

**Listing 1.** The blunt instrument versus the surgical one: most "needs privileged" workloads actually need one capability and one device node. CLI shapes per the run reference — not executed in the review environment.

The isolation stack a privileged container bypasses is exactly the namespaces-plus-cgroups-plus-filters story ([[How does Docker isolate containers with Linux namespaces and cgroups]]): namespaces still apply (it is still a container), but the protective defaults that make that isolation meaningful are gone.

> [!warning] Privileged is host root with extra steps — and so is the Docker socket
> The documented warning is literal: "Containers in this mode can get a root shell on the host and take control over the system." Related footgun: mounting `/var/run/docker.sock` into an ordinary container lets it spawn privileged containers of its own — same effective power, lazier audit trail. Prefer the minimal grants (`--cap-add`, `--device`, `--security-opt`), rootless daemon for the daemon-side risk ([[How do you run a Docker container as a non-root user]]), and treat every privileged workload as an exception to justify.

> [!tip] Interview answer
> **--privileged removes the security defaults: all capabilities, no seccomp/AppArmor/SELinux confinement, every host device exposed, writable /sys — Docker documents that such a container can take over the host. Legitimate uses exist (DinD, device drivers, FUSE) but the right reflex is cap-add and --device for the single capability actually needed, plus rootless mode where possible.**

