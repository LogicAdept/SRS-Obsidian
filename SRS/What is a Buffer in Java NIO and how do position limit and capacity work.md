<!--
reps: 0
priority: 0
-->
#Java/NIO/Buffers #SRS

# What is a Buffer in Java NIO and how do position limit and capacity work?

> [!abstract] Short answer
> **A `Buffer` is a fixed-capacity container for primitive data that a channel fills and drains.** One invariant governs every buffer: `0 ≤ mark ≤ position ≤ limit ≤ capacity`. `capacity` never changes; `position` is the index of the next element to read or write; `limit` is the first index you must not touch. The toggles move those indices: **`flip`** (write mode → read mode: `limit = position; position = 0`), **`clear`** (`position = 0; limit = capacity` — data is **not** erased), **`rewind`** (`position = 0`, reread), **`reset`** (`position = mark`). Buffers exist for every primitive **except `boolean`**, and they are **not** thread-safe ([[What notable features does Java NIO offer]], [[What are channels in Java NIO]]).

## The invariant and the toggles

A buffer has exactly one data holder: `capacity` elements (`byte[]` inside a `ByteBuffer`, `char[]` inside a `CharBuffer`, …). Where the data "is" is answered by `position`, not by the array. `remaining()` returns `limit - position`; absolute `get(int)` / `put(int, x)` bypass the position, relative ones advance it and can throw `BufferUnderflowException` / `BufferOverflowException` / `InvalidMarkException`.

| Method | Position | Limit | Mark | Typical use |
| --- | --- | --- | --- | --- |
| `flip()` | `0` | old position | discarded | written → about to read |
| `clear()` | `0` | `capacity` | discarded | done reading → fill again |
| `rewind()` | `0` | unchanged | discarded | reread same data |
| `reset()` | old mark | unchanged | kept | retry from a saved spot |
| `compact()` | moved to start | `capacity` | discarded | keep unread tail, write more |

`clear()` is a bookkeeping reset, **not** a wipe: the elements stay in the backing array until overwritten. `compact()` copies the unread tail (`position..limit`) to the start so a partially drained buffer can be refilled — the standard move in a selector read loop.

```java
import java.nio.ByteBuffer;
import java.nio.charset.StandardCharsets;

class BufDemo {
    public static void main(String[] args) {
        ByteBuffer b = ByteBuffer.allocate(16);
        System.out.println("fresh: cap=" + b.capacity() + " pos=" + b.position() + " lim=" + b.limit());
        b.put(StandardCharsets.UTF_8.encode("abc"));
        b.flip();                                   // write mode -> read mode
        System.out.println("flipped: pos=" + b.position() + " lim=" + b.limit());
        System.out.println("read: " + (char) b.get() + (char) b.get() + " remaining=" + b.remaining());
        b.mark();
        System.out.println("after mark: pos=" + b.position());
        b.reset();                                  // back to the mark
        System.out.println("after reset: pos=" + b.position() + " lim=" + b.limit());
        b.rewind();
        System.out.println("rewound: pos=" + b.position() + " lim=" + b.limit());
    }
}
```

**Listing 1.** Fill, `flip`, read, `mark`/`reset`, `rewind` — indices move, storage stays:

```text
fresh: cap=16 pos=0 lim=16
flipped: pos=0 lim=3
read: ab remaining=1
after mark: pos=2
after reset: pos=2
rewound: pos=0 lim=3
```

**Listing 2.** The buffer indices across five operations; the backing array never moves.

```d2
direction: right
fill: "fill\nposition climbs to limit" {
  width: 240
  height: 55
  style.fill: "#e3f2fd"
}
flip: "flip\nlimit=position, position=0" {
  width: 260
  height: 55
  style.fill: "#e8f5e9"
}
drain: "drain\nread up to limit" {
  width: 220
  height: 55
  style.fill: "#fff8e1"
}
clear: "clear / compact\nposition=0, limit=capacity" {
  width: 280
  height: 55
  style.fill: "#ffebee"
}
fill -> flip -> drain -> clear -> fill
```

**Fig. 1.** The life of one buffer: fill, flip, drain, clear, repeat. Channels do exactly this loop ([[What are channels in Java NIO]]).

> [!warning] Index traps beat data traps
> Setting the position below the mark **discards** the mark; `reset()` after that throws `InvalidMarkException`. Relative `get`/`put` throw `BufferUnderflowException` / `BufferOverflowException` instead of growing anything — the capacity is fixed at construction. `flip()` on an empty buffer gives `limit = 0` (nothing to read); calling `flip()` twice in a row gives you a zero limit both times. And no buffer method is safe from another thread: synchronize externally or hand the buffer to one consumer at a time.

> [!tip] Interview answer
> A NIO buffer is capacity + position + limit (+ optional mark) with the invariant `0 ≤ mark ≤ position ≤ limit ≤ capacity`. `flip` switches from writing to reading by turning the old position into the limit and zeroing the position; `clear` and `rewind` reset indices without erasing data; `compact` keeps the unread tail. Typed subclasses exist for every primitive except boolean, views can reinterpret a `ByteBuffer`, and buffers are not thread-safe — the selector loop drives them single-threaded.

