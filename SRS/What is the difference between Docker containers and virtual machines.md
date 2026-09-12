<!--
reps: 0
priority: 0
-->
#DevOps/Tools/Docker #DevOps/Containerisation #DevOps/Virtualisation #SRS

# What is the difference between Docker containers and virtual machines

> [!abstract] Short answer
> A VM virtualizes hardware: a hypervisor runs a full guest operating system (its own kernel) per machine. A container does not virtualize hardware at all — it is an isolated process on the **shared host Linux kernel**, sandboxed by namespaces and limited by cgroups. Containers therefore start in milliseconds, weigh megabytes, and are far denser per host.

## Where the isolation actually comes from

The kernel-level mechanism is the dividing line. Each VM boots its own kernel, so a VM can run a different OS or kernel version than the host. All containers on a host share one kernel; Docker only fences off what each process can see (namespaces) and how much it may consume (cgroups).

```d2
direction: right
vm: "Virtual machines" {
  app1: "App A" {width: 110; height: 60}
  guest1: "Guest OS + kernel" {width: 200; height: 70; style.fill: "#ffebee"}
  app2: "App B" {width: 110; height: 60}
  guest2: "Guest OS + kernel" {width: 200; height: 70; style.fill: "#ffebee"}
  hyp: "Hypervisor" {width: 200; height: 60; style.fill: "#e3f2fd"}
  hostk: "Host hardware" {width: 460; height: 60}
  app1 -> guest1
  app2 -> guest2
  guest1 -> hyp
  guest2 -> hyp
  hyp -> hostk
}
ctr: "Docker containers" {
  c1: "App C\n(namespaces + cgroups)" {width: 210; height: 80; style.fill: "#e8f5e9"}
  c2: "App D\n(namespaces + cgroups)" {width: 210; height: 80; style.fill: "#e8f5e9"}
  eng: "Docker Engine" {width: 210; height: 60; style.fill: "#e3f2fd"}
  hostkk: "Host OS + ONE kernel" {width: 460; height: 60; style.fill: "#fff3e0"}
  c1 -> eng
  c2 -> eng
  eng -> hostkk
}
vm -> ctr: "contrast"
```

**Fig. 1.** A VM pays for a guest OS per machine; a container shares the host kernel and only isolates the process view. That is why images are megabytes and start instantly.

Because every container sees the same host kernel, `uname -r` inside a container prints the host's kernel version:

```bash
uname -r   # same value on the host and inside every container
```

**Listing 1.** No guest kernel exists to boot — the container process issues syscalls straight into the host kernel, which is why container startup is process-start fast, not OS-boot slow.

For a Java service this means the container packages the JRE and app, but the kernel (and its syscall ABI) comes from the host — you pin the runtime in the image ([[What are Docker containers and images at a high level]]), not the OS.

> [!warning] "Containers are lightweight VMs" — and the macOS exception
> The shared-kernel model has sharp edges: a kernel vulnerability is in scope for every container on that host, and one host kernel version constrains all of them. Also, on macOS and Windows, Docker Desktop runs containers inside a hidden Linux VM — so there "a container on a laptop" silently includes a VM after all; the no-guest-kernel claim is strictly a Linux-host claim. The kernel-side mechanics of the container side are in [[How does Docker isolate containers with Linux namespaces and cgroups]], and the orchestration layer built on top is [[How does Docker differ from Kubernetes]]. The kernel-side mechanics of the container side are in [[How does Docker isolate containers with Linux namespaces and cgroups]], and the orchestration layer built on top is [[How does Docker differ from Kubernetes]].

> [!tip] Interview answer
> **VMs virtualize hardware and boot a full guest OS per machine; containers share the host's Linux kernel and isolate processes with namespaces and cgroups instead. Result: image sizes in megabytes vs gigabytes, startup in milliseconds vs minutes, much higher density — at the price of a weaker isolation boundary and a pinned-to-Linux runtime.**

