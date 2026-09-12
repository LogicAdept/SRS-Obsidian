<!--
reps: 0
priority: 0
-->
#DevOps/VCS/Git #SRS

# How does Git store data internally

> [!abstract] Short answer
> Git is a **content-addressed object database**. It stores four object types — **blobs** (file contents), **trees** (directory listings mapping names to blob/tree ids), **commits** (pointers to a tree plus parent(s), author, message), and **annotated tags** — and every object's name is the SHA-1 hash of its own content. Nothing is stored as diffs: each commit references complete trees, and identical content anywhere collapses to the same blob. Branches and tags are just small files containing an object id (refs).

## A walk through real objects

```text
$ git hash-object hello.txt        # raw content hash
5f4d3383169f69b893e723cdc98046e674d908a1
$ git hash-object -w hello.txt     # write blob into .git/objects
5f4d3383169f69b893e723cdc98046e674d908a1
$ git cat-file -p HEAD             # a commit object
tree 71ab9f3d9dfc2afcc1959aba3ecb32abea592f4b
author SRS Demo <srs-demo@example.com> 1788253260 +0000
committer SRS Demo <srs-demo@example.com> 1788253260 +0000

First commit
$ git cat-file -p HEAD^{tree}      # the root tree
100644 blob 5f4d3383169f69b893e723cdc98046e674d908a1	hello.txt
040000 tree f33c17bc7ed44123cee35d93920e761b53ed218b	src
$ git cat-file -p HEAD:src         # a subtree
100644 blob 9f4b93d846968cd97b319ef13389da340b0130b4	A.java
```

**Listing 1.** git 2.47.3, empirics sandbox (verbatim): hashing content, then reading a commit, its tree, and a subtree. The blob id depends only on content — `"hello objects"` hashes the same wherever it appears.

Key consequences of content addressing:

- **Integrity by construction.** A commit id proves the history up to that point: change one byte anywhere and every hash above it changes. Nothing can be edited in place without the ids screaming.
- **Deduplication.** Copy a 10 MB file, commit twice — one blob. Reverting a huge change stores nothing new if the exact tree already exists.
- **Snapshots, not diffs.** Each commit pins complete trees; the diff you see in `git log -p` is *computed* between snapshots. Storage stays small because blobs are deduplicated and loose objects are periodically packed into `packfiles` with delta compression — that is what `git gc` schedules.
- **Refs are trivial.** `.git/refs/heads/main` is a 41-byte text file with a commit id — this is why [[How would you explain what a Git branch is]] says a branch is a pointer, and why [[What is HEAD and what is a detached HEAD]] can describe HEAD as a special ref.

```d2
direction: up
c: "commit 9c610c1\ntree T1, parent —" {
  width: 300
  height: 90
  style.fill: "#e3f2fd"
}
c2: "commit 2b5a507\ntree T2, parent 9c610c1" {
  width: 310
  height: 90
  style.fill: "#e3f2fd"
}
t1: "tree T1\nhello.txt -> blob A\nsrc/ -> tree S" {
  width: 300
  height: 110
  style.fill: "#fff3e0"
}
t2: "tree T2\nhello.txt -> blob B\nsrc/ -> tree S" {
  width: 300
  height: 110
  style.fill: "#fff3e0"
}
b: "blob B\n'hello objects v2'" {
  width: 250
  height: 80
  style.fill: "#e8f5e9"
}
s: "tree S\nA.java -> blob C" {
  width: 250
  height: 80
  style.fill: "#fff3e0"
}
bc: "blob C\n'public class A {}'" {
  width: 250
  height: 80
  style.fill: "#e8f5e9"
}
c2 -> c: "parent"
c2 -> t2: "tree"
c -> t1: "tree"
t2 -> b
t2 -> s
t1 -> s
s -> bc
```

**Fig. 1.** Two commits forming a chain through the parent pointer; each pins a tree, trees name blobs and subtrees, and the unchanged `src/` tree is shared between both snapshots.

> [!warning] The hash is SHA-1 of "blob <size>\0<content>" — not of the file alone
> A bare `sha1sum` of a file does not match `hash-object` output because Git prefixes the type and size. Also: storing data in `.git/objects` (as `hash-object -w` does) is not the same as tracking it — the blob becomes reachable history only once a tree/commit references it, which is why uncommitted blobs vanish from `gc` but unreferenced ones linger until pruning. And SHA-1 in Git has a known transition path to SHA-256 (repo-format opt-in) — a fact interviewers occasionally probe.

> [!tip] Interview answer
> **Git is a key-value store keyed by SHA-1 of content: blobs hold file contents, trees map names to blobs and subtrees, commits pin a tree plus parent, author and message, and tags wrap a commit with metadata. Branches are files containing commit ids. Everything is addressed by content hash — that gives integrity, snapshot semantics instead of diffs, and free deduplication; packfiles and deltas keep storage compact over time.**

