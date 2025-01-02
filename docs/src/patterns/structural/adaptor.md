```mermaid
---
title: Adaptor Pattern
---
classDiagram
    class Client {
        +method()
    }
    class Target {
        <<interface>>
        +request()
    }
    class Adapter {
        -adaptee
        +request()
    }
    class Adaptee {
        +specificRequest()
    }

    Client --> Target
    Target <|.. Adapter
    Adapter --> Adaptee
```
