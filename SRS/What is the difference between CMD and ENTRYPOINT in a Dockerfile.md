<!--
reps: 0
priority: 0
-->
#DevOps/Tools/Docker #SRS

# What is the difference between CMD and ENTRYPOINT in a Dockerfile

> [!abstract] Short answer
> `ENTRYPOINT` fixes the executable the container runs; `CMD` supplies defaults that are easy to replace. `docker run image args` **overrides** CMD wholesale, but **appends** to an exec-form ENTRYPOINT; only `docker run --entrypoint` replaces the ENTRYPOINT itself. The idiomatic pairing is exec-form `ENTRYPOINT ["java","-jar","app.jar"]` with `CMD` holding default flags.

## The override matrix

Only the last `CMD` and the last `ENTRYPOINT` in a Dockerfile take effect. `CMD` has three forms: exec form, shell form, and the exec form with only parameters — `CMD ["param1"]` alone, which supplies arguments for ENTRYPOINT. How a `docker run image arg` lands depends on that setup:

```d2
direction: down
entry: "exec-form ENTRYPOINT [\"java\",\"-jar\",\"app.jar\"]" {
  width: 420
  height: 80
  style.fill: "#e3f2fd"
}
cmd: "CMD [\"--profile=dev\"]" {
  width: 420
  height: 70
  style.fill: "#e8f5e9"
}
q1: "docker run app:1.0 --profile=prod" {
  width: 420
  height: 70
  style.fill: "#fff3e0"
}
res1: "java -jar app.jar --profile=prod\n(args replaced CMD)" {
  width: 420
  height: 80
  style.fill: "#e8f5e9"
}
res2: "--entrypoint sh\nreplaces the executable itself" {
  width: 420
  height: 80
  style.fill: "#ffebee"
}
entry -> cmd
entry -> q1: "run args"
q1 -> res1
entry -> res2: "flag override"
```

**Fig. 1.** Runtime arguments replace CMD but are appended to an exec-form ENTRYPOINT; `--entrypoint` is the only way to swap the executable.

```dockerfile
FROM eclipse-temurin:21-jre
WORKDIR /app
COPY target/app.jar app.jar
ENTRYPOINT ["java", "-jar", "app.jar"]
CMD ["--spring.profiles.active=dev"]
```

**Listing 1.** `docker run app:1.0` starts the app with the dev profile; `docker run app:1.0 --spring.profiles.active=prod` replaces the CMD argument — no image rebuild for a flag flip.

This split is what makes an image behave like a command-line tool: the image **is** the program (ENTRYPOINT), the run arguments are its flags (CMD). It is the same pattern behind images like `postgres`, where `docker run postgres:18` and extra args configure the executable — and behind Kubernetes pod commands that override them ([[What happens when you run kubectl run in Kubernetes]]).

> [!warning] Shell-form ENTRYPOINT silently ignores CMD
> With `ENTRYPOINT java -jar app.jar` (shell form), the actual PID 1 is `/bin/sh -c "java -jar app.jar"`: any CMD or `docker run` arguments are thrown away, and — worse — SIGTERM from `docker stop` goes to `sh`, not to your process ([[What is the difference between shell form and exec form in a Dockerfile]]). Mixing an exec-form ENTRYPOINT with a shell-form CMD is the quieter cousin: the shell invocation itself becomes the argument string.

> [!tip] Interview answer
> **ENTRYPOINT is the fixed executable, CMD is overridable defaults. Run arguments override CMD entirely but append to exec-form ENTRYPOINT, and --entrypoint replaces the executable. The standard Java image uses exec-form ENTRYPOINT for java -jar plus CMD for default flags; shell-form ENTRYPOINT breaks both argument passing and signal delivery.**

