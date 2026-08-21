<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Unchecked #Java/Collections/Iteration #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Что такое ConcurrentModificationException?**

Бросается итератором, если коллекция изменилась во время итерации не через сам итератор. Реализуется через счётчик modCount внутри коллекции и expectedModCount внутри итератора. Если они разъезжаются — исключение. // ❌ Так нельзя List<String> list = new ArrayList<>(List.of("a", "b", "c")); for (String s : list) { if (s.equals("b")) list.remove(s); // ConcurrentModificationException }
