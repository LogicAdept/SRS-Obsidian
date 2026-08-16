<!--
reps: 0
priority: 0
-->
#Caching #SystemDesign/Performance #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

Caching is a mechanism to enhance the performance of a system. It is a temporary memory that lies between the application and the persistent database. Cache memory stores recently used data items in order to reduce the number of database hits as much as possible.

**Types of cache**
* **In-memory caching**: This is the most frequently used area where caching is used extensively to increase performance of the application. In-memory caches such as `Memcached` and `Radis` are key-value stores between your application and your data storage. Since the data is held in RAM, it is much faster than typical databases where data is stored on disk.
* **Database caching**: Database usually includes some level of caching in a default configuration, optimized for a generic use case. Tweaking these settings for specific usage patterns can further boost performance. One popular in this area is first level cache of `Hibernate` or any `ORM frameworks`.
* **Web server caching**: Reverse proxies and caches such as Varnish can serve static and dynamic content directly. Web servers can also cache requests, returning responses without having to contact application servers. In today’s API age, this option is a viable if we want to cache API responses in web server level.
* **CDN caching**: Caches can be located on the client side (OS or browser), server side, or in a distinct cache layer.

**Spring Boot Cache Annotations**
* **@EnableCaching**: It can be added to the boot application class annotated with `@SpringBootApplication`. Spring provides one concurrent hashmap as default cache, but we can override CacheManager to register external cache providers as well easily.
* **@Cacheable**: It is used on the method level to let spring know that the response of the method are cacheable. Spring manages the request/response of this method to the cache specified in annotation attribute. 
```java
@Cacheable(value="books", key="#isbn")
public Book findStoryBook(ISBN isbn, boolean checkWarehouse, boolean includeUsed)
```
* **@CachePut**: It allow us to update the cache and will also allow the method to be executed. It supports the same options as `@Cacheable` and should be used for cache population rather then method flow optimization.
* **@CacheEvict**: It is used when we need to evict (remove) the cache previously loaded of master data. When CacheEvict annotated methods will be executed, it will clear the cache.
* **@Caching**: This annotation is required when we need both `@CachePut` and `@CacheEvict` at the same time.

**Spring Boot Caching Example** 
* **Create HTTP GET REST API**

**Student.java**
```java
public class Student {
 
    String id;
    String name;
    String clz;
 
    public Student(String id, String name, String clz) {
        super();
        this.id = id;
        this.name = name;
        this.clz = clz;
    } 
    //Setters and getters
}
```

**StudentService.java**
```java 
import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;
import com.example.springcache.domain.Student;
 
@Service
public class StudentService {

    @Cacheable("student")
    public Student getStudentByID(String id) {

        try {
            System.out.println("Going to sleep for 5 Secs.. to simulate backend call.");
            Thread.sleep(1000*5);
        }
        catch (InterruptedException e) {
            e.printStackTrace();
        }
        return new Student(id, "Pradeep", "V");
    }
}
```

**StudentController.java**
```java
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;
import com.example.springcache.domain.Student;
import com.example.springcache.service.StudentService;
 
@RestController
public class StudentController {
 
    @Autowired
    StudentService studentService;
 
    @GetMapping("/student/{id}")
    public Student findStudentById(@PathVariable String id) {

        System.out.println("Searching by ID  : " + id);
        return studentService.getStudentByID(id);
    }
}
```
Enable Spring managed Caching

**SpringCacheApplication.java**
```java
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cache.annotation.EnableCaching;
 
@SpringBootApplication
@EnableCaching
public class SpringCacheApplication {
 
    public static void main(String[] args) {
        SpringApplication.run(SpringCacheApplication.class, args);
    }
}
```
Output
```
Searching by ID  : 1
Going to sleep for 5 Secs.. to simulate backend call.
 
Searching by ID  : 1
Searching by ID  : 1
Searching by ID  : 1
Searching by ID  : 1
Searching by ID  : 1
 
Searching by ID  : 2
Going to sleep for 5 Secs.. to simulate backend call.
 
Searching by ID  : 2
Searching by ID  : 2
```
