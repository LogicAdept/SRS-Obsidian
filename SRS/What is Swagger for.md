<!--
reps: 0
priority: 0
-->
#API/OpenAPI #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

Swagger is widely used for visualizing APIs, and with Swagger UI it provides online sandbox for frontend developers. 
Swagger is a tool, a specification and a complete framework implementation for producing the visual representation of RESTful Web Services. It enables documentation to be updated at the same pace as the server. When properly defined via Swagger, a consumer can understand and interact with the remote service with a minimal amount of implementation logic. 

**Create REST APIs** 
* Open `application.properties` and add below property. This will start the application in /swagger2-demo context path.
```
server.contextPath=/swagger2-demo
```
* Add one REST controller `Swagger2DemoRestController` which will provide basic REST based functionalities on Student entity.

**Swagger2DemoRestController.java**
```java
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import com.example.springbootswagger2.model.Student;
 
@RestController
public class Swagger2DemoRestController {
 
    List<Student> students = new ArrayList<Student>();
    {
        students.add(new Student("Sajal", "IV", "India"));
        students.add(new Student("Lokesh", "V", "India"));
        students.add(new Student("Kajal", "III", "USA"));
        students.add(new Student("Sukesh", "VI", "USA"));
    }
 
    @RequestMapping(value = "/getStudents")
    public List<Student> getStudents() {
        return students;
    }
 
    @RequestMapping(value = "/getStudent/{name}")
    public Student getStudent(@PathVariable(value = "name") String name) {
        return students.stream().filter(x -> x.getName().equalsIgnoreCase(name)).collect(Collectors.toList()).get(0);
    }
 
    @RequestMapping(value = "/getStudentByCountry/{country}")
    public List<Student> getStudentByCountry(@PathVariable(value = "country") String country) {
        System.out.println("Searching Student in country : " + country);
        List<Student> studentsByCountry = students.stream().filter(x -> x.getCountry().equalsIgnoreCase(country))
                .collect(Collectors.toList());
        System.out.println(studentsByCountry);
        return studentsByCountry;
    }
 
    @RequestMapping(value = "/getStudentByClass/{cls}")
    public List<Student> getStudentByClass(@PathVariable(value = "cls") String cls) {
        return students.stream().filter(x -> x.getCls().equalsIgnoreCase(cls)).collect(Collectors.toList());
    }
}
```

**Student.java**
```java
public class Student {
     
    private String name;
    private String cls;
    private String country;
 
    public Student(String name, String cls, String country) {
        super();
        this.name = name;
        this.cls = cls;
        this.country = country;
    }
 
    public String getName() {
        return name;
    }
 
    public String getCls() {
        return cls;
    }
 
    public String getCountry() {
        return country;
    }
 
    @Override
    public String toString() {
        return "Student [name=" + name + ", cls=" + cls + ", country=" + country + "]";
    }
}
```
* Start the application as Spring boot application. Test couple of REST Endpoints to check if they are working fine:
```
http://localhost:8080/swagger2-demo/getStudents
http://localhost:8080/swagger2-demo/getStudent/sajal
http://localhost:8080/swagger2-demo/getStudentByCountry/india
http://localhost:8080/swagger2-demo/getStudentByClass/v
```
**Swagger2 Configuration**
* **Add Swagger2 Maven Dependencies**: Open pom.xml file of the spring-boot-swagger2 project and add below two swagger related dependencies i.e. springfox-swagger2 and springfox-swagger-ui.
```xml
<dependency>
    <groupId>io.springfox</groupId>
    <artifactId>springfox-swagger2</artifactId>
    <version>2.6.1</version>
</dependency>

<dependency>
    <groupId>io.springfox</groupId>
    <artifactId>springfox-swagger-ui</artifactId>
    <version>2.6.1</version>
</dependency>
```
* **Add Swagger2 Configuration**: Add the below configuration in the code base. To help you understand the configuration, I have added inline comments.
```java
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.ResourceHandlerRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurerAdapter;
import com.google.common.base.Predicates;
import springfox.documentation.builders.RequestHandlerSelectors;
import springfox.documentation.spi.DocumentationType;
import springfox.documentation.spring.web.plugins.Docket;
import springfox.documentation.swagger2.annotations.EnableSwagger2;
 
@Configuration
@EnableSwagger2
public class Swagger2UiConfiguration extends WebMvcConfigurerAdapter
{
    @Bean
    public Docket api() {
        // @formatter:off
        //Register the controllers to swagger
        //Also it is configuring the Swagger Docket
        return new Docket(DocumentationType.SWAGGER_2).select()
                // .apis(RequestHandlerSelectors.any())
                .apis(Predicates.not(RequestHandlerSelectors.basePackage("org.springframework.boot")))
                // .paths(PathSelectors.any())
                // .paths(PathSelectors.ant("/swagger2-demo"))
                .build();
        // @formatter:on
    }
 
    @Override
    public void addResourceHandlers(ResourceHandlerRegistry registry)
    {
        //enabling swagger-ui part for visual documentation
        registry.addResourceHandler("swagger-ui.html").addResourceLocations("classpath:/META-INF/resources/");
        registry.addResourceHandler("/webjars/**").addResourceLocations("classpath:/META-INF/resources/webjars/");
    }
}
```
* **Verify Swagger2 UI Docs**
```
 http://localhost:8080/swagger2-demo/swagger-ui.html
```
![alt text](https://github.com/learning-zone/spring-interview-questions/blob/spring/assets/Swagger2-UI-Docs-without-Annotations.png)

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**OpenAPI / Swagger — для чего?**

Спецификация REST API в формате YAML/JSON. Описывает endpoints, методы, параметры, тела запросов/ответов, коды ответов. Swagger UI — интерактивная документация (можно отправлять запросы). API-First: сначала пишем спецификацию, потом код. Для AQA: из OpenAPI можно автогенерировать тесты и модели.
