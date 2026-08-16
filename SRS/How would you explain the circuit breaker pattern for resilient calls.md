<!--
reps: 0
priority: 0
-->
#Patterns/DistributedSystems #SystemDesign/Reliability #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Circuit Breaker — зачем?**

Защита от каскадных падений. При N ошибках подряд «размыкается» — запросы сразу отклоняются, сервис получает время оправиться.

**Circuit Breaker: три состояния.**

CLOSED: всё работает, запросы проходят. При N ошибок (или % ошибок > threshold) → OPEN. OPEN: все запросы блокируются, возвращается fallback. Через waitDuration → HALF_OPEN. HALF_OPEN: пропускает N тестовых запросов. Если успешны → CLOSED. Если неуспешны → OPEN. Resilience4j: @CircuitBreaker(name="backend", fallbackMethod="fallback").
