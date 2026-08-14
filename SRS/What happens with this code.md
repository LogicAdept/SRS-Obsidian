<!--
reps: 0
priority: 0
-->
#Java/Language #Java/JVM #Java/Concurrency  #Java/CodeSnippet #Career/Interview/Exercises #SRS #New
```java
private void iter() {  
     List<Integer> list = new ArrayList<>();  
     list.add(0);  
  
     for (Integer integer : list) {  
       list.add(0, 1);  
     }  
  
     for (int i = 0; i < list.size(); i++) {  
       list.add(0, 2);  
     }  
  
     System.out.println(list.get(1));  
   }  
  
   -----  
   - ConcurrentModificationException on the first for-loop  
   - infinite loop on the second for-loop  
   - на сколько будет бесконечный цикл? До какого предела мы будем итерировать? Какая ошибка вывалит?
```