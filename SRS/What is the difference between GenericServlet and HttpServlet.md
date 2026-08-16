<!--
reps: 0
priority: 0
-->
#Java/Servlet #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Generics — зачем нужны?**

Типобезопасность на этапе компиляции. Без generics: List list = new ArrayList(); list.add(123); String s = (String)list.get(0) → ClassCastException в рантайме. С generics: List<String> — компилятор не даст положить Integer. Type erasure: в рантайме параметр стирается (List<String> → List).
