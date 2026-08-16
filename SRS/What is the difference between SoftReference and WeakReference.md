<!--
reps: 0
priority: 0
-->
#Java/JVM/Memory #Java/Language #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**WeakReference / SoftReference / PhantomReference.**

Weak — GC собирает при первой сборке (WeakHashMap). Soft — при нехватке памяти (кэши). Phantom — постфинализационная очистка. ReferenceQueue для уведомлений.

**WeakReference / SoftReference / PhantomReference.**

Weak — GC собирает при первой же сборке. Soft — GC собирает при нехватке памяти (для кэшей). Phantom — для постфинализационной очистки ресурсов. WeakHashMap — ключи через WeakReference.

**How do SoftReference and WeakReference differ?**

Источник: https://habr.com/ru/articles/967190/

Soft: объект живёт до давления по памяти, типично для кешей. Weak: может быть собран немедленно, если сильных ссылок нет; WeakHashMap с автоудалением.
