
from abc import ABC, abstractmethod

class AccountHandlerInterace(ABC):
    
    @abstractmethod
    def register_user(self, name, email):
        pass

    @abstractmethod
    def login_user(self, name, email):
        pass 

    @abstractmethod
    def get_users(self):
        pass

    @abstractmethod
    def create_tables(self):
        pass