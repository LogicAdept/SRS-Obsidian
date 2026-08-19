<!--
reps: 0
priority: 0
-->
#Java/Collections/List/ArrayList #Java/Collections/Map/HashMap #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: build an `ArrayList` from the map’s **key set**, **values**, or **entry set**:

```java
HashMap<String, String> performanceMap = new HashMap<String, String>();
performanceMap.put("John Kevin", "Average");

ArrayList<String> listOfKeys = new ArrayList<String>(performanceMap.keySet());
ArrayList<String> listOfValues = new ArrayList<String>(performanceMap.values());
ArrayList<Map.Entry<String, String>> listOfEntry =
    new ArrayList<Map.Entry<String, String>>(performanceMap.entrySet());
```
