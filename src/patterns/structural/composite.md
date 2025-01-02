```mermaid
classDiagram: Composite Pattern
    class Component {
        +operation()
        +add(component)
        +remove(component)
        +getChild(index)
    }
    class Leaf {
        +operation()
    }
    class Composite {
        -children: List
        +operation()
        +add(component)
        +remove(component)
        +getChild(index)
    }
    Component <|-- Leaf
    Component <|-- Composite
    Composite o-- Component
```