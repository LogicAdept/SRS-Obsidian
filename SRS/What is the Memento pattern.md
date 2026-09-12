<!--
reps: 0
priority: 0
-->
#Patterns/GoF/Behavioral #SRS

# What is the Memento pattern

> [!abstract] Short answer
> Memento is a behavioral pattern that saves and restores an object's previous state without exposing its implementation details. The originator produces opaque snapshots of itself; a caretaker stores them and hands them back when the state must roll back, never inspecting what is inside.

## How the pattern works

Undo needs state snapshots, and naive snapshots break encapsulation in both directions: either the caretaker reaches into private fields, or the snapshot class publishes every field just so the history can read and write it. Memento gives the job to the originator itself. Only the originator can read a memento's contents - typically through a narrow constructor or package-private access - while the caretaker treats snapshots as opaque tokens, pushing them onto a history stack and handing back the latest one when the user hits undo. The classic owner is a text editor whose snapshots carry text, caret, and scroll position.

```java
import java.util.ArrayDeque;
import java.util.Deque;

class EditorSnapshot {                  // memento: opaque to everyone but Editor
    private final String text;
    private final int caret;

    EditorSnapshot(String text, int caret) {
        this.text = text;
        this.caret = caret;
    }
}

class Editor {                          // originator
    private String text = "";
    private int caret = 0;

    EditorSnapshot save() {
        return new EditorSnapshot(text, caret);
    }

    void restore(EditorSnapshot snapshot) {
        // only the originator reads memento contents
    }
}

class History {                         // caretaker: stores tokens, never inspects them
    private final Deque<EditorSnapshot> undoStack = new ArrayDeque<>();
}
```

**Listing 1.** The memento's fields are private and the caretaker keeps only opaque tokens; producing and reading snapshots stays inside the originator.

```d2
direction: right
o: "Editor (originator)\nsave() / restore()" {
  width: 240
  height: 90
  style.fill: "#e3f2fd"
}
m: "EditorSnapshot\nopaque state" {
  width: 210
  height: 80
  style.fill: "#fff3e0"
}
c: "History (caretaker)\nstack of tokens" {
  width: 220
  height: 90
  style.fill: "#e8f5e9"
}
o -> m: creates
m -> c: stored as opaque
c -> o: returns for undo
```

**Fig. 1.** State flows from originator to caretaker and back, but only the originator can ever look inside a memento.

## Where mementos earn their cost

Snapshots are memory-hungry for large states, so real systems take them before meaningful operations only, or serialize them; caretakers may need to handle many mementos efficiently. Two relations decide most interview follow-ups. Command-based undo stores the operations and replays or reverses them, and the two combine: a command performs the change while a memento, taken just before execution, holds the state to fall back on. Prototype offers a lighter alternative - cloning the originator itself works when the state is simple and holds no external resources that are hard to re-establish. Both comparisons are drawn in [[How would you explain the Command design pattern]] and [[What is the Prototype pattern]], and the pattern belongs to the survey in [[What are examples of behavioral design patterns]].

> [!warning] Who can read the memento decides the pattern's value
> A memento with public getters and setters is just an exposed object - the encapsulation problem returns, and every editor refactor breaks the history code. The whole point is that only the originator accesses the snapshot's contents. Also do not promise "undo for free": each snapshot costs memory proportional to the state, so caretakers of large or long histories need explicit budgeting - claiming snapshots are always cheap is the standard trap.

> [!tip] Interview answer
> Memento implements undo without breaking encapsulation: the originator produces opaque snapshots of its own state, the caretaker stores them as tokens it cannot inspect, and restoration hands a snapshot back for the originator to read. A text editor's undo stack is the canonical use. It pairs with Command - commands perform, mementos capture state before they run - and for simple states, cloning via Prototype can replace it entirely.
