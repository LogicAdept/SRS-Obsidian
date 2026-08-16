<!--
reps: 0
priority: 0
-->
#Java/Servlet #Java/Spring/Framework/WebMvc #Java/Listeners #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

Interceptor can be used to perform operations in the following situations − 
* Before sending the request to the controller
* Before sending the response to the client

For example, interceptor can be used to add the request header before sending the request to the controller and add the response header before sending the response to the client. 

Interceptors support three methods − 

* **preHandle()** − This is used to perform operations before sending the request to the controller. This method should return true to return the response to the client.
* **postHandle()** − This is used to perform operations before sending the response to the client.
* **afterCompletion()** − This is used to perform operations after completing the request and response.

```java
@Component
public class ProductServiceInterceptor implements HandlerInterceptor {
   @Override
   public boolean preHandle(
      HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
      
       log.info("[preHandle][" + request + "]" + "[" + request.getMethod()
      + "]" + request.getRequestURI() + getParameters(request));
      return true;
   }
   @Override
   public void postHandle(
      HttpServletRequest request, HttpServletResponse response, Object handler, 
      ModelAndView modelAndView) throws Exception {
          log.info("[postHandle][" + request + "]");
      }
   
   @Override
   public void afterCompletion(HttpServletRequest request, HttpServletResponse response, 
      Object handler, Exception ex) throws Exception {
           if (ex != null) {
              ex.printStackTrace();
           }
           log.info("[afterCompletion][" + request + "][exception: " + ex + "]");
      }
}
```

**В чем разница между Filters, Listeners and Interceptors?**

Концептуально всё просто, фильтры сервлетов могут перехватывать только HTTPServlets. Listeners могут перехватывать специфические события. Как перехватить события которые относятся ни к тем не другим?

Фильтры и перехватчики делают по сути одно и тоже: они перехватывают какое-то событие, и делают что-то до или после.
Java EE использует термин Filter, Spring называет их Interceptors. Именно здесь AOP используется в полную силу,
благодаря чему возможно перехватывание вызовов любых объектов.

**Where does Spring Security sit vs interceptors?**

Security is a servlet Filter chain before DispatcherServlet. Interceptors run after the servlet mapped a handler. Listeners are servlet lifecycle (context/session/request), not per-controller AOP.
