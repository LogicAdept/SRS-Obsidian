<!--
reps: 0
priority: 0
-->
#Java/Versions/13 #SRS

# What was new in Java 13

> [!abstract] Short answer
> **Java 13 (September 2019) previewed text blocks (JEP 355), re-previewed switch expressions (354), let ZGC uncommit unused memory (351), added dynamic CDS archives (350), and reimplemented the legacy `java.net.Socket`/`ServerSocket` API on the NIO-based `NioSocketImpl` (353). String gained `formatted`, `stripIndent`, `translateEscapes`.**

## Text blocks and the quiet socket swap

Text blocks solve multi-line string readability with incidental-indentation rules: the compiler computes the minimal indentation across content lines (the closing delimiter position sets the removal) and strips it ([[What are text blocks]]). The socket reimplementation (353) is the sleeper: `PlainSocketImpl`, the last pre-NIO runtime path, was replaced by `NioSocketImpl` backed by NIO primitives — same `java.net` API, modern internals, easier maintenance; `DatagramSocket` followed in 15 (373). ZGC uncommitting memory (351) paired with G1 346 from the previous train: heap-shrink behavior became a platform property, not a collector-specific bonus.

```java
public class V29_Java13 {
    public static void main(String[] args) {
        String row = "%s scored %d".formatted("ada", 36);   // JDK 13
        System.out.println(row);
        String block = """
                line one
                line two
                """;                                        // preview in 13 (JEP 355), standard in 15
        System.out.println(block.stripIndent().trim().replace('\n', '|'));
        String escaped = "a\\tb\\n".translateEscapes();   // JDK 13
        System.out.println("translateEscapes length=" + escaped.length()
                + " chars=" + escaped.replace('\t', 'T').replace('\n', 'L'));
    }
}
```

**Listing 1.** Verified on JDK 21 (V29_Java13 in empirics): `ada scored 36`, `line one|line two`, `translateEscapes length=4 chars=aTbL` (out/V29_Java13.txt).

```d2
direction: right
lang: "text blocks PREVIEW (355)\nswitch 2nd preview (354)\nString formatted / stripIndent /\ntranslateEscapes" { style.fill: "#fff3e0"; width: 320; height: 110 }
runtime: "ZGC uncommit (351)\nDynamic CDS (350)\nNioSocketImpl (353)" { style.fill: "#e8f5e9"; width: 250; height: 110 }
lang -> runtime: ""
```

**Fig. 1.** Java 13: preview-heavy on the language side, memory- and socket-level swaps on the runtime side.

> [!warning] Text block indentation is positional, not cosmetic
> The closing `"""` position participates in the indentation math — shifting it changes the runtime string. And in 13 this whole feature needed `--enable-preview`; it ran as plain syntax only from 15 ([[What are text blocks]]).

> [!tip] Interview answer
> **Java 13 is the text-blocks-preview release, with the quiet gem being JEP 353: the legacy Socket implementation was swapped for NioSocketImpl — same API, NIO internals. It also re-previewed switch expressions, let ZGC return memory to the OS, added dynamic CDS archives, and gave String `formatted`, `stripIndent`, and `translateEscapes`.**
