
from abc import ABC, abstractmethod


class UserInterface(ABC):
    @abstractmethod
    def get_input(self):
        pass


class ConsoleUserInterface(UserInterface):
    def get_input(self):
        a = input("Введите сторону A: ")
        b = input("Введите сторону B: ")
        c = input("Введите сторону C: ")
        return a, b, c
