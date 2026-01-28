# -*- coding: utf-8 -*-
from __future__ import annotations
"""
Created on Tue Jan 27 09:31:42 2026

@author: laisz
"""
from abc import abstractmethod, ABC
from dataclasses import dataclass


class UOM(ABC):
    @abstractmethod
    def __str__(self) -> str:
        pass

     
class Page(UOM):
    __instance = None
    
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def __str__(self):
        return "page"
    
   
class Mark(ABC):
    @abstractmethod
    def __lt__(self, other: Mark):   # <
        pass

    @abstractmethod
    def __le__(self, other: Mark):   # <=
        pass

    @abstractmethod
    def __eq__(self, other: Mark):   # ==
        pass
    
    @abstractmethod
    def __ne__(self, other: Mark):   # !=
        pass
    
    @abstractmethod
    def __gt__(self, other: Mark):   # >
        pass
    
    @abstractmethod
    def __ge__(self, other: Mark):   # >=
        pass
    
    @abstractmethod
    def __str__(self) -> str:
        pass
    
    @abstractmethod
    def increment(self) -> Mark:
        pass
    

@dataclass(slots=True)
class Bookmark(Mark):
    index: int
    uom: UOM = Page() 
        

    def __type_check(self, other: Bookmark) -> None:
        if not isinstance(other, self.__class__):
            return NotImplemented
    
        if self.uom is not other.uom:
            raise TypeError(f"Unit of measure mismatch: '{self.uom}' and '{other.uom}'")
            
            
    def __lt__(self, other: Bookmark):   # <
        self.__type_check(other)        
        return self.index < other.index
    

    def __le__(self, other: Bookmark):   # <=
        self.__type_check(other) 
        return self.index <= other.index
    

    def __eq__(self, other: Bookmark):   # ==
        self.__type_check(other) 
        return self.index == other.index
    
    
    def __ne__(self, other: Bookmark):   # !=
        if not isinstance(other, self.__class__):
            return True
        elif self.uom is not other.uom:
            return True
        
        return self.index != other.index
    

    def __gt__(self, other: Bookmark):   # >
        self.__type_check(other) 
        return self.index > other.index
    

    def __ge__(self, other: Bookmark):   # >=
        self.__type_check(other) 
        return self.index >= other.index
    
    def __str__(self) -> str:
        return str(self.index)
    
    def increment(self) -> Bookmark:
        return type(self)(self.index + 1, self.uom)
    
    
    
if __name__ == "__main__":
    mark_1 = Bookmark(5)
    print(mark_1)
    print(mark_1.uom)
    mark_2 = Bookmark(0)
    print(mark_1 < mark_2)