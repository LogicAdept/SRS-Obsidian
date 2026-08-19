<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebSocket #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Convenience `WebSocketHandler` for text frames. Dumps override `handleTextMessage`. Binary counterpart is `BinaryWebSocketHandler`. Session type is `WebSocketSession`.

> [!warning] Unverified traps from the dump
> - Not a STOMP controller. STOMP text still arrives as STOMP frames on the broker stack, not this class, unless you chose raw WebSocket.

