<!--
reps: 0
priority: 0
-->
#Java/Library #Java/Versions/8 #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Как создать Base64 кодировщик и декодировщик?**

```java
// Encode
String b64 = Base64.getEncoder().encodeToString("input".getBytes("utf-8")); //aW5wdXQ==
// Decode
new String(Base64.getDecoder().decode("aW5wdXQ=="), "utf-8"); //input
```

# Источники
+ [Хабрахабр - Новое в Java 8](https://habrahabr.ru/post/216431/)
+ [Хабрахабр - Шпаргалка Java программиста 4. Java Stream API](https://habrahabr.ru/company/luxoft/blog/270383/)
+ [METANIT.COM](http://metanit.com/java/tutorial/9.1.php)
+ [javadevblog.com](http://javadevblog.com/interfejsy-v-java-8-staticheskie-metody-metody-po-umolchaniyu-funktsional-ny-e-interfejsy.html)
