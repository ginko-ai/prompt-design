"""
@startuml
title classDiagram: Adaptor Pattern
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
@enduml
"""

"""
@startuml
title Adapter Pattern Structure

participant Client
participant Target
participant Adapter
participant Adaptee

note over Target: <<interface>>
    +request()

note over Adapter
    -adaptee: Adaptee
    +request()
end note

note over Adaptee
    +specificRequest()
end note

Client -> Target: request()
activate Target
Target -> Adapter: request()
activate Adapter
Adapter -> Adaptee: specificRequest()
activate Adaptee
Adaptee --> Adapter: result
deactivate Adaptee
Adapter --> Target: adapted result
deactivate Adapter
Target --> Client: result
deactivate Target

@enduml
"""

from abc import ABC, abstractmethod

class Target(ABC):
    """Interface that client expects"""
    @abstractmethod
    def request(self) -> str:
        pass

class Adaptee:
    """Incompatible interface that needs adapting"""
    def specific_request(self) -> str:
        return "Specific request from Adaptee"

class Adapter(Target):
    """Adapts Adaptee to Target interface"""
    def __init__(self, adaptee: Adaptee):
        self._adaptee = adaptee

    def request(self) -> str:
        # Adapt the incompatible interface
        return f"Adapter: {self._adaptee.specific_request()}"

# Client code
def client_code(target: Target) -> None:
    print(target.request())

# Usage
adaptee = Adaptee()
adapter = Adapter(adaptee)
client_code(adapter)  # Output: "Adapter: Specific request from Adaptee"