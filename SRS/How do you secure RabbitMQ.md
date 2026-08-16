<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS #New

> [!warning] Черновик без доверия
> Текст собран из публичных списков вопросов по RabbitMQ (2026). Не сверен с официальной документацией RabbitMQ. Не считать ответом для ревью.

**How do you secure a broker?**

AMQPS (5671) / TLS for management, strong users (not guest remote), least-privilege per vhost, loopback_users, firewall, disable unused plugins, LDAP/OAuth if enterprise. Management UI is not public. Guest/guest only on localhost by default.
