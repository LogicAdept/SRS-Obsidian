<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #API/REST #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

* **@RestController**: The @RestController is a stereotype annotation. It adds `@Controller` and `@ResponseBody` annotations to the class. It requires to import `org.springframework.web.bind.annotation` package.
The @RestController annotation informs to the Spring to render the result back to the caller.
```java
import org.springframework.web.bind.annotation.RestController;  
@RestController  // using @RestController annotation  
public class HomeController {  
    // controller body  
}  
```
* **@RequestMapping**: The @RequestMapping annotation is used to provide routing information. It tells to the Spring that any HTTP request should map to the corresponding method. It requires to import `org.springframework.web.annotation` package.
Example: Here method index() should map with `/index` url
```java
import org.springframework.web.bind.annotation.RequestMapping;  
import org.springframework.web.bind.annotation.RestController;  
@RestController  
public class HomeController {  
    @RequestMapping(value = "/index", method = "GET")  
    public String index() {  
        return "Dashboard Page!";  
    }  
}  
```
* **@RequestParam**: @RequestParam is a Spring annotation used to bind a web request parameter to a method parameter.
It has the following optional elements: 

 * **defaultValue**: used as a fallback when the request parameter is not provided or has an empty value
 * **name**: name of the request parameter to bind to
 * **required**: tells whether the parameter is required
 * **value**: alias for name

1. A Simple Mapping
```java
@GetMapping("/api/foos")
@ResponseBody
public String getFoos(@RequestParam String id) {
    return "ID: " + id;
}
```
Output
```
http://localhost:8080/api/foos?id=abc
----
ID: abc
```
2. Specifying the Request Parameter Name
```java
@PostMapping("/api/foos")
@ResponseBody
public String addFoo(@RequestParam(name = "id") String fooId, @RequestParam String name) { 
    return "ID: " + fooId + " Name: " + name;
}
```
3. Making an Optional Request Parameter
```java
@GetMapping("/api/foos")
@ResponseBody
public String getFoos(@RequestParam(required = false) String id) { 
    return "ID: " + id;
}
```
Output
```
http://localhost:8080/api/foos?id=abc
----
ID: abc

http://localhost:8080/api/foos
----
ID: null
```
4. A Default Value for the Request Parameter
```java
@GetMapping("/api/foos")
@ResponseBody
public String getFoos(@RequestParam(defaultValue = "test") String id) {
    return "ID: " + id;
}
```
Output
```
http://localhost:8080/api/foos
----
ID: test

http://localhost:8080/api/foos?id=abc
----
ID: abc
```
5. Mapping All Parameters
```java
@PostMapping("/api/foos")
@ResponseBody
public String updateFoos(@RequestParam Map<String,String> allParams) {
    return "Parameters are " + allParams.entrySet();
}
```
Output
```
curl -X POST -F 'name=abc' -F 'id=123' http://localhost:8080/api/foos
-----
Parameters are {[name=abc], [id=123]}
```
6. Mapping a Multi-Value Parameter
```java
@GetMapping("/api/foos")
@ResponseBody
public String getFoos(@RequestParam List<String> id) {
    return "IDs are " + id;
}
```
Output
```
http://localhost:8080/api/foos?id=1,2,3
----
IDs are [1,2,3]

http://localhost:8080/api/foos?id=1&id=2
----
IDs are [1,2]
```

* **@ContextConfiguration**: This annotation specifies how to load the application context while writing a unit test for the Spring environment. Here is an example of using @ContextConfiguration along with @RunWith annotation of JUnit to test a Service class in Spring Boot.
```java
@RunWith(SpringJUnit4ClassRunner.class)
@ContextConfiguration(classes=PaymentConfiguration.class)
public class PaymentServiceTests {

  @Autowired
  private PaymentService paymentService;

  @Test
  public void testPaymentService() {
      // code to test PaymentService class
  }
}
```
Here, `@ContextConfiguration` class instructs to load the Spring application context defined in the PaymentConfiguration class.

* **@ResponseBody**: The @ResponseBody annotation tells a controller that the object returned is automatically serialized into JSON and passed back into the HttpResponse object.
```java
@Controller
@RequestMapping("/post")
public class ExamplePostController {
 
    @Autowired
    ExampleService exampleService;
 
    @PostMapping("/response")
    @ResponseBody
    public ResponseTransfer postResponseController(
      @RequestBody LoginForm loginForm) {
        return new ResponseTransfer("Thanks For Posting!!!");
     }
}
```
Output
```
{"text":"Thanks For Posting!!!"}
```

* **@pathVariable**: @PathVariable is a Spring annotation which indicates that a method parameter should be bound to a URI template variable.
It has the following optional elements:

 * **name**: name of the path variable to bind to
 * **required**: tells whether the path variable is required
 * **value**: alias for name
```java
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class MyController {

    @RequestMapping(path="/{name}/{age}")
    public String getMessage(@PathVariable("name") String name, 
            @PathVariable("age") String age) {
        
        var msg = String.format("%s is %s years old", name, age);
        return msg;
    }
}
```
* **@ResponseEntity**: ResponseEntity represents an HTTP response, including headers, body, and status. While `@ResponseBody` puts the return value into the body of the response, ResponseEntity also allows us to add headers and status code.
```java
@GetMapping("/customHeader")
ResponseEntity<String> customHeader() {
    HttpHeaders headers = new HttpHeaders();
    headers.add("Custom-Header", "foo");
         
    return new ResponseEntity<>(
      "Custom header set", headers, HttpStatus.OK);
}
```
* **@Qualifier**: Spring Boot `@Qualifier` shows how to differentiate beans of the same type with @Qualifier. It can also be used to annotate other custom annotations that can then be used as qualifiers.
```java
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Component;

@Component
@Qualifier("manager")
public class Manager implements Person {

    @Override
    public String info() {
        return "Manager";
    }
}
```
