<!--
reps: 0
priority: 0
-->
#Java/NIO #SRS

# How does NIO provide non-blocking access to resources

> [!abstract] Short answer
> **Through the selector/selection-key mechanism: a `SelectableChannel` set to non-blocking mode registers interest in readiness events (`OP_ACCEPT`, `OP_CONNECT`, `OP_READ`, `OP_WRITE`) with a `Selector`, and one thread's `select()` call reports which of thousands of channels are ready — instead of one blocked thread per connection.** Non-blocking applies to sockets and pipes; files stay blocking-only.

## The multiplexing loop

Three moving parts: the channel (opened and configured non-blocking), the selector (created via `Selector.open()`), and the `SelectionKey` that ties them together and carries the interest set. Registration is only possible in non-blocking mode. Each `select()` returns the count of channels that became ready, and `selectedKeys()` hands you the set to drain.

```d2
direction: down
reg: "channels register interest\n(accept / connect / read / write)" {
  width: 330
  height: 90
  style.fill: "#e3f2fd"
}
sel: "Selector.select()\none thread waits for many" {
  width: 300
  height: 90
  style.fill: "#fff3e0"
}
sk: "selectedKeys()\nonly READY channels returned" {
  width: 300
  height: 90
  style.fill: "#fff3e0"
}
h: "handler reads into ByteBuffer\nimmediately, never blocks" {
  width: 340
  height: 90
  style.fill: "#e8f5e9"
}
reg -> sel -> sk -> h
```

**Fig. 1.** One thread, many channels: the selector inverts the model — instead of threads waiting on data, the thread waits on the selector and data is ready when it returns.

The selector maintains three key sets (from the javadoc): the key set of current registrations, the selected-key set of channels ready for operations in their interest set, and the cancelled-key set. The standard loop removes each ready key from the selected set, dispatches it, and re-arms.

```java
ServerSocketChannel server = ServerSocketChannel.open();
server.bind(new InetSocketAddress(0));      // ephemeral port for the demo
server.configureBlocking(false);            // required for registration
Selector selector = Selector.open();
server.register(selector, SelectionKey.OP_ACCEPT);

// a client connects from another thread
Thread client = new Thread(() -> {
    try (SocketChannel c = SocketChannel.open()) {
        c.connect(new InetSocketAddress("localhost", server.socket().getLocalPort()));
        c.write(ByteBuffer.wrap("ping".getBytes(StandardCharsets.UTF_8)));
    } catch (IOException e) { }
});
client.start();

while (true) {
    int ready = selector.select(5_000);      // blocks up to 5 s, then 0
    System.out.println("select returned: " + ready);
    if (ready == 0) break;
    Iterator<SelectionKey> it = selector.selectedKeys().iterator();
    while (it.hasNext()) {
        SelectionKey key = it.next();
        it.remove();                         // the set is NOT auto-cleared
        if (key.isAcceptable()) {
            SocketChannel peer = server.accept();
            System.out.println("accepted a connection, non-blocking: " + peer.isBlocking());
            peer.configureBlocking(false);
            peer.register(selector, SelectionKey.OP_READ);
        }
    }
}
```

**Listing 1.** The accept side of a single-threaded server. `select()` woke up only when the client's TCP connect arrived — no thread sat blocked inside `accept()` between events. (Verified on JDK 21; the client side was a separate thread that then wrote "ping".)

> [!warning] Non-blocking is not the same as asynchronous, and selected keys bite
> The interview traps in order of frequency. First, "NIO never blocks" is false — `select()` blocks (that is the point); what never blocks is channel I/O after `configureBlocking(false)`: a `read()` on a socket without data returns `0` immediately instead of parking the thread. Second, NIO is synchronous non-blocking — the readiness event model — while `AsynchronousSocketChannel`/`AsynchronousChannelGroup` (NIO.2, Java 7+) is the asynchronous completion-based API; mixing them up is a classic slip. Third, the bug pattern: `selector.selectedKeys()` is not cleared automatically — forgetting `it.remove()` re-dispatches stale events; and `accept()` in non-blocking mode can legally return `null`, so code assuming a connection crashes on the benign case. Files: `FileChannel` has no selector support — multiplexing is socket/pipe territory. Stream-level context: [[What are channels in Java NIO]], the trade-off comparison in [[How would you explain advantages of Java NIO over classic blocking IO]], and the blocking baseline in [[How would you explain in how is difference between IO and NIO]].

> [!tip] Interview answer
> **NIO gets non-blocking behavior from selectable channels plus a selector: you set the channel non-blocking, register it with interest ops like OP_ACCEPT or OP_READ, and one thread calls select(), which reports exactly which channels are ready. That replaces one blocked thread per connection with one thread multiplexing thousands. Channel I/O returns immediately with zero bytes instead of blocking; files are the exception — no selector support. And it is synchronous non-blocking, not async NIO.2.**

