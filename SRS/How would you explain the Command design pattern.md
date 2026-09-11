<!--
reps: 0
priority: 0
-->
#Patterns/GoF/Behavioral #SRS

# How would you explain the Command design pattern

> [!abstract] Short answer
> Command turns a request into a **stand-alone object** holding everything needed to execute it — the receiver and the arguments. That object can be passed around, queued, scheduled, logged, and undone, because the caller now holds the request itself, not a method call.

## The mechanism

A command interface declares a single execution method, usually parameterless — all request details live as fields of the concrete command, initialized in its constructor, which makes commands effectively immutable value objects. The receiver is the object with the real business logic; the concrete command just forwards to it, and the client wires receiver plus arguments into the command at construction time. The sender — the invoker, a button, a scheduler, a message handler — keeps a reference to the command interface and triggers `execute` without knowing what will happen or to whom. This is how one GUI action, one menu entry, and one keyboard shortcut bind to the same command object with zero duplication, and how a queue can hold operations for later.

```java
interface Command { boolean execute(); }

class CutCommand implements Command {
    private final Editor editor;                 // receiver
    private String backup;
    CutCommand(Editor editor) { this.editor = editor; }
    public boolean execute() {
        backup = editor.getSelection();
        editor.deleteSelection();
        return true;                             // state changed
    }
}
```

**Listing 1.** A concrete command: pre-configured with its receiver, executed later by an invoker that only knows the interface; the boolean drives whether it enters the undo history.

## What the object-ness buys

Once the request is an object, the classic applications follow: parameterize UI elements with operations; queue or serialize commands for deferred and remote execution; keep a history stack for undo — executed state-changing commands store a backup of the receiver's state, and undo pops the stack and restores it, with Memento as the partner pattern when the state is too private to copy naively. The cost the catalog names is a new layer between senders and receivers, which is overkill for requests used once — the case [[What is a lightweight alternative to the Command pattern]] covers.

> [!warning] Command versus Strategy is intent, not shape
> Both parameterize an object with something behind an interface, and mixing them up is a standard follow-up trap: Command converts any operation into an object so it can be deferred, queued, or undone; Strategy supplies different ways of doing the same thing inside one context. See [[What is the Strategy pattern used for]] for that side.

> [!tip] Interview answer
> Command encapsulates a request as an object: an interface with one execute method, concrete commands holding receiver and arguments as fields, and invokers that call execute without knowing the details. It buys parameterized UI, queuing, scheduling, logging, and undo through a command history — at the price of an extra layer that trivial one-shot calls do not need.
