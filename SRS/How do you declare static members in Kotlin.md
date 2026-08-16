<!--
reps: 0
priority: 0
-->
#Kotlin #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

Привычного static в Kotlin нет.

Если взять java код и автоматически преобразовать его в kotlin, то static сотрётся. По-крайней мере так было во времена версии 1.3.

Но static в байт-коде создаётся, если
- создать функцию уровня пакета:
```kotlin
package com.example.mytestapplication

fun testFun(){
    // some code
}
```

- использовать companion object + @JvmStatic внутри класса:
```kotlin
class SimpleClassKotlin1 {

    companion object{

        // @JvmField делает поле прямым статическим полем
        @JvmStatic // будут сгенерированы статический геттер и сеттер к этому свойству
        var companionField = "Hello!"

        @JvmStatic // чтобы функция объекта-компаньона также преобразовалась в статический метод
        fun companionFun (vaue: String){
            // some code
        }
    }
}
```
