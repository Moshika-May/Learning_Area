from abc import ABC, abstractmethod

class Base(ABC):
    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def draw(self):
        pass

class A(Base):
    def update(self):
        pass

    def draw(self):
        pass

print(Base.__abstractmethods__)
print(A.__abstractmethods__)
obj = Base()
