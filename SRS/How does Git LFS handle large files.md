<!--
reps: 0
priority: 0
-->
#DevOps/VCS/Git #SRS

# How does Git LFS handle large files

> [!abstract] Short answer
> **Git LFS** (Large File Storage) replaces big binary blobs inside the Git object store with tiny **pointer files**: the repo commits a text pointer (LFS version, SHA-256 object id, size) while the actual content lives on an LFS content server, downloaded on demand by `git lfs` filters. Result: clones stay small and history stays fast; binaries still get versioning, branching, and review. You opt files in per *pattern* via `.gitattributes` (`git lfs track "*.psd"`), and the choice is per file type, made *before* the first big commit.

## The pointer, verbatim

```text
$ git lfs track "*.psd"
Tracking "*.psd"
$ git add model.psd
$ git commit -m "Add model.psd via LFS"
$ git cat-file -p HEAD:model.psd
version https://git-lfs.github.com/spec/v1
oid sha256:547ac568992afcb63b916ca7bdd1efb528e84ab845ff91b59047c03ef2d79be8
size 11
$ git lfs ls-files
547ac56899 * model.psd
```

**Listing 1.** git-lfs 3.7.0, empirics sandbox (verbatim): the committed object is a three-line pointer; the smudge filter swaps it for real content on checkout, and the clean filter runs the reverse on `add` (that is why LFS needs `git lfs install` to wire the filters).

How the machinery fits together: `.gitattributes` (committed!) maps patterns to `filter=lfs`; on `push`/`fetch`, `git lfs` transfers objects over HTTPS to/from the LFS endpoint — GitHub, GitLab, Bitbucket all host LFS with storage quotas; teammates just need LFS installed (`git lfs install` once per machine). Speed comes from *not downloading history you don't need*: `GIT_LFS_SKIP_SMUDGE=1 git clone …` fetches pointers only, then `git lfs pull --include="models/**"` fetches selected content later — the CI-friendly pattern for repos with gigabytes of assets.

## When to reach for LFS

- **Large binaries with real history needs**: trained ML models, media assets, firmware, datasets that must be versioned alongside code — every version addressable, every PR reviewing the binary's *presence* (not its diff).
- **Repos slowed down by binaries**: when clone times and `git status` latency suffer, migrating the offending types to LFS (`git lfs migrate import --everything --include="*.psd"`) rewrites history to replace blobs with pointers — a coordinated, force-push-grade operation ([[Why should you not rewrite history of shared branches]] applies fully).
- **Release artifacts** usually do *not* belong: a jar built by CI is reproducible from a tagged source ([[What is a tag in Git and how does it differ from a branch]]) and belongs in an artifact repository ([[Which build tools for Java do you know]]'s ecosystem), not in any Git.

> [!warning] LFS is not retroactive, not free of quotas, and not invisible to tooling
> Files committed *before* `git lfs track` stay ordinary blobs — tracking affects future adds only; retroactive fixes are history rewrites. Every LFS host enforces storage/bandwidth quotas, and CI that checks out LFS content multiplies bandwidth costs — skip-smudge where assets are not needed. Consumers *without* LFS installed see pointer files instead of content (builds mysteriously "read" a 130-byte model); legacy tooling that assumes file content is byte-identical to the object store (some signing, hashing pipelines) can misbehave around filters. And like anything content-addressed in Git, the same binary version across commits is stored once — LFS preserves that dedup on the server side.

```d2
direction: right
add: "git add model.psd\nclean filter runs" {
  width: 280
  height: 100
  style.fill: "#e3f2fd"
}
git: "Git history\npointer: oid sha256 + size" {
  width: 300
  height: 100
  style.fill: "#e8f5e9"
}
lfs: "LFS server\nreal binary content" {
  width: 290
  height: 100
  style.fill: "#fff3e0"
}
push: "git push\n-> LFS upload" {
  width: 260
  height: 90
}
co: "checkout / smudge\npointer -> content" {
  width: 280
  height: 90
}
add -> git: "commit pointer"
add -> lfs: "content goes to server"
git -> push
push -> lfs
lfs -> co
```

**Fig. 1.** Two stores, one view: Git's history carries pointers, the LFS server carries bytes; filters swap them transparently at add/checkout time.

> [!tip] Interview answer
> **Git LFS keeps large binaries out of the Git object store: the repo commits a small pointer — LFS version, SHA-256, size — while content lives on an LFS server, swapped in and out by clean/smudge filters declared in .gitattributes. Clones stay small, binaries get real versioning, and CI can skip smudge and pull selected assets. The caveats: tracking is not retroactive — history rewrites fix the past — hosts have quotas, and anyone without LFS installed sees pointers, not content.**

