<!--
reps: 0
priority: 0
-->
#Patterns/GoF/Behavioral #SRS

# What is the Mediator pattern

> [!abstract] Short answer
> Mediator is a behavioral pattern that reduces chaotic dependencies between objects: colleagues stop communicating directly and collaborate only through a mediator object, which receives their notifications and redirects or coordinates the responses.

## How the pattern works

The problem shape: a set of objects - form controls, subsystem modules - whose interactions multiply. A checkbox reveals a text field, the submit button validates every field, each element knows a dozen others; the classes become impossible to reuse outside that exact tangle. The pattern cuts the direct links: every colleague holds one dependency - the mediator - and instead of acting on other elements, it notifies the mediator about events. The mediator, often a class that already knows all the elements (a dialog, for instance), implements the coordination: it decides who reacts to whom.

```java
import java.util.ArrayList;
import java.util.List;

interface Mediator {
    void notify(Component sender, String event);
}

abstract class Component {
    final Mediator mediator;

    Component(Mediator mediator) {
        this.mediator = mediator;
    }
}

class Button extends Component {
    Button(Mediator mediator) {
        super(mediator);
    }

    void click() {
        mediator.notify(this, "click");   // no references to other components
    }
}

class ProfileDialog implements Mediator {
    final List<Component> components = new ArrayList<>();
    boolean dogSelected = false;
    TextField dogNameField;

    @Override
    public void notify(Component sender, String event) {
        if (event.equals("toggle")) {
            dogSelected = !dogSelected;
            dogNameField.setVisible(dogSelected);   // coordination lives here
        }
    }
}
```

**Listing 1.** The button knows only its mediator; the visibility rule that used to bind checkbox to text field now lives in the dialog.

```d2
direction: right
direct: "Without mediator\nN x (N - 1) direct links" {
  width: 250
  height: 80
  style.fill: "#ffebee"
}
via: "With mediator\neach colleague -> 1 mediator" {
  width: 260
  height: 80
  style.fill: "#e8f5e9"
}
m: "Mediator\ndialog" {
  width: 170
  height: 70
  style.fill: "#fff3e0"
}
c1: "Checkbox" {
  width: 130
  height: 60
  style.fill: "#e3f2fd"
}
c2: "Button" {
  width: 120
  height: 60
  style.fill: "#e3f2fd"
}
c3: "TextField" {
  width: 140
  height: 60
  style.fill: "#e3f2fd"
}
via -> m
m -> c1
m -> c2
m -> c3
```

**Fig. 1.** The dependency count drops from a mesh to a star; colleagues become reusable because they reference nothing but the mediator interface.

## Mediator among the connector patterns

Chain of Responsibility, Command, Mediator, and Observer are the four standard answers to connecting senders and receivers: the chain tries receivers sequentially, command wires a one-way sender-to-receiver link, mediator eliminates direct connections in favor of a hub, and observer lets receivers subscribe and unsubscribe dynamically - the event-broadcast flavor is what [[How does ApplicationContext publish events]] implements at the framework level. Mediator and facade have similar jobs - organizing collaboration among tightly coupled classes - but a facade just simplifies access to a subsystem whose objects still talk to each other, while mediator components genuinely communicate through the hub; the split is drawn in [[What is the Facade pattern]]. At the responsibility level, inserting the hub is an application of [[What is the Indirection principle in GRASP]], and the observer alternative is compared in [[What is Observer]].

> [!warning] The mediator can become a god object
> Because every coordination rule lands in one class, the mediator tends to accumulate the complexity the colleagues dropped - a dialog that validates, routes, and decides everything is a god object in the making, and a large mediator is as hard to maintain as the mesh it replaced. Also name the trade-off precisely: loose coupling between colleagues is bought with tight coupling to the mediator interface, and changing broadcast semantics is Observer's job, not Mediator's.

> [!tip] Interview answer
> Mediator forces objects that would tangle each other with direct references to collaborate only through one mediator object: colleagues notify it about events, it coordinates the reactions. A dialog class mediating its form controls is the textbook case. Compared to Observer it is a hub, not a broadcast; compared to Facade it sits in the communication path, not in front of it. The known risk is the mediator itself becoming a god object.
