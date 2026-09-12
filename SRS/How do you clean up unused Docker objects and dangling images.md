<!--
reps: 0
priority: 0
-->
#DevOps/Tools/Docker #SRS

# How do you clean up unused Docker objects and dangling images

> [!abstract] Short answer
> `docker system prune` removes stopped containers, dangling (untagged) images, unused networks, and build cache in one shot; `--all` extends it to **all** images not used by an existing container, and volumes are only touched with an explicit `--volumes`. A dangling image is an old layer stack whose tag was moved by a rebuild — it shows as `<none>:<none>`, is harmless, and is pure reclaimable disk.

## The prune family

Every object class has its own prune plus a filter, which is what you actually use in scripts:

```bash
docker system df                       # usage + RECLAIMABLE per class
docker container prune --filter until=24h   # stopped containers older than a day
docker image prune                     # dangling only (<none>:<none>)
docker image prune -a                  # also tagged images no container uses
docker builder prune                   # build cache; next build re-downloads
docker system prune -a --volumes       # the dangerous union
```

**Listing 1.** Targeted prunes first, the union last: `--volumes` makes `system prune` delete named volumes not used by any container, which is data loss, not cleanup.

Dangling images come from the tag workflow: rebuilding `api:latest` leaves the previous image alive but tagless. They are also why a "large" `docker images` list is not automatically waste — tagged images in active use are the point of local caching, and `docker image prune -a` on a build host deletes exactly the layers that made the next build fast ([[How does the Docker build cache work]] pays the price). `docker system df -v` gives the per-image/per-container breakdown before you decide.

## Removal semantics worth an interview follow-up

`docker rm` refuses a **running** container unless you pass `-f`, which SIGKILLs the main process instead of the graceful SIGTERM-then-wait dance of `docker stop` ([[What happens when you stop a Docker container]]) — the stop-then-rm pair is the safe default for anything stateful. It also refuses a **paused** container: unpause first, because the freezer state blocks removal ([[What is the lifecycle of a Docker container]]). Removing a container discards its writable layer — logs, temp files, and everything not in a volume ([[What is the difference between volumes and bind mounts in Docker]]) — which is precisely why the engine keeps exited containers around until you prune them.

> [!warning] prune is a footgun on shared hosts
> `system prune -a` on a build server wipes every image not currently attached to a container — including the ones your rollback plan or another team depends on; combined with `--volumes` it deletes any unmounted named volume, including the database volume of a stopped, not-yet-restarted service. The `until=24h` filter and per-class prunes exist because the blunt union is only safe on disposable CI runners.

> [!tip] Interview answer
> Dangling images are old layer stacks left tagless by rebuilds; they show as none-none and are what plain image prune removes. system prune unions stopped containers, dangling images, unused networks and build cache, with -a for all unused images and --volumes, which I never use outside disposable CI runners because it deletes unmounted data volumes. I check docker system df first, use per-class prunes with an until filter, and remember that rm -f is SIGKILL, not a graceful stop.
