<!--
reps: 0
priority: 0
-->
#Java/Versions #SRS

# How did the implementations of core data structures change across Java versions

> [!abstract] Short answer
> **Java 8 rebuilt the hashing core: HashMap bins treeify into red-black trees at eight collisions (JEP 180) and ConcurrentHashMap dropped segment locks for CAS-plus-synchronized bins (155/266). Java 9 compacted String to a byte[] with a coder byte (254). Java 13/15 moved sockets to NIO internals (353/373); 16 made Metaspace elastic (387); 18 reimplemented core reflection on method handles (416); 24/25 cut the object header from 96 to 64 bits via compact object headers (450/519). Same APIs, different internals.**

## Why each change happened

Treeification (180) defends against adversarial or accidental poor hashing: once a bin exceeds eight nodes (and the table is at least 64 buckets), the linked list becomes a red-black tree, so worst-case lookup falls from O(n) to O(log n) ([[Can HashMap degrade to a linked list when keys have different hashCodes]], [[How does HashMap handle collisions]]). The ConcurrentHashMap rewrite (266) replaced fixed segment locking with per-bin `synchronized` plus `casTabAt` — finer lock granularity and better resize parallelism ([[How does ConcurrentHashMap use CAS and synchronized in Java 8]], [[Why did ConcurrentHashMap drop segment locks in Java 8]]). Compact strings (254) exploit the observation that most strings are Latin-1: `String` stores `byte[]` plus a `coder` flag, halving footprint for the common case, with intrinsified ASCII paths keeping `charAt` fast ([[How is java.lang.String implemented under the hood]], [[Is it accurate to say String is backed by a character array internally]]). Compact object headers (450 experimental in 24, 519 product in 25) fold the class pointer into the mark word — eight fewer bytes per object, which compounds across a heap of small objects ([[How do you calculate the memory footprint of a Java object]]).

```java
import java.lang.reflect.Field;
import java.util.HashMap;
import java.util.Map;

public class V40_DataStructures {
    static final class Collide {
        public int hashCode() { return 1; }    // every key lands in the same bin
    }

    public static void main(String[] args) throws Exception {
        Field value = String.class.getDeclaredField("value");
        System.out.println("String.value type = " + value.getType().getName());  // byte[] since 9

        Map<Collide, String> map = new HashMap<>();
        for (int i = 0; i < 60; i++) map.put(new Collide(), "v" + i);            // force treeify
        Field table = HashMap.class.getDeclaredField("table");
        table.setAccessible(true);
        Object[] bins = (Object[]) table.get(map);
        int nodes = 0, treeBins = 0;
        for (Object bin : bins) {
            if (bin == null) continue;
            nodes++;
            if (bin.getClass().getName().contains("TreeNode")) treeBins++;
        }
        System.out.println("bins=" + nodes + " treeified=" + treeBins
                + " (JEP 180, JDK 8)");
    }
}
```

**Listing 1.** Verified on JDK 21 with `--add-opens java.base/java.lang=ALL-UNNAMED --add-opens java.base/java.util=ALL-UNNAMED` (V40_DataStructures in empirics): `String.value type = [B`, `bins=1 treeified=1 (JEP 180, JDK 8)` (out/V40_DataStructures.txt) — `String` holds a byte array and the all-colliding bin became a `TreeNode` bin.

```d2
direction: right
j8: "JDK 8\nHashMap treeify (180)\nCHM CAS rewrite (266)" { style.fill: "#e8f5e9"; width: 230; height: 100 }
j9: "JDK 9\ncompact strings (254)\nbyte[] + coder" { style.fill: "#e8f5e9"; width: 210; height: 100 }
mid: "JDK 13/15/16/18\nNioSocketImpl (353), Datagram NIO (373),\nelastic Metaspace (387), reflection on MH (416)" { style.fill: "#e3f2fd"; width: 420; height: 100 }
j24: "JDK 24/25\ncompact object headers (450/519)\n96-bit -> 64-bit" { style.fill: "#e8f5e9"; width: 260; height: 100 }
j8 -> j9 -> mid -> j24: ""
```

**Fig. 1.** Implementation shifts by release: hashing in 8, string layout in 9, plumbing in the middle, object headers at the far end.

> [!warning] Internals are not spec — and reflection proves it
> `TREEIFY_THRESHOLD`, `table`, and `value` are implementation details; the only reason this probe can read them is `--add-opens`, and strong encapsulation (default since 16, final in 17) is exactly the platform telling you to stop depending on them ([[What is strong encapsulation of JDK internals]]). Contract-wise, none of these changes altered a single public signature.

> [!tip] Interview answer
> **The big internal shifts: Java 8 treeified HashMap bins and rewrote ConcurrentHashMap to CAS plus per-bin synchronized; Java 9 compacted String to byte[] with a coder; 16 made Metaspace elastic; 24/25 compacted the object header itself from 96 to 64 bits. I frame each as a footprint or worst-case fix that never changed the public API.**
