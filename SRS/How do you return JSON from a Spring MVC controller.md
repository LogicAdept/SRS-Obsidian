<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Put `@ResponseBody` on the method (or use `@RestController`) and return a POJO. Jackson’s `HttpMessageConverter` writes JSON.

```java
@RestController
public class JsonController {
    @RequestMapping(value = "/data", method = RequestMethod.GET)
    public MyData getData() {
        return new MyData("Hello", 123);
    }
}
```

> [!warning] Unverified traps from the dump
> - @RestController already implies @ResponseBody; repeating it is redundant.
> - Without Jackson on the classpath, conversion fails.
