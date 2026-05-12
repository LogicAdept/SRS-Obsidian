<!--
reps: 0
priority: 0
-->
#Patterns/Architecture/UI #SRS

# What is the MVC pattern

**MVC (Model–View–Controller)** is a design pattern that splits an app into three parts: **Model**, **View**, and **Controller**. That gives **separation of concerns**: business logic and data are separate from presentation and from the code that ties user input to state changes. That makes maintenance, parallel work, and testing easier; other patterns build on MVC — [[What is the MVP pattern]], [[What is the MVVM pattern]], [[What is the MVW pattern]].

## The three parts

| Part           | Role                                                                                                                                                                                                                                         |
| -------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Model**      | App data and business logic: rules, validation, persistence. In the classic story it **does not depend on the UI**. When state changes, the model often **notifies** the view (and sometimes the controller) so the UI can refresh.       |
| **View**       | **Layout and presentation**: how data is shown to the user. It gets data to render (from the model or via the controller). In many stacks the view is **passive**: it does not talk to the model directly; it forwards input to the controller. |
| **Controller** | **Mediator** between model and view: handles input (clicks, forms), updates the model when needed, **routes** commands to the model and view. May hold input validation and data shaping.                                                  |

## Diagram: roles and links

```d2
direction: right

user: "User" {
  width: 240
  height: 130
  style.fill: "#eceff1"
}

view: "View" {
  width: 240
  height: 130
  style.fill: "#e3f2fd"
}

controller: "Controller" {
  width: 240
  height: 130
  style.fill: "#fff3e0"
}

model: "Model" {
  width: 240
  height: 130
  style.fill: "#e8f5e9"
}

user -> view
view -> controller: input
controller -> model: data
controller -> view: refresh
model -> view: notify
```

**Fig. 1.** Roles and main flows: input through View and Controller to Model; View updates from the controller and from model notifications.

The exact “who calls whom” layout depends on the framework: sometimes the view is updated **only** through the controller; sometimes the model is **observed** by the view.

## Diagram: typical interaction loop

Typical flow: the user acts through the View, the Controller interprets input and changes the Model, then the UI is brought in line with the new state.

```d2
direction:down

u: "1. User" {
  shape: person
  width: 160
  height: 200
  style.font-size: 24
}

v: "2. View\ncaptures input" {
  width: 280
  height: 100
  style.font-size: 24
  style.fill: "#e3f2fd"
}

c: "3. Controller\nhandles input" {
  width: 280
  height: 100
  style.font-size: 24
  style.fill: "#fff3e0"
}

m: "4. Model\nupdates" {
  width: 280
  height: 100
  style.font-size: 24
  style.fill: "#e8f5e9"
}

u -> v
v -> c
c -> m

refresh: "5. Controller refreshes View\nor Model notifies View" {
  width: 360
  height: 110
  style.font-size: 22
  style.fill: "#f3e5f5"
}

m -> refresh: state changed
c -> refresh: request redraw
```

**Fig. 2.** Chain from user action to Model update and View redraw.

## Domain examples

**Web:** the model often lives in a **DB** (MySQL, etc.) or client storage (IndexedDB); control in **HTML/JavaScript**; UI in **HTML/CSS**. MVC used to be mostly **server-side** (forms, links → new HTML); now logic and data are partly on the **client**, with partial page updates via Fetch and SPA-style flows.

**E-commerce:** Model — backend and data (products, cart, orders); View — catalog and cart pages; Controller — add to cart, checkout, payment while updating model and view.

**Everyday analogy:** Model — “kitchen,” recipes, stock; View — menu and plated dish; Controller — waiter between dining room and kitchen.

```d2
direction: down

customer: Customer {
  shape: person
  width: 160
  height: 200
  style.font-size: 26
}

kitchen: Model\nkitchen, recipes, stock {
  width: 300
  height: 130
  style.font-size: 26
  style.fill: "#e8f5e9"
}

plate: View\nmenu & presentation {
  width: 300
  height: 130
  style.font-size: 26
  style.fill: "#e3f2fd"
}

waiter: Controller\nwaiter {
  width: 300
  height: 130
  style.font-size: 26
  style.fill: "#fff3e0"
}

customer -> plate: reads menu
customer -> waiter: order
waiter -> kitchen: pass order
kitchen -> waiter: dish ready
waiter -> plate: serve
```

**Fig. 3.** Analogy: dining room and plating (View), waiter (Controller), kitchen (Model).

## Pros and cons

**Pros:** clear split of responsibilities; **parallel** work on UI vs logic; easier **unit tests** for logic without UI; scaling and reuse.

**Cons:** for tiny apps — **extra complexity**; you need upfront architecture thinking; higher bar than a single monolithic script.