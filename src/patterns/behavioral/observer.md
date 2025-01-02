```mermaid
classDiagram: Observer Pattern
    class Subject {
        <<interface>>
        -observers: List
        +attach(observer)
        +detach(observer)
        +notify()
    }
    class Observer {
        <<interface>>
        +update(subject)
    }
    class ConcreteSubject {
        -state
        +getState()
        +setState(state)
    }
    class ConcreteObserver {
        -observerState
        +update(subject)
    }
    Subject <|-- ConcreteSubject
    Observer <|-- ConcreteObserver
    Subject ..> Observer
    ConcreteObserver ..> ConcreteSubject
```