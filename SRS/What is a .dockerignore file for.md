<!--
reps: 0
priority: 0
-->
#DevOps/Tools/Docker #SRS

# What is a .dockerignore file for

> [!abstract] Short answer
> `.dockerignore` filters what the client sends to the daemon as the **build context** — the tar of the current directory shipped over the Docker API before any build step runs. Excluding junk keeps builds fast, keeps unstable files from busting the `COPY` cache, and keeps secrets and VCS metadata out of image layers.

## The context is shipped wholesale

`docker build .` tars up the directory (minus `.dockerignore` matches) and sends it to the daemon, even for a one-line Dockerfile. Everything present is also fair game for `COPY . /app` — and for the layer checksums that drive [[How does the Docker build cache work]].

```
.git
target
node_modules
*.log
.env
docker-compose*.yml
```

**Listing 1.** A typical Java-node `.dockerignore`: build outputs, VCS internals, logs, and env files never reach the context, so they cannot be copied into a layer or shift its checksum.

The file sits at the context root next to the Dockerfile (a per-Dockerfile variant `Dockerfile.dockerignore` exists in newer BuildKit setups), and its patterns follow Go `filepath.Match` semantics with `**` support.

> [!warning] .dockerignore is a build hygiene tool, not a security boundary
> It prevents files from entering the **context** — it does not encrypt, redact, or protect anything on the host, and it cannot un-leak a secret that a RUN instruction downloads itself ([[What is the difference between ARG and ENV in a Dockerfile]] is where build-arg leakage lives — kept out of layers only via secret mounts). Defense still requires real secret management; the ignore file just removes the most common accidental COPY path.

> [!tip] Interview answer
> **The build context is a tar of the project directory sent to the daemon on every build; .dockerignore prunes that tar. Effects: smaller context uploads, stable COPY checksums that stop cache thrash, and no .git or .env files silently copied into layers. It is hygiene and leak prevention, not a security sandbox.**

