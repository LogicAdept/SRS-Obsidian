<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/HashMap #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Какова оценка временной сложности операций над элементами из `HashMap`? Гарантирует ли `HashMap` указанную сложность выборки элемента?**

В общем случае операции добавления, поиска и удаления элементов занимают константное время.

Данная сложность не гарантируется, т.к. если хэш-функция распределяет элементы по корзинам равномерно, временная сложность станет не хуже [_Логарифмического времени_ ](https://ru.wikipedia.org/wiki/%D0%92%D1%80%D0%B5%D0%BC%D0%B5%D0%BD%D0%BD%D0%B0%D1%8F_%D1%81%D0%BB%D0%BE%D0%B6%D0%BD%D0%BE%D1%81%D1%82%D1%8C_%D0%B0%D0%BB%D0%B3%D0%BE%D1%80%D0%B8%D1%82%D0%BC%D0%B0#%D0%9B%D0%BE%D0%B3%D0%B0%D1%80%D0%B8%D1%84%D0%BC%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%BE%D0%B5_%D0%B2%D1%80%D0%B5%D0%BC%D1%8F) O(log(N)), а в случае, когда хэш-функция постоянно возвращает одно и то же значение, `HashMap` превратится в связный список со сложностью О(n).

Пример кода двоичного поиска:
```java
public class Q {
    public static void main(String[] args) {
        Q q = new Q();
        q.binSearch();
    }

    private void binSearch() {
        int[] inpArr = {1, 2, 3, 4, 5, 6, 7, 8, 9};
        Integer result = binSearchF(inpArr, 1, 0, inpArr.length - 1);
        System.out.println("-----------------------");
        result = binSearchF(inpArr, 2, 0, inpArr.length - 1);
        System.out.println("Found at position " + result);
    }

    private Integer binSearchF(int[] inpArr, int searchValue, int low, int high) {
        Integer index = null;
        while (low <= high) {
            System.out.println("New iteration, low = " + low + ", high = " + high);
            int mid = (low + high) / 2;
            System.out.println("trying mid = " + mid + " inpArr[mid] = " + inpArr[mid]);
            if (inpArr[mid] < searchValue) {
                low = mid + 1;
                System.out.println("inpArr[mid] (" + inpArr[mid] + ") < searchValue(" + searchValue + "), mid = " + mid
                        + ", setting low = " + low);
            } else if (inpArr[mid] > searchValue) {
                high = mid - 1;
                System.out.println("inpArr[mid] (" + inpArr[mid] + ") > searchValue(" + searchValue + "), mid = " + mid
                        + ", setting high = " + high);
            } else if (inpArr[mid] == searchValue) {
                index = mid;
                System.out.println("found at index " + mid);
                break;
            }
        }
        return index;
    }
}
```
