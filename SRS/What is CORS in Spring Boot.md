<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #Java/Spring/Framework/WebMvc #Java/Annotations #Java/Spring/Boot #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

Cross-Origin Resource Sharing (CORS) is a security concept that allows restricting the resources implemented in web browsers. It prevents the JavaScript code producing or consuming the requests against different origin.

* **Enable CORS in Controller Method**
```java
@RequestMapping(value = "/products")
@CrossOrigin(origins = "http://localhost:8080")
public ResponseEntity<Object> getProduct() {
   return null;
}
```
* **Global CORS Configuration**
We need to define the shown `@Bean` configuration to set the CORS configuration support globally to your Spring Boot application.
```java
@Bean
public WebMvcConfigurer corsConfigurer() {
   return new WebMvcConfigurerAdapter() {
      @Override
      public void addCorsMappings(CorsRegistry registry) {
         registry.addMapping("/products").allowedOrigins("http://localhost:9000");
      }    
   };
}
```
To code to set the CORS configuration globally in main Spring Boot application is given below.
```java
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurerAdapter;

@SpringBootApplication
public class DemoApplication {
   public static void main(String[] args) {
      SpringApplication.run(DemoApplication.class, args);
   }
   @Bean
   public WebMvcConfigurer corsConfigurer() {
      return new WebMvcConfigurerAdapter() {
         @Override
         public void addCorsMappings(CorsRegistry registry) {
            registry.addMapping("/products").allowedOrigins("http://localhost:8080");
         }
      };
   }
}
```

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**CORS — что это и когда возникает?**

Cross-Origin Resource Sharing: браузер блокирует запросы к другому домену. Сервер разрешает через заголовки: Access-Control-Allow-Origin, Access-Control-Allow-Methods. Preflight запрос (OPTIONS) перед POST/PUT. Для AQA: CORS не мешает Rest Assured (нет браузера), но может мешать Postman в браузерной версии.

**Where to configure CORS?**

Browser same-origin policy. Configure in SecurityFilterChain (CorsConfigurationSource) so preflight OPTIONS is handled before CSRF/auth. @CrossOrigin on a controller is easy to miss globally.
