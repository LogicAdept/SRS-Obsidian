<!--
reps: 0
priority: 0
-->
#Networking/Web #SRS
# What is the World Wide Web

> [!abstract] Short answer
> The World Wide Web is the information service built on the Internet where documents (and now applications) are addressed by URLs, transferred by HTTP(S), and interlinked by hyperlinks. Invented by Tim Berners-Lee at CERN around 1989–1991, it runs *on top of* the Internet — the web is one service among many (alongside mail, DNS, chat), not a synonym for the network itself.

## The three primitives

1. **URL/URI** — a uniform name for every resource: scheme (protocol), host (resolved by DNS), path/query/fragment.
2. **HTTP(S)** — the request/response protocol browsers and servers speak: "GET this resource" → bytes + metadata ([[What is HTTP]]).
3. **HTML + hyperlinks** — the document format whose links turn separate pages into one navigable graph ("web"); CSS styles it, JavaScript makes it dynamic.

```d2
direction: down
browser: "Browser" { width: 180; height: 60; style.fill: "#e3f2fd" }
dns: "DNS: name -> IP" { width: 220; height: 60; style.fill: "#fff3e0" }
http: "HTTP(S) over TCP: fetch document" { width: 300; height: 60; style.fill: "#fff3e0" }
doc: "HTML document\nwith links to more URLs" { width: 280; height: 70; style.fill: "#e8f5e9" }
browser -> dns -> http -> doc
doc -> browser: "render; links point onward"
```

**Fig. 1.** One page load cycles all web primitives; every link in the document repeats the cycle — that recursion *is* the web.

## Web vs Internet vs applications

The **Internet** is the packet-switching network (IP, routers, links); the **web** is the hypertext service layered on it, alongside email (SMTP/IMAP), file transfer, games. A "web application" is the modern end of this evolution: pages whose logic lives in the browser (JavaScript) talking to servers over HTTP APIs rather than shipping static documents ([[What is a web application]]). Standards for all of it are stewarded by W3C (HTML, CSS, accessibility) together with WHATWG, IETF (HTTP, URL specs) and ECMA (JavaScript) — see [[What is the W3C]].

> [!warning] "WWW" is not "the Internet", and it is not the prefix either
> Two classic conflations: (1) saying "the WWW and the Internet are the same" erases the service/network distinction — email worked decades beside it; (2) `www.` is merely a hostname convention, a subdomain whose record points at the web server — the *service* does not depend on it ([[What is the difference between a MAC address and an IP address]]-level basic, but the confusion is real in interviews). Also, deep tech: the first browser was also an editor — read/write web was the original vision; read-only web won for decades.

Deeper mechanics: [[What happens when you type a URL into a browser and press Enter]], [[What is the difference between HTTP and HTTPS]]; history anchor: the first site at info.cern.ch (1991) described "The WorldWideWeb project" — hierarchical names, hypertext links, and a browser/editor, most of which survived.

> [!tip] Interview answer
> The web is the hypertext system on top of the Internet: resources named by URLs, fetched by HTTP(S), and rendered from HTML with hyperlinks binding pages into one graph. I keep the layering straight — Internet is the network, the web is a service on it, alongside mail and others — and mention CERN 1991 and the standards bodies (W3C/WHATWG, IETF) as the governance frame.
