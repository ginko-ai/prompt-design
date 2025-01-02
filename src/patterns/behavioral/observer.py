"""
@startuml
title classDiagram: Observer Pattern
    class Subject {
        <<interface>>
        -observers: List
        +attach(observer)
        +detach(observer)
        +notify()
    }
    class Observer {
        <<interface>>
        +update(subject)
    }
    class ConcreteSubject {
        -state
        +getState()
        +setState(state)
    }
    class ConcreteObserver {
        -observerState
        +update(subject)
    }
    Subject <|-- ConcreteSubject
    Observer <|-- ConcreteObserver
    Subject ..> Observer
    ConcreteObserver ..> ConcreteSubject
@enduml
"""

"""
@startuml
title Observer Pattern - Detailed Design

package "Observer Pattern Core" {
    interface Subject {
        + attach(observer: Observer)
        + detach(observer: Observer)
        + notify()
        .. State ..
        - observers: List<Observer>
    }

    interface Observer {
        + update(subject: Subject)
    }

    class NewsAgency {
        - observers: List<Observer>
        - latest_news: str
        + attach(observer: Observer)
        + detach(observer: Observer)
        + notify()
        + get_latest_news(): str
        + set_latest_news(news: str)
    }

    class NewsChannel {
        - name: str
        - news: str
        + update(subject: Subject)
    }

    Subject <|.. NewsAgency
    Observer <|.. NewsChannel
    NewsAgency o-- Observer
}

note right of Subject
    Maintains list of observers and
    notifies them of state changes
end note

note right of Observer
    Defines interface for objects
    that should be notified of changes
end note

note right of NewsAgency
    Concrete implementation that
    broadcasts news updates to channels
end note

note right of NewsChannel
    Concrete observer that receives
    and displays news updates
end note

@enduml
"""



from abc import ABC, abstractmethod
from typing import List

class Observer(ABC):
    """
    Observer interface declaring the update method used by subjects.
    """
    @abstractmethod
    def update(self, subject: 'Subject') -> None:
        pass

class Subject(ABC):
    """
    Subject interface declaring operations for attaching and detaching observers.
    """
    @abstractmethod
    def attach(self, observer: Observer) -> None:
        pass

    @abstractmethod
    def detach(self, observer: Observer) -> None:
        pass

    @abstractmethod
    def notify(self) -> None:
        pass

class NewsAgency(Subject):
    """
    Concrete subject that sends notifications to observers when news changes.
    """
    def __init__(self):
        self._observers: List[Observer] = []
        self._latest_news: str = ""

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self) -> None:
        for observer in self._observers:
            observer.update(self)

    @property
    def latest_news(self) -> str:
        return self._latest_news

    @latest_news.setter
    def latest_news(self, news: str) -> None:
        self._latest_news = news
        self.notify()

class NewsChannel(Observer):
    """
    Concrete observer that reacts to updates from the news agency.
    """
    def __init__(self, name: str):
        self.name = name
        self.news = ""

    def update(self, subject: NewsAgency) -> None:
        self.news = subject.latest_news
        print(f"{self.name} received news: {self.news}")

# Example usage
if __name__ == "__main__":
    news_agency = NewsAgency()

    channel1 = NewsChannel("CNN")
    channel2 = NewsChannel("BBC")

    news_agency.attach(channel1)
    news_agency.attach(channel2)

    news_agency.latest_news = "Breaking: Major tech breakthrough!"