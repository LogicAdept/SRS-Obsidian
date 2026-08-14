<!--
reps: 0
priority: 0
-->
#Java/Collections/Map #SRS #New

```java
   public static void main(String args[]) {  
        Map map = new HashMap();  
  
        int[] k1 = new int[] {1, 2};  
        int hash1 = k1.hashCode();  
  
        map.put(k1, new Object());  
  
        int[] k2 = new int[] {1, 2};  
        int hash2 = k2.hashCode();  
  
        System.out.println(map.get(k1));  
        System.out.println(map.get(k2));  
        System.out.println(hash1 == hash2);  
    }
```

