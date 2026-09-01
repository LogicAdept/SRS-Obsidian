<!--
reps: 0
priority: 0
-->
#Java/OOP/Initialization #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Каков порядок вызова конструкторов и блоков инициализации с учётом иерархии классов?**

Сначала вызываются все статические блоки в очередности от первого статического блока корневого предка и выше по цепочке иерархии до статических блоков самого класса.

Затем вызываются нестатические блоки инициализации корневого предка, конструктор корневого предка и так далее вплоть до нестатических блоков и конструктора самого класса.

>Parent static block(s) → Child static block(s) → Grandchild static block(s)
>
> → Parent non-static block(s) → Parent constructor →
>
> → Child non-static block(s) → Child constructor →
>
> → Grandchild non-static block(s) → Grandchild constructor

Пример 1:

```java
public class MainClass {

    public static void main(String args[]) {
        System.out.println(TestClass.v);
        new TestClass().a();
    }

}
```

```java
public class TestClass {

    public static String v = "Some val";

    {
        System.out.println("!!! Non-static initializer");
    }

    static {
        System.out.println("!!! Static initializer");
    }

    public void a() {
        System.out.println("!!! a() called");
    }

}
```

Результат выполнения:

```
!!! Static initializer
Some val
!!! Non-static initializer
!!! a() called
```

Пример 2:

```java
public class MainClass {

    public static void main(String args[]) {
        new TestClass().a();
    }

}
```

```java
public class TestClass {

    public static String v = "Some val";

    {
        System.out.println("!!! Non-static initializer");
    }

    static {
        System.out.println("!!! Static initializer");
    }

    public void a() {
        System.out.println("!!! a() called");
    }

}
```

Результат выполнения:

```
!!! Static initializer
!!! Non-static initializer
!!! a() called
```
