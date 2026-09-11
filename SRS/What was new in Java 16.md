<!--
reps: 0
priority: 0
-->
#Java/Versions/16 #SRS

# What was new in Java 16

> [!abstract] Short answer
> **Java 16 (March 2021) finalized records (JEP 395) and pattern matching for instanceof (394), turned on strong encapsulation of JDK internals by default (396), added elastic Metaspace (387), Unix-domain socket channels (380), the Vector API incubator (338), the jpackage tool (392), and `Stream.toList()`. Sealed classes were on their second preview.**

## Records final, internals sealed, memory elastic

With records final, the boilerplate story changed: state description in one line, `equals`/`hashCode`/`toString` generated, accessors named after components ([[In which Java version were records standardized]], [[What is a Java record]]). Instanceof patterns finalized the cast-after-check idiom. JEP 396 (strong encapsulation by default) was the breaking one: code reflecting into `java.lang`/`java.util` internals — caches, `String.value`, older ORM tricks — started throwing `InaccessibleObjectException` unless `--add-opens` was passed; 17 made it impossible to restore the old laxity ([[What is strong encapsulation of JDK internals]]). Elastic Metaspace (387) made class metadata return unused memory to the OS, fixing the "Metaspace never shrinks" complaint. `Stream.toList()` arrived as the short-form terminal op — unmodifiable, unlike `Collectors.toList()`.

```java
import java.util.List;
import java.util.stream.Stream;

public class V32_Java16 {
    record Point(int x, int y) {}                          // JEP 395, final in 16

    public static void main(String[] args) {
        Object o = new Point(2, 5);
        if (o instanceof Point p) {                        // JEP 394, final in 16
            System.out.println("matched " + p + " sum=" + (p.x() + p.y()));
        }
        List<Integer> list = Stream.of(1, 2, 3).map(i -> i * 10).toList();  // JDK 16
        System.out.println(list + " immutable=" + isImmutable(list));
    }

    static boolean isImmutable(List<Integer> l) {
        try { l.add(99); return false; }
        catch (UnsupportedOperationException e) { return true; }
    }
}
```

**Listing 1.** Verified on JDK 21 (V32_Java16 in empirics): `matched Point[x=2, y=5] sum=7`, `[10, 20, 30] immutable=true` (out/V32_Java16.txt).

```d2
direction: right
final: "records FINAL (395)\ninstanceof patterns FINAL (394)" { style.fill: "#e8f5e9"; width: 270; height: 80 }
enc: "strong encapsulation DEFAULT (396)\nelastic Metaspace (387)\nUnix-domain sockets (380)" { style.fill: "#e3f2fd"; width: 330; height: 100 }
inc: "Vector API incubator (338)\njpackage (392)\nStream.toList()" { style.fill: "#fff3e0"; width: 240; height: 100 }
final -> enc -> inc: ""
```

**Fig. 1.** Java 16: the records/patterns line finalizes while JDK internals become harder to touch.

> [!warning] `Stream.toList()` is not `Collectors.toList()`
> The 16 short form returns an unmodifiable list — `add`/`set` throw `UnsupportedOperationException` — while `Collectors.toList()` returns a mutable `ArrayList` and never promised immutability. Swapping one for the other during migration silently changes the contract for callers who mutate the result.

> [!tip] Interview answer
> **Java 16 finalized records and instanceof patterns, turned on strong encapsulation of JDK internals by default (the `--add-opens` era begins), added elastic Metaspace, Unix-domain socket channels, and `Stream.toList()`. Sealed classes were still a preview here and finalized in 17. If asked about upgrade pain, 16 is where reflection-into-internals code first broke.**
