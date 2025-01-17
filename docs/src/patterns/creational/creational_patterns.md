```mermaid
---
title: Creational Patterns
---
classDiagram
    class CreationalPatterns{
        +Factory Method
        +Abstract Factory
        +Builder
        +Prototype
        +Singleton
    }

    class FactoryMethod{
        +createProduct()
        #Product
    }

    class AbstractFactory{
        +createProductA()
        +createProductB()
        #ProductA
        #ProductB
    }

    class Builder{
        +buildPartA()
        +buildPartB()
        +getResult()
    }

    class Prototype{
        +clone()
        -prototype
    }

    class Singleton{
        -instance
        +getInstance()
    }

    CreationalPatterns --> FactoryMethod
    CreationalPatterns --> AbstractFactory
    CreationalPatterns --> Builder
    CreationalPatterns --> Prototype
    CreationalPatterns --> Singleton
