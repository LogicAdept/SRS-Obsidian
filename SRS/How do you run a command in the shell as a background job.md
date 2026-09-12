<!--
reps: 0
priority: 0
-->
#DevOps/Shell #SRS

# How do you run a command in the shell as a background job

> [!abstract] Short answer
> Append **`&`** to the command: `long_task &`. The shell starts it asynchronously, prints a job line like `[1] 25647` (job number and process id), and `$!` holds that pid for later. Manage it with **`jobs`**, resume with **`fg %1`** / **`bg %1`**, stop with Ctrl-Z — and remember that the job still belongs to the terminal session: `nohup` or `disown` are what protect it when the shell exits.

Formally, bash associates a **job** with each pipeline: the job's processes sit in one process group, and the interactive shell keeps a job table you list with `jobs`. The kernel's terminal driver maintains a current foreground process group; only it receives keyboard-generated signals, and only it may read from the terminal — a background process that tries to read is sent SIGTTIN and suspended unless it handles it. Ctrl-Z sends SIGTSTP, stopping the foreground job and returning control to the shell; from there `bg` resumes it in the background, `fg` brings it back. Job specs refer to jobs as `%n`, by a name prefix (`%ce`), or by substring (`%?ce`).

```bash
$ long_migration &          # start asynchronously
[1] 25647
$ echo $!                   # pid of the background job
25647
$ jobs                      # table: running / stopped
[1]+  Running    long_migration &
$ kill %1                   # signal by jobspec, not by pid
$ Ctrl-Z, then: bg          # stop foreground, resume in background
$ nohup backup.sh &         # immune to SIGHUP, output to nohup.out
$ disown -h %2              # or: mark an existing job SIGHUP-free
```

**Listing 1.** The full lifecycle: start with `&`, inspect with `jobs`, signal via jobspec, and survive shell exit with `nohup` or `disown`.

## What actually kills a background job

When an interactive shell exits, it resends SIGHUP to all jobs — running or stopped. That is the mechanism behind "my background process died when I closed the terminal". `nohup utility` starts a command with SIGHUP ignored (output redirected to nohup.out if not redirected); `disown` removes the job from the shell's table so it is never signaled. For anything that must outlive sessions and restart on boot, neither is the right tool — a service manager (systemd units, container supervisors) is, which is how [[What is a Unix shell]] scripting scales into real operations. Orphaned background jobs are also easy to forget: they keep consuming CPU and memory outside any session, and a resource sweep ([[How do you check system resource usage from the shell]]) is how stray ones are found.

```d2
direction: down
run: "command &\nstarted asynchronously" {
  width: 300
  height: 90
  style.fill: "#e3f2fd"
}
live: "Running in background\nimmune to keyboard signals" {
  width: 340
  height: 90
  style.fill: "#fff3e0"
}
stopped: "Stopped\n(Ctrl-Z or SIGTTIN)" {
  width: 300
  height: 80
  style.fill: "#ffebee"
}
gone: "Shell exits\nSIGHUP resent to jobs" {
  width: 320
  height: 90
  style.fill: "#ffebee"
}
safe: "nohup / disown -h\nsurvives exit" {
  width: 300
  height: 90
  style.fill: "#e8f5e9"
}
run -> live
live -> stopped: "fg / Ctrl-Z"
stopped -> live: "bg"
live -> gone
live -> safe
```

**Fig. 1.** Background job states: Ctrl-Z stops, `bg` resumes, and only SIGHUP protection changes what happens when the shell exits.

> [!warning] `&` does not detach
> Starting a job with `&` changes scheduling, not ownership: the process remains a child of the shell in its session, still holding the terminal as controlling terminal. Two classic failures: a background process that later reads stdin gets SIGTTIN and silently suspends; and without job control (in scripts), an asynchronous command's stdin is redirected from /dev/null and it inherits SIGINT/SIGQUIT ignored. The interview trap is the reverse claim — "`&` is the same as a daemon": daemons detach session, standard streams, and working directory deliberately, which is why service managers exist.

> [!tip] Interview answer
> **Append & to run asynchronously: the shell prints a job number and pid, $! captures it, jobs lists the table, fg and bg move a job between states, and Ctrl-Z stops the foreground job first. The subtlety is lifetime: on exit the interactive shell resends SIGHUP to all jobs, so nohup or disown -h protects a job from hangup; anything long-lived belongs in systemd rather than a backgrounded shell job. Background processes are also immune to keyboard signals and get SIGTTIN if they try to read the terminal.**
