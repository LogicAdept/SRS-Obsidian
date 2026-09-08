<!--
reps: 0
priority: 0
-->
#Java/Spring/Batch #SRS

# What is Spring Batch?

> [!abstract] Short answer
> **Spring Batch** is a framework for **offline bulk jobs**: read a large set of records, apply rules, write results, with **transactions, restart, skip, and statistics**. A **`Job`** is an ordered **`Step`** graph. The usual step is **chunk-oriented**: `ItemReader` → optional `ItemProcessor` → `ItemWriter` inside a transaction every **commit interval**. A **`Tasklet`** step is one `execute` call instead of a chunk loop. It is **not a scheduler** (use Quartz, Control-M, cron, Kubernetes CronJob) and **not** Spring Cloud Stream.

## Job, step, chunk

Enterprise batch: month-end files, benefit runs, load-and-validate into a system of record — **no user in the loop**. Spring Batch supplies logging, **job repository** metadata, **restart** from the last execution context, **skip**, and **partitioning** for volume. `JobRepository` is required by `Job`/`Step`; `@EnableBatchProcessing` (or `DefaultBatchConfiguration`) exposes `jobRepository` and related infrastructure ([[How do you handle security for a Spring Batch application]], [[What is Spring Cloud]]).

Chunk loop (simplified): read until the commit interval, optionally process, **write the list**, **commit**. `read()` returning **`null`** ends the step. Readers exist for files, XML, SQL, and others; you can implement `ItemReader` / `ItemWriter` (add `ItemStream` if restart must restore position).

```java
@Bean
public Step loadStep(JobRepository jobRepository, PlatformTransactionManager tx) {
	return new StepBuilder("loadStep", jobRepository)
			.<Order, Order>chunk(100, tx)
			.reader(orderReader())
			.processor(orderProcessor())
			.writer(orderWriter())
			.build();
}

@Bean
public Job loadJob(JobRepository jobRepository, Step loadStep) {
	return new JobBuilder("loadJob", jobRepository)
			.start(loadStep)
			.build();
}
```

**Listing 1.** Conceptual. Batch **5** builders take `JobRepository`; this is not `JobBuilderFactory` from Batch 4.

```java
public RepeatStatus execute(StepContribution contribution, ChunkContext chunkContext) {
	// one-shot work
	return RepeatStatus.FINISHED;
}
```

**Listing 2.** Conceptual. `Tasklet` step — dumps that only show two `System.out` tasklets omit the **chunk** model interviews expect.

```d2
direction: down
job: "Job" {
  width: 120
  height: 40
  style.fill: "#e3f2fd"
}
s1: "Step (chunk)" {
  width: 160
  height: 40
  style.fill: "#fff3e0"
}
read: "ItemReader" {
  width: 140
  height: 40
  style.fill: "#e8f5e9"
}
proc: "ItemProcessor?" {
  width: 140
  height: 40
  style.fill: "#e8f5e9"
}
write: "ItemWriter\ncommit interval" {
  width: 180
  height: 45
  style.fill: "#fce4ec"
}
repo: "JobRepository\nrestart metadata" {
  width: 200
  height: 45
  style.fill: "#fce4ec"
}
job -> s1
s1 -> read
read -> proc
proc -> write
s1 -> repo
```

**Fig. 1.** Job sequences steps; a chunk step commits every N items and can restart from the repository.

Launch with `JobOperator` / `JobLauncher` and `JobParameters` (a new identity for a restartable job, or an incrementer). Parallelism is **split/partition** of a step, not “the listener concurrency knob”.

> [!warning] Batch 4 factories are gone
> `JobBuilderFactory` / `StepBuilderFactory` plus a dump `pom` on Boot **2.0.3** are **not** current. Use `new JobBuilder(name, jobRepository)` / `new StepBuilder(name, jobRepository)`. `@EnableBatchProcessing` still means “give me infrastructure,” not “this XML from 2018”.

> [!warning] Not a scheduler and not a web API
> Cron/Quartz **starts** the JVM or calls `JobOperator`. Batch does **not** replace them. A `Job` bean is not an HTTP resource ([[How do you handle security for a Spring Batch application]]).

> [!tip] Interview answer
> Spring Batch runs finite, restartable bulk work: Job of Steps, usually chunk read/process/write with a commit interval and a JobRepository. Tasklets are the simple one-shot step. Pair it with an external scheduler. It is not Cloud Stream and not a replacement for Kafka listeners.
