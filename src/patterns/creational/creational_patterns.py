"""
# Creational Design Patterns Documentation

## Singleton Pattern
```plantuml
@startuml
class Singleton {
    - static instance: Singleton
    - constructor()
    + static getInstance(): Singleton
}
@enduml


**Purpose**: Ensures a class has only one instance and provides a global point of access to it.
- Use when exactly one instance of a class is needed
- Provides controlled access to the sole instance

## Factory Method Pattern
```plantuml
@startuml
interface Product
class ConcreteProduct
class Creator {
    + factoryMethod()
    + operation()
}
class ConcreteCreator

Product <|.. ConcreteProduct
Creator <|-- ConcreteCreator
ConcreteCreator ..> ConcreteProduct
@enduml
```

**Purpose**: Defines an interface for creating objects but lets subclasses decide which class to instantiate.
- Useful when a class can't anticipate the type of objects it needs to create
- Delegates object creation to subclasses

## Builder Pattern
```plantuml
@startuml
class Director {
    + construct()
}
class Builder {
    + buildPartA()
    + buildPartB()
    + getResult()
}
class ConcreteBuilder
class Product

Director o-- Builder
Builder <|-- ConcreteBuilder
ConcreteBuilder ..> Product
@enduml
```

**Purpose**: Separates the construction of a complex object from its representation.
- Used when the algorithm for creating a complex object should be independent of the parts that make up the object and how they're assembled
- Allows fine control over the construction process

## Abstract Factory Pattern
```plantuml
@startuml
interface AbstractFactory {
    + createProductA()
    + createProductB()
}
interface AbstractProductA
interface AbstractProductB
class ConcreteFactory1
class ConcreteProductA1
class ConcreteProductB1

AbstractFactory <|.. ConcreteFactory1
AbstractProductA <|.. ConcreteProductA1
AbstractProductB <|.. ConcreteProductB1
ConcreteFactory1 ..> ConcreteProductA1
ConcreteFactory1 ..> ConcreteProductB1
@enduml
```

**Purpose**: Provides an interface for creating families of related or dependent objects without specifying their concrete classes.
- Useful when a system should be independent of how its products are created, composed, and represented
- Enforces consistency among products

## Prototype Pattern
```plantuml
@startuml
interface Prototype {
    + clone()
}
class ConcretePrototype1
class ConcretePrototype2

Prototype <|.. ConcretePrototype1
Prototype <|.. ConcretePrototype2
@enduml
```

**Purpose**: Creates new objects by cloning an existing object, known as the prototype.
- Useful when the cost of creating an object is more expensive than copying an existing one
- Reduces subclassing by hiding the complexity of object creation
"""

from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Any

# Singleton Pattern
class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.connection_string = "mongodb://localhost:27017"
        return cls._instance

# Factory Method Pattern
class Document(ABC):
    @abstractmethod
    def create(self) -> None:
        pass

class PDFDocument(Document):
    def create(self) -> str:
        return "Creating PDF document"

class WordDocument(Document):
    def create(self) -> str:
        return "Creating Word document"

class DocumentFactory:
    def create_document(self, doc_type: str) -> Document:
        if doc_type == "pdf":
            return PDFDocument()
        elif doc_type == "word":
            return WordDocument()
        raise ValueError(f"Unknown document type: {doc_type}")

# Builder Pattern
class Computer:
    def __init__(self):
        self.parts = []

    def add(self, part: str) -> None:
        self.parts.append(part)

    def list_parts(self) -> str:
        return f"Computer parts: {', '.join(self.parts)}"

class ComputerBuilder:
    def __init__(self):
        self.computer = Computer()

    def add_cpu(self) -> None:
        self.computer.add("CPU")

    def add_memory(self) -> None:
        self.computer.add("Memory")

    def add_storage(self) -> None:
        self.computer.add("Storage")

    def get_result(self) -> Computer:
        return self.computer

# Prototype Pattern
class Prototype:
    def clone(self):
        return deepcopy(self)

class DocumentTemplate(Prototype):
    def __init__(self, content: str):
        self.content = content

    def modify_content(self, new_content: str) -> None:
        self.content = new_content

# Usage examples
def main():
    # Singleton
    db1 = DatabaseConnection()
    db2 = DatabaseConnection()
    assert db1 is db2  # Same instance

    # Factory Method
    factory = DocumentFactory()
    pdf = factory.create_document("pdf")
    word = factory.create_document("word")

    # Builder
    builder = ComputerBuilder()
    builder.add_cpu()
    builder.add_memory()
    builder.add_storage()
    computer = builder.get_result()

    # Prototype
    template = DocumentTemplate("Original Content")
    clone = template.clone()
    clone.modify_content("Modified Content")

    print(f"Original template: {template.content}")
    print(f"Modified clone: {clone.content}")

if __name__ == "__main__":
    main()