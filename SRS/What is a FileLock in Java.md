<!--
reps: 0
priority: 0
-->
#Java/NIO/Channels #SRS

# What is a FileLock in Java?

> [!abstract] Short answer
> **A `FileLock` is an advisory lock on a file (or a region of it), taken through a `FileChannel`: `lock()` blocks, `tryLock()` returns `null` if it cannot.** The javadoc is explicit that "file locks are held on behalf of the entire Java virtual machine" and are "not suitable for controlling access to a file by multiple threads within the same JVM" — two threads of one JVM contending for the same region throw `OverlappingFileLockException`. Locks coordinate **processes**, not threads; whether an OS actually enforces them against uncooperative programs is platform-dependent ([[What are channels in Java NIO]], [[Which class is intended for working with filesystem entries]]).

## Advisory and JVM-wide

The lock is a contract between cooperating processes: everyone who touches the file must call `lock()` themselves. A program that ignores locking and just opens the file will read or write — on UNIX the lock is advisory by tradition, on Windows it is more often mandatory, and the Java API does not promise either. Regions let several JVMs lock different parts of one file (a log head vs tail); `lock(0, Long.MAX_VALUE, true)` is the idiom for "whole file, including future growth".

| Operation | Behaviour |
| --- | --- |
| `lock()` | exclusive, whole file, blocks until available |
| `tryLock()` / `tryLock(pos, size, shared)` | immediate `null` on failure |
| `shared = true` | needs a channel opened for reading; some platforms allow only one kind |
| Overlap inside one JVM | `OverlappingFileLockException` — always, even across threads |
| Release | `release()`, channel `close()`, or JVM exit |

The lock object is immutable once taken; `isValid()` turns `false` after release or channel close. Locks are **not inherited** by child processes and vanish when the JVM dies — the OS guarantees that cleanup.

```java
import java.io.IOException;
import java.io.RandomAccessFile;
import java.nio.channels.FileLock;

class Guard {
    public static void main(String[] args) throws IOException {
        try (RandomAccessFile raf = new RandomAccessFile("/tmp/app.lock", "rw")) {
            FileLock lock = raf.getChannel().tryLock();
            if (lock == null) {
                System.out.println("another instance holds the file");
                return;
            }
            System.out.println("locked: valid=" + lock.isValid()
                    + " shared=" + lock.isShared());
            lock.close();                       // or closing the channel releases it
            System.out.println("released: valid=" + lock.isValid());
        }
    }
}
```

**Listing 1.** Single-instance guard: `tryLock`, work, release on close:

```text
locked: valid=true shared=false
released: valid=false
```

**Listing 2.** Closing the channel released the lock; `isValid()` flipped to false.

```d2
direction: right
jvm1: "JVM 1\ntryLock -> exclusive" {
  width: 220
  height: 55
  style.fill: "#e8f5e9"
}
file: "file on disk\nadvisory lock" {
  width: 220
  height: 50
  style.fill: "#e3f2fd"
}
jvm2: "JVM 2\ntryLock -> null (must wait)" {
  width: 250
  height: 55
  style.fill: "#ffebee"
}
jvm1 <-> file
jvm2 -> file: "cooperates via lock()"
```

**Fig. 1.** One JVM holds the region; the second JVM sees `null` from `tryLock` — cooperation, not compulsion.

> [!warning] Threads are not the audience
> Use `synchronized` / `ReentrantLock` / `Semaphore` for threads inside one JVM — `FileLock` will only give you `OverlappingFileLockException` between threads of the same JVM. `createNewFile()` is **not** a lock either (a stale file from a crash leaves every later run locked out — a real lock dies with its holder). Region locks do not follow file growth unless you lock to `Long.MAX_VALUE`. And never assume the OS enforces the lock against a process that never asks for it.

> [!tip] Interview answer
> `FileChannel.lock` / `tryLock` produce an advisory, JVM-wide, region-scoped `FileLock`: it coordinates processes that cooperate, throws `OverlappingFileLockException` for overlapping claims inside one JVM, is released by `release()`, channel close or JVM exit, and its hard enforcement is platform-dependent. For threads inside one JVM it is the wrong tool — use concurrency primitives.

