```mermaid
classDiagram: Design Pattern Categories
    class DesignPatterns {
        +Structural
        +Creational
        +Behavioral
        +Concurrency
    }

    class Structural {
        +Adapter
        +Bridge
        +Composite
        +Decorator
        +Facade
        +Proxy
        +Marker
    }

    class Creational {
        +AbstractFactory
        +Builder
        +FactoryMethod
        +Singleton
    }

    class Behavioral {
        +Command
        +Interpreter
        +Iterator
        +Mediator
        +Memento
        +Observer
        +Strategy
        +Specification
    }

    class Concurrency {
        +ActiveObject
        +Balking
        +EventBasedAsync
        +GuardedSuspension
        +Lock
        +MonitorObject
    }

    DesignPatterns --> Structural
    DesignPatterns --> Creational
    DesignPatterns --> Behavioral
    DesignPatterns --> Concurrency
```