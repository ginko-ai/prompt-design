"""
@startuml
title classDiagram: Strategy Pattern
    class Context {
        -strategy: Strategy
        +setStrategy(Strategy)
        +executeStrategy()
    }
    class Strategy {
        <<interface>>
        +execute()
    }
    class ConcreteStrategyA {
        +execute()
    }
    class ConcreteStrategyB {
        +execute()
    }
    class ConcreteStrategyC {
        +execute()
    }

    Context o-- Strategy
    Strategy <|.. ConcreteStrategyA
    Strategy <|.. ConcreteStrategyB
    Strategy <|.. ConcreteStrategyC
@enduml
"""


"""
@startuml

title Strategy Pattern - Payment Processing Example

package "Payment Strategy Pattern" {
    interface PaymentStrategy {
        + {abstract} pay(amount: float): void
    }

    class CreditCardStrategy {
        - card_number: string
        - expiry: string
        - cvv: string
        + pay(amount: float): void
    }

    class PayPalStrategy {
        - email: string
        + pay(amount: float): void
    }

    class ShoppingCart {
        - payment_strategy: PaymentStrategy
        - items: List<float>
        + set_payment_strategy(strategy: PaymentStrategy): void
        + add_item(price: float): void
        + checkout(): void
    }
}

PaymentStrategy <|.. CreditCardStrategy
PaymentStrategy <|.. PayPalStrategy
ShoppingCart o-> PaymentStrategy

note right of ShoppingCart
  Context class that uses different
  payment strategies interchangeably
end note

note right of PaymentStrategy
  Defines interface for all concrete
  payment strategies
end note
@enduml
"""

from abc import ABC, abstractmethod

class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: float) -> None:
        pass

class CreditCardStrategy(PaymentStrategy):
    def __init__(self, card_number: str, expiry: str, cvv: str):
        self.card_number = card_number
        self.expiry = expiry
        self.cvv = cvv

    def pay(self, amount: float) -> None:
        print(f"Paid ${amount} using Credit Card: {self.card_number}")

class PayPalStrategy(PaymentStrategy):
    def __init__(self, email: str):
        self.email = email

    def pay(self, amount: float) -> None:
        print(f"Paid ${amount} using PayPal account: {self.email}")

class ShoppingCart:
    def __init__(self):
        self.payment_strategy = None
        self.items = []

    def set_payment_strategy(self, strategy: PaymentStrategy):
        self.payment_strategy = strategy

    def add_item(self, price: float):
        self.items.append(price)

    def checkout(self):
        total = sum(self.items)
        if not self.payment_strategy:
            raise ValueError("Payment strategy not set")
        self.payment_strategy.pay(total)

# Usage Example
cart = ShoppingCart()
cart.add_item(100)
cart.add_item(50)

# Pay with credit card
cart.set_payment_strategy(CreditCardStrategy("1234-5678", "12/25", "123"))
cart.checkout()

# Pay with PayPal
cart.set_payment_strategy(PayPalStrategy("user@example.com"))
cart.checkout()