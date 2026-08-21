<!--
reps: 0
priority: 0
-->
#Networking/OSI #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Common interview mapping of the seven layers:

- Application: end-user network services and application protocols (often cited: HTTP).
- Presentation: context between application entities; dumps often put encryption and format conversion here.
- Session: establish, manage, and terminate sessions between applications.
- Transport: end-to-end transfer of data sequences between hosts (TCP and UDP).
- Network: transfer datagrams between networks; logical addressing (IP).
- Data link: link between directly connected nodes; MAC addressing and frames.
- Physical: electrical, optical, or radio specifications; bits on the medium.
> [!warning] Unverified traps from the dump
> - Real stacks blur Session/Presentation into the TCP/IP Application layer.
> - Putting TLS solely at Presentation is a popular teaching simplification; implementations sit across transport and application concerns.
