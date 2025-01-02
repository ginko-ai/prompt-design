```mermaid
classDiagram: Singleton Pattern
    class Singleton {
        -instance: Singleton
        -Singleton()
        +getInstance() Singleton
        +businessLogic()
    }
    Singleton --> Singleton : has single instance

```