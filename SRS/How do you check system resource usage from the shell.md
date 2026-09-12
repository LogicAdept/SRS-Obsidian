<!--
reps: 0
priority: 0
-->
#DevOps/Shell #OperatingSystems/Linux #SRS

# How do you check system resource usage from the shell

> [!abstract] Short answer
> **`top`** (or `htop`) shows live per-process CPU and memory plus load average; **`free -h`** reports RAM — read the *available* column, not *free*; **`df -h`** shows filesystem space and **`df -i`** inode exhaustion; **`du -sh dir`** finds which directory consumes the space; **`uptime`** gives the load averages in one line. Together they answer the three operational questions: is CPU saturated, is memory exhausted, is disk full.

`top` is the all-in-one monitor: the header shows uptime, load averages (1, 5, and 15 minutes), and CPU time split by mode (`us` user, `sy` system, `id` idle, `wa` iowait), while the task list shows per-process %CPU, %MEM, RES (resident memory), and state; `-bn1` produces a one-shot batch snapshot instead of the interactive screen. `free` summarizes memory: total, used, free, **buff/cache** — kernel page cache that is reclaimed on demand — and **available**, an estimate of what can be allocated without swapping; `-h` prints human-scaled units (Ki, Mi, Gi). `df` reports mounted filesystems: size, used, available, and usage percentage per mount — with `-i` the same table for inodes, the resource that dies first when millions of small files appear. `du` walks directories and sums file sizes, which is how you chase what `df` found.

```bash
$ uptime                       # load: 1, 5, 15 min averages
 14:02:31 up 9 days,  load average: 4.21, 3.87, 2.10
$ free -h                      # RAM: read 'available'
       total  used  free  buff/cache  available
Mem:    15Gi  9.2Gi 1.1Gi       5.0Gi     5.8Gi
$ df -h /var                   # filesystem space
/dev/nvme0n1p2   98G   91G  2.3G  98%  /
$ du -sh /var/log              # who ate it
4.1G    /var/log
$ top -bn1 | head -5           # one-shot CPU snapshot
```

**Listing 1.** The canonical resource sweep: load, memory, filesystem, then drill into the suspect directory.

## Reading the numbers correctly

Load average counts runnable and (on Linux) uninterruptible-waiting tasks, so a rising 15-minute figure with high `wa` in `top` points to storage, not CPU — the number is a *trend*, and comparing it against core count gives saturation. `free` is the classic misread: a machine showing a few hundred MiB *free* but gigabytes *available* is healthy, because buff/cache is reclaimable. The `df`-versus-`du` mystery — `df` says full, `du` finds nothing — usually means a deleted file still held open by a process: the blocks are released only when the descriptor closes. These same counters are what container tooling exposes externally ([[How do you monitor Docker containers in production]] for cgroup-scoped views, [[How do you limit CPU and memory for a Docker container]] for the enforcement side).

> [!warning] Three traps
> Judging memory by the *free* column — page cache makes it look like a leak when nothing is wrong; *available* is the decision number. Diagnosing CPU by load average alone: a load of 8 on 32 cores is idle, on 2 cores it is 4× saturation, and on Linux it includes uninterruptible D-state tasks that never reached the run queue. And forgetting `df -i`: inode exhaustion fails writes on a filesystem with gigabytes of free space — the trap looks like a disk-full error and behaves like nothing of the sort.

> [!tip] Interview answer
> **For a quick sweep: top for live CPU and memory per process with load averages and iowait, free -h where the available column is the real memory signal, df -h for filesystem space and df -i for inodes, and du -sh to drill into what consumed the space. Load average is a trend relative to core count and includes uninterruptible waits on Linux. The classic gotchas: free memory looks low because of page cache, and df full with du empty means a deleted-but-open file.**
