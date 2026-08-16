<!--
reps: 0
priority: 0
-->
#Networking/Web/Protocols/WebSocket #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

WebSocket is a protocol which enables communication between the server and the browser. It has an advantage over RESTful HTTP because communications are both bi-directional and real-time. This allows for the server to notify the client at any time instead of the client polling on a regular interval for updates.

Following are some of the drawbacks of HTTP due to which they are unsuitable for certain scenarios-

![alt text](https://github.com/learning-zone/spring-interview-questions/blob/spring/assets/http-request.jpg)

* **Traditional HTTP** requests are unidirectional - In traditional client server communication, the client always initiates the * request.
* **Half Duplex** - User requests for a resource and the server then serves it to the client. The response is only sent after the request. So at a time only a single request occurs.
* **Multiple TCP connections** - For each request a new TCPsession is needed to be established and then closed after receiving the response. So without using WebSockets we will have multiple sessions.
* **Heavy** - Normal HTTP request and response require exchange of extra data between client and server.

WebSocket is a computer communications protocol, providing full-duplex communication channels over a single TCP connection.

![alt text](https://github.com/learning-zone/spring-interview-questions/blob/spring/assets/web-socket.jpg)

* **WebSocket are bi-directional** - Using WebSocket either client or server can initiate sending a message.
* **WebSocket are Full Duplex** - The client and server communication is independent of each other.
* **Single TCP connection** - The initial connection is using HTTP, then this connection gets upgraded to a socket based * connection. This single connection is then used for all the future communication
* **Light** - The WebSocket message data exchange is much lighter compared to http.

**WebSockets Implementation** 

In the Maven we need the spring boot WebSocket dependency.Maven will be as follows-
```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
	<modelVersion>4.0.0</modelVersion>

	<groupId>com.javaexample</groupId>
	<artifactId>boot-websocket</artifactId>
	<version>1.0-SNAPSHOT</version>

	<parent>
		<groupId>org.springframework.boot</groupId>
		<artifactId>spring-boot-starter-parent</artifactId>
		<version>1.4.1.RELEASE</version>
	</parent>

	<dependencies>
		<dependency>
			<groupId>org.springframework.boot</groupId>
			<artifactId>spring-boot-starter-websocket</artifactId>
		</dependency>

		<dependency>
			<groupId>org.json</groupId>
			<artifactId>json</artifactId>
			<version>20171018</version>
		</dependency>
	</dependencies>

	<build>
		<plugins>
			<plugin>
				<groupId>org.springframework.boot</groupId>
				<artifactId>spring-boot-maven-plugin</artifactId>
			</plugin>
		</plugins>
	</build>

</project>
```
Create the SpringBoot Bootstrap class as below-
```java
package com.javaexample.websocket.config;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class Application {

	public static void main(String[] args) {
		SpringApplication.run(Application.class, args);
	}
}
```
On the Server end, we recieve the data and reply back to the client. In Spring we can create a customized handler by using either TextWebSocketHandler or BinaryWebSocketHandler.

```java
package com.javaexample.websocket.config;
import java.io.IOException;
import org.json.JSONObject;
import org.springframework.stereotype.Component;
import org.springframework.web.socket.TextMessage;
import org.springframework.web.socket.WebSocketSession;
import org.springframework.web.socket.handler.TextWebSocketHandler;

@Component
public class SocketTextHandler extends TextWebSocketHandler {

	@Override
	public void handleTextMessage(WebSocketSession session, TextMessage message)
			throws InterruptedException, IOException {

		String payload = message.getPayload();
		JSONObject jsonObject = new JSONObject(payload);
		session.sendMessage(new TextMessage("Hi " + jsonObject.get("user") + " how may we help you?"));
	}

}
```
In order to tell Spring to forward client requests to the endpoint , we need to register the handler.
```java
package com.javaexample.websocket.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.web.socket.config.annotation.EnableWebSocket;
import org.springframework.web.socket.config.annotation.WebSocketConfigurer;
import org.springframework.web.socket.config.annotation.WebSocketHandlerRegistry;

@Configuration
@EnableWebSocket
public class WebSocketConfig implements WebSocketConfigurer {

	public void registerWebSocketHandlers(WebSocketHandlerRegistry registry) {
		registry.addHandler(new SocketTextHandler(), "/user");
	}

}
```
Next we define the UI part for establishing WebSocket and making the calls-
Define the app.js as follows-
```javascript
var ws;
function setConnected(connected) {
	$("#connect").prop("disabled", connected);
	$("#disconnect").prop("disabled", !connected);
}

function connect() {
	ws = new WebSocket('ws://localhost:8080/user');
	ws.onmessage = function(data) {
		helloWorld(data.data);
	}
	setConnected(true);
}

function disconnect() {
	if (ws != null) {
		ws.close();
	}
	setConnected(false);
	console.log("Websocket is in disconnected state");
}

function sendData() {
	var data = JSON.stringify({
		'user' : $("#user").val()
	})
	ws.send(data);
}

function helloWorld(message) {
	$("#helloworldmessage").append(" " + message + "");
}

$(function() {
	$("form").on('submit', function(e) {
		e.preventDefault();
	});
	$("#connect").click(function() {
		connect();
	});
	$("#disconnect").click(function() {
		disconnect();
	});
	$("#send").click(function() {
		sendData();
	});
});
```
Define the index.html as follows-
```html
<!DOCTYPE html>
<html>
<head>
    <title>WebSocket Chat Application </title>
    <link href="/bootstrap.min.css" rel="stylesheet">
    <link href="/style.css" rel="stylesheet">
    <script src="/jquery-1.10.2.min.js"></script>
    <script src="/app.js"></script>
</head>
<body>
<div id="main-content" class="container">
    <div class="row">
        <div class="col-md-8">
            <form class="form-inline">
                <div class="form-group">
                    <label for="connect">Chat Application:</label>
                    <button id="connect" type="button">Start New Chat</button>
                    <button id="disconnect" type="button" disabled="disabled">End Chat
                    </button>
                </div>
            </form>
        </div>
    </div>
    <div class="row">
        <div class="col-md-12">
            <table id="chat">
                <thead>
                <tr>
                    <th>Welcome user. Please enter you name</th>
                </tr>
                </thead>
                <tbody id="helloworldmessage">
                </tbody>
            </table>
        </div>
            <div class="row">
        
        <div class="col-md-6">
            <form class="form-inline">
                <div class="form-group">
                    <textarea id="user" placeholder="Write your message here..." required></textarea>
                </div>
                <button id="send" type="submit">Send</button>
            </form>
        </div>
        </div>
    </div>
  </div>
</body>
</html>
```
Start the application- http://localhost:8080 Click on start new chat it opens the WebSocket connection.

**Что такое _WebSocket_?**

__WebSocket__ — протокол полнодуплексной связи поверх TCP-соединения, предназначенный для обмена сообщениями между браузером и web-сервером в режиме реального времени.

Протокол _WebSocket_ определяет две URI схемы

+ `ws:` - нешифрованное соединение
+ `wss:` - шифрованное соединение
