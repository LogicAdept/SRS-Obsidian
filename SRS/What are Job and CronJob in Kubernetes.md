<!--
reps: 0
priority: 0
-->
#DevOps/Tools/Kubernetes #SRS

# What are Job and CronJob in Kubernetes

> [!abstract] Short answer
> A **Job** runs pods *to completion*: it restarts failed containers per its retry budget until the work finishes successfully, then stops — the opposite of a Deployment, whose pods must never be "done". A **CronJob** creates Jobs on a schedule (standard cron syntax), with policies for what to do when a run is still alive at the next trigger. Use them for migrations, batch processing, reports, and any task with a natural end.

## Job: completion semantics and the retry budget

The Job controller counts successful completions: `completions` sets how many successful pods the work needs, `parallelism` how many may run at once — together they express both single-shot tasks and work queues. Failure handling is governed by `backoffLimit` (default 6): a pod whose container exits non-zero is recreated with exponential backoff (10s, 20s, 40s, capped at 6 minutes), and once the backoff count is spent the Job fails and stops. Two safety valves matter in interviews: `activeDeadlineSeconds` kills a Job that runs too long regardless of retries, and `ttlSecondsAfterFinished` cleans up finished Jobs and their pods so the API does not silt up. The pod template's `restartPolicy` must be `OnFailure` or `Never` — `Always` is illegal precisely because a Job's pods must be able to end ([[What happens when you run kubectl run in Kubernetes]] — `run --restart=Never` mimics the shape without the controller).

## CronJob: schedules with sharp edges

A CronJob's `schedule` is standard cron; each tick creates a Job with a generated name. `concurrencyPolicy` decides collisions: `Allow` (default — runs pile up), `Forbid` (skip if previous still running), `Replace` (kill and restart). `startingDeadlineSeconds` bounds how late a missed trigger may still fire — and if it is unset and the controller misses a whole window, runs are skipped and counted. `suspend: true` pauses future runs without touching a currently running one. The gotcha everyone eventually meets: Kubernetes cron has no time zone guarantee — `timeZone` is only a field since 1.27, so schedules written against "local midnight" break when the controller's UTC horizon differs ([[What is the difference between kubectl apply and kubectl create]] — schedules live in the manifest, so fixes go through the file, not the live object).

```bash
./kubectl create cronjob batch --image=busybox:1.36 --schedule="*/5 * * * *" --dry-run=client -o yaml
```

**Listing 1.** kubectl v1.37.0 generating a CronJob: the schedule is top level, and the inner Job template already carries `restartPolicy: OnFailure` — completion semantics are baked into the generated object.

```
apiVersion: batch/v1
kind: CronJob
metadata:
  name: batch
spec:
  jobTemplate:
    metadata:
      name: batch
    spec:
      template:
        metadata: {}
        spec:
          containers:
          - image: busybox:1.36
            name: batch
            resources: {}
          restartPolicy: OnFailure
  schedule: '*/5 * * * *'
status: {}
```

```d2
direction: right
cron: "CronJob\nevery */5 min" {
  width: 210
  height: 90
  style.fill: "#e3f2fd"
}
j2: "Job 10:05\nrunning" {
  width: 190
  height: 90
  style.fill: "#e8f5e9"
}
tick: "tick 10:10\nprevious still alive?" {
  width: 260
  height: 90
  style.fill: "#fff3e0"
}
allow: "Allow: new Job anyway\nForbid: skip\nReplace: kill + start" {
  width: 290
  height: 110
  style.fill: "#fff3e0"
}
done: "pods exit 0\ncompletions met" {
  width: 220
  height: 90
  style.fill: "#e8f5e9"
}
cron -> j2 -> tick -> allow
j2 -> done
```

**Fig. 1.** Overlap policy is the only real decision: everything else — schedule, deadline, TTL — is parameters on the same Job-creating loop.

> [!warning] "Finished" is not "done with"
> A Job marked complete keeps its pods and object around until TTL or manual cleanup — dashboards lie if you assume otherwise. `backoffLimit` counts *pods given up on*, not container restarts, and a Job can fail with all retries spent even though the bug is a bad argument, not flakiness — retries do not fix a wrong config. For CronJobs the classic trap: a five-minute schedule with a ten-minute run and `Allow` silently multiplies the work — and time zones are UTC unless stated.

> [!tip] Interview answer
> A Job runs pods to successful completion — completions and parallelism shape the work, backoffLimit caps retries with exponential backoff, activeDeadlineSeconds bounds total runtime, and TTL cleans up afterward; its restartPolicy must be OnFailure or Never. CronJob just adds time: cron schedule, concurrencyPolicy for overlaps, startingDeadlineSeconds for missed ticks, and a timeZone field you should set explicitly. Deployments keep pods alive, Jobs make them finish — that is the axis.
