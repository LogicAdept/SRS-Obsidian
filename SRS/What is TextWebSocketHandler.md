<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebSocket #SRS

# What is `TextWebSocketHandler`?

> [!abstract] Short answer
> **`TextWebSocketHandler`** (Framework 4.0, `org.springframework.web.socket.handler`) is a **`WebSocketHandler`** base class for **text frames only**. Override **`handleTextMessage(WebSocketSession, TextMessage)`** from **`AbstractWebSocketHandler`**. A **binary** frame closes the session with **`CloseStatus.NOT_ACCEPTABLE` (1003)** and reason `"Binary messages not supported"`. Lifecycle methods default to empty. It is **not** a STOMP `@MessageMapping` controller.

## Handler API, not destinations

Implement **`WebSocketHandler`** yourself, or extend **`TextWebSocketHandler`** / **`BinaryWebSocketHandler`**. `handleMessage` on the abstract class dispatches to `handleTextMessage` / `handleBinaryMessage` / `handlePongMessage`. **`supportsPartialMessages()`** defaults to **`false`**. Uncaught exceptions from handler methods are wrapped by **`ExceptionWebSocketHandlerDecorator`** (Java-config / XML) and close with **1011** (`SERVER_ERROR`). Session type: [[What is WebSocketSession]]. Handshake: [[How does the WebSocket handshake work in Spring]]. Mapping: [[What is the EnableWebSocket annotation]]. Contrast STOMP: [[What is STOMP in Spring WebSocket]].

```java
public class MyHandler extends TextWebSocketHandler {

	@Override
	public void handleTextMessage(WebSocketSession session, TextMessage message) {
		// payload: message.getPayload()
	}
}
```

**Listing 1.** Official shape. Register with `registry.addHandler(new MyHandler(), "/myHandler")`. Binary twin: **`BinaryWebSocketHandler`** (text frames rejected the same 1003 way).

`SockJsWebSocketHandler` **extends** `TextWebSocketHandler` **inside** the SockJS transport. Application code still writes a normal handler; SockJS wrapping is not “use `TextWebSocketHandler` to get STOMP.”

```d2
direction: down
api: "WebSocketHandler" {
  width: 240
  height: 40
  style.fill: "#e3f2fd"
}
abs: "AbstractWebSocketHandler" {
  width: 260
  height: 40
  style.fill: "#fff3e0"
}
text: "TextWebSocketHandler\nhandleTextMessage" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}

api -> abs
abs -> text
```

**Fig. 1.** STOMP controllers sit on the **message-broker** configuration, not this type hierarchy.

> [!warning]Binary frames close the socket
> `TextWebSocketHandler` does **not** ignore binary data. It **closes** with **1003**. Partial messages are off unless you override `supportsPartialMessages`. JSR-356 still forbids overlapping `sendMessage` calls — wrap the session (see [[What is WebSocketSession]]).

> [!tip] Interview answer
> **`TextWebSocketHandler` is the raw-API helper: override `handleTextMessage`, register a path with `@EnableWebSocket`.** Binary input gets 1003. For `/app` destinations and a broker, you want `@EnableWebSocketMessageBroker`, not this class.
