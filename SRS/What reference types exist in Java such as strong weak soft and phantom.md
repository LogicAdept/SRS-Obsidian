<!--
reps: 0
priority: 0
-->
#Java/JVM/Memory #Java/Language #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Виды ссылок: Strong, Soft, Weak, Phantom.**

Strong: обычная, GC не трогает. Soft: GC собирает при нехватке памяти (кэши). Weak: GC собирает при первой сборке (WeakHashMap). Phantom: get() всегда null, уведомление через ReferenceQueue (постфинализационная очистка). Циклические ссылки: GC соберёт — определяет достижимость от GC Roots, а не reference counting.

**Какие виды ссылок в Java?**

Strong (обычная new) — пока есть Strong-ссылка, объект не соберётся. Soft (SoftReference) — собирается, когда не хватает памяти. Для кэшей. Weak (WeakReference) — собирается при следующей сборке, даже если есть память. Например, ключи WeakHashMap. Phantom (PhantomReference) — для post-finalization очистки, используется редко.

**What Java reference types exist?**

Источник: https://habr.com/ru/articles/967190/

Strong — обычные ссылки; пока есть хотя бы одна, объект не собирается. Soft — удаляется только при нехватке памяти; кеши; get() может вернуть null. Weak — может быть собран сразу, если остались только weak; WeakHashMap. Phantom — объект уже помечен к удалению; get() всегда null; нужен ReferenceQueue для контроля финализации/off-heap.
