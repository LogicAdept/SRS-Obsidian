<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot #Java/Spring/Framework/WebMvc #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

Spring Boot provides a number of options for error/exception handling. 
**1. @ExceptionHandler Annotation**: This annotation works at the `@Controller` class level. The issue with the approach is only active for the given controller. The annotation is not global, so we need to implement in each and every controller.
```java
@RestController
public class WelcomeController {

    @GetMapping("/greeting")
    String greeting() throws Exception {
      //
    }

    @ExceptionHandler({Exception.class})
    public  handleException(){
       //
    }
}
```
**2. @ControllerAdvice Annotation**: This annotation supports global Exception handler mechanism. So we can implement the controller exception handling events in a central location.
```java
@ControllerAdvice
public class GlobalRestExceptionHandler extends ResponseEntityExceptionHandler {

    @ResponseStatus(HttpStatus.BAD_REQUEST)
    @ExceptionHandler(Exception.class)
    public void defaultExceptionHandler() {
        // Nothing to do
    }
}
```
**3. @ResponseEntityExceptionHandler**: This method can be used with `@ControllerAdvice` classes. It allows the developer to specify some specific templates of ResponseEntity and return values.

**4. @RestControllerAdvice**: Spring Boot 1.4 introduced the `@RestControllerAdvice` annotation for easier exception handling. It is a convenience annotation that is itself annotated with `@ControllerAdvice` and `@ResponseBody`.
```java
@RestControllerAdvice
public class RestExceptionHandler {

@ExceptionHandler(CustomNotFoundException.class)
public ApiErrorResponse handleNotFoundException(CustomNotFoundException ex) {

ApiErrorResponse response = new ApiErrorResponse.ApiErrorResponseBuilder()
      .withStatus(HttpStatus.NOT_FOUND)
      .withError_code("NOT_FOUND")
      .withMessage(ex.getLocalizedMessage()).build();

    return responseMsg;
    }
}
```

**Global API errors in Boot 3?**

@RestControllerAdvice + @ExceptionHandler, return ProblemDetail. @ExceptionHandler on one @Controller is local only. Validation: MethodArgumentNotValidException.
