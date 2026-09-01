<!--
reps: 0
priority: 0
-->
#Java/Language/Parameters #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Как передается параметры в метод по значению или по ссылке?**

В Java параметр метода – всегда копия объека. Значит параметры передаются всегда по значению, просто это значение может быть ссылкой на объект. Код ниже это демонстрирует.
````java
public static void main(String[] args) {
    var o = new Object();
    var i = 10;
    method(o, i);
    System.out.println(i + " " + o); // 10 and java.lang.Object@....
}

public static void method(Object o, int i) {
    o = null;
    i = 1000;
}
````
