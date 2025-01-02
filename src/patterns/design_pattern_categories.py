from abc import ABC, abstractmethod
from typing import List
import asyncio
import threading

# Creational Pattern Example - Abstract Factory
class GUIFactory(ABC):
    @abstractmethod
    def create_button(self): pass

    @abstractmethod
    def create_checkbox(self): pass

# Structural Pattern Example - Adapter
class LegacySystem:
    def old_operation(self) -> str:
        return "Legacy operation"

class ModernInterface(ABC):
    @abstractmethod
    def new_operation(self) -> str: pass

class Adapter(ModernInterface):
    def __init__(self, legacy: LegacySystem):
        self._legacy = legacy

    def new_operation(self) -> str:
        return self._legacy.old_operation()

# Behavioral Pattern Example - Observer
class Subject:
    def __init__(self):
        self._observers: List = []
        self._state = None

    def attach(self, observer) -> None:
        self._observers.append(observer)

    def notify(self) -> None:
        for observer in self._observers:
            observer.update(self._state)

# Concurrency Pattern Example - Active Object
class ActiveObject:
    def __init__(self):
        self._loop = asyncio.new_event_loop()
        self._thread = threading.Thread(target=self._run_loop)
        self._thread.start()

    async def async_operation(self):
        await asyncio.sleep(1)
        return "Operation complete"

    def _run_loop(self):
        asyncio.set_event_loop(self._loop)
        self._loop.run_forever()