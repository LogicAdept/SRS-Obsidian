<!--
reps: 0
priority: 0
-->
#Java/Spring/Transactions #Java/Annotations #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**@Transactional — под капотом.**

Spring создаёт прокси-обёртку. JDK dynamic proxy (если интерфейс) или CGLIB (наследование). Прокси: открывает транзакцию (PlatformTransactionManager), вызывает метод, commit при успехе, rollback при RuntimeException/Error. Checked НЕ откатывают — нужно rollbackFor.

**Что такое @Transactional?**

Аннотация, которая открывает транзакцию перед методом и коммитит после или откатывает при исключении. По умолчанию откат на RuntimeException и Error, но не на checked.

**Как работает @Transactional под капотом?**

Spring создаёт прокси (JDK dynamic proxy для интерфейсов или CGLIB для классов). Прокси открывает транзакцию перед методом, коммитит после или откатывает при исключении.

**Почему @Transactional не работает при self-invocation?**

Вызов this.method() идёт минуя прокси. Решение: вынести метод в другой бин или инжектить self через ApplicationContext / @Lazy self.

**Что такое @Transactional?**

Аннотация, которая открывает транзакцию вокруг метода. На успешный возврат — COMMIT, на RuntimeException — ROLLBACK. Реализуется через AOP-прокси: вызов идёт через прокси, который и управляет транзакцией.

**Что произойдёт при вызове @Transactional-метода из того же класса?**

Транзакция НЕ откроется. Внутри одного бина вызов this.method() идёт напрямую на объект, в обход прокси. Это любимая ловушка на собесах — самая частая ошибка. Решения: (1) Self-injection — внедрить бин сам в себя через ApplicationContext. (2) Вынести метод в другой бин. (3) Перейти на AspectJ — там работает self-invocation.

**Как работает @Transactional под капотом?**

Spring создаёт прокси (JDK dynamic proxy или CGLIB). При вызове метода через прокси — открывается транзакция, в finally — commit/rollback.

**Почему @Transactional не работает при вызове метода того же класса?**

Self-invocation идёт минуя прокси. Решение: вынести метод в отдельный бин или inject self.

**@Transactional на private методе — что произойдёт?**

Ничего — транзакция не создастся. CGLIB-прокси наследует класс, но private методы не переопределяемы → прокси их не видит. JDK Dynamic Proxy работает через интерфейс — private вообще не в интерфейсе. Решение: сделать метод package-private или public.

**Два @Transactional метода в одном классе: A() вызывает B(). Сколько транзакций?**

Одна. Вызов this.B() минует прокси → @Transactional на B() не работает. B() выполняется в транзакции A() (Propagation.REQUIRED по умолчанию). Если нужна отдельная транзакция для B() — вынести в другой бин или self-injection через @Lazy.

**@Transactional + долгий REST-вызов внутри — чем опасно?**

Транзакция удерживает соединение к БД всё время REST-вызова (секунды). Пул соединений исчерпается → все потоки ждут → сервис висит (connection starvation). Решение: read → close transaction → REST → open transaction → write. Или вынести REST-вызов за @Transactional.

**В какой момент происходит коммит @Transactional?**

После успешного завершения метода (без исключений). Прокси: try { beginTransaction; target.method(); commit; } catch { rollback; }. Rollback по умолчанию: RuntimeException и Error. Checked — НЕ откатывают (нужен rollbackFor). flush != commit: flush отправляет SQL, commit фиксирует.

**@Transactional.**

Прокси (JDK/CGLIB). Открывает транзакцию, commit/rollback. self-call минует прокси. Rollback на RuntimeException/Error; checked — нужен rollbackFor.

**@Transactional — прокси.**

Spring создаёт прокси (JDK/CGLIB). Прокси открывает транзакцию, вызывает метод, commit/rollback. self-call минует прокси → @Transactional/@Cacheable/@Async не работают. Решение: вынести в другой бин.

**How does @Transactional work at interview level?**

Источник: https://habr.com/ru/articles/967632/

Прокси вокруг метода (JDK или CGLIB). TransactionInterceptor открывает транзакцию до метода и commit/rollback после.
Propagation: REQUIRED (default), REQUIRES_NEW, NESTED, SUPPORTS, NOT_SUPPORTED, NEVER, MANDATORY.
Isolation: READ_COMMITTED, REPEATABLE_READ, SERIALIZABLE, READ_UNCOMMITTED.
Почему может не работать: private метод; внутренний this.method(); final класс/метод; setRollbackOnly без корректного отката.

**Default rollback and proxy recap?**

Rollback on unchecked only. REQUIRED default. Proxy AOP: private/self-invoke/final skip it. rollbackFor, isolation, timeout, readOnly.
