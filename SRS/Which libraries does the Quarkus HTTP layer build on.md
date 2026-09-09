<!--
reps: 0
priority: 0
-->
#Java/Quarkus #SRS #New

# Which libraries does the Quarkus HTTP layer build on

> [!warning] Untrusted draft
> Drafted from general framework knowledge, not from an opened question dump. Not yet checked against official documentation. Do not treat this as a review answer.
Draft cue: Quarkus HTTP is served by Vert.x Web on top of Netty (quarkus-vertx-http); Quarkus REST (formerly RESTEasy Reactive) sits on that stack, as do reactive routes, websockets and the dev console.
Interview point: it is NOT Tomcat/Undertow by default; blocking servlet stack is a separate Undertow extension.
