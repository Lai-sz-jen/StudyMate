# -*- coding: utf-8 -*-
from __future__ import annotations
"""
Created on Tue Jan 27 09:12:00 2026

@author: laisz
"""
from dataclasses import dataclass
from common.mark import Mark
from common.tree import Node

class RootSplitError(Exception):
    pass

class Unit:
    def __init__(self, title: str, start: Mark, stop: Mark):
        self.__node = Node(UnitInfo(title, start, stop))
        
    @property
    def info(self) -> UnitInfo:
        return self.__node.value

    # Automatically expose UnitInfo attributes (title, start, stop) on the Unit
    def __getattr__(self, name):
        return getattr(self.info, name)
    
    
    def split(self, divide: Mark, title_1: str = None, title_2: str = None):        
        node = self.__node
        info = self.info
        if node.is_root:
            raise RootSplitError("Cannot split when there is no parent unit.")
        elif info.start > divide or info.stop < divide:
            raise ValueError("divide out of range")
        
        index = node.index
        if title_1 is None:
            title_1 = info.title + "-1"
            title_2 = info.title + "-2"
        elif title_2 is None:
            title_2 = title_1
            title_1 = info.title
        
        info_1 = info.copy()
        info_2 = info.copy()
        info_1.stop = divide
        info_1.title = title_1
        divide = divide.increment()
        info_2.start = divide
        info_2.title = title_2
        node.value = info_1
        node.parent.branch(info_2, index + 1)
        
    
    def merge(self, new_title):
        target = self.__node
        info = target.value
        merged = target.parent.get_child(target.index + 1)
        info.stop = merged.value.stop
        info.title = new_title
        target.parent.prune(target.index + 1)
        
        
    def branch(self, title: str, start: Mark, stop: Mark, index: int):
        self.__node.branch(UnitInfo(title, start, stop), index)
        
    def attach(self, unit: Unit) -> None:
        self.__node.attach(unit.__node.value)
    
    def prune(self, index: int) -> Unit:
        node = self.__node.prune(index)
        return self._wrap(node)
        
    def get_child(self, index: int) -> Unit:
        child = self.__node.get_child(index)
        return self._wrap(child)
    
    def get_parent(self) -> Unit:
        parent = self.__node.parent
        return self._wrap(parent)
    
    def flatten(self) -> list(UnitInfo):
        yield from self.__node.get_leaves()
    
    @classmethod
    def from_string(cls, toc: str) -> Unit:
        # TODO
        pass
    
    @classmethod
    def _wrap(cls, node:Node) -> Unit:
        if node is None:
            return None
        instance = cls.__new__(cls)
        instance.__node = node
        return instance
    
    def __eq__(self, unit: object):
        if not isinstance(unit, type(self)):
            return False
        else:
            return self.__node is unit.__node
        
    def __str__(self) -> str:
        def _build_str(node: Node, prefix: str, is_last: bool):
            if is_last:
                connector = "\u2514\u2500\u2500"            # "└──"
                new_prefix = prefix + " " * 6                        # "      "
            else:
                connector = "\u251C\u2500\u2500"            # "├──"
                new_prefix = prefix + "\u2502" + " " * 4    # "│    "
                
            text = f"{prefix}{connector}{node.value}\n"
            
            for i in range(node.size):
                text += _build_str(node[i], new_prefix, i==node.size - 1)
            
            return text

        
        return _build_str(self.__node, "", True)


@dataclass
class UnitInfo:
    title: str
    start: Mark
    stop: Mark
    
    def copy(self) -> UnitInfo:
        return type(self)(self.title, self.start, self.stop)
    
    def __str__(self) -> str:
        return f"{self.title}----{self.start}~{self.stop}"

if __name__ == "__main__":
    from common.mark import Bookmark as mark
    book = Unit("Title", mark(0), mark(100))
    book.branch("Chapter 1", mark(0), mark(50),0)
    book.branch("Chapter 2", mark(51), mark(100),1)
    unit_1 = book.get_child(0)
    unit_1.split(mark(25))
    unit_1.merge("Chapter 1")
    print(book)
    gen = book.flatten()
    for item in gen:
        print(item)
    
    
