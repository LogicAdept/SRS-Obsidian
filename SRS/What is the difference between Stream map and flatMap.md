<!--
reps: 0
priority: 0
-->
#Java/Streams #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**map vs flatMap.**

map: T → R, один элемент → один. flatMap: T → Stream<R> с уплощением. Пример: List<List<String>> → flatMap(Collection::stream) → плоский Stream<String>. Для Optional: flatMap избегает Optional<Optional<T>>.

**Разница между map и flatMap.**

map: T → R. flatMap: T → Stream с уплощением результата.

**Разница между map и flatMap.**

map: T → R; flatMap: T → Stream<R> с «уплощением».
