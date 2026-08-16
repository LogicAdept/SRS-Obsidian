<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/HashMap #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Сделайте `HashMap` из `HashSet<Mindmap.Entry<K, V>>`.**

```java
HashMap<K, V> map = new HashMap<>(set.size());
for (Mindmap.Entry<K, V> entry : set) {
    map.put(entry.getKey(), entry.getValue());
}
```

# Источник
+ [parshinpn.pro](http://www.parshinpn.pro/content/voprosy-i-otvety-na-sobesedovanii-po-teme-java-collection-framework-chast-1)
+ [Хабрахабр](https://habrahabr.ru/post/162017/)
+ [Quizful](http://www.quizful.net/interview/java)
+ [JavaRush](http://info.javarush.ru/)
+ [Хабрахабр:Справочник по Java Collections Framework](https://habrahabr.ru/post/237043/)
