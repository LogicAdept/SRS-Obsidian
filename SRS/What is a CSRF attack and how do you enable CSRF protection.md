<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/CSRF #Security/AppSec #SRS #New

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**CSRF**: CSRF stands for Cross-Site Request Forgery. It is an attack that forces an end user to execute unwanted actions on a web application in which they are currently authenticated. CSRF attacks specifically target state-changing requests, not theft of data, since the attacker has no way to see the response to the forged request.

In order to use the Spring Security CSRF protection, we'll first need to make sure we use the proper HTTP methods for anything that modifies state (PATCH, POST, PUT, and DELETE – not GET).

**1. Java Configuration** 
CSRF protection is **enabled by default** in the Java configuration. We can still disable it if we need to:
```java
@Override
protected void configure(HttpSecurity http) throws Exception {
    http
      .csrf().disable();
}
```
**2. XML Configuration** 
Starting from Spring Security 4.x – the CSRF protection is enabled by default in the XML configuration as well; we can of course still disable it if we need to:
```xml
<http>
    ...
    <csrf disabled="true"/>
</http>
```
**3. Extra Form Parameters** 
With CSRF protection enabled on the server side, we'll need to include the CSRF token in our requests on the client side as well:
```html
<input type="hidden" name="${_csrf.parameterName}" value="${_csrf.token}"/>
```
**4. Using JSON** 
We can't submit the CSRF token as a parameter if we're using JSON; instead we can submit the token within the header.
We'll first need to include the token in our page – and for that we can use meta tags:
```html
<meta name="_csrf" content="${_csrf.token}"/>
<meta name="_csrf_header" content="${_csrf.headerName}"/>
```
Then we'll construct the header:
```javascript
var token = $("meta[name='_csrf']").attr("content");
var header = $("meta[name='_csrf_header']").attr("content");
 
$(document).ajaxSend(function(e, xhr, options) {
    xhr.setRequestHeader(header, token);
});
```

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**CSRF — что это и как проверить?**

Cross-Site Request Forgery: злоумышленник заставляет браузер отправить запрос от имени авторизованного пользователя. Пример: скрытая форма на вредоносном сайте делает POST /transfer. Защита: CSRF-токен в форме/заголовке, SameSite cookie. Для AQA: попробовать запрос без CSRF-токена → должен быть 403.

**When is CSRF required in Boot 3?**

Cookie-session browser apps: keep CSRF. Bearer JWT APIs: usually disable. Unexpected 403 POST after upgrade: CSRF still enabled.
