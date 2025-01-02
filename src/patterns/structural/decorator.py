"""
@startuml
title classDiagram: Decorator Pattern
    class Component {
        <<interface>>
        +operation()
    }
    class ConcreteComponent {
        +operation()
    }
    class Decorator {
        <<abstract>>
        -component: Component
        +operation()
    }
    class ConcreteDecoratorA {
        -addedState
        +operation()
        +addedBehavior()
    }
    class ConcreteDecoratorB {
        +operation()
        +addedBehavior()
    }

    Component <|-- ConcreteComponent
    Component <|-- Decorator
    Decorator <|-- ConcreteDecoratorA
    Decorator <|-- ConcreteDecoratorB
    Decorator o-- Component
@enduml
"""

"""
@startuml
title Decorator Pattern

interface Component {
    +operation()
}

class ConcreteComponent {
    +operation()
}

abstract class Decorator {
    -component: Component
    +operation()
}

class ConcreteDecoratorA {
    -addedState
    +operation()
    +addedBehavior()
}

class ConcreteDecoratorB {
    +operation()
    +addedBehavior()
}

Component <|.. ConcreteComponent
Component <|.. Decorator
Decorator <|-- ConcreteDecoratorA
Decorator <|-- ConcreteDecoratorB
Decorator o-- Component : wraps

note right of Decorator
    Maintains a reference to a Component
    object and defines an interface that
    conforms to Component's interface
end note

note right of ConcreteDecoratorA
    Adds state or behavior to the
    component without affecting
    other objects
end note
@enduml
"""

from abc import ABC, abstractmethod
from typing import Optional

class TextComponent(ABC):
    """Base component interface"""
    @abstractmethod
    def render(self) -> str:
        pass

class PlainText(TextComponent):
    """Concrete component implementation"""
    def __init__(self, text: str):
        self._text = text

    def render(self) -> str:
        return self._text

class TextDecorator(TextComponent):
    """Base decorator class"""
    def __init__(self, component: TextComponent):
        self._component = component

    def render(self) -> str:
        return self._component.render()

class BoldDecorator(TextDecorator):
    """Adds bold formatting"""
    def render(self) -> str:
        return f"<b>{super().render()}</b>"

class ItalicDecorator(TextDecorator):
    """Adds italic formatting"""
    def render(self) -> str:
        return f"<i>{super().render()}</i>"

# Usage example
text = PlainText("Hello World")
bold_italic = BoldDecorator(ItalicDecorator(text))
print(bold_italic.render())  # Outputs: <b><i>Hello World</i></b>
