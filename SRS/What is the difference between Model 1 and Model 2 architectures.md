<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #Patterns/Architecture/UI/MVC #SRS

# What is the difference between Model 1 and Model 2 architectures?

> [!abstract] Short answer
> **Model 1** mixes **presentation and business logic** in the page that handles the request (classic JSP/servlet that both computes and renders). **Model 2** is **MVC on the web**: a **controller** interprets HTTP GET/POST, talks to the **model**, and **selects the view**; the view **only renders**. Spring MVC is Model 2 with a **front controller** (`DispatcherServlet`) so one servlet owns dispatch and `@Controller` methods are handlers, not per-URL servlets.

## Mix vs separate controller

Java EE’s JSP chapter: MVC splits **model** (data and operations), **view** (how that data is shown), and **controller** (dispatch, map input to model actions, choose the next view). **In a web app that MVC is often called Model-2.** The earlier bookstore that **intermixes presentation and business logic** is **Model-1**. Model-2 is the **recommended** web design.

Jakarta’s JSP guide still warns against embedding business logic in the page. A Model 2 controller may be **one servlet per flow** (Java EE “Dispatcher” mapping URLs to JSPs) or Spring’s **single** `DispatcherServlet` plus many handler methods.

```d2
direction: down
m1: "Model 1\nJSP/servlet does logic + HTML" {
  width: 300
  height: 50
  style.fill: "#fff3e0"
}
m2: "Model 2 / MVC\ncontroller → model → view" {
  width: 300
  height: 50
  style.fill: "#e8f5e9"
}
fc: "Spring: DispatcherServlet\nfront controller" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}

m1 -> m2: "separate C from V"
m2 -> fc: "one servlet algorithm"
```

**Fig. 1.** Model 1 is the mixed page. Model 2 is MVC. Spring’s front controller is how Model 2 is wired: [[What is the Front Controller pattern in Spring MVC]], [[What is Spring MVC DispatcherServlet]]. View rendering: [[What is a ViewResolver in Spring MVC]].

```java
@Controller
public class CatalogController {
    @GetMapping("/books")
    public String list(Model model) {
        model.addAttribute("books", catalog.findAll());
        return "bookcatalog";   // view name — not business logic in the JSP
    }
}
```

**Listing 1.** Conceptual Model 2 in Spring: the method is the controller action; the template only formats `books`. Stereotype: [[How do you create a Spring MVC controller]].

> [!warning] Model 1 is not a Spring term
> Interviewers mean **JSP-centric** apps. Spring MVC does not have a `@Model1` switch. If your `@Controller` still computes HTML strings, you have slipped back toward Model 1.

> [!warning] Many servlets can still be Model 2
> Separate controller + JSP is Model 2 even **without** `DispatcherServlet`. Front controller is a **way** to implement Model 2, not a third official “Model 3”.

> [!warning] `@RestController` still has a model
> JSON APIs skip HTML views but still separate **handler** (controller) from **payload** (model). That is Model 2 without `ViewResolver`.

> [!tip] Interview answer
> **Model 1:** the JSP or servlet both decides and draws. **Model 2:** MVC — controller chooses the view after talking to the model. Spring MVC is Model 2 plus **`DispatcherServlet`** as the front controller.
