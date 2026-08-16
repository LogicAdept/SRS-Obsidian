<!--
reps: 0
priority: 0
-->
#Java/Collections #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Реализуйте симметрическую разность двух коллекций используя методы `Collection` (`addAll(...)`, `removeAll(...)`, `retainAll(...)`).**

Симметрическая разность двух коллекций - это множество элементов, одновременно не принадлежащих обоим исходным коллекциям.

```java
<T> Collection<T> symmetricDifference(Collection<T> a, Collection<T> b) {
    // Объединяем коллекции.
    Collection<T> result = new ArrayList<>(a);
    result.addAll(b);

    // Получаем пересечение коллекций.
    Collection<T> intersection = new ArrayList<>(a);
    intersection.retainAll(b);

    // Удаляем элементы, расположенные в обоих коллекциях.
    result.removeAll(intersection);

    return result;
}
```
