<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #Java/Spring/Integration #SRS

# What is the difference between Invalid Message Channel and an error channel?

> [!abstract] Short answer
> **Invalid Message Channel** (EIP): the **receiver** already **got** a message whose **type, format, or headers** it cannot process, so it **moves that message** to a quarantine channel. Payload on that channel is the **improper message**. Spring Integration **`errorChannel`**: an **exception** becomes the payload of an **`ErrorMessage`**. The original `Message` is on **`MessagingException.failedMessage`**, not as the ErrorMessage payload. Glossaries that list Error Channel / DLQ as **AKA** for Invalid Message Channel are **wrong** — related patterns, different contracts.

## Delivered-but-wrong vs thrown vs undeliverable

EIP **Invalid Message Channel**: administrator-defined channel for messages that **make no sense** to the endpoint. The **Dead Letter Channel** is what the **messaging system** does with a message it **cannot deliver** (broker DLQ). SI **errorChannel** is framework **exception** plumbing ([[What is the Invalid Message Channel pattern]], [[What is the Dead Letter Channel pattern]], [[How does a Spring Integration filter discard-channel implement Invalid Message Channel]]).

Resolution for `ErrorMessage`: `errorChannel` **header** on the failed request, else the global bean named **`errorChannel`**. Default global channel is a **`PublishSubscribeChannel`** with a **`LoggingHandler`** at ERROR (`Ordered.LOWEST_PRECEDENCE - 100`). You can subscribe `ErrorMessageExceptionTypeRouter` to split by exception type (that **still** routes **ErrorMessages**, not the raw order body).

Messaging-based `errorChannel` applies to work on a **`TaskExecutor`**, a **queue/executor channel**, or a **poller** (`MessagePublishingErrorHandler` on the scheduler). A **`DirectChannel`** handler runs on the **sender thread**: the exception **propagates to the caller** (gateway / `MessagingTemplate`) and is **not** published to `errorChannel`.

```d2
direction: down
msg: "Delivered Message" {
  width: 180
  height: 40
  style.fill: "#fff3e0"
}
imc: "Invalid Message Channel\nsame payload" {
  width: 220
  height: 50
  style.fill: "#e8f5e9"
}
err: "ErrorMessage\npayload = Exception" {
  width: 240
  height: 50
  style.fill: "#fce4ec"
}
dlc: "Dead Letter Channel\nundeliverable" {
  width: 220
  height: 50
  style.fill: "#e3f2fd"
}
msg -> imc: "receiver cannot process"
msg -> err: "handler throws (async)"
msg -> dlc: "broker cannot deliver"
```

**Fig. 1.** Three different “bad message” places; only IMC keeps the original body as the channel payload.

`ErrorMessageStrategy` can set `originalMessage`; `DefaultErrorMessageStrategy` stores the request under `ErrorMessageUtils.INPUT_MESSAGE_CONTEXT_KEY`. Triage that binds `@Payload Order` on `errorChannel` will not see the order — unwrap **`failedMessage`**.

> [!warning] ErrorMessage payload is the exception
> Operators who subscribe to `errorChannel` expecting the **rejected Order** will see a **`MessagingException`** (or cause). The business body is **`failedMessage.getPayload()`**. Filter **discard-channel** does not wrap.

> [!warning] DirectChannel skips errorChannel
> Sync flows throw like a Java call stack. Enabling a logging subscriber on `errorChannel` does **nothing** for those exceptions unless a gateway **`error-channel`** maps them.

> [!tip] Interview answer
> Invalid Message Channel parks the bad **message**. `errorChannel` parks an **ErrorMessage** whose payload is the **exception**, and only for async/poller failures. Dead letter is **delivery** failure at the broker. Do not treat the three names as synonyms.
