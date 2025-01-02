"""
@startuml
title classDiagram: Builder Pattern
    class Director {
        +construct()
    }
    class Builder {
        <<interface>>
        +buildPartA()
        +buildPartB()
        +getResult()
    }
    class ConcreteBuilder {
        -product: Product
        +buildPartA()
        +buildPartB()
        +getResult()
    }
    class Product {
        -parts: List
        +add(part)
        +show()
    }

    Director --> Builder
    ConcreteBuilder ..|> Builder
    ConcreteBuilder --> Product
@enduml
"""

"""
# Builder Pattern UML Documentation

## Class Relationships

### Director
```
@startuml
class Director {
    +construct()
    -builder: Builder
    +setBuilder(Builder)
}
@enduml
```
- Orchestrates object construction
- Works with builders through abstract interface
- Doesn't know concrete builder classes

### Builder Interface
```
@startuml
interface Builder {
    +buildPartA()
    +buildPartB()
    +getResult()
}
@enduml
```
- Declares interface for creating parts
- Each method represents construction step
- Returns final product via getResult()

### ConcreteBuilder
```
@startuml
class ConcreteBuilder {
    -product: Product
    +buildPartA()
    +buildPartB()
    +getResult()
}
@enduml
```
- Implements Builder interface
- Constructs and assembles parts
- Provides access to product

### Product
```
@startuml
class Product {
    -parts: List
    +add(part)
    +show()
}
@enduml
```

- Complex object being built
- Represents final result
- Independent of how it's assembled

## Key Relationships
@startuml
- Director → Builder: Composition
- ConcreteBuilder → Builder: Implementation
- ConcreteBuilder → Product: Creates
@enduml

## Sequence Flow
1. Client creates Director and Builder
2. Director is associated with Builder
3. Client requests construction
4. Director calls Builder methods
5. Client retrieves Product

"""


from abc import ABC, abstractmethod
from typing import Any

class Pizza:
    def __init__(self):
        self.parts = []

    def add(self, part: str) -> None:
        self.parts.append(part)

    def list_parts(self) -> str:
        return f"Pizza parts: {', '.join(self.parts)}"

class PizzaBuilder(ABC):
    @abstractmethod
    def reset(self) -> None:
        pass

    @abstractmethod
    def add_dough(self) -> None:
        pass

    @abstractmethod
    def add_sauce(self) -> None:
        pass

    @abstractmethod
    def add_toppings(self) -> None:
        pass

    @abstractmethod
    def get_result(self) -> Pizza:
        pass

class MargheritaBuilder(PizzaBuilder):
    def __init__(self):
        self.reset()

    def reset(self) -> None:
        self._pizza = Pizza()

    def add_dough(self) -> None:
        self._pizza.add("thin crust dough")

    def add_sauce(self) -> None:
        self._pizza.add("tomato sauce")

    def add_toppings(self) -> None:
        self._pizza.add("mozzarella")
        self._pizza.add("fresh basil")

    def get_result(self) -> Pizza:
        pizza = self._pizza
        self.reset()
        return pizza

class PizzaMaker:
    def __init__(self):
        self._builder = None

    @property
    def builder(self) -> PizzaBuilder:
        return self._builder

    @builder.setter
    def builder(self, builder: PizzaBuilder) -> None:
        self._builder = builder

    def make_pizza(self) -> None:
        self.builder.add_dough()
        self.builder.add_sauce()
        self.builder.add_toppings()

# Usage example
if __name__ == "__main__":
    maker = PizzaMaker()
    builder = MargheritaBuilder()
    maker.builder = builder

    maker.make_pizza()
    pizza = builder.get_result()
    print(pizza.list_parts())