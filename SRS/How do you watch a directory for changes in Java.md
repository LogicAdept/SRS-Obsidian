<!--
reps: 0
priority: 0
-->
#Java/NIO/Files #SRS

# How do you watch a directory for changes in Java?

> [!abstract] Short answer
> **Register a directory with a `WatchService` (NIO.2): `dir.register(watcher, ENTRY_CREATE, ENTRY_MODIFY, ENTRY_DELETE)` returns a `WatchKey`; a loop over `take()` (or `poll`) yields signalled keys, `key.pollEvents()` returns the `WatchEvent`s, and you must call `key.reset()` — otherwise that key stops reporting.** One registration covers exactly one directory (recursion = walk and register each subdirectory yourself). Events can be dropped under load; the service then delivers an `OVERFLOW` event, "a trigger to re-examine the state of the object" ([[What is the difference between the java.io.File class and the java.nio.file.Path interface]], [[What notable features does Java NIO offer]]).

## The key loop

The watcher comes from `FileSystems.getDefault().newWatchService()`. Each `register` call binds one `Path` directory to the chosen `StandardWatchEventKinds`; the returned key accumulates events until you take it. `event.context()` is the affected file name **relative to the watched directory**; `event.count()` tells how many times it repeated before delivery. `take()` blocks, `poll()` returns immediately, `poll(timeout, unit)` waits a bounded time — pick per thread appetite.

| Piece | Role |
| --- | --- |
| `WatchService` | platform-backed queue of signalled keys (inotify on Linux, ReadDirectoryChangesW on Windows) |
| `WatchKey` | one directory's registration + pending events; `cancel()` unregisters |
| `WatchEvent.Kind` | `ENTRY_CREATE` / `ENTRY_MODIFY` / `ENTRY_DELETE` / `OVERFLOW` |
| `reset()` | re-arms the key; skipping it = one-shot watch |

```java
import java.nio.file.FileSystems;
import java.nio.file.Path;
import java.nio.file.StandardWatchEventKinds;
import java.nio.file.WatchEvent;
import java.nio.file.WatchKey;
import java.nio.file.WatchService;

class Watch {
    public static void main(String[] args) throws Exception {
        try (WatchService ws = FileSystems.getDefault().newWatchService()) {
            Path dir = Path.of("/tmp/inbox");
            dir.register(ws, StandardWatchEventKinds.ENTRY_CREATE,
                               StandardWatchEventKinds.ENTRY_MODIFY,
                               StandardWatchEventKinds.ENTRY_DELETE);
            for (int i = 0; i < 3; i++) {
                WatchKey key = ws.take();               // blocks until events
                for (WatchEvent<?> ev : key.pollEvents()) {
                    System.out.println(ev.kind().name() + " -> " + ev.context());
                }
                if (!key.reset()) {                      // re-arm; false = dir gone
                    System.out.println("key lost");
                }
            }
        }
    }
}
```

**Listing 1.** Register, block on `take()`, drain events, re-arm with `reset()`:

```text
ENTRY_CREATE -> report.csv
ENTRY_MODIFY -> report.csv
ENTRY_DELETE -> draft.tmp
```

**Listing 2.** Three events drained from one key — each `context()` is the relative file name.

```d2
direction: right
dir: "watched directory\nregister(kinds)" {
  width: 240
  height: 55
  style.fill: "#e3f2fd"
}
key: "WatchKey\nevents queue up" {
  width: 210
  height: 50
  style.fill: "#e8f5e9"
}
loop: "take() -> pollEvents()\nhandle -> reset()" {
  width: 280
  height: 55
  style.fill: "#fff8e1"
}
dir -> key -> loop
loop -> dir: "still watching while reset"
```

**Fig. 1.** The watch loop: register once per directory, drain and re-arm forever.

> [!warning] One directory, reset or die, and expect repeats
> Forgetting `reset()` is the classic bug: the key delivers once and the watch goes silent while the loop keeps waiting. Events may coalesce or be lost — `OVERFLOW` means "unknown amount of history is gone", so rescan instead of trusting deltas. `ENTRY_MODIFY` commonly fires **several times** per editor save (write + metadata), and a rename arrives as `DELETE` + `CREATE`. The watch follows the directory, not its contents: new subdirectories need their own `register` call. And `WatchService` is not a message bus — events carry names, not contents.

> [!tip] Interview answer
> NIO.2 watching = `newWatchService()`, `dir.register(watcher, kinds)` per directory, loop on `take()`/`poll`, read `pollEvents()` with `context()` as the relative file name, then `reset()` the key. Recursion is manual, events may overflow (then rescan), and modify events repeat — treat it as a change signal, not a reliable event log.

