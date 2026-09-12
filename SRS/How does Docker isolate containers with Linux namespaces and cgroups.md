<!--
reps: 0
priority: 0
-->
#DevOps/Tools/Docker #Java/JVM #SRS

# How does Docker isolate containers with Linux namespaces and cgroups

> [!abstract] Short answer
> Two kernel mechanisms, two questions. **Namespaces** answer "what can the process see": its own PID tree, network stack, mounts, hostname, IPC, and (optionally) user table. **Cgroups** answer "how much can it use": CPU, memory, pids, block I/O budgets. Docker creates a set of namespaces and a cgroup per container; there is no hypervisor and no guest kernel.

## See less, use less

On `docker run` the daemon asks the kernel for new namespaces and registers the container's processes in a cgroup. The process believes it is alone; the kernel enforces the accounting.

```d2
direction: right
ns: "namespaces = the VIEW\npid: own process tree (PID 1)\nnet: own interfaces, routes\nmnt: own filesystem root\nuts/ipc/user: name, IPC, UIDs" {
  width: 420
  height: 130
  style.fill: "#e3f2fd"
}
cg: "cgroups = the BUDGET\nmemory.max: RAM ceiling\ncpu.max: CPU quota/period\npids.max: process count" {
  width: 420
  height: 130
  style.fill: "#e8f5e9"
}
k: "shared host kernel\n(seccomp filter + capability set applied)" {
  width: 460
  height: 70
  style.fill: "#fff3e0"
}
ns -> k
cg -> k
```

**Fig. 1.** View and budget are orthogonal: a container with its own PID namespace still shares the kernel that counts its memory.

Because the JVM reads these limits to size its heaps and thread pools ([[How does the JVM detect container memory and CPU limits]]), the cgroup configuration is not invisible plumbing — it directly decides `-Xmx` ergonomics inside the container. A side effect of namespacing is that the container's init process is genuinely PID 1 within its own pid namespace, which gives it special kernel duties ([[What is the PID 1 problem in Docker containers]]).

> [!warning] Shared kernel means one security domain
> Namespaces fence views; they do not create a second kernel. Root inside a container is UID 0 against the host kernel unless user namespaces remap it ([[How do you run a Docker container as a non-root user]]), the default seccomp profile blocks ~44 syscalls but a kernel exploit remains in scope for every container on the host, and `--privileged` drops nearly all of this isolation ([[What does it mean to run a Docker container in privileged mode]]). That is the honest boundary between "container" and "VM".

> [!tip] Interview answer
> **Docker uses namespaces so a container sees its own process tree, network stack, and mounts, and cgroups so the kernel caps its CPU, memory, and process counts. Isolation is view-plus-budget on one shared kernel — cheap and dense, but weaker than VM hardware virtualization, which is why root in the container, kernel bugs, and privileged mode matter.**

