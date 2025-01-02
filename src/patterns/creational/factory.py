"""
@startuml
title classDiagram: Factory
    class Creator {
        <<abstract>>
        +factoryMethod()
        +someOperation()
    }
    class ConcreteCreator {
        +factoryMethod()
    }
    class Product {
        <<interface>>
        +doStuff()
    }
    class ConcreteProduct {
        +doStuff()
    }

    Creator <|-- ConcreteCreator
    Product <|.. ConcreteProduct
    ConcreteCreator ..> ConcreteProduct
@enduml
"""

"""
```plantuml
@startuml
title Factory Method Pattern

interface Product {
    +operation()
}

abstract class Creator {
    {abstract} +factoryMethod(): Product
    +someOperation()
}

class ConcreteCreator {
    +factoryMethod(): Product
}

class ConcreteProduct {
    +operation()
}

Creator <|-- ConcreteCreator
Product <|.. ConcreteProduct
ConcreteCreator ..> ConcreteProduct : creates

note right of Creator
  someOperation() {
    product = factoryMethod()
    product.operation()
  }
end note
@enduml
```

Key components:
1. Product: Defines the interface for objects created by factory
2. ConcreteProduct: Implements the Product interface
3. Creator: Declares factory method returning Product objects
4. ConcreteCreator: Overrides factory method to return ConcreteProduct

Benefits:
- Single Responsibility Principle: Moves product creation code into one place
- Open/Closed Principle: Introduces new types of products without breaking code
- Loose coupling between concrete products and creator code
"""

from abc import ABC, abstractmethod

class LogisticsTransport(ABC):
    @abstractmethod
    def deliver(self) -> str:
        pass

class Truck(LogisticsTransport):
    def deliver(self) -> str:
        return "Delivering by land in a truck"

class Ship(LogisticsTransport):
    def deliver(self) -> str:
        return "Delivering by sea in a ship"

class Logistics(ABC):
    @abstractmethod
    def create_transport(self) -> LogisticsTransport:
        pass

    def plan_delivery(self) -> str:
        transport = self.create_transport()
        return f"Logistics: Planning delivery... {transport.deliver()}"

class RoadLogistics(Logistics):
    def create_transport(self) -> LogisticsTransport:
        return Truck()

class SeaLogistics(Logistics):
    def create_transport(self) -> LogisticsTransport:
        return Ship()

# Client code
def client_code(logistics: Logistics) -> None:
    print(logistics.plan_delivery())

# Usage
road_logistics = RoadLogistics()
sea_logistics = SeaLogistics()

client_code(road_logistics)  # Output: Logistics: Planning delivery... Delivering by land in a truck
client_code(sea_logistics)   # Output: Logistics: Planning delivery... Delivering by sea in a ship