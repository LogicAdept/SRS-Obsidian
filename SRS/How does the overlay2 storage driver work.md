<!--
reps: 0
priority: 0
-->
#DevOps/Tools/Docker #SRS

# How does the overlay2 storage driver work

> [!abstract] Short answer
> `overlay2` is the default Docker storage driver on Linux: it union-mounts the image's read-only layers (`lowerdir`) with the container's writable layer (`upperdir`) and presents the combined view as `merged`. First writes to an image file trigger a `copy_up` of the **whole file** into the upper layer; deletes create whiteouts — the image below is never modified.

## Layers on disk

OverlayFS needs at most two real directories per mount plus a work directory; The driver stitches up to 128 lower layers natively, which is what makes multi-layer images practical; how Dockerfile instructions produce those layers in the first place is [[How do Docker image layers relate to a Dockerfile]]. `docker inspect` on a running container shows the assembled mount:

```bash
docker inspect -f '{{ .GraphDriver.Data }}' web
# LowerDir: .../l/X:.../l/Y:.../l/Z   <- image layers (read-only)
# UpperDir: .../diff                 <- this container's writes
# MergedDir: .../merged              <- what the container sees as /
# WorkDir:  .../work
```

**Listing 1.** The overlay mount assembled per container; CLI output shape simplified for the review cue.

```d2
direction: down
img: "image layers (lowerdir)\nread-only, shared by all containers" {
  width: 400
  height: 80
  style.fill: "#e3f2fd"
}
up: "container layer (upperdir)\nwritable, per container" {
  width: 400
  height: 80
  style.fill: "#e8f5e9"
}
mrg: "merged view = container /\nupper wins on conflict" {
  width: 400
  height: 80
  style.fill: "#fff3e0"
}
img -> mrg
up -> mrg
```

**Fig. 1.** Same-path files in upper shadow the lower copies; everything else is inherited from the image.

Three write behaviors carry all the interview weight. `copy_up`: the first modification of an image file copies the entire file upward (file-level, not block-level — a one-byte edit of a 1 GB file copies 1 GB once, then edits hit the copy). Deletes: a whiteout entry in upper hides the lower file. Renames of directories across layers return `EXDEV`, so applications must cope with a copy-and-unlink fallback.

> [!warning] Heavy writers do not belong on the container layer
> Databases and anything with sustained random writes punish the copy-up model and balloon `upperdir`; the platform answer is a volume, not tuning the driver ([[What is the difference between volumes and bind mounts in Docker]]). And because image layers are immutable, disk space consumed by deleted-in-upper files is reclaimed only by image cleanup, not by the container's `rm`.

> [!tip] Interview answer
> **overlay2 union-mounts read-only image layers as lowerdir with a per-container writable upperdir, exposing the merged view as the container's root. First writes copy up whole files, deletes add whiteouts, and the image never changes. It is fast for reads and cache-friendly, which is exactly why write-heavy data goes on volumes instead.**

