<!--
reps: 0
priority: 0
-->
#Java/Language #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Какие функциональные интерфейсы из java.util.function ты знаешь?**

Consumer<T> — принимает T, ничего не возвращает (T → void). Supplier<T> — без параметров, возвращает T (() → T). Predicate<T> — принимает T, возвращает boolean. Function<T,R> — T → R. BiFunction<T,U,R> — два параметра. UnaryOperator<T> = Function<T,T>. BinaryOperator<T> = BiFunction<T,T,T>.
