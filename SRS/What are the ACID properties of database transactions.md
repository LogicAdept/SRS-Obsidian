<!--
reps: 0
priority: 0
-->
#Databases/Transactions #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**ACID.**

Atomicity — целиком или никак. Consistency — валидное состояние БД (constraints). Isolation — параллельные транзакции изолированы (зависит от уровня). Durability — после COMMIT данные сохранятся (WAL в PostgreSQL).

**Что такое ACID?**

Atomicity — транзакция выполняется целиком или не выполняется вовсе. Consistency — БД переходит из одного валидного состояния в другое. Isolation — параллельные транзакции не мешают друг другу. Durability — после commit данные не пропадут даже при сбое.

**ACID — расшифровать каждое.**

Atomicity — транзакция целиком или никак. Consistency — БД переходит из валидного состояния в валидное. Isolation — параллельные транзакции не мешают. Durability — после commit данные не теряются.

**Расскажи ACID.**

Atomicity — атомарность: транзакция выполняется целиком или откатывается. Consistency — консистентность: БД переходит из одного валидного состояния в другое (констрейнты соблюдаются). Isolation — изоляция: параллельные транзакции не мешают друг другу. Durability — стойкость: после COMMIT данные сохраняются даже при сбое.

**ACID — расшифровать.**

Atomicity (всё или ничего), Consistency (целостность), Isolation (параллельные транзакции), Durability (сохранность после commit).

**ACID.**

Atomicity, Consistency, Isolation, Durability. WAL в PostgreSQL для Durability.

**ACID.**

Atomicity (целиком/никак), Consistency (валидное состояние), Isolation (изоляция транзакций), Durability (после COMMIT данные сохранятся — WAL в PostgreSQL).

**ACID with a Postgres money-transfer example?**

Atomic: both accounts or neither. Consistent: constraints. Isolated: snapshot/SSI. Durable: WAL. Retry serialization_failure.
