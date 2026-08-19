<!--
reps: 0
priority: 0
-->
#Java/Collections/List/ArrayList #Java/Collections/List/LinkedList #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**ArrayList vs LinkedList.**

ArrayList: O(1) доступ по индексу, O(n) вставка в середину, дружелюбно к CPU-кэшу (непрерывная память). LinkedList: O(1) вставка в начало/конец (если есть ссылка), O(n) доступ по индексу. На практике ArrayList почти всегда лучше — даже вставка в середину быстрее из-за локальности кэша.

**Как сделать List неизменяемым?**

List.of(1,2,3) — Java 9+, immutable, null запрещён. List.copyOf(list) — Java 10+, глубокая неизменяемая копия. Collections.unmodifiableList(list) — обёртка (изменения в оригинале видны!). Предпочитай List.of или List.copyOf.

**Как устроен ArrayList внутри?**

Динамический массив. При нехватке места создаёт новый массив в 1.5 раза больше и копирует данные через Arrays.copyOf.

**ArrayList vs LinkedList — что когда использовать?**

ArrayList: быстрый доступ по индексу O(1), быстрая итерация. LinkedList: быстрая вставка/удаление в начале O(1), но поиск O(n). На практике почти всегда выигрывает ArrayList.

**Как из List сделать неизменяемый?**

List.copyOf(list) (Java 10+) или Collections.unmodifiableList(list) — обёртка, которая бросит UnsupportedOperationException на add/remove.

**Как устроен ArrayList?**

Динамический массив. При нехватке места создаёт новый массив в 1.5 раза больше и копирует через Arrays.copyOf.

**ArrayList vs LinkedList.**

ArrayList: O(1) доступ по индексу, быстрая итерация, локальность в кэше. LinkedList: O(1) вставка в начало, но O(n) поиск. На практике почти всегда выигрывает ArrayList.

**Как сделать List неизменяемым?**

List.copyOf(list) (Java 10+) или Collections.unmodifiableList(list). На add/remove — UnsupportedOperationException.

**Коллекции: ArrayList vs LinkedList vs HashMap.**

ArrayList: динамический массив, O(1) доступ, O(n) вставка в середину. LinkedList: двусвязный список, O(1) вставка/удаление, O(n) доступ. HashMap: бакеты + связный список → дерево при ≥8 коллизиях. Для Junior: знать когда что использовать.

**Какие реализации List ты знаешь?**

ArrayList — на основе массива. Доступ по индексу O(1), вставка в конец амортизированно O(1), в середину O(n). Самая популярная. LinkedList — двусвязный список. Доступ по индексу O(n), вставка/удаление в любом месте — O(1) при наличии итератора. Vector — synchronized аналог ArrayList, legacy, не используется.

**Сравни ArrayList и LinkedList по сложности.**

Доступ по индексу: ArrayList O(1), LinkedList O(n) (нужно идти от головы или хвоста). Вставка в конец: ArrayList амортизированный O(1), LinkedList O(1). Вставка в середину: ArrayList O(n) (сдвиг элементов), LinkedList O(n) на поиск + O(1) на саму вставку.

**Почему ArrayList на практике быстрее LinkedList?**

Cache locality. ArrayList хранит элементы в непрерывном куске памяти — процессор подгружает целые блоки в L1/L2 кэш. У LinkedList узлы разбросаны по куче — каждый next() это cache miss. На реальных данных ArrayList выигрывает почти всегда. LinkedList в современном коде использовать не надо — для очередей есть ArrayDeque.

**Как растёт ArrayList?**

Начальная capacity = 10. При переполнении создаётся новый массив размером 1.5× от старого, элементы копируются. Метод trimToSize() ужимает массив до текущего количества элементов. Если заранее знаешь приблизительный размер — задавай в конструкторе: new ArrayList<>(expectedSize).

**Как сортировать List по убыванию по полю?**

list.sort(Comparator.comparing(User::getAge).reversed()) или с лямбдой list.sort((a, b) -> b.getAge() - a.getAge()) — но безопаснее через Comparator.comparing.

**ArrayList vs LinkedList — где быстрее вставка в середину?**

У LinkedList O(1) на саму вставку, но O(n) на поиск позиции. В реальности ArrayList почти всегда быстрее из-за локальности в кэше CPU.

**ArrayList vs LinkedList.**

ArrayList: O(1) доступ, CPU-кэш. LinkedList: O(1) вставка в начало. На практике ArrayList всегда лучше.

**ArrayList vs LinkedList.**

ArrayList: O(1) доступ, O(n) вставка в середину, дружелюбен к CPU-кэшу. LinkedList: O(1) вставка/удаление в начало, O(n) доступ. На практике ArrayList почти всегда лучше.
