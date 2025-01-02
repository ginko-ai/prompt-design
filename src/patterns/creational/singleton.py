"""
@startuml
title classDiagram: Singleton
    class Singleton {
        -instance: Singleton
        -Singleton()
        +getInstance() Singleton
        +businessLogic()
    }
    Singleton --> Singleton : has single instance

@enduml
"""

"""
@startuml

title Singleton Pattern Documentation

package "Singleton Pattern" {
    class Singleton {
        - static instance: Singleton
        - constructorData: any
        - Singleton()
        + {static} getInstance(): Singleton
        + businessMethod()
    }
}

note right of Singleton
    Purpose:
    Ensures a class has only one instance and provides
    a global point of access to that instance.

    Key Characteristics:
    1. Private constructor
    2. Static instance field
    3. Public static access method
    4. Thread-safety considerations

    Common Use Cases:
    - Database connections
    - Configuration managers
    - Logging services
end note

Singleton --> "1" Singleton : creates/maintains

@enduml
"""

from threading import Lock

class DatabaseConnection:
    _instance = None
    _lock = Lock()

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self._host = "localhost"
            self._port = 5432
            self._connection = None
            self.initialized = True

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = cls()
        return cls._instance

    def connect(self):
        if not self._connection:
            # Simulate database connection
            self._connection = f"Connected to {self._host}:{self._port}"
        return self._connection

# Usage
db1 = DatabaseConnection.get_instance()
db2 = DatabaseConnection.get_instance()
print(db1 is db2)  # True - same instance